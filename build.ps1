# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Mingyang Zhang
#
# This build script is licensed under the MIT License.
# See Examples/LICENSE for the full license text.

$ErrorActionPreference = 'Stop'

if (-not (Get-Command pdflatex -ErrorAction SilentlyContinue)) {
    throw 'pdflatex was not found. Install TeX Live and add its bin directory to PATH.'
}

$sourceFolder = Join-Path $PSScriptRoot 'manuscript'

New-Item -ItemType Directory -Force -Path (Join-Path $sourceFolder 'build') | Out-Null

Push-Location -LiteralPath $sourceFolder

try {
    for ($pass = 1; $pass -le 3; $pass++) {
        & pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build The_Nature_of_Noise.tex

        if ($LASTEXITCODE -ne 0) {
            throw "Compilation failed on pass $pass."
        }
    }

    New-Item -ItemType Directory -Force -Path 'output/pdf' | Out-Null

    Copy-Item -LiteralPath 'build/The_Nature_of_Noise.pdf' `
        -Destination 'output/pdf/The_Nature_of_Noise.pdf' -Force

    Write-Host 'The Nature of Noise compiled successfully.'
}
finally {
    Pop-Location
}
