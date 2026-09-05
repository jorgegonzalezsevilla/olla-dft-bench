# Auditoría y correcciones de septiembre de 2026

- [REVISION.md](REVISION.md): auditoría histórica de Olla-DFT 1.1.0 y benchmark 0.1.0; las ubicaciones corresponden al código de entonces.
- [CORRECCIONES.md](CORRECCIONES.md): reparación, validación y resultados nuevos de Olla-DFT 1.1.1 / benchmark 0.2.0.
- `evidence.json`, `metrics.json`, logs y XML: evidencia original, conservada sin alterar los valores medidos.
- `reproduce.py` y `qe_gap_case.py`: reproducciones para el código anterior. No ejecutarlos para sobrescribir esta evidencia desde una versión nueva. Las regresiones actuales están en `tests/test_reliability.py` y en los tests de Olla-DFT.
- `synthetic-incomplete-run/`, `Si_occupied_only.xml`, `Si_unconverged.xml` y los inputs inválidos son controles negativos deliberados. No son cálculos físicos publicables.
