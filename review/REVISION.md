# Revisión de olla-dft-bench y Olla-DFT — 4 de septiembre de 2026

La revisión encontró defectos reproducibles tanto en Olla-DFT como en el benchmark. Las marcas de corrección y `VERIFY PASS` del benchmark no bastan para concluir que un cálculo es válido: hay fallos, datos incompletos y propiedades que no se comprueban.

Se revisó el benchmark en `b54d88235d5a1dfdc57bf68d47a04b015087b877` y la instalación Olla-DFT 1.1.0, commit `caf08257293e1fe1ef2ebf9db051b3ec827a7f45`. Los archivos Python instalados coinciden con los hashes de su registro de instalación. No se cambiaron los algoritmos ni los criterios de calificación durante la auditoría.

## Defectos de Olla-DFT reproducidos

### O1 · Alta · Declara metálico un cálculo sin bandas de conducción

Se creó una copia del XML de Si conservando únicamente sus cuatro bandas ocupadas, sus ocho electrones y su nivel de Fermi. Las ocupaciones son todas 1 y ninguna banda cruza el nivel de Fermi. `olla-dft gap` termina con código 0 e informa: «Sistema METÁLICO: hay bandas que cruzan el nivel de Fermi».

La ausencia de bandas vacías impide determinar el gap; no demuestra metalicidad. El error está en `qekit/modules/bands.py:184-186`: la condición que detecta ausencia de bandas por encima del nivel de referencia retorna `is_metal=True` antes del manejo posterior de bandas de conducción ausentes.

Primero se reprodujo con `Si_occupied_only.xml`, una copia derivada, y las claves `occupied_only_gap_cli` y `occupied_only_details` de `evidence.json`.

**Confirmación con cálculo real:** se ejecutó `gen Si_relajado.cif -p scf --insulator --kgrid 4 4 4 --ecutwfc 30 --ecutrho 240`, seguido de QE 7.4 y `gap`. QE terminó y convergió correctamente, con energía −22.82476715 Ry, cuatro bandas y ocho electrones. Olla-DFT volvió a declarar «Sistema METÁLICO». El generador no solicitó bandas vacías adicionales. Se conservaron el input, el XML y las salidas originales en `qe-default-scf/`, junto con `evidence.json`. No hace falta modificar un XML para desencadenar el defecto.

Corrección propuesta: distinguir datos insuficientes de metalicidad y comprobar ocupaciones/número de bandas antes de clasificar.

### O2 · Alta · Genera entradas inválidas y devuelve éxito

Dos invocaciones reales de `gen` produjeron archivos `scf.in` con código de salida 0:

- `--kgrid 0 -2 4` escribe exactamente `0 -2 4 0 0 0` en `K_POINTS automatic`.
- `--ecutwfc -30 --ecutrho -240` escribe ambos valores negativos.

`qekit/modules/inputgen.py:655-656,685` acepta directamente los valores; el parser de `gen` solo comprueba que la malla contenga tres enteros. El usuario recibe un mensaje de generación exitosa y descubre el error después, al intentar calcular.

Evidencia: `invalid_kgrid/scf.in`, `negative_cutoffs/scf.in`, claves homónimas de `evidence.json`. Estas entradas inválidas no se enviaron a QE.

Corrección propuesta: validar enteros de malla mayores que cero y cutoffs positivos y finitos antes de escribir archivos, tanto en la CLI como en la API.

### O3 · Media · El reporte de gap omite la falta de convergencia

Una copia del XML original con `convergence_achieved=false` produce el mismo gap de 0.6155 eV y termina con código 0, sin advertencia de convergencia. El lector sí obtiene `converged=False`; `gap_report` no lo utiliza.

Ubicación: `qekit/cli.py:538-543` y `qekit/modules/bands.py:222` en adelante. Evidencia: `Si_unconverged.xml`, `unconverged_gap_cli` y `unconverged_parsed_flag`.

Corrección propuesta: mostrar explícitamente que los resultados proceden de un cálculo no convergido y definir una política de salida para automatización.

## Defectos del benchmark

