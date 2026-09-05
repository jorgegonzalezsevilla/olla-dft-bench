# Olla-DFT benchmark — run 20260904-143453

*Generated from `results.json`; every number is recomputable with `python bench.py verify`.*

## Environment

- CPU: 12th Gen Intel(R) Core(TM) i5-12450H (12 logical CPUs), pinned to CPU 0
- RAM: 7.4 GiB; governor `powersave`; turbo disabled: `False`
- OS: Linux-7.1.5-76070105-generic-x86_64-with-glibc2.39; Python 3.12.3; pw.x: /home/jorge/GITHUB/olla-dft-bench/.qe/bin/pw.x
- Packages: ase 3.29.0, matplotlib 3.11.1, numpy 2.2.6, olla-dft 1.1.0, pymatgen 2026.5.4, scipy 1.18.1, seekpath 2.2.1, spglib 2.7.0
- Olla-DFT source: `https://github.com/jorgegonzalezsevilla/olla-dft` @ `caf08257293e1fe1ef2ebf9db051b3ec827a7f45`
- Repetitions per cell: 15 (+1 warm-up, discarded); threads per process: 1; tool order shuffled per repetition (seed 20260904)
- End-to-end repetitions: 5; opportunity threshold: 1.15× (stated here, applied identically to time and memory)
- Load average at start / end: [1.6240234375, 1.21484375, 0.85302734375] / [1.93896484375, 2.95654296875, 2.3349609375]

> **Environment warnings**

> - CPU governor is 'powersave', not 'performance': timings are noisier. Fix: sudo cpupower frequency-set -g performance
> - Turbo boost enabled: single-thread timings drift with temperature. Fix: echo 1 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo
> - 1-min load average 1.62 > 1.0: other processes were competing for CPU.

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
| Si_relajado.cif | olla-dft | 0.490 | 0.479 | 0.142 | 0.489 | 97 | ✔ | sg 227 vs ref 227; prim atoms 2 vs 2 |
| Si_relajado.cif | ase | 0.373 | 0.358 | 0.130 | 0.371 | 81 | ✔ | sg 227 vs ref 227; prim atoms 2 vs 2 |
| Si_relajado.cif | pymatgen | 0.341 **←fastest** | 0.327 | 0.123 | 0.341 | 78 | ✔ | sg 227 vs ref 227; prim atoms 2 vs 2 |
| ZnO.cif | olla-dft | 0.650 | 0.545 | 0.111 | 0.648 | 97 | ✔ | sg 186 vs ref 186; prim atoms 4 vs 4 |
| ZnO.cif | ase | 0.499 | 0.431 | 0.058 | 0.498 | 81 | ✔ | sg 186 vs ref 186; prim atoms 4 vs 4 |
| ZnO.cif | pymatgen | 0.457 **←fastest** | 0.368 | 0.070 | 0.455 | 78 | ✔ | sg 186 vs ref 186; prim atoms 4 vs 4 |
| grafito.cif | olla-dft | 1.994 | 0.549 | 2.975 | 1.989 | 97 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| grafito.cif | ase | 1.329 | 0.412 | 1.641 | 1.326 | 81 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| grafito.cif | pymatgen | 0.988 **←fastest** | 0.374 | 1.897 | 0.985 | 78 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| hbn.cif | olla-dft | 1.095 | 0.688 | 0.951 | 1.092 | 97 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| hbn.cif | ase | 0.605 | 0.500 | 0.199 | 0.604 | 81 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| hbn.cif | pymatgen | 0.549 **←fastest** | 0.449 | 0.168 | 0.547 | 78 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| POSCAR_NaCl | olla-dft | 0.781 | 0.601 | 0.162 | 0.779 | 97 | ✔ | sg 225 vs ref 225; prim atoms 2 vs 2 |
| POSCAR_NaCl | ase | 0.568 **←fastest** | 0.515 | 0.157 | 0.566 | 80 | ✔ | sg 225 vs ref 225; prim atoms 2 vs 2 |
| POSCAR_NaCl | pymatgen | 1.231 | 0.946 | 0.617 | 1.228 | 121 | ✔ | sg 225 vs ref 225; prim atoms 2 vs 2 |

