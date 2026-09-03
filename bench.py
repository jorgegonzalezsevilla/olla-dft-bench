#!/usr/bin/env python3
"""olla-dft-bench: reproducible benchmarks of Olla-DFT against comparable tools.

  python bench.py env                      show the environment fingerprint and warnings
  python bench.py run [--reps 15] [--e2e-reps 5] [--isolate] [--with-qe] [--tasks a,b] [--label local] [--seed N] [--opp-threshold 1.15]
  python bench.py verify results/<run>     recompute every aggregate from raw samples, check hashes
  python bench.py report results/<run>     regenerate report.md, history.json and docs/index.html
  python bench.py judge-pack results/<run> build the packet for an independent evaluator
"""
import argparse, json, os, shutil, sys, time, hashlib, difflib, random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from benchlib import envinfo, measure, report
from benchlib.tasks import TASKS, TOOLS, INP

PY = str(ROOT / ".venv" / "bin" / "python") if (ROOT / ".venv").exists() else sys.executable
TOOLDIR = ROOT / "tools"


def tool_cmd(wrapper, task, args):
    return [PY, str(TOOLDIR / wrapper), task] + list(args)


def reference(task, args, env, cwd):
    r = measure.run_measured(tool_cmd("reference.py", task, args), env, cwd)
    if r["returncode"] != 0 or not r["payload"]:
        sys.exit(f"reference for {task} failed:\n{r['stderr']}")
    return r["payload"]


def cmd_env(a):
    env = envinfo.collect(PY, sorted(INP.glob("*")))
    print(json.dumps(env, indent=2))
    for w in envinfo.warnings(env):
        print("WARNING:", w, file=sys.stderr)


