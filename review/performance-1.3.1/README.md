# Olla-DFT 1.3.1: less waiting, less memory

Olla now loads plotting and font discovery when drawing a figure, and keeps equation-of-state fitting separate from structure preparation. The formulas, tolerances and generated calculation inputs are unchanged.

**Español:** se redujo el tiempo de espera entre 17 % y 39 % y la memoria entre 14 % y 32 % en la comparación alternada de cinco operaciones. Esto mejora la respuesta de los comandos; no demuestra acelerar el cálculo físico de Quantum ESPRESSO.

## Interleaved Olla 1.3.0 → 1.3.1

One existing input per task; 15 randomized A/B pairs, same interpreter/dependencies, CPU 0, one thread and a private cache warmed before timing. Each sample is a fresh process using the original wrapper.

| Operation / Operación | Before (ms) | After (ms) | Less time | Descriptive 95% interval | Less peak memory |
|---|---:|---:|---:|---:|---:|
| Structure symmetry / Simetría | 546 | 447 | 18.2% | 14.9–19.8% | 14.2% |
| k-point paths / Rutas k | 629 | 508 | 19.3% | 11.5–22.0% | 14.1% |
| Equation-of-state fit / Ajuste EOS | 477 | 345 | 27.6% | 25.7–30.5% | 17.9% |
| Read electronic gap / Leer brecha electrónica | 265 | 163 | 38.6% | 32.0–44.3% | 31.9% |
| Generate QE input / Preparar entrada QE | 566 | 468 | 17.4% | 12.9–21.0% | 13.8% |

All 160 records (including warmups) passed the original numerical grades. Paired scientific payloads and executable QE input bytes matched exactly; originals retain version/time comments. Full CPU and memory medians are in [comparison.json](comparison.json).

## Against other libraries

The two full runs each contain 832 records: 15 repetitions plus warmup per cell, all original inputs and fixed versions of ASE, pymatgen, seekpath and qeschema. Unsupported formats and different path conventions remain visible and excluded from rankings.

| Metric | Olla 1.3.0 | Olla 1.3.1 |
|---|---:|---:|
| Geometric time ratio to best comparable competitor | 1.30× | 1.02× |
| Geometric peak-memory ratio | 1.22× | 1.02× |
| Cells with higher median time | 13/14 | 11/14 |
| Cells with higher peak memory | 14/14 | 12/14 |

A ratio above one means Olla costs more. A geometric average is not a claim that every operation is equally fast. EOS has the lowest median time in the new run; structure reporting, paths and input generation still need work. Ratios are conditional on the selected best competitor.

[Baseline report](../../results/20260904-223352/report.md) · [Candidate report](../../results/20260904-224340/report.md) · [Recomputed comparison](comparison.json)

## Validation and limits

- Both full runs pass `bench.py verify`: hashes, complete sample journals, grades and report regeneration.
- Both software editions pass 1,041 local tests, one skipped test, Pyflakes and wheel/sdist builds. GitHub also passed Python 3.9–3.13. Six new cases cover non-plotting startup, help/errors, three EOS equations and PNG/SVG rendering.
- [Package hashes](package-hashes.json) identify the exact release wheels; all 124 packaged files match the corresponding committed source. [Provenance](provenance.json) records that only Olla changed between environments.
- [Fable review](fable-review.md) and [review decisions](review-decisions.md) are retained. The model reviewed a summary, not the source or measurements.
- One laptop, turbo enabled and background load. A/B pair bootstrap intervals are descriptive; they do not cover hardware diversity or thermal autocorrelation. The full-run before/after blocks are not interleaved; use their contemporaneous competitor ratios and the supplementary pairs together.
- Timings include imports and wrapper/reporting work. The font cache is persistent after warmup; no repeated cold-cache claim. No new pw.x timings, physical parameters or interruption tests.

## Reproduce

Install the locked dependencies, then select the exact release wheel. The baseline SHA-256 is recorded in provenance.json; the candidate hash is pinned in requirements.lock.

```bash
python bench.py run --reps 15 --seed 20260905 --cpu 0 --label reproduction
python bench.py verify results/<new-run>
python review/performance-1.3.1/summarize.py
```

For a new interleaved run, install each wheel with `pip install --no-deps --target` into separate fresh directories while keeping the same interpreter and dependencies, then run:

```bash
python review/performance-1.3.1/paired.py /tmp/olla-base /tmp/olla-candidate /tmp/new-paired-run
```

The supplementary script asserts version and import location before timing. Raw pairs and original generated inputs are retained in [paired-run](paired-run/). The results release is 0.3.1; the unchanged measurement engine remains 0.3.0 so existing runs retain their original verification rules.