## High-symmetry k-path from a structure

*Reference is the HPKOT convention (seekpath). Olla-DFT and the seekpath contestant call the same library, so their agreement is expected and only shows the path is passed through intact. ASE and pymatgen implement Setyawan–Curtarolo; a mismatch there is a convention difference, not an error.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | correct | detail |
|---|---|---|---|---|---|---|---|---|
| Si_relajado.cif | olla-dft | 0.734 | 0.617 | 0.190 | 0.733 | 98 | ✔ | segments identical to HPKOT reference |
| Si_relajado.cif | seekpath | 0.523 | 0.450 | 0.128 | 0.522 | 81 | ✔ | segments identical to HPKOT reference |
| Si_relajado.cif | ase | 0.518 **←fastest** | 0.453 | 0.076 | 0.517 | 82 | ✘ | path differs from HPKOT reference (Jaccard 0.60); a different convention, not necessarily an error |
| Si_relajado.cif | pymatgen | 0.622 | 0.528 | 0.128 | 0.621 | 89 | ✘ | path differs from HPKOT reference (Jaccard 0.60); a different convention, not necessarily an error |
| ZnO.cif | olla-dft | 0.680 | 0.582 | 0.174 | 0.679 | 98 | ✔ | segments identical to HPKOT reference |
| ZnO.cif | seekpath | 0.577 | 0.435 | 0.115 | 0.575 | 81 | ✔ | segments identical to HPKOT reference |
| ZnO.cif | ase | 0.532 **←fastest** | 0.442 | 0.110 | 0.531 | 82 | ✔ | segments identical to HPKOT reference |
| ZnO.cif | pymatgen | 0.593 | 0.493 | 0.111 | 0.592 | 89 | ✔ | segments identical to HPKOT reference |
| grafito.cif | olla-dft | 0.649 | 0.559 | 0.141 | 0.647 | 98 | ✔ | segments identical to HPKOT reference |
| grafito.cif | seekpath | 0.458 | 0.443 | 0.030 | 0.457 | 81 | ✔ | segments identical to HPKOT reference |
| grafito.cif | ase | 0.451 **←fastest** | 0.431 | 0.066 | 0.450 | 82 | ✔ | segments identical to HPKOT reference |
| grafito.cif | pymatgen | 0.546 | 0.481 | 0.111 | 0.545 | 89 | ✔ | segments identical to HPKOT reference |
| hbn.cif | olla-dft | 0.559 | 0.523 | 0.030 | 0.555 | 98 | ✔ | segments identical to HPKOT reference |
| hbn.cif | seekpath | 0.428 **←fastest** | 0.408 | 0.015 | 0.426 | 81 | ✔ | segments identical to HPKOT reference |
| hbn.cif | ase | 0.432 | 0.399 | 0.043 | 0.431 | 82 | ✔ | segments identical to HPKOT reference |
| hbn.cif | pymatgen | 0.474 | 0.438 | 0.030 | 0.473 | 89 | ✔ | segments identical to HPKOT reference |
| POSCAR_NaCl | olla-dft | 0.535 | 0.522 | 0.018 | 0.533 | 98 | ✔ | segments identical to HPKOT reference |
| POSCAR_NaCl | seekpath | 0.412 | 0.398 | 0.010 | 0.410 | 81 | ✔ | segments identical to HPKOT reference |
| POSCAR_NaCl | ase | 0.388 **←fastest** | 0.380 | 0.010 | 0.387 | 82 | ✘ | path differs from HPKOT reference (Jaccard 0.09); a different convention, not necessarily an error |
| POSCAR_NaCl | pymatgen | 0.979 | 0.962 | 0.023 | 0.978 | 131 | ✘ | path differs from HPKOT reference (Jaccard 0.60); a different convention, not necessarily an error |

## Birch–Murnaghan fit of an E(V) table (9 points, Si)

