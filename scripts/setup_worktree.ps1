# Prepare bench/work from fixtures/sample (git baseline).
$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$Fixture = Join-Path $Root "fixtures\sample"
$Work = Join-Path $Root "bench\work"
$Sample = Join-Path $Work "sample"

if (-not (Test-Path (Join-Path $Fixture "CMakeLists.txt"))) {
  throw "Missing fixture: $Fixture"
}

New-Item -ItemType Directory -Force -Path $Work | Out-Null
if (Test-Path $Sample) { Remove-Item $Sample -Recurse -Force }
Copy-Item $Fixture $Sample -Recurse

Push-Location $Sample
try {
  git init -b main | Out-Null
  git add -A
  git -c user.name=lab -c user.email=lab@localhost commit -m "baseline calculator" | Out-Null
  git tag -f baseline
} finally {
  Pop-Location
}

"keep me" | Set-Content (Join-Path $Work "outside.txt") -Encoding utf8
Write-Host "Ready: $Sample (tag baseline)"
Write-Host "SVN copy: run bench/svn_setup.sh inside the bench-tools container after mounting work/sample-svn."
