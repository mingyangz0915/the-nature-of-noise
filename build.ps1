param(
    [ValidateSet('manuscript', 'early-draft', 'All')]
    [string]$Target = 'manuscript'
)

$ErrorActionPreference = 'Stop'
if (-not (Get-Command pdflatex -ErrorAction SilentlyContinue)) {
    throw 'pdflatex was not found. Install TeX Live and add its bin directory to PATH.'
}
$targetsToBuild = if ($Target -eq 'All') { @('manuscript', 'early-draft') } else { @($Target) }

foreach ($targetName in $targetsToBuild) {
    $relativeFolder = if ($targetName -eq 'early-draft') { 'archive/early-draft' } else { 'manuscript' }
    $sourceFolder = Join-Path $PSScriptRoot $relativeFolder
    New-Item -ItemType Directory -Force -Path (Join-Path $sourceFolder 'build') | Out-Null
    Push-Location -LiteralPath $sourceFolder
    try {
        for ($pass = 1; $pass -le 3; $pass++) {
            & pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build The_Nature_of_Noise.tex
            if ($LASTEXITCODE -ne 0) { throw "Compilation failed for $targetName on pass $pass." }
        }
        New-Item -ItemType Directory -Force -Path 'output/pdf' | Out-Null
        Copy-Item -LiteralPath 'build/The_Nature_of_Noise.pdf' -Destination 'output/pdf/The_Nature_of_Noise.pdf' -ErrorAction Stop
        Write-Host "$targetName compiled successfully: $sourceFolder/output/pdf/The_Nature_of_Noise.pdf"
    }
    finally {
        Pop-Location
    }
}