*Olla-DFT is called through the fit function behind `olla-dft eos --collect`, because the command reads pw.x outputs, not a bare table. EOS.dat is the table exported by `olla-dft eos Si.cif --run` in examples/demo_calculo of the Olla-DFT repository (QE 6.6, 9 volumes, ±10 %). The reference is an analytic linear fit, deliberately a different algorithm from every contestant's curve_fit.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | correct | detail |
|---|---|---|---|---|---|---|---|---|
| EOS.dat | olla-dft | 0.449 | 0.435 | 0.015 | 0.448 | 92 | ✔ | ΔV0=+6.07e-08 Å³, ΔB0=-1.25e-06 GPa |
| EOS.dat | ase | 0.378 **←fastest** | 0.331 | 0.012 | 0.377 | 79 | ✔ | ΔV0=-1.52e-08 Å³, ΔB0=+4.24e-07 GPa; B' not reported |
| EOS.dat | pymatgen | 0.686 | 0.669 | 0.019 | 0.685 | 113 | ✔ | ΔV0=+6.07e-08 Å³, ΔB0=-4.69e-07 GPa |

## Band gap from pw.x output (XML and text)

*The XML and the text output of the same scf run, generated with the shipped inputs/Si_scf.in (QE 7.4), so that each format counts once and no tool is judged only on the format it prefers. Olla-DFT and qeschema read the XML; ASE reads the text output; pymatgen reads neither for eigenvalues.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | correct | detail |
|---|---|---|---|---|---|---|---|---|
| Si_scf.xml | olla-dft | 0.245 **←fastest** | 0.239 | 0.008 | 0.244 | 52 | ✔ | gap 0.6155 eV vs ref 0.6155 eV |
| Si_scf.xml | qeschema | 0.482 | 0.469 | 0.020 | 0.481 | 48 | ✔ | gap 0.6155421137080532 eV vs ref 0.6155 eV |
| Si_scf.xml | ase | — | — | — | — | — | n/a | not supported: ASE reads pw.x text output (espresso-out), not the data-file-schema XML |
| Si_scf.xml | pymatgen | — | — | — | — | — | n/a | not supported: pymatgen.io.pwscf.PWOutput parses energies only (no eigenvalues) and there is no XML parser |
| Si_scf.out | olla-dft | — | — | — | — | — | n/a | not supported: `olla-dft gap` reads the data-file-schema XML, not the pw.x text output |
| Si_scf.out | qeschema | — | — | — | — | — | n/a | not supported: qeschema reads the data-file-schema XML, not the text output |
| Si_scf.out | ase | 0.388 **←fastest** | 0.376 | 0.011 | 0.387 | 79 | ✔ | gap 0.6154999999999999 eV vs ref 0.6155 eV |
| Si_scf.out | pymatgen | — | — | — | — | — | n/a | not supported: pymatgen.io.pwscf.PWOutput parses energies only (no eigenvalues) and there is no XML parser |

## pw.x scf input from a structure (Si 4×4×4, ZnO 6×6×4, fixed cutoffs)

*Each generated file is parsed back by ASE (reference) to check atoms, volume, k-grid and ecutwfc. Cutoffs and grid are forced equal so the comparison is about correctness and cost, not defaults; other defaults (mixing, smearing) remain each tool's own and show up in the end-to-end stage.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | correct | detail |
|---|---|---|---|---|---|---|---|---|
| Si_relajado.cif | olla-dft | 0.532 | 0.519 | 0.018 | 0.529 | 99 | ✔ | parsed back: 2 atoms, V=39.40187769469898 Å³ (ref 2, 39.4019); k-grid [4, 4, 4] (expected [4, 4, 4]), ecutwfc 30.0 (expected 30) |
| Si_relajado.cif | ase | 0.385 | 0.382 | 0.009 | 0.384 | 80 | ✔ | parsed back: 2 atoms, V=39.401877693982705 Å³ (ref 2, 39.4019); k-grid [4, 4, 4] (expected [4, 4, 4]), ecutwfc 30.0 (expected 30) |
| Si_relajado.cif | pymatgen | 0.355 **←fastest** | 0.354 | 0.012 | 0.355 | 78 | ✔ | parsed back: 2 atoms, V=39.40186569661943 Å³ (ref 2, 39.4019); k-grid [4, 4, 4] (expected [4, 4, 4]), ecutwfc 30.0 (expected 30) |
| ZnO.cif | olla-dft | 0.652 | 0.633 | 0.012 | 0.650 | 98 | ✔ | parsed back: 4 atoms, V=47.61490819424488 Å³ (ref 4, 47.6149); k-grid [6, 6, 4] (expected [6, 6, 4]), ecutwfc 30.0 (expected 30) |
| ZnO.cif | ase | 0.473 | 0.424 | 0.019 | 0.472 | 80 | ✔ | parsed back: 4 atoms, V=47.614908194203096 Å³ (ref 4, 47.6149); k-grid [6, 6, 4] (expected [6, 6, 4]), ecutwfc 30.0 (expected 30) |
| ZnO.cif | pymatgen | 0.437 **←fastest** | 0.426 | 0.010 | 0.436 | 78 | ✔ | parsed back: 4 atoms, V=47.6149158149325 Å³ (ref 4, 47.6149); k-grid [6, 6, 4] (expected [6, 6, 4]), ecutwfc 30.0 (expected 30) |

