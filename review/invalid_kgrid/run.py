#!/usr/bin/env python3
# Corre los pasos de este calculo, en orden. Generado por Olla-DFT.
# Hace lo mismo que correr.sh y funciona igual en Windows, donde no hay bash.
import os
import shutil
import subprocess
import sys
from pathlib import Path

PASOS = [('pw.x', 'scf.in', 'scf.out')]          # (ejecutable, entrada, salida)
NPROC_DEF = 4
AQUI = Path(__file__).resolve().parent


def binario(nombre):
    base = nombre
    for suf in (".x", ".exe"):
        if base.endswith(suf):
            base = base[: -len(suf)]
    for cand in (nombre, base + ".exe", base + ".x"):
        hallado = shutil.which(cand)
        if hallado:
            return hallado
        if Path(cand).exists():
            return str(Path(cand).resolve())
    return None


def main():
    np_ = int(os.environ.get("NPROC", str(NPROC_DEF)))
    lanz = []
    if np_ > 1:
        for cand, bandera in (("mpirun", "-np"), ("mpiexec", "-n")):
            if shutil.which(cand):
                lanz = [cand, bandera, str(np_)]
                break
    for exe, entrada, salida in PASOS:
        ruta = binario(exe)
        if ruta is None:
            print("No encuentro '%s'. Instalalo o ponlo en el PATH." % exe)
            return 2
        print(">> %s < %s" % (exe, entrada), flush=True)
        with open(AQUI / entrada) as fi, open(AQUI / salida, "w") as fo:
            r = subprocess.run(lanz + [ruta], stdin=fi, stdout=fo,
                               stderr=subprocess.STDOUT, cwd=str(AQUI))
        if r.returncode != 0:
            print("  fallo en %s (codigo %d). Mira %s." %
                  (exe, r.returncode, salida))
            return 1
    print("Listo.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
