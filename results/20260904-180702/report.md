# Olla-DFT benchmark — run 20260904-180702

*Generated from `results.json`; every number is recomputable with `python bench.py verify`.*

## Environment

- CPU: 12th Gen Intel(R) Core(TM) i5-12450H (12 logical CPUs), pinned to CPU 0
- RAM: 7.4 GiB; governor `powersave`; turbo disabled: `False`
- OS: Linux-7.1.5-76070105-generic-x86_64-with-glibc2.39; Python 3.12.3; pw.x: Program PWSCF v.7.4 starts on  4Sep2026 at 18: 7: 3
- Packages: Pygments 2.21.0, ase 3.29.0, bibtexparser 1.4.4, certifi 2026.7.22, charset-normalizer 3.5.1, cloudpickle 3.1.2, contourpy 1.3.3, cycler 0.12.1, elementpath 4.8.0, fonttools 4.64.0, idna 3.19, iniconfig 2.3.0, joblib 1.6.0, kiwisolver 1.5.1, lxml 6.1.3, matplotlib 3.11.1, monty 2026.7.16, mpmath 1.3.0, narwhals 2.25.0, networkx 3.6.1, numpy 2.2.6, olla-dft 1.1.1, orjson 3.12.0, packaging 26.3, palettable 3.3.3, pandas 3.0.5, pillow 12.3.0, pip 26.2.1, plotly 7.0.0, pluggy 1.6.0, pyflakes 3.4.0, pymatgen 2026.5.4, pymatgen-core 2026.8.30, pyparsing 3.3.2, pytest 9.1.1, python-dateutil 2.9.0.post0, qeschema 1.5.1, requests 2.34.2, ruamel.yaml 0.19.1, scipy 1.18.1, seekpath 2.2.1, six 1.17.0, spglib 2.7.0, sympy 1.14.0, tabulate 0.10.0, tqdm 4.70.0, typing_extensions 4.16.0, uncertainties 3.2.3, urllib3 2.7.0, xmlschema 2.3.1
- Olla-DFT source: `https://github.com/jorgegonzalezsevilla/olla-dft` @ `d244d96e6ce6aa3ca5669a4fe2cc039ca04b0dc9`
- Repetitions per cell: 15 (+1 warm-up, discarded); threads per process: 1; tool order shuffled per repetition (seed 20260904)
- End-to-end repetitions: 5; opportunity threshold: 1.15× (stated here, applied identically to time and memory)
- Load average at start / end: [2.03125, 1.9658203125, 1.82958984375] / [1.88330078125, 2.15234375, 2.07177734375]

**Run status: complete**

> **Environment warnings**

> - CPU governor is 'powersave', not 'performance': timings are noisier. Fix: sudo cpupower frequency-set -g performance
> - Turbo boost enabled: single-thread timings drift with temperature. Fix: echo 1 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo
> - 1-min load average 2.03 > 1.0: other processes were competing for CPU.

## How to read the tables

Wall time is the median of a fresh process per repetition (imports included, because that is what the
command line costs). CPU is user+system time; RSS is peak resident memory. `correct` is the deterministic
grade against the reference described in each task's note; where the reference shares a backend with a
contestant, the note says so and the grade only shows the wrapper passes the result through. `—` means
the tool does not cover the task; that is a coverage fact, not a failure, and such cells are excluded from
every speed or memory comparison.

## Structure parsing and symmetry (file → space group, primitive cell)

