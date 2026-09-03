"""Run one tool wrapper in a fresh process and measure wall time, CPU time and peak RSS.

Every measurement is a separate subprocess so that import cost is included (that is what a
user pays on the command line) and so that one tool cannot warm caches for another.
"""
import json, os, shutil, subprocess, time

CLEAN_ENV_KEYS = ("PATH", "HOME", "LANG", "TERM", "USER", "XDG_CONFIG_HOME", "XDG_CACHE_HOME",
                  "DBUS_SESSION_BUS_ADDRESS", "XDG_RUNTIME_DIR", "BENCH_PW_X")  # last two: systemd-run needs the session bus


def clean_env(threads=1):
    env = {k: os.environ[k] for k in CLEAN_ENV_KEYS if k in os.environ}
    env.update({
        "OMP_NUM_THREADS": str(threads), "OPENBLAS_NUM_THREADS": str(threads),
        "MKL_NUM_THREADS": str(threads), "NUMEXPR_NUM_THREADS": str(threads),
        "MPLBACKEND": "Agg", "PYTHONHASHSEED": "0", "LC_ALL": "C.UTF-8",
        "PYTHONIOENCODING": "utf-8", "OLLA_DFT_LANG": "en",
        # keep the toolkit from touching the real user configuration
        "XDG_CONFIG_HOME": env.get("XDG_CONFIG_HOME", os.path.join(os.getcwd(), ".bench_home", "config")),
        "XDG_CACHE_HOME": env.get("XDG_CACHE_HOME", os.path.join(os.getcwd(), ".bench_home", "cache")),
    })
    os.makedirs(env["XDG_CONFIG_HOME"], exist_ok=True)
    os.makedirs(env["XDG_CACHE_HOME"], exist_ok=True)
    return env


def wrap_isolation(cmd, cpu=None, mem_max=None, cpu_quota=None):
    """Pin to one CPU and, when available, put the process in a transient systemd scope
    with memory and CPU limits. Falls back silently to plain taskset."""
    if cpu is not None and shutil.which("taskset"):
        cmd = ["taskset", "-c", str(cpu)] + cmd
    if (mem_max or cpu_quota) and shutil.which("systemd-run"):
        props = []
        if mem_max:
            props += ["-p", f"MemoryMax={mem_max}"]
        if cpu_quota:
            props += ["-p", f"CPUQuota={cpu_quota}"]
        cmd = ["systemd-run", "--user", "--scope", "-q", "--collect"] + props + cmd
    return cmd


def run_measured(cmd, env, cwd, timeout=600):
    """Like run_once but with per-child rusage (user/sys CPU and peak RSS) via os.wait4."""
    t0 = time.perf_counter()
    p = subprocess.Popen(cmd, env=env, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out_chunks, err_chunks = [], []
    import threading
    def drain(stream, sink):
        for chunk in iter(lambda: stream.read(65536), b""):
            sink.append(chunk)
    to = threading.Thread(target=drain, args=(p.stdout, out_chunks))
    te = threading.Thread(target=drain, args=(p.stderr, err_chunks))
    to.start(); te.start()
    try:
        _, status, ru = os.wait4(p.pid, 0)
    except ChildProcessError:
        status, ru = p.wait(), None
    wall = time.perf_counter() - t0
    to.join(); te.join()
    p.returncode = os.waitstatus_to_exitcode(status) if isinstance(status, int) else status
    res = {"wall_s": wall, "returncode": p.returncode,
           "user_s": ru.ru_utime if ru else None, "sys_s": ru.ru_stime if ru else None,
           "max_rss_kb": ru.ru_maxrss if ru else None,
           "stdout": b"".join(out_chunks).decode("utf-8", "replace"),
           "stderr": b"".join(err_chunks).decode("utf-8", "replace")[-4000:]}
    payload = None
    for line in reversed(res["stdout"].splitlines()):
        if line.startswith("@@RESULT "):
            try:
                payload = json.loads(line[len("@@RESULT "):])
            except json.JSONDecodeError:
                pass
            break
    res["payload"] = payload
    return res
