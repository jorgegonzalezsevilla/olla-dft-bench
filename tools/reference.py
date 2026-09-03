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
    from scipy.optimize import curve_fit
    V, E = map(np.array, read_ev(args[0]))
    def bm3(V, E0, V0, B0, Bp):
        eta = (V0 / V) ** (2.0 / 3.0)
        return E0 + 9 * V0 * B0 / 16 * ((eta - 1) ** 3 * Bp + (eta - 1) ** 2 * (6 - 4 * eta))
    c = np.polyfit(V, E, 2); V0g = -c[1] / (2 * c[0]); E0g = np.polyval(c, V0g); B0g = 2 * c[0] * V0g
    p, _ = curve_fit(bm3, V, E, p0=[E0g, V0g, B0g, 4.0], maxfev=20000)
    emit({"via": "scipy curve_fit of 3rd-order Birch-Murnaghan (independent code)",
          "V0_A3": float(p[1]), "B0_GPa": float(p[2] * 160.21766208), "Bp": float(p[3]), "E0_eV": float(p[0])})
elif task == "bandgap":
    import xml.etree.ElementTree as ET
    root = ET.parse(open_xml(args[0])).getroot()
    out = root.find("output")
    bs = out.find("band_structure")
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
