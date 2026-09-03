# Olla-DFT benchmark — run 20260903-145333

*Generated from `results.json`; every number is recomputable with `python bench.py verify`.*

## Environment

- CPU: 12th Gen Intel(R) Core(TM) i5-12450H (12 logical CPUs), pinned to CPU 0
- RAM: 7.4 GiB; governor `powersave`; turbo disabled: `False`
- OS: Linux-7.1.5-76070105-generic-x86_64-with-glibc2.39; Python 3.12.3; pw.x: Program PWSCF v.7.4 starts on  3Sep2026 at 14:53:34
- Packages: ase 3.29.0, matplotlib 3.11.1, numpy 2.2.6, olla-dft 1.0.1, pymatgen 2026.5.4, scipy 1.18.1, seekpath 2.2.1, spglib 2.7.0
- Olla-DFT source: `https://github.com/jorgegonzalezsevilla/olla-dft` @ `558ed7e234d3549e57fdfb8107d06e960fc5ec4a`
- Repetitions per cell: 15 (+1 warm-up, discarded); threads per process: 1; tool order shuffled per repetition (seed 20260903)
- End-to-end repetitions: 5; opportunity threshold: 1.15× (stated here, applied identically to time and memory)
- Load average at start / end: [1.84619140625, 2.5390625, 2.896484375] / [2.31787109375, 3.4443359375, 3.81298828125]

> **Environment warnings**

> - CPU governor is 'powersave', not 'performance': timings are noisier. Fix: sudo cpupower frequency-set -g performance
> - Turbo boost enabled: single-thread timings drift with temperature. Fix: echo 1 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo
> - 1-min load average 1.85 > 1.0: other processes were competing for CPU.

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
| Si_relajado.cif | olla-dft | 0.839 | 0.568 | 0.232 | 0.778 | 97 | ✔ | sg 227 vs ref 227; prim atoms 2 vs 2 |
| Si_relajado.cif | ase | 0.628 | 0.471 | 0.066 | 0.560 | 81 | ✔ | sg 227 vs ref 227; prim atoms 2 vs 2 |
| Si_relajado.cif | pymatgen | 0.597 **←fastest** | 0.421 | 0.093 | 0.543 | 78 | ✔ | sg 227 vs ref 227; prim atoms 2 vs 2 |
| ZnO.cif | olla-dft | 1.178 | 0.722 | 1.673 | 1.040 | 97 | ✔ | sg 186 vs ref 186; prim atoms 4 vs 4 |
| ZnO.cif | ase | 1.244 | 0.550 | 0.872 | 0.963 | 81 | ✔ | sg 186 vs ref 186; prim atoms 4 vs 4 |
| ZnO.cif | pymatgen | 0.862 **←fastest** | 0.504 | 0.511 | 0.753 | 78 | ✔ | sg 186 vs ref 186; prim atoms 4 vs 4 |
| grafito.cif | olla-dft | 0.926 | 0.687 | 0.472 | 0.857 | 97 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| grafito.cif | ase | 0.666 | 0.549 | 0.296 | 0.616 | 81 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| grafito.cif | pymatgen | 0.584 **←fastest** | 0.417 | 0.335 | 0.536 | 78 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| hbn.cif | olla-dft | 1.429 | 0.656 | 1.137 | 1.296 | 97 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| hbn.cif | ase | 0.878 | 0.600 | 0.592 | 0.808 | 80 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| hbn.cif | pymatgen | 0.750 **←fastest** | 0.560 | 0.607 | 0.693 | 77 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| POSCAR_NaCl | olla-dft | 1.053 **←fastest** | 0.558 | 1.361 | 0.945 | 97 | ✔ | sg 225 vs ref 225; prim atoms 2 vs 2 |
| POSCAR_NaCl | ase | 1.092 | 0.495 | 1.269 | 0.954 | 80 | ✔ | sg 225 vs ref 225; prim atoms 2 vs 2 |
| POSCAR_NaCl | pymatgen | 1.845 | 0.907 | 1.485 | 1.699 | 120 | ✔ | sg 225 vs ref 225; prim atoms 2 vs 2 |

