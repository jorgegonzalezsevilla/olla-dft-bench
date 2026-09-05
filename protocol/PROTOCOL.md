# Benchmark protocol

## Version 0.2.0 integrity requirements

All expected (task, input, tool, repetition) entries, including warmups, must be present exactly once. Failed processes, missing payloads, failed grades and timeouts fail the run. Unsupported uses the explicit wrapper exit code 3; alternate k-path conventions are supported but not comparable to HPKOT. Errors remain visible and cannot win a performance ranking.

Every new result retains a sample journal and hashes of generated inputs and per-repetition QE output/error logs. Input generation checks species and periodic sites, cell metric, both cutoffs, pseudopotentials, occupations, grid and shifts. Band-gap grading checks all three energies. HPKOT coordinates are checked. Every QE sample needs exit code 0, convergence, JOB DONE and finite energy; the full energy spread must stay within 1e-6 Ry.

Historical runs are not rewritten or scientifically recertified: verification reports legacy consistency and any newly identified execution warnings. Bootstrap intervals are descriptive and conditional on the chosen comparator; they do not include competitor-selection uncertainty or thermal autocorrelation. Reported comparisons include wrapper/import costs.

## Purpose
Measure, honestly and reproducibly, how Olla-DFT compares with other open-source tools on tasks
that all of them can perform from the same inputs. The goal is to find where Olla-DFT is weak as
much as where it is strong; the report generator applies the same rules to every tool.

## Contestants and versions
Pinned in `requirements.lock`. Olla-DFT is installed from its public repository at a pinned commit;
`results/<run>/env.json` records URL and commit under `olla_dft_source`. Competitors: ASE, pymatgen,
seekpath/spglib, qeschema. Where a reference shares a backend with a contestant (spglib, seekpath)
the task note says so; independent verdicts and the responses to them are in `judge/`.

## Tasks (see `benchlib/tasks.py`)
| task | input | what is compared | reference |
|---|---|---|---|
| symmetry | 5 structure files | space group number, atoms in primitive cell | spglib called directly |
| kpath | 5 structure files | segments and coordinates within HPKOT | seekpath called directly (HPKOT) |
| eos | 9-point E(V) table | V0, B0 | analytic linear fit of E as cubic in V^(-2/3) |
| bandgap | XML + text output of the shipped scf input | gap, VBM, CBM | independent XML parse; pw.x's own HOMO/LUMO line for text |
| inputgen | 2 structures | species, periodic sites, cell metric, grid and shifts, both cutoffs, occupations and pseudopotentials | ASE parse of the source structure + requested grid/cutoff |
| end-to-end (optional) | Si input from each tool | pw.x total energy, SCF iterations, pw.x time | agreement between tools |

Reference implementations live in `tools/reference.py` and are not timed. Structure and generated-input parsing use ASE; symmetry and HPKOT references use spglib and seekpath. These shared dependencies limit independence. A task a tool cannot perform is recorded as *not supported* with the reason; it is not
counted as a failure and not silently dropped.

## Measurement
- Each repetition is a fresh process (`python wrapper.py task args`), so import time is included:
  it is what a user pays at the command line. One warm-up per cell is recorded and checked, but excluded from timing statistics.
- Wall time with `time.perf_counter()`; CPU user/system time and peak RSS from `os.wait4` rusage.
- Default 15 repetitions per (task, input, tool); within each repetition the tool order is shuffled
  with a recorded seed, so thermal drift and background noise affect all tools alike.
- Reported: median, min, IQR, mean, standard deviation, and for every contested cell the ratio of
  Olla-DFT to the best correct, comparable, failure-free competitor with a descriptive 95 % bootstrap interval. Raw samples are kept in `results.json`.
- The end-to-end stage runs pw.x 5 times per tool (median reported) and shows irreducible k-points.
- "Areas of opportunity" are listed by a stated threshold (default 1.15×, `--opp-threshold`) applied
  identically to time and memory; a rule also fires when Olla-DFT loses every contested cell.
