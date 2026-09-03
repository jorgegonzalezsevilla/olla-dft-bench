# Fully pinned userland for the benchmark. Does not remove CPU-frequency or thermal noise.
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends quantum-espresso util-linux git && rm -rf /var/lib/apt/lists/*
WORKDIR /bench
COPY requirements.lock .
RUN python -m venv .venv && .venv/bin/pip install --no-cache-dir -r requirements.lock
COPY . .
# docker run --cpus=1 --memory=3g --cpuset-cpus=2 olla-dft-bench run --reps 5 --with-qe --label docker
ENTRYPOINT ["python", "bench.py"]