## High-symmetry k-path from a structure

*Reference is the HPKOT convention (seekpath). Olla-DFT and the seekpath contestant call the same library, so their agreement is expected and only shows the path is passed through intact. ASE and pymatgen implement Setyawan–Curtarolo; a mismatch there is a convention difference, not an error.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | correct | detail |
|---|---|---|---|---|---|---|---|---|
| Si_relajado.cif | olla-dft | 0.943 | 0.536 | 0.542 | 0.798 | 97 | ✔ | segments identical to HPKOT reference |
| Si_relajado.cif | seekpath | 0.766 **←fastest** | 0.574 | 0.935 | 0.689 | 81 | ✔ | segments identical to HPKOT reference |
| Si_relajado.cif | ase | 0.971 | 0.423 | 0.551 | 0.875 | 81 | ✘ | path differs from HPKOT reference (Jaccard 0.60); a different convention, not necessarily an error |
| Si_relajado.cif | pymatgen | 0.926 | 0.494 | 0.531 | 0.810 | 88 | ✘ | path differs from HPKOT reference (Jaccard 0.60); a different convention, not necessarily an error |
| ZnO.cif | olla-dft | 1.005 | 0.799 | 0.321 | 0.934 | 97 | ✔ | segments identical to HPKOT reference |
| ZnO.cif | seekpath | 0.895 | 0.574 | 0.414 | 0.774 | 81 | ✔ | segments identical to HPKOT reference |
| ZnO.cif | ase | 0.830 **←fastest** | 0.595 | 0.418 | 0.722 | 82 | ✔ | segments identical to HPKOT reference |
| ZnO.cif | pymatgen | 0.893 | 0.536 | 0.568 | 0.795 | 88 | ✔ | segments identical to HPKOT reference |
| grafito.cif | olla-dft | 0.903 | 0.721 | 0.718 | 0.817 | 97 | ✔ | segments identical to HPKOT reference |
| grafito.cif | seekpath | 0.708 | 0.564 | 0.250 | 0.639 | 81 | ✔ | segments identical to HPKOT reference |
| grafito.cif | ase | 0.631 **←fastest** | 0.443 | 0.291 | 0.554 | 82 | ✔ | segments identical to HPKOT reference |
| grafito.cif | pymatgen | 0.774 | 0.461 | 0.416 | 0.664 | 88 | ✔ | segments identical to HPKOT reference |
| hbn.cif | olla-dft | 0.786 | 0.635 | 0.211 | 0.723 | 97 | ✔ | segments identical to HPKOT reference |
| hbn.cif | seekpath | 0.742 | 0.573 | 0.260 | 0.662 | 80 | ✔ | segments identical to HPKOT reference |
| hbn.cif | ase | 0.677 **←fastest** | 0.526 | 0.349 | 0.603 | 81 | ✔ | segments identical to HPKOT reference |
| hbn.cif | pymatgen | 0.786 | 0.561 | 0.452 | 0.701 | 88 | ✔ | segments identical to HPKOT reference |
| POSCAR_NaCl | olla-dft | 0.758 | 0.597 | 0.086 | 0.704 | 97 | ✔ | segments identical to HPKOT reference |
| POSCAR_NaCl | seekpath | 0.605 | 0.459 | 0.049 | 0.536 | 80 | ✔ | segments identical to HPKOT reference |
| POSCAR_NaCl | ase | 0.597 **←fastest** | 0.549 | 0.078 | 0.529 | 81 | ✘ | path differs from HPKOT reference (Jaccard 0.09); a different convention, not necessarily an error |
| POSCAR_NaCl | pymatgen | 1.385 | 1.265 | 0.250 | 1.326 | 130 | ✘ | path differs from HPKOT reference (Jaccard 0.60); a different convention, not necessarily an error |

## Birch–Murnaghan fit of an E(V) table (9 points, Si)

