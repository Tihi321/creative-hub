# Starts, stops and checks every tool in the creative hub (see ..\services.json).
# Run it before a production run, or whenever an MCP server in .mcp.json fails to connect.
# Rerunnable; needs no admin rights. Managed engines are started detached (no inherited handles, so piping
# `start` into tail/cat returns) and append to ..\logs\<id>.out.log / .err.log.
#
#   pwsh -File scripts\hub.ps1                      status of every service
#   pwsh -File scripts\hub.ps1 start                start the default set (not scriptorium, not strata)
#   pwsh -File scripts\hub.ps1 start vn-studio pixel-studio
#   pwsh -File scripts\hub.ps1 start strata deepseek   a service with variants takes the variant after its id (default: defaultVariant)
#   pwsh -File scripts\hub.ps1 variants [service]  list the variants (bat files) of services that have them, and the default
#   pwsh -File scripts\hub.ps1 start scriptorium -Force   (Scriptorium resumes its factory, see services.json)
#   pwsh -File scripts\hub.ps1 start scriptorium -Force -Window   with its window (Electron apps only), MCP still on
#   pwsh -File scripts\hub.ps1 stop [ids|all]       stops hub-managed engines only (-Force for the rest; also closes the leftover holder of an `orphan` port)
#   pwsh -File scripts\hub.ps1 build [ids]          rebuild repos after pulling or editing them
#   pwsh -File scripts\hub.ps1 logs vn-studio
#   pwsh -File scripts\hub.ps1 check [ids]          MCP handshake + tool count for each running server
#   pwsh -File scripts\hub.ps1 call vn-studio vno_status '{"slug":"x"}'   call one tool (when Claude's MCP link is down);
#                                                   args may also be @path\to\args.json
#   pwsh -File scripts\hub.ps1 setup [-EnableVibeTts]  one-time: Book Translator token, VibeTTS MCP

param(
    [Parameter(Position = 0)][ValidateSet('status', 'start', 'stop', 'build', 'logs', 'setup', 'check', 'call', 'variants')][string]$Command = 'status',
    [Parameter(Position = 1, ValueFromRemainingArguments)][string[]]$Ids,
    [switch]$Force,
    [switch]$Window,
    [switch]$EnableVibeTts,
    [int]$WaitSeconds = 60
)

