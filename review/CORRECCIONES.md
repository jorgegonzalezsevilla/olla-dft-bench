# Correcciones verificadas — 2026-09-04

Se conserva la auditoría anterior en `REVISION.md`. Las mediciones y reproducciones originales no se reescriben: documentan los fallos de las versiones 1.1.0 y 0.1.0.

## Olla-DFT 1.1.1, ediciones inglesa y española

| Defecto | Cambio y evidencia |
|---|---|
| O1: falso metal sin bandas vacías | La ausencia de bandas de conducción produce diagnóstico insuficiente y código 2. Verificado sobre el XML del cálculo real `qe-default-scf`, que antes devolvía metal y código 0. |
| O2: mallas y cortes inválidos | Rechaza mallas no enteras o no positivas, cortes no finitos/no positivos y espaciados negativos antes de crear archivos. Diez regresiones de entradas inválidas. |
| O3: convergencia omitida | El informe advierte explícitamente cuando el cálculo no convergió; el comando devuelve código 2. |
| Documentación desactualizada | El generador importa el checkout, evitando tomar la versión del paquete instalado. |
| Cita española incorrecta | Concept DOI español corregido a `10.5281/zenodo.22287496`; antes apuntaba al proyecto inglés. |

Cada edición: **995 pruebas correctas y 1 omitida**, incluyendo 17 regresiones nuevas; pyflakes sin errores. Matriz de GitHub aprobada en Python 3.9–3.13 y construcción del paquete aprobada. Los wheels también pasan `selftest`. Pull requests: [inglés #1](https://github.com/jorgegonzalezsevilla/olla-dft/pull/1) y [español #1](https://github.com/jorgegonzalezsevilla/olla-dft-esp/pull/1).

## Benchmark 0.2.0

| Defectos | Corrección |
|---|---|
| B1–B2 | Conserva los fallos en el conteo y la calificación, los excluye de ganadores; valida muestras esperadas, duplicados, warmups y cobertura QE. |
| B3 | Timeout efectivo con terminación del grupo de procesos; diario de muestras y checkpoints incrementales. |
| B4 | Exige salida correcta, convergencia y JOB DONE de cada QE; compara todas las energías y retiene salida/error de cada repetición. |
| B5 | Comprueba especies, posiciones periódicas, métrica de celda, pseudopotenciales, desplazamientos, ocupaciones y ambos cortes. |
| B6 | Verifica gap, VBM y CBM; compara coordenadas HPKOT. Otras convenciones quedan fuera de la clasificación de rendimiento. |
| B7 | Usa la opción explícita `--kgrid`, eliminando el cálculo auxiliar no medido. |
| B8–B9 | Configuración privada y listado completo de paquetes, junto con hashes del código ejecutado. |
| B10 | El dashboard admite métricas nulas y escapa texto embebido; regresión ejecutada en Node. |
| Adicionales | Valida argumentos, evita regenerar informes antiguos con reglas nuevas, conserva artefactos con hashes, ajusta el script periódico a 15 repeticiones y declara los límites de Docker/CI y de las referencias compartidas. |

Una corrección adicional evita interpretar la ruta de QE como una orden de shell al recoger el entorno. Se aplica después del inicio de la medición completa: no cambia los wrappers, las funciones medidas ni las calificaciones. Los hashes del código de esa medición corresponden al commit `02156eb`; el `bench_git_sha` original refleja que se inició desde un checkout con cambios pendientes.

Los intervalos bootstrap se presentan como descriptivos y condicionados al competidor seleccionado. No se afirma independencia estadística, validez universal ni superioridad de rendimiento.

## Publicación de Olla-DFT

- Inglés: [GitHub 1.1.1](https://github.com/jorgegonzalezsevilla/olla-dft/releases/tag/v1.1.1), [Zenodo 10.5281/zenodo.22313696](https://doi.org/10.5281/zenodo.22313696).
- Español: [GitHub 1.1.1](https://github.com/jorgegonzalezsevilla/olla-dft-esp/releases/tag/v1.1.1), [Zenodo 10.5281/zenodo.22313675](https://doi.org/10.5281/zenodo.22313675).

Los checksums de los wheels publicados están en `wheel-manifest-1.1.1.json` y en los assets `SHA256SUMS` de cada release. El benchmark fija el commit público inglés `d244d96e6ce6aa3ca5669a4fe2cc039ca04b0dc9`, incluido en la versión integrada.

## Medición nueva y validación final

Corrida [20260904-180702](../results/20260904-180702/report.md): **780 muestras medidas + 52 calentamientos**, 15 repeticiones por caso, Olla-DFT 1.1.1. Todas las 210 muestras soportadas de Olla-DFT son correctas. Cero fallos de proceso y `VERIFY PASS` con el verificador 0.2.0. Los **15/15 cálculos QE** convergieron, terminaron correctamente y presentan una dispersión total de energía de **3.00e-08 Ry**.

Olla-DFT sigue siendo más lento en **13/14** casos comparables (media geométrica **1.301×**) y usa más memoria en **14/14** (media geométrica **1.214×**). Estas reparaciones corrigen validez e integridad, sin afirmar una optimización de rendimiento.

Permanecen avisos de gobernador powersave, turbo y carga de fondo. Es una sesión interactiva con otras tareas del sistema y comprobaciones breves, no una medición en una máquina inactiva. No comparar tiempos absolutos entre las corridas antigua y nueva. El coste incluye wrappers, importaciones y muestreo del proceso.

**30 pruebas del benchmark correctas** y pyflakes sin errores. Además, `recheck_fixes.py` ejecuta cuatro casos reales de CLI y confirma los códigos de salida, la advertencia de no convergencia y la ausencia de archivos ante parámetros inválidos; evidencia en `fixed-evidence.json`.