| ID | Prioridad | Hallazgo y reproducción | Ubicación |
|---|---|---|---|
| B1 | Alta | Elimina las muestras fallidas antes de calcular `correct`. Con 14 fallos y un acierto, conserva `correct=[true]`, presenta la celda como correcta y permite que gane por velocidad. El contador `failed` existe en JSON, pero no se usa para esa decisión ni se muestra en la tabla. | `benchlib/report.py:21-29,59-71,118-121` |
| B2 | Alta | `verify` acepta cero registros aun con 15 repeticiones y tareas declaradas. La copia deliberadamente incompleta devuelve `VERIFY PASS`. No valida cardinalidad, presencia de tareas/celdas, unicidad de repeticiones ni cobertura e2e requerida. | `bench.py:183-236` |
| B3 | Alta | El parámetro `timeout=600` no se utiliza. Una prueba con timeout de 0.01 s y un hijo que duerme 0.25 s retorna normalmente después de vencer el límite. Un hijo colgado puede detener toda la corrida, que guarda los resultados únicamente al final. | `benchlib/measure.py:43-60`; `bench.py:131-139` |
| B4 | Alta | La etapa QE acepta cualquier muestra con energía, aunque tenga `rc != 0` o no haya convergido. Solo usa la primera energía y las primeras iteraciones; otra repetición con una energía distinta queda fuera de la comprobación de concordancia. El wrapper tampoco propaga el código de salida de QE. | `benchlib/report.py:74-81`; `tools/run_pw.py:9-17`; `bench.py:120-123` |
| B5 | Alta | La calificación de estructuras generadas no verifica elementos, posiciones, forma de celda, pseudopotenciales, desplazamiento de malla ni `ecutrho`. El mismo número de átomos y volumen puede corresponder a una estructura completamente distinta. Un input con He superpuesto y `ecutrho=-1` pasa si mantiene los cuatro campos evaluados. | `benchlib/tasks.py:64-68`; `tools/reference.py:75-84` |
| B6 | Media | La tarea anuncia gap, VBM y CBM, pero solo verifica el gap. VBM=-999 y CBM=999 pasan si `gap_eV` coincide. K-path solo evalúa etiquetas de segmentos: coordenadas erróneas tampoco se detectarían. | `benchlib/tasks.py:42-47,59-61`; `tools/ollad.py:26-30` |
| B7 | Media | El wrapper dice que no existe una malla explícita y calcula un espaciado con Olla-DFT fuera de la medición. La misma versión fijada sí ofrece `gen --kgrid N N N`; la ausencia de esa opción no es un defecto actual de Olla-DFT. | `tools/ollad.py:55-65`; Olla-DFT `qekit/cli.py:189-190` |
| B8 | Media | `clean_env` conserva `XDG_CONFIG_HOME` y `XDG_CACHE_HOME` cuando ya existen, a pesar de prometer una configuración privada. Se reprodujo que devuelve la ruta externa recibida. La configuración personal puede afectar una corrida sin quedar registrada. | `benchlib/measure.py:8-21` |
| B9 | Media | La huella del entorno omite qeschema, uno de los competidores, y pymatgen-core, que contiene implementación utilizada. La lista de paquetes registrada no equivale a «every package version». | `benchlib/envinfo.py:90-91` |
| B10 | Media | El dashboard llama `toFixed` sobre métricas nulas cuando todos los procesos de una celda fallan. Eso puede interrumpir su renderizado. Hallazgo por inspección, sin prueba de navegador. | `benchlib/report.py:195` |

Las reproducciones B1, B2 y B4 usan datos sintéticos deliberados y están fuera de `results/`; no son mediciones reales. El verificador demuestra consistencia interna de lo que recibe, pero hoy no garantiza integridad de una corrida completa ni éxito físico.

## Límites metodológicos