*Olla-DFT is called through the fit function behind `olla-dft eos --collect`, because the command reads pw.x outputs, not a bare table. EOS.dat is the table exported by `olla-dft eos Si.cif --run` in examples/demo_calculo of the Olla-DFT repository (QE 6.6, 9 volumes, ±10 %). The reference is an analytic linear fit, deliberately a different algorithm from every contestant's curve_fit.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | correct | detail |
|---|---|---|---|---|---|---|---|---|
| EOS.dat | olla-dft | 0.743 | 0.722 | 0.023 | 0.682 | 95 | ✔ | ΔV0=+6.07e-08 Å³, ΔB0=-1.25e-06 GPa |
| EOS.dat | ase | 0.539 **←fastest** | 0.517 | 0.057 | 0.485 | 78 | ✔ | ΔV0=-1.52e-08 Å³, ΔB0=+4.24e-07 GPa; B' not reported |
| EOS.dat | pymatgen | 0.925 | 0.905 | 0.048 | 0.869 | 112 | ✔ | ΔV0=+6.07e-08 Å³, ΔB0=-4.69e-07 GPa |

## Band gap from pw.x output (XML and text)

*The XML and the text output of the same scf run, generated with the shipped inputs/Si_scf.in (QE 7.4), so that each format counts once and no tool is judged only on the format it prefers. Olla-DFT and qeschema read the XML; ASE reads the text output; pymatgen reads neither for eigenvalues.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | correct | detail |
|---|---|---|---|---|---|---|---|---|
| Si_scf.xml | olla-dft | 0.720 | 0.646 | 0.053 | 0.660 | 97 | ✔ | gap 0.6155 eV vs ref 0.6155 eV |
| Si_scf.xml | qeschema | 0.663 **←fastest** | 0.629 | 0.088 | 0.600 | 48 | ✔ | gap 0.6155421137080532 eV vs ref 0.6155 eV |
| Si_scf.xml | ase | — | — | — | — | — | n/a | not supported: ASE reads pw.x text output (espresso-out), not the data-file-schema XML |
| Si_scf.xml | pymatgen | — | — | — | — | — | n/a | not supported: pymatgen.io.pwscf.PWOutput parses energies only (no eigenvalues) and there is no XML parser |
| Si_scf.out | olla-dft | — | — | — | — | — | n/a | not supported: `olla-dft gap` reads the data-file-schema XML, not the pw.x text output |
| Si_scf.out | qeschema | — | — | — | — | — | n/a | not supported: qeschema reads the data-file-schema XML, not the text output |
| Si_scf.out | ase | 0.541 **←fastest** | 0.513 | 0.033 | 0.484 | 78 | ✔ | gap 0.6154999999999999 eV vs ref 0.6155 eV |
| Si_scf.out | pymatgen | — | — | — | — | — | n/a | not supported: pymatgen.io.pwscf.PWOutput parses energies only (no eigenvalues) and there is no XML parser |

## pw.x scf input from a structure (Si 4×4×4, ZnO 6×6×4, fixed cutoffs)

