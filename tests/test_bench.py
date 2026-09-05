"""Unit tests for the harness: grading, aggregation, references and the verify contract."""
import json, subprocess, sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from benchlib import report, tasks, envinfo  # noqa: E402

PY = str(ROOT / ".venv" / "bin" / "python") if (ROOT / ".venv").exists() else sys.executable


def test_label_normalisation_and_segments():
    assert tasks.norm_label("GAMMA") == tasks.norm_label("\\Gamma") == tasks.norm_label("G") == "Γ"
    a = tasks.path_segments(["GAMMA-M", "M-K", "K-GAMMA"])
    b = tasks.path_segments(["\\Gamma-M-K-\\Gamma"])
    c = tasks.path_segments(["GMKG"])            # ASE compact notation
    assert a == b == c and len(a) == 3


def test_grades_are_symmetric_and_tolerant():
    ref = {"V0_A3": 39.4018722, "B0_GPa": 94.20838, "Bp": 4.2}
    ok, _ = tasks.grade_eos({"V0_A3": 39.40187, "B0_GPa": 94.2085, "Bp": None}, ref)
    assert ok
    bad, detail = tasks.grade_eos({"V0_A3": 39.5, "B0_GPa": 94.2, "Bp": 4.0}, ref)
    assert not bad and "ΔV0" in detail
    assert tasks.grade_bandgap({"gap_eV": 0.6155, "vbm_eV": 0., "cbm_eV": .6155}, {"gap_eV": 0.61554, "vbm_eV": 0., "cbm_eV": .61554})[0]
    assert not tasks.grade_bandgap({"gap_eV": 0.62}, {"gap_eV": 0.61554})[0]
    r = {"natoms": 1, "volume_A3": 1., "kgrid_expected": [4, 4, 4],
         "symbols": ["Si"], "cell": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
         "scaled_positions": [[0, 0, 0]], "pseudopotentials": {"Si": "Si.UPF"}}
    rt = {**r, "kgrid": [4, 4, 4], "kshift": [0, 0, 0], "ecutwfc": 30., "ecutrho": 240., "occupations": "fixed"}
    assert tasks.grade_inputgen({"roundtrip": rt}, r)[0]
    assert not tasks.grade_inputgen({"roundtrip": {**rt, "symbols": ["He"]}}, r)[0]


def _rec(tool, wall, rss=1000, ok=True, unsupported=False, warm=False):
    return {"task": "t", "input": "i", "tool": tool, "rep": 0, "warmup": warm, "wall_s": wall, "user_s": wall, "sys_s": 0.0,
            "max_rss_kb": rss, "returncode": 0, "correct": ok, "unsupported": unsupported, "payload": {"via": "x"}}


def test_aggregate_excludes_warmup_and_unsupported_from_ratios():
    recs = [_rec("olla-dft", 9.0, warm=True)] + [_rec("olla-dft", w) for w in (1.0, 1.2, 1.1)] \
        + [_rec("ase", w) for w in (0.5, 0.6, 0.55)] + [_rec("pymatgen", 0.01, unsupported=True)]
    summ = report.aggregate(recs)["t"]["i"]
    assert summ["olla-dft"]["wall_s"]["n"] == 3 and summ["olla-dft"]["wall_s"]["median"] == 1.1
    assert summ["pymatgen"]["unsupported"]
    run = {"summary": {"t": {"i": summ}}, "records": recs}
    rows = report.ratios(run)
    assert len(rows) == 1 and rows[0]["vs"] == "ase" and abs(rows[0]["wall_ratio"] - 2.0) < 1e-9
    lo, hi = rows[0]["ci"]
    assert lo <= 2.0 <= hi


def test_bootstrap_is_deterministic():
    a, b = [1.0, 1.1, 1.2, 1.3], [0.5, 0.55, 0.6, 0.65]
    assert report.boot_ratio(a, b) == report.boot_ratio(a, b)


def test_reference_eos_is_analytic_and_close_to_curve_fit():
    out = subprocess.run([PY, str(ROOT / "tools" / "reference.py"), "eos", str(ROOT / "inputs" / "EOS.dat")],
                         capture_output=True, text=True, check=True).stdout
    p = json.loads(out.strip().splitlines()[-1][len("@@RESULT "):])
    assert abs(p["V0_A3"] - 39.40187) < 1e-4 and abs(p["B0_GPa"] - 94.2084) < 1e-3
    assert "no optimiser" in p["via"]


def test_inputs_manifest_matches_files():
    sums = dict(line.split()[::-1] for line in (ROOT / "inputs" / "SHA256SUMS").read_text().splitlines())
    for name, h in sums.items():
        assert envinfo.sha256(ROOT / "inputs" / name) == h, name


@pytest.mark.parametrize("run_dir", sorted(p for p in (ROOT / "results").glob("2*") if (p / "results.json").exists()))
def test_published_runs_verify(run_dir):
    r = subprocess.run([PY, str(ROOT / "bench.py"), "verify", str(run_dir)], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