*Reference shares its backend (spglib) with all three contestants: the grade checks that each wrapper preserves the result, not the algorithm. Timing measures wrapper cost (import + parse + report).*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | n | failures | correct | detail |
|---|---|---|---|---|---|---|---|---|---|---|
| Si_relajado.cif | olla-dft | 0.894 | 0.837 | 0.071 | 0.890 | 97 | 15 | 0 | ✔ | sg 227 vs ref 227; prim atoms 2 vs 2 |
| Si_relajado.cif | ase | 0.721 | 0.640 | 0.151 | 0.708 | 81 | 15 | 0 | ✔ | sg 227 vs ref 227; prim atoms 2 vs 2 |
| Si_relajado.cif | pymatgen | 0.611 **←fastest** | 0.569 | 0.040 | 0.604 | 78 | 15 | 0 | ✔ | sg 227 vs ref 227; prim atoms 2 vs 2 |
| ZnO.cif | olla-dft | 0.833 | 0.793 | 0.052 | 0.832 | 97 | 15 | 0 | ✔ | sg 186 vs ref 186; prim atoms 4 vs 4 |
| ZnO.cif | ase | 0.627 | 0.599 | 0.031 | 0.619 | 81 | 15 | 0 | ✔ | sg 186 vs ref 186; prim atoms 4 vs 4 |
| ZnO.cif | pymatgen | 0.569 **←fastest** | 0.548 | 0.081 | 0.563 | 78 | 15 | 0 | ✔ | sg 186 vs ref 186; prim atoms 4 vs 4 |
| grafito.cif | olla-dft | 0.863 | 0.812 | 0.093 | 0.859 | 97 | 15 | 0 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| grafito.cif | ase | 0.630 | 0.600 | 0.050 | 0.627 | 81 | 15 | 0 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| grafito.cif | pymatgen | 0.570 **←fastest** | 0.559 | 0.021 | 0.565 | 78 | 15 | 0 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| hbn.cif | olla-dft | 0.559 | 0.529 | 0.051 | 0.554 | 97 | 15 | 0 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| hbn.cif | ase | 0.418 | 0.407 | 0.053 | 0.413 | 81 | 15 | 0 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| hbn.cif | pymatgen | 0.377 **←fastest** | 0.364 | 0.030 | 0.375 | 78 | 15 | 0 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| POSCAR_NaCl | olla-dft | 0.662 | 0.596 | 0.116 | 0.652 | 97 | 15 | 0 | ✔ | sg 225 vs ref 225; prim atoms 2 vs 2 |
| POSCAR_NaCl | ase | 0.498 **←fastest** | 0.447 | 0.034 | 0.488 | 80 | 15 | 0 | ✔ | sg 225 vs ref 225; prim atoms 2 vs 2 |
| POSCAR_NaCl | pymatgen | 1.056 | 0.929 | 0.199 | 1.042 | 121 | 15 | 0 | ✔ | sg 225 vs ref 225; prim atoms 2 vs 2 |

## High-symmetry k-path from a structure

*Reference is the HPKOT convention (seekpath). Olla-DFT and the seekpath contestant call the same library, so their agreement is expected and only shows the path is passed through intact. ASE and pymatgen implement Setyawan–Curtarolo; a mismatch there is a convention difference, not an error.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | n | failures | correct | detail |
|---|---|---|---|---|---|---|---|---|---|---|
| Si_relajado.cif | olla-dft | 0.641 | 0.539 | 0.120 | 0.635 | 98 | 15 | 0 | ✔ | HPKOT segments and coordinates match |
| Si_relajado.cif | seekpath | 0.477 **←fastest** | 0.417 | 0.061 | 0.467 | 81 | 15 | 0 | ✔ | HPKOT segments and coordinates match |
| Si_relajado.cif | ase | 0.468 | 0.407 | 0.091 | 0.458 | 82 | 15 | 0 | other convention | different convention; not compared with HPKOT |
| Si_relajado.cif | pymatgen | 0.530 | 0.479 | 0.080 | 0.523 | 89 | 15 | 0 | other convention | different convention; not compared with HPKOT |
| ZnO.cif | olla-dft | 0.691 | 0.529 | 0.121 | 0.681 | 98 | 15 | 0 | ✔ | HPKOT segments and coordinates match |
| ZnO.cif | seekpath | 0.519 **←fastest** | 0.437 | 0.080 | 0.510 | 81 | 15 | 0 | ✔ | HPKOT segments and coordinates match |
| ZnO.cif | ase | 0.499 | 0.408 | 0.100 | 0.494 | 82 | 15 | 0 | other convention | different convention; not compared with HPKOT |
| ZnO.cif | pymatgen | 0.559 | 0.448 | 0.102 | 0.550 | 89 | 15 | 0 | other convention | different convention; not compared with HPKOT |
| grafito.cif | olla-dft | 0.569 | 0.519 | 0.060 | 0.559 | 98 | 15 | 0 | ✔ | HPKOT segments and coordinates match |
| grafito.cif | seekpath | 0.428 **←fastest** | 0.397 | 0.070 | 0.424 | 81 | 15 | 0 | ✔ | HPKOT segments and coordinates match |
| grafito.cif | ase | 0.417 | 0.397 | 0.059 | 0.411 | 82 | 15 | 0 | other convention | different convention; not compared with HPKOT |
| grafito.cif | pymatgen | 0.468 | 0.438 | 0.091 | 0.466 | 89 | 15 | 0 | other convention | different convention; not compared with HPKOT |
| hbn.cif | olla-dft | 0.631 | 0.566 | 0.054 | 0.623 | 98 | 15 | 0 | ✔ | HPKOT segments and coordinates match |
| hbn.cif | seekpath | 0.468 **←fastest** | 0.414 | 0.050 | 0.460 | 81 | 15 | 0 | ✔ | HPKOT segments and coordinates match |
| hbn.cif | ase | 0.458 | 0.417 | 0.041 | 0.450 | 82 | 15 | 0 | other convention | different convention; not compared with HPKOT |
| hbn.cif | pymatgen | 0.509 | 0.455 | 0.051 | 0.504 | 89 | 15 | 0 | other convention | different convention; not compared with HPKOT |
| POSCAR_NaCl | olla-dft | 0.589 | 0.538 | 0.108 | 0.580 | 98 | 15 | 0 | ✔ | HPKOT segments and coordinates match |
| POSCAR_NaCl | seekpath | 0.447 **←fastest** | 0.414 | 0.068 | 0.441 | 81 | 15 | 0 | ✔ | HPKOT segments and coordinates match |
| POSCAR_NaCl | ase | 0.417 | 0.394 | 0.074 | 0.412 | 82 | 15 | 0 | other convention | different convention; not compared with HPKOT |
| POSCAR_NaCl | pymatgen | 1.080 | 0.968 | 0.135 | 1.072 | 131 | 15 | 0 | other convention | different convention; not compared with HPKOT |

