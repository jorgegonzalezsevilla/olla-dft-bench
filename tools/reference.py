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
    emit({"via": "seekpath direct (HPKOT convention)", "labels": sorted(set(r["point_coords"])),
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
    # the reference for input generation is the structure itself: natoms and volume from the CIF
    from ase.io import read
    a = read(args[0])
    emit({"via": "ase.io.read of the source structure", "natoms": len(a), "volume_A3": float(a.get_volume())})
elif task == "roundtrip":
    # parse a generated pw.x input back and report natoms, volume, k-grid, ecut (used to grade inputgen)
    from ase.io import read
    a = read(args[0], format="espresso-in")
    txt = open(args[0]).read()
    k = re.search(r"K_POINTS\s+automatic\s*\n\s*(\d+)\s+(\d+)\s+(\d+)", txt, re.I)
    ec = re.search(r"ecutwfc\s*=\s*([\d.]+)", txt)
    emit({"natoms": len(a), "volume_A3": float(a.get_volume()),
          "kgrid": [int(g) for g in k.groups()] if k else None, "ecutwfc": float(ec.group(1)) if ec else None,
          "bytes": len(txt)})
else:
    unsupported(task)
