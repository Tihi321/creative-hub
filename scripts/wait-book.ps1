# Waits until a Scriptorium story has become a finished book, printing each stage change.
# Run it in the background after add_story; a book takes from tens of minutes to hours.
# It reads the files in the Scriptorium data folder, so it works without an MCP connection.
#
#   pwsh -File scripts\wait-book.ps1 -Story <story-slug> [-TimeoutMinutes 600] [-PollSeconds 30]
# Exit code 0 = published, 1 = failed/rejected, 2 = timeout.

param(
    [Parameter(Mandatory)][string]$Story,
    [string]$Data = $(if ($env:SCRIPTORIUM_DATA) { $env:SCRIPTORIUM_DATA } else { Join-Path $HOME 'Scriptorium' }),
    [int]$TimeoutMinutes = 600,
    [int]$PollSeconds = 30
)

function Get-Front([string]$file, [string]$key) {
    if (-not (Test-Path $file)) { return $null }
    $m = Select-String -Path $file -Pattern "^${key}:\s*(.*)$" | Select-Object -First 1
    if ($m) { $m.Matches[0].Groups[1].Value.Trim().Trim('"', "'") }
}

$idea = Join-Path $Data "ideas\$Story.md"
if (-not (Test-Path $idea)) { Write-Error "No story at $idea"; exit 1 }
$deadline = (Get-Date).AddMinutes($TimeoutMinutes)
$last = ''
while ((Get-Date) -lt $deadline) {
    $book = Get-Front $idea 'book'
    if (-not $book) { $line = 'waiting for the factory to pick up the story' }
    else {
        $bookMd = Join-Path $Data "books\$book\book.md"
        $stage = Get-Front $bookMd 'stage'
        $chapters = (Get-ChildItem (Join-Path $Data "books\$book\chapters") -Filter 'ch-*.md' -ErrorAction SilentlyContinue | Measure-Object).Count
        $line = "book=$book stage=$stage chapters=$chapters"
        if ($stage -eq 'published') {
            Write-Host "$(Get-Date -Format HH:mm) $line"
            Write-Host "DONE folder=$(Join-Path $Data "books\$book")"
            exit 0
        }
        if ($stage -in 'failed', 'rejected') { Write-Host "$(Get-Date -Format HH:mm) $line"; exit 1 }
    }
    if ($line -ne $last) { Write-Host "$(Get-Date -Format HH:mm) $line"; $last = $line }
    Start-Sleep -Seconds $PollSeconds
}
Write-Host "Timed out after $TimeoutMinutes minutes ($last)"
exit 2