## Birch–Murnaghan fit of an E(V) table (9 points, Si)

*Olla-DFT is called through the fit function behind `olla-dft eos --collect`, because the command reads pw.x outputs, not a bare table. EOS.dat is the table exported by `olla-dft eos Si.cif --run` in examples/demo_calculo of the Olla-DFT repository (QE 6.6, 9 volumes, ±10 %). The reference is an analytic linear fit, deliberately a different algorithm from every contestant's curve_fit.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | n | failures | correct | detail |
|---|---|---|---|---|---|---|---|---|---|---|
| EOS.dat | olla-dft | 0.527 | 0.466 | 0.079 | 0.516 | 92 | 15 | 0 | ✔ | ΔV0=+6.07e-08 Å³, ΔB0=-1.25e-06 GPa |
| EOS.dat | ase | 0.448 **←fastest** | 0.384 | 0.048 | 0.441 | 79 | 15 | 0 | ✔ | ΔV0=-1.52e-08 Å³, ΔB0=+4.24e-07 GPa; B' not reported |
| EOS.dat | pymatgen | 0.782 | 0.700 | 0.066 | 0.775 | 113 | 15 | 0 | ✔ | ΔV0=+6.07e-08 Å³, ΔB0=-4.69e-07 GPa |

## Band gap from pw.x output (XML and text)

*The XML and the text output of the same scf run, generated with the shipped inputs/Si_scf.in (QE 7.4), so that each format counts once and no tool is judged only on the format it prefers. Olla-DFT and qeschema read the XML; ASE reads the text output; pymatgen reads neither for eigenvalues.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | n | failures | correct | detail |
|---|---|---|---|---|---|---|---|---|---|---|
| Si_scf.xml | olla-dft | 0.293 **←fastest** | 0.265 | 0.012 | 0.285 | 52 | 15 | 0 | ✔ | gap 0.6155 eV vs ref 0.6155 eV; VBM/CBM checked |
| Si_scf.xml | qeschema | 0.548 | 0.507 | 0.037 | 0.547 | 48 | 15 | 0 | ✔ | gap 0.6155421137080532 eV vs ref 0.6155 eV; VBM/CBM checked |
| Si_scf.xml | ase | — | — | — | — | — | 15 | 0 | n/a | not supported: ASE reads pw.x text output (espresso-out), not the data-file-schema XML |
| Si_scf.xml | pymatgen | — | — | — | — | — | 15 | 0 | n/a | not supported: pymatgen.io.pwscf.PWOutput parses energies only (no eigenvalues) and there is no XML parser |
| Si_scf.out | olla-dft | — | — | — | — | — | 15 | 0 | n/a | not supported: `olla-dft gap` reads the data-file-schema XML, not the pw.x text output |
| Si_scf.out | qeschema | — | — | — | — | — | 15 | 0 | n/a | not supported: qeschema reads the data-file-schema XML, not the text output |
| Si_scf.out | ase | 0.475 **←fastest** | 0.407 | 0.162 | 0.467 | 79 | 15 | 0 | ✔ | gap 0.6154999999999999 eV vs ref 0.6155 eV; VBM/CBM checked |
| Si_scf.out | pymatgen | — | — | — | — | — | 15 | 0 | n/a | not supported: pymatgen.io.pwscf.PWOutput parses energies only (no eigenvalues) and there is no XML parser |

