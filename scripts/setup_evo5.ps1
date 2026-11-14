# One-time (or after fixture change) setup on the Windows EVO-5 box.
# Does not start the 2-day run. See run_unattended.ps1 for that.
$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$Fixture = Join-Path $Root "fixtures\sample"
$Work = Join-Path $Root "bench\work"
$Sample = Join-Path $Work "sample"
$Svn = Join-Path $Work "sample-svn"
$Image = if ($env:BENCH_TOOLS_IMAGE) { $env:BENCH_TOOLS_IMAGE } else { "pumba-tools" }
$Docker = if ($env:BENCH_DOCKER) { $env:BENCH_DOCKER } else { "docker" }

if (-not (Test-Path (Join-Path $Fixture "CMakeLists.txt"))) {
  throw "Missing fixture: $Fixture"
}

New-Item -ItemType Directory -Force -Path $Work | Out-Null
if (Test-Path $Sample) { Remove-Item $Sample -Recurse -Force }
Copy-Item $Fixture $Sample -Recurse
# Windows copies can mark scripts/files read-only; git needs a clean tree.
Get-ChildItem $Sample -Recurse -File | ForEach-Object { $_.IsReadOnly = $false }

Push-Location $Sample
try {
  git init -b main | Out-Null
  git add -A
  git -c user.name=lab -c user.email=lab@localhost commit -m "baseline calculator" | Out-Null
  git tag -f baseline
} finally {
  Pop-Location
}

"keep me" | Set-Content (Join-Path $Work "outside.txt") -Encoding utf8NoBOM
if (Test-Path $Svn) { Remove-Item $Svn -Recurse -Force }
New-Item -ItemType Directory -Force -Path $Svn | Out-Null

Write-Host "Git worktree: $Sample (tag baseline)"

$running = & $Docker ps -q --filter "name=^bench-tools$"
if ($running) {
  Write-Host "Removing existing bench-tools container"
  & $Docker rm -f bench-tools | Out-Null
}

Write-Host "Starting $Image as bench-tools"
& $Docker run -d --name bench-tools `
  -v "${Sample}:/workspace/app" `
  -v "${Svn}:/workspace/svn" `
  -v "${Root}\bench:/workspace/bench:ro" `
  $Image sleep infinity | Out-Null

& $Docker exec bench-tools sh /workspace/bench/svn_setup.sh
if ($LASTEXITCODE -ne 0) {
  throw "svn_setup.sh failed inside bench-tools (need svnadmin + svn in the image)"
}

Write-Host "SVN copy: $Svn"
Write-Host "Next: python bench\preflight.py"
Write-Host "Then: powershell -File scripts\run_unattended.ps1"
