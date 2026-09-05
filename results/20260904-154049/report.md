# Olla-DFT benchmark — run 20260904-154049

*Generated from `results.json`; every number is recomputable with `python bench.py verify`.*

## Environment

- CPU: 12th Gen Intel(R) Core(TM) i5-12450H (12 logical CPUs), pinned to CPU 0
- RAM: 7.4 GiB; governor `powersave`; turbo disabled: `False`
- OS: Linux-7.1.5-76070105-generic-x86_64-with-glibc2.39; Python 3.12.3; pw.x: /home/jorge/GITHUB/olla-dft-bench/.qe/bin/pw.x
- Packages: Pygments 2.21.0, ase 3.29.0, bibtexparser 1.4.4, certifi 2026.7.22, charset-normalizer 3.5.1, cloudpickle 3.1.2, contourpy 1.3.3, cycler 0.12.1, elementpath 4.8.0, fonttools 4.64.0, idna 3.19, iniconfig 2.3.0, joblib 1.6.0, kiwisolver 1.5.1, lxml 6.1.3, matplotlib 3.11.1, monty 2026.7.16, mpmath 1.3.0, narwhals 2.25.0, networkx 3.6.1, numpy 2.2.6, olla-dft 1.1.0, orjson 3.12.0, packaging 26.3, palettable 3.3.3, pandas 3.0.5, pillow 12.3.0, pip 26.2.1, plotly 7.0.0, pluggy 1.6.0, pyflakes 3.4.0, pymatgen 2026.5.4, pymatgen-core 2026.8.30, pyparsing 3.3.2, pytest 9.1.1, python-dateutil 2.9.0.post0, qeschema 1.5.1, requests 2.34.2, ruamel.yaml 0.19.1, scipy 1.18.1, seekpath 2.2.1, six 1.17.0, spglib 2.7.0, sympy 1.14.0, tabulate 0.10.0, tqdm 4.70.0, typing_extensions 4.16.0, uncertainties 3.2.3, urllib3 2.7.0, xmlschema 2.3.1
- Olla-DFT source: `https://github.com/jorgegonzalezsevilla/olla-dft` @ `caf08257293e1fe1ef2ebf9db051b3ec827a7f45`
- Repetitions per cell: 1 (+1 warm-up, discarded); threads per process: 1; tool order shuffled per repetition (seed 20260904)
- End-to-end repetitions: 5; opportunity threshold: 1.15× (stated here, applied identically to time and memory)
- Load average at start / end: [2.46923828125, 2.01904296875, 1.6416015625] / [3.13818359375, 2.255859375, 1.7470703125]

**Run status: complete**

> **Environment warnings**

> - CPU governor is 'powersave', not 'performance': timings are noisier. Fix: sudo cpupower frequency-set -g performance
> - Turbo boost enabled: single-thread timings drift with temperature. Fix: echo 1 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo
> - 1-min load average 2.47 > 1.0: other processes were competing for CPU.

## How to read the tables

Wall time is the median of a fresh process per repetition (imports included, because that is what the
command line costs). CPU is user+system time; RSS is peak resident memory. `correct` is the deterministic
grade against the reference described in each task's note; where the reference shares a backend with a
contestant, the note says so and the grade only shows the wrapper passes the result through. `—` means
the tool does not cover the task; that is a coverage fact, not a failure, and such cells are excluded from
every speed or memory comparison.

## pw.x scf input from a structure (Si 4×4×4, ZnO 6×6×4, fixed cutoffs)

*Each generated file is parsed back by ASE to check species, positions, cell metric, pseudopotentials, grid/shift, occupations and both cutoffs. Cutoffs and grid are forced equal so the comparison is about correctness and cost, not defaults; other defaults (mixing, smearing) remain each tool's own and show up in the end-to-end stage.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | n | failures | correct | detail |
|---|---|---|---|---|---|---|---|---|---|---|
| Si_relajado.cif | olla-dft | 1.223 | 1.223 | 0.000 | 1.217 | 98 | 1 | 0 | ✔ | geometry, species, pseudos, grid/shift, occupations and cutoffs match |
| Si_relajado.cif | ase | 0.528 **←fastest** | 0.528 | 0.000 | 0.527 | 79 | 1 | 0 | ✔ | geometry, species, pseudos, grid/shift, occupations and cutoffs match |
| Si_relajado.cif | pymatgen | 0.538 | 0.538 | 0.000 | 0.530 | 77 | 1 | 0 | ✔ | geometry, species, pseudos, grid/shift, occupations and cutoffs match |
| ZnO.cif | olla-dft | 1.169 | 1.169 | 0.000 | 1.160 | 98 | 1 | 0 | ✔ | geometry, species, pseudos, grid/shift, occupations and cutoffs match |
| ZnO.cif | ase | 0.668 | 0.668 | 0.000 | 0.665 | 79 | 1 | 0 | ✔ | geometry, species, pseudos, grid/shift, occupations and cutoffs match |
| ZnO.cif | pymatgen | 0.497 **←fastest** | 0.497 | 0.000 | 0.497 | 77 | 1 | 0 | ✔ | geometry, species, pseudos, grid/shift, occupations and cutoffs match |