## pw.x scf input from a structure (Si 4×4×4, ZnO 6×6×4, fixed cutoffs)

*Each generated file is parsed back by ASE to check species, positions, cell metric, pseudopotentials, grid/shift, occupations and both cutoffs. Cutoffs and grid are forced equal so the comparison is about correctness and cost, not defaults; other defaults (mixing, smearing) remain each tool's own and show up in the end-to-end stage.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | n | failures | correct | detail |
|---|---|---|---|---|---|---|---|---|---|---|
| Si_relajado.cif | olla-dft | 0.620 | 0.550 | 0.143 | 0.610 | 99 | 15 | 0 | ✔ | geometry, species, pseudos, grid/shift, occupations and cutoffs match |
| Si_relajado.cif | ase | 0.437 | 0.397 | 0.071 | 0.432 | 80 | 15 | 0 | ✔ | geometry, species, pseudos, grid/shift, occupations and cutoffs match |
| Si_relajado.cif | pymatgen | 0.417 **←fastest** | 0.366 | 0.061 | 0.407 | 77 | 15 | 0 | ✔ | geometry, species, pseudos, grid/shift, occupations and cutoffs match |
| ZnO.cif | olla-dft | 0.659 | 0.560 | 0.070 | 0.652 | 98 | 15 | 0 | ✔ | geometry, species, pseudos, grid/shift, occupations and cutoffs match |
| ZnO.cif | ase | 0.445 | 0.407 | 0.071 | 0.441 | 80 | 15 | 0 | ✔ | geometry, species, pseudos, grid/shift, occupations and cutoffs match |
| ZnO.cif | pymatgen | 0.417 **←fastest** | 0.367 | 0.040 | 0.414 | 78 | 15 | 0 | ✔ | geometry, species, pseudos, grid/shift, occupations and cutoffs match |

## Olla-DFT relative to the best supported competitor, every contested cell

Ratios > 1 mean Olla-DFT is slower or heavier. `min` ratio uses the fastest sample of each (robust to background noise); the CI is a 95 % bootstrap of the ratio of medians, conditional on the chosen competitor; descriptive, not a multiple-comparison significance test.

| task | input | vs | wall ratio (median) | 95 % CI | wall ratio (min) | RSS ratio |
|---|---|---|---|---|---|---|
| symmetry | Si_relajado.cif | pymatgen | 1.46 | 1.39–1.54 | 1.47 | 1.25 |
| symmetry | ZnO.cif | pymatgen | 1.46 | 1.36–1.52 | 1.45 | 1.25 |
| symmetry | grafito.cif | pymatgen | 1.51 | 1.43–1.58 | 1.45 | 1.25 |
| symmetry | hbn.cif | pymatgen | 1.48 | 1.35–1.50 | 1.45 | 1.25 |
| symmetry | POSCAR_NaCl | ase | 1.33 | 1.23–1.46 | 1.33 | 1.21 |
| kpath | Si_relajado.cif | seekpath | 1.34 | 1.21–1.50 | 1.29 | 1.20 |
| kpath | ZnO.cif | seekpath | 1.33 | 1.21–1.48 | 1.21 | 1.20 |
| kpath | grafito.cif | seekpath | 1.33 | 1.17–1.41 | 1.31 | 1.20 |
| kpath | hbn.cif | seekpath | 1.35 | 1.28–1.46 | 1.37 | 1.20 |
| kpath | POSCAR_NaCl | seekpath | 1.32 | 1.21–1.45 | 1.30 | 1.21 |
| eos | EOS.dat | ase | 1.17 | 1.11–1.33 | 1.21 | 1.17 |
| bandgap | Si_scf.xml | qeschema | 0.54 | 0.50–0.54 | 0.52 | 1.08 |
| inputgen | Si_relajado.cif | pymatgen | 1.49 | 1.35–1.71 | 1.50 | 1.28 |
| inputgen | ZnO.cif | pymatgen | 1.58 | 1.49–1.68 | 1.53 | 1.27 |

**Summary:** Olla-DFT is slower than the best supported competitor in 13 of 14 contested cells (geometric-mean wall ratio 1.30×, min-based 1.28×) and uses more peak memory in 14 of 14 (geometric mean 1.21×).

## End to end with pw.x (same binary, same k-grid and cutoffs, inputs from each tool)

