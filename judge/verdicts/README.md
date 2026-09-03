# Independent verdicts

One file per evaluation, named `<evaluator>_<run_id>.md`, committed exactly as received.
The evaluator follows [protocol/JUDGE.md](../../protocol/JUDGE.md) and works from the packet
`judge/packet_<run_id>.md`. Anyone can produce one; the deterministic cross-check is
`python bench.py verify results/<run_id>`.
