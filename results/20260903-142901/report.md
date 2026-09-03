# Olla-DFT benchmark — run 20260903-142901

*Generated from `results.json`; every number is recomputable with `python bench.py verify`.*

## Environment

- CPU: 12th Gen Intel(R) Core(TM) i5-12450H (12 logical CPUs), pinned to CPU 0
- RAM: 7.4 GiB; governor `powersave`; turbo disabled: `False`
- OS: Linux-7.1.5-76070105-generic-x86_64-with-glibc2.39; Python 3.12.3; pw.x: Program PWSCF v.7.4 starts on  3Sep2026 at 14:29: 1
- Packages: ase 3.29.0, matplotlib 3.11.1, numpy 2.2.6, olla-dft 1.0.0, pymatgen 2026.5.4, scipy 1.18.1, seekpath 2.2.1, spglib 2.7.0
- Olla-DFT source: `https://github.com/jorgegonzalezsevilla/olla-dft` @ `15b44febbfdd218667da5a7c8a11715ca98758b3`
- Repetitions per cell: 15 (+1 warm-up, discarded); threads per process: 1; tool order shuffled per repetition (seed 20260903)
- End-to-end repetitions: 5; opportunity threshold: 1.15× (stated here, applied identically to time and memory)
- Load average at start / end: [1.91259765625, 1.93408203125, 1.982421875] / [2.68017578125, 3.5771484375, 3.1611328125]

> **Environment warnings**

> - CPU governor is 'powersave', not 'performance': timings are noisier. Fix: sudo cpupower frequency-set -g performance
> - Turbo boost enabled: single-thread timings drift with temperature. Fix: echo 1 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo
> - 1-min load average 1.91 > 1.0: other processes were competing for CPU.

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
| Si_relajado.cif | olla-dft | 0.741 | 0.563 | 0.180 | 0.682 | 97 | ✔ | sg 227 vs ref 227; prim atoms 2 vs 2 |
| Si_relajado.cif | ase | 0.575 | 0.418 | 0.136 | 0.519 | 81 | ✔ | sg 227 vs ref 227; prim atoms 2 vs 2 |
| Si_relajado.cif | pymatgen | 0.542 **←fastest** | 0.406 | 0.127 | 0.476 | 78 | ✔ | sg 227 vs ref 227; prim atoms 2 vs 2 |
| ZnO.cif | olla-dft | 0.743 | 0.588 | 0.321 | 0.685 | 97 | ✔ | sg 186 vs ref 186; prim atoms 4 vs 4 |
| ZnO.cif | ase | 0.598 | 0.566 | 0.200 | 0.536 | 81 | ✔ | sg 186 vs ref 186; prim atoms 4 vs 4 |
| ZnO.cif | pymatgen | 0.540 **←fastest** | 0.507 | 0.107 | 0.478 | 78 | ✔ | sg 186 vs ref 186; prim atoms 4 vs 4 |
| grafito.cif | olla-dft | 0.814 | 0.736 | 0.207 | 0.751 | 97 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| grafito.cif | ase | 0.660 | 0.552 | 0.414 | 0.596 | 81 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| grafito.cif | pymatgen | 0.567 **←fastest** | 0.433 | 0.191 | 0.506 | 77 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| hbn.cif | olla-dft | 0.848 | 0.701 | 0.413 | 0.788 | 97 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| hbn.cif | ase | 0.700 | 0.516 | 0.291 | 0.644 | 80 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| hbn.cif | pymatgen | 0.608 **←fastest** | 0.570 | 0.165 | 0.540 | 78 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| POSCAR_NaCl | olla-dft | 0.899 | 0.768 | 0.373 | 0.850 | 97 | ✔ | sg 225 vs ref 225; prim atoms 2 vs 2 |
| POSCAR_NaCl | ase | 0.765 **←fastest** | 0.599 | 0.297 | 0.647 | 80 | ✔ | sg 225 vs ref 225; prim atoms 2 vs 2 |
| POSCAR_NaCl | pymatgen | 1.262 | 1.049 | 0.196 | 1.199 | 120 | ✔ | sg 225 vs ref 225; prim atoms 2 vs 2 |

## High-symmetry k-path from a structure

