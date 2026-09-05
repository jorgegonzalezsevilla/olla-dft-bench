"""Run pw.x on a generated input and report total energy, SCF iterations and wall time.
Used by the optional end-to-end stage. pw.x itself is the same binary for every tool, so the
only thing that can differ is the input each tool produced."""
import sys, re, subprocess, time, os
from _common import emit
from pathlib import Path
inp, cwd = sys.argv[1], sys.argv[2]
env = dict(os.environ, OMP_NUM_THREADS="1")
t0 = time.perf_counter()
with (Path(cwd) / "pw.out").open("w") as stdout, (Path(cwd) / "pw.stderr").open("w") as stderr:
    p = subprocess.run([os.environ.get("BENCH_PW_X", "pw.x"), "-in", os.path.basename(inp)],
                       cwd=cwd, stdout=stdout, stderr=stderr, text=True, env=env, timeout=1800)
wall = time.perf_counter() - t0
out = (Path(cwd) / "pw.out").read_text(errors="replace")
err = (Path(cwd) / "pw.stderr").read_text(errors="replace")
energies = re.findall(r"!\s+total energy\s+=\s+(-?[\d.]+)\s+Ry", out)
e = energies[-1] if energies else None
it = re.search(r"convergence has been achieved in\s+(\d+) iterations", out)
kp = re.search(r"number of k points=\s*(\d+)", out)
emit({"total_energy_Ry": float(e) if e else None, "scf_iterations": int(it.group(1)) if it else None,
      "converged": bool(it), "job_done": "JOB DONE." in out,
      "nkpoints": int(kp.group(1)) if kp else None, "pw_wall_s": wall, "rc": p.returncode,
      "tail": (out[-600:] + "\nSTDERR: " + err[-600:]) if not e else ""})

sys.exit(0 if p.returncode == 0 and e and it and "JOB DONE." in out else 1)
