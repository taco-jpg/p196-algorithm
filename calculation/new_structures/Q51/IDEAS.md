# Q51 T* red-team findings

**Redirect:** Q03 and downstream users must tighten the universal overflow first-contact row 18 -> 9 from `cL:any` to `cL=0` before relying on the general table. This correction is proof-critical; it does not refute the T* specialization, whose actual physical carry is `cL=0`.

The published `reports/Q03FirstContactInterface.md` row `18 -> 9` states `cL:any, cU:any, dU=0`. Counterexample: the symmetric pairwords
- `P=[10,18,18,9,6,10,6,9,18,18,10]`, representing canonical N=99996500991;
- `R=[10,18,9,9,6,10,6,9,9,18,10]`, representing canonical M=99996500091.

The first lower difference is j=2, 18 -> 9, with mirrored j'=8, outer neighbor P[j-1]=18 != 9, and actual incoming carries (cL,cU,dU)=(1,0,0). Both ordinary reverse-and-add steps overflow to 12 digits, but their successor pairwords are:
- R(N): `[1,10,18,8,16,7,7,16,8,18,10,1]`;
- R(M): `[1,10,8,9,16,7,7,16,9,8,10,1]`.

They first disagree at index j=2, contradicting the published row. For 18 -> 9, the low carry must be cL=0; cU may be either bit and dU=0. The local T* gate table remains consistent because its physical 18 -> 9 gate has cL=0.

Reproducer: `python3 calculation/new_structures/Q51/audit_q03_first_contact.py`.