def cmd_run(a):
    pw = a.pw_x or os.environ.get("BENCH_PW_X") or (str(ROOT / ".qe" / "bin" / "pw.x") if (ROOT / ".qe" / "bin" / "pw.x").exists() else "pw.x")
    os.environ["BENCH_PW_X"] = pw
    run_id = time.strftime("%Y%m%d-%H%M%S")
    rdir = ROOT / "results" / run_id
    work = rdir / "work"; (work / "pp").mkdir(parents=True)
    for upf in INP.glob("*.UPF"):
        shutil.copy(upf, work / "pp")
    inputs = sorted(p for p in INP.glob("*") if p.name != "SHA256SUMS")
    env_info = envinfo.collect(PY, inputs)
    warns = envinfo.warnings(env_info)
    for w in warns:
        print("WARNING:", w, file=sys.stderr)
    cpu = a.cpu if a.cpu is not None else envinfo.fastest_cpu()
    penv = measure.clean_env()
    tasks = [t for t in (a.tasks.split(",") if a.tasks else TASKS) if t in TASKS]
    tools_used = sorted({t for k in tasks for t in TASKS[k]["tools"]}, key=lambda t: (t != "olla-dft", t))
    seed = a.seed if a.seed is not None else int(time.time()) % 100000
    rng = random.Random(seed)
    config = {"reps": a.reps, "cpu": cpu, "isolate": a.isolate, "mem_max": a.mem_max, "label": a.label,
              "tasks": tasks, "tools": tools_used, "with_qe": a.with_qe, "seed": seed,
              "e2e_reps": a.e2e_reps, "opp_threshold": a.opp_threshold}
    records, refs = [], {}

    def wrap(cmd):
        return measure.wrap_isolation(cmd, cpu=cpu, mem_max=a.mem_max if a.isolate else None,
                                      cpu_quota="100%" if a.isolate else None)

    def one(task, inp, tool, rep, warmup):
        meta = TASKS[task]
        args = meta["args"](inp, work)
        if task == "inputgen":
            shutil.rmtree(work / "gen", ignore_errors=True)
            if tool == "olla-dft":
                args = args + [str(refs[(task, inp)].get("kspacing_for_olla"))]
        r = measure.run_measured(wrap(tool_cmd(TOOLS[tool], task, args)), penv, str(work))
        rec = {"task": task, "input": inp, "tool": tool, "rep": rep, "warmup": warmup,
               "wall_s": r["wall_s"], "user_s": r["user_s"], "sys_s": r["sys_s"], "max_rss_kb": r["max_rss_kb"],
               "returncode": r["returncode"], "payload": r["payload"], "stderr_tail": r["stderr"][-600:]}
        if r["payload"] and r["payload"].get("unsupported"):
            rec.update(unsupported=True, reason=r["payload"].get("reason"), returncode=0)
        elif r["returncode"] == 0 and r["payload"]:
            p = dict(r["payload"])
            if task == "inputgen":
                p["roundtrip"] = reference("roundtrip", [p["file"]], penv, str(work))
                if not warmup and rep == 0 and a.with_qe and inp == "Si_relajado.cif":
                    dest = work / "e2e" / tool; dest.mkdir(parents=True, exist_ok=True)
                    shutil.copy(p["file"], dest / "scf.in")
            ok, detail = meta["grade"](p, refs[(task, inp)])
            rec.update(correct=bool(ok), detail=detail, payload=p)
        else:
            rec.update(correct=False, detail=f"exit {r['returncode']}: {r['stderr'][-200:].strip()}")
        records.append(rec)
        flag = "warm" if warmup else f"rep{rep}"
        print(f"  {task:9s} {inp:17s} {tool:9s} {flag:5s} wall={r['wall_s']:.3f}s rss={(r['max_rss_kb'] or 0)//1024}MB "
              f"{'n/a' if rec.get('unsupported') else ('ok' if rec.get('correct') else 'MISMATCH')}", flush=True)

    print(f"run {run_id}: tasks={tasks} tools={tools_used} reps={a.reps} cpu={cpu} isolate={a.isolate}")
    for task in tasks:
        meta = TASKS[task]
        for inp in meta["inputs"]:
            refs[(task, inp)] = reference(task, meta["args"](inp, work)[:1], penv, str(work))
            if task == "inputgen":
                refs[(task, inp)]["kgrid_expected"] = [int(x) for x in meta["args"](inp, work)[3].split("x")]
                ksp = reference("kspacing", [str(INP / inp), meta["args"](inp, work)[3]], penv, str(work))
                refs[(task, inp)]["kspacing_for_olla"] = ksp.get("kspacing")
            for tool in meta["tools"]:
                one(task, inp, tool, -1, True)
            for rep in range(a.reps):
                order = list(meta["tools"]); rng.shuffle(order)   # random order per repetition
                for tool in order:
                    one(task, inp, tool, rep, False)

    e2e = {}
    if a.with_qe and (work / "e2e").exists():
        print(f"end-to-end: running pw.x {a.e2e_reps}x on each tool's Si input")
        dirs = sorted((work / "e2e").iterdir())
        for d in dirs:
            rt = reference("roundtrip", [str(d / "scf.in")], penv, str(work))
            via = next((x["payload"]["via"] for x in records if x["task"] == "inputgen" and x["tool"] == d.name and x.get("payload")), "")
            e2e[d.name] = {"samples": [], "kgrid": rt.get("kgrid"), "ecutwfc": rt.get("ecutwfc"), "via": via}
        for rep in range(a.e2e_reps):
            order = list(dirs); rng.shuffle(order)
            for d in order:
                shutil.rmtree(d / "out", ignore_errors=True)
                r = measure.run_measured(wrap(tool_cmd("run_pw.py", str(d / "scf.in"), [str(d)])), penv, str(d))
                p = r["payload"] or {}
                e2e[d.name]["samples"].append(p)
                print(f"  {d.name:9s} rep{rep} E={p.get('total_energy_Ry')} Ry  iters={p.get('scf_iterations')}  nk={p.get('nkpoints')}  pw.x {p.get('pw_wall_s',0):.2f}s")
        for d in dirs:
            shutil.rmtree(d / "out", ignore_errors=True)
    env_info["load_avg_end"] = envinfo.load_avg()

    run = {"run_id": run_id, "env": env_info, "warnings": warns, "config": config,
           "tasks_meta": {t: {"title": TASKS[t]["title"], "note": TASKS[t]["note"], "inputs": TASKS[t]["inputs"], "tools": TASKS[t]["tools"]} for t in tasks},
           "references": {f"{k[0]}/{k[1]}": v for k, v in refs.items()},
           "records": records, "e2e": e2e}
    run["summary"] = report.aggregate(records)
    shutil.rmtree(work, ignore_errors=True)
    (rdir / "results.json").write_text(json.dumps(run, indent=1, ensure_ascii=False, default=str))
    (rdir / "env.json").write_text(json.dumps(env_info, indent=2))
    write_reports(rdir, run)
    print(f"\nwritten {rdir}/results.json, report.md; dashboard docs/index.html")


def write_reports(rdir, run):
    (rdir / "report.md").write_text(report.markdown(run))
    hist_path = ROOT / "results" / "history.json"
    hist = json.loads(hist_path.read_text()) if hist_path.exists() else {"runs": []}
    hist["runs"] = [h for h in hist["runs"] if h["run_id"] != run["run_id"]]
    slim = {}
    for task, inputs in run["summary"].items():
        for inp, tools in inputs.items():
            for tool, d in tools.items():
                slim.setdefault(task, {}).setdefault(inp, {})[tool] = {
                    "unsupported": d["unsupported"], "wall": d["wall_s"].get("median"),
                    "rss": d["max_rss_mb"].get("median"), "correct": bool(d["correct"]) and all(d["correct"])}
    hist["runs"].append({"run_id": run["run_id"], "timestamp": run["env"]["timestamp_utc"], "cpu": run["env"]["cpu_model"],
                         "label": run["config"].get("label"), "warnings": run["warnings"], "summary": slim,
                         "packages": run["env"]["packages"]})
    hist["runs"].sort(key=lambda h: h["run_id"], reverse=True)
    hist_path.write_text(json.dumps(hist, indent=1))
    (ROOT / "docs").mkdir(exist_ok=True)
    (ROOT / "docs" / "index.html").write_text(report.html(hist))
    idx = ["# Benchmark runs", "", "| run | date (UTC) | label | CPU | olla-dft | warnings |", "|---|---|---|---|---|---|"]
    for h in hist["runs"]:
        idx.append(f"| [{h['run_id']}]({h['run_id']}/report.md) | {h['timestamp']} | {h.get('label')} | {h['cpu']} | {h['packages'].get('olla-dft')} | {len(h['warnings'])} |")
    (ROOT / "results" / "README.md").write_text("\n".join(idx) + "\n")