*Reference is the HPKOT convention (seekpath). Olla-DFT and the seekpath contestant call the same library, so their agreement is expected and only shows the path is passed through intact. ASE and pymatgen implement Setyawan–Curtarolo; a mismatch there is a convention difference, not an error.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | correct | detail |
|---|---|---|---|---|---|---|---|---|
| Si_relajado.cif | olla-dft | 0.790 | 0.673 | 0.300 | 0.734 | 97 | ✔ | segments identical to HPKOT reference |
| Si_relajado.cif | seekpath | 0.642 | 0.565 | 0.057 | 0.574 | 80 | ✔ | segments identical to HPKOT reference |
| Si_relajado.cif | ase | 0.612 **←fastest** | 0.560 | 0.123 | 0.553 | 81 | ✘ | path differs from HPKOT reference (Jaccard 0.60); a different convention, not necessarily an error |
| Si_relajado.cif | pymatgen | 0.726 | 0.612 | 0.079 | 0.664 | 88 | ✘ | path differs from HPKOT reference (Jaccard 0.60); a different convention, not necessarily an error |
| ZnO.cif | olla-dft | 0.796 | 0.724 | 0.112 | 0.740 | 97 | ✔ | segments identical to HPKOT reference |
| ZnO.cif | seekpath | 0.624 **←fastest** | 0.477 | 0.115 | 0.566 | 80 | ✔ | segments identical to HPKOT reference |
| ZnO.cif | ase | 0.625 | 0.563 | 0.051 | 0.567 | 81 | ✔ | segments identical to HPKOT reference |
| ZnO.cif | pymatgen | 0.674 | 0.568 | 0.120 | 0.611 | 88 | ✔ | segments identical to HPKOT reference |
| grafito.cif | olla-dft | 0.798 | 0.738 | 0.063 | 0.741 | 97 | ✔ | segments identical to HPKOT reference |
| grafito.cif | seekpath | 0.632 | 0.557 | 0.159 | 0.563 | 81 | ✔ | segments identical to HPKOT reference |
| grafito.cif | ase | 0.596 **←fastest** | 0.576 | 0.081 | 0.531 | 81 | ✔ | segments identical to HPKOT reference |
| grafito.cif | pymatgen | 0.734 | 0.618 | 0.129 | 0.659 | 88 | ✔ | segments identical to HPKOT reference |
| hbn.cif | olla-dft | 1.081 | 0.730 | 0.329 | 0.939 | 97 | ✔ | segments identical to HPKOT reference |
| hbn.cif | seekpath | 0.653 **←fastest** | 0.483 | 0.346 | 0.596 | 80 | ✔ | segments identical to HPKOT reference |
| hbn.cif | ase | 0.692 | 0.491 | 0.246 | 0.611 | 82 | ✔ | segments identical to HPKOT reference |
| hbn.cif | pymatgen | 0.841 | 0.635 | 0.413 | 0.756 | 88 | ✔ | segments identical to HPKOT reference |
| POSCAR_NaCl | olla-dft | 0.972 | 0.689 | 0.551 | 0.896 | 97 | ✔ | segments identical to HPKOT reference |
| POSCAR_NaCl | seekpath | 0.800 | 0.467 | 0.544 | 0.710 | 80 | ✔ | segments identical to HPKOT reference |
| POSCAR_NaCl | ase | 0.756 **←fastest** | 0.550 | 0.291 | 0.698 | 81 | ✘ | path differs from HPKOT reference (Jaccard 0.09); a different convention, not necessarily an error |
| POSCAR_NaCl | pymatgen | 1.411 | 1.253 | 0.319 | 1.347 | 130 | ✘ | path differs from HPKOT reference (Jaccard 0.60); a different convention, not necessarily an error |

## Birch–Murnaghan fit of an E(V) table (9 points, Si)

*Olla-DFT is called through the fit function behind `olla-dft eos --collect`, because the command reads pw.x outputs, not a bare table. The reference is an analytic linear fit, deliberately a different algorithm from every contestant's curve_fit.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | correct | detail |
|---|---|---|---|---|---|---|---|---|
| EOS.dat | olla-dft | 0.907 | 0.752 | 0.379 | 0.812 | 95 | ✔ | ΔV0=+6.07e-08 Å³, ΔB0=-1.25e-06 GPa |
| EOS.dat | ase | 0.828 **←fastest** | 0.485 | 0.241 | 0.704 | 78 | ✔ | ΔV0=-1.52e-08 Å³, ΔB0=+4.24e-07 GPa; B' not reported |
| EOS.dat | pymatgen | 1.275 | 0.889 | 0.356 | 1.189 | 111 | ✔ | ΔV0=+6.07e-08 Å³, ΔB0=-4.69e-07 GPa |

