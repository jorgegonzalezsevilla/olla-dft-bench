"""Task registry: inputs, contestants, reference and grading. Grading is deterministic and
symmetric: the same rule is applied to every tool, including Olla-DFT."""
import re
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INP = ROOT / "inputs"
TOOLS = {"olla-dft": "ollad.py", "ase": "ase_tool.py", "pymatgen": "pymatgen_tool.py", "seekpath": "seekpath_tool.py", "qeschema": "qeschema_tool.py"}
STRUCTURES = ["Si_relajado.cif", "ZnO.cif", "grafito.cif", "hbn.cif", "POSCAR_NaCl"]

GAMMA = {"G", "GAMMA", "\\GAMMA", "Γ", "\\Gamma", "Gamma"}


def norm_label(s):
    s = s.strip()
    s = "Γ" if s in GAMMA else re.sub(r"[_{}]", "", s)
    for a, b in (("SIGMA", "Σ"), ("DELTA", "Δ"), ("LAMBDA", "Λ")):
        s = s.replace(a, b)
    return s


def path_segments(paths):
    """Undirected set of consecutive special-point pairs from any of the path notations."""
    segs = set()
    for p in paths:
        for chunk in re.split(r"[,|]", p):
            pts = [norm_label(x) for x in re.split(r"-|—", chunk) if x.strip()]
            if len(pts) == 1 and len(chunk) > 1 and "-" not in chunk:   # ASE compact 'GMKG'
                pts = [norm_label(c) for c in chunk]
            for a, b in zip(pts, pts[1:]):
                segs.add(frozenset((a, b)))
    return segs


def close(a, b, tol):
    return (isinstance(a, (int, float)) and isinstance(b, (int, float))
            and math.isfinite(a) and math.isfinite(b) and abs(a - b) <= tol)


# ---- grading functions: (payload, reference_payload) -> (ok: bool|None, detail: str) ----
def grade_symmetry(p, r):
    ok = p.get("spacegroup") == r["spacegroup"] and p.get("natoms_primitive") == r["natoms_primitive"]
    return ok, f"sg {p.get('spacegroup')} vs ref {r['spacegroup']}; prim atoms {p.get('natoms_primitive')} vs {r['natoms_primitive']}"


def grade_kpath(p, r):
    if p.get("convention") != r.get("convention"):
        return None, "different convention; not compared with HPKOT"
    sp, sr = path_segments(p.get("path", [])), path_segments(r["path"])
    points = {norm_label(k): v for k, v in p.get("point_coords", {}).items()}
    ref = {norm_label(k): v for k, v in r.get("point_coords", {}).items()}
    used = set().union(*sr) if sr else set()
    ok = sp == sr and bool(used) and all(
        k in points and k in ref and len(points[k]) == 3 and
        all(close(a, b, 1e-5) for a, b in zip(points[k], ref[k])) for k in used)
    return ok, "HPKOT segments and coordinates match" if ok else "HPKOT segments or coordinates differ"


def grade_eos(p, r):
    okV = close(p.get("V0_A3"), r["V0_A3"], 1e-4)
    okB = close(p.get("B0_GPa"), r["B0_GPa"], 1e-3)
    if not isinstance(p.get("V0_A3"), (int, float)) or not isinstance(p.get("B0_GPa"), (int, float)):
        return False, "EOS fit returned no finite parameters"
    d = f"ΔV0={p.get('V0_A3', float('nan')) - r['V0_A3']:+.2e} Å³, ΔB0={p.get('B0_GPa', float('nan')) - r['B0_GPa']:+.2e} GPa"
    if p.get("Bp") is None:
        d += "; B' not reported"
    return okV and okB and p.get("ok", True) is True, d


def grade_bandgap(p, r):
    ok = all(close(p.get(k), r.get(k), 1e-3) for k in ("gap_eV", "vbm_eV", "cbm_eV"))
    return ok, f"gap {p.get('gap_eV')} eV vs ref {r['gap_eV']:.4f} eV; VBM/CBM checked"


