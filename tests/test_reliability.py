"""Adversarial regressions: data integrity must survive failed or partial runs."""
import copy
import json
import os
import shutil
import subprocess
import sys
import time

import pytest
from benchlib import measure, report, tasks, validation
from test_bench import ROOT, PY, _rec


def test_timeout_kills_descendants(tmp_path):
    marker = tmp_path / 'escaped'
    child = f'import time;time.sleep(.5);open({str(marker)!r},"w").write("bad")'
    code = f'import subprocess,time;subprocess.Popen([{sys.executable!r},"-c",{child!r}]);time.sleep(60)'
    r = measure.run_measured([sys.executable, '-c', code], dict(os.environ), str(tmp_path), timeout=.15)
    assert r['timed_out'] and r['returncode'] != 0 and r['wall_s'] < 3
    time.sleep(.6)
    assert not marker.exists()


def test_configuration_is_private(monkeypatch, tmp_path):
    monkeypatch.setenv('XDG_CONFIG_HOME', str(tmp_path / 'personal'))
    monkeypatch.setenv('XDG_CACHE_HOME', str(tmp_path / 'cache'))
    env = measure.clean_env()
    assert env['XDG_CONFIG_HOME'] != str(tmp_path / 'personal')
    assert env['XDG_CACHE_HOME'] != str(tmp_path / 'cache')
    assert env['OLLA_DFT_CONFIG_DIR'].startswith(env['XDG_CONFIG_HOME'])


def test_failed_samples_cannot_win():
    good = _rec('olla-dft', .1)
    bad = {**good, 'returncode': 1, 'correct': False}
    rs = [good] + [bad] * 14 + [_rec('ase', 1.)]
    s = report.aggregate(rs)
    d = s['t']['i']['olla-dft']
    assert d['n'] == 15 and d['failed'] == 14 and not all(d['correct'])
    assert report.ratios({'summary': s, 'records': rs}) == []


def test_failed_qe_and_each_repetition_checked():
    p = {'rc': 0, 'converged': True, 'job_done': True, 'total_energy_Ry': -22.,
         'scf_iterations': 8, 'nkpoints': 13, 'pw_wall_s': 1.}
    summary = report.e2e_rows({'olla-dft': {'samples': [p, {**p, 'rc': 1}]}})['olla-dft']
    assert summary['n'] == 1 and summary['failed'] == 1
    assert not validation.e2e_success({**p, 'converged': False})
    assert not validation.e2e_success({**p, 'total_energy_Ry': float('nan')})


def test_missing_band_edges_and_wrong_k_coordinates_fail():
    ref = {'gap_eV': 1., 'vbm_eV': 0., 'cbm_eV': 1.}
    assert not tasks.grade_bandgap({'gap_eV': 1.}, ref)[0]
    assert not tasks.grade_bandgap({'gap_eV': 1., 'vbm_eV': -999., 'cbm_eV': 999.}, ref)[0]
    path = {'convention': 'HPKOT', 'path': ['GAMMA-X'], 'point_coords': {'GAMMA': [0, 0, 0], 'X': [0, .5, 0]}}
    assert tasks.grade_kpath(path, path)[0]
    assert not tasks.grade_kpath({**path, 'point_coords': {'GAMMA': [0, 0, 0], 'X': [9, 9, 9]}}, path)[0]
    assert tasks.grade_kpath({**path, 'convention': 'other'}, path)[0] is None


