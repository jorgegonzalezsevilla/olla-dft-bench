"""Supplementary interleaved A/B check; the canonical harness is unchanged.

Two wheel-only --target directories share the exact same interpreter and
dependencies. Select the installed Olla with PYTHONPATH, assert its version
and import location, then use the original wrapper, inputs and grading.
Fifteen randomized A/B pairs per task, one warmup, persistent private caches.
This representative subset is not the full competitor benchmark.
"""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import random
import shutil
import statistics
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from benchlib import measure
from benchlib.tasks import TASKS, INP


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("baseline", type=Path)
    ap.add_argument("candidate", type=Path)
    ap.add_argument("out", type=Path)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    work = args.out / "work"
    (work / "pp").mkdir(parents=True)
    for p in INP.glob("*.UPF"):
        shutil.copy(p, work / "pp")
    envs = {}
    identities = {}
    for name, path, version in [("baseline", args.baseline, "1.3.0"),
                                ("candidate", args.candidate, "1.3.1")]:
        envs[name] = dict(measure.clean_env(), PYTHONPATH=str(path.resolve()))
        identity = json.loads(subprocess.check_output([
            sys.executable, "-c",
            "import qekit,json; print(json.dumps([qekit.__version__,qekit.__file__]))"
        ], env=envs[name], text=True))
        assert identity[0] == version
        assert Path(identity[1]).resolve().is_relative_to(path.resolve())
        identities[name] = identity
    (args.out / "protocol.json").write_text(json.dumps({
        "seed": 20260905, "reps": 15, "cpu": 0, "python": sys.executable,
        "identities": identities, "cache": "private, persistent after warmup",
        "cases": {task: meta["inputs"][0] for task, meta in TASKS.items()},
        "dependencies": {name: importlib.metadata.version(name) for name in
                         ("numpy", "scipy", "matplotlib", "ase", "spglib", "seekpath")},
        "input_manifest": (INP / "SHA256SUMS").read_text(),
        "wrapper_sha256": hashlib.sha256((ROOT / "tools/ollad.py").read_bytes()).hexdigest(),
    }, indent=2))
    rng = random.Random(20260905)
    records = []
    for task, meta in TASKS.items():
        inp = meta["inputs"][0]
        argv = meta["args"](inp, work)
        ref_result = measure.run_measured([
            sys.executable, str(ROOT / "tools/reference.py"), task, argv[0]
        ], envs["baseline"], str(work))
        assert ref_result["returncode"] == 0 and ref_result["payload"]
        ref = ref_result["payload"]
        if task == "inputgen":
            ref["kgrid_expected"] = [int(x) for x in argv[3].split("x")]
        for rep in range(-1, 15):
            order = list(envs)
            rng.shuffle(order)
            pair = []
            for variant in order:
                shutil.rmtree(work / "gen", ignore_errors=True)
                r = measure.run_measured(measure.wrap_isolation([
                    sys.executable, str(ROOT / "tools/ollad.py"), task, *argv
                ], cpu=0), envs[variant], str(work))
                assert r["returncode"] == 0 and r["payload"], r
                payload = dict(r["payload"])
                assert payload.get("rc", 0) == 0 and not r["timed_out"]
                if task == "inputgen":
                    path = Path(payload["file"])
                    dest = args.out / f"input-{rep}-{variant}.in"
                    shutil.copy(path, dest)
                    rt = measure.run_measured([
                        sys.executable, str(ROOT / "tools/reference.py"),
                        "roundtrip", str(path)
                    ], envs[variant], str(work))
                    assert rt["returncode"] == 0 and rt["payload"]
                    payload["roundtrip"] = rt["payload"]
                    r["input_sha256"] = hashlib.sha256(dest.read_bytes()).hexdigest()
                    # Only comments contain version/time provenance; retain
                    # originals and compare all executable input bytes.
                    body = "\n".join(s for s in path.read_text().splitlines()
                                     if not s.lstrip().startswith(("!", "#")))
                    payload["input_body_sha256"] = hashlib.sha256(body.encode()).hexdigest()
                ok, detail = meta["grade"](payload, ref)
                assert ok is True, detail
                comparable = {k: v for k, v in payload.items() if k != "raw"}
                pair.append(comparable)
                r.update(task=task, input=inp, variant=variant, rep=rep,
                         warmup=rep == -1, correct=ok, detail=detail)
                records.append(r)
                with (args.out / "records.jsonl").open("a") as stream:
                    stream.write(json.dumps(r) + "\n")
            assert pair[0] == pair[1], (task, rep, pair)
        rows = [r for r in records if r["task"] == task and not r["warmup"]]
        med = {name: statistics.median(r["wall_s"] for r in rows
                                      if r["variant"] == name) for name in envs}
        print(task, med, flush=True)
    assert len(records) == 160
    (args.out / "complete.json").write_text(json.dumps({
        "status": "complete", "records": len(records),
        "all_grades_pass": True, "all_paired_payloads_identical": True,
        "journal_sha256": hashlib.sha256((args.out / "records.jsonl").read_bytes()).hexdigest(),
    }, indent=2))


if __name__ == "__main__":
    main()
