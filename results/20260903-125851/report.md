# Olla-DFT benchmark — run 20260903-125851

*Generated from `results.json`; every number is recomputable with `python bench.py verify`.*

## Environment

- CPU: 12th Gen Intel(R) Core(TM) i5-12450H (12 logical CPUs), pinned to CPU 0
- RAM: 7.4 GiB; governor `powersave`; turbo disabled: `False`
- OS: Linux-7.1.5-76070105-generic-x86_64-with-glibc2.39; Python 3.12.3
- Packages: ase 3.29.0, matplotlib 3.11.1, numpy 2.2.6, olla-dft 1.0.0, pymatgen 2026.5.4, scipy 1.18.1, seekpath 2.2.1, spglib 2.7.0
- Repetitions per cell: 5 (+1 warm-up, discarded); threads per process: 1; order interleaved across tools
- Load average at start: [3.48583984375, 1.95166015625, 1.50927734375]

> **Environment warnings**

> - CPU governor is 'powersave', not 'performance': timings are noisier. Fix: sudo cpupower frequency-set -g performance
> - Turbo boost enabled: single-thread timings drift with temperature. Fix: echo 1 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo
> - 1-min load average 3.49 > 1.0: other processes were competing for CPU.

## How to read the tables

Wall time is the median of a fresh process per repetition (imports included, because that is what the
command line costs). CPU is user+system time; RSS is peak resident memory of the process. `correct` is
the deterministic grade against an independent reference described in each task's note. `—` means the
tool does not cover the task; that is a coverage fact, not a failure.

## Structure parsing and symmetry (file → space group, primitive cell)

*All three use spglib underneath; this measures the wrapper cost (import + parse + report), not the algorithm.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | correct | detail |
|---|---|---|---|---|---|---|---|---|
| Si_relajado.cif | olla-dft | 0.784 | 0.618 | 0.568 | 0.722 | 97 | ✔ | sg 227 vs ref 227; prim atoms 2 vs 2 |
| Si_relajado.cif | ase | 0.589 | 0.490 | 0.148 | 0.530 | 81 | ✔ | sg 227 vs ref 227; prim atoms 2 vs 2 |
| Si_relajado.cif | pymatgen | 0.489 **←fastest** | 0.445 | 0.038 | 0.429 | 78 | ✔ | sg 227 vs ref 227; prim atoms 2 vs 2 |
| ZnO.cif | olla-dft | 0.793 | 0.710 | 0.369 | 0.727 | 97 | ✔ | sg 186 vs ref 186; prim atoms 4 vs 4 |
| ZnO.cif | ase | 0.517 **←fastest** | 0.430 | 0.313 | 0.461 | 81 | ✔ | sg 186 vs ref 186; prim atoms 4 vs 4 |
| ZnO.cif | pymatgen | 0.597 | 0.414 | 0.366 | 0.528 | 78 | ✔ | sg 186 vs ref 186; prim atoms 4 vs 4 |
| grafito.cif | olla-dft | 1.388 | 0.760 | 1.151 | 1.286 | 97 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| grafito.cif | ase | 0.878 | 0.610 | 0.494 | 0.805 | 81 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| grafito.cif | pymatgen | 0.731 **←fastest** | 0.590 | 0.329 | 0.674 | 78 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| hbn.cif | olla-dft | 0.699 | 0.650 | 0.147 | 0.629 | 97 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| hbn.cif | ase | 0.548 | 0.475 | 0.119 | 0.486 | 81 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| hbn.cif | pymatgen | 0.475 **←fastest** | 0.449 | 0.099 | 0.422 | 78 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| POSCAR_NaCl | olla-dft | 0.722 | 0.623 | 0.906 | 0.668 | 97 | ✔ | sg 225 vs ref 225; prim atoms 2 vs 2 |
| POSCAR_NaCl | ase | 0.527 **←fastest** | 0.494 | 0.168 | 0.469 | 80 | ✔ | sg 225 vs ref 225; prim atoms 2 vs 2 |
| POSCAR_NaCl | pymatgen | 1.073 | 0.932 | 0.140 | 1.013 | 121 | ✔ | sg 225 vs ref 225; prim atoms 2 vs 2 |

## High-symmetry k-path from a structure

