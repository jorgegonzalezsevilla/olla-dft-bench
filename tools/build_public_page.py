#!/usr/bin/env python3
"""Build the bilingual public introduction from existing, unchanged evidence."""
import argparse
import html
import json
from pathlib import Path

COPY = {
'es': {
 'title':'Descubre cómo se comportan los materiales', 'language':'English', 'other':'index-en.html',
 'skip':'Ir al contenido', 'eyebrow':'CIENCIA DE MATERIALES, PASO A PASO',
 'intro':'¿Cómo responde un material a la luz? ¿Qué cambia al comprimirlo? Olla-DFT ayuda a estudiar estas preguntas en una computadora y a convertir los resultados en gráficas que puedes explorar y compartir.',
 'context':'Olla-DFT organiza el trabajo con Quantum ESPRESSO, el programa que realiza las simulaciones de átomos y electrones.',
 'examples_cta':'Descubrir los ejemplos', 'try_cta':'Probar con datos de ejemplo',
 'workflow_title':'De una estructura a una explicación',
 'workflow':[('Describe el material','El punto de partida es cómo están colocados sus átomos.'),('Calcula sus propiedades','La simulación estima cómo se comportan esos átomos y sus electrones.'),('Explora y comparte','Olla-DFT reúne los resultados y te ayuda a crear gráficas y tablas.')],
 'examples_title':'Cinco preguntas que puedes explorar',
 'examples_intro':'Estas gráficas salen de ejemplos ya calculados. No necesitas entender cada símbolo: empieza por la pregunta y la explicación de cada tarjeta.',
 'cards':[
  ('bands','¿Cómo se comportan sus electrones?','Las líneas muestran las energías que pueden tener los electrones en el silicio. Ayudan a estudiar su comportamiento electrónico, relevante para materiales usados en dispositivos.','Leer la gráfica: la separación entre grupos de líneas se llama «gap». Es una propiedad calculada; su valor depende del método utilizado.'),
  ('spin','¿Qué podemos aprender sobre su magnetismo?','Este ejemplo de hierro separa dos grupos de electrones según una propiedad llamada espín. La diferencia entre ambos ayuda a estudiar el magnetismo.','Leer la gráfica: las curvas se dibujan a lados opuestos para distinguir los dos grupos. La parte inferior no representa una cantidad negativa de electrones.'),
  ('eos','¿Qué cambia cuando lo comprimimos?','Al cambiar el volumen del silicio, cambia su energía. Esta curva ayuda a encontrar su tamaño de equilibrio y a estudiar cuánto se resiste a la compresión.','Leer la gráfica: los puntos son resultados calculados y la línea es un ajuste. La parte más baja señala el volumen preferido dentro de este modelo.'),
  ('phonons','¿Cómo vibran sus átomos?','Los átomos de un sólido pueden vibrar alrededor de sus posiciones. Este ejemplo muestra esas vibraciones en el silicio, una base para estudiar propiedades térmicas.','Leer la gráfica: cada curva representa una forma de vibración. Las alturas indican frecuencias, no el movimiento de un átomo a lo largo del tiempo.'),
  ('optics','¿Cómo responde a la luz?','El ejemplo muestra cómo cambia la respuesta óptica del silicio según la energía de la luz. Ayuda a estudiar qué luz absorbe el material.','Leer la gráfica: las distintas curvas describen aspectos de esa respuesta. La estimación óptica mostrada no es el mismo valor que el gap electrónico de la primera tarjeta.')],
 'see_chart':'Ver la gráfica y cómo leerla', 'technical':'Condiciones científicas del ejemplo',
 'source':'Consultar los archivos del cálculo',
 'examples_note':'Son ejemplos de lo que la herramienta permite estudiar. No garantizan el mismo comportamiento en otros materiales ni sustituyen las comprobaciones de cada investigación.',
 'try_title':'Prueba cómo convertir resultados en una gráfica',
 'try_intro':'Abrirás un ejemplo con ocho resultados ya preparados. Puedes cambiar su presentación y descargar una imagen sin instalar Olla-DFT, subir archivos ni ejecutar una simulación.',
 'try_steps':[('Mira el ejemplo','Cada punto corresponde a un resultado guardado. No es una animación de átomos.'),('Dale tu estilo','Abre «Personalizar presentación» y cambia el título, el color o el tamaño.'),('Guarda una imagen','Pulsa «PNG · imagen» para usarla en una presentación. «CSV · tabla» sirve para abrir los datos en una hoja de cálculo.')],
 'open_demo':'Abrir el ejemplo interactivo', 'demo_note':'Esta prueba sirve para aprender a usar la interfaz. Sus puntos no forman una serie de experimentos comparables. Los cambios de presentación solo afectan a tu copia.',
 'recover_title':'Si un cálculo se interrumpe, ¿hay que empezar de cero?',
 'recover_intro':'Olla-DFT puede guardar puntos de continuación para ciertos cálculos. Si se conserva el disco y lo guardado es válido, permite retomar el trabajo al volver a arrancar.',
 'recover_steps':[('Guardar','Conservar avances en un disco persistente.'),('Comprobar','Revisar que lo guardado esté completo y sea compatible.'),('Continuar','Retomar desde un punto válido cuando sea posible.')],
 'recover_result':'¿Qué comprobamos? En tres pruebas pequeñas, interrumpimos procesos y comparamos el resultado recuperado con el de una ejecución continua. Las diferencias quedaron dentro de los límites de aceptación definidos para esas pruebas.',
 'recover_limit':'Esto no garantiza recuperarse de cualquier apagón o de perder el disco.',
 'evidence':'Ver las pruebas, sus cifras y sus límites',
 'figure_read':'Cómo leer esta figura: cada marca indica cuánto difiere un resultado recuperado del continuo. La línea del 100 % es el límite de aceptación; las marcas quedan por debajo. Un 0 significa coincidencia a la precisión registrada, no exactitud física absoluta.',
 'evidence_scope':'QE 7.4 serial; una pareja SCF, una relax y una vc-relax, sin repeticiones estadísticas. Mismos inputs y entorno dentro de cada pareja. Se simularon cortes de procesos locales; no apagones físicos ni pérdida del disco.',
 'columns':['Caso','Propiedad / unidad','Diferencia máxima','Límite de aceptación'],
 'numeric':'Consultar la tabla de cifras',
 'take_title':'Llévate los ejemplos o empieza tu proyecto',
 'take_intro':'El PDF reúne las gráficas y sus condiciones. Si quieres trabajar con tus propios materiales, el repositorio explica cómo instalar la aplicación y preparar los cálculos.',
 'pdf':'Descargar la galería PDF', 'install':'Ver cómo empezar con Olla-DFT',
 'footer':'Olla-DFT · Jorge Enrique González Sevilla · Software libre', 'methods':'Métodos y datos originales', 'repo':'olla-dft/blob/main/README.es.md',
 'download_html':'Guardar el ejemplo para abrirlo sin conexión',
},
'en': {
 'title':'Discover how materials behave', 'language':'Español', 'other':'index.html',
 'skip':'Skip to content', 'eyebrow':'MATERIALS SCIENCE, STEP BY STEP',
 'intro':'How does a material respond to light? What changes when you compress it? Olla-DFT helps study these questions on a computer and turn the results into charts you can explore and share.',
 'context':'Olla-DFT organizes work with Quantum ESPRESSO, the program that runs the simulations of atoms and electrons.',
 'examples_cta':'Discover the examples', 'try_cta':'Try it with example data',
 'workflow_title':'From a structure to an explanation',
 'workflow':[('Describe the material','Start with how its atoms are arranged.'),('Calculate its properties','A simulation estimates how those atoms and their electrons behave.'),('Explore and share','Olla-DFT brings the results together and helps you create charts and tables.')],
 'examples_title':'Five questions you can explore',
 'examples_intro':'These charts come from existing calculations. You do not need to understand every symbol: start with the question and explanation on each card.',
 'cards':[
  ('bands','How do its electrons behave?','The lines show the energies that electrons can have in silicon. They help study electronic behavior, which matters when researching materials for devices.','Reading the chart: the separation between groups of lines is called a gap. It is a calculated property whose value depends on the method used.'),
  ('spin','What can we learn about its magnetism?','This iron example separates two groups of electrons by a property called spin. The difference between them helps study magnetism.','Reading the chart: the curves sit on opposite sides to distinguish the two groups. The lower half does not mean a negative number of electrons.'),
  ('eos','What changes when we compress it?','Changing the volume of silicon changes its energy. This curve helps find its equilibrium size and study how strongly it resists compression.','Reading the chart: the dots are calculated results and the line is a fit. The lowest part marks the preferred volume within this model.'),
  ('phonons','How do its atoms vibrate?','Atoms in a solid can vibrate around their positions. This silicon example shows those vibrations, a starting point for studying thermal properties.','Reading the chart: each curve represents a type of vibration. Heights indicate frequencies, not the motion of one atom over time.'),
  ('optics','How does it respond to light?','This example shows how the optical response of silicon changes with the energy of light. It helps study which light the material absorbs.','Reading the chart: different curves describe parts of that response. The optical estimate shown is not the electronic gap from the first card.')],
 'see_chart':'See the chart and how to read it', 'technical':'Scientific conditions for this example',
 'source':'View the calculation files',
 'examples_note':'These examples show what the tool can help study. They do not guarantee the same behavior in other materials or replace the checks needed for each research project.',
 'try_title':'Try turning results into a chart',
 'try_intro':'Open an example with eight ready-made results. Change its appearance and download an image without installing Olla-DFT, uploading files or running a simulation.',
 'try_steps':[('Look at the example','Choose English in the Idioma menu. Each dot is one saved result, not an animation of atoms.'),('Make it your own','Open “Customize appearance” and change the title, color or size.'),('Save an image','Choose “PNG · image” to use it in a presentation. “CSV · table” opens the data in a spreadsheet.')],
 'open_demo':'Open the interactive example', 'demo_note':'This demo helps you learn the interface. Its points are not a series of comparable experiments. Appearance changes only affect your copy.',
 'recover_title':'If a calculation stops, must you start over?',
 'recover_intro':'Olla-DFT can save restart points for certain calculations. If the disk survives and the saved data is valid, it can resume work when restarted.',
 'recover_steps':[('Save','Keep progress on a persistent disk.'),('Check','Check that saved data is complete and compatible.'),('Continue','Resume from a valid point when possible.')],
 'recover_result':'What did we check? In three small tests, we interrupted processes and compared the recovered result with an uninterrupted run. Differences stayed within the acceptance limits defined for those tests.',
 'recover_limit':'This does not guarantee recovery from every power outage or disk loss.',
 'evidence':'See the tests, numbers and limits',
 'figure_read':'Reading this figure: each mark shows how much a recovered result differs from the uninterrupted one. The 100% line is the acceptance limit; the marks stay below it. A zero means agreement at the recorded precision, not absolute physical accuracy.',
 'evidence_scope':'Serial QE 7.4; one SCF pair, one relax pair and one vc-relax pair, without statistical repetitions. Inputs and environment match within each pair. Local process interruptions were simulated; physical power outages and disk loss were not tested.',
 'columns':['Case','Property / unit','Maximum difference','Acceptance limit'],
 'numeric':'View the table of numbers',
 'take_title':'Take the examples with you or start a project',
 'take_intro':'The PDF collects the charts and their conditions. To work with your own materials, the repository explains how to install the application and prepare calculations.',
 'pdf':'Download the PDF gallery', 'install':'See how to get started with Olla-DFT',
 'footer':'Olla-DFT · Jorge Enrique González Sevilla · Free software', 'methods':'Methods and original data', 'repo':'olla-dft',
 'download_html':'Save the example to open it offline',
}}


