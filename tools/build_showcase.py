#!/usr/bin/env python3
"""Package existing public example figures; no simulation or numerical editing."""
import argparse
import hashlib
import json
from pathlib import Path
import textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

SAMPLES = [
 ('bands', 'demo_Si/Si_bandas_dos.png', 'demo_Si', 'Bandas y DOS · silicio', 'Bands and DOS · silicon',
  'Ejemplo LDA; gap calculado de 0,52 eV. No equivale al gap experimental.', 'LDA example; calculated gap 0.52 eV. This is not the experimental gap.'),
 ('spin', 'demo_Fe/Fe_dos.png', 'demo_Fe', 'Magnetismo · hierro bcc', 'Magnetism · bcc iron',
  'DOS resuelta por espín de un ejemplo ferromagnético. Canales opuestos por convención gráfica.', 'Spin-resolved DOS of a ferromagnetic example. Opposite channels follow the plotting convention.'),
 ('eos', 'demo_calculo/eos.png', 'demo_calculo', 'Ecuación de estado · silicio', 'Equation of state · silicon',
  'Energía frente a volumen y residuos del ajuste Birch–Murnaghan. Ejemplo LDA.', 'Energy versus volume and Birch–Murnaghan fit residuals. LDA example.'),
 ('phonons', 'demo_propiedades/fonones_Si.png', 'demo_propiedades', 'Vibraciones de la red · silicio', 'Lattice vibrations · silicon',
  'Dispersión y DOS de fonones. Ejemplo LDA, malla q de 2×2×2; no implica convergencia para otros materiales.', 'Phonon dispersion and DOS. LDA example, 2×2×2 q mesh; not a convergence claim for other materials.'),
 ('optics', 'demo_propiedades/opticas_Si.png', 'demo_propiedades', 'Respuesta óptica · silicio', 'Optical response · silicon',
  'Funciones ópticas del ejemplo: corrección scissor de 0,65 eV. El ajuste óptico mostrado no es el gap electrónico indirecto.', 'Example optical functions with a 0.65 eV scissor correction. The displayed optical fit is not the indirect electronic gap.'),
]


def build(source, output):
    assets=output/'gallery'
    assets.mkdir(exist_ok=True)
    manifest=[]
    for key, rel, example, *captions in SAMPLES:
        raw=(source/'examples'/rel).read_bytes()
        (assets/f'{key}.png').write_bytes(raw)
        manifest.append({'id':key,'file':f'{key}.png','sha256':hashlib.sha256(raw).hexdigest(),
                         'source':f'https://github.com/jorgegonzalezsevilla/olla-dft/blob/v1.2.0/examples/{rel}',
                         'conditions':f'https://github.com/jorgegonzalezsevilla/olla-dft/tree/v1.2.0/examples/{example}',
                         'caption_es':captions[0],'caption_en':captions[1],'scope_es':captions[2],'scope_en':captions[3]})
    (assets/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    for lang in ['es','en']:
        es=lang=='es'
        with PdfPages(assets/f'olla-dft-gallery-{lang}.pdf') as pdf:
            for item in manifest:
                fig=plt.figure(figsize=(11.7,8.3),facecolor='white')
                fig.text(.055,.93,'OLLA-DFT 1.2.0',size=12,color='#007567',weight='bold')
                fig.text(.055,.865,item[f'caption_{lang}'],size=24,weight='bold',color='#193840')
                ax=fig.add_axes((.055,.23,.89,.57));ax.imshow(plt.imread(assets/item['file']));ax.axis('off')
                fig.text(.055,.16,textwrap.fill(item[f'scope_{lang}'],110),size=11,linespacing=1.4)
                fig.text(.055,.075,'Ejemplo existente · condiciones y archivos fuente' if es else 'Existing example · conditions and source files',size=10,color='#007567',url=item['conditions'])
                fig.text(.055,.04,'Jorge Enrique González Sevilla · GPL-3.0-or-later · '+('Sin simulaciones nuevas para esta galería.' if es else 'No new simulations for this gallery.'),size=9,color='#52666b')
                pdf.savefig(fig);plt.close(fig)
            fig=plt.figure(figsize=(8.3,11.7),facecolor='white')
            ax=fig.add_axes((0,0,1,1));ax.imshow(plt.imread(output/f'recovery-{lang}.png'));ax.axis('off')
            pdf.savefig(fig);plt.close(fig)
    # Keep the public introduction in sync without restoring the old technical landing.
    from build_public_page import render
    render(output)
    (assets/'README.md').write_text('''# Olla-DFT visual guide / Guía visual

Five original example images and a six-page PDF in each language. The final page shows local recovery validation from the benchmark. No new calculations were run and no numerical figure content was changed.

Each original PNG is copied byte for byte from the public software examples; `manifest.json` records SHA-256, captions, scope and versioned source links. The PDF is a presentation of those images, not a new scientific result. Existing figure labels may be in Spanish in both PDFs.

The examples use different inputs and methods. In particular, the LDA electronic band gap, scissor-corrected optical fit and phonon calculation are not interchangeable results. Check source conditions before reuse. Local recovery checks do not establish recovery after physical power loss or disk loss.

Author: Jorge Enrique González Sevilla. License: GPL-3.0-or-later, matching the software examples. Cite Olla-DFT, Quantum ESPRESSO and the pseudopotentials used.

Regenerate from the benchmark repository: `python tools/build_showcase.py --source ../olla-dft`.
''')
    print('Packaged five original PNGs, two six-page PDFs and their provenance.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--output',type=Path,default=Path('docs/publication-1.2.0'))
    args=parser.parse_args()
    build(args.source,args.output)
