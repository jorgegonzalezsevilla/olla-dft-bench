"""Markdown and HTML reports generated only from results.json. Every number is recomputable by
`bench.py verify`; the bootstrap uses a fixed seed so the report regenerates byte for byte."""
import json, random, statistics as st
from .validation import e2e_success

def agg(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return {"n": 0}
    q = st.quantiles(xs, n=4) if len(xs) >= 2 else [xs[0], xs[0], xs[0]]
    return {"n": len(xs), "median": st.median(xs), "min": min(xs), "max": max(xs),
            "iqr": q[2] - q[0], "mean": st.fmean(xs), "stdev": st.pstdev(xs) if len(xs) > 1 else 0.0}

def aggregate(results):
    out = {}
    for r in results:
        d = out.setdefault(r["task"], {}).setdefault(r["input"], {}).setdefault(r["tool"], {"samples": []})
        d["samples"].append(r)
    for task in out.values():
        for inp in task.values():
            for tool, d in inp.items():
                s = [x for x in d["samples"] if not x.get("warmup")]
                ok = [x for x in s if x.get("returncode") == 0 and not x.get("unsupported")]
                d["unsupported"] = bool(s) and all(x.get("unsupported") for x in s)
                d["n"] = len(s)
                d["comparable"] = all(x.get("comparable", True) for x in s)
                d["reason"] = next((x.get("reason") for x in s if x.get("reason")), None)
                d["failed"] = sum(1 for x in s if not x.get("unsupported") and
                                  (x.get("returncode") != 0 or not x.get("payload") or
                                   x.get("correct") is False or (x.get("payload") or {}).get("rc", 0) != 0))
                d["wall_s"] = agg([x["wall_s"] for x in ok])
                d["cpu_s"] = agg([(x["user_s"] or 0) + (x["sys_s"] or 0) for x in ok if x.get("user_s") is not None])
                d["max_rss_mb"] = agg([x["max_rss_kb"] / 1024 for x in ok if x.get("max_rss_kb")])
                d["correct"] = [bool(x.get("correct")) and x.get("returncode") == 0
                                and (x.get("payload") or {}).get("rc", 0) == 0
                                for x in s if not x.get("unsupported")]
                d["detail"] = next((x.get("detail") for x in ok if x.get("detail")), None)
                d["via"] = next(((x.get("payload") or {}).get("via") for x in ok if x.get("payload")), None)
                del d["samples"]
    return out

def raw_walls(records, task, inp, tool):
    return [x["wall_s"] for x in records if x["task"] == task and x["input"] == inp and x["tool"] == tool
            and not x.get("warmup") and x.get("returncode") == 0 and not x.get("unsupported")]

def boot_ratio(a, b, n=2000, seed=0):
    """95% bootstrap CI of median(a)/median(b)."""
    rng = random.Random(seed); rs = []
    for _ in range(n):
        sa = [rng.choice(a) for _ in a]; sb = [rng.choice(b) for _ in b]
        rs.append(st.median(sa) / st.median(sb))
    rs.sort()
    return rs[int(0.025 * n)], rs[int(0.975 * n) - 1]

def _fmt(a, key="median", unit="", digits=3):
    if not a or a.get("n", 0) == 0:
        return "—"
    return f"{a[key]:.{digits}f}{unit}"

def ratios(run):
    """Per contested cell: olla-dft vs best *supported* competitor."""
    rows = []
    for task, inputs in run["summary"].items():
        for inp, tools in inputs.items():
            o = tools.get("olla-dft")
            if not o or o["unsupported"] or o.get("failed") or not o.get("comparable", True) or not o["wall_s"].get("n"):
                continue
            comp = {t: d for t, d in tools.items() if t != "olla-dft" and not d["unsupported"] and not d.get("failed") and d.get("comparable", True) and d["wall_s"].get("n")}
            if not comp:
                continue
            bt, bd = min(comp.items(), key=lambda kv: kv[1]["wall_s"]["median"])
            bm = min(comp.values(), key=lambda d: d["max_rss_mb"]["median"] if d["max_rss_mb"].get("n") else 1e9)
            lo, hi = boot_ratio(raw_walls(run["records"], task, inp, "olla-dft"), raw_walls(run["records"], task, inp, bt))
            rows.append({"task": task, "input": inp, "vs": bt,
                         "wall_ratio": o["wall_s"]["median"] / bd["wall_s"]["median"], "ci": (lo, hi),
                         "min_ratio": o["wall_s"]["min"] / bd["wall_s"]["min"],
                         "rss_ratio": o["max_rss_mb"]["median"] / bm["max_rss_mb"]["median"] if o["max_rss_mb"].get("n") and bm["max_rss_mb"].get("n") else None,
                         "correct": bool(o["correct"]) and all(o["correct"])})
    return rows

def e2e_rows(e2e):
    rows = {}
    for tool, e in e2e.items():
        s = e.get("samples") or []
        okk = [x for x in s if e2e_success(x)]
        rows[tool] = {"n": len(okk), "energy": st.median(x["total_energy_Ry"] for x in okk) if okk else None,
                      "failed": len(s) - len(okk),
                      "energy_min": min((x["total_energy_Ry"] for x in okk), default=None),
                      "energy_max": max((x["total_energy_Ry"] for x in okk), default=None),
                      "iters": st.median(x["scf_iterations"] for x in okk) if okk else None, "nk": sorted({x.get("nkpoints") for x in okk}) if okk else None,
                      "wall": agg([x["pw_wall_s"] for x in okk]), "kgrid": e.get("kgrid"), "ecutwfc": e.get("ecutwfc"), "via": e.get("via", "")}
    return rows

def markdown(run):
    env, summ, tasks, cfg = run["env"], run["summary"], run["tasks_meta"], run["config"]
    thr = cfg.get("opp_threshold", 1.15)
    L = [f"# Olla-DFT benchmark — run {run['run_id']}", "",
         "*Generated from `results.json`; every number is recomputable with `python bench.py verify`.*", "",
         "## Environment", "",
         f"- CPU: {env.get('cpu_model')} ({env.get('cpu_count')} logical CPUs), pinned to CPU {cfg.get('cpu')}",
         f"- RAM: {round((env.get('mem_total_kb') or 0)/1048576, 1)} GiB; governor `{env.get('governor')}`; turbo disabled: `{env.get('intel_no_turbo') == '1'}`",
         f"- OS: {env.get('os')}; {env.get('python')}; pw.x: {env.get('pw_x_version') or env.get('pw_x')}",
         "- Packages: " + ", ".join(f"{k} {v}" for k, v in sorted(env.get("packages", {}).items())),
         f"- Olla-DFT source: `{(env.get('olla_dft_source') or {}).get('url', '?')}` @ `{((env.get('olla_dft_source') or {}).get('vcs_info') or {}).get('commit_id', '?')}`",
         f"- Repetitions per cell: {cfg['reps']} (+1 warm-up, discarded); threads per process: 1; tool order shuffled per repetition (seed {cfg.get('seed')})",
         f"- End-to-end repetitions: {cfg.get('e2e_reps', 1)}; opportunity threshold: {thr}× (stated here, applied identically to time and memory)",
         f"- Load average at start / end: {env.get('load_avg_start')} / {env.get('load_avg_end')}", ""]
    L += [f"**Run status: {run.get('status', 'legacy/unvalidated')}**", ""]
    if run.get("validation_errors"):
        L += ["Execution/validation failures:", ""] + [f"- {e}" for e in run["validation_errors"]] + [""]
    if run.get("warnings"):
        L += ["> **Environment warnings**", ""] + [f"> - {w}" for w in run["warnings"]] + [""]
    L += ["## How to read the tables", "",
          "Wall time is the median of a fresh process per repetition (imports included, because that is what the",
          "command line costs). CPU is user+system time; RSS is peak resident memory. `correct` is the deterministic",
          "grade against the reference described in each task's note; where the reference shares a backend with a",
          "contestant, the note says so and the grade only shows the wrapper passes the result through. `—` means",
          "the tool does not cover the task; that is a coverage fact, not a failure, and such cells are excluded from",
          "every speed or memory comparison.", ""]
    for task, inputs in summ.items():
        meta = tasks[task]
        L += [f"## {meta['title']}", "", f"*{meta['note']}*", "",
              "| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | n | failures | correct | detail |", "|---|---|---|---|---|---|---|---|---|---|---|"]
        for inp, tools in inputs.items():
            sup = [(d["wall_s"]["median"], t) for t, d in tools.items() if not d["unsupported"] and not d.get("failed") and d.get("comparable", True) and d["wall_s"].get("n")]
            fastest = min(sup)[1] if sup else None
            for tool, d in tools.items():
                if d["unsupported"]:
                    L.append(f"| {inp} | {tool} | — | — | — | — | — | {d.get('n', 0)} | 0 | n/a | not supported: {d['reason']} |"); continue
                c = d["correct"]; cs = "✔" if c and all(c) else ("✘" if c else "?")
                if not d.get("comparable", True) and not d.get("failed"):
                    cs = "other convention"
                mark = " **←fastest**" if fastest == tool else ""
                L.append(f"| {inp} | {tool} | {_fmt(d['wall_s'])}{mark} | {_fmt(d['wall_s'],'min')} | {_fmt(d['wall_s'],'iqr')} | {_fmt(d['cpu_s'])} | {_fmt(d['max_rss_mb'],digits=0)} | {d.get('n', 0)} | {d.get('failed', 0)} | {cs} | {d['detail'] or ''} |")
        L.append("")
    # ---- ratio table ----
    R = ratios(run); opp = []
    L += ["## Olla-DFT relative to the best supported competitor, every contested cell", "",
          "Ratios > 1 mean Olla-DFT is slower or heavier. `min` ratio uses the fastest sample of each (robust to background noise); the CI is a 95 % bootstrap of the ratio of medians, conditional on the chosen competitor; descriptive, not a multiple-comparison significance test.", "",
          "| task | input | vs | wall ratio (median) | 95 % CI | wall ratio (min) | RSS ratio |", "|---|---|---|---|---|---|---|"]
    for r in R:
        L.append(f"| {r['task']} | {r['input']} | {r['vs']} | {r['wall_ratio']:.2f} | {r['ci'][0]:.2f}–{r['ci'][1]:.2f} | {r['min_ratio']:.2f} | {r['rss_ratio']:.2f} |" if r['rss_ratio'] else
                 f"| {r['task']} | {r['input']} | {r['vs']} | {r['wall_ratio']:.2f} | {r['ci'][0]:.2f}–{r['ci'][1]:.2f} | {r['min_ratio']:.2f} | — |")
    if R:
        slower = sum(r["wall_ratio"] > 1 for r in R); heavier = sum((r["rss_ratio"] or 0) > 1 for r in R)
        gm = st.geometric_mean([r["wall_ratio"] for r in R]); gmr = st.geometric_mean([r["rss_ratio"] for r in R if r["rss_ratio"]])
        L += ["", f"**Summary:** Olla-DFT is slower than the best supported competitor in {slower} of {len(R)} contested cells "
              f"(geometric-mean wall ratio {gm:.2f}×, min-based {st.geometric_mean([r['min_ratio'] for r in R]):.2f}×) and uses more peak memory in {heavier} of {len(R)} (geometric mean {gmr:.2f}×).", ""]
        for r in R:
            if r["wall_ratio"] > thr:
                tag = "" if r["ci"][0] > 1.0 else " — descriptive CI includes 1"
                opp.append(f"{r['task']}/{r['input']}: {r['wall_ratio']:.2f}× the wall time of {r['vs']} (95 % CI {r['ci'][0]:.2f}–{r['ci'][1]:.2f}){tag}")
            if r["rss_ratio"] and r["rss_ratio"] > thr:
                opp.append(f"{r['task']}/{r['input']}: {r['rss_ratio']:.2f}× the peak memory of the lightest competitor")
            if not r["correct"]:
                opp.append(f"{r['task']}/{r['input']}: result did not match the reference")
        if slower == len(R):
            opp.append(f"Olla-DFT is slower in every contested cell: the benchmark does not isolate the cause of this overhead (geometric mean {gm:.2f}×)")
        if heavier == len(R):
            opp.append(f"Olla-DFT uses more peak memory in every contested cell (geometric mean {gmr:.2f}×)")
    for task, inputs in summ.items():
        for inp, tools in inputs.items():
            d = tools.get("olla-dft", {})
            if d.get("failed"):
                opp.append(f"{task}/{inp}: {d['failed']} failed or incorrect samples")
    # ---- e2e ----
    if run.get("e2e"):
        E = e2e_rows(run["e2e"])
        L += ["## End to end with pw.x (same binary, same k-grid and cutoffs, inputs from each tool)", "",
              "| tool | k-grid | irreducible k | ecutwfc | total energy (Ry) | SCF iterations | pw.x wall s (median of n) | n | input generated by |", "|---|---|---|---|---|---|---|---|---|"]
        for tool, e in E.items():
            if e["failed"]:
                L += [f"**{tool}: {e['failed']} failed/unconverged QE samples.**", ""]
            L.append(f"| {tool} | {e['kgrid']} | {e['nk']} | {e['ecutwfc']} | {e['energy']} | {e['iters']} | {_fmt(e['wall'], digits=2)} | {e['n']} | {e['via']} |")
        es = [x["total_energy_Ry"] for e in run["e2e"].values() for x in e.get("samples", []) if e2e_success(x)]
        if len(es) > 1:
            L += ["", f"Spread of all total energies across tools and repetitions: {max(es)-min(es):.2e} Ry. Same grid and cutoffs should agree to ≲ 1e-6 Ry; the number of irreducible k-points may differ if a tool writes the cell differently, which is itself a difference in the input."]
        o = E.get("olla-dft"); others = [e for t, e in E.items() if t != "olla-dft" and e["energy"] is not None]
        if o and o["energy"] is not None and others:
            bi = min(e["iters"] or 1e9 for e in others); bt = min(e["wall"]["median"] for e in others if e["wall"].get("n"))
            if (o["iters"] or 0) > thr * bi:
                opp.append(f"end-to-end/Si: Olla-DFT's input needed {o['iters']} SCF iterations vs {bi} for the best competitor at the same energy (its defaults, e.g. mixing_beta, differ)")
            if o["wall"].get("n") and o["wall"]["median"] > thr * bt:
                opp.append(f"end-to-end/Si: pw.x took {o['wall']['median']:.2f} s on Olla-DFT's input vs {bt:.2f} s on the best competitor's")
            if any(abs(e["energy"] - o["energy"]) > 1e-6 for e in others):
                opp.append("end-to-end/Si: total energy from Olla-DFT's input differs by > 1e-6 Ry from another tool's")
        L.append("")
    L += ["## Coverage matrix", "", "| task | " + " | ".join(cfg["tools"]) + " |", "|---|" + "---|" * len(cfg["tools"])]
    for task, inputs in summ.items():
        row = []
        for t in cfg["tools"]:
            cells = [d for inp in inputs.values() for tt, d in inp.items() if tt == t]
            n_ok = sum(1 for d in cells if not d["unsupported"])
            row.append("—" if not cells else (f"✔ {n_ok}/{len(cells)} inputs" if 0 < n_ok < len(cells) else ("✘ n/a" if n_ok == 0 else "✔")))
        L.append(f"| {task} | " + " | ".join(row) + " |")
    L += ["", f"## Areas of opportunity for Olla-DFT (generated automatically; threshold {thr}×, same rule for every tool)", ""]
    L += [f"- {o}" for o in opp] or [f"- none triggered (nothing above {thr}× and no mismatch)"]
    L += ["", "## Known limitations of this benchmark", "",
          "- One consumer laptop, hybrid CPU: absolute times are only comparable within one run; compare ratios across runs.",
          "- Post-processing tasks are small; import time dominates and favours light dependency trees. That is a real cost for a CLI tool, but it is not algorithmic speed.",
          "- Only tasks every tool can express with the same inputs are compared; Olla-DFT features without a counterpart are not benchmarked here, and features of the other tools that Olla-DFT lacks are visible in the coverage matrix.",
          "- symmetry and kpath references share a backend with some contestants (stated in the notes); eos and bandgap references are independent code.",
          "- The end-to-end stage uses one small system (Si, 2 atoms).", ""]
    return "\n".join(L)

def html(history):
    data = json.dumps(history).replace("<", "\\u003c")
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Olla-DFT benchmark dashboard</title>
<style>body{{font:14px system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#222}}table{{border-collapse:collapse;width:100%;margin:1rem 0}}td,th{{border:1px solid #ddd;padding:4px 8px;text-align:left}}th{{background:#f4f4f4}}.bar{{height:10px;background:#4a7;display:inline-block}}.o{{background:#e63}}small{{color:#666}}h2{{margin-top:2rem}}</style></head><body>
<nav aria-label="Related results"><a href="publication-1.2.0/index.html">Recuperación y explorador · Español</a> · <a href="publication-1.2.0/index-en.html">Recovery figures and explorer · English</a></nav>
<h1>Olla-DFT benchmark dashboard</h1><p><small>Rendered from <code>results/history.json</code>. Medians of wall time in seconds; bar length relative to the slowest supported tool in the row. Olla-DFT in orange, competitors in green. Lower is better. Nothing here is hand-edited.</small></p>
<div id="app"></div>
<script>const H={data};const app=document.getElementById('app');const fmt=(v,n)=>Number.isFinite(v)?v.toFixed(n):'—';const esc=v=>String(v).replace(/[&<>]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;'}}[c]));
for(const run of H.runs){{const h=document.createElement('h2');h.textContent=`Run ${{run.run_id}} — ${{run.timestamp}} — ${{run.label}} — ${{run.cpu}}`;app.appendChild(h);
if(run.warnings.length){{const w=document.createElement('p');w.textContent='Warnings: '+run.warnings.join(' · ');app.appendChild(w);}}
for(const [task,inputs] of Object.entries(run.summary)){{const t=document.createElement('table');t.innerHTML=`<tr><th colspan=6>${{esc(task)}}</th></tr><tr><th>input</th><th>tool</th><th>wall s</th><th></th><th>RSS MB</th><th>correct</th></tr>`;
for(const [inp,tools] of Object.entries(inputs)){{const mx=Math.max(...Object.values(tools).filter(d=>!d.unsupported).map(d=>d.wall||0));for(const [tool,d] of Object.entries(tools)){{const tr=document.createElement('tr');
tr.innerHTML=`<td>${{esc(inp)}}</td><td>${{esc(tool)}}</td><td>${{d.unsupported?'—':fmt(d.wall,3)}}</td><td>${{d.unsupported?'<small>n/a</small>':`<span class="bar ${{tool==='olla-dft'?'o':''}}" style="width:${{(200*d.wall/mx)|0}}px"></span>`}}</td><td>${{d.unsupported?'—':fmt(d.rss,0)}}</td><td>${{d.unsupported?'n/a':(d.comparable===false?'other convention':(d.correct?'✔':'✘'))}}</td>`;t.appendChild(tr);}}}}app.appendChild(t);}}}}
</script></body></html>"""
