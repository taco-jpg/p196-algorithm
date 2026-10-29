# N26 binary inverse-emitter gate at the last p8/m20 decimal return edge

**PAPER PROOF (conditional all-length necessary condition); COMPUTED (160 independent ordinary-integer witnesses).** This does not prove a decimal Lychrel number exists and is not an 80-edge centre return.

Let B_t and W_t be the rooted p8/m20 rec0 exterior (39 columns) and spatial bulk (20 columns) in calculation/decimal_frontier/lattice_formats/p8_scc.txt, temporal phases t=0,...,7. Coefficients are d_i+d_(n-1-i), least significant first. Suppose a true rooted phase-7 pairword has initial B_7 W_7^q (q>=1), its genuine last-edge overflow gamma_7=0, and the next pairword must contain B_0 W_0^(q+k), k>=1, so that k more spatial bulk copies are restored in the return.

The previously proved all-q rooted port theorem calculation/new_structures/T02/port_contract.py forces the two-ended carry state at the cut after B_7 W_7^q to be (low, high-out)=(0,0) whenever that exterior transition is correct. This theorem is used, not reproduced as new.

**Exact new necessary condition:** the 20k source coefficients immediately inside this rooted exterior are either W_7^k or W_7^(k-1) A, where

    W_7 = [8,11,10,6,8,15,16,11,8,10,10,9,13,1,7,6,7,14,13,6]
    A   = [8,11,10,6,8,15,16,11,8,10,10,9,13,1,7,6,7, 9,13,16].

The only differences A-W_7 are offsets 17:-5 (14->9) and 19:+10 (6->16). An active A emitter must be the FINAL (innermost) source block; two A emitters cannot occur in a clean W_0^k return. At the end of the 20-cell inverse, W_7 leaves low carry 0 and A leaves low carry 1, both with high-facing carry 0.

**Proof, valid for every k:** At one coefficient x in 0..18, let l be the ascending carry and eta the unknown incoming carry from the mirrored high side. The digit-pair output and outgoing carries are

    y = ((x+l) mod 10) + ((x+eta) mod 10),
    l' = floor((x+l)/10),  h = floor((x+eta)/10).

For gamma=0, y is the next pair coefficient. Read outer-to-inner with current state (l,h) and successor state (l',eta). Exhaustively enumerate x in 0..18 and eta in {0,1} across the 20 desired target outputs W_0. The COMPLETE block-transfer table is:

| Input state | Output state | Unique predecessor |
|---|---|---|
| (0,0) | (0,0) | W_7 |
| (0,0) | (1,0) | A |
| (0,1) | (0,1) | D |
| (1,0) | none | none |
| (1,1) | none | none |

where D=[18,11,0,6,18,15,6,11,18,10,0,10,3,1,17,5,17,14,3,6]. Each listed transition has multiplicity one; all others zero. The table is computed exhaustively without caps. From physical state (0,0), choosing A makes state (1,0), which has no further W_0 predecessor; hence arbitrary-k induction gives exactly the two displayed families. This finite proof is independent of any time horizon or centre length.

**Physical local realizability:** Both source alternatives genuinely occur in canonical base-10 integers. For example, for any q,k>=1, take the symmetric phase-7 pairword with half B_7 W_7^q W_7^(k-1) A [0]^12. Its canonical decimal realization has gamma=0 and after one ordinary reverse-add, the pairword begins B_0 W_0^(q+k). A centre whose nearest coefficient is <=8 forces the inward high carry to 0, enabling A. This is a positive one-step local emitter, NOT evidence that an 80-step phase-0-to-phase-0 cycle produces it.

Reproduce from repository root:

    python3 calculation/new_structures/agent-N26/binary_emitter_gate.py

The code uses previously committed exact rec0 rows in the same directory, exhausts the finite carry matrix and checks 160 ordinary Python decimal integer additions n+int(str(n)[::-1]) for q=1,2,5,20; k=1,2,4,8; centre digits 0,1,2,6,8; both source alternatives. The exact missing lemma is a physically reached complete 80-edge or longer interface/centre return with nonnegative drift and an all-phase nonpalindrome invariant. No infinite base-10 result or Lean claim is made.
