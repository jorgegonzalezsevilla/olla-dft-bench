"""Olla-DFT wrapper. Uses the command-line entry point in-process (what a user runs) and,
where no command consumes the benchmark input directly (E-V table), the public function
behind the command. Every such choice is stated in the payload as 'via'."""
import sys, io, re, os, contextlib, tempfile, shutil
from _common import emit, unsupported, read_ev

task, args = sys.argv[1], sys.argv[2:]

def cli(argv):
    from qekit.cli import main
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            rc = main(["--language", "en"] + argv)
        except SystemExit as e:
            rc = e.code
    return rc, buf.getvalue()

if task == "symmetry":
    rc, out = cli(["info", args[0]])
    m = re.search(r"\(N\S*\s*(\d+)\)", out)
    n = re.search(r"celda primitiva:\s*(\d+)|primitive cell:\s*(\d+)", out)
    emit({"via": "cli info", "spacegroup": int(m.group(1)) if m else None,
          "natoms_primitive": int([g for g in n.groups() if g][0]) if n else None, "rc": rc})
elif task == "kpath":
    rc, out = cli(["kpath", args[0]])
    labels = re.findall(r"^\s{2}(\S+)\s+-?\d\.\d{6}\s+-?\d\.\d{6}\s+-?\d\.\d{6}", out, re.M)
    path = re.findall(r"^\s{2}(\S+(?:\s+—\s+\S+)+)\s*$", out, re.M)
    emit({"via": "cli kpath", "labels": sorted(set(labels)), "path": [p.replace(" — ", "-") for p in path], "rc": rc})
elif task == "eos":
    from qekit.modules.eos import EOSRun, fit
    V, E = read_ev(args[0])
    run = EOSRun(volumes=V, energies=E, natoms=2)
    f = fit(run, "birch-murnaghan")
    emit({"via": "qekit.modules.eos.fit (function behind `olla-dft eos`)",
          "V0_A3": f.V0, "B0_GPa": f.B0, "Bp": f.Bp, "E0_eV": f.E0, "ok": f.ok})
elif task == "bandgap":
    if args[0].endswith(".out"):
        unsupported("`olla-dft gap` reads the data-file-schema XML, not the pw.x text output")
    d = tempfile.mkdtemp(prefix="ollad_gap_")
    import gzip
    if args[0].endswith(".gz"):
        with gzip.open(args[0], "rb") as f, open(os.path.join(d, "Si.xml"), "wb") as g:
            shutil.copyfileobj(f, g)
    else:
        shutil.copy(args[0], os.path.join(d, "Si.xml"))
    rc, out = cli(["gap", d])
    shutil.rmtree(d, ignore_errors=True)
    def grab(pat):
        m = re.search(pat, out); return float(m.group(1)) if m else None
    emit({"via": "cli gap", "gap_eV": grab(r"[Gg]ap[^\n]*?(-?\d+\.\d+)\s*eV"),
          "vbm_eV": grab(r"VBM[^\n]*?(-?\d+\.\d+)"), "cbm_eV": grab(r"CBM[^\n]*?(-?\d+\.\d+)"),
          "rc": rc, "raw": out[:600]})
elif task == "inputgen":
    cif, outdir, pseudo_dir = args[0], args[1], args[2]
    want = args[3]
    # the --kspacing that reproduces the requested grid is computed once, untimed, by the harness
    # (tools/reference.py kspacing) because olla-dft has no explicit k-grid option; it arrives as args[4]
    ks = float(args[4]) if len(args) > 4 else None
    if ks is None:
        unsupported("no --kspacing supplied for the requested grid (olla-dft has no explicit k-grid option)")
    rc, out = cli(["gen", cif, "-p", "scf", "-o", outdir, "--pseudo-dir", pseudo_dir,
                   "--kspacing", f"{ks:.6f}", "--ecutwfc", "30", "--ecutrho", "240", "--insulator"])
    emit({"via": f"cli gen -p scf --kspacing {ks:.4f} --ecutwfc 30 --ecutrho 240 --insulator (no explicit k-grid option; spacing precomputed untimed by the harness)",
          "file": os.path.join(outdir, "scf.in"), "rc": rc})
else:
    unsupported(f"task {task} not wired for olla-dft")