*Reference is the HPKOT convention (seekpath). ASE and pymatgen implement Setyawan–Curtarolo; a mismatch there is a convention difference.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | correct | detail |
|---|---|---|---|---|---|---|---|---|
| Si_relajado.cif | olla-dft | 0.650 | 0.612 | 0.089 | 0.588 | 98 | ✔ | segments identical to HPKOT reference |
| Si_relajado.cif | seekpath | 0.514 | 0.490 | 0.024 | 0.464 | 81 | ✔ | segments identical to HPKOT reference |
| Si_relajado.cif | ase | 0.483 **←fastest** | 0.444 | 0.070 | 0.425 | 82 | ✘ | path differs from HPKOT reference (Jaccard 0.60); a different convention, not necessarily an error |
| Si_relajado.cif | pymatgen | 0.560 | 0.544 | 0.194 | 0.508 | 89 | ✘ | path differs from HPKOT reference (Jaccard 0.60); a different convention, not necessarily an error |
| ZnO.cif | olla-dft | 0.655 | 0.625 | 0.503 | 0.598 | 98 | ✔ | segments identical to HPKOT reference |
| ZnO.cif | seekpath | 0.636 | 0.489 | 0.322 | 0.554 | 81 | ✔ | segments identical to HPKOT reference |
| ZnO.cif | ase | 0.542 | 0.503 | 0.157 | 0.484 | 82 | ✔ | segments identical to HPKOT reference |
| ZnO.cif | pymatgen | 0.532 **←fastest** | 0.514 | 0.247 | 0.471 | 89 | ✔ | segments identical to HPKOT reference |
| grafito.cif | olla-dft | 0.659 | 0.567 | 0.094 | 0.578 | 97 | ✔ | segments identical to HPKOT reference |
| grafito.cif | seekpath | 0.469 | 0.467 | 0.062 | 0.423 | 81 | ✔ | segments identical to HPKOT reference |
| grafito.cif | ase | 0.467 **←fastest** | 0.444 | 0.164 | 0.419 | 82 | ✔ | segments identical to HPKOT reference |
| grafito.cif | pymatgen | 0.486 | 0.449 | 0.033 | 0.433 | 88 | ✔ | segments identical to HPKOT reference |
| hbn.cif | olla-dft | 0.626 | 0.591 | 0.056 | 0.566 | 97 | ✔ | segments identical to HPKOT reference |
| hbn.cif | seekpath | 0.468 **←fastest** | 0.452 | 0.043 | 0.421 | 81 | ✔ | segments identical to HPKOT reference |
| hbn.cif | ase | 0.490 | 0.456 | 0.037 | 0.428 | 82 | ✔ | segments identical to HPKOT reference |
| hbn.cif | pymatgen | 0.526 | 0.491 | 0.039 | 0.474 | 88 | ✔ | segments identical to HPKOT reference |
| POSCAR_NaCl | olla-dft | 0.643 | 0.551 | 0.118 | 0.591 | 97 | ✔ | segments identical to HPKOT reference |
| POSCAR_NaCl | seekpath | 0.486 | 0.467 | 0.422 | 0.439 | 81 | ✔ | segments identical to HPKOT reference |
| POSCAR_NaCl | ase | 0.451 **←fastest** | 0.432 | 0.068 | 0.392 | 81 | ✘ | path differs from HPKOT reference (Jaccard 0.09); a different convention, not necessarily an error |
| POSCAR_NaCl | pymatgen | 1.030 | 1.021 | 0.139 | 0.992 | 130 | ✘ | path differs from HPKOT reference (Jaccard 0.60); a different convention, not necessarily an error |

## Birch–Murnaghan fit of an E(V) table (9 points, Si)

*Olla-DFT is called through the fit function behind `olla-dft eos --collect`, because the command reads pw.x outputs, not a bare table.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | correct | detail |
|---|---|---|---|---|---|---|---|---|
| EOS.dat | olla-dft | 0.868 | 0.786 | 0.114 | 0.766 | 95 | ✔ | ΔV0=+0.00e+00 Å³, ΔB0=+0.00e+00 GPa |
| EOS.dat | ase | 0.781 **←fastest** | 0.630 | 0.223 | 0.682 | 78 | ✔ | ΔV0=-7.59e-08 Å³, ΔB0=+1.67e-06 GPa; B' not reported |
| EOS.dat | pymatgen | 1.069 | 0.837 | 0.564 | 0.981 | 112 | ✔ | ΔV0=+0.00e+00 Å³, ΔB0=+7.76e-07 GPa |

## Band gap from a pw.x data-file-schema XML (Si, 122 k-points)

*ASE and pymatgen do not read this XML; they are listed to make the coverage gap explicit.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | correct | detail |
|---|---|---|---|---|---|---|---|---|
| Si.xml.gz | olla-dft | 0.672 | 0.526 | 0.177 | 0.580 | 98 | ✔ | gap 0.4987 eV vs ref 0.4987 eV |
| Si.xml.gz | ase | — | — | — | — | — | n/a | not supported: ASE reads pw.x text output (espresso-out), not the data-file-schema XML |
| Si.xml.gz | pymatgen | — | — | — | — | — | n/a | not supported: pymatgen has no parser for the pw.x data-file-schema XML |

