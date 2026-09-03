"""Environment fingerprint: everything that could plausibly change a number."""
import hashlib, json, os, platform, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _read(p):
    try:
        return Path(p).read_text().strip()
    except OSError:
        return None


def _cmd(*args):
    try:
        return subprocess.run(args, capture_output=True, text=True, timeout=20).stdout.strip()
    except Exception:
        return None


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def cpu_topology():
    """List of (cpu, core, max_mhz) so we can pin to the fastest cores."""
    rows = []
    out = _cmd("lscpu", "-p=CPU,CORE,MAXMHZ") or ""
    for line in out.splitlines():
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split(",")
        try:
            rows.append((int(parts[0]), int(parts[1]), float(parts[2] or 0)))
        except ValueError:
            pass
    return rows


def fastest_cpu():
    rows = cpu_topology()
    if not rows:
        return 0
    rows.sort(key=lambda r: (-r[2], r[0]))
    return rows[0][0]


def package_versions(python):
    code = ("import json,importlib.metadata as m;"
            "print(json.dumps({d.metadata['Name']:d.version for d in m.distributions()}))")
    out = _cmd(python, "-c", code)
    try:
        return json.loads(out)
    except Exception:
        return {}


def git_sha(path):
    return _cmd("git", "-C", str(path), "rev-parse", "HEAD")


def load_avg():
    try:
        return list(os.getloadavg())
    except OSError:
        return None


def collect(python=sys.executable, input_files=()):
    model = None
    for line in (_read("/proc/cpuinfo") or "").splitlines():
        if line.startswith("model name"):
            model = line.split(":", 1)[1].strip()
            break
    mem_kb = None
    for line in (_read("/proc/meminfo") or "").splitlines():
        if line.startswith("MemTotal"):
            mem_kb = int(line.split()[1])
    pkgs = package_versions(python)
    keep = {k: v for k, v in pkgs.items() if k.lower() in
            {"olla-dft", "ase", "pymatgen", "spglib", "seekpath", "numpy", "scipy", "matplotlib"}}
    return {
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "hostname_hash": hashlib.sha256(platform.node().encode()).hexdigest()[:12],
        "os": platform.platform(),
        "kernel": platform.release(),
        "cpu_model": model,
        "cpu_count": os.cpu_count(),
        "cpu_topology": cpu_topology(),
        "mem_total_kb": mem_kb,
        "governor": _read("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"),
        "intel_no_turbo": _read("/sys/devices/system/cpu/intel_pstate/no_turbo"),
        "load_avg_start": load_avg(),
        "python": _cmd(python, "--version"),
        "python_path": python,
        "packages": keep,
        "pw_x": os.environ.get("BENCH_PW_X") or _cmd("bash", "-c", "command -v pw.x"),
        "pw_x_version": (_cmd("bash", "-c", f"echo | {os.environ.get('BENCH_PW_X', 'pw.x')} 2>/dev/null | grep -m1 'Program PWSCF'") or "").strip(),
        "bench_git_sha": git_sha(ROOT),
        "inputs_sha256": {str(Path(p).relative_to(ROOT)) if str(p).startswith(str(ROOT)) else str(p): sha256(p)
                          for p in input_files},
    }


def warnings(env):
    w = []
    if env.get("governor") not in (None, "performance"):
        w.append(f"CPU governor is '{env['governor']}', not 'performance': timings are noisier. "
                 "Fix: sudo cpupower frequency-set -g performance")
    if env.get("intel_no_turbo") == "0":
        w.append("Turbo boost enabled: single-thread timings drift with temperature. "
                 "Fix: echo 1 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo")
    la = env.get("load_avg_start") or [0]
    if la[0] > 1.0:
        w.append(f"1-min load average {la[0]:.2f} > 1.0: other processes were competing for CPU.")
    return w
