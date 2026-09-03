"""Task registry: inputs, contestants, reference and grading. Grading is deterministic and
symmetric: the same rule is applied to every tool, including Olla-DFT."""
import math, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INP = ROOT / "inputs"
TOOLS = {"olla-dft": "ollad.py", "ase": "ase_tool.py", "pymatgen": "pymatgen_tool.py", "seekpath": "seekpath_tool.py", "qeschema": "qeschema_tool.py"}
STRUCTURES = ["Si_relajado.cif", "ZnO.cif", "grafito.cif", "hbn.cif", "POSCAR_NaCl"]

GAMMA = {"G", "GAMMA", "\\GAMMA", "Γ", "\\Gamma", "Gamma"}


def norm_label(s):
    s = s.strip()
    return "Γ" if s in GAMMA else re.sub(r"[_{}]", "", s)


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
    return a is not None and b is not None and abs(a - b) <= tol


# ---- grading functions: (payload, reference_payload) -> (ok: bool|None, detail: str) ----
def grade_symmetry(p, r):
    ok = p.get("spacegroup") == r["spacegroup"] and p.get("natoms_primitive") == r["natoms_primitive"]
    return ok, f"sg {p.get('spacegroup')} vs ref {r['spacegroup']}; prim atoms {p.get('natoms_primitive')} vs {r['natoms_primitive']}"


def grade_kpath(p, r):
    sp, sr = path_segments(p.get("path", [])), path_segments(r["path"])
    same = sp == sr
    j = len(sp & sr) / len(sp | sr) if (sp | sr) else 0.0
    return same, (f"segments identical to HPKOT reference" if same else
                  f"path differs from HPKOT reference (Jaccard {j:.2f}); a different convention, not necessarily an error")


def grade_eos(p, r):
    okV = close(p.get("V0_A3"), r["V0_A3"], 1e-4)
    okB = close(p.get("B0_GPa"), r["B0_GPa"], 1e-3)
    d = f"ΔV0={p.get('V0_A3', float('nan')) - r['V0_A3']:+.2e} Å³, ΔB0={p.get('B0_GPa', float('nan')) - r['B0_GPa']:+.2e} GPa"
    if p.get("Bp") is None:
        d += "; B' not reported"
    return okV and okB, d


def grade_bandgap(p, r):
    ok = close(p.get("gap_eV"), r["gap_eV"], 1e-3)
    return ok, f"gap {p.get('gap_eV')} eV vs ref {r['gap_eV']:.4f} eV"


def grade_inputgen(p, r):
    rt = p.get("roundtrip") or {}
    ok = (rt.get("natoms") == r["natoms"] and close(rt.get("volume_A3"), r["volume_A3"], 1e-3)
          and rt.get("kgrid") == r.get("kgrid_expected") and rt.get("ecutwfc") == 30.0)
    return ok, f"parsed back: {rt.get('natoms')} atoms, V={rt.get('volume_A3')} Å³ (ref {r['natoms']}, {r['volume_A3']:.4f}); k-grid {rt.get('kgrid')} (expected {r.get('kgrid_expected')}), ecutwfc {rt.get('ecutwfc')} (expected 30)"


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
        "note": "Olla-DFT is called through the fit function behind `olla-dft eos --collect`, because the command reads pw.x outputs, not a bare table. The reference is an analytic linear fit, deliberately a different algorithm from every contestant's curve_fit.",
    },
    "bandgap": {
        "title": "Band gap from pw.x output (XML and text)",
        "inputs": ["Si.xml.gz", "Si_scf.xml", "Si_scf.out"], "tools": ["olla-dft", "qeschema", "ase", "pymatgen"], "grade": grade_bandgap,
        "args": lambda inp, work: [str(INP / inp)],
        "note": "Three inputs so that no tool is judged only on the format it prefers: the XML of a 122-k bands run (QE 6.6, no input shipped), and the XML and text output of the same scf run generated with the shipped inputs/Si_scf.in (QE 7.4). Olla-DFT and qeschema read the XML; ASE reads the text output; pymatgen reads neither for eigenvalues.",
    },
    "inputgen": {
        "title": "pw.x scf input from a structure (Si 4×4×4, ZnO 6×6×4, fixed cutoffs)",
        "inputs": ["Si_relajado.cif", "ZnO.cif"], "tools": ["olla-dft", "ase", "pymatgen"], "grade": grade_inputgen,
        "args": lambda inp, work: [str(INP / inp), str(work / "gen"), str(work / "pp"), {"Si_relajado.cif": "4x4x4", "ZnO.cif": "6x6x4"}[inp]],
        "note": "Each generated file is parsed back by ASE (reference) to check atoms, volume, k-grid and ecutwfc. Cutoffs and grid are forced equal so the comparison is about correctness and cost, not defaults; other defaults (mixing, smearing) remain each tool's own and show up in the end-to-end stage.",
    },
}