- Solo hay cinco estructuras pequeñas, una tabla EOS y un par XML/texto de Si. No hay pruebas de escala, metales, sistemas magnéticos, SOC, entradas dañadas ni bandas de conducción ausentes.
- Las referencias de simetría y k-path comparten spglib/seekpath con participantes. Verifican integración, no un algoritmo independiente.
- Los k-path de convenciones distintas aparecen con una cruz de «correct», aunque el texto diga que la diferencia no implica un error. Sus tiempos se mezclan en la elección del competidor más rápido.
- El coste medido incluye importaciones, parsing y formato de salida. El benchmark compara la CLI de Olla-DFT con APIs más estrechas de otros paquetes; la diferencia temporal no demuestra por sí sola que el algoritmo de Olla-DFT sea más lento.
- Los intervalos bootstrap actuales no incorporan la incertidumbre de escoger el mejor competidor a partir de las mismas muestras. Las mediciones sucesivas además pueden compartir perturbaciones de carga y temperatura.
- Se borran los inputs generados y salidas de trabajo al terminar. Esto limita la revisión posterior de la física y de los errores de QE.
- En esta sesión systemd no es accesible y MPI requiere sockets que el sandbox bloquea. Esos fallos de ejecución pertenecen al entorno, no a Olla-DFT.

## Reproducción

