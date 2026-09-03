import re
import sys, os, re, warnings
warnings.filterwarnings("ignore")
from _common import emit, unsupported, read_ev
task, args = sys.argv[1], sys.argv[2:]
from pymatgen.core import Structure

if task == "symmetry":
    from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
    s = Structure.from_file(args[0])
    sga = SpacegroupAnalyzer(s, symprec=1e-4)
    emit({"via": "pymatgen SpacegroupAnalyzer", "spacegroup": sga.get_space_group_number(),
          "natoms_primitive": len(sga.find_primitive())})
elif task == "kpath":
    from pymatgen.symmetry.bandstructure import HighSymmKpath
    from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
    s = Structure.from_file(args[0])
    prim = SpacegroupAnalyzer(s, symprec=1e-4).get_primitive_standard_structure()
    kp = HighSymmKpath(prim, path_type="setyawan_curtarolo")
    emit({"via": "pymatgen HighSymmKpath(setyawan_curtarolo)",
          "labels": sorted(set(kp.kpath["kpoints"])), "path": ["-".join(seg) for seg in kp.kpath["path"]]})
elif task == "eos":
    from pymatgen.analysis.eos import EOS
    V, E = read_ev(args[0])
    f = EOS(eos_name="birch_murnaghan").fit(V, E)
    emit({"via": "pymatgen.analysis.eos.EOS('birch_murnaghan')", "V0_A3": float(f.v0),
          "B0_GPa": float(f.b0_GPa), "Bp": float(f.b1), "E0_eV": float(f.e0), "ok": True})
elif task == "bandgap":
    unsupported("pymatgen has no parser for the pw.x data-file-schema XML")
elif task == "inputgen":
    from pymatgen.io.pwscf import PWInput
    cif, outdir, pseudo_dir = args[0], args[1], args[2]
    kpts = [int(x) for x in args[3].split("x")] if len(args) > 3 else [4, 4, 4]
    s = Structure.from_file(cif)
    pseudos = {sp.symbol: f for sp in s.composition for f in os.listdir(pseudo_dir)
               if re.match(rf"{sp.symbol}[._-]", f, re.I)}
    pw = PWInput(s, pseudo=pseudos,
                 control={"calculation": "scf", "pseudo_dir": pseudo_dir, "outdir": "./out",
                          "tprnfor": True, "tstress": True},
                 system={"ecutwfc": 30, "ecutrho": 240, "occupations": "fixed"},
                 electrons={"conv_thr": 1e-8}, kpoints_grid=kpts)
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "scf.in")
    pw.write_file(path)
    emit({"via": "pymatgen.io.pwscf.PWInput", "file": path, "rc": 0})
else:
    unsupported(f"task {task} not wired for pymatgen")
