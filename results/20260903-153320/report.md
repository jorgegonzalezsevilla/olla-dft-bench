# Olla-DFT benchmark — run 20260903-153320

*Generated from `results.json`; every number is recomputable with `python bench.py verify`.*

## Environment

- CPU: 12th Gen Intel(R) Core(TM) i5-12450H (12 logical CPUs), pinned to CPU 0
- RAM: 7.4 GiB; governor `powersave`; turbo disabled: `False`
- OS: Linux-7.1.5-76070105-generic-x86_64-with-glibc2.39; Python 3.12.3; pw.x: Program PWSCF v.7.4 starts on  3Sep2026 at 15:33:21
- Packages: ase 3.29.0, matplotlib 3.11.1, numpy 2.2.6, olla-dft 1.1.0, pymatgen 2026.5.4, scipy 1.18.1, seekpath 2.2.1, spglib 2.7.0
- Olla-DFT source: `https://github.com/jorgegonzalezsevilla/olla-dft` @ `caf08257293e1fe1ef2ebf9db051b3ec827a7f45`
- Repetitions per cell: 15 (+1 warm-up, discarded); threads per process: 1; tool order shuffled per repetition (seed 20260903)
- End-to-end repetitions: 5; opportunity threshold: 1.15× (stated here, applied identically to time and memory)
- Load average at start / end: [2.037109375, 2.3330078125, 2.96240234375] / [2.3310546875, 3.10888671875, 3.072265625]

> **Environment warnings**

> - CPU governor is 'powersave', not 'performance': timings are noisier. Fix: sudo cpupower frequency-set -g performance
> - Turbo boost enabled: single-thread timings drift with temperature. Fix: echo 1 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo
> - 1-min load average 2.04 > 1.0: other processes were competing for CPU.

## How to read the tables

Wall time is the median of a fresh process per repetition (imports included, because that is what the
command line costs). CPU is user+system time; RSS is peak resident memory. `correct` is the deterministic
grade against the reference described in each task's note; where the reference shares a backend with a
contestant, the note says so and the grade only shows the wrapper passes the result through. `—` means
the tool does not cover the task; that is a coverage fact, not a failure, and such cells are excluded from
every speed or memory comparison.

## Structure parsing and symmetry (file → space group, primitive cell)

*Reference shares its backend (spglib) with all three contestants: the grade checks that each wrapper preserves the result, not the algorithm. Timing measures wrapper cost (import + parse + report).*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | correct | detail |
|---|---|---|---|---|---|---|---|---|
| Si_relajado.cif | olla-dft | 0.613 | 0.543 | 0.079 | 0.546 | 97 | ✔ | sg 227 vs ref 227; prim atoms 2 vs 2 |
| Si_relajado.cif | ase | 0.469 | 0.423 | 0.089 | 0.415 | 81 | ✔ | sg 227 vs ref 227; prim atoms 2 vs 2 |
| Si_relajado.cif | pymatgen | 0.434 **←fastest** | 0.393 | 0.101 | 0.381 | 78 | ✔ | sg 227 vs ref 227; prim atoms 2 vs 2 |
| ZnO.cif | olla-dft | 0.601 | 0.575 | 0.056 | 0.544 | 97 | ✔ | sg 186 vs ref 186; prim atoms 4 vs 4 |
| ZnO.cif | ase | 0.469 | 0.448 | 0.022 | 0.407 | 81 | ✔ | sg 186 vs ref 186; prim atoms 4 vs 4 |
| ZnO.cif | pymatgen | 0.427 **←fastest** | 0.414 | 0.043 | 0.370 | 78 | ✔ | sg 186 vs ref 186; prim atoms 4 vs 4 |
| grafito.cif | olla-dft | 0.615 | 0.565 | 0.067 | 0.565 | 97 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| grafito.cif | ase | 0.465 | 0.444 | 0.066 | 0.413 | 81 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| grafito.cif | pymatgen | 0.431 **←fastest** | 0.359 | 0.075 | 0.375 | 78 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| hbn.cif | olla-dft | 0.588 | 0.565 | 0.032 | 0.539 | 97 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| hbn.cif | ase | 0.461 | 0.447 | 0.029 | 0.409 | 81 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| hbn.cif | pymatgen | 0.436 **←fastest** | 0.411 | 0.017 | 0.379 | 78 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| POSCAR_NaCl | olla-dft | 0.666 | 0.535 | 0.211 | 0.597 | 97 | ✔ | sg 225 vs ref 225; prim atoms 2 vs 2 |
| POSCAR_NaCl | ase | 0.501 **←fastest** | 0.461 | 0.209 | 0.448 | 80 | ✔ | sg 225 vs ref 225; prim atoms 2 vs 2 |
| POSCAR_NaCl | pymatgen | 0.937 | 0.819 | 0.158 | 0.889 | 121 | ✔ | sg 225 vs ref 225; prim atoms 2 vs 2 |