## Band gap from pw.x output (XML and text)

*Three inputs so that no tool is judged only on the format it prefers: the XML of a 122-k bands run (QE 6.6, no input shipped), and the XML and text output of the same scf run generated with the shipped inputs/Si_scf.in (QE 7.4). Olla-DFT and qeschema read the XML; ASE reads the text output; pymatgen reads neither for eigenvalues.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | correct | detail |
|---|---|---|---|---|---|---|---|---|
| Si.xml.gz | olla-dft | 0.862 **←fastest** | 0.638 | 0.257 | 0.810 | 97 | ✔ | gap 0.4987 eV vs ref 0.4987 eV |
| Si.xml.gz | qeschema | 0.885 | 0.649 | 0.499 | 0.819 | 48 | ✔ | gap 0.49865633045947355 eV vs ref 0.4987 eV |
| Si.xml.gz | ase | — | — | — | — | — | n/a | not supported: ASE reads pw.x text output (espresso-out), not the data-file-schema XML |
| Si.xml.gz | pymatgen | — | — | — | — | — | n/a | not supported: pymatgen.io.pwscf.PWOutput parses energies only (no eigenvalues) and there is no XML parser |
| Si_scf.xml | olla-dft | 0.791 | 0.731 | 0.113 | 0.739 | 96 | ✔ | gap 0.6155 eV vs ref 0.6155 eV |
| Si_scf.xml | qeschema | 0.733 **←fastest** | 0.662 | 0.165 | 0.667 | 48 | ✔ | gap 0.6155421137080532 eV vs ref 0.6155 eV |
| Si_scf.xml | ase | — | — | — | — | — | n/a | not supported: ASE reads pw.x text output (espresso-out), not the data-file-schema XML |
| Si_scf.xml | pymatgen | — | — | — | — | — | n/a | not supported: pymatgen.io.pwscf.PWOutput parses energies only (no eigenvalues) and there is no XML parser |
| Si_scf.out | olla-dft | — | — | — | — | — | n/a | not supported: `olla-dft gap` reads the data-file-schema XML, not the pw.x text output |
| Si_scf.out | qeschema | — | — | — | — | — | n/a | not supported: qeschema reads the data-file-schema XML, not the text output |
| Si_scf.out | ase | 0.552 **←fastest** | 0.523 | 0.029 | 0.489 | 77 | ✔ | gap 0.6154999999999999 eV vs ref 0.6155 eV |
| Si_scf.out | pymatgen | — | — | — | — | — | n/a | not supported: pymatgen.io.pwscf.PWOutput parses energies only (no eigenvalues) and there is no XML parser |

## pw.x scf input from a structure (Si 4×4×4, ZnO 6×6×4, fixed cutoffs)

*Each generated file is parsed back by ASE (reference) to check atoms, volume, k-grid and ecutwfc. Cutoffs and grid are forced equal so the comparison is about correctness and cost, not defaults; other defaults (mixing, smearing) remain each tool's own and show up in the end-to-end stage.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | correct | detail |
|---|---|---|---|---|---|---|---|---|
| Si_relajado.cif | olla-dft | 0.741 | 0.705 | 0.062 | 0.721 | 98 | ✔ | parsed back: 2 atoms, V=39.40187769469898 Å³ (ref 2, 39.4019); k-grid [4, 4, 4] (expected [4, 4, 4]), ecutwfc 30.0 (expected 30) |
| Si_relajado.cif | ase | 0.537 | 0.407 | 0.149 | 0.516 | 78 | ✔ | parsed back: 2 atoms, V=39.401877693982705 Å³ (ref 2, 39.4019); k-grid [4, 4, 4] (expected [4, 4, 4]), ecutwfc 30.0 (expected 30) |
| Si_relajado.cif | pymatgen | 0.516 **←fastest** | 0.425 | 0.045 | 0.494 | 76 | ✔ | parsed back: 2 atoms, V=39.40186569661943 Å³ (ref 2, 39.4019); k-grid [4, 4, 4] (expected [4, 4, 4]), ecutwfc 30.0 (expected 30) |
| ZnO.cif | olla-dft | 0.728 | 0.703 | 0.034 | 0.708 | 98 | ✔ | parsed back: 4 atoms, V=47.61490819424488 Å³ (ref 4, 47.6149); k-grid [6, 6, 4] (expected [6, 6, 4]), ecutwfc 30.0 (expected 30) |
| ZnO.cif | ase | 0.546 | 0.505 | 0.062 | 0.527 | 78 | ✔ | parsed back: 4 atoms, V=47.614908194203096 Å³ (ref 4, 47.6149); k-grid [6, 6, 4] (expected [6, 6, 4]), ecutwfc 30.0 (expected 30) |
| ZnO.cif | pymatgen | 0.500 **←fastest** | 0.397 | 0.034 | 0.478 | 76 | ✔ | parsed back: 4 atoms, V=47.6149158149325 Å³ (ref 4, 47.6149); k-grid [6, 6, 4] (expected [6, 6, 4]), ecutwfc 30.0 (expected 30) |

