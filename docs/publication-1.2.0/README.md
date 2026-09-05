# Olla-DFT 1.2.0: recovery validation and interactive result explorer

The scientific figures and the interface demo have different purposes:

- [Recovery figure (English)](recovery-en.png), [figura en español](recovery-es.png):
  compare continuous/recovered jobs **within each matched pair**. Axes use percent of
  a predeclared tolerance, with absolute component differences labelled and units retained.
- [Interactive explorer](explorer.html): eight existing records illustrate UI filters and
  exports. Their energy values must not be read as a single physical convergence series.
- [JSON with observables/provenance](validation.json), [CSV differences](validation.csv)
  and public XML/input copies under `evidence/` allow independent recomputation.

## Protocol and scope

Three small serial Quantum ESPRESSO 7.4 cases: displaced Si SCF, relax and vc-relax.
One continuous/recovered pair per case; no repeatability estimate or uncertainty bars.
The recovery exercises included clean checkpoints, SIGKILL of supervisor/QE, simulated
incomplete scratch writes and restoration from an earlier verified checkpoint. The host
remained running. Physical power loss, disk loss, VM replacement and cloud savings were
not measured. These are software recovery checks, not convergence studies of the material.

Input/UPF hashes, executable/library records, architecture, threads, environment and
runtime identifier matched within each pair. The original `si-scf` pair is excluded
from this figure because its old job record lacks the full runtime metadata.

The figure shows max absolute component differences. XML energy/force/stress values
are in Hartree atomic units and multiplied by 2 to express Ry-based units; positions
and cell remain in bohr. 0 means equality at the stored XML precision, not a physical
certainty or zero uncertainty. The acceptance tolerances are 1e-7 Ry, 1e-6 Ry/bohr,
1e-8 Ry/bohr³, 1e-6 bohr (positions) and 1e-6 bohr (cell), unchanged from the recovery gate.
All 15 checks pass. The largest relative difference is 27.8834% of the cell tolerance.

The public XML/input copies replace only local `pseudo_dir` infrastructure paths with
`./pp`. Original and public SHA-256 values are recorded separately. Numerical values
are verified against the XML before drawing. UPFs are identified by their original
content hashes; their binaries and scratch are not bundled here. This is evidence,
not a runnable checkpoint or a hardware-independent reproduction of the original runtime.

## Recompute without running a simulation

From the benchmark checkout with its normal plotting dependencies:

```sh
.venv/bin/python tools/plot_recovery_validation.py
```

This verifies six public XML hashes, checks all stored observables and 15 differences,
and rebuilds PNG/SVG/PDF in Spanish and English. It never launches QE or accesses a
cloud provider. The preceding benchmark 0.2.0 measurements remain unchanged.

## Public introduction

The ES/EN landing pages introduce the examples and recovery checks in plain language. Technical figures, conditions and numerical tables remain available in expandable sections. Regenerate the pages with `python tools/build_public_page.py`; this reads the existing manifests and evidence without changing figures, PDFs or numerical results. Styling is in `public-page.css`. The showcase packager also calls this page builder.
