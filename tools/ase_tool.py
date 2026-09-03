import sys, os
from _common import emit, unsupported, read_ev
task, args = sys.argv[1], sys.argv[2:]
from ase.io import read, write

if task == "symmetry":
    import spglib
    a = read(args[0])
    cell = (a.cell[:], a.get_scaled_positions(), a.numbers)
    ds = spglib.get_symmetry_dataset(cell, symprec=1e-4)
    prim = spglib.find_primitive(cell, symprec=1e-4)
    emit({"via": "ase.io.read + spglib.get_symmetry_dataset", "spacegroup": int(ds.number),
          "natoms_primitive": len(prim[2])})
elif task == "kpath":
    a = read(args[0])
    bp = a.cell.bandpath()   # ASE's own special-point tables (Setyawan-Curtarolo style)
    emit({"via": "ase Cell.bandpath()", "labels": sorted(set(bp.special_points)), "path": [bp.path]})
elif task == "eos":
    from ase.eos import EquationOfState
    from ase.units import kJ
    V, E = read_ev(args[0])
    eos = EquationOfState(V, E, eos="birchmurnaghan")
    v0, e0, B = eos.fit()
    emit({"via": "ase.eos.EquationOfState('birchmurnaghan')", "V0_A3": v0, "B0_GPa": B / kJ * 1.0e24,
          "Bp": None, "E0_eV": e0, "ok": True,
          "note": "ASE does not expose B' from fit(); reported as null"})
elif task == "bandgap":
    unsupported("ASE reads pw.x text output (espresso-out), not the data-file-schema XML")
elif task == "inputgen":
    cif, outdir, pseudo_dir = args[0], args[1], args[2]
    kpts = tuple(int(x) for x in args[3].split("x")) if len(args) > 3 else (4, 4, 4)
    a = read(cif)
    pseudos = {s: f for s in set(a.get_chemical_symbols())
               for f in os.listdir(pseudo_dir) if re.match(rf"{s}[._-]", f, re.I)}
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "scf.in")
    write(path, a, format="espresso-in", pseudopotentials=pseudos, kpts=kpts,
          input_data={"control": {"calculation": "scf", "pseudo_dir": pseudo_dir, "outdir": "./out",
                                  "tprnfor": True, "tstress": True},
                      "system": {"ecutwfc": 30, "ecutrho": 240, "occupations": "fixed"},
                      "electrons": {"conv_thr": 1e-8}})
    emit({"via": "ase.io.write(format='espresso-in')", "file": path, "rc": 0})
else:
    unsupported(f"task {task} not wired for ASE")
