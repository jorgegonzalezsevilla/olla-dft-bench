"""Markdown and HTML reports generated only from results.json. No number in a report exists
that cannot be recomputed from the raw samples by `bench.py verify`."""
import json, statistics as st
from pathlib import Path

def agg(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return {"n": 0}
    q = st.quantiles(xs, n=4) if len(xs) >= 2 else [xs[0], xs[0], xs[0]]
    return {"n": len(xs), "median": st.median(xs), "min": min(xs), "max": max(xs),
            "iqr": q[2] - q[0], "mean": st.fmean(xs), "stdev": st.pstdev(xs) if len(xs) > 1 else 0.0}

def aggregate(results):
    """results: list of measurement records -> nested summary {task: {input: {tool: {...}}}}"""
    out = {}
    for r in results:
        d = out.setdefault(r["task"], {}).setdefault(r["input"], {}).setdefault(r["tool"], {"samples": []})
        d["samples"].append(r)
    for task in out.values():
        for inp in task.values():
            for tool, d in inp.items():
                s = [x for x in d["samples"] if not x.get("warmup")]
                d["unsupported"] = any(x.get("unsupported") for x in s)
                d["reason"] = next((x.get("reason") for x in s if x.get("reason")), None)
                d["failed"] = sum(1 for x in s if x.get("returncode") not in (0, None) and not x.get("unsupported"))
                d["wall_s"] = agg([x["wall_s"] for x in s if x.get("returncode") == 0])
                d["cpu_s"] = agg([(x["user_s"] or 0) + (x["sys_s"] or 0) for x in s if x.get("returncode") == 0 and x.get("user_s") is not None])
                d["max_rss_mb"] = agg([x["max_rss_kb"] / 1024 for x in s if x.get("returncode") == 0 and x.get("max_rss_kb")])
                d["correct"] = [x.get("correct") for x in s if x.get("returncode") == 0]
                d["detail"] = next((x.get("detail") for x in s if x.get("detail")), None)
                d["via"] = next(((x.get("payload") or {}).get("via") for x in s if x.get("payload")), None)
                del d["samples"]
    return out

def _fmt(a, key="median", unit="", digits=3):
    if not a or a.get("n", 0) == 0:
        return "—"
    return f"{a[key]:.{digits}f}{unit}"

def markdown(run):
    env, summ, tasks = run["env"], run["summary"], run["tasks_meta"]
    L = [f"# Olla-DFT benchmark — run {run['run_id']}", "",
         f"*Generated from `results.json`; every number is recomputable with `python bench.py verify`.*", "",
         "## Environment", "",
         f"- CPU: {env.get('cpu_model')} ({env.get('cpu_count')} logical CPUs), pinned to CPU {run['config'].get('cpu')}",
         f"- RAM: {round((env.get('mem_total_kb') or 0)/1048576, 1)} GiB; governor `{env.get('governor')}`; turbo disabled: `{env.get('intel_no_turbo') == '1'}`",
         f"- OS: {env.get('os')}; {env.get('python')}",
         f"- Packages: " + ", ".join(f"{k} {v}" for k, v in sorted(env.get("packages", {}).items())),
         f"- Repetitions per cell: {run['config']['reps']} (+1 warm-up, discarded); threads per process: 1; order interleaved across tools",
         f"- Load average at start: {env.get('load_avg_start')}", ""]
    if run.get("warnings"):
        L += ["> **Environment warnings**", ""] + [f"> - {w}" for w in run["warnings"]] + [""]
    L += ["## How to read the tables", "",
          "Wall time is the median of a fresh process per repetition (imports included, because that is what the",
          "command line costs). CPU is user+system time; RSS is peak resident memory of the process. `correct` is",
          "the deterministic grade against an independent reference described in each task's note. `—` means the",
          "tool does not cover the task; that is a coverage fact, not a failure.", ""]
    opp = []
    for task, inputs in summ.items():
        meta = tasks[task]
        L += [f"## {meta['title']}", "", f"*{meta['note']}*", "",
              "| input | tool | wall s (median) | min | IQR | CPU s | peak RSS MB | correct | detail |", "|---|---|---|---|---|---|---|---|---|"]
        for inp, tools in inputs.items():
            fastest = min((d["wall_s"]["median"], t) for t, d in tools.items() if d["wall_s"].get("n")) if any(d["wall_s"].get("n") for d in tools.values()) else (None, None)
            for tool, d in tools.items():
                if d["unsupported"]:
                    L.append(f"| {inp} | {tool} | — | — | — | — | — | n/a | not supported: {d['reason']} |")
                    continue
                c = d["correct"]; cs = "✔" if c and all(c) else ("✘" if c else "?")
                mark = " **←fastest**" if fastest[1] == tool else ""
                L.append(f"| {inp} | {tool} | {_fmt(d['wall_s'])}{mark} | {_fmt(d['wall_s'],'min')} | {_fmt(d['wall_s'],'iqr')} | {_fmt(d['cpu_s'])} | {_fmt(d['max_rss_mb'],digits=0)} | {cs} | {d['detail'] or ''} |")
                if tool == "olla-dft":
                    others = [x for t, x in tools.items() if t != tool and x["wall_s"].get("n")]
                    if others:
                        best = min(x["wall_s"]["median"] for x in others)
                        if d["wall_s"].get("n") and d["wall_s"]["median"] > 1.5 * best:
                            opp.append(f"{task}/{inp}: Olla-DFT wall time {d['wall_s']['median']:.2f} s vs best competitor {best:.2f} s ({d['wall_s']['median']/best:.1f}×)")
                        bestm = min(x["max_rss_mb"]["median"] for x in others if x["max_rss_mb"].get("n"))
                        if d["max_rss_mb"].get("n") and d["max_rss_mb"]["median"] > 1.5 * bestm:
                            opp.append(f"{task}/{inp}: Olla-DFT peak RSS {d['max_rss_mb']['median']:.0f} MB vs best competitor {bestm:.0f} MB")
                    if c and not all(c):
                        opp.append(f"{task}/{inp}: Olla-DFT result did not match the reference ({d['detail']})")
        L.append("")
    if run.get("e2e"):
        L += ["## End to end with pw.x (same binary, inputs from each tool)", "",
              "| tool | k-grid | ecutwfc | total energy (Ry) | SCF iterations | pw.x wall s | input generated by |", "|---|---|---|---|---|---|---|"]
        for tool, e in run["e2e"].items():
            L.append(f"| {tool} | {e.get('kgrid')} | {e.get('ecutwfc')} | {e.get('total_energy_Ry')} | {e.get('scf_iterations')} | {e.get('pw_wall_s', 0):.1f} | {e.get('via','')} |")
        es = [e["total_energy_Ry"] for e in run["e2e"].values() if e.get("total_energy_Ry") is not None]
        if len(es) > 1:
            L += ["", f"Spread of total energies across tools: {max(es)-min(es):.2e} Ry (identical physics ⇒ should be ≲ 1e-6 Ry). "]
        L.append("")
    L += ["## Coverage matrix", "", "| task | " + " | ".join(run["config"]["tools"]) + " |", "|---|" + "---|" * len(run["config"]["tools"])]
    for task, inputs in summ.items():
        row = []
        for t in run["config"]["tools"]:
            cells = [d for inp in inputs.values() for tt, d in inp.items() if tt == t]
            row.append("—" if not cells else ("✘ n/a" if all(d["unsupported"] for d in cells) else "✔"))
        L.append(f"| {task} | " + " | ".join(row) + " |")
    L += ["", "## Areas of opportunity for Olla-DFT (generated automatically, same rule for every tool)", ""]
    L += [f"- {o}" for o in opp] or ["- none triggered by the automatic rules (>1.5× slower / >1.5× memory / mismatch)"]
    L += ["", "## Known limitations of this benchmark", "",
          "- One consumer laptop, hybrid CPU: absolute times are only comparable within one run; compare ratios across runs.",
          "- Post-processing tasks are small; import time dominates and favours light dependency trees.",
          "- Only tasks every tool can express with the same inputs are compared; Olla-DFT features without a counterpart are not benchmarked here, and features of the other tools that Olla-DFT lacks are visible in the coverage matrix.",
          "- Correctness is checked against independent code for the numeric tasks; for k-paths, only agreement with one convention is measured.", ""]
    return "\n".join(L)

def html(history):
    """Static dashboard: embeds the history JSON and renders tables client-side."""
    data = json.dumps(history)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Olla-DFT benchmark dashboard</title>
<style>body{{font:14px system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#222}}table{{border-collapse:collapse;width:100%;margin:1rem 0}}td,th{{border:1px solid #ddd;padding:4px 8px;text-align:left}}th{{background:#f4f4f4}}.bar{{height:10px;background:#4a7;display:inline-block}}.o{{background:#e63}}small{{color:#666}}h2{{margin-top:2rem}}</style></head><body>
<h1>Olla-DFT benchmark dashboard</h1><p><small>Rendered from <code>results/history.json</code>. Medians of wall time in seconds; bar length relative to the slowest tool in the row. Olla-DFT in orange, competitors in green. Lower is better. Nothing here is hand-edited.</small></p>
<div id="app"></div>
<script>const H={data};const app=document.getElementById('app');
for(const run of H.runs){{const h=document.createElement('h2');h.textContent=`Run ${{run.run_id}} — ${{run.timestamp}} — ${{run.cpu}}`;app.appendChild(h);
if(run.warnings.length){{const w=document.createElement('p');w.innerHTML='<b>Warnings:</b> '+run.warnings.join(' · ');app.appendChild(w);}}
for(const [task,inputs] of Object.entries(run.summary)){{const t=document.createElement('table');t.innerHTML=`<tr><th colspan=6>${{task}}</th></tr><tr><th>input</th><th>tool</th><th>wall s</th><th></th><th>RSS MB</th><th>correct</th></tr>`;
for(const [inp,tools] of Object.entries(inputs)){{const mx=Math.max(...Object.values(tools).map(d=>d.wall||0));for(const [tool,d] of Object.entries(tools)){{const tr=document.createElement('tr');
tr.innerHTML=`<td>${{inp}}</td><td>${{tool}}</td><td>${{d.unsupported?'—':d.wall.toFixed(3)}}</td><td>${{d.unsupported?'<small>n/a</small>':`<span class="bar ${{tool==='olla-dft'?'o':''}}" style="width:${{(200*d.wall/mx)|0}}px"></span>`}}</td><td>${{d.unsupported?'—':d.rss.toFixed(0)}}</td><td>${{d.unsupported?'n/a':(d.correct?'✔':'✘')}}</td>`;t.appendChild(tr);}}}}app.appendChild(t);}}}}
</script></body></html>"""