## Olla-DFT relative to the best supported competitor, every contested cell

Ratios > 1 mean Olla-DFT is slower or heavier. `min` ratio uses the fastest sample of each (robust to background noise); the CI is a 95 % bootstrap of the ratio of medians.

| task | input | vs | wall ratio (median) | 95 % CI | wall ratio (min) | RSS ratio |
|---|---|---|---|---|---|---|
| symmetry | Si_relajado.cif | pymatgen | 1.37 | 1.07–1.75 | 1.38 | 1.25 |
| symmetry | ZnO.cif | pymatgen | 1.38 | 1.25–1.64 | 1.16 | 1.25 |
| symmetry | grafito.cif | pymatgen | 1.44 | 1.34–1.79 | 1.70 | 1.25 |
| symmetry | hbn.cif | pymatgen | 1.40 | 1.16–1.74 | 1.23 | 1.25 |
| symmetry | POSCAR_NaCl | ase | 1.18 | 0.95–1.57 | 1.28 | 1.21 |
| kpath | Si_relajado.cif | ase | 1.29 | 1.17–1.68 | 1.20 | 1.20 |
| kpath | ZnO.cif | seekpath | 1.28 | 1.08–1.40 | 1.52 | 1.20 |
| kpath | grafito.cif | ase | 1.34 | 1.22–1.39 | 1.28 | 1.20 |
| kpath | hbn.cif | seekpath | 1.66 | 1.10–1.88 | 1.51 | 1.20 |
| kpath | POSCAR_NaCl | ase | 1.28 | 1.02–2.00 | 1.25 | 1.21 |
| eos | EOS.dat | ase | 1.10 | 0.97–1.53 | 1.55 | 1.22 |
| bandgap | Si.xml.gz | qeschema | 0.97 | 0.72–1.25 | 0.98 | 1.99 |
| bandgap | Si_scf.xml | qeschema | 1.08 | 0.98–1.22 | 1.10 | 2.01 |
| inputgen | Si_relajado.cif | pymatgen | 1.44 | 1.39–1.57 | 1.66 | 1.29 |
| inputgen | ZnO.cif | pymatgen | 1.46 | 1.39–1.50 | 1.77 | 1.28 |

**Summary:** Olla-DFT is slower than the best supported competitor in 14 of 15 contested cells (geometric-mean wall ratio 1.30×, min-based 1.35×) and uses more peak memory in 15 of 15 (geometric mean 1.31×).

## End to end with pw.x (same binary, same k-grid and cutoffs, inputs from each tool)

| tool | k-grid | irreducible k | ecutwfc | total energy (Ry) | SCF iterations | pw.x wall s (median of n) | n | input generated by |
|---|---|---|---|---|---|---|---|---|
| ase | [4, 4, 4] | 13 | 30.0 | -22.82476715 | 8 | 3.55 | 5 | ase.io.write(format='espresso-in') |
| olla-dft | [4, 4, 4] | 13 | 30.0 | -22.82476715 | 14 | 4.70 | 5 | cli gen -p scf --kspacing 0.5250 --ecutwfc 30 --ecutrho 240 --insulator (no explicit k-grid option) |
| pymatgen | [4, 4, 4] | 24 | 30.0 | -22.82476712 | 7 | 3.76 | 5 | pymatgen.io.pwscf.PWInput |