## High-symmetry k-path from a structure

*Reference is the HPKOT convention (seekpath). Olla-DFT and the seekpath contestant call the same library, so their agreement is expected and only shows the path is passed through intact. ASE and pymatgen implement Setyawan–Curtarolo; a mismatch there is a convention difference, not an error.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | correct | detail |
|---|---|---|---|---|---|---|---|---|
| Si_relajado.cif | olla-dft | 0.618 | 0.593 | 0.038 | 0.564 | 98 | ✔ | segments identical to HPKOT reference |
| Si_relajado.cif | seekpath | 0.480 | 0.461 | 0.026 | 0.428 | 81 | ✔ | segments identical to HPKOT reference |
| Si_relajado.cif | ase | 0.473 **←fastest** | 0.451 | 0.016 | 0.419 | 82 | ✘ | path differs from HPKOT reference (Jaccard 0.60); a different convention, not necessarily an error |
| Si_relajado.cif | pymatgen | 0.555 | 0.536 | 0.042 | 0.507 | 89 | ✘ | path differs from HPKOT reference (Jaccard 0.60); a different convention, not necessarily an error |
| ZnO.cif | olla-dft | 0.677 | 0.593 | 0.151 | 0.621 | 98 | ✔ | segments identical to HPKOT reference |
| ZnO.cif | seekpath | 0.478 | 0.461 | 0.094 | 0.424 | 81 | ✔ | segments identical to HPKOT reference |
| ZnO.cif | ase | 0.475 **←fastest** | 0.448 | 0.056 | 0.426 | 82 | ✔ | segments identical to HPKOT reference |
| ZnO.cif | pymatgen | 0.528 | 0.494 | 0.078 | 0.466 | 89 | ✔ | segments identical to HPKOT reference |
| grafito.cif | olla-dft | 0.937 | 0.670 | 0.306 | 0.857 | 97 | ✔ | segments identical to HPKOT reference |
| grafito.cif | seekpath | 0.761 **←fastest** | 0.587 | 1.026 | 0.700 | 81 | ✔ | segments identical to HPKOT reference |
| grafito.cif | ase | 0.816 | 0.587 | 0.442 | 0.739 | 82 | ✔ | segments identical to HPKOT reference |
| grafito.cif | pymatgen | 0.829 | 0.609 | 0.398 | 0.767 | 89 | ✔ | segments identical to HPKOT reference |
| hbn.cif | olla-dft | 0.776 | 0.720 | 0.140 | 0.718 | 97 | ✔ | segments identical to HPKOT reference |
| hbn.cif | seekpath | 0.631 | 0.469 | 0.307 | 0.559 | 81 | ✔ | segments identical to HPKOT reference |
| hbn.cif | ase | 0.617 **←fastest** | 0.462 | 0.109 | 0.538 | 82 | ✔ | segments identical to HPKOT reference |
| hbn.cif | pymatgen | 0.689 | 0.559 | 0.173 | 0.611 | 89 | ✔ | segments identical to HPKOT reference |
| POSCAR_NaCl | olla-dft | 0.819 | 0.679 | 0.350 | 0.745 | 97 | ✔ | segments identical to HPKOT reference |
| POSCAR_NaCl | seekpath | 0.624 **←fastest** | 0.476 | 0.638 | 0.558 | 81 | ✔ | segments identical to HPKOT reference |
| POSCAR_NaCl | ase | 0.820 | 0.476 | 0.511 | 0.739 | 82 | ✘ | path differs from HPKOT reference (Jaccard 0.09); a different convention, not necessarily an error |
| POSCAR_NaCl | pymatgen | 1.523 | 1.256 | 0.674 | 1.463 | 131 | ✘ | path differs from HPKOT reference (Jaccard 0.60); a different convention, not necessarily an error |