*Each generated file is parsed back by ASE (reference) to check atoms, volume, k-grid and ecutwfc. Cutoffs and grid are forced equal so the comparison is about correctness and cost, not defaults; other defaults (mixing, smearing) remain each tool's own and show up in the end-to-end stage.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | correct | detail |
|---|---|---|---|---|---|---|---|---|
| Si_relajado.cif | olla-dft | 0.721 | 0.676 | 0.144 | 0.701 | 98 | ✔ | parsed back: 2 atoms, V=39.40187769469898 Å³ (ref 2, 39.4019); k-grid [4, 4, 4] (expected [4, 4, 4]), ecutwfc 30.0 (expected 30) |
| Si_relajado.cif | ase | 0.530 | 0.501 | 0.048 | 0.510 | 79 | ✔ | parsed back: 2 atoms, V=39.401877693982705 Å³ (ref 2, 39.4019); k-grid [4, 4, 4] (expected [4, 4, 4]), ecutwfc 30.0 (expected 30) |
| Si_relajado.cif | pymatgen | 0.496 **←fastest** | 0.422 | 0.052 | 0.474 | 76 | ✔ | parsed back: 2 atoms, V=39.40186569661943 Å³ (ref 2, 39.4019); k-grid [4, 4, 4] (expected [4, 4, 4]), ecutwfc 30.0 (expected 30) |
| ZnO.cif | olla-dft | 0.716 | 0.669 | 0.034 | 0.694 | 98 | ✔ | parsed back: 4 atoms, V=47.61490819424488 Å³ (ref 4, 47.6149); k-grid [6, 6, 4] (expected [6, 6, 4]), ecutwfc 30.0 (expected 30) |
| ZnO.cif | ase | 0.526 | 0.506 | 0.116 | 0.503 | 79 | ✔ | parsed back: 4 atoms, V=47.614908194203096 Å³ (ref 4, 47.6149); k-grid [6, 6, 4] (expected [6, 6, 4]), ecutwfc 30.0 (expected 30) |
| ZnO.cif | pymatgen | 0.502 **←fastest** | 0.474 | 0.044 | 0.482 | 76 | ✔ | parsed back: 4 atoms, V=47.6149158149325 Å³ (ref 4, 47.6149); k-grid [6, 6, 4] (expected [6, 6, 4]), ecutwfc 30.0 (expected 30) |

## Olla-DFT relative to the best supported competitor, every contested cell

Ratios > 1 mean Olla-DFT is slower or heavier. `min` ratio uses the fastest sample of each (robust to background noise); the CI is a 95 % bootstrap of the ratio of medians.

| task | input | vs | wall ratio (median) | 95 % CI | wall ratio (min) | RSS ratio |
|---|---|---|---|---|---|---|
| symmetry | Si_relajado.cif | pymatgen | 1.41 | 1.21–1.65 | 1.35 | 1.25 |
| symmetry | ZnO.cif | pymatgen | 1.37 | 1.03–3.12 | 1.43 | 1.25 |
| symmetry | grafito.cif | pymatgen | 1.59 | 0.93–2.04 | 1.65 | 1.25 |
| symmetry | hbn.cif | pymatgen | 1.90 | 0.86–2.66 | 1.17 | 1.25 |
| symmetry | POSCAR_NaCl | ase | 0.96 | 0.56–2.73 | 1.13 | 1.21 |
| kpath | Si_relajado.cif | seekpath | 1.23 | 0.62–1.71 | 0.93 | 1.20 |
| kpath | ZnO.cif | ase | 1.21 | 0.94–1.69 | 1.34 | 1.20 |
| kpath | grafito.cif | ase | 1.43 | 1.05–2.31 | 1.63 | 1.21 |
| kpath | hbn.cif | ase | 1.16 | 0.92–1.48 | 1.21 | 1.20 |
| kpath | POSCAR_NaCl | ase | 1.27 | 1.22–1.41 | 1.09 | 1.21 |
| eos | EOS.dat | ase | 1.38 | 1.26–1.39 | 1.40 | 1.22 |
| bandgap | Si_scf.xml | qeschema | 1.09 | 1.00–1.14 | 1.03 | 2.01 |
| inputgen | Si_relajado.cif | pymatgen | 1.45 | 1.37–1.66 | 1.60 | 1.29 |
| inputgen | ZnO.cif | pymatgen | 1.43 | 1.37–1.50 | 1.41 | 1.28 |

**Summary:** Olla-DFT is slower than the best supported competitor in 13 of 14 contested cells (geometric-mean wall ratio 1.33×, min-based 1.29×) and uses more peak memory in 14 of 14 (geometric mean 1.28×).

## End to end with pw.x (same binary, same k-grid and cutoffs, inputs from each tool)

| tool | k-grid | irreducible k | ecutwfc | total energy (Ry) | SCF iterations | pw.x wall s (median of n) | n | input generated by |
|---|---|---|---|---|---|---|---|---|
| ase | [4, 4, 4] | 13 | 30.0 | -22.82476715 | 8 | 3.43 | 5 | ase.io.write(format='espresso-in') |
| olla-dft | [4, 4, 4] | 13 | 30.0 | -22.82476715 | 14 | 4.83 | 5 | cli gen -p scf --kspacing 0.5250 --ecutwfc 30 --ecutrho 240 --insulator (no explicit k-grid option; spacing precomputed untimed by the harness) |
| pymatgen | [4, 4, 4] | 24 | 30.0 | -22.82476712 | 7 | 3.94 | 5 | pymatgen.io.pwscf.PWInput |

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

