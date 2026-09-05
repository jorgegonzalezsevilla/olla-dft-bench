"""Independent reference implementations written for this benchmark. They share no code with
Olla-DFT and are deliberately minimal: they define 'the right answer' for each task, so that
correctness is not judged by any of the contestants. They are not timed."""
import sys, re
import numpy as np
from _common import emit, unsupported, read_ev, open_xml, HA_EV
task, args = sys.argv[1], sys.argv[2:]

if task == "symmetry":
    import spglib
    from ase.io import read
    a = read(args[0])
    cell = (a.cell[:], a.get_scaled_positions(), a.numbers)
    ds = spglib.get_symmetry_dataset(cell, symprec=1e-4)
    emit({"via": "spglib direct", "spacegroup": int(ds.number),
          "natoms_primitive": len(spglib.find_primitive(cell, symprec=1e-4)[2])})
elif task == "kpath":
    import seekpath
    from ase.io import read
    a = read(args[0])
    r = seekpath.get_path((a.cell[:], a.get_scaled_positions(), a.numbers), symprec=1e-4)
    emit({"via": "seekpath direct (HPKOT convention)", "convention": "HPKOT", "point_coords": r["point_coords"], "labels": sorted(set(r["point_coords"])),
          "path": ["-".join(seg) for seg in r["path"]]})
elif task == "eos":
    # Third-order Birch-Murnaghan is a cubic polynomial in x = V^(-2/3): E = a + b x + c x^2 + d x^3.
    # Linear least squares (closed form, no iterative optimiser, no seed) then V0 and B0 analytically.
    V, E = map(np.array, read_ev(args[0]))
    x = V ** (-2.0 / 3.0)
    a, b, c, d = np.linalg.lstsq(np.vander(x, 4, increasing=True), E, rcond=None)[0]
    roots = np.roots([3 * d, 2 * c, b])                    # dE/dx = 0
    x0 = float(min((r.real for r in roots if abs(r.imag) < 1e-12 and r.real > 0), key=lambda r: abs(r - x.mean())))
    V0 = x0 ** (-1.5)
    d2E_dx2 = 2 * c + 6 * d * x0
    dx_dV = -(2.0 / 3.0) * V0 ** (-5.0 / 3.0)
    B0 = V0 * d2E_dx2 * dx_dV ** 2                          # eV/Å^3 (dE/dx = 0 at the minimum)
    emit({"via": "linear least squares of E as cubic in V^(-2/3), V0/B0 analytic (no shared code, no optimiser)",
          "V0_A3": float(V0), "B0_GPa": float(B0 * 160.21766208), "Bp": None,
          "E0_eV": float(a + b * x0 + c * x0 ** 2 + d * x0 ** 3)})
elif task == "bandgap":
    if args[0].endswith(".out"):
        txt = open(args[0]).read()
        m = re.search(r"highest occupied, lowest unoccupied level \(ev\):\s*(-?[\d.]+)\s+(-?[\d.]+)", txt)
        if not m:
            unsupported("text output has no 'highest occupied, lowest unoccupied level' line")
        vbm, cbm = float(m.group(1)), float(m.group(2))
        emit({"via": "pw.x's own 'highest occupied, lowest unoccupied level' line", "gap_eV": cbm - vbm, "vbm_eV": vbm, "cbm_eV": cbm})
    else:
        import xml.etree.ElementTree as ET
        root = ET.parse(open_xml(args[0])).getroot()
        bs = root.find("output").find("band_structure")
        nelec = float(bs.find("nelec").text); lsda = bs.find("lsda").text.strip() == "true"
        eigs = np.array([[float(x) for x in ks.find("eigenvalues").text.split()] for ks in bs.findall("ks_energies")]) * HA_EV
        if lsda:
            unsupported("reference gap for lsda not implemented")
        nv = int(round(nelec / 2))
        vbm, cbm = eigs[:, nv - 1].max(), eigs[:, nv].min()
        emit({"via": "ElementTree parse of data-file-schema; VBM=max band nelec/2, CBM=min band nelec/2+1",
              "gap_eV": float(cbm - vbm), "vbm_eV": float(vbm), "cbm_eV": float(cbm)})
elif task == "inputgen":
    from ase.io import read
    from pathlib import Path
    a = read(args[0])
    pp = {s: f.name for s in set(a.get_chemical_symbols()) for f in Path(args[0]).parent.glob("*.UPF")
          if re.match(rf"{s}[._-]", f.name, re.I)}
    emit({"via": "source structure and prescribed parameters", "natoms": len(a),
          "volume_A3": float(a.get_volume()), "symbols": a.get_chemical_symbols(),
          "cell": a.cell.array.tolist(), "scaled_positions": a.get_scaled_positions().tolist(),
          "pseudopotentials": pp})
elif task == "roundtrip":
    from ase.io import read
    from ase.io.espresso import read_fortran_namelist
    a = read(args[0], format="espresso-in")
    with open(args[0]) as f:
        namelists, cards = read_fortran_namelist(f)
    system = namelists.get("system", {})
    txt = open(args[0]).read()
    k = re.search(r"K_POINTS\s+automatic\s*\n\s*((?:[+-]?\d+\s+){5}[+-]?\d+)", txt, re.I)
    grid = [int(x) for x in k.group(1).split()] if k else []
    start = next(i for i, line in enumerate(cards) if line.upper().startswith("ATOMIC_SPECIES")) + 1
    pp = {line.split()[0]: line.split()[2] for line in cards[start:start + int(system["ntyp"])]}
    emit({"natoms": len(a), "volume_A3": float(a.get_volume()),
          "symbols": a.get_chemical_symbols(), "cell": a.cell.array.tolist(),
          "scaled_positions": a.get_scaled_positions().tolist(), "pseudopotentials": pp,
          "kgrid": grid[:3], "kshift": grid[3:], "ecutwfc": system.get("ecutwfc"),
          "ecutrho": system.get("ecutrho"), "occupations": system.get("occupations"), "bytes": len(txt)})
else:
    unsupported(task)