## Birch–Murnaghan fit of an E(V) table (9 points, Si)

*Olla-DFT is called through the fit function behind `olla-dft eos --collect`, because the command reads pw.x outputs, not a bare table. EOS.dat is the table exported by `olla-dft eos Si.cif --run` in examples/demo_calculo of the Olla-DFT repository (QE 6.6, 9 volumes, ±10 %). The reference is an analytic linear fit, deliberately a different algorithm from every contestant's curve_fit.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | correct | detail |
|---|---|---|---|---|---|---|---|---|
| EOS.dat | olla-dft | 0.652 | 0.602 | 0.337 | 0.604 | 92 | ✔ | ΔV0=+6.07e-08 Å³, ΔB0=-1.25e-06 GPa |
| EOS.dat | ase | 0.573 **←fastest** | 0.530 | 0.399 | 0.510 | 79 | ✔ | ΔV0=-1.52e-08 Å³, ΔB0=+4.24e-07 GPa; B' not reported |
| EOS.dat | pymatgen | 0.973 | 0.920 | 0.644 | 0.907 | 112 | ✔ | ΔV0=+6.07e-08 Å³, ΔB0=-4.69e-07 GPa |

## Band gap from pw.x output (XML and text)

*The XML and the text output of the same scf run, generated with the shipped inputs/Si_scf.in (QE 7.4), so that each format counts once and no tool is judged only on the format it prefers. Olla-DFT and qeschema read the XML; ASE reads the text output; pymatgen reads neither for eigenvalues.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | correct | detail |
|---|---|---|---|---|---|---|---|---|
| Si_scf.xml | olla-dft | 0.384 **←fastest** | 0.352 | 0.131 | 0.316 | 52 | ✔ | gap 0.6155 eV vs ref 0.6155 eV |
| Si_scf.xml | qeschema | 0.681 | 0.648 | 0.351 | 0.618 | 48 | ✔ | gap 0.6155421137080532 eV vs ref 0.6155 eV |
| Si_scf.xml | ase | — | — | — | — | — | n/a | not supported: ASE reads pw.x text output (espresso-out), not the data-file-schema XML |
| Si_scf.xml | pymatgen | — | — | — | — | — | n/a | not supported: pymatgen.io.pwscf.PWOutput parses energies only (no eigenvalues) and there is no XML parser |
| Si_scf.out | olla-dft | — | — | — | — | — | n/a | not supported: `olla-dft gap` reads the data-file-schema XML, not the pw.x text output |
| Si_scf.out | qeschema | — | — | — | — | — | n/a | not supported: qeschema reads the data-file-schema XML, not the text output |
| Si_scf.out | ase | 0.531 **←fastest** | 0.518 | 0.031 | 0.472 | 78 | ✔ | gap 0.6154999999999999 eV vs ref 0.6155 eV |
| Si_scf.out | pymatgen | — | — | — | — | — | n/a | not supported: pymatgen.io.pwscf.PWOutput parses energies only (no eigenvalues) and there is no XML parser |

## pw.x scf input from a structure (Si 4×4×4, ZnO 6×6×4, fixed cutoffs)

