# Olla-DFT benchmark — run 20260903-153320

*Generated from `results.json`; every number is recomputable with `python bench.py verify`.*

## Environment

- CPU: 12th Gen Intel(R) Core(TM) i5-12450H (12 logical CPUs), pinned to CPU 0
- RAM: 7.4 GiB; governor `powersave`; turbo disabled: `False`
- OS: Linux-7.1.5-76070105-generic-x86_64-with-glibc2.39; Python 3.12.3; pw.x: Program PWSCF v.7.4 starts on  3Sep2026 at 15:33:21
- Packages: ase 3.29.0, matplotlib 3.11.1, numpy 2.2.6, olla-dft 1.1.0, pymatgen 2026.5.4, scipy 1.18.1, seekpath 2.2.1, spglib 2.7.0
- Olla-DFT source: `https://github.com/jorgegonzalezsevilla/olla-dft` @ `caf08257293e1fe1ef2ebf9db051b3ec827a7f45`
- Repetitions per cell: 15 (+1 warm-up, discarded); threads per process: 1; tool order shuffled per repetition (seed 20260903)
- End-to-end repetitions: 5; opportunity threshold: 1.15× (stated here, applied identically to time and memory)
- Load average at start / end: [2.037109375, 2.3330078125, 2.96240234375] / [2.3310546875, 3.10888671875, 3.072265625]

> **Environment warnings**

> - CPU governor is 'powersave', not 'performance': timings are noisier. Fix: sudo cpupower frequency-set -g performance
> - Turbo boost enabled: single-thread timings drift with temperature. Fix: echo 1 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo
> - 1-min load average 2.04 > 1.0: other processes were competing for CPU.

## How to read the tables

Wall time is the median of a fresh process per repetition (imports included, because that is what the
command line costs). CPU is user+system time; RSS is peak resident memory. `correct` is the deterministic
grade against the reference described in each task's note; where the reference shares a backend with a
contestant, the note says so and the grade only shows the wrapper passes the result through. `—` means
the tool does not cover the task; that is a coverage fact, not a failure, and such cells are excluded from
every speed or memory comparison.

## Olla-DFT relative to the best supported competitor, every contested cell

Ratios > 1 mean Olla-DFT is slower or heavier. `min` ratio uses the fastest sample of each (robust to background noise); the CI is a 95 % bootstrap of the ratio of medians.

| task | input | vs | wall ratio (median) | 95 % CI | wall ratio (min) | RSS ratio |
|---|---|---|---|---|---|---|
## Coverage matrix

| task | olla-dft | ase | pymatgen | qeschema | seekpath |
|---|---|---|---|---|---|

## Areas of opportunity for Olla-DFT (generated automatically; threshold 1.15×, same rule for every tool)

- none triggered (nothing above 1.15× and no mismatch)

## Known limitations of this benchmark

- One consumer laptop, hybrid CPU: absolute times are only comparable within one run; compare ratios across runs.
- Post-processing tasks are small; import time dominates and favours light dependency trees. That is a real cost for a CLI tool, but it is not algorithmic speed.
- Only tasks every tool can express with the same inputs are compared; Olla-DFT features without a counterpart are not benchmarked here, and features of the other tools that Olla-DFT lacks are visible in the coverage matrix.
- symmetry and kpath references share a backend with some contestants (stated in the notes); eos and bandgap references are independent code.
- The end-to-end stage uses one small system (Si, 2 atoms).
