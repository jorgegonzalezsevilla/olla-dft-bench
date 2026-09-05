"""Read-only audit probes; outputs and synthetic inputs stay under review/.

Run with .venv/bin/python review/reproduce.py. These probes record the existing
behavior; they deliberately do not change benchmark or contestant code.
"""
import base64
import hashlib
import importlib.metadata as metadata
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from benchlib import measure, report, tasks  # noqa: E402

OUT = ROOT / "review"
PY = str(ROOT / ".venv/bin/python")
env = measure.clean_env()
evidence = {}


def run_cli(args):
    p = subprocess.run([PY, "-m", "qekit.cli", *args], cwd=ROOT,
                       env=env, text=True, capture_output=True, timeout=30)
    return {"rc": p.returncode, "stdout": p.stdout, "stderr": p.stderr}


d = metadata.distribution("olla-dft")
modified = []
for f in d.files:
    if str(f).endswith(".py") and f.hash:
        actual = base64.urlsafe_b64encode(hashlib.sha256(d.locate_file(f).read_bytes()).digest()).rstrip(b"=").decode()
        if actual != f.hash.value:
            modified.append(str(f))
evidence["installation"] = {"version": d.version, "source": json.loads(d.read_text("direct_url.json")),
                            "modified_python_files_against_RECORD": modified}

r = measure.run_measured([PY, "-c", "import time; time.sleep(0.25)"], env, str(ROOT), timeout=0.01)
evidence["timeout_ignored"] = {"requested_s": 0.01, "wall_s": r["wall_s"], "rc": r["returncode"]}

evidence["wrong_band_edges_pass"] = tasks.grade_bandgap(
    {"gap_eV": 1., "vbm_eV": -999., "cbm_eV": 999.},
    {"gap_eV": 1., "vbm_eV": 0., "cbm_eV": 1.})
evidence["wrong_structure_and_ecutrho_pass"] = tasks.grade_inputgen(
    {"roundtrip": {"natoms": 2, "volume_A3": 39.4, "kgrid": [4, 4, 4], "ecutwfc": 30.,
                   "ecutrho": -1., "symbols": ["He", "He"], "positions": [[0, 0, 0], [0, 0, 0]]}},
    {"natoms": 2, "volume_A3": 39.4, "kgrid_expected": [4, 4, 4]})
evidence["wrong_kpoint_coordinates_pass"] = tasks.grade_kpath(
    {"path": ["GAMMA-X"], "point_coords": {"X": [999, 999, 999]}},
    {"path": ["GAMMA-X"], "point_coords": {"X": [0, .5, 0]}})

def rec(tool, rc, wall):
    return {"task": "symmetry", "input": "Si_relajado.cif", "tool": tool,
            "rep": 0, "warmup": False, "wall_s": wall, "user_s": wall, "sys_s": 0,
            "max_rss_kb": 1000, "returncode": rc, "correct": rc == 0,
            "payload": {"via": "synthetic"}, "detail": "synthetic"}

records = [rec("olla-dft", 0, 1.)] + [rec("olla-dft", 1, .01) for _ in range(14)] + [rec("ase", 0, 2.)]
agg = report.aggregate(records)
evidence["fourteen_failures_hidden_from_correct"] = {
    "summary": agg["symmetry"]["Si_relajado.cif"]["olla-dft"],
    "ratios": report.ratios({"records": records, "summary": agg})}

evidence["failed_e2e_and_later_energy_ignored"] = report.e2e_rows({"olla-dft": {"samples": [
    {"total_energy_Ry": -22., "pw_wall_s": 1., "rc": 1, "scf_iterations": None},
    {"total_energy_Ry": 100., "pw_wall_s": 1., "rc": 0, "scf_iterations": 8}]}})

# An intentionally incomplete copy must never be confused with a measured run.
source = ROOT / "results/20260903-153320/results.json"
incomplete = json.loads(source.read_text())
incomplete["records"] = []
incomplete["summary"] = {}
incomplete["e2e"] = {}
target = OUT / "synthetic-incomplete-run"
target.mkdir(exist_ok=True)
(target / "results.json").write_text(json.dumps(incomplete))
(target / "report.md").write_text(report.markdown(incomplete))
p = subprocess.run([PY, str(ROOT / "bench.py"), "verify", str(target)],
                   capture_output=True, text=True, timeout=30)
evidence["verify_accepts_zero_records_with_15_reps_configured"] = {"rc": p.returncode, "stdout": p.stdout}

with_config = dict(os.environ, XDG_CONFIG_HOME=str(OUT / "synthetic-user-config"))
original_config = os.environ.get("XDG_CONFIG_HOME")
os.environ["XDG_CONFIG_HOME"] = with_config["XDG_CONFIG_HOME"]
evidence["config_is_not_isolated"] = {"user_config": with_config["XDG_CONFIG_HOME"],
                                       "clean_env_config": measure.clean_env()["XDG_CONFIG_HOME"]}