def load_run(path):
    p = Path(path)
    return p, json.loads((p / "results.json").read_text())


def cmd_report(a):
    rdir, run = load_run(a.run)
    run["summary"] = report.aggregate(run["records"])
    write_reports(rdir, run)
    print("regenerated", rdir / "report.md")


def cmd_verify(a):
    rdir, run = load_run(a.run)
    ok = True
    # 1. inputs unchanged
    sums = dict(line.split()[::-1] for line in (INP / "SHA256SUMS").read_text().splitlines())
    for name, h in run["env"]["inputs_sha256"].items():
        base = Path(name).name
        cur = envinfo.sha256(INP / base) if (INP / base).exists() else None
        if cur != h or sums.get(base) != h:
            ok = False; print(f"FAIL input hash {base}: run={h[:12]} now={str(cur)[:12]} manifest={str(sums.get(base))[:12]}")
    print("inputs: hashes match run and manifest" if ok else "inputs: MISMATCH")
    # 2. aggregates recomputed from raw samples
    recomputed = json.loads(json.dumps(report.aggregate(run["records"]), default=str))
    stored = json.loads(json.dumps(run["summary"], default=str))
    if recomputed != stored:
        ok = False; print("FAIL summary differs from recomputation")
    else:
        print(f"summary: {sum(len(t) for t in recomputed.values())} cells recomputed from {len(run['records'])} raw samples, identical")
    # 3. grades recomputed
    bad = 0
    for r in run["records"]:
        if r.get("payload") and not r.get("unsupported") and r["returncode"] == 0:
            g, _ = TASKS[r["task"]]["grade"](r["payload"], run["references"][f"{r['task']}/{r['input']}"])
            bad += bool(g) != bool(r.get("correct"))
    print(f"grades: {bad} of {len(run['records'])} records disagree with re-grading" if bad else "grades: all records re-graded identically")
    ok &= bad == 0
    # 4. report text matches
    fresh = report.markdown({**run, "summary": recomputed}).splitlines()
    old = (rdir / "report.md").read_text().splitlines()
    if fresh != old:
        ok = False; print("FAIL report.md differs from regeneration:"); print("\n".join(list(difflib.unified_diff(old, fresh, lineterm=""))[:40]))
    else:
        print("report.md: identical to regeneration")
    print("VERIFY", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)


def cmd_judge(a):
    rdir, run = load_run(a.run)
    slim = {k: v for k, v in run.items() if k != "records"}
    slim["records_sha256"] = hashlib.sha256(json.dumps(run["records"], sort_keys=True, default=str).encode()).hexdigest()
    out = ROOT / "judge" / f"packet_{run['run_id']}.md"
    out.write_text("\n\n".join([
        (ROOT / "protocol" / "JUDGE.md").read_text(),
        "# Report under evaluation\n\n" + (rdir / "report.md").read_text(),
        "# results.json (records omitted; their SHA-256 is given so they can be checked)\n\n```json\n" + json.dumps(slim, indent=1, default=str) + "\n```",
    ]))
    print("wrote", out, "- give this file to an independent model or reviewer; store the verdict in judge/verdicts/")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("env").set_defaults(f=cmd_env)
    r = sub.add_parser("run"); r.set_defaults(f=cmd_run)
    r.add_argument("--reps", type=int, default=15); r.add_argument("--e2e-reps", type=int, default=5); r.add_argument("--seed", type=int); r.add_argument("--opp-threshold", type=float, default=1.15); r.add_argument("--isolate", action="store_true", help="systemd scope with MemoryMax and CPUQuota=100%%")
    r.add_argument("--mem-max", default="3G"); r.add_argument("--cpu", type=int); r.add_argument("--tasks"); r.add_argument("--label", default="local")
    r.add_argument("--with-qe", action="store_true", help="also run pw.x on each tool's Si input (needs pw.x)")
    r.add_argument("--pw-x", help="pw.x executable to use (default: BENCH_PW_X env, else ./.qe/bin/pw.x if present, else pw.x on PATH)")
    for name, f in (("verify", cmd_verify), ("report", cmd_report), ("judge-pack", cmd_judge)):
        s = sub.add_parser(name); s.add_argument("run"); s.set_defaults(f=f)
    a = ap.parse_args(); a.f(a)
