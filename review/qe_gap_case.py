"""Real, converged SCF -> gap regression, retaining QE input/output/XML.

Run after the timed benchmark, where local MPI sockets are allowed:
    .venv/bin/python review/qe_gap_case.py
"""
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from benchlib.measure import clean_env  # noqa: E402

env = clean_env()
py = str(ROOT / ".venv/bin/python")
folder = ROOT / "review/qe-default-scf"
folder.mkdir(exist_ok=True)
gen = subprocess.run([
    py, "-m", "qekit.cli", "gen", str(ROOT / "inputs/Si_relajado.cif"),
    "-p", "scf", "-o", str(folder), "--pseudo-dir", str(ROOT / "inputs"),
    "--kgrid", "4", "4", "4", "--ecutwfc", "30", "--ecutrho", "240", "--insulator",
], cwd=ROOT, env=env, capture_output=True, text=True, timeout=60)
(folder / "generation.log").write_text(gen.stdout + gen.stderr)
gen.check_returncode()
qe = subprocess.run([str(ROOT / ".qe/bin/pw.x"), "-in", "scf.in"],
                    cwd=folder, env=env, capture_output=True, text=True, timeout=120)
(folder / "pw.out").write_text(qe.stdout)
(folder / "pw.stderr").write_text(qe.stderr)
qe.check_returncode()
assert "convergence has been achieved" in qe.stdout and "JOB DONE." in qe.stdout
gap = subprocess.run([py, "-m", "qekit.cli", "gap", str(folder)],
                     cwd=ROOT, env=env, capture_output=True, text=True, timeout=60)
(folder / "gap.log").write_text(gap.stdout + gap.stderr)
e = re.search(r"!\s+total energy\s+=\s+(-?[\d.]+)", qe.stdout)
result = {"generation_rc": gen.returncode, "qe_rc": qe.returncode,
          "qe_converged": True, "qe_job_done": True,
          "total_energy_Ry": float(e.group(1)) if e else None,
          "gap_rc": gap.returncode, "gap_stdout": gap.stdout,
          "gap_stderr": gap.stderr}
(folder / "evidence.json").write_text(json.dumps(result, indent=2, ensure_ascii=False))
print(json.dumps(result, indent=2, ensure_ascii=False))
