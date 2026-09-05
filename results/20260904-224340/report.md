# Olla-DFT benchmark — run 20260904-224340

*Generated from `results.json`; every number is recomputable with `python bench.py verify`.*

## Environment

- CPU: 12th Gen Intel(R) Core(TM) i5-12450H (12 logical CPUs), pinned to CPU 0
- RAM: 7.4 GiB; governor `performance`; turbo disabled: `False`
- OS: Linux-7.1.5-76070105-generic-x86_64-with-glibc2.39; Python 3.12.3; pw.x: see retained QE output artifacts
- Packages: Pygments 2.21.0, ase 3.29.0, bibtexparser 1.4.4, certifi 2026.7.22, charset-normalizer 3.5.1, cloudpickle 3.1.2, contourpy 1.3.3, cycler 0.12.1, elementpath 4.8.0, fonttools 4.64.0, idna 3.19, iniconfig 2.3.0, joblib 1.6.0, kiwisolver 1.5.1, lxml 6.1.3, matplotlib 3.11.1, monty 2026.7.16, mpmath 1.3.0, narwhals 2.25.0, networkx 3.6.1, numpy 2.2.6, olla-dft 1.3.1, orjson 3.12.0, packaging 26.3, palettable 3.3.3, pandas 3.0.5, pillow 12.3.0, pip 26.2.1, plotly 7.0.0, pluggy 1.6.0, pyflakes 3.4.0, pymatgen 2026.5.4, pymatgen-core 2026.8.30, pyparsing 3.3.2, pytest 9.1.1, python-dateutil 2.9.0.post0, qeschema 1.5.1, requests 2.34.2, ruamel.yaml 0.19.1, scipy 1.18.1, seekpath 2.2.1, six 1.17.0, spglib 2.7.0, sympy 1.14.0, tabulate 0.10.0, tqdm 4.70.0, typing_extensions 4.16.0, uncertainties 3.2.3, urllib3 2.7.0, xmlschema 2.3.1
- Olla-DFT source: `file:///tmp/olla-perf-dist-en/olla_dft-1.3.1-py3-none-any.whl` @ `?`
- Repetitions per cell: 15 (+1 warm-up, discarded); threads per process: 1; tool order shuffled per repetition (seed 20260905)
- End-to-end repetitions: 5; opportunity threshold: 1.15× (stated here, applied identically to time and memory)
- Load average at start / end: [2.23974609375, 2.7412109375, 2.47412109375] / [3.1044921875, 3.18798828125, 2.861328125]

**Run status: complete**

> **Environment warnings**

> - Turbo boost enabled: single-thread timings drift with temperature. Fix: echo 1 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo
> - 1-min load average 2.24 > 1.0: other processes were competing for CPU.

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
| Si_relajado.cif | olla-dft | 0.457 | 0.435 | 0.041 | 0.450 | 84 | 15 | 0 | ✔ | sg 227 vs ref 227; prim atoms 2 vs 2 |
| Si_relajado.cif | ase | 0.426 | 0.405 | 0.030 | 0.423 | 81 | 15 | 0 | ✔ | sg 227 vs ref 227; prim atoms 2 vs 2 |
| Si_relajado.cif | pymatgen | 0.395 **←fastest** | 0.375 | 0.029 | 0.386 | 78 | 15 | 0 | ✔ | sg 227 vs ref 227; prim atoms 2 vs 2 |
| ZnO.cif | olla-dft | 0.476 | 0.425 | 0.091 | 0.472 | 84 | 15 | 0 | ✔ | sg 186 vs ref 186; prim atoms 4 vs 4 |
| ZnO.cif | ase | 0.426 | 0.394 | 0.050 | 0.420 | 81 | 15 | 0 | ✔ | sg 186 vs ref 186; prim atoms 4 vs 4 |
| ZnO.cif | pymatgen | 0.386 **←fastest** | 0.355 | 0.061 | 0.378 | 78 | 15 | 0 | ✔ | sg 186 vs ref 186; prim atoms 4 vs 4 |
| grafito.cif | olla-dft | 0.457 | 0.417 | 0.051 | 0.452 | 84 | 15 | 0 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| grafito.cif | ase | 0.407 | 0.384 | 0.030 | 0.404 | 81 | 15 | 0 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| grafito.cif | pymatgen | 0.374 **←fastest** | 0.356 | 0.030 | 0.369 | 78 | 15 | 0 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| hbn.cif | olla-dft | 0.445 | 0.424 | 0.102 | 0.440 | 84 | 15 | 0 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| hbn.cif | ase | 0.406 | 0.385 | 0.041 | 0.402 | 81 | 15 | 0 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| hbn.cif | pymatgen | 0.366 **←fastest** | 0.354 | 0.052 | 0.362 | 78 | 15 | 0 | ✔ | sg 194 vs ref 194; prim atoms 4 vs 4 |
| POSCAR_NaCl | olla-dft | 0.466 **←fastest** | 0.425 | 0.102 | 0.458 | 83 | 15 | 0 | ✔ | sg 225 vs ref 225; prim atoms 2 vs 2 |
| POSCAR_NaCl | ase | 0.497 | 0.404 | 0.328 | 0.484 | 80 | 15 | 0 | ✔ | sg 225 vs ref 225; prim atoms 2 vs 2 |
| POSCAR_NaCl | pymatgen | 0.912 | 0.832 | 0.365 | 0.909 | 121 | 15 | 0 | ✔ | sg 225 vs ref 225; prim atoms 2 vs 2 |