Desde la raíz del repositorio:

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m pyflakes bench.py benchlib tools tests
.venv/bin/python review/reproduce.py
.venv/bin/python bench.py run --reps 15 --e2e-reps 5 --with-qe --seed 20260904 --label audit-20260904
# En un entorno que permita los sockets locales de MPI:
.venv/bin/python review/qe_gap_case.py
.venv/bin/python bench.py run --tasks inputgen --reps 1 --e2e-reps 5 --with-qe --seed 20260904 --label audit-qe-host
```

`reproduce.py` escribe únicamente pruebas y evidencias dentro de `review/` y usa las funciones existentes. `synthetic-incomplete-run/` es una prueba negativa, no un resultado publicable. Los scripts de entradas inválidas son artefactos de la reproducción; no deben ejecutarse como cálculos.

## Orden recomendado de reparación

1. Corregir clasificación de gap y validación de parámetros en Olla-DFT; agregar regresiones de los casos O1–O3.
2. Hacer que el benchmark conserve y muestre todos los fallos, valide todas las repeticiones esperadas y exija convergencia/éxito de cada ejecución QE.
3. Aplicar realmente el timeout y guardar muestras incrementalmente.
4. Ampliar las comprobaciones de geometría, bandas y coordenadas k; actualizar el wrapper a `--kgrid`.
5. Repetir las mediciones con menor carga, configuración privada e identidad completa de dependencias antes de publicar conclusiones de rendimiento.

## Mediciones de esta revisión

Corrida principal: [20260904-143453](../results/20260904-143453/report.md). 780 muestras medidas y 52 calentamientos; 15 repeticiones por celda. Olla-DFT obtuvo 210/210 aciertos en las muestras soportadas según los criterios existentes. La lectura de gap desde texto se registra como no soportada.

Olla-DFT fue más lento en 13/14 celdas comparadas: razón geométrica de tiempos **1.36×**. Usó más memoria en 14/14: razón geométrica **1.21×**. Los intervalos del benchmark excluyen 1 por el lado de lentitud en 12/14 celdas. La cifra de grafito/simetría tiene un intervalo muy amplio que incluye 1; no demuestra por sí sola una diferencia. Estos son costes de los wrappers/CLI con importaciones y carga variable, no rendimiento algorítmico aislado.

| Tarea | Entrada | Competidor de tiempo | Razón de tiempo | IC 95 % | Razón de memoria frente al más ligero |
|---|---|---|---:|---|---:|
| symmetry | Si_relajado.cif | pymatgen | 1.43 | 1.11–1.82 | 1.25 |
| symmetry | ZnO.cif | pymatgen | 1.42 | 1.29–1.54 | 1.25 |
| symmetry | grafito.cif | pymatgen | 2.02 | 0.56–3.08 | 1.25 |
| symmetry | hbn.cif | pymatgen | 1.99 | 1.36–2.54 | 1.25 |
| symmetry | POSCAR_NaCl | ase | 1.38 | 1.22–1.54 | 1.21 |
| kpath | Si_relajado.cif | ase | 1.42 | 1.26–1.71 | 1.20 |
| kpath | ZnO.cif | ase | 1.28 | 1.09–1.52 | 1.20 |
| kpath | grafito.cif | ase | 1.44 | 1.26–1.63 | 1.20 |
| kpath | hbn.cif | seekpath | 1.31 | 1.28–1.36 | 1.20 |
| kpath | POSCAR_NaCl | ase | 1.38 | 1.35–1.41 | 1.21 |
| eos | EOS.dat | ase | 1.19 | 1.17–1.21 | 1.17 |
| bandgap | Si_scf.xml | qeschema | 0.51 | 0.49–0.52 | 1.08 |
| inputgen | Si_relajado.cif | pymatgen | 1.50 | 1.46–1.52 | 1.28 |
| inputgen | ZnO.cif | pymatgen | 1.49 | 1.48–1.53 | 1.27 |

La lectura de gap XML fue la excepción favorable: 0.51× el tiempo del wrapper de qeschema, con 1.08× su memoria. Generar entradas costó alrededor de 1.49–1.50× el tiempo de pymatgen y 1.27–1.28× la memoria del competidor más ligero.

`verify` devolvió `PASS` para esta corrida pese a que **las 15 ejecuciones QE fallaron** por sockets MPI bloqueados y no produjeron energía. Esto confirma la insuficiencia del verificador y del estado global de ejecución. No se atribuye ese bloqueo a Olla-DFT. La comparación física se ejecutó por separado fuera del sandbox.

Se registraron `powersave`, turbo activo y carga fluctuante; una observación durante la corrida fue 13.13 de carga a un minuto. El suplemento de entorno conserva esa observación, 50 versiones de paquetes y hashes de ocho archivos del benchmark. Las reproducciones breves se ejecutaron durante parte de la corrida: también son una fuente acotada de carga adicional. No se deben publicar las razones como mediciones de una máquina en reposo.

### Validación real con Quantum ESPRESSO

Corrida [20260904-144439](../results/20260904-144439/report.md), fuera del sandbox. Se usó una repetición de generación de entradas para preparar la etapa y **cinco ejecuciones QE por herramienta**. Los tiempos de generación de esta corrida corta no se mezclan con la comparación principal de 15 repeticiones.

Las 15 ejecuciones terminaron con código 0, energía presente y convergencia registrada. Se comprobaron todas las energías, no solamente la primera muestra.

| Herramienta | n | Energía mínima / máxima (Ry) | Iteraciones | k irreducibles | Mediana QE (s) |
|---|---:|---|---|---|---:|
| ase | 5 | -22.82476715 / -22.82476715 | [8] | [13] | 3.17 |
| olla-dft | 5 | -22.82476715 / -22.82476715 | [8] | [13] | 3.24 |
| pymatgen | 5 | -22.82476712 / -22.82476712 | [7] | [24] | 3.49 |

Dispersión entre todas las energías: **3.00e-08 Ry**, dentro de 1e-6 Ry. No se encontró discrepancia energética de Olla-DFT en este caso de Si. Pymatgen usa 24 puntos irreducibles frente a 13 en los otros dos inputs; la comparación temporal QE también incluye esa diferencia.

### Comprobaciones finales

- Suite del repositorio: **12 pruebas aprobadas** (incluye verificación de las dos corridas nuevas).
- Análisis estático con pyflakes: sin hallazgos en benchmark, wrappers, pruebas y scripts de auditoría.
- Ambas corridas devuelven `VERIFY PASS`; el caso de MPI fallido demuestra por qué ese estado no certifica éxito físico.
- Se añadieron resultados, evidencias y esta revisión; el benchmark regeneró su índice y dashboard. No se corrigió código de producción ni se publicó nada.

Archivos principales: `metrics.json`, `evidence.json`, `environment-supplement.json`, `tests.log`, `verify-main.log`, `verify-qe-host.log`, `benchmark.log`, `benchmark-qe-host.log` y `qe-default-scf/`.
