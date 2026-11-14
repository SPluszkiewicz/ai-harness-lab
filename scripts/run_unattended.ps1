# Start the matrix and leave it. No prompts.
# If python dies, this script starts it again (resume via summary.jsonl) until the
# matrix finishes or 48 hours have passed. A missing worktree does not retry.
$ErrorActionPreference = "Continue"
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
  $PSNativeCommandUseErrorActionPreference = $false
}
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$Bench = Join-Path $Root "bench"
Set-Location $Bench

$env:PYTHONUNBUFFERED = "1"
if (-not $env:BENCH_TIMEOUT) { $env:BENCH_TIMEOUT = "420" }

$py = if ($env:BENCH_PYTHON) { $env:BENCH_PYTHON } else { "python" }
New-Item -ItemType Directory -Force -Path (Join-Path $Bench "results") | Out-Null
$console = Join-Path $Bench "results\console.log"
$deadline = (Get-Date).AddHours(48)

if (-not (Test-Path (Join-Path $Bench "work\sample\.git"))) {
  throw "bench\work\sample missing. Run scripts\setup_evo5.ps1 first."
}

function Write-Console([string]$Message) {
  $line = "{0} {1}" -f (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ"), $Message
  Write-Host $line
  Add-Content -Path $console -Value $line
}

function Invoke-Py([string[]]$PyArgs, [int]$CapSeconds) {
  $stamp = Get-Date -Format "yyyyMMddHHmmss"
  $out = Join-Path $Bench "results\stdout-$stamp.log"
  $err = Join-Path $Bench "results\stderr-$stamp.log"
  $proc = Start-Process -FilePath $py -ArgumentList (@("-u") + $PyArgs) -WorkingDirectory $Bench `
    -WindowStyle Hidden -PassThru -RedirectStandardOutput $out -RedirectStandardError $err
  if ($CapSeconds -gt 0) {
    if (-not $proc.WaitForExit($CapSeconds * 1000)) {
      & taskkill.exe /F /T /PID $proc.Id 2>$null | Out-Null
      Write-Console "killed python $($PyArgs -join ' ') after ${CapSeconds}s — see $err"
      return 75
    }
  } else {
    $proc.WaitForExit() | Out-Null
  }
  if ($null -eq $proc.ExitCode) { return 75 }
  return [int]$proc.ExitCode
}

Write-Console "waiting for preflight (llama-server + bench-tools). Deadline $deadline"
$pre = 1
while ((Get-Date) -lt $deadline) {
  $pre = Invoke-Py @("preflight.py") 360
  if ($pre -eq 0) { break }
  Write-Console "preflight exit $pre — retry in 60s"
  Start-Sleep -Seconds 60
}
if ($pre -ne 0) {
  throw "preflight never passed. See $console"
}

Write-Console "starting run_all.py — safe to lock the session"
$code = 1
while ((Get-Date) -lt $deadline) {
  $runArgs = @("run_all.py") + @($args)
  $code = Invoke-Py $runArgs 0
  if ($code -eq 0 -or $code -eq 2) { break }
  Write-Console "run_all exit $code — resume in 30s (done cells are skipped)"
  Start-Sleep -Seconds 30
}

$null = Invoke-Py @("report.py") 600
Write-Console "finished exit $code — read bench\results\decision.md"
if ($code -eq 2) { throw "worktree missing — run setup_evo5.ps1" }
exit $code
