"""Completeness, execution success, and finite-value checks for recorded runs."""
import math
from collections import Counter
from .tasks import TASKS


def e2e_success(p):
    return (p.get('rc') == 0 and p.get('converged') is True and p.get('job_done') is True
            and isinstance(p.get('total_energy_Ry'), (int, float))
            and math.isfinite(p['total_energy_Ry']) and isinstance(p.get('scf_iterations'), int)
            and p['scf_iterations'] > 0)


def check_run(run, strict=True):
    errors = []
    cfg = run['config']
    n = cfg.get('reps', 0)
    selected = cfg.get('tasks', [])
    if not isinstance(n, int) or n < 1 or not selected or len(set(selected)) != len(selected):
        return ['invalid task list or repetitions']
    expected = Counter()
    for task in selected:
        if task not in TASKS:
            errors.append(f'unknown task {task}')
            continue
        meta = TASKS[task] if strict else run['tasks_meta'][task]
        for inp in meta['inputs']:
            if f'{task}/{inp}' not in run['references']:
                errors.append(f'missing reference {task}/{inp}')
            for tool in meta['tools']:
                for rep in [-1, *range(n)]:
                    expected[task, inp, tool, rep, rep == -1] += 1
    actual = Counter((r['task'], r['input'], r['tool'], r['rep'], r['warmup']) for r in run['records'])
    if actual != expected:
        errors.append('missing, duplicate or unexpected samples (including warmups)')
    for r in run['records']:
        label = f"{r['task']}/{r['input']}/{r['tool']}/{r['rep']}"
        if r.get('returncode') != 0 or r.get('timed_out') or (r.get('payload') or {}).get('rc', 0) != 0:
            errors.append(f'execution failed: {label}')
        if r.get('unsupported'):
            if not r.get('reason'):
                errors.append(f'unsupported without reason: {label}')
            continue
        if not r.get('payload') or r.get('correct') is False:
            # Older k-path grades use False for an alternate convention.
            if strict or r['task'] != 'kpath':
                errors.append(f'missing or incorrect result: {label}')
        if strict and r.get('correct') is None and not (r['task'] == 'kpath' and r.get('comparable') is False):
            errors.append(f'ungraded result: {label}')
        for field in ('wall_s', 'user_s', 'sys_s', 'max_rss_kb'):
            x = r.get(field)
            if not isinstance(x, (int, float)) or not math.isfinite(x) or x < 0:
                errors.append(f'invalid {field}: {label}')
    if strict:
        expected_artifacts = set()
        if 'inputgen' in selected:
            for inp in TASKS['inputgen']['inputs']:
                for tool in TASKS['inputgen']['tools']:
                    expected_artifacts.add(f'artifacts/inputgen/{inp}/{tool}/scf.in')
        if cfg.get('with_qe'):
            for tool in TASKS['inputgen']['tools']:
                for rep in range(cfg.get('e2e_reps', 1)):
                    for suffix in ('pw.out', 'pw.stderr'):
                        expected_artifacts.add(f'artifacts/qe/{tool}/rep-{rep}-{suffix}')
        if set(run.get('artifacts_sha256', {})) != expected_artifacts:
            errors.append('missing or unexpected retained artifacts')
    if cfg.get('with_qe'):
        if 'inputgen' not in selected:
            errors.append('--with-qe requires inputgen')
        expected_tools = set(TASKS['inputgen']['tools'])
        if set(run.get('e2e', {})) != expected_tools:
            errors.append('missing or unexpected QE tools')
        energies = []
        for tool, item in run.get('e2e', {}).items():
            samples = item.get('samples', [])
            if len(samples) != cfg.get('e2e_reps', 1):
                errors.append(f'wrong QE sample count: {tool}')
            for p in samples:
                valid = e2e_success(p) if strict else (p.get('rc', 0) == 0 and p.get('total_energy_Ry') is not None)
                if not valid:
                    errors.append(f'QE failed or unconverged: {tool}')
                else:
                    energies.append(p['total_energy_Ry'])
        if energies and max(energies) - min(energies) > 1e-6:
            errors.append('QE energies disagree across tools or repetitions')
    return errors
