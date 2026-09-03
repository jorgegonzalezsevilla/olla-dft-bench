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
    # the CLI wants a folder with the .xml (uncompressed) inside
    d = tempfile.mkdtemp(prefix="ollad_gap_")
    import gzip
    with gzip.open(args[0], "rb") as f, open(os.path.join(d, "Si.xml"), "wb") as g:
        shutil.copyfileobj(f, g)
    rc, out = cli(["gap", d])
    shutil.rmtree(d, ignore_errors=True)
    def grab(pat):
        m = re.search(pat, out); return float(m.group(1)) if m else None
    emit({"via": "cli gap", "gap_eV": grab(r"[Gg]ap[^\n]*?(-?\d+\.\d+)\s*eV"),
          "vbm_eV": grab(r"VBM[^\n]*?(-?\d+\.\d+)"), "cbm_eV": grab(r"CBM[^\n]*?(-?\d+\.\d+)"),
          "rc": rc, "raw": out[:600]})
elif task == "inputgen":
    cif, outdir, pseudo_dir = args[0], args[1], args[2]
    want = tuple(int(x) for x in args[3].split("x")) if len(args) > 3 else (4, 4, 4)
    # olla-dft has no explicit k-grid option: find the --kspacing that yields the requested grid
    from qekit.core.structure import load
    from qekit.core.kpoints import kgrid_from_spacing
    atoms = load(cif); lo, hi = 0.05, 1.0; ks = None
    for _ in range(40):
        mid = 0.5 * (lo + hi); g = tuple(kgrid_from_spacing(atoms, mid))
        if g == want: ks = mid; break
        if g < want: hi = mid
        else: lo = mid
    if ks is None:
        unsupported(f"no --kspacing reproduces grid {want} (bisection failed)")
    rc, out = cli(["gen", cif, "-p", "scf", "-o", outdir, "--pseudo-dir", pseudo_dir,
                   "--kspacing", f"{ks:.6f}", "--ecutwfc", "30", "--ecutrho", "240", "--insulator"])
    emit({"via": f"cli gen -p scf --kspacing {ks:.4f} --ecutwfc 30 --ecutrho 240 --insulator (no explicit k-grid option)",
          "file": os.path.join(outdir, "scf.in"), "rc": rc})
else:
    unsupported(f"task {task} not wired for olla-dft")