def same_geometry(p, r):
    try:
        cp, cr = p["cell"], r["cell"]
        if len(cp) != 3 or any(len(row) != 3 for row in cp):
            return False
        metric = lambda c, i, j: sum(c[i][k] * c[j][k] for k in range(3))
        if not all(close(metric(cp, i, j), metric(cr, i, j), 1e-4) for i in range(3) for j in range(3)):
            return False
        ps, rs = p["scaled_positions"], r["scaled_positions"]
        if len(ps) != len(rs) or len(ps) != len(p["symbols"]):
            return False
        available = set(range(len(rs)))
        for symbol, position in zip(p["symbols"], ps):
            if len(position) != 3 or not all(math.isfinite(x) for x in position):
                return False
            for j in sorted(available):
                delta = [(position[k] - rs[j][k] + .5) % 1 - .5 for k in range(3)]
                dist = math.sqrt(sum(sum(delta[k] * cr[k][l] for k in range(3)) ** 2 for l in range(3)))
                if symbol == r["symbols"][j] and dist < 1e-4:
                    available.remove(j)
                    break
            else:
                return False
        return not available
    except (KeyError, TypeError, ValueError, IndexError):
        return False


def grade_inputgen(p, r):
    rt = p.get("roundtrip") or {}
    ok = (rt.get("natoms") == r["natoms"] and close(rt.get("volume_A3"), r["volume_A3"], 1e-3)
          and rt.get("kgrid") == r.get("kgrid_expected") and rt.get("kshift") == [0, 0, 0]
          and close(rt.get("ecutwfc"), 30., 1e-8) and close(rt.get("ecutrho"), 240., 1e-8)
          and rt.get("occupations") == "fixed" and rt.get("pseudopotentials") == r.get("pseudopotentials")
          and same_geometry(rt, r))
    return ok, "geometry, species, pseudos, grid/shift, occupations and cutoffs " + ("match" if ok else "MISMATCH")



TASKS = {
    "symmetry": {
        "title": "Structure parsing and symmetry (file → space group, primitive cell)",
        "inputs": STRUCTURES, "tools": ["olla-dft", "ase", "pymatgen"], "grade": grade_symmetry,
        "args": lambda inp, work: [str(INP / inp)],
        "note": "Reference shares its backend (spglib) with all three contestants: the grade checks that each wrapper preserves the result, not the algorithm. Timing measures wrapper cost (import + parse + report).",
    },
    "kpath": {
        "title": "High-symmetry k-path from a structure",
        "inputs": STRUCTURES, "tools": ["olla-dft", "seekpath", "ase", "pymatgen"], "grade": grade_kpath,
        "args": lambda inp, work: [str(INP / inp)],
        "note": "Reference is the HPKOT convention (seekpath). Olla-DFT and the seekpath contestant call the same library, so their agreement is expected and only shows the path is passed through intact. ASE and pymatgen implement Setyawan–Curtarolo; a mismatch there is a convention difference, not an error.",
    },
    "eos": {
        "title": "Birch–Murnaghan fit of an E(V) table (9 points, Si)",
        "inputs": ["EOS.dat"], "tools": ["olla-dft", "ase", "pymatgen"], "grade": grade_eos,
        "args": lambda inp, work: [str(INP / inp)],
        "note": "Olla-DFT is called through the fit function behind `olla-dft eos --collect`, because the command reads pw.x outputs, not a bare table. EOS.dat is the table exported by `olla-dft eos Si.cif --run` in examples/demo_calculo of the Olla-DFT repository (QE 6.6, 9 volumes, ±10 %). The reference is an analytic linear fit, deliberately a different algorithm from every contestant's curve_fit.",
    },
    "bandgap": {
        "title": "Band gap from pw.x output (XML and text)",
        "inputs": ["Si_scf.xml", "Si_scf.out"], "tools": ["olla-dft", "qeschema", "ase", "pymatgen"], "grade": grade_bandgap,
        "args": lambda inp, work: [str(INP / inp)],
        "note": "The XML and the text output of the same scf run, generated with the shipped inputs/Si_scf.in (QE 7.4), so that each format counts once and no tool is judged only on the format it prefers. Olla-DFT and qeschema read the XML; ASE reads the text output; pymatgen reads neither for eigenvalues.",
    },
    "inputgen": {
        "title": "pw.x scf input from a structure (Si 4×4×4, ZnO 6×6×4, fixed cutoffs)",
        "inputs": ["Si_relajado.cif", "ZnO.cif"], "tools": ["olla-dft", "ase", "pymatgen"], "grade": grade_inputgen,
        "args": lambda inp, work: [str(INP / inp), str(work / "gen"), str(work / "pp"), {"Si_relajado.cif": "4x4x4", "ZnO.cif": "6x6x4"}[inp]],
        "note": "Each generated file is parsed back by ASE to check species, positions, cell metric, pseudopotentials, grid/shift, occupations and both cutoffs. Cutoffs and grid are forced equal so the comparison is about correctness and cost, not defaults; other defaults (mixing, smearing) remain each tool's own and show up in the end-to-end stage.",
    },
}