- Environment: single thread (`OMP_NUM_THREADS=1` etc.), `MPLBACKEND=Agg`, `PYTHONHASHSEED=0`,
  private `XDG_CONFIG_HOME` so no user configuration leaks in, process pinned with `taskset` to the
  fastest core; with `--isolate`, a transient systemd scope adds `MemoryMax` and `CPUQuota=100%`.
- The environment fingerprint (CPU model and topology, governor, turbo state, load average before
  and after, kernel, Python, package versions, git SHAs, SHA-256 of every input) is stored with the
  results. Warnings are emitted when the governor is not `performance`, turbo is on, or load > 1.

## Grading
Deterministic functions in `benchlib/tasks.py`. Numeric tolerances: V0 1e-4 Å³, B0 1e-3 GPa,
gap 1e-3 eV, volume 1e-3 Å³. k-paths are compared as sets of undirected segments after label
normalisation and HPKOT coordinates must agree within 1e-5. Only explicitly different conventions are non-comparable; a wrong HPKOT path fails. Periodic Cartesian sites and cell metrics must agree within 1e-4 Å.

## Reproducing
```bash
git clone https://github.com/jorgegonzalezsevilla/olla-dft-bench && cd olla-dft-bench
python3 -m venv .venv && .venv/bin/pip install -r requirements.lock
python bench.py env                      # check warnings, fix governor/turbo if you can
python bench.py run --reps 15 --isolate --with-qe
python bench.py verify results/<run_id>
```
Without Quantum ESPRESSO drop `--with-qe`. Without systemd drop `--isolate` (taskset still applies).
A Dockerfile pins Python packages, but its base image and operating-system packages are not immutable. A container does not remove CPU
frequency or thermal noise.

## Adding a tool or a task
A tool is one file in `tools/` that prints a single `@@RESULT {json}` line; a task is one entry in
`TASKS` with inputs, tools, argument builder and grading function, plus a reference branch in
`tools/reference.py`. Contributions to the benchmark itself are welcome as issues.

## Quantum ESPRESSO binary
The benchmark does not measure pw.x itself, but the end-to-end stage needs a working one. On the
reference machine the Ubuntu 24.04 package `quantum-espresso 6.7-2build4` aborts with
`*** buffer overflow detected ***` while reading any UPF pseudopotential (glibc fortify check in
the UPF reader; reproduced with v1 and v2 files, with and without MPI). It is therefore not used.
The reference runs use QE pinned from conda-forge:
```bash
curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xj -C .micromamba bin/micromamba
./.micromamba/bin/micromamba create -r .micromamba/root -n .qe -c conda-forge --no-rc qe=7.4 && ln -s .micromamba/root/envs/.qe .qe
python bench.py run --with-qe            # picks ./.qe/bin/pw.x automatically; or --pw-x /path/to/pw.x
```
The exact pw.x version banner is retained in each end-to-end `pw.out` artifact.

## Not yet compared (future work)
- `postqe` (QE's post-processing Python package) reads the XML but needs compiled Fortran extensions; not installed.
- `aiida-quantumespresso` generates pw.x inputs but requires a running AiiDA profile and database; not installed.
- `sumo` / `pyprocar` plot bands and DOS from QE outputs; a plotting task is not defined yet.
Adding any of them is one wrapper in `tools/` plus one line in `benchlib/tasks.py`.

## Input provenance
| input | origin |
|---|---|
| `Si_scf.in`, `Si_scf.out`, `Si_scf.xml` | generated here with QE 7.4 (conda-forge); the input is shipped |
| `EOS.dat` | exported by `olla-dft eos Si.cif --run` in `examples/demo_calculo` of Olla-DFT (QE 6.6) |
| `Si.xml.gz` | 122-k bands run from the Olla-DFT test suite (QE 6.6); its input is not available, so it is no longer used for grading and is kept only for reference |
| structure files | Olla-DFT `examples/` and `tests/datos/` |