*Each generated file is parsed back by ASE (reference) to check atoms, volume, k-grid and ecutwfc. Cutoffs and grid are forced equal so the comparison is about correctness and cost, not defaults; other defaults (mixing, smearing) remain each tool's own and show up in the end-to-end stage.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | correct | detail |
|---|---|---|---|---|---|---|---|---|
| Si_relajado.cif | olla-dft | 0.706 | 0.667 | 0.050 | 0.682 | 99 | ✔ | parsed back: 2 atoms, V=39.40187769469898 Å³ (ref 2, 39.4019); k-grid [4, 4, 4] (expected [4, 4, 4]), ecutwfc 30.0 (expected 30) |
| Si_relajado.cif | ase | 0.532 | 0.506 | 0.045 | 0.507 | 80 | ✔ | parsed back: 2 atoms, V=39.401877693982705 Å³ (ref 2, 39.4019); k-grid [4, 4, 4] (expected [4, 4, 4]), ecutwfc 30.0 (expected 30) |
| Si_relajado.cif | pymatgen | 0.493 **←fastest** | 0.423 | 0.092 | 0.470 | 77 | ✔ | parsed back: 2 atoms, V=39.40186569661943 Å³ (ref 2, 39.4019); k-grid [4, 4, 4] (expected [4, 4, 4]), ecutwfc 30.0 (expected 30) |
| ZnO.cif | olla-dft | 0.710 | 0.687 | 0.038 | 0.688 | 98 | ✔ | parsed back: 4 atoms, V=47.61490819424488 Å³ (ref 4, 47.6149); k-grid [6, 6, 4] (expected [6, 6, 4]), ecutwfc 30.0 (expected 30) |
| ZnO.cif | ase | 0.524 | 0.495 | 0.020 | 0.503 | 80 | ✔ | parsed back: 4 atoms, V=47.614908194203096 Å³ (ref 4, 47.6149); k-grid [6, 6, 4] (expected [6, 6, 4]), ecutwfc 30.0 (expected 30) |
| ZnO.cif | pymatgen | 0.484 **←fastest** | 0.400 | 0.029 | 0.464 | 77 | ✔ | parsed back: 4 atoms, V=47.6149158149325 Å³ (ref 4, 47.6149); k-grid [6, 6, 4] (expected [6, 6, 4]), ecutwfc 30.0 (expected 30) |

## Olla-DFT relative to the best supported competitor, every contested cell

Ratios > 1 mean Olla-DFT is slower or heavier. `min` ratio uses the fastest sample of each (robust to background noise); the CI is a 95 % bootstrap of the ratio of medians.

| task | input | vs | wall ratio (median) | 95 % CI | wall ratio (min) | RSS ratio |
|---|---|---|---|---|---|---|
| symmetry | Si_relajado.cif | pymatgen | 1.41 | 1.26–1.55 | 1.38 | 1.25 |
| symmetry | ZnO.cif | pymatgen | 1.41 | 1.32–1.47 | 1.39 | 1.25 |
| symmetry | grafito.cif | pymatgen | 1.43 | 1.32–1.55 | 1.57 | 1.25 |
| symmetry | hbn.cif | pymatgen | 1.35 | 1.34–1.42 | 1.37 | 1.25 |
| symmetry | POSCAR_NaCl | ase | 1.33 | 1.11–1.65 | 1.16 | 1.21 |
| kpath | Si_relajado.cif | ase | 1.31 | 1.28–1.37 | 1.32 | 1.20 |
| kpath | ZnO.cif | ase | 1.42 | 1.19–1.53 | 1.32 | 1.20 |
| kpath | grafito.cif | seekpath | 1.23 | 0.63–1.56 | 1.14 | 1.20 |
| kpath | hbn.cif | ase | 1.26 | 1.12–1.42 | 1.56 | 1.20 |
| kpath | POSCAR_NaCl | seekpath | 1.31 | 0.73–1.68 | 1.42 | 1.20 |
| eos | EOS.dat | ase | 1.14 | 0.69–1.37 | 1.14 | 1.16 |
| bandgap | Si_scf.xml | qeschema | 0.56 | 0.41–0.74 | 0.54 | 1.07 |
| inputgen | Si_relajado.cif | pymatgen | 1.43 | 1.28–1.52 | 1.58 | 1.28 |
| inputgen | ZnO.cif | pymatgen | 1.47 | 1.41–1.53 | 1.72 | 1.27 |

**Summary:** Olla-DFT is slower than the best supported competitor in 13 of 14 contested cells (geometric-mean wall ratio 1.26×, min-based 1.29×) and uses more peak memory in 14 of 14 (geometric mean 1.21×).

## End to end with pw.x (same binary, same k-grid and cutoffs, inputs from each tool)

| tool | k-grid | irreducible k | ecutwfc | total energy (Ry) | SCF iterations | pw.x wall s (median of n) | n | input generated by |
|---|---|---|---|---|---|---|---|---|
| ase | [4, 4, 4] | 13 | 30.0 | -22.82476715 | 8 | 3.37 | 5 | ase.io.write(format='espresso-in') |
| olla-dft | [4, 4, 4] | 13 | 30.0 | -22.82476715 | 8 | 3.61 | 5 | cli gen -p scf --kspacing 0.5250 --ecutwfc 30 --ecutrho 240 --insulator (no explicit k-grid option; spacing precomputed untimed by the harness) |
| pymatgen | [4, 4, 4] | 24 | 30.0 | -22.82476712 | 7 | 3.68 | 5 | pymatgen.io.pwscf.PWInput |

