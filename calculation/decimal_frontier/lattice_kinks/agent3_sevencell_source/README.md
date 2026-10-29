# Seven-cell rec2 physical-carry source-cycle classification

C++17 standard library and `sha256sum` only. From repository root:

    sh calculation/decimal_frontier/lattice_kinks/agent3_sevencell_source/run_checks.sh

The primary exhausts the seven-cell 21-bit parity/carry graph via physical 4-cell gluing, reconstructs an actual seven-column state path for every allowed mask, embeds it into a cyclic 48-coefficient word, and writes exactly 97,216 independent 48-byte witnesses to a **generated** 4,666,368-byte file (under 5 MB). The SHA256 is checked before independent validation. The independent checker instead propagates exact sets of 76 physical carry states, builds a different BFS spanning tree, uses opposite-pivot GF(2) elimination, and independently normalizes every 386-digit source word using ordinary base-10 schoolbook addition. It also checks all eight 406-digit rec2 phase controls and wrong-overflow-shift negatives.

Expected graph: allowed masks by length 2..7 = 64, 288, 1312, 5984, 27296, 124512. Seven-cell graph 27,296 vertices, 124,512 edges, six self-loops, connected, 97,217 chords; 48-cycle even space rank 97,216. Independent source witness rank 97,216. Expected generated witness SHA256: `a2d878e8247679cb7e0b70bb2cdd2171678e17c3b193f09fc35a31de1c32d143`.

Local control runs: primary 2.21 seconds/621,076 KB maximum RSS; independent 2.74 seconds/594,928 KB maximum RSS; deterministic primary rerun byte-identical. Full repository `tools/verify.py --changed` is **not claimed** when the local GitHub checkout is unavailable. This classifies source cyclic-word functionals only, not image covariance, a finite-centre exclusion, or a decimal Lychrel certificate.
