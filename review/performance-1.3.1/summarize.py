"""Recompute the version comparison from retained canonical and paired data."""
import hashlib
import json
import math
from pathlib import Path
import random
import statistics as st
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from benchlib.report import ratios
from benchlib.validation import check_run


def main():
    runs = {}
    for version, rid in [("1.3.0", "20260904-223352"), ("1.3.1", "20260904-224340")]:
        run = json.loads((ROOT / "results" / rid / "results.json").read_text())
        assert run["status"] == "complete" and not check_run(run, strict=True)
        assert run["env"]["packages"]["olla-dft"] == version
        rr = ratios(run)
        assert len(rr) == 14 and all(r["correct"] for r in rr)
        runs[version] = {
            "run": rid, "samples_including_warmups": len(run["records"]),
            "cells": rr,
            "geomean_time_ratio": st.geometric_mean(r["wall_ratio"] for r in rr),
            "geomean_rss_ratio": st.geometric_mean(r["rss_ratio"] for r in rr),
            "slower_cells": sum(r["wall_ratio"] > 1 for r in rr),
            "heavier_cells": sum(r["rss_ratio"] > 1 for r in rr),
        }
    pairdir = HERE / "paired-run"
    complete = json.loads((pairdir / "complete.json").read_text())
    raw = (pairdir / "records.jsonl").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == complete["journal_sha256"]
    samples = [json.loads(line) for line in raw.splitlines()]
    assert len(samples) == 160 and all(s["correct"] for s in samples)
    rows = []
    for task in ("symmetry", "kpath", "eos", "bandgap", "inputgen"):
        variants = {name: sorted([r for r in samples if r["task"] == task
                    and r["variant"] == name and not r["warmup"]],
                    key=lambda r: r["rep"]) for name in ("baseline", "candidate")}
        b, c = variants["baseline"], variants["candidate"]
        assert [r["rep"] for r in b] == [r["rep"] for r in c] == list(range(15))
        r = {"task": task, "input": b[0]["input"], "pairs": 15}
        for name, items in variants.items():
            r[name] = {"wall_s": st.median(x["wall_s"] for x in items),
                       "cpu_s": st.median(x["user_s"] + x["sys_s"] for x in items),
                       "rss_mb": st.median(x["max_rss_kb"] / 1024 for x in items)}
        r["time_reduction_percent"] = 100 * (1 - r["candidate"]["wall_s"] / r["baseline"]["wall_s"])
        r["rss_reduction_percent"] = 100 * (1 - r["candidate"]["rss_mb"] / r["baseline"]["rss_mb"])
        # Resample whole A/B pairs, preserving local timing dependence.
        rng = random.Random(20260905)
        boot = []
        for _ in range(2000):
            ii = [rng.randrange(15) for _ in range(15)]
            boot.append(100 * (1 - st.median(c[i]["wall_s"] for i in ii)
                               / st.median(b[i]["wall_s"] for i in ii)))
        boot.sort()
        r["descriptive_95pct_pair_bootstrap"] = [boot[50], boot[1949]]
        rows.append(r)
    result = {"canonical": runs, "paired": rows,
              "scope": "Fresh-process wrapper time, including imports; no QE solver timings.",
              "limits": "One laptop, turbo and background load; intervals are descriptive, not independent hardware replication."}
    assert all(math.isfinite(r["time_reduction_percent"]) for r in rows)
    (HERE / "comparison.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
