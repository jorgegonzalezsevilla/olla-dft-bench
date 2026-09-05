# Review decisions

Fable 5.1 High reviewed the implementation and measurement summary in `fable-prompt.txt`. Its unedited response is in `fable-review.md`; it did not inspect source code or independently reproduce results.

Accepted: fresh-process help/error coverage; isolated font cache; rendering after deferred imports; checking type annotations, import side effects and existing monkeypatches; CPU and peak-memory measurements; an additional interleaved A/B comparison with identical dependencies. Canonical competitor wrappers, scoring, CPU affinity and seed are retained.

Checked against the actual code: the package namespace is `qekit`; the touched functions have no rendering-object annotations; importing style does not apply rcParams; provenance reads Olla's version without importing Matplotlib; qeout does not require ASE. Matplotlib is a declared dependency, and plotting already selects Agg. Existing tests and consumers in the repository do not patch the removed incidental import attributes. The public plotting functions, constants and options remain available. The project uses Pyflakes, not Ruff.

Not adopted: treating import-time profiling as almost deterministic, changing CPU/core settings midway, or treating all byte differences as scientific regressions. Version and timestamp comments legitimately differ; the supplementary comparison retains originals, requires identical executable input bytes and checks the original numerical grades. Both standard runs retain all cases and contemporaneous competitors; the A/B subset checks one existing input from each task. Warmups are excluded; this iteration does not claim a repeated cold-font-cache speedup or faster pw.x calculations.

The timing intervals are descriptive for this laptop. They do not measure variation across hardware, thermal autocorrelation or the uncertainty from selecting the fastest competitor.
