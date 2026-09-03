"""qeschema (Quantum ESPRESSO's own XML schema package) as a bandgap contestant."""
import sys, gzip, shutil, tempfile, os
import numpy as np
from _common import emit, unsupported, HA_EV
task, args = sys.argv[1], sys.argv[2:]
if task != "bandgap":
    unsupported("qeschema only reads the pw.x XML")
path = args[0]
if path.endswith(".out"):
    unsupported("qeschema reads the data-file-schema XML, not the text output")
import qeschema
tmp = None
if path.endswith(".gz"):
    tmp = tempfile.mkdtemp(); dst = os.path.join(tmp, "data-file-schema.xml")
    with gzip.open(path, "rb") as f, open(dst, "wb") as g: shutil.copyfileobj(f, g)
    path = dst
doc = qeschema.PwDocument(); doc.read(path, validation="lax")
bs = doc.to_dict(validation="lax")["qes:espresso"]["output"]["band_structure"]
nelec = float(bs["nelec"]); ks = bs["ks_energies"]
eigs = np.array([k["eigenvalues"]["$"] for k in ks]) * HA_EV
nv = int(round(nelec / 2)); vbm, cbm = eigs[:, nv - 1].max(), eigs[:, nv].min()
if tmp: shutil.rmtree(tmp, ignore_errors=True)
emit({"via": "qeschema.PwDocument + numpy (VBM/CBM from eigenvalues)", "gap_eV": float(cbm - vbm), "vbm_eV": float(vbm), "cbm_eV": float(cbm)})