## Olla-DFT relative to the best supported competitor, every contested cell

Ratios > 1 mean Olla-DFT is slower or heavier. `min` ratio uses the fastest sample of each (robust to background noise); the CI is a 95 % bootstrap of the ratio of medians.

| task | input | vs | wall ratio (median) | 95 % CI | wall ratio (min) | RSS ratio |
|---|---|---|---|---|---|---|
| symmetry | Si_relajado.cif | pymatgen | 1.43 | 1.11–1.82 | 1.47 | 1.25 |
| symmetry | ZnO.cif | pymatgen | 1.42 | 1.29–1.54 | 1.48 | 1.25 |
| symmetry | grafito.cif | pymatgen | 2.02 | 0.56–3.08 | 1.47 | 1.25 |
| symmetry | hbn.cif | pymatgen | 1.99 | 1.36–2.54 | 1.53 | 1.25 |
| symmetry | POSCAR_NaCl | ase | 1.38 | 1.22–1.54 | 1.17 | 1.21 |
| kpath | Si_relajado.cif | ase | 1.42 | 1.26–1.71 | 1.36 | 1.20 |
| kpath | ZnO.cif | ase | 1.28 | 1.09–1.52 | 1.32 | 1.20 |
| kpath | grafito.cif | ase | 1.44 | 1.26–1.63 | 1.30 | 1.20 |
| kpath | hbn.cif | seekpath | 1.31 | 1.28–1.36 | 1.28 | 1.20 |
| kpath | POSCAR_NaCl | ase | 1.38 | 1.35–1.41 | 1.37 | 1.21 |
| eos | EOS.dat | ase | 1.19 | 1.17–1.21 | 1.31 | 1.17 |
| bandgap | Si_scf.xml | qeschema | 0.51 | 0.49–0.52 | 0.51 | 1.08 |
| inputgen | Si_relajado.cif | pymatgen | 1.50 | 1.46–1.52 | 1.47 | 1.28 |
| inputgen | ZnO.cif | pymatgen | 1.49 | 1.48–1.53 | 1.49 | 1.27 |

**Summary:** Olla-DFT is slower than the best supported competitor in 13 of 14 contested cells (geometric-mean wall ratio 1.36×, min-based 1.29×) and uses more peak memory in 14 of 14 (geometric mean 1.21×).

## End to end with pw.x (same binary, same k-grid and cutoffs, inputs from each tool)

| tool | k-grid | irreducible k | ecutwfc | total energy (Ry) | SCF iterations | pw.x wall s (median of n) | n | input generated by |
|---|---|---|---|---|---|---|---|---|
| ase | [4, 4, 4] | None | 30.0 | None | None | — | 0 | ase.io.write(format='espresso-in') |
| olla-dft | [4, 4, 4] | None | 30.0 | None | None | — | 0 | cli gen -p scf --kspacing 0.5250 --ecutwfc 30 --ecutrho 240 --insulator (no explicit k-grid option; spacing precomputed untimed by the harness) |
| pymatgen | [4, 4, 4] | None | 30.0 | None | None | — | 0 | pymatgen.io.pwscf.PWInput |

