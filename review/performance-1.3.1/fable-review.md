# Fable 5.1 High — review of the proposed performance change

The reviewer received a product-level implementation summary, not source code or scientific data. Response below is unedited; recommendations require verification.

Reviso el cambio propuesto y el plan de medición. Aquí va mi valoración en español, sin usar herramientas.

**Valoración general.** El diseño es sólido: aplaza los imports pesados sin duplicar catálogos ni tocar el ajuste numérico. Los riesgos reales están en la compatibilidad de la superficie de módulo, en cómo se verifica que matplotlib no se carga, y en la validez estadística de la medición.

## Riesgos del cambio de código

- **Símbolos de módulo que desaparecen.** Hoy `olla_dft.eos.structure`, `olla_dft.eos.sweep`, `olla_dft.eos.provenance` y `olla_dft.style.matplotlib` existen como atributos. Cualquier test o usuario que haga `monkeypatch.setattr("olla_dft.eos.style...")` o `from olla_dft.eos import sweep` se rompe. Eso es una eliminación de API aunque no se elimine ninguna función pública. Revisad la suite en busca de patches sobre esos atributos antes de mover nada.
- **Anotaciones de tipo.** Si `finish_axes`, `panel_label` o `save` anotan `Axes` o `Figure`, el import perezoso produce `NameError` en tiempo de ejecución o fallos en mypy. Hace falta `from __future__ import annotations` más un bloque `TYPE_CHECKING`.
- **Efectos secundarios en import.** Si `style.py` modifica `rcParams` o llama a `matplotlib.use()` al importarse, quien hoy hace `import olla_dft.style` para configurar el estilo deja de obtener ese efecto. Confirmad que no hay estado global aplicado en import.
- **Provenance y versión de matplotlib.** Si `provenance` registra `matplotlib.__version__` accediendo al módulo, el export del EOS seguirá importando matplotlib. Usad `importlib.metadata.version` para leer versiones sin importar el paquete. Si la salida de provenance cambia por esto, los hashes del benchmark cambiarán y hay que decidirlo antes de medir.
- **Imports indirectos.** El test "EOS puro sin ASE/spglib/matplotlib" solo se sostiene si `qeout` tampoco importa ASE. Comprobadlo, porque es el import más probable de colarse.
- **Dependencia opcional o dura.** Si matplotlib es opcional, el import perezoso convierte un error de instalación en un error tardío dentro de `plot`. Envolvedlo con un mensaje claro que indique el extra a instalar.
- **Linter.** Ruff marcará PLC0415 en cada import dentro de función. Añadid un ignore por fichero con comentario que explique el motivo, no un `noqa` por línea.
- **Import de pyplot en hilos.** Si `plot` puede llamarse desde un pool de hilos, el primer import de pyplot fuera del hilo principal puede seleccionar backend de forma inesperada. Forzad `Agg` cuando no haya display o importad solo `matplotlib` y no `pyplot` donde baste.

## Riesgos de la cobertura de regresión

- **Verificación de "no inicializado".** Tras terminar el subproceso no se puede inspeccionar `sys.modules`. La forma robusta es lanzar el CLI con `-X importtime` y comprobar que ninguna línea contiene `matplotlib`, o ejecutar el comando vía `runpy` dentro de un `python -c` que imprima el estado al final.
- **Verificación de "sin caché".** Solo tiene sentido con `MPLCONFIGDIR` apuntando a un directorio temporal vacío por test. Sin eso, la aserción es vacía porque la caché del desarrollador ya existe.
- **Casos no cubiertos.** Añadid `--help` y una invocación con argumentos inválidos, porque argparse puede tocar los metadatos de estilo al formatear ayuda o errores. Añadid también `import olla_dft` e `import olla_dft.eos` en subproceso limpio, no solo el comando `info`.
- **Test en español.** No dependáis de que exista `es_ES.UTF-8` en CI. Usad el mecanismo propio del paquete para fijar idioma.
- **Test de renderizado.** Fijad `MPLBACKEND=Agg` en el entorno del test para que no dependa de la máquina.

## Riesgos del plan de medición

- **Instalación secuencial rompe el intercalado.** Si la wheel base se mide en una franja horaria y la candidata en otra, carga de fondo y estado térmico se confunden con el efecto. Mejor dos venvs idénticos salvo `olla-dft`, verificados con el hash de `pip freeze`, y alternar A/B en cada repetición.
- **Caché de fuentes.** La ganancia grande está en el primer arranque sin caché. Medid dos escenarios explícitos: `MPLCONFIGDIR` persistente tras el warmup, y `MPLCONFIGDIR` limpio en cada repetición. Reportad ambos por separado.
- **Afinidad a un solo núcleo.** Evitad el núcleo 0, que suele atender interrupciones. Fijad el governor en `performance` y, si es posible, desactivad turbo y anotadlo en los límites.
- **Métrica complementaria.** El tiempo de pared en portátil es ruidoso. Registrad también tiempo de CPU usuario+sistema y la suma de `-X importtime` del subárbol de matplotlib. Esa última cifra es casi determinista y explica el mecanismo.
- **Estadística.** Con 15 repeticiones usad mediana e intervalo intercuartílico, más un intervalo bootstrap para la diferencia. Fijad de antemano el umbral de efecto que consideráis relevante.
- **Proceso de medición.** Si el wrapper del harness importa matplotlib en el mismo intérprete antes de invocar la herramienta, la ganancia desaparece. Confirmad que cada tarea se cronometra en un subproceso propio.
- **Expectativas por tarea.** Solo debería mejorar lo que pase por el parser o por `eos`. Si `symmetry` y `kpath` también mejoran, es porque el `__init__` importa `eos`. Si no mejora nada, revisad si el harness ya tenía matplotlib cargado.
- **Hashes de salida.** Exigid salida bit a bit idéntica entre base y candidata en las cinco tareas, excluyendo timestamps. Cualquier diferencia es una regresión de comportamiento, no ruido.

Estoy de acuerdo en no tocar el harness para mejorar posiciones. Lo único que recomiendo cambiar en él es lo estrictamente instrumental: el intercalado A/B y la captura de tiempo de CPU.
