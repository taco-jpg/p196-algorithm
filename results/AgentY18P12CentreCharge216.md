# AgentY18P12CentreCharge216

**PAPER PROOF (all widths and band counts).** Let W_t be the published base-10 period-12/spatial-9 lattice row, B_t its rooted exterior, and T_t(q,C) = B_t ++ W_t^q ++ C ++ reverse(W_t)^q ++ reverse(B_t), where C is any legal palindromic pairword centre.
**Theorem:** If an ordinary decimal reverse-and-add orbit has pairwords T_t(q,C) and T_t(q+k,C') separated by 72k steps, then sum(C')-sum(C) = -2k sum(W_t) (mod 9), regardless of centre width or intervening carries.
**Proof:** Every pairword P_s represents N_s+reverse(N_s), so sum(P_s) = 2N_s (mod 9). Also N_(s+1) = 2N_s (mod 9); because 2^(72k) = 1 (mod 9), endpoint pairword coefficient sums agree. Subtract the two templates: exterior sums cancel, and the two inserted bands contribute 2k sum(W_t).
**Published-row evaluation:** The twelve sums sum(W_t) (mod 9) alternate 6,3. Thus sum(C')-sum(C) = 6k for even t, and 3k for odd t, modulo 9.
**All-width obstruction:** If centre charge is preserved (including C'=C or a permutation), then 3 divides k. Neither a 72-step nor 144-step unchanged-centre regenerative return can exist; the earliest modularly admissible return is 216 steps, without any claim that such a return exists.
**Search redirect:** Backward centre reconstruction must seek a 216-step charge-preserving macrocycle, or explicitly transfer the nonzero centre charge needed for a shorter repair.
**Scope:** A necessary condition only, not a full decimal certificate, a proof of a 216-step centre, or a base-10 Lychrel existence theorem. Not Lean-verified.
**Code and independent checks:** calculation/new_structures/agent-Y18/charge_contract.py. Reproduce with python3 calculation/new_structures/agent-Y18/charge_contract.py: all twelve phase charges, k=1..12, and four 144-step ordinary Python-bigint orbits.