| tool | k-grid | irreducible k | ecutwfc | total energy (Ry) | SCF iterations | pw.x wall s (median of n) | n | input generated by |
|---|---|---|---|---|---|---|---|---|
| ase | [4, 4, 4] | [13] | 30 | -22.82476715 | 8 | 3.17 | 5 | ase.io.write(format='espresso-in') |
| olla-dft | [4, 4, 4] | [13] | 30 | -22.82476715 | 8 | 3.47 | 5 | cli gen --kgrid 4 4 4 |
| pymatgen | [4, 4, 4] | [24] | 30 | -22.82476712 | 7 | 3.67 | 5 | pymatgen.io.pwscf.PWInput |

Spread of all total energies across tools and repetitions: 3.00e-08 Ry. Same grid and cutoffs should agree to ≲ 1e-6 Ry; the number of irreducible k-points may differ if a tool writes the cell differently, which is itself a difference in the input.

## Coverage matrix

| task | olla-dft | ase | pymatgen | qeschema | seekpath |
|---|---|---|---|---|---|
| symmetry | ✔ | ✔ | ✔ | — | — |
| kpath | ✔ | ✔ | ✔ | — | ✔ |
| eos | ✔ | ✔ | ✔ | — | — |
| bandgap | ✔ 1/2 inputs | ✔ 1/2 inputs | ✘ n/a | ✔ 1/2 inputs | — |
| inputgen | ✔ | ✔ | ✔ | — | — |

## Areas of opportunity for Olla-DFT (generated automatically; threshold 1.15×, same rule for every tool)

- symmetry/Si_relajado.cif: 1.46× the wall time of pymatgen (95 % CI 1.39–1.54)
- symmetry/Si_relajado.cif: 1.25× the peak memory of the lightest competitor
- symmetry/ZnO.cif: 1.46× the wall time of pymatgen (95 % CI 1.36–1.52)
- symmetry/ZnO.cif: 1.25× the peak memory of the lightest competitor
- symmetry/grafito.cif: 1.51× the wall time of pymatgen (95 % CI 1.43–1.58)
- symmetry/grafito.cif: 1.25× the peak memory of the lightest competitor
- symmetry/hbn.cif: 1.48× the wall time of pymatgen (95 % CI 1.35–1.50)
- symmetry/hbn.cif: 1.25× the peak memory of the lightest competitor
- symmetry/POSCAR_NaCl: 1.33× the wall time of ase (95 % CI 1.23–1.46)
- symmetry/POSCAR_NaCl: 1.21× the peak memory of the lightest competitor
- kpath/Si_relajado.cif: 1.34× the wall time of seekpath (95 % CI 1.21–1.50)
- kpath/Si_relajado.cif: 1.20× the peak memory of the lightest competitor
- kpath/ZnO.cif: 1.33× the wall time of seekpath (95 % CI 1.21–1.48)
- kpath/ZnO.cif: 1.20× the peak memory of the lightest competitor
- kpath/grafito.cif: 1.33× the wall time of seekpath (95 % CI 1.17–1.41)
- kpath/grafito.cif: 1.20× the peak memory of the lightest competitor
- kpath/hbn.cif: 1.35× the wall time of seekpath (95 % CI 1.28–1.46)
- kpath/hbn.cif: 1.20× the peak memory of the lightest competitor
- kpath/POSCAR_NaCl: 1.32× the wall time of seekpath (95 % CI 1.21–1.45)
- kpath/POSCAR_NaCl: 1.21× the peak memory of the lightest competitor
- eos/EOS.dat: 1.17× the wall time of ase (95 % CI 1.11–1.33)
- eos/EOS.dat: 1.17× the peak memory of the lightest competitor
- inputgen/Si_relajado.cif: 1.49× the wall time of pymatgen (95 % CI 1.35–1.71)
- inputgen/Si_relajado.cif: 1.28× the peak memory of the lightest competitor
- inputgen/ZnO.cif: 1.58× the wall time of pymatgen (95 % CI 1.49–1.68)
- inputgen/ZnO.cif: 1.27× the peak memory of the lightest competitor
- Olla-DFT uses more peak memory in every contested cell (geometric mean 1.21×)

## Known limitations of this benchmark

- One consumer laptop, hybrid CPU: absolute times are only comparable within one run; compare ratios across runs.
- Post-processing tasks are small; import time dominates and favours light dependency trees. That is a real cost for a CLI tool, but it is not algorithmic speed.
- Only tasks every tool can express with the same inputs are compared; Olla-DFT features without a counterpart are not benchmarked here, and features of the other tools that Olla-DFT lacks are visible in the coverage matrix.
- symmetry and kpath references share a backend with some contestants (stated in the notes); eos and bandgap references are independent code.
- The end-to-end stage uses one small system (Si, 2 atoms).