Spread of total energies across tools: 3.00e-08 Ry. Same grid and cutoffs should agree to ≲ 1e-6 Ry; the number of irreducible k-points may differ if a tool writes the cell differently, which is itself a difference in the input.

## Coverage matrix

| task | olla-dft | ase | pymatgen | qeschema | seekpath |
|---|---|---|---|---|---|
| symmetry | ✔ | ✔ | ✔ | — | — |
| kpath | ✔ | ✔ | ✔ | — | ✔ |
| eos | ✔ | ✔ | ✔ | — | — |
| bandgap | ✔ 1/2 inputs | ✔ 1/2 inputs | ✘ n/a | ✔ 1/2 inputs | — |
| inputgen | ✔ | ✔ | ✔ | — | — |

## Areas of opportunity for Olla-DFT (generated automatically; threshold 1.15×, same rule for every tool)

- symmetry/Si_relajado.cif: 1.41× the wall time of pymatgen (95 % CI 1.26–1.55)
- symmetry/Si_relajado.cif: 1.25× the peak memory of the lightest competitor
- symmetry/ZnO.cif: 1.41× the wall time of pymatgen (95 % CI 1.32–1.47)
- symmetry/ZnO.cif: 1.25× the peak memory of the lightest competitor
- symmetry/grafito.cif: 1.43× the wall time of pymatgen (95 % CI 1.32–1.55)
- symmetry/grafito.cif: 1.25× the peak memory of the lightest competitor
- symmetry/hbn.cif: 1.35× the wall time of pymatgen (95 % CI 1.34–1.42)
- symmetry/hbn.cif: 1.25× the peak memory of the lightest competitor
- symmetry/POSCAR_NaCl: 1.33× the wall time of ase (95 % CI 1.11–1.65)
- symmetry/POSCAR_NaCl: 1.21× the peak memory of the lightest competitor
- kpath/Si_relajado.cif: 1.31× the wall time of ase (95 % CI 1.28–1.37)
- kpath/Si_relajado.cif: 1.20× the peak memory of the lightest competitor
- kpath/ZnO.cif: 1.42× the wall time of ase (95 % CI 1.19–1.53)
- kpath/ZnO.cif: 1.20× the peak memory of the lightest competitor
- kpath/grafito.cif: 1.23× the wall time of seekpath (95 % CI 0.63–1.56) — not significant: the CI includes 1
- kpath/grafito.cif: 1.20× the peak memory of the lightest competitor
- kpath/hbn.cif: 1.26× the wall time of ase (95 % CI 1.12–1.42)
- kpath/hbn.cif: 1.20× the peak memory of the lightest competitor
- kpath/POSCAR_NaCl: 1.31× the wall time of seekpath (95 % CI 0.73–1.68) — not significant: the CI includes 1
- kpath/POSCAR_NaCl: 1.20× the peak memory of the lightest competitor
- eos/EOS.dat: 1.16× the peak memory of the lightest competitor
- inputgen/Si_relajado.cif: 1.43× the wall time of pymatgen (95 % CI 1.28–1.52)
- inputgen/Si_relajado.cif: 1.28× the peak memory of the lightest competitor
- inputgen/ZnO.cif: 1.47× the wall time of pymatgen (95 % CI 1.41–1.53)
- inputgen/ZnO.cif: 1.27× the peak memory of the lightest competitor
- Olla-DFT uses more peak memory in every contested cell (geometric mean 1.21×)

## Known limitations of this benchmark

- One consumer laptop, hybrid CPU: absolute times are only comparable within one run; compare ratios across runs.
- Post-processing tasks are small; import time dominates and favours light dependency trees. That is a real cost for a CLI tool, but it is not algorithmic speed.
- Only tasks every tool can express with the same inputs are compared; Olla-DFT features without a counterpart are not benchmarked here, and features of the other tools that Olla-DFT lacks are visible in the coverage matrix.
- symmetry and kpath references share a backend with some contestants (stated in the notes); eos and bandgap references are independent code.
- The end-to-end stage uses one small system (Si, 2 atoms).
