# Responses to independent verdicts

Each verdict is committed unedited in `verdicts/`. This file records what changed in the
benchmark because of it, so that the loop verdict → fix → rerun is visible.

## Verdict `claude-opus-5_20260903-125851`

| finding | response |
|---|---|
| Two "areas of opportunity" were spurious: unsupported cells leaked into the "best competitor" set | Fixed in `report.py`: unsupported cells are excluded from every speed/memory comparison |
| Opportunity threshold (1.5×) undisclosed; uniform ~1.3× slowdown and ~1.25× memory penalty unreported | Threshold lowered to 1.15×, printed in the report, parameterisable (`--opp-threshold`); new per-cell ratio table with 95 % bootstrap CI and a summary line ("slower in N of M cells, geometric mean …"); rule added that fires when Olla-DFT is slower/heavier in *every* contested cell |
| eos reference reimplemented Olla-DFT's own fit (same seed, same optimiser) | Replaced by an analytic linear least-squares fit of E as a cubic in V^(-2/3), no optimiser, no shared code |
| kpath and symmetry references share a backend with contestants | Kept (there is no other ground truth for a convention), but now disclosed in each task note and in the report's reading guide; the grade is described as a pass-through check |
| bandgap defined only on the XML that only Olla-DFT reads | Two more inputs: the XML and the text output of the same scf run, generated with the shipped `inputs/Si_scf.in` (QE 7.4). ASE competes on the text output; qeschema (QE's own package) competes on the XML; Olla-DFT is marked *not supported* on the text output |
| Olla-DFT installed from a local path; commit not recorded | Installed from the public repository at a pinned commit; `env.json` records the source URL and commit (`olla_dft_source`) |
| 5 repetitions too few; fixed tool order | Default 15 repetitions; tool order shuffled per repetition with a recorded seed |
| End-to-end n = 1; irreducible k-points hidden; "identical physics" overstated | End-to-end repeated 5× (median reported), irreducible k-points shown, wording corrected |
| inputgen graded only on atoms and volume | Also graded on k-grid and ecutwfc matching the request |
| Missing competitors `qeschema`/`postqe`/`aiida-quantumespresso` | `qeschema` added. `postqe` and `aiida-quantumespresso` listed under *Not yet compared* in PROTOCOL.md with the reason (the first version of this row claimed that before the file said it; the second verdict caught it) |
| No provenance for `Si.xml.gz` and `EOS.dat` | *Input provenance* table added to PROTOCOL.md and to the eos task note. `Si.xml.gz` (no input available) is no longer graded; the Si inputs used ship their pw.x input |

## Verdict `claude-opus-5_20260903-142901`

| finding | response |
|---|---|
| Olla-DFT's inputgen wrapper ran a 40-step k-spacing bisection inside the timed region (~7 % against Olla-DFT) | The spacing is now computed once, untimed, by the harness and passed to the wrapper |
| bandgap counted the XML twice, flattering Olla-DFT's coverage and diluting the geometric mean | `Si.xml.gz` dropped from grading; one XML input and one text input |
| One opportunity bullet had a CI that includes 1 | Bullets whose 95 % CI includes 1 are tagged "not significant" |
| Two RESPONSES.md claims were not backed by any file | PROTOCOL.md now has *Not yet compared* and *Input provenance* sections; the rows above were corrected to say so |
| Dispersion did not improve with more repetitions; environment warnings still fire | True and unchanged: the machine's governor and turbo need root; the warnings stay in every report |
