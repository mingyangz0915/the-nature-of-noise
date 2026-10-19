# The Nature of Noise

**From Random Motion to Spectral Density, Thermal Equilibrium, and Circuit Analysis**

**Author:** Mingyang Zhang  
**Version:** 1.0  
**First Public Release:** October 2026

*The Nature of Noise* is a collection of educational notes on the mathematical and physical foundations of noise, with applications to analog and RF circuit analysis.

The manuscript develops noise theory from random variables and stochastic processes to correlation functions, power spectral density, thermal equilibrium, and circuit-level noise analysis. The emphasis is on connecting mathematical definitions, physical intuition, and engineering models through explicit derivations.

## Read the Manuscript

**[Download the PDF](The_Nature_of_Noise.pdf)**

The PDF is the recommended format for reading. The LaTeX source, original figures, and supporting numerical examples are also available in this repository.

## Contents

The manuscript covers:

- Probability, random variables, and stochastic processes
- Stationarity, ergodicity, and correlation functions
- Power spectral density and its mathematical interpretation
- Spectral estimation and finite observation effects
- Thermal noise, statistical mechanics, and thermal equilibrium
- Noise propagation through linear time-invariant systems
- Noise analysis in analog and RF circuits
- Phase noise and related concepts

The goal is to establish a consistent framework connecting microscopic random motion, statistical descriptions, frequency-domain representations, and observable circuit noise.

## Repository Structure

| Path | Description |
|---|---|
| `The_Nature_of_Noise.pdf` | Compiled PDF manuscript |
| `manuscript/The_Nature_of_Noise.tex` | Main LaTeX document |
| `manuscript/preamble.tex` | LaTeX packages, commands, and formatting |
| `manuscript/sections/` | Individual manuscript sections |
| `manuscript/figures/` | Figures and supporting figure files |
| `Examples/` | Numerical and computational examples |
| `build.ps1` | PowerShell build script |
| `LICENSE` | CC BY-NC-ND 4.0 license text |

## Building from Source

The manuscript is written in LaTeX and can be compiled using `pdflatex`.

**Requirements:**
- A LaTeX distribution such as TeX Live, with the packages required by the manuscript
- PowerShell, if using the provided build script

From the repository root, run:

```powershell
.\build.ps1
```

The script runs `pdflatex` three times to resolve cross-references and writes the compiled PDF to:

`manuscript/output/pdf/The_Nature_of_Noise.pdf`

Alternatively, the manuscript can be compiled manually from the `manuscript/` directory using `pdflatex`.

## Citation

If you find these notes useful in your research or teaching, please cite:

Zhang, M. (2026). *The Nature of Noise: From Random Motion to Spectral Density, Thermal Equilibrium, and Circuit Analysis*. Version 1.0.

A DOI and version-specific citation information may be added following archival release.

## License

Copyright © 2026 Mingyang Zhang.

The manuscript, its LaTeX source, and original figures are licensed under the [Creative Commons Attribution–NonCommercial–NoDerivatives 4.0 International License (CC BY-NC-ND 4.0)](https://creativecommons.org/licenses/by-nc-nd/4.0/).

You may copy and redistribute the unmodified licensed material for noncommercial purposes, provided that appropriate attribution is given and the license terms are followed.

Redistribution of adapted versions, including modified or translated editions, requires separate permission from the copyright holder, except where permitted by applicable law.

The software examples in `Examples/` and the `build.ps1` script are not included in the manuscript license grant. Separate software licensing terms may be provided for these files.

Third-party materials, if any, remain subject to their respective rights and licenses.
