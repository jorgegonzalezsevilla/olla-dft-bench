"""Run one tool wrapper in a fresh process and measure wall time, CPU time and peak RSS.

Every measurement is a separate subprocess so that import cost is included (that is what a
user pays on the command line) and so that one tool cannot warm caches for another.
"""
import json, os, shutil, subprocess, time, tempfile

CLEAN_ENV_KEYS = ("PATH", "HOME", "LANG", "TERM", "USER", "XDG_CONFIG_HOME", "XDG_CACHE_HOME",
                  "DBUS_SESSION_BUS_ADDRESS", "XDG_RUNTIME_DIR", "BENCH_PW_X")  # last two: systemd-run needs the session bus


def clean_env(threads=1):
    env = {k: os.environ[k] for k in CLEAN_ENV_KEYS if k in os.environ}
    private = tempfile.mkdtemp(prefix="olla-bench-env-")
    env.update({
        "OMP_NUM_THREADS": str(threads), "OPENBLAS_NUM_THREADS": str(threads),
        "MKL_NUM_THREADS": str(threads), "NUMEXPR_NUM_THREADS": str(threads),
        "MPLBACKEND": "Agg", "PYTHONHASHSEED": "0", "LC_ALL": "C.UTF-8",
        "PYTHONIOENCODING": "utf-8", "OLLA_DFT_LANG": "en",
        # keep the toolkit from touching the real user configuration
        "XDG_CONFIG_HOME": os.path.join(private, "config"),
        "XDG_CACHE_HOME": os.path.join(private, "cache"),
        "OLLA_DFT_CONFIG_DIR": os.path.join(private, "config", "olla-dft"),
        "OLLA_DFT_DATA_DIR": os.path.join(private, "data"),
        "MPLCONFIGDIR": os.path.join(private, "cache", "matplotlib"),
    })
    os.makedirs(env["XDG_CONFIG_HOME"], exist_ok=True)
    os.makedirs(env["XDG_CACHE_HOME"], exist_ok=True)
    return env


def wrap_isolation(cmd, cpu=None, mem_max=None, cpu_quota=None):
    """Pin to one CPU and, when available, put the process in a transient systemd scope
    with memory and CPU limits. A systemd scope error fails the sample."""
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
    """Measure the process tree, enforcing timeout and killing descendants."""
    import signal
    if timeout <= 0:
        raise ValueError("timeout must be positive")
    t0 = time.perf_counter()
    timed_out = False
    with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
        p = subprocess.Popen(cmd, env=env, cwd=cwd, stdout=stdout, stderr=stderr,
                             start_new_session=True)
        try:
            while True:
                pid, status, ru = os.wait4(p.pid, os.WNOHANG)
                if pid:
                    break
                if time.perf_counter() - t0 >= timeout:
                    timed_out = True
                    os.killpg(p.pid, signal.SIGKILL)
                    _, status, ru = os.wait4(p.pid, 0)
                    break
                time.sleep(0.01)
        except BaseException:
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            p.wait()
            raise
        p.returncode = os.waitstatus_to_exitcode(status)
        wall = time.perf_counter() - t0
        def tail(stream, limit):
            stream.seek(0, 2)
            stream.seek(max(0, stream.tell() - limit))
            return stream.read().decode("utf-8", "replace")
        out, err = tail(stdout, 1048576), tail(stderr, 4000)
    res = {"wall_s": wall, "returncode": p.returncode, "timed_out": timed_out,
           "user_s": ru.ru_utime, "sys_s": ru.ru_stime, "max_rss_kb": ru.ru_maxrss,
           "stdout": out, "stderr": err + ("\nmeasurement timeout" if timed_out else "")}
    res["payload"] = None
    for line in reversed(out.splitlines()):
        if line.startswith("@@RESULT "):
            try:
                payload = json.loads(line[len("@@RESULT "):])
                if isinstance(payload, dict):
                    res["payload"] = payload
            except json.JSONDecodeError:
                pass
            break
    return res