## High-symmetry k-path from a structure

*Reference is the HPKOT convention (seekpath). Olla-DFT and the seekpath contestant call the same library, so their agreement is expected and only shows the path is passed through intact. ASE and pymatgen implement Setyawan–Curtarolo; a mismatch there is a convention difference, not an error.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | n | failures | correct | detail |
|---|---|---|---|---|---|---|---|---|---|---|
| Si_relajado.cif | olla-dft | 0.660 | 0.660 | 0.000 | 0.652 | 97 | 1 | 0 | ✔ | HPKOT segments and coordinates match |
| Si_relajado.cif | seekpath | 0.499 **←fastest** | 0.499 | 0.000 | 0.496 | 81 | 1 | 0 | ✔ | HPKOT segments and coordinates match |
| Si_relajado.cif | ase | 0.559 | 0.559 | 0.000 | 0.556 | 82 | 1 | 0 | other convention | different convention; not compared with HPKOT |
| Si_relajado.cif | pymatgen | 0.600 | 0.600 | 0.000 | 0.590 | 88 | 1 | 0 | other convention | different convention; not compared with HPKOT |
| ZnO.cif | olla-dft | 1.046 | 1.046 | 0.000 | 1.043 | 97 | 1 | 0 | ✔ | HPKOT segments and coordinates match |
| ZnO.cif | seekpath | 0.832 **←fastest** | 0.832 | 0.000 | 0.831 | 81 | 1 | 0 | ✔ | HPKOT segments and coordinates match |
| ZnO.cif | ase | 0.537 | 0.537 | 0.000 | 0.527 | 82 | 1 | 0 | other convention | different convention; not compared with HPKOT |
| ZnO.cif | pymatgen | 0.669 | 0.669 | 0.000 | 0.666 | 88 | 1 | 0 | other convention | different convention; not compared with HPKOT |
| grafito.cif | olla-dft | 1.097 | 1.097 | 0.000 | 1.091 | 97 | 1 | 0 | ✔ | HPKOT segments and coordinates match |
| grafito.cif | seekpath | 0.812 **←fastest** | 0.812 | 0.000 | 0.806 | 81 | 1 | 0 | ✔ | HPKOT segments and coordinates match |
| grafito.cif | ase | 0.771 | 0.771 | 0.000 | 0.764 | 82 | 1 | 0 | other convention | different convention; not compared with HPKOT |
| grafito.cif | pymatgen | 0.823 | 0.823 | 0.000 | 0.818 | 88 | 1 | 0 | other convention | different convention; not compared with HPKOT |
| hbn.cif | olla-dft | 1.267 **←fastest** | 1.267 | 0.000 | 1.257 | 97 | 1 | 0 | ✔ | HPKOT segments and coordinates match |
| hbn.cif | seekpath | 1.317 | 1.317 | 0.000 | 1.309 | 81 | 1 | 0 | ✔ | HPKOT segments and coordinates match |
| hbn.cif | ase | 1.002 | 1.002 | 0.000 | 0.999 | 82 | 1 | 0 | other convention | different convention; not compared with HPKOT |
| hbn.cif | pymatgen | 1.243 | 1.243 | 0.000 | 1.238 | 88 | 1 | 0 | other convention | different convention; not compared with HPKOT |
| POSCAR_NaCl | olla-dft | 1.179 | 1.179 | 0.000 | 1.171 | 97 | 1 | 0 | ✔ | HPKOT segments and coordinates match |
| POSCAR_NaCl | seekpath | 1.113 **←fastest** | 1.113 | 0.000 | 1.107 | 80 | 1 | 0 | ✔ | HPKOT segments and coordinates match |
| POSCAR_NaCl | ase | 1.036 | 1.036 | 0.000 | 1.026 | 81 | 1 | 0 | other convention | different convention; not compared with HPKOT |
| POSCAR_NaCl | pymatgen | 2.053 | 2.053 | 0.000 | 2.048 | 131 | 1 | 0 | other convention | different convention; not compared with HPKOT |

## Band gap from pw.x output (XML and text)

*The XML and the text output of the same scf run, generated with the shipped inputs/Si_scf.in (QE 7.4), so that each format counts once and no tool is judged only on the format it prefers. Olla-DFT and qeschema read the XML; ASE reads the text output; pymatgen reads neither for eigenvalues.*

| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | n | failures | correct | detail |
|---|---|---|---|---|---|---|---|---|---|---|
| Si_scf.xml | olla-dft | 0.468 **←fastest** | 0.468 | 0.000 | 0.465 | 52 | 1 | 0 | ✔ | gap 0.6155 eV vs ref 0.6155 eV; VBM/CBM checked |
| Si_scf.xml | qeschema | 0.974 | 0.974 | 0.000 | 0.964 | 48 | 1 | 0 | ✔ | gap 0.6155421137080532 eV vs ref 0.6155 eV; VBM/CBM checked |
| Si_scf.xml | ase | — | — | — | — | — | 1 | 0 | n/a | not supported: ASE reads pw.x text output (espresso-out), not the data-file-schema XML |
| Si_scf.xml | pymatgen | — | — | — | — | — | 1 | 0 | n/a | not supported: pymatgen.io.pwscf.PWOutput parses energies only (no eigenvalues) and there is no XML parser |
| Si_scf.out | olla-dft | — | — | — | — | — | 1 | 0 | n/a | not supported: `olla-dft gap` reads the data-file-schema XML, not the pw.x text output |
| Si_scf.out | qeschema | — | — | — | — | — | 1 | 0 | n/a | not supported: qeschema reads the data-file-schema XML, not the text output |
| Si_scf.out | ase | 0.791 **←fastest** | 0.791 | 0.000 | 0.790 | 78 | 1 | 0 | ✔ | gap 0.6154999999999999 eV vs ref 0.6155 eV; VBM/CBM checked |
| Si_scf.out | pymatgen | — | — | — | — | — | 1 | 0 | n/a | not supported: pymatgen.io.pwscf.PWOutput parses energies only (no eigenvalues) and there is no XML parser |

## Olla-DFT relative to the best supported competitor, every contested cell

Ratios > 1 mean Olla-DFT is slower or heavier. `min` ratio uses the fastest sample of each (robust to background noise); the CI is a 95 % bootstrap of the ratio of medians, conditional on the chosen competitor; descriptive, not a multiple-comparison significance test.

| task | input | vs | wall ratio (median) | 95 % CI | wall ratio (min) | RSS ratio |
|---|---|---|---|---|---|---|
| inputgen | Si_relajado.cif | ase | 2.32 | 2.32–2.32 | 2.32 | 1.28 |
| inputgen | ZnO.cif | pymatgen | 2.35 | 2.35–2.35 | 2.35 | 1.27 |
| kpath | Si_relajado.cif | seekpath | 1.32 | 1.32–1.32 | 1.32 | 1.21 |
| kpath | ZnO.cif | seekpath | 1.26 | 1.26–1.26 | 1.26 | 1.21 |
| kpath | grafito.cif | seekpath | 1.35 | 1.35–1.35 | 1.35 | 1.20 |
| kpath | hbn.cif | seekpath | 0.96 | 0.96–0.96 | 0.96 | 1.20 |
| kpath | POSCAR_NaCl | seekpath | 1.06 | 1.06–1.06 | 1.06 | 1.21 |
| bandgap | Si_scf.xml | qeschema | 0.48 | 0.48–0.48 | 0.48 | 1.08 |

**Summary:** Olla-DFT is slower than the best supported competitor in 6 of 8 contested cells (geometric-mean wall ratio 1.25×, min-based 1.25×) and uses more peak memory in 8 of 8 (geometric mean 1.21×).

## Coverage matrix

| task | olla-dft | ase | pymatgen | qeschema | seekpath |
|---|---|---|---|---|---|
| inputgen | ✔ | ✔ | ✔ | — | — |
| kpath | ✔ | ✔ | ✔ | — | ✔ |
| bandgap | ✔ 1/2 inputs | ✔ 1/2 inputs | ✘ n/a | ✔ 1/2 inputs | — |

## Areas of opportunity for Olla-DFT (generated automatically; threshold 1.15×, same rule for every tool)

- inputgen/Si_relajado.cif: 2.32× the wall time of ase (95 % CI 2.32–2.32)
- inputgen/Si_relajado.cif: 1.28× the peak memory of the lightest competitor
- inputgen/ZnO.cif: 2.35× the wall time of pymatgen (95 % CI 2.35–2.35)
- inputgen/ZnO.cif: 1.27× the peak memory of the lightest competitor
- kpath/Si_relajado.cif: 1.32× the wall time of seekpath (95 % CI 1.32–1.32)
- kpath/Si_relajado.cif: 1.21× the peak memory of the lightest competitor
- kpath/ZnO.cif: 1.26× the wall time of seekpath (95 % CI 1.26–1.26)
- kpath/ZnO.cif: 1.21× the peak memory of the lightest competitor
- kpath/grafito.cif: 1.35× the wall time of seekpath (95 % CI 1.35–1.35)
- kpath/grafito.cif: 1.20× the peak memory of the lightest competitor
- kpath/hbn.cif: 1.20× the peak memory of the lightest competitor
- kpath/POSCAR_NaCl: 1.21× the peak memory of the lightest competitor
- Olla-DFT uses more peak memory in every contested cell (geometric mean 1.21×)

## Known limitations of this benchmark

- One consumer laptop, hybrid CPU: absolute times are only comparable within one run; compare ratios across runs.
- Post-processing tasks are small; import time dominates and favours light dependency trees. That is a real cost for a CLI tool, but it is not algorithmic speed.
- Only tasks every tool can express with the same inputs are compared; Olla-DFT features without a counterpart are not benchmarked here, and features of the other tools that Olla-DFT lacks are visible in the coverage matrix.
- symmetry and kpath references share a backend with some contestants (stated in the notes); eos and bandgap references are independent code.
- The end-to-end stage uses one small system (Si, 2 atoms).
