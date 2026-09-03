"""Run pw.x on a generated input and report total energy, SCF iterations and wall time.
Used by the optional end-to-end stage. pw.x itself is the same binary for every tool, so the
only thing that can differ is the input each tool produced."""
import sys, re, subprocess, time, os
from _common import emit
inp, cwd = sys.argv[1], sys.argv[2]
env = dict(os.environ, OMP_NUM_THREADS="1")
t0 = time.perf_counter()
p = subprocess.run([os.environ.get("BENCH_PW_X", "pw.x"), "-in", os.path.basename(inp)], cwd=cwd, capture_output=True, text=True, env=env, timeout=1800)
wall = time.perf_counter() - t0
out = p.stdout
e = re.search(r"!\s+total energy\s+=\s+(-?[\d.]+)\s+Ry", out)
it = re.search(r"convergence has been achieved in\s+(\d+) iterations", out)
kp = re.search(r"number of k points=\s*(\d+)", out)
emit({"total_energy_Ry": float(e.group(1)) if e else None, "scf_iterations": int(it.group(1)) if it else None,
      "nkpoints": int(kp.group(1)) if kp else None, "pw_wall_s": wall, "rc": p.returncode,
      "tail": (out[-600:] + "\nSTDERR: " + p.stderr[-600:]) if not e else ""})
