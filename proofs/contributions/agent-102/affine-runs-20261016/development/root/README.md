# Root proof-development history

These are verbatim source and output snapshots of actual compilation attempts.
The local driver records exact commands, source SHA-256, exits and elapsed time.
Attempts 001 and 003 fail in proof scripts; their original source and errors are retained.
Attempt 002 repairs the endpoint proof, 004 completes the five-module core, and
005 adds the finite coefficient checker without changing the frozen core.
All project modules were built into a newly created directory with --trust=0.
Compiled .olean/.ilean files are reproducible build outputs and are excluded.
The Lean runtime and original download are excluded; the official version and
download evidence are retained separately. Paths in historical receipts describe
the environment actually used, not portable assumptions for a future machine.