def esc(value):
    return html.escape(str(value), quote=True)


def steps(items):
    return '<ol class="steps">'+''.join(f'<li><strong>{esc(title)}</strong><p>{esc(body)}</p></li>' for title,body in items)+'</ol>'


def render(folder):
    manifest={item['id']:item for item in json.loads((folder/'gallery/manifest.json').read_text())}
    evidence=json.loads((folder/'validation.json').read_text())
    for lang,c in COPY.items():
        cards=[]
        for key,title,body,reading in c['cards']:
            item=manifest[key]
            cards.append(f'''<article class="example"><p class="eyebrow">{esc(item[f'caption_{lang}'])}</p>
<h3>{esc(title)}</h3><p>{esc(body)}</p>
<details class="chart"><summary>{esc(c['see_chart'])}</summary>
<a href="gallery/{esc(item['file'])}"><img loading="lazy" src="gallery/{esc(item['file'])}" alt="{esc(item[f'caption_{lang}'])}"></a>
<p>{esc(reading)}</p><details class="conditions"><summary>{esc(c['technical'])}</summary><p>{esc(item[f'scope_{lang}'])}</p>
<a href="{esc(item['conditions'])}">{esc(c['source'])}</a></details></details></article>''')
        rows=''.join('<tr>'+''.join(f'<td>{esc(value)}</td>' for value in [case['case'],metric,case['max_absolute_differences'][metric],limit])+'</tr>' for case in evidence['cases'] for metric,limit in case['tolerances'].items())
        page=f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Olla-DFT · {esc(c['title'])}</title><meta name="description" content="{esc(c['intro'])}"><link rel="stylesheet" href="public-page.css"></head>
