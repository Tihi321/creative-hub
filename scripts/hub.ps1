# Starts, stops and checks every tool in the creative hub (see ..\services.json).
# Run it before a production run, or whenever an MCP server in .mcp.json fails to connect.
# Rerunnable; needs no admin rights. Headless engines log to ..\logs\<id>.out.log / .err.log.
#
#   pwsh -File scripts\hub.ps1                      status of every service
#   pwsh -File scripts\hub.ps1 start                start the default set (not scriptorium, not strata)
#   pwsh -File scripts\hub.ps1 start vn-studio pixel-studio
#   pwsh -File scripts\hub.ps1 start scriptorium -Force   (Scriptorium resumes its factory, see services.json)
#   pwsh -File scripts\hub.ps1 stop [ids|all]       stops hub-managed engines only (-Force for the rest)
#   pwsh -File scripts\hub.ps1 build [ids]          rebuild repos after pulling or editing them
#   pwsh -File scripts\hub.ps1 logs vn-studio
#   pwsh -File scripts\hub.ps1 check [ids]          MCP handshake + tool count for each running server
#   pwsh -File scripts\hub.ps1 call vn-studio vno_status '{"slug":"x"}'   call one tool (when Claude's MCP link is down);
#                                                   args may also be @path\to\args.json
#   pwsh -File scripts\hub.ps1 setup [-EnableVibeTts]  one-time: Book Translator token, VibeTTS MCP

param(
    [Parameter(Position = 0)][ValidateSet('status', 'start', 'stop', 'build', 'logs', 'setup', 'check', 'call')][string]$Command = 'status',
    [Parameter(Position = 1, ValueFromRemainingArguments)][string[]]$Ids,
    [switch]$Force,
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

function Select-Services([string[]]$ids, [bool]$defaultsOnly) {
    if (-not $ids -or $ids.Count -eq 0) {
        if ($defaultsOnly) { return $services | Where-Object default }
        return $services
    }
    if ($ids -contains 'all') { return $services }
    foreach ($id in $ids) {
        $s = $services | Where-Object id -EQ $id
        if (-not $s) { throw "Unknown service '$id'. Known: $($services.id -join ', ')" }
        $s
    }
}

function Get-Listener([int]$port) {
    Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
}

function Get-BtToken {
    $t = $env:BOOK_TRANSLATOR_MCP_TOKEN
    if (-not $t) { $t = [Environment]::GetEnvironmentVariable('BOOK_TRANSLATOR_MCP_TOKEN', 'User') }
    $t
}

function Show-Status {
    $rows = foreach ($s in $services) {
        $l = Get-Listener $s.port
        $proc = if ($l) { (Get-Process -Id $l.OwningProcess -ErrorAction SilentlyContinue).ProcessName } else { '' }
        [pscustomobject]@{
            Service = $s.id
            State   = if ($l) { 'up' } else { 'down' }
            Port    = $s.port
            Pid     = if ($l) { $l.OwningProcess } else { '' }
            Process = $proc
            Url     = if ($s.mcp) { $s.mcp } else { $s.http }
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

function Start-Service1($s) {
    if (Get-Listener $s.port) { Write-Host "$($s.id): already up on $($s.port)"; return }
    if ($s.warning -and -not $Force) {
        Write-Host "$($s.id): skipped. $($s.warning) Add -Force to start it." -ForegroundColor Yellow
        return
    }
    $st = $s.start
    $repo = if ($st.cwd) { Expand $st.cwd } else { $s.repo }
    $args2 = @($st.args | ForEach-Object { Expand $_ })
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
            $p = @{
                FilePath               = $exe
                ArgumentList           = $args2
                WorkingDirectory       = $repo
                WindowStyle            = 'Hidden'
                RedirectStandardOutput = Join-Path $logs "$($s.id).out.log"
                RedirectStandardError  = Join-Path $logs "$($s.id).err.log"
                PassThru               = $true
            }
            if ($env2.Count) { $p.Environment = $env2 }
            $proc = Start-Process @p
            Write-Host "$($s.id): started (pid $($proc.Id)), waiting for port $($s.port)..."
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
    if (-not $s.managed -and -not $Force) { Write-Host "$($s.id): not hub-managed (your app), left running. Add -Force to stop it."; return }
    # Electron listens from a child (utility) process: kill the top process of the same program, or the main one lives on.
    $root = Get-CimInstance Win32_Process -Filter "ProcessId=$($l.OwningProcess)"
    while ($root) {
        $parent = Get-CimInstance Win32_Process -Filter "ProcessId=$($root.ParentProcessId)"
        if (-not $parent -or $parent.Name -ne $root.Name) { break }
        $root = $parent
    }
    $rootId = if ($root) { $root.ProcessId } else { $l.OwningProcess }
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
    $r = Invoke-WebRequest -Uri $url -Method Post -ContentType 'application/json' -Headers $h -Body ($body | ConvertTo-Json -Depth 10 -Compress) -TimeoutSec $timeoutSec -SkipHttpErrorCheck
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
    'setup' { Invoke-Setup }
    'check' { foreach ($s in Select-Services $Ids $false) { Test-Mcp $s } }
    'call' { Invoke-Tool $Ids }
}