## High-symmetry k-path from a structure

*Reference is the HPKOT convention (seekpath). Olla-DFT and the seekpath contestant call the same library, so their agreement is expected and only shows the path is passed through intact. ASE and pymatgen implement Setyawan–Curtarolo; a mismatch there is a convention difference, not an error.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | n | failures | correct | detail |
|---|---|---|---|---|---|---|---|---|---|---|
| Si_relajado.cif | olla-dft | 0.506 | 0.446 | 0.161 | 0.497 | 84 | 15 | 0 | ✔ | HPKOT segments and coordinates match |
| Si_relajado.cif | seekpath | 0.467 **←fastest** | 0.386 | 0.091 | 0.457 | 81 | 15 | 0 | ✔ | HPKOT segments and coordinates match |
| Si_relajado.cif | ase | 0.436 | 0.376 | 0.171 | 0.428 | 82 | 15 | 0 | other convention | different convention; not compared with HPKOT |
| Si_relajado.cif | pymatgen | 0.527 | 0.447 | 0.307 | 0.522 | 89 | 15 | 0 | other convention | different convention; not compared with HPKOT |
| ZnO.cif | olla-dft | 0.507 | 0.477 | 0.060 | 0.502 | 84 | 15 | 0 | ✔ | HPKOT segments and coordinates match |
| ZnO.cif | seekpath | 0.466 **←fastest** | 0.426 | 0.051 | 0.463 | 81 | 15 | 0 | ✔ | HPKOT segments and coordinates match |
| ZnO.cif | ase | 0.457 | 0.416 | 0.060 | 0.452 | 82 | 15 | 0 | other convention | different convention; not compared with HPKOT |
| ZnO.cif | pymatgen | 0.507 | 0.457 | 0.051 | 0.501 | 89 | 15 | 0 | other convention | different convention; not compared with HPKOT |
| grafito.cif | olla-dft | 0.477 | 0.437 | 0.039 | 0.468 | 84 | 15 | 0 | ✔ | HPKOT segments and coordinates match |
| grafito.cif | seekpath | 0.416 **←fastest** | 0.396 | 0.031 | 0.410 | 81 | 15 | 0 | ✔ | HPKOT segments and coordinates match |
| grafito.cif | ase | 0.426 | 0.396 | 0.051 | 0.421 | 82 | 15 | 0 | other convention | different convention; not compared with HPKOT |
| grafito.cif | pymatgen | 0.466 | 0.437 | 0.030 | 0.460 | 89 | 15 | 0 | other convention | different convention; not compared with HPKOT |
| hbn.cif | olla-dft | 0.447 | 0.427 | 0.041 | 0.443 | 84 | 15 | 0 | ✔ | HPKOT segments and coordinates match |
| hbn.cif | seekpath | 0.407 **←fastest** | 0.386 | 0.061 | 0.402 | 81 | 15 | 0 | ✔ | HPKOT segments and coordinates match |
| hbn.cif | ase | 0.406 | 0.386 | 0.040 | 0.402 | 82 | 15 | 0 | other convention | different convention; not compared with HPKOT |
| hbn.cif | pymatgen | 0.447 | 0.436 | 0.031 | 0.444 | 89 | 15 | 0 | other convention | different convention; not compared with HPKOT |
| POSCAR_NaCl | olla-dft | 0.438 | 0.427 | 0.031 | 0.432 | 83 | 15 | 0 | ✔ | HPKOT segments and coordinates match |
| POSCAR_NaCl | seekpath | 0.416 **←fastest** | 0.396 | 0.040 | 0.407 | 81 | 15 | 0 | ✔ | HPKOT segments and coordinates match |
| POSCAR_NaCl | ase | 0.386 | 0.376 | 0.030 | 0.384 | 82 | 15 | 0 | other convention | different convention; not compared with HPKOT |
| POSCAR_NaCl | pymatgen | 0.934 | 0.913 | 0.191 | 0.932 | 131 | 15 | 0 | other convention | different convention; not compared with HPKOT |

