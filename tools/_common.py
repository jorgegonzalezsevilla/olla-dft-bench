import json, sys, gzip

def emit(d):
    print("@@RESULT " + json.dumps(d, sort_keys=True))
    sys.stdout.flush()

def unsupported(reason):
    emit({"unsupported": True, "reason": reason}); sys.exit(3)

def read_ev(path):
    V, E = [], []
    for line in open(path):
        if line.strip() and not line.startswith("#"):
            p = line.split(); V.append(float(p[0])); E.append(float(p[2]))
    return V, E

def open_xml(path):
    return gzip.open(path, "rb") if path.endswith(".gz") else open(path, "rb")

HA_EV = 27.211386245988
