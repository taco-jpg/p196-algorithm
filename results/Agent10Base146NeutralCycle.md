# Agent10Base146NeutralCycle
**COMPUTED.** A complete four-edge neutral-band reverse-and-add certificate exists in base 146, absent from the repository's previously proved-base list.
Overflow and lower carry streams are `0101`; the exact 80-coordinate exterior cycle and four centre states are in `calculation/neutral_band/agent10_base146/cert_b146.json`.
Initial palindromic centre `[182,45,102,102,45,182]`, neutral coefficient 145, initial band width 12 on each side.
Exact trim counts `(u,v)=(1,0),(0,0),(1,1),(0,0)` and overflows `0,1,0,1` give net band gain `+1` per four-step cycle.
All four arithmetic `norm`/`nextB`/`nextC` edges are independently checked; `B` and `C` return exactly to the start.
Python checks 1,000 actual base-146 big-integer reverse-add steps and full pairword, no palindrome at every step.
Independent C++ ordinary digit-list algorithm checks 20,000 steps, full pairword and no palindrome at every step (final digits 10,190, band width 5,012).
Deterministic generator, explicit JSON data, independent checker, C++ replayer and runner are all under `calculation/neutral_band/agent10_base146/`.
Reproduce from a clean clone: `bash calculation/neutral_band/agent10_base146/reproduce.sh`.
Runner also verifies base-9 period-4 depth-61 and base-13 depth-55/75 exterior SCC positive controls with repository `bauto3.cpp`.
Full exact edge derivation, seed reconstruction and numerical outputs: `reports/Agent10Base146NeutralCycle.md`.
Scope: a base-146 finite neutral-band certificate, not a kernel-checked Lean instance, not an infinite-base family, not a base-10/196 result.
