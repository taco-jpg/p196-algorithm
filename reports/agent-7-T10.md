# Agent 7 / T10.canonical-8source-controls

**COMPUTED independent positive regression, not a new Lean theorem**.
This audit tests all eight **existing** base-b neutral-band cycle
certificates in their original Lean source against the arbitrary-base
B/C normalization and deterministic trimming developed in Agent 7
drafts #315/#326. It is not a base-10 certificate, nor an exclusion
of any period or width.

Sources are fetched from:

- lean/P196/Drafts/Agent120NeutralBandCalibration/A120PowerTwo.lean
- lean/P196/Agent213KnownBaseMechanisms/KnownBases.lean

Existing certificate checks there are Lean kernel-reduced by decide.
This audit *does not* assert kernel verification of our new
normalization lemmas; it reads existing coefficient lists as data
and independently evaluates the arithmetic.

## Exact verification protocol

For every edge (B,C,B2,C2,u,v) from each listed source:

1. independently normalize B with initial carry 0, C with e1 and
   reverse B with e2; require e1!=e2.
2. independently evaluate raw nextB and nextC for both gamma branches
   and require the full original edge equalities with trailing
   neutral suffix and symmetric neutral center pair trims.
3. strip the maximal neutral h=b-1 suffix of each B source/target and
   maximal paired h ends of every C source/target. Set transformed
   U=u+q_target-q_source and V=v+a_target-a_source.
4. require U,V>=0; independently recompute all three carry bits and
   raw blocks for the normalized source; require every transformed
   edge equality, identical original carry/overflow bits, and
   gamma=1 => U=V=0.
5. require cyclic links (including last edge back to first),
   preservation of sum u and sum v and exact closed length
   identities sum U=sum gamma, 2sum V=sum gamma.

All assertions above are regression-test assertions, *not* an
untrusted input certificate acceptance routine.

## Reproducible command

Run in a full source checkout from the repository root:

    python3 calculation/agent-7/eight_source_controls.py

This is standalone Python standard library, without imports from
neutral_band_search.py, cauto or generic_trim.py. It parses all
certificate edge definitions directly from the existing Lean files.
In a separate execution environment, the corresponding independent
JavaScript mirror fetched those exact source files through GitHub
and checked each edge. It produced:

| Base | Source certificate edges | Sum gamma | Original sum(u),sum(v) | Normalized sum(U),sum(V) | Verdict |
| --- | ---: | ---: | --- | --- | --- |
| 2 | 4 | 2 | (2,1) | (2,1) | PASS |
| 4 | 6 | 2 | (2,1) | (2,1) | PASS |
| 8 | 8 | 2 | (2,1) | (2,1) | PASS |
| 11 | 6 | 2 | (2,1) | (2,1) | PASS |
| 16 | 10 | 2 | (2,1) | (2,1) | PASS |
| 17 | 6 | 2 | (2,1) | (2,1) | PASS |
| 26 | 4 | 2 | (2,1) | (2,1) | PASS |
| 32 | 12 | 2 | (2,1) | (2,1) | PASS |

**56 / 56 edges pass** original and normalized equality checks,
with no positive trims on overflow steps. Different coefficient
lengths include nonempty/empty B interfaces and odd-length C states.

## Scope and limitations

This is a **positive-control** test of exact code and source data:
a general statement cannot be proved solely by enumerating 56
already existing witnesses, and this says nothing about whether
base-10 certificates exist. The general statement remains a
PAPER PROOF in #315 and #326, still requiring independent
mathematical review or future Lean formalization.

No new Lean file, new theorem or decimal candidate was built;
python3 tools/verify.py --changed has not been run in this
environment. Leave the PR DRAFT until checked in a full clone.
