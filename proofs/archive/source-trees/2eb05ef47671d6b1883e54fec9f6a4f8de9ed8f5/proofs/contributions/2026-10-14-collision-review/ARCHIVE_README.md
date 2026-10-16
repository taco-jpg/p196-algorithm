# Restore the complete driver trace before replay

The exact 29,648,893-byte gzip trace is stored as five ordered raw parts
because the connector rejects requests exceeding 16 MiB. No trace records
were omitted. The parts reconstruct the original gzip bytes, not a newly
compressed approximation. The retained archive index records every part
hash, the whole compressed hash and the 50,997,008-byte decoded trace hash.

From the repository root, run:

```sh
python3 proofs/contributions/2026-10-14-collision-review/restore_driver_trace.py
python3 -B proofs/contributions/2026-10-14-collision-audit/verify_driver_trace.py
python3 -B proofs/contributions/2026-10-14-driver-family/check_family.py
```

The first command creates the `driver_trace.bin.gz` path used by the proof,
the generation script and all checkers. It verifies each part and both
complete byte streams using only the Python standard library. Add
`--decompress` to also write the full `driver_trace.bin`.

Whole compressed SHA-256:
`6431d3a11008f81e9249f05187e207a73f9f1dc0e87c897e46030f2a16b02404`.

Whole decoded SHA-256:
`bb3e02a3b1f14278eaad67a7242aa56352516fd7434e59198a71fef9b5f2d7ab`.

The complete trace is finite evidence. Its 10,000 driver states do not
establish infinite safety or settle the orbit of 196.