- symmetry/Si_relajado.cif: 1.41× the wall time of pymatgen (95 % CI 1.21–1.65)
- symmetry/Si_relajado.cif: 1.25× the peak memory of the lightest competitor
- symmetry/ZnO.cif: 1.37× the wall time of pymatgen (95 % CI 1.03–3.12)
- symmetry/ZnO.cif: 1.25× the peak memory of the lightest competitor
- symmetry/grafito.cif: 1.59× the wall time of pymatgen (95 % CI 0.93–2.04) — not significant: the CI includes 1
- symmetry/grafito.cif: 1.25× the peak memory of the lightest competitor
- symmetry/hbn.cif: 1.90× the wall time of pymatgen (95 % CI 0.86–2.66) — not significant: the CI includes 1
- symmetry/hbn.cif: 1.25× the peak memory of the lightest competitor
- symmetry/POSCAR_NaCl: 1.21× the peak memory of the lightest competitor
- kpath/Si_relajado.cif: 1.23× the wall time of seekpath (95 % CI 0.62–1.71) — not significant: the CI includes 1
- kpath/Si_relajado.cif: 1.20× the peak memory of the lightest competitor
- kpath/ZnO.cif: 1.21× the wall time of ase (95 % CI 0.94–1.69) — not significant: the CI includes 1
- kpath/ZnO.cif: 1.20× the peak memory of the lightest competitor
- kpath/grafito.cif: 1.43× the wall time of ase (95 % CI 1.05–2.31)
- kpath/grafito.cif: 1.21× the peak memory of the lightest competitor
- kpath/hbn.cif: 1.16× the wall time of ase (95 % CI 0.92–1.48) — not significant: the CI includes 1
- kpath/hbn.cif: 1.20× the peak memory of the lightest competitor
- kpath/POSCAR_NaCl: 1.27× the wall time of ase (95 % CI 1.22–1.41)
- kpath/POSCAR_NaCl: 1.21× the peak memory of the lightest competitor
- eos/EOS.dat: 1.38× the wall time of ase (95 % CI 1.26–1.39)
- eos/EOS.dat: 1.22× the peak memory of the lightest competitor
- bandgap/Si_scf.xml: 2.01× the peak memory of the lightest competitor
- inputgen/Si_relajado.cif: 1.45× the wall time of pymatgen (95 % CI 1.37–1.66)
- inputgen/Si_relajado.cif: 1.29× the peak memory of the lightest competitor
- inputgen/ZnO.cif: 1.43× the wall time of pymatgen (95 % CI 1.37–1.50)
- inputgen/ZnO.cif: 1.28× the peak memory of the lightest competitor
- Olla-DFT uses more peak memory in every contested cell (geometric mean 1.28×)
- end-to-end/Si: Olla-DFT's input needed 14 SCF iterations vs 7 for the best competitor at the same energy (its defaults, e.g. mixing_beta, differ)
- end-to-end/Si: pw.x took 4.83 s on Olla-DFT's input vs 3.43 s on the best competitor's

## Known limitations of this benchmark

- One consumer laptop, hybrid CPU: absolute times are only comparable within one run; compare ratios across runs.
- Post-processing tasks are small; import time dominates and favours light dependency trees. That is a real cost for a CLI tool, but it is not algorithmic speed.
- Only tasks every tool can express with the same inputs are compared; Olla-DFT features without a counterpart are not benchmarked here, and features of the other tools that Olla-DFT lacks are visible in the coverage matrix.
- symmetry and kpath references share a backend with some contestants (stated in the notes); eos and bandgap references are independent code.
- The end-to-end stage uses one small system (Si, 2 atoms).
