# Changelog

## 0.3.1 — 2026-09-04

- Retain complete performance runs for Olla-DFT 1.3.0 and 1.3.1 with fixed competitor versions.
- Add an interleaved same-interpreter A/B check, raw samples, package hashes and review decisions.
- Pin the measured Olla wheel by SHA-256 for reproduction.
- Keep measurement engine 0.3.0, original wrappers, numerical grading and historical records unchanged; this is a results release, without new QE solver timings.

## 0.3.0 — 2026-09-04

- Publish matched continuous/recovered QE figures, raw observables and recomputation checks.
- Add an offline interactive result explorer demonstration and bilingual publication pages.
- Preserve the existing benchmark protocol/results; no new QE measurements.

## 0.2.0 — 2026-09-04

- Enforce measurement timeouts and terminate descendant processes; preserve incremental samples.
- Validate expected cells/repetitions, sample journals, input and generated-artifact hashes.
- Expose process failures and reject failed/unconverged QE runs, checking every energy sample.
- Check species, periodic positions, cell metric, pseudopotentials, k-grid shifts, both cutoffs and VBM/CBM.
- Validate HPKOT coordinates and display other path conventions separately from incorrect results.
- Use Olla-DFT's explicit --kgrid, isolate configuration and fingerprint all installed packages and source files.
- Handle failed cells and escaped text safely in the dashboard; retain historical evidence without upgrading its guarantees.
- Add adversarial regression tests and a new benchmark against Olla-DFT 1.1.1.

## 0.1.0 — 2026-09-03

First tagged version. Five tasks (symmetry, k-path, EOS fit, band gap from XML and text output,
pw.x input generation) plus an end-to-end stage with pw.x; contestants Olla-DFT, ASE, pymatgen,
seekpath, qeschema; independent references; `verify` recomputes everything from raw samples;
per-cell ratio table with bootstrap CI; isolation via taskset and systemd scopes; dashboard;
judge packets and two independent verdicts with responses; three published runs.