## Birch–Murnaghan fit of an E(V) table (9 points, Si)

*Olla-DFT is called through the fit function behind `olla-dft eos --collect`, because the command reads pw.x outputs, not a bare table. EOS.dat is the table exported by `olla-dft eos Si.cif --run` in examples/demo_calculo of the Olla-DFT repository (QE 6.6, 9 volumes, ±10 %). The reference is an analytic linear fit, deliberately a different algorithm from every contestant's curve_fit.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | n | failures | correct | detail |
|---|---|---|---|---|---|---|---|---|---|---|
| EOS.dat | olla-dft | 0.335 **←fastest** | 0.295 | 0.040 | 0.326 | 75 | 15 | 0 | ✔ | ΔV0=+6.07e-08 Å³, ΔB0=-1.25e-06 GPa |
| EOS.dat | ase | 0.376 | 0.355 | 0.041 | 0.375 | 79 | 15 | 0 | ✔ | ΔV0=-1.52e-08 Å³, ΔB0=+4.24e-07 GPa; B' not reported |
| EOS.dat | pymatgen | 0.690 | 0.660 | 0.110 | 0.689 | 112 | 15 | 0 | ✔ | ΔV0=+6.07e-08 Å³, ΔB0=-4.69e-07 GPa |

## Band gap from pw.x output (XML and text)

*The XML and the text output of the same scf run, generated with the shipped inputs/Si_scf.in (QE 7.4), so that each format counts once and no tool is judged only on the format it prefers. Olla-DFT and qeschema read the XML; ASE reads the text output; pymatgen reads neither for eigenvalues.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | n | failures | correct | detail |
|---|---|---|---|---|---|---|---|---|---|---|
| Si_scf.xml | olla-dft | 0.152 **←fastest** | 0.132 | 0.020 | 0.146 | 35 | 15 | 0 | ✔ | gap 0.6155 eV vs ref 0.6155 eV; VBM/CBM checked |
| Si_scf.xml | qeschema | 0.467 | 0.437 | 0.030 | 0.460 | 48 | 15 | 0 | ✔ | gap 0.6155421137080532 eV vs ref 0.6155 eV; VBM/CBM checked |
| Si_scf.xml | ase | — | — | — | — | — | 15 | 0 | n/a | not supported: ASE reads pw.x text output (espresso-out), not the data-file-schema XML |
| Si_scf.xml | pymatgen | — | — | — | — | — | 15 | 0 | n/a | not supported: pymatgen.io.pwscf.PWOutput parses energies only (no eigenvalues) and there is no XML parser |
| Si_scf.out | olla-dft | — | — | — | — | — | 15 | 0 | n/a | not supported: `olla-dft gap` reads the data-file-schema XML, not the pw.x text output |
| Si_scf.out | qeschema | — | — | — | — | — | 15 | 0 | n/a | not supported: qeschema reads the data-file-schema XML, not the text output |
| Si_scf.out | ase | 0.396 **←fastest** | 0.385 | 0.031 | 0.395 | 78 | 15 | 0 | ✔ | gap 0.6154999999999999 eV vs ref 0.6155 eV; VBM/CBM checked |
| Si_scf.out | pymatgen | — | — | — | — | — | 15 | 0 | n/a | not supported: pymatgen.io.pwscf.PWOutput parses energies only (no eigenvalues) and there is no XML parser |

## pw.x scf input from a structure (Si 4×4×4, ZnO 6×6×4, fixed cutoffs)

*Each generated file is parsed back by ASE to check species, positions, cell metric, pseudopotentials, grid/shift, occupations and both cutoffs. Cutoffs and grid are forced equal so the comparison is about correctness and cost, not defaults; other defaults (mixing, smearing) remain each tool's own and show up in the end-to-end stage.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | n | failures | correct | detail |
|---|---|---|---|---|---|---|---|---|---|---|
| Si_relajado.cif | olla-dft | 0.467 | 0.446 | 0.041 | 0.461 | 85 | 15 | 0 | ✔ | geometry, species, pseudos, grid/shift, occupations and cutoffs match |
| Si_relajado.cif | ase | 0.416 | 0.386 | 0.049 | 0.410 | 80 | 15 | 0 | ✔ | geometry, species, pseudos, grid/shift, occupations and cutoffs match |
| Si_relajado.cif | pymatgen | 0.386 **←fastest** | 0.355 | 0.020 | 0.380 | 77 | 15 | 0 | ✔ | geometry, species, pseudos, grid/shift, occupations and cutoffs match |
| ZnO.cif | olla-dft | 0.506 | 0.457 | 0.089 | 0.501 | 84 | 15 | 0 | ✔ | geometry, species, pseudos, grid/shift, occupations and cutoffs match |
| ZnO.cif | ase | 0.467 | 0.416 | 0.070 | 0.459 | 80 | 15 | 0 | ✔ | geometry, species, pseudos, grid/shift, occupations and cutoffs match |
| ZnO.cif | pymatgen | 0.447 **←fastest** | 0.375 | 0.059 | 0.443 | 77 | 15 | 0 | ✔ | geometry, species, pseudos, grid/shift, occupations and cutoffs match |

