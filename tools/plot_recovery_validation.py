#!/usr/bin/env python3
"""Recompute publication figures from archived XML; never launch QE."""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def verify(folder):
    payload = json.loads((folder/'validation.json').read_text())
    for case in payload['cases']:
        for role in ['continuous', 'recovered']:
            source = case['sources'][role]
            raw = (folder/source['file']).read_bytes()
            if hashlib.sha256(raw).hexdigest() != source['sha256_public']:
                raise ValueError('Published XML hash mismatch')
            root = ET.fromstring(raw).find('output')
            mapping = {'energy_Ry': ('total_energy/etot', 2),
                       'forces_Ry_bohr': ('forces', 2),
                       'stress_Ry_bohr3': ('stress', 2),
                       'positions_bohr': ('atomic_structure/atomic_positions', 1),
                       'cell_bohr': ('atomic_structure/cell', 1)}
            for metric, (node, factor) in mapping.items():
                values = [float(v)*factor for text in root.find(node).itertext() for v in text.split()]
                if values != case[role][metric]:
                    raise ValueError('Published observables differ from XML')
        for metric, limit in case['tolerances'].items():
            delta = max(abs(a-b) for a, b in zip(case['continuous'][metric], case['recovered'][metric]))
            if delta != case['max_absolute_differences'][metric] or delta > limit:
                raise ValueError('Difference/tolerance gate failed')
    return payload


def plot(folder, language='es'):
    payload = verify(folder)
    es = language == 'es'
    labels = [('energy_Ry', 'Energía total' if es else 'Total energy', 'Ry'),
              ('forces_Ry_bohr', 'Fuerzas' if es else 'Forces', 'Ry/bohr'),
              ('stress_Ry_bohr3', 'Estrés' if es else 'Stress', 'Ry/bohr³'),
              ('positions_bohr', 'Posiciones' if es else 'Positions', 'bohr'),
              ('cell_bohr', 'Celda' if es else 'Cell', 'bohr')]
    names = ['SCF · Si desplazado' if es else 'SCF · displaced Si', 'relax', 'vc-relax']
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11, 'svg.fonttype': 'none'})
    fig, axes = plt.subplots(5, 1, figsize=(10.6, 11.8))
    fig.subplots_adjust(left=.25, right=.94, top=.85, bottom=.15, hspace=1.05)
    colors = ['#0072B2', '#007567', '#B34E00']
    markers = ['o', 's', 'D']
    for ax, (metric, title, unit) in zip(axes, labels):
        tolerance = payload['cases'][0]['tolerances'][metric]
        for i, case in enumerate(payload['cases']):
            delta = case['max_absolute_differences'][metric]
            ratio = 100*delta/tolerance
            ax.scatter(ratio, i, color=colors[i], marker=markers[i], s=62, zorder=3, clip_on=False)
            val = '0' if delta == 0 else f'{delta:.3g}'
            ax.annotate(f'{val} {unit}', (ratio, i), xytext=(10, 0), textcoords='offset points', va='center', fontsize=10)
        ax.axvline(100, color='#5a6468', linestyle='--', linewidth=1.2)
        ax.set_xlim(-1, 110);ax.set_ylim(2.55, -.65)
        ax.set_yticks(range(3), names)
        ax.set_xticks([0, 25, 50, 75, 100], ['0', '25', '50', '75', '100'])
        ax.set_title(f'{title}  |  '+('Tolerancia' if es else 'Tolerance')+f': {tolerance:g} {unit}', loc='left', fontsize=12, pad=10)
        ax.grid(axis='x', color='#e1e6e8', linewidth=.7)
        ax.set_axisbelow(True);ax.tick_params(length=0, pad=6)
        for spine in ax.spines.values():spine.set_visible(False)
    fig.text(.065, .958, 'Olla-DFT 1.2.0 · '+('validación local de recuperación' if es else 'local recovery validation'), fontsize=19, weight='bold', color='#173941')
    fig.text(.065, .919, 'Diferencia frente a la ejecución continua' if es else 'Difference from the continuous execution', fontsize=14)
    fig.text(.065, .891, 'Tres parejas de cálculos QE 7.4 seriales; mismos inputs y entorno por pareja.' if es else 'Three pairs of serial QE 7.4 jobs; same inputs and environment within each pair.', fontsize=11, color='#4f646a')
    fig.text(.25, .101, 'Diferencia máxima / tolerancia (%) · menor es mejor' if es else 'Maximum difference / tolerance (%) · lower is better', fontsize=12)
    note = ('Las etiquetas muestran diferencias absolutas, no incertidumbres. 100% = límite de aceptación.\n'
            '0 significa coincidencia a la precisión del XML. Una pareja por caso, sin inferencia estadística.\n'
            'Interrupciones locales simuladas; no se midió recuperación tras apagones físicos o pérdida del disco.') if es else (
            'Labels show absolute differences, not uncertainties. 100% = acceptance limit.\n'
            '0 means identical at XML precision. One pair per case; no statistical inference.\n'
            'Simulated local interruptions; recovery after physical power loss or disk loss was not measured.')
    fig.text(.065, .032, note, fontsize=10, linespacing=1.5, color='#4f646a')
    for ext in ['png', 'svg', 'pdf']:
        target = folder/f'recovery-{language}.{ext}'
        fig.savefig(target, dpi=180, facecolor='white')
        if ext == 'svg':
            target.write_text('\n'.join(line.rstrip() for line in target.read_text().splitlines())+'\n')
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', nargs='?', type=Path, default=Path(__file__).resolve().parents[1]/'docs/publication-1.2.0')
    args = parser.parse_args()
    for language in ['es', 'en']:plot(args.folder, language)
    print('Verified XML, hashes and 15 differences; generated ES/EN PNG, SVG and PDF.')


if __name__ == '__main__':
    main()