<body><a class="skip" href="#main">{esc(c['skip'])}</a>
<header><a class="brand" href="{'index.html' if lang=='es' else 'index-en.html'}">Olla-DFT <span>1.2.0</span></a><a href="{c['other']}" lang="{'en' if lang=='es' else 'es'}">{c['language']}</a></header>
<main id="main"><section class="hero"><div><p class="eyebrow">{c['eyebrow']}</p><h1>{c['title']}</h1><p class="lead">{c['intro']}</p><p>{c['context']}</p>
<div class="actions"><a class="button" href="#examples">{c['examples_cta']}</a><a class="button secondary" href="#try">{c['try_cta']}</a></div></div>
<aside class="workflow"><h2>{c['workflow_title']}</h2>{steps(c['workflow'])}</aside></section>
<section id="examples"><div class="section-heading"><p class="eyebrow">01 / {'DESCUBRE' if lang=='es' else 'DISCOVER'}</p><h2>{c['examples_title']}</h2><p>{c['examples_intro']}</p></div>
<div class="examples">{''.join(cards)}</div><p class="fine">{c['examples_note']}</p></section>
<section id="try" class="panel try"><p class="eyebrow">02 / {'PRUEBA' if lang=='es' else 'TRY IT'}</p><h2>{c['try_title']}</h2><p class="lead">{c['try_intro']}</p>{steps(c['try_steps'])}
<div class="actions"><a class="button" href="explorer.html">{c['open_demo']}</a><a href="explorer.html" download>{c['download_html']}</a></div><p class="fine">{c['demo_note']}</p></section>
<section id="recovery" class="panel"><p class="eyebrow">03 / {'CONTINÚA' if lang=='es' else 'KEEP GOING'}</p><h2>{c['recover_title']}</h2><p class="lead">{c['recover_intro']}</p>{steps(c['recover_steps'])}
<p>{c['recover_result']}</p><p class="note">{c['recover_limit']}</p>
<details class="evidence"><summary>{c['evidence']}</summary><p>{c['figure_read']}</p><img loading="lazy" src="recovery-{lang}.png" alt="{esc(c['figure_read'])}"><p>{c['evidence_scope']}</p>
<p class="downloads"><a href="recovery-{lang}.pdf">PDF</a><a href="recovery-{lang}.svg">SVG</a><a href="validation.csv">CSV</a><a href="validation.json">JSON</a></p>
<details><summary>{c['numeric']}</summary><div class="scroll" tabindex="0" role="region" aria-label="{esc(c['numeric'])}"><table><thead><tr>{''.join('<th scope="col">'+esc(v)+'</th>' for v in c['columns'])}</tr></thead><tbody>{rows}</tbody></table></div></details></details></section>
<section class="panel take"><h2>{c['take_title']}</h2><p>{c['take_intro']}</p><div class="actions"><a class="button" href="gallery/olla-dft-gallery-{lang}.pdf">{c['pdf']}</a><a class="button secondary" href="https://github.com/jorgegonzalezsevilla/{c['repo']}">{c['install']}</a></div></section>
</main><footer><p>{c['footer']}</p><a href="https://github.com/jorgegonzalezsevilla/olla-dft-bench/tree/main/docs/publication-1.2.0">{c['methods']}</a></footer></body></html>
'''
        (folder/('index.html' if lang=='es' else 'index-en.html')).write_text(page)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder',nargs='?',type=Path,default=Path(__file__).resolve().parents[1]/'docs/publication-1.2.0')
    render(parser.parse_args().folder)
    print('Built ES/EN public introductions; source figures and evidence unchanged.')
