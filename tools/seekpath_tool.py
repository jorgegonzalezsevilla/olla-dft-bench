import sys
from _common import emit, unsupported
task, args = sys.argv[1], sys.argv[2:]
if task != "kpath":
    unsupported("seekpath only provides k-paths")
from ase.io import read
import seekpath
a = read(args[0])
r = seekpath.get_path((a.cell[:], a.get_scaled_positions(), a.numbers), symprec=1e-4)
emit({"via": "seekpath.get_path (HPKOT)", "labels": sorted(set(r["point_coords"])),
      "path": ["-".join(seg) for seg in r["path"]], "spacegroup": r["spacegroup_number"]})