$ErrorActionPreference = 'Stop'
# Tool results carry any language: print UTF-8, or the console code page turns "š" into "s" and „…” into quotes that break the JSON.
[Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
$OutputEncoding = [Text.UTF8Encoding]::new($false)
$hub = Split-Path $PSScriptRoot -Parent
$logs = Join-Path $hub 'logs'
$registry = Get-Content (Join-Path $hub 'services.json') -Raw | ConvertFrom-Json
$services = $registry.services

function Expand([string]$p) { if ($p) { $p -replace '^~', $HOME } }

# Variant picked on the command line per service id (hub.ps1 start strata deepseek).
$script:Variants = @{}

function Select-Services([string[]]$ids, [bool]$defaultsOnly) {
    if (-not $ids -or $ids.Count -eq 0) {
        if ($defaultsOnly) { return $services | Where-Object default }
        return $services
    }
    if ($ids -contains 'all') { return $services }
    $prev = $null
    foreach ($id in $ids) {
        $s = $services | Where-Object id -EQ $id
        if (-not $s -and $prev -and $prev.variants) {
            $names = @($prev.variants.PSObject.Properties.Name)
            if ($names -notcontains $id) {
                Write-Host "Unknown variant '$id' for '$($prev.id)'. Run: hub.ps1 variants $($prev.id)" -ForegroundColor Yellow
                Write-Host "Variants: $($names -join ', ') (default: $($prev.defaultVariant))" -ForegroundColor Yellow
                exit 1
            }
            $script:Variants[$prev.id] = $id
            continue
        }
        if (-not $s) { throw "Unknown service '$id'. Known: $($services.id -join ', ')" }
        $prev = $s
        $s
    }
}

function Show-Variants([string[]]$ids) {
    $withVariants = @($services | Where-Object variants)
    $pick = $withVariants
    if ($ids -and $ids.Count -gt 0) {
        $pick = @($withVariants | Where-Object { $ids -contains $_.id })
        if ($pick.Count -ne $ids.Count) {
            Write-Host "No variants for '$($ids -join ', ')'. Services with variants: $($withVariants.id -join ', ')" -ForegroundColor Yellow
            exit 1
        }
    }
    $rows = foreach ($s in $pick) {
        foreach ($p in $s.variants.PSObject.Properties) {
            [pscustomobject]@{
                Service = $s.id
                Variant = $p.Name
                'Bat file' = Expand $p.Value
                Default = if ($p.Name -eq $s.defaultVariant) { 'default' } else { '' }
                Exists  = if (Test-Path (Expand $p.Value)) { 'yes' } else { 'MISSING' }
            }
        }
    }
    $rows | Format-Table -AutoSize | Out-String -Width 250 | Write-Host
}

# The listener on $port. Get-NetTCPConnection returns nothing at times (and in sandboxed shells it never sees listeners), so when
# it finds none a TCP connect to 127.0.0.1:$port decides; such a listener has OwningProcess 0 and Get-Owner looks for the owner.
function Get-Listener([int]$port) {
    $l = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($l) { return $l }
    $c = [Net.Sockets.TcpClient]::new()
    try {
        $t = $c.ConnectAsync('127.0.0.1', $port)
        if ($t.Wait(400) -and $c.Connected) { return [pscustomobject]@{ LocalPort = $port; OwningProcess = 0 } }
    }
    catch { }
    finally { $c.Dispose() }
    $null
}

# True when the service's health URL answers with any HTTP response (services with only an MCP url have none: false).
function Test-Health($s) {
    if (-not $s.http) { return $false }
    try { Invoke-WebRequest -Uri $s.http -TimeoutSec 3 -UseBasicParsing -SkipHttpErrorCheck | Out-Null; $true } catch { $false }
}

# Who holds the port of service $s with listener $l. Windows may report OwningProcess 0 (or a dead pid) for a listener whose
# socket was inherited by a child, so a pid of 0 alone does not mean the service is gone. Returns Kind:
#   live   - the owning pid exists (Pid, Name)
#   owner  - owner is 0/dead but processes run under the service's folder; Pid/Name = topmost ancestor under that folder
#   up     - owner is 0/dead and nothing is found under the folder, but the health URL answers (owner unknown)
#   orphan - owner is 0/dead, nothing under the folder and no health answer. Holders are GUESSES: processes whose command
#            line mentions 127.0.0.1:<port> or localhost:<port> (never this script's own shell).
function Get-Owner($s, $listener) {
    if (-not $listener) { return $null }
    $op = [int]$listener.OwningProcess
    if ($op -ne 0) {
        $p = Get-Process -Id $op -ErrorAction SilentlyContinue
        if ($p) { return [pscustomobject]@{ Kind = 'live'; Pid = $op; Name = $p.ProcessName; Holders = @() } }
    }
    $all = @(Get-CimInstance Win32_Process -ErrorAction SilentlyContinue)
    $path = if ($s.start -and $s.start.path) { Expand $s.start.path } else { $null }
    $folder = if ($path) { Split-Path $path } elseif ($s.repo) { Expand $s.repo } else { $null }
    $shell = '^(bash|sh|cmd|pwsh|powershell|conhost)(\.exe)?$'
    # A service this script started runs under a cmd.exe whose command line names its log file (Start-Detached); a `node out/...`
    # command line names no folder, so this is how such an owner is found. taskkill /T on that cmd.exe takes fnm and node with it.
    $logMark = (Join-Path $logs "$($s.id).out.log")
    $started = @($all | Where-Object { $_.ProcessId -ne $PID -and $_.Name -eq 'cmd.exe' -and $_.CommandLine -and $_.CommandLine.IndexOf($logMark, [StringComparison]::OrdinalIgnoreCase) -ge 0 })
    if ($started.Count) {
        $t = $started[0]
        $leaf = $t
        while ($next = $all | Where-Object { $_.ParentProcessId -eq $leaf.ProcessId -and $_.Name -ne 'conhost.exe' } | Select-Object -First 1) { $leaf = $next }
        return [pscustomobject]@{ Kind = 'owner'; Pid = [int]$t.ProcessId; Name = [IO.Path]::GetFileNameWithoutExtension($leaf.Name); Holders = @() }
    }
    if ($folder) {
        $f = $folder.TrimEnd('\') + '\'
        $under = @($all | Where-Object {
            $_.ProcessId -ne $PID -and $_.Name -notmatch $shell -and
            (($_.ExecutablePath -and $_.ExecutablePath.StartsWith($f, [StringComparison]::OrdinalIgnoreCase)) -or
             ($_.CommandLine -and $_.CommandLine.IndexOf($f, [StringComparison]::OrdinalIgnoreCase) -ge 0))
        })
        if ($under.Count) {
            $ids = @($under.ProcessId)
            $tops = @($under | Where-Object { $ids -notcontains $_.ParentProcessId })
            $t = $tops[0]
            return [pscustomobject]@{ Kind = 'owner'; Pid = [int]$t.ProcessId; Name = [IO.Path]::GetFileNameWithoutExtension($t.Name); Holders = @() }
        }
    }
    if (Test-Health $s) { return [pscustomobject]@{ Kind = 'up'; Pid = $null; Name = 'unknown'; Holders = @() } }
    $port = $s.port
    $holders = @($all | Where-Object {
        $_.CommandLine -and $_.ProcessId -ne $PID -and $_.Name -notmatch $shell -and
        ($_.CommandLine -match "(127\.0\.0\.1|localhost):$port(?!\d)")
    } | ForEach-Object { [pscustomobject]@{ Name = [IO.Path]::GetFileNameWithoutExtension($_.Name); Pid = [int]$_.ProcessId } })
    [pscustomobject]@{ Kind = 'orphan'; Pid = $null; Name = 'unknown'; Holders = $holders }
}

function Get-OrphanText($s, $orphan) {
    $h = @($orphan.Holders)
    $who = if ($h.Count -eq 0) { 'an unknown holder' } else { 'likely held by ' + (($h | ForEach-Object { "$($_.Name) (pid $($_.Pid))" }) -join ', ') + ' (a guess)' }
    if ($h.Count -eq 0) { "$($s.id): port $($s.port) is held by $who, left over from a process that has exited." }
    else { "$($s.id): port $($s.port) is $who, left over from a process that has exited." }
}

function Get-BtToken {
    $t = $env:BOOK_TRANSLATOR_MCP_TOKEN
    if (-not $t) { $t = [Environment]::GetEnvironmentVariable('BOOK_TRANSLATOR_MCP_TOKEN', 'User') }
    $t
}

# The model a service reports in its health answer (Strata: /health has `model` and `loaded`); empty when it has none.
function Get-HealthModel([string]$url) {
    try {
        $h = Invoke-RestMethod -Uri $url -TimeoutSec 3
        if ($h.model) { if ($h.PSObject.Properties.Name -contains 'loaded' -and -not $h.loaded) { "$($h.model) (loading)" } else { [string]$h.model } }
    }
    catch { '' }
}

function Show-Status {
    $rows = foreach ($s in $services) {
        $l = Get-Listener $s.port
        $o = Get-Owner $s $l
        $orphan = $o -and $o.Kind -eq 'orphan'
        $h = if ($orphan) { @($o.Holders) } else { @() }
        $proc = if ($orphan) { if ($h.Count -ge 1) { ($h.Name | Select-Object -Unique) -join ',' } else { 'unknown' } }
                elseif ($o) { $o.Name } else { '' }
        [pscustomobject]@{
            Service = $s.id
            State   = if ($orphan) { 'orphan' } elseif ($l) { 'up' } else { 'down' }
            Port    = $s.port
            Pid     = if ($orphan) { if ($h.Count -eq 1) { $h[0].Pid } else { '' } } elseif ($o -and $o.Pid) { $o.Pid } else { '' }
            Process = $proc
            Url     = if ($s.mcp) { $s.mcp } else { $s.http }
            Model   = if ($l -and $s.http) { Get-HealthModel $s.http } else { '' }
        }
    }
    $rows | Format-Table -AutoSize | Out-String -Width 200 | Write-Host
    $vt = 'D:\Programs\VibeTTS\config.toml'
    if ((Test-Path $vt) -and (Select-String -Path $vt -Pattern '^\s*enabled\s*=\s*false' -Quiet)) {
        Write-Host "Note: VibeTTS MCP is disabled in $vt. Run: hub.ps1 setup -EnableVibeTts" -ForegroundColor Yellow
    }
    if (-not (Get-BtToken)) {
        Write-Host 'Note: BOOK_TRANSLATOR_MCP_TOKEN is not set. Run: hub.ps1 setup' -ForegroundColor Yellow
    }
}

# Starts a process that inherits no handles from this one (Start-Process with redirected output does, so a piped
# `hub.ps1 start ... | tail` never saw EOF). WMI creates it outside our process tree; cmd.exe appends its output to the logs.
function Start-Detached([string]$exe, [string[]]$argList, [string]$workDir, [string]$outLog, [string]$errLog, [hashtable]$extraEnv, [bool]$visible) {
    $line = "cmd.exe /d /c `"`"$exe`" $($argList -join ' ') 1>>`"$outLog`" 2>>`"$errLog`"`""
    $vars = @{}
    foreach ($e in [Environment]::GetEnvironmentVariables().GetEnumerator()) { $vars[[string]$e.Key] = [string]$e.Value }
    # An agent session may export ELECTRON_RUN_AS_NODE=1 (the harness itself runs on Electron): an Electron app started with it
    # runs as plain Node and crashes (e.g. Scriptorium's main process has no `electron`). Never pass it to an Electron app.
    if ($exe -match 'electron(\.exe)?$') { $vars.Remove('ELECTRON_RUN_AS_NODE') }
    foreach ($k in $extraEnv.Keys) { $vars[$k] = [string]$extraEnv[$k] }
    $startup = New-CimInstance -ClassName Win32_ProcessStartup -ClientOnly -Property @{
        ShowWindow           = [uint16]$(if ($visible) { 1 } else { 0 })
        EnvironmentVariables = [string[]]@($vars.GetEnumerator() | ForEach-Object { "$($_.Key)=$($_.Value)" })
    }
    $r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{
        CommandLine = $line; CurrentDirectory = $workDir; ProcessStartupInformation = $startup }
    if ($r.ReturnValue -ne 0) { throw "Could not start $exe (WMI Win32_Process.Create returned $($r.ReturnValue))" }
    [int]$r.ProcessId
}

function Start-Service1($s) {
    $l0 = Get-Listener $s.port
    if ($l0) {
        $orphan = Get-Owner $s $l0
        if ($orphan.Kind -eq 'orphan') {
            $h = @($orphan.Holders)
            $fix = if ($h.Count -eq 1) { "Close $($h[0].Name) if that is right, or run: hub.ps1 stop $($s.id) -Force" } else { "Close it, or run: hub.ps1 stop $($s.id) -Force" }
            Write-Host "$(Get-OrphanText $s $orphan) $fix" -ForegroundColor Yellow
        }
        else { Write-Host "$($s.id): already up on $($s.port)" }
        return
    }
    if ($s.warning -and -not $Force) {
        Write-Host "$($s.id): skipped. $($s.warning) Add -Force to start it." -ForegroundColor Yellow
        return
    }
    $st = $s.start
    if ($s.variants) {
        $v = if ($script:Variants.ContainsKey($s.id)) { $script:Variants[$s.id] } else { $s.defaultVariant }
        $vp = $s.variants.$v
        if (-not $vp) { throw "$($s.id): no variant '$v'. Variants: $(@($s.variants.PSObject.Properties.Name) -join ', ')" }
        $st = [pscustomobject]@{ kind = $st.kind; path = $vp; args = $st.args }
        Write-Host "$($s.id): variant $v"
    }
    $repo = if ($st.cwd) { Expand $st.cwd } else { $s.repo }
    $args2 = @($st.args | ForEach-Object { Expand $_ })
    $showWindow = $false
    if ($Window) {
        if ($st.kind -eq 'electron') {
            # Windowed start: drop the headless flags, keep the MCP server on.
            $showWindow = $true
            $args2 = @($args2 | Where-Object { $_ -notin '--headless', '--mcp-only' })
            if ($args2 -notcontains '--mcp') { $args2 += '--mcp' }
        }
        else { Write-Host "$($s.id): -Window has no effect (only Electron apps get a window)" }
    }
    switch ($st.kind) {
        'node' {
            if (-not (Test-Path (Join-Path $repo $args2[0]))) { throw "$($s.id): $($args2[0]) is missing. Run: hub.ps1 build $($s.id)" }
            $exe = 'fnm'; $args2 = @('exec', '--using=24', 'node') + $args2
        }
        'electron' {
            $exe = Join-Path $repo 'node_modules\electron\dist\electron.exe'
            if (-not (Test-Path (Join-Path $repo 'out'))) { throw "$($s.id): out\ is missing. Run: hub.ps1 build $($s.id)" }
        }
        'exe' { $exe = Expand $st.path }
        'console' {
            Start-Process -FilePath 'cmd.exe' -ArgumentList '/k', "`"$(Expand $st.path)`"" -WorkingDirectory (Split-Path (Expand $st.path))
            Write-Host "$($s.id): started in its own console window"
            $exe = $null
        }
    }
    if ($exe) {
        # Start-Process joins arguments with spaces and does not quote them.
        $args2 = @($args2 | ForEach-Object { if ($_ -match '\s') { "`"$_`"" } else { $_ } })
        if ($s.managed) {
            New-Item -ItemType Directory -Force $logs | Out-Null
            $env2 = @{}
            if ($st.env) { $st.env.PSObject.Properties | ForEach-Object { $env2[$_.Name] = $_.Value } }
            if ($s.id -eq 'book-translator') {
                $tok = Get-BtToken
                if (-not $tok) { throw 'book-translator: BOOK_TRANSLATOR_MCP_TOKEN is not set. Run: hub.ps1 setup' }
                $env2['BOOK_TRANSLATOR_MCP_TOKEN'] = $tok
            }
            $procId = Start-Detached $exe $args2 $repo (Join-Path $logs "$($s.id).out.log") (Join-Path $logs "$($s.id).err.log") $env2 $showWindow
            Write-Host "$($s.id): started (pid $procId), waiting for port $($s.port)..."
        }
        else {
            Start-Process -FilePath $exe -ArgumentList $args2 | Out-Null
            Write-Host "$($s.id): launched $exe, waiting for port $($s.port)..."
        }
    }
    $wait = [Math]::Max($WaitSeconds, [int]$s.startTimeout)
    $deadline = (Get-Date).AddSeconds($wait)
    while ((Get-Date) -lt $deadline) {
        if (Get-Listener $s.port) { Write-Host "$($s.id): up at $(if ($s.mcp) { $s.mcp } else { $s.http })" -ForegroundColor Green; return }
        Start-Sleep -Milliseconds 500
    }
    Write-Host "$($s.id): not listening after $wait s. Check: hub.ps1 logs $($s.id)" -ForegroundColor Red
}

function Stop-Service1($s) {
    $l = Get-Listener $s.port
    if (-not $l) { Write-Host "$($s.id): not running"; return }
    $o = Get-Owner $s $l
    if ($o.Kind -eq 'up') {
        Write-Host "$($s.id): port $($s.port) answers but its owner process could not be found. Try: netstat -ano | findstr :$($s.port)" -ForegroundColor Yellow
        return
    }
    $orphan = if ($o.Kind -eq 'orphan') { $o } else { $null }
    if ($orphan) {
        $h = @($orphan.Holders)
        Write-Host (Get-OrphanText $s $orphan) -ForegroundColor Yellow
        if (-not $Force) {
            if ($h.Count) { Write-Host "Add -Force to close $(($h | ForEach-Object { "$($_.Name) (pid $($_.Pid))" }) -join ', ') (a guess, check it first)." -ForegroundColor Yellow }
            else { Write-Host "Could not find the holder. Try: netstat -ano | findstr :$($s.port)" -ForegroundColor Yellow }
            return
        }
        if (-not $h.Count) { Write-Host "$($s.id): could not find the holder. Try: netstat -ano | findstr :$($s.port)" -ForegroundColor Yellow; return }
        foreach ($c in $h) { & taskkill.exe /PID $c.Pid /T /F | Out-Null; Write-Host "$($s.id): closed $($c.Name) (pid $($c.Pid))" }
        Start-Sleep -Seconds 1
        if (Get-Listener $s.port) { Write-Host "$($s.id): port $($s.port) is still held." -ForegroundColor Yellow } else { Write-Host "$($s.id): port $($s.port) is free." -ForegroundColor Green }
        return
    }
    if (-not $s.managed -and -not $Force) { Write-Host "$($s.id): not hub-managed (your app), left running. Add -Force to stop it."; return }
    # Electron listens from a child (utility) process: kill the top process of the same program, or the main one lives on.
    # When Windows reports owner 0, $o.Pid is the topmost process under the service's folder (taskkill /T takes its children).
    $ownerId = $o.Pid
    $root = Get-CimInstance Win32_Process -Filter "ProcessId=$ownerId"
    while ($o.Kind -eq 'live' -and $root) {
        $parent = Get-CimInstance Win32_Process -Filter "ProcessId=$($root.ParentProcessId)"
        if (-not $parent -or $parent.Name -ne $root.Name) { break }
        $root = $parent
    }
    $rootId = if ($root) { $root.ProcessId } else { $ownerId }
    & taskkill.exe /PID $rootId /T /F | Out-Null
    Write-Host "$($s.id): stopped (pid $rootId)"
}

function Build-Service1($s) {
    if (-not $s.build) { Write-Host "$($s.id): nothing to build"; return }
    Write-Host "$($s.id): $($s.build) in $($s.repo)"
    Push-Location $s.repo
    try { & fnm exec --using=24 cmd /c $s.build; if ($LASTEXITCODE) { throw "$($s.id): build failed ($LASTEXITCODE)" } }
    finally { Pop-Location }
}

function Invoke-Mcp([string]$url, [hashtable]$headers, [object]$body, [int]$timeoutSec = 15) {
    $h = @{ Accept = 'application/json, text/event-stream' } + $headers
    $r = Invoke-WebRequest -Uri $url -Method Post -ContentType 'application/json' -Headers $h -Body ($body | ConvertTo-Json -Depth 100 -Compress) -TimeoutSec $timeoutSec -SkipHttpErrorCheck
    if ($r.StatusCode -ge 400) { throw "HTTP $($r.StatusCode): $($r.Content)" }
    $text = if ($r.Content -is [byte[]]) { [Text.Encoding]::UTF8.GetString($r.Content) } else { [string]$r.Content }
    # Streamable HTTP answers with JSON or with an SSE stream whose data lines hold the JSON.
    $json = if ($text.TrimStart().StartsWith('{')) { $text } else { (($text -split "`n") | Where-Object { $_ -like 'data:*' } | Select-Object -Last 1) -replace '^data:\s*', '' }
    [pscustomobject]@{ Session = $r.Headers['mcp-session-id'] | Select-Object -First 1; Body = if ($json) { $json | ConvertFrom-Json } else { $null } }
}

function Open-Mcp($s) {
    $h = @{}
    if ($s.id -eq 'book-translator') { $h.Authorization = "Bearer $(Get-BtToken)" }
    $init = Invoke-Mcp $s.mcp $h @{ jsonrpc = '2.0'; id = 1; method = 'initialize'; params = @{ protocolVersion = '2025-06-18'; capabilities = @{}; clientInfo = @{ name = 'creative-hub'; version = '1' } } }
    if ($init.Session) { $h['mcp-session-id'] = $init.Session }
    Invoke-Mcp $s.mcp $h @{ jsonrpc = '2.0'; method = 'notifications/initialized' } | Out-Null
    [pscustomobject]@{ Headers = $h; Init = $init }
}

# Calls one MCP tool without a Claude MCP connection: hub.ps1 call <id> <tool> ['<json args>']
function Invoke-Tool([string[]]$a) {
    if ($a.Count -lt 2) { throw "Usage: hub.ps1 call <service> <tool> ['{json args}']" }
    $s = Select-Services @($a[0]) $false
    $raw = if ($a.Count -ge 3) { if ($a[2].StartsWith('@')) { Get-Content $a[2].Substring(1) -Raw } else { $a[2] } } else { '{}' }
    $toolArgs = $raw | ConvertFrom-Json -AsHashtable
    $c = Open-Mcp $s
    # a tool call may render for minutes (comfy-mcp waits up to 600 s), so it gets a long timeout
    $r = Invoke-Mcp $s.mcp $c.Headers @{ jsonrpc = '2.0'; id = 3; method = 'tools/call'; params = @{ name = $a[1]; arguments = $toolArgs } } 660
    if ($r.Body.error) { Write-Host "error: $($r.Body.error.message)" -ForegroundColor Red; exit 1 }
    $res = $r.Body.result
    if ($res.structuredContent) { $res.structuredContent | ConvertTo-Json -Depth 20 }
    else { $res.content | Where-Object type -EQ 'text' | ForEach-Object text }
    if ($res.isError) { exit 1 }
}

function Test-Mcp($s) {
    if (-not $s.mcp) { return }
    if (-not (Get-Listener $s.port)) { Write-Host "$($s.id): down"; return }
    try {
        $c = Open-Mcp $s; $h = $c.Headers; $init = $c.Init
        $list = Invoke-Mcp $s.mcp $h @{ jsonrpc = '2.0'; id = 2; method = 'tools/list' }
        $tools = $list.Body.result.tools.name
        Write-Host "$($s.id): OK, $($init.Body.result.serverInfo.name) $($init.Body.result.serverInfo.version), $($tools.Count) tools" -ForegroundColor Green
    }
    catch { Write-Host "$($s.id): MCP error: $($_.Exception.Message)" -ForegroundColor Red }
}

function Invoke-Setup {
    if (-not (Get-BtToken)) {
        $bytes = [byte[]]::new(32); [Security.Cryptography.RandomNumberGenerator]::Fill($bytes)
        $tok = [Convert]::ToHexString($bytes).ToLower()
        [Environment]::SetEnvironmentVariable('BOOK_TRANSLATOR_MCP_TOKEN', $tok, 'User')
        $env:BOOK_TRANSLATOR_MCP_TOKEN = $tok
        Write-Host 'Set user env var BOOK_TRANSLATOR_MCP_TOKEN (restart Claude Code so .mcp.json can use it).'
    }
    else { Write-Host 'BOOK_TRANSLATOR_MCP_TOKEN already set.' }

    $vt = 'D:\Programs\VibeTTS\config.toml'
    if ($EnableVibeTts -and (Test-Path $vt)) {
        $text = Get-Content $vt -Raw
        if ($text -match '(?ms)^\[mcp\]\s*\r?\nenabled\s*=\s*false') {
            # VibeTTS rewrites config.toml when it saves settings, so stop it before editing.
            $running = Get-Process VibeTTS -ErrorAction SilentlyContinue
            if ($running) { $running | Stop-Process -Force; Start-Sleep 2 }
            $text = $text -replace '(?ms)(^\[mcp\]\s*\r?\nenabled\s*=\s*)false', '${1}true'
            Set-Content -Path $vt -Value $text -NoNewline
            Start-Process 'D:\Programs\VibeTTS\VibeTTS.exe' -ArgumentList '--hidden'
            Write-Host 'VibeTTS: MCP enabled and app restarted (http://127.0.0.1:7723/mcp).'
        }
        else { Write-Host 'VibeTTS: MCP already enabled.' }
    }
}

switch ($Command) {
    'status' { Show-Status }
    'start' { foreach ($s in Select-Services $Ids $true) { Start-Service1 $s }; Show-Status }
    'stop' { foreach ($s in Select-Services $Ids $false) { Stop-Service1 $s } }
    'build' { foreach ($s in Select-Services $Ids $false) { Build-Service1 $s } }
    'logs' {
        foreach ($s in Select-Services $Ids $false) {
            foreach ($f in "$($s.id).out.log", "$($s.id).err.log") {
                $path = Join-Path $logs $f
                if (Test-Path $path) { Write-Host "== $f"; Get-Content $path -Tail 40 }
            }
        }
    }
    'variants' { Show-Variants $Ids }
    'setup' { Invoke-Setup }
    'check' { foreach ($s in Select-Services $Ids $false) { Test-Mcp $s } }
    'call' { Invoke-Tool $Ids }
}
