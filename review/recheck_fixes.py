#!/usr/bin/env python3
"""Recheck fixed Olla-DFT behavior without overwriting the historical audit."""
import importlib.metadata as metadata
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    data = {'olla_dft_version': metadata.version('olla-dft'), 'cases': {}}
    for name, path in [('occupied_only_real', ROOT / 'review/qe-default-scf'),
                       ('unconverged_xml', ROOT / 'review/Si_unconverged.xml')]:
        p = subprocess.run([sys.executable, '-m', 'qekit', 'gap', str(path)], capture_output=True, text=True)
        data['cases'][name] = {'returncode': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}
        assert p.returncode == 2
    assert 'METÁLICO' not in data['cases']['occupied_only_real']['stdout']
    assert 'no convergió' in data['cases']['unconverged_xml']['stdout']
    for name, args in [('invalid_grid', ['--kgrid', '0', '-2', '4']),
                       ('negative_cutoffs', ['--ecutwfc', '-30', '--ecutrho', '-240'])]:
        with tempfile.TemporaryDirectory(prefix='olla-fixed-') as tmp:
            dest = Path(tmp) / 'must-not-exist'
            p = subprocess.run([sys.executable, '-m', 'qekit', 'gen', str(ROOT / 'inputs/Si_relajado.cif'),
                                '-o', str(dest), *args], capture_output=True, text=True)
            data['cases'][name] = {'returncode': p.returncode, 'output_created': dest.exists(),
                                  'stdout': p.stdout, 'stderr': p.stderr}
            assert p.returncode != 0 and not dest.exists()
    path = ROOT / 'review/fixed-evidence.json'
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
    print('4 fixed CLI cases passed:', path)

if __name__ == '__main__':
    main()