Spread of total energies across tools: 3.00e-08 Ry. Same grid and cutoffs should agree to ≲ 1e-6 Ry; the number of irreducible k-points may differ if a tool writes the cell differently, which is itself a difference in the input.

## Coverage matrix

| task | olla-dft | ase | pymatgen | qeschema | seekpath |
|---|---|---|---|---|---|
| symmetry | ✔ | ✔ | ✔ | — | — |
| kpath | ✔ | ✔ | ✔ | — | ✔ |
| eos | ✔ | ✔ | ✔ | — | — |
| bandgap | ✔ 2/3 inputs | ✔ 1/3 inputs | ✘ n/a | ✔ 2/3 inputs | — |
| inputgen | ✔ | ✔ | ✔ | — | — |

## Areas of opportunity for Olla-DFT (generated automatically; threshold 1.15×, same rule for every tool)

- symmetry/Si_relajado.cif: 1.37× the wall time of pymatgen (95 % CI 1.07–1.75)
- symmetry/Si_relajado.cif: 1.25× the peak memory of the lightest competitor
- symmetry/ZnO.cif: 1.38× the wall time of pymatgen (95 % CI 1.25–1.64)
- symmetry/ZnO.cif: 1.25× the peak memory of the lightest competitor
- symmetry/grafito.cif: 1.44× the wall time of pymatgen (95 % CI 1.34–1.79)
- symmetry/grafito.cif: 1.25× the peak memory of the lightest competitor
- symmetry/hbn.cif: 1.40× the wall time of pymatgen (95 % CI 1.16–1.74)
- symmetry/hbn.cif: 1.25× the peak memory of the lightest competitor
- symmetry/POSCAR_NaCl: 1.18× the wall time of ase (95 % CI 0.95–1.57)
- symmetry/POSCAR_NaCl: 1.21× the peak memory of the lightest competitor
- kpath/Si_relajado.cif: 1.29× the wall time of ase (95 % CI 1.17–1.68)
- kpath/Si_relajado.cif: 1.20× the peak memory of the lightest competitor
- kpath/ZnO.cif: 1.28× the wall time of seekpath (95 % CI 1.08–1.40)
- kpath/ZnO.cif: 1.20× the peak memory of the lightest competitor
- kpath/grafito.cif: 1.34× the wall time of ase (95 % CI 1.22–1.39)
- kpath/grafito.cif: 1.20× the peak memory of the lightest competitor
- kpath/hbn.cif: 1.66× the wall time of seekpath (95 % CI 1.10–1.88)
- kpath/hbn.cif: 1.20× the peak memory of the lightest competitor
- kpath/POSCAR_NaCl: 1.28× the wall time of ase (95 % CI 1.02–2.00)
- kpath/POSCAR_NaCl: 1.21× the peak memory of the lightest competitor
- eos/EOS.dat: 1.22× the peak memory of the lightest competitor
- bandgap/Si.xml.gz: 1.99× the peak memory of the lightest competitor
- bandgap/Si_scf.xml: 2.01× the peak memory of the lightest competitor
- inputgen/Si_relajado.cif: 1.44× the wall time of pymatgen (95 % CI 1.39–1.57)
- inputgen/Si_relajado.cif: 1.29× the peak memory of the lightest competitor
- inputgen/ZnO.cif: 1.46× the wall time of pymatgen (95 % CI 1.39–1.50)
- inputgen/ZnO.cif: 1.28× the peak memory of the lightest competitor
- Olla-DFT uses more peak memory in every contested cell (geometric mean 1.31×)
- end-to-end/Si: Olla-DFT's input needed 14 SCF iterations vs 7 for the best competitor at the same energy (its defaults, e.g. mixing_beta, differ)
- end-to-end/Si: pw.x took 4.70 s on Olla-DFT's input vs 3.55 s on the best competitor's

## Known limitations of this benchmark

- One consumer laptop, hybrid CPU: absolute times are only comparable within one run; compare ratios across runs.
- Post-processing tasks are small; import time dominates and favours light dependency trees. That is a real cost for a CLI tool, but it is not algorithmic speed.
- Only tasks every tool can express with the same inputs are compared; Olla-DFT features without a counterpart are not benchmarked here, and features of the other tools that Olla-DFT lacks are visible in the coverage matrix.
- symmetry and kpath references share a backend with some contestants (stated in the notes); eos and bandgap references are independent code.
- The end-to-end stage uses one small system (Si, 2 atoms).
