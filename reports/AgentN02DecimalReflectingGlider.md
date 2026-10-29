# Agent N02: a transient reflecting centre for the decimal p8 travelling defect

**Label: COMPUTED** (exact finite replay). This is a second positive centre structure, not an exclusion. No infinite base-10 Lychrel number or Lean-verified theorem is claimed.

## Construction and why it is different

Start from the first period-8 / spatial-period-20 decimal rooted lattice in `calculation/decimal_frontier/lattice_formats/p8_scc.txt`, exactly as in `reports/AgentN02DecimalGlider20000.md`. In least-significant-first lower-half pair coefficient coordinates, let `B_0` be the length-39 rooted prefix and `W_0` the length-20 recurring spatial block. New **47-cell centre suffix**:

`C = [8,13,14,8,9,17,16,8,5,7,1,8,4,14,12,10,1,9,0,4,18,1,17,9,10,14,3,10,4,14,1,0,5,5,4,1,7,9,17,11,5,4,7,6,10,8,4]`.

For each positive q use `A_q = B_0 ++ (W_0)^q ++ C`. Form the symmetric pairword `A_q ++ reverse(A_q)` (even length) and canonical **actual decimal** seed by setting the low digit `d_i=min(A_q[i],9)` and its opposite high digit `d_{n-1-i}=A_q[i]-d_i`. This gives `n=2(39+20q+47)=172+40q` genuine decimal digits. At phase t define the exact front `J_q(t)` as the first mismatch of the lower-half pairword with infinite reference `B_t ++ W_t^infinity`, or the halfword length when no mismatch exists. All comparisons use real arithmetic, not a simulated symbolic certificate.

A deterministic search seeded with a previously replayed active-centre suffix mutated individual coefficients, inserted/deleted coefficients, and selected longer prefix-survival candidates. The reported suffix is a concrete reproducible result, independently replayed, not a claim of global optimality. The front for this suffix, relative to `J_q(0)` at t=0, has the following verified **non-monotone** offsets (for q=1,2,3,5,8,12): at t=88: **0**, t=176: **+1**, t=264: **0**, t=352: **+1**, t=440: **-7**. A centre can therefore temporarily stop and reverse the earlier inward glider drift, even with the same period-8 lattice exterior. It does not maintain outward motion forever.

## Independent smaller-seed arithmetic controls

`glider_reflect_independent.py` reads the original tracked `p8_scc.txt`, constructs the **number** independently, computes ordinary Python arbitrary-precision `N+int(str(N)[::-1])` at every time, rejects any palindrome, validates overflow `10101010`, and reconstructs the pairword and the first mismatch with the reference lattice. For each `q in {1,2,3,5,8,12}` it observed exactly `first_bad_step=88q+412` at spatial coefficient 38 (q=1→500, q=2→588, q=3→676, q=5→852, q=8→1116, q=12→1468). Relative to the bare seam first failure `88q+4`, this suffix adds exactly **408 steps** in every tested case. This measured affine formula is not asserted for all q.

## Independent 20,000-step GMP control

For q=224 the seed has **9,132 decimal digits**, 66 fewer than the preceding bare-seam q=228 seed. `glider_reflect_replay.cpp` includes the previous complete, independently checked `glider_replay.cpp` support functions; it executes each actual decimal reverse-and-add step in two fully independent engines, GNU GMP (`mpz_class`) and a separate digit-list schoolbook algorithm, comparing the entire resulting number at **every iteration**. Every input is tested for being a palindrome; every generated pairword is checked against the exterior and maximal matching periodic bulk. Every overflow follows `10101010`. All of the first **20,000 steps passed**, and the resulting integer has **19,132 digits**. The last pre-step match front at step 20,000 is index **67**, compared with 54 for the previous 9,198-digit bare-seam candidate. Continuing the SAME seed, the first loss of the claimed pairword exterior occurs exactly at **step 20,124, column 38**; this is not a claim that the integer becomes a palindrome there.

The checkpoints at step 5k / 10k / 15k / 20k are lengths 11,632 / 14,132 / 16,632 / 19,132 and first-front values 3,476 / 2,339 / 1,203 / 67. Corresponding FNV64 trace checksums: `11627441376575543699`, `4888327442568017363`, `2620931701426065987`, `3701112320307447811`. FNV is a deterministic regression marker, not a cryptographic proof. `glider_reflect_data.json` holds the exact suffix and expected outputs.

## Reproduce from a repository checkout

```sh
sh calculation/new_structures/agent-N02/glider_reflect_run.sh
```

The shell command runs independent Python integer controls, compiles the GMP+schoolbook 20,000-step replayer (requires `g++`, `libgmpxx`, `libgmp` and development headers), verifies all checkpoints, and confirms the separate exact step-20,124 exterior failure. Its final line is `N02_REFLECTING_CENTRE_20000_GMP_STEPS_PASS`. Both full replay and integrated shell checks passed locally against source-equivalent lattice fixtures. The C++ source includes the **already committed** `glider_replay.cpp` and the Python source imports the **already committed** `glider_independent.py`; there are no untracked inputs. A full repository `tools/verify.py --changed` run could not be performed without a checkout, so none is claimed.

## Constructive next goal

Model the finite time-t centre as a composition of a freely growing defect region and one or more **reflection gates**. A reusable gate must restore or advance the spatial exterior frontier by at least 20 cells each 88-step window, indefinitely. The measured alternating front offsets 0,+1,0,+1 and subsequent -7 show transient reflection without sustained production. An automatic sequence or multi-gate composition could be searched by symbolic carry-language preimages, rather than restarting a bounded kink census. The infinite decimal case remains **UNDECIDED**.