## Olla-DFT relative to the best supported competitor, every contested cell

Ratios > 1 mean Olla-DFT is slower or heavier. `min` ratio uses the fastest sample of each (robust to background noise); the CI is a 95 % bootstrap of the ratio of medians, conditional on the chosen competitor; descriptive, not a multiple-comparison significance test.

| task | input | vs | wall ratio (median) | 95 % CI | wall ratio (min) | RSS ratio |
|---|---|---|---|---|---|---|
| symmetry | Si_relajado.cif | pymatgen | 1.16 | 1.13–1.26 | 1.16 | 1.07 |
| symmetry | ZnO.cif | pymatgen | 1.23 | 1.11–1.35 | 1.20 | 1.07 |
| symmetry | grafito.cif | pymatgen | 1.22 | 1.13–1.33 | 1.17 | 1.07 |
| symmetry | hbn.cif | pymatgen | 1.22 | 1.08–1.44 | 1.20 | 1.07 |
| symmetry | POSCAR_NaCl | ase | 0.94 | 0.64–1.20 | 1.05 | 1.03 |
| kpath | Si_relajado.cif | seekpath | 1.08 | 0.96–1.36 | 1.16 | 1.03 |
| kpath | ZnO.cif | seekpath | 1.09 | 1.02–1.17 | 1.12 | 1.03 |
| kpath | grafito.cif | seekpath | 1.15 | 1.07–1.17 | 1.10 | 1.03 |
| kpath | hbn.cif | seekpath | 1.10 | 1.03–1.17 | 1.10 | 1.03 |
| kpath | POSCAR_NaCl | seekpath | 1.05 | 1.00–1.13 | 1.08 | 1.03 |
| eos | EOS.dat | ase | 0.89 | 0.82–0.94 | 0.83 | 0.96 |
| bandgap | Si_scf.xml | qeschema | 0.33 | 0.29–0.34 | 0.30 | 0.73 |
| inputgen | Si_relajado.cif | pymatgen | 1.21 | 1.15–1.27 | 1.26 | 1.10 |
| inputgen | ZnO.cif | pymatgen | 1.13 | 1.04–1.28 | 1.22 | 1.09 |

**Summary:** Olla-DFT is slower than the best supported competitor in 11 of 14 contested cells (geometric-mean wall ratio 1.02×, min-based 1.02×) and uses more peak memory in 12 of 14 (geometric mean 1.02×).

## Coverage matrix

| task | olla-dft | ase | pymatgen | qeschema | seekpath |
|---|---|---|---|---|---|
| symmetry | ✔ | ✔ | ✔ | — | — |
| kpath | ✔ | ✔ | ✔ | — | ✔ |
| eos | ✔ | ✔ | ✔ | — | — |
| bandgap | ✔ 1/2 inputs | ✔ 1/2 inputs | ✘ n/a | ✔ 1/2 inputs | — |
| inputgen | ✔ | ✔ | ✔ | — | — |

## Areas of opportunity for Olla-DFT (generated automatically; threshold 1.15×, same rule for every tool)

- symmetry/Si_relajado.cif: 1.16× the wall time of pymatgen (95 % CI 1.13–1.26)
- symmetry/ZnO.cif: 1.23× the wall time of pymatgen (95 % CI 1.11–1.35)
- symmetry/grafito.cif: 1.22× the wall time of pymatgen (95 % CI 1.13–1.33)
- symmetry/hbn.cif: 1.22× the wall time of pymatgen (95 % CI 1.08–1.44)
- inputgen/Si_relajado.cif: 1.21× the wall time of pymatgen (95 % CI 1.15–1.27)

## Known limitations of this benchmark

- One consumer laptop, hybrid CPU: absolute times are only comparable within one run; compare ratios across runs.
- Post-processing tasks are small; import time dominates and favours light dependency trees. That is a real cost for a CLI tool, but it is not algorithmic speed.
- Only tasks every tool can express with the same inputs are compared; Olla-DFT features without a counterpart are not benchmarked here, and features of the other tools that Olla-DFT lacks are visible in the coverage matrix.
- symmetry and kpath references share a backend with some contestants (stated in the notes); eos and bandgap references are independent code.
- The end-to-end stage uses one small system (Si, 2 atoms).
