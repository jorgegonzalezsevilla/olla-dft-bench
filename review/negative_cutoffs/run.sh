#!/bin/bash
# Generado por Olla-DFT — ejecuta los cálculos en orden.
# En Windows, o sin bash:  python run.py
set -e -o pipefail
NP=${NPROC:-4}
if [ "$NP" -gt 1 ] && command -v mpirun >/dev/null 2>&1; then
  LANZ="mpirun -np $NP"
elif [ "$NP" -gt 1 ] && command -v mpiexec >/dev/null 2>&1; then
  LANZ="mpiexec -n $NP"
else
  LANZ=""
fi

echo ">> pw.x < scf.in"
$LANZ pw.x -in scf.in | tee scf.out

