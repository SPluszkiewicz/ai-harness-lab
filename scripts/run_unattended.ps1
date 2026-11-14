# Start the 2-day matrix and leave it. No prompts.
# Requires setup_evo5.ps1 already done, llama-server on BENCH_BASE_URL (default http://127.0.0.1:8080/v1).
$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$Bench = Join-Path $Root "bench"
Set-Location $Bench

$env:PYTHONUNBUFFERED = "1"
if (-not $env:BENCH_TIMEOUT) { $env:BENCH_TIMEOUT = "420" }

$py = if ($env:BENCH_PYTHON) { $env:BENCH_PYTHON } else { "python" }

Write-Host "preflight..."
& $py preflight.py
if ($LASTEXITCODE -ne 0) { throw "preflight failed — fix llama-server / bench-tools / worktree, then rerun." }

$log = Join-Path $Bench "results\unattended.log"
New-Item -ItemType Directory -Force -Path (Join-Path $Bench "results") | Out-Null
Write-Host "starting run_all.py — log $log"
Write-Host "Safe to lock the session / walk away. Resume is automatic if you rerun this script."

& $py run_all.py @args
$code = $LASTEXITCODE
& $py report.py
Write-Host "exit $code — read bench\results\decision.md"
exit $code