## Coverage matrix

| task | olla-dft | ase | pymatgen | qeschema | seekpath |
|---|---|---|---|---|---|
| symmetry | ✔ | ✔ | ✔ | — | — |
| kpath | ✔ | ✔ | ✔ | — | ✔ |
| eos | ✔ | ✔ | ✔ | — | — |
| bandgap | ✔ 1/2 inputs | ✔ 1/2 inputs | ✘ n/a | ✔ 1/2 inputs | — |
| inputgen | ✔ | ✔ | ✔ | — | — |

## Areas of opportunity for Olla-DFT (generated automatically; threshold 1.15×, same rule for every tool)

- symmetry/Si_relajado.cif: 1.43× the wall time of pymatgen (95 % CI 1.11–1.82)
- symmetry/Si_relajado.cif: 1.25× the peak memory of the lightest competitor
- symmetry/ZnO.cif: 1.42× the wall time of pymatgen (95 % CI 1.29–1.54)
- symmetry/ZnO.cif: 1.25× the peak memory of the lightest competitor
- symmetry/grafito.cif: 2.02× the wall time of pymatgen (95 % CI 0.56–3.08) — not significant: the CI includes 1
- symmetry/grafito.cif: 1.25× the peak memory of the lightest competitor
- symmetry/hbn.cif: 1.99× the wall time of pymatgen (95 % CI 1.36–2.54)
- symmetry/hbn.cif: 1.25× the peak memory of the lightest competitor
- symmetry/POSCAR_NaCl: 1.38× the wall time of ase (95 % CI 1.22–1.54)
- symmetry/POSCAR_NaCl: 1.21× the peak memory of the lightest competitor
- kpath/Si_relajado.cif: 1.42× the wall time of ase (95 % CI 1.26–1.71)
- kpath/Si_relajado.cif: 1.20× the peak memory of the lightest competitor
- kpath/ZnO.cif: 1.28× the wall time of ase (95 % CI 1.09–1.52)
- kpath/ZnO.cif: 1.20× the peak memory of the lightest competitor
- kpath/grafito.cif: 1.44× the wall time of ase (95 % CI 1.26–1.63)
- kpath/grafito.cif: 1.20× the peak memory of the lightest competitor
- kpath/hbn.cif: 1.31× the wall time of seekpath (95 % CI 1.28–1.36)
- kpath/hbn.cif: 1.20× the peak memory of the lightest competitor
- kpath/POSCAR_NaCl: 1.38× the wall time of ase (95 % CI 1.35–1.41)
- kpath/POSCAR_NaCl: 1.21× the peak memory of the lightest competitor
- eos/EOS.dat: 1.19× the wall time of ase (95 % CI 1.17–1.21)
- eos/EOS.dat: 1.17× the peak memory of the lightest competitor
- inputgen/Si_relajado.cif: 1.50× the wall time of pymatgen (95 % CI 1.46–1.52)
- inputgen/Si_relajado.cif: 1.28× the peak memory of the lightest competitor
- inputgen/ZnO.cif: 1.49× the wall time of pymatgen (95 % CI 1.48–1.53)
- inputgen/ZnO.cif: 1.27× the peak memory of the lightest competitor
- Olla-DFT uses more peak memory in every contested cell (geometric mean 1.21×)

## Known limitations of this benchmark

- One consumer laptop, hybrid CPU: absolute times are only comparable within one run; compare ratios across runs.
- Post-processing tasks are small; import time dominates and favours light dependency trees. That is a real cost for a CLI tool, but it is not algorithmic speed.
- Only tasks every tool can express with the same inputs are compared; Olla-DFT features without a counterpart are not benchmarked here, and features of the other tools that Olla-DFT lacks are visible in the coverage matrix.
- symmetry and kpath references share a backend with some contestants (stated in the notes); eos and bandgap references are independent code.
- The end-to-end stage uses one small system (Si, 2 atoms).