## pw.x scf input from a structure (Si 4×4×4, ZnO 6×6×4, fixed cutoffs)

*Each generated file is parsed back by ASE (reference) to check atoms and volume. Cutoffs are forced equal so the comparison is about correctness and cost, not defaults.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | correct | detail |
|---|---|---|---|---|---|---|---|---|
| Si_relajado.cif | olla-dft | 0.606 | 0.576 | 0.034 | 0.587 | 99 | ✔ | parsed back: 2 atoms, V=39.40187769469898 Å³ (ref 2, 39.4019); k-grid [4, 4, 4], ecutwfc 30.0 |
| Si_relajado.cif | ase | 0.431 | 0.426 | 0.059 | 0.415 | 79 | ✔ | parsed back: 2 atoms, V=39.401877693982705 Å³ (ref 2, 39.4019); k-grid [4, 4, 4], ecutwfc 30.0 |
| Si_relajado.cif | pymatgen | 0.406 **←fastest** | 0.390 | 0.095 | 0.388 | 77 | ✔ | parsed back: 2 atoms, V=39.40186569661943 Å³ (ref 2, 39.4019); k-grid [4, 4, 4], ecutwfc 30.0 |
| ZnO.cif | olla-dft | 0.600 | 0.554 | 0.056 | 0.585 | 98 | ✔ | parsed back: 4 atoms, V=47.61490819424488 Å³ (ref 4, 47.6149); k-grid [6, 6, 4], ecutwfc 30.0 |
| ZnO.cif | ase | 0.421 | 0.411 | 0.042 | 0.405 | 79 | ✔ | parsed back: 4 atoms, V=47.614908194203096 Å³ (ref 4, 47.6149); k-grid [6, 6, 4], ecutwfc 30.0 |
| ZnO.cif | pymatgen | 0.413 **←fastest** | 0.388 | 0.056 | 0.391 | 77 | ✔ | parsed back: 4 atoms, V=47.6149158149325 Å³ (ref 4, 47.6149); k-grid [6, 6, 4], ecutwfc 30.0 |

## End to end with pw.x (same binary, inputs from each tool)

| tool | k-grid | ecutwfc | total energy (Ry) | SCF iterations | pw.x wall s | input generated by |
|---|---|---|---|---|---|---|
| ase | [4, 4, 4] | 30.0 | -22.82476715 | 8 | 3.0 | ase.io.write(format='espresso-in') |
| olla-dft | [4, 4, 4] | 30.0 | -22.82476715 | 14 | 4.6 | cli gen -p scf --kspacing 0.5250 --ecutwfc 30 --ecutrho 240 --insulator (no explicit k-grid option) |
| pymatgen | [4, 4, 4] | 30.0 | -22.82476712 | 7 | 3.2 | pymatgen.io.pwscf.PWInput |

Spread of total energies across tools: 3.00e-08 Ry (identical physics ⇒ should be ≲ 1e-6 Ry). 

## Coverage matrix

| task | olla-dft | ase | pymatgen | seekpath |
|---|---|---|---|---|
| symmetry | ✔ | ✔ | ✔ | — |
| kpath | ✔ | ✔ | ✔ | ✔ |
| eos | ✔ | ✔ | ✔ | — |
| bandgap | ✔ | ✘ n/a | ✘ n/a | — |
| inputgen | ✔ | ✔ | ✔ | — |

## Areas of opportunity for Olla-DFT (generated automatically, same rule for every tool)

- symmetry/Si_relajado.cif: Olla-DFT wall time 0.78 s vs best competitor 0.49 s (1.6×)
- symmetry/ZnO.cif: Olla-DFT wall time 0.79 s vs best competitor 0.52 s (1.5×)
- symmetry/grafito.cif: Olla-DFT wall time 1.39 s vs best competitor 0.73 s (1.9×)
- bandgap/Si.xml.gz: Olla-DFT wall time 0.67 s vs best competitor 0.23 s (2.9×)
- bandgap/Si.xml.gz: Olla-DFT peak RSS 98 MB vs best competitor 40 MB
- end-to-end/Si: the input written by Olla-DFT needed 14 SCF iterations vs 7 for the best competitor at the same energy (defaults such as mixing_beta differ)
- end-to-end/Si: pw.x took 4.6 s on Olla-DFT's input vs 3.0 s on the best competitor's

## Known limitations of this benchmark

- One consumer laptop, hybrid CPU: absolute times are only comparable within one run; compare ratios across runs.
- Post-processing tasks are small; import time dominates and favours light dependency trees.
- Only tasks every tool can express with the same inputs are compared; Olla-DFT features without a counterpart are not benchmarked here, and features of the other tools that Olla-DFT lacks are visible in the coverage matrix.
- Correctness is checked against independent code for the numeric tasks; for k-paths, only agreement with one convention is measured.