def test_wrong_geometry_actual_parser(tmp_path):
    inp = (ROOT / 'review/invalid_kgrid/scf.in').read_text() if (ROOT / 'review/invalid_kgrid/scf.in').exists() else None
    if inp is None:
        inp = '''&CONTROL\n/\n&SYSTEM\nibrav=0, nat=2, ntyp=1, ecutwfc=30, ecutrho=240, occupations='fixed'\n/\nATOMIC_SPECIES\nSi 28.085 Si.UPF\nATOMIC_POSITIONS crystal\nSi 0 0 0\nSi .25 .25 .25\nCELL_PARAMETERS angstrom\n4 0 0\n0 4 0\n0 0 4\nK_POINTS automatic\n4 4 4 0 0 0\n'''
    inp = inp.replace('0 -2 4 0 0 0', '4 4 4 0 0 0')
    path = tmp_path / 'valid.in'; path.write_text(inp)
    def parse():
        r = subprocess.run([PY, str(ROOT / 'tools/reference.py'), 'roundtrip', str(path)], capture_output=True, text=True, check=True)
        return json.loads(r.stdout.split('@@RESULT ')[-1])
    ref = parse(); ref['kgrid_expected'] = [4, 4, 4]
    assert tasks.grade_inputgen({'roundtrip': ref}, ref)[0]
    path.write_text(inp.replace('0.2500000000', '0.0000000000').replace('Si .25 .25 .25', 'Si 0 0 0'))
    assert not tasks.grade_inputgen({'roundtrip': parse()}, ref)[0]
    for key, value in [('symbols', ['He', 'He']), ('ecutrho', -1), ('kshift', [1, 1, 1]), ('pseudopotentials', {})]:
        assert not tasks.grade_inputgen({'roundtrip': {**ref, key: value}}, ref)[0]


def test_empty_or_duplicate_run_is_incomplete():
    source = ROOT / 'results/20260903-153320/results.json'
    run = json.loads(source.read_text())
    run['records'] = []
    assert any('samples' in e for e in validation.check_run(run))
    run = json.loads(source.read_text())
    run['records'].append(copy.deepcopy(run['records'][0]))
    assert any('samples' in e for e in validation.check_run(run, strict=False))


@pytest.mark.parametrize('args', [['--reps', '0'], ['--e2e-reps', '-1'], ['--tasks', 'misspelled'], ['--tasks', 'eos', '--with-qe'], ['--opp-threshold', 'nan'], ['--opp-threshold', '-1']])
def test_invalid_run_arguments(args):
    r = subprocess.run([PY, str(ROOT / 'bench.py'), 'run', *args], capture_output=True, text=True)
    assert r.returncode != 0


def test_failed_cell_dashboard_does_not_crash():
    node = shutil.which('node')
    if not node:
        pytest.skip('Node is not installed')
    history = {'runs': [{'run_id': 'failure', 'timestamp': '', 'label': '</script><script>bad()</script>', 'cpu': '', 'warnings': [],
                         'summary': {'t': {'i': {'olla-dft': {'unsupported': False, 'wall': None, 'rss': None, 'correct': False}}}}}]}
    html = report.html(history)
    assert html.count('</script>') == 1
    script = html.split('<script>')[1].split('</script>')[0]
    stub = 'const element=()=>({appendChild(){},innerHTML:"",textContent:""});const document={getElementById:element,createElement:element};'
    r = subprocess.run([node, '-e', stub + script], text=True, capture_output=True)
    assert r.returncode == 0, r.stderr


def test_strict_run_rejects_qe_energy_outlier_and_missing_artifact():
    run = json.loads((ROOT / 'results/20260904-154049/results.json').read_text())
    assert validation.check_run(run) == []
    missing = copy.deepcopy(run)
    missing['artifacts_sha256'].pop(next(iter(missing['artifacts_sha256'])))
    assert any('artifacts' in e for e in validation.check_run(missing))
    run['config'].update(with_qe=True, e2e_reps=2)
    sample = {'rc': 0, 'converged': True, 'job_done': True, 'total_energy_Ry': -22., 'scf_iterations': 8}
    run['e2e'] = {tool: {'samples': [dict(sample), dict(sample)]} for tool in tasks.TASKS['inputgen']['tools']}
    for tool in run['e2e']:
        for rep in range(2):
            for suffix in ('pw.out', 'pw.stderr'):
                run['artifacts_sha256'][f'artifacts/qe/{tool}/rep-{rep}-{suffix}'] = 'test-only'
    assert validation.check_run(run) == []
    run['e2e']['olla-dft']['samples'][1]['total_energy_Ry'] = -21.
    assert any('energies disagree' in e for e in validation.check_run(run))


def test_environment_never_executes_qe_path_as_shell(tmp_path):
    marker = tmp_path / 'injected'
    env = dict(os.environ, BENCH_PW_X=f'/missing/pw.x; touch {marker}; true')
    r = subprocess.run([PY, str(ROOT / 'bench.py'), 'env'], env=env, text=True, capture_output=True)
    assert r.returncode == 0
    assert not marker.exists()
    assert json.loads(r.stdout)['pw_x'] == env['BENCH_PW_X']