if original_config is None:
    del os.environ["XDG_CONFIG_HOME"]
else:
    os.environ["XDG_CONFIG_HOME"] = original_config

help_result = run_cli(["gen", "--help"])
evidence["explicit_kgrid_is_supported"] = {"rc": help_result["rc"], "found": "--kgrid" in help_result["stdout"]}
for name, flags in [
    ("invalid_kgrid", ["--kgrid", "0", "-2", "4", "--ecutwfc", "30", "--ecutrho", "240"]),
    ("negative_cutoffs", ["--kgrid", "4", "4", "4", "--ecutwfc", "-30", "--ecutrho", "-240"]),
]:
    folder = OUT / name
    result = run_cli(["gen", str(ROOT / "inputs/Si_relajado.cif"), "-p", "scf", "-o", str(folder),
                      "--pseudo-dir", str(ROOT / "inputs"), "--insulator", *flags])
    generated = folder / "scf.in"
    result["generated_input"] = generated.read_text() if generated.exists() else None
    evidence[name] = result

# Exercise the actual roundtrip parser on a geometrically wrong input.
bad_text = (OUT / "invalid_kgrid/scf.in").read_text().replace("0 -2 4 0 0 0", "4 4 4 0 0 0")
bad_text = re.sub(r"\bSi(?=\s)", "He", bad_text)
bad_text = bad_text.replace("0.2500000000", "0.0000000000")
bad_text = re.sub(r"ecutrho\s*=\s*240", "ecutrho = -1", bad_text)
bad_file = OUT / "wrong_geometry.in"
bad_file.write_text(bad_text)
parsed = subprocess.run([PY, str(ROOT / "tools/reference.py"), "roundtrip", str(bad_file)],
                        cwd=ROOT, env=env, capture_output=True, text=True, check=True, timeout=30)
rt = json.loads(parsed.stdout.strip().split("@@RESULT ")[-1])
evidence["wrong_geometry_actual_roundtrip"] = {
    "roundtrip": rt,
    "grade": tasks.grade_inputgen({"roundtrip": rt}, {
        "natoms": 2, "volume_A3": 39.401877693982705, "kgrid_expected": [4, 4, 4]})}

# Derive an occupied-only XML from the shipped Si output, without changing it.
tree = ET.parse(ROOT / "inputs/Si_scf.xml")
bs = tree.getroot().find("output/band_structure")
bs.find("nbnd").text = "4"
for node in bs.findall("ks_energies"):
    for tag in ("eigenvalues", "occupations"):
        entry = node.find(tag)
        entry.text = " ".join(entry.text.split()[:4])
        entry.set("size", "4")
low = bs.find("lowestUnoccupiedLevel")
if low is not None:
    bs.remove(low)
tree.getroot().find("input/bands/nbnd").text = "4"
xml_path = OUT / "Si_occupied_only.xml"
tree.write(xml_path)
evidence["occupied_only_gap_cli"] = run_cli(["gap", str(xml_path)])

# A non-converged copy tests whether the CLI discloses that existing flag.
tree = ET.parse(ROOT / "inputs/Si_scf.xml")
for node in tree.getroot().iter("convergence_achieved"):
    node.text = "false"
xml_path = OUT / "Si_unconverged.xml"
tree.write(xml_path)
evidence["unconverged_gap_cli"] = run_cli(["gap", str(xml_path)])

# Inspect the same fixtures in a child with the benchmark's clean environment.
check_code = """
import json, numpy as np
from qekit.modules import bands
from qekit.core import qeout
b = bands.load('review/Si_occupied_only.xml')
e = b.energies[0]; ref = b.result.fermi
cross = (e.min(axis=0) < ref-bands.CROSS_TOL) & (e.max(axis=0) > ref+bands.CROSS_TOL)
print(json.dumps({'occupied_only_details': {
    'nbnd': b.result.nbnd, 'nelec': b.result.nelec,
    'occupation_min': float(b.result.occupations.min()),
    'occupation_max': float(b.result.occupations.max()),
    'any_band_crosses_fermi': bool(np.any(cross)),
    'reported_is_metal': bands.analyze_gap(b).is_metal},
    'unconverged_parsed_flag': qeout.read_xml('review/Si_unconverged.xml').converged}))
"""
checked = subprocess.run([PY, "-c", check_code], cwd=ROOT, env=env,
                         capture_output=True, text=True, check=True, timeout=30)
evidence.update(json.loads(checked.stdout))

(OUT / "evidence.json").write_text(json.dumps(evidence, indent=2, ensure_ascii=False))
for key, value in evidence.items():
    if isinstance(value, dict) and "stdout" in value:
        print(key, json.dumps({"rc": value["rc"], "stdout": value["stdout"][-900:]}, ensure_ascii=False))
    else:
        print(key, json.dumps(value, ensure_ascii=False))
