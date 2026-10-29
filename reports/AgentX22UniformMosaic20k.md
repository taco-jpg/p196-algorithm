# Agent X22: all-Q Markov mosaics surviving 20,000 decimal steps

**COMPUTED (reference guards); PAPER PROOF (uniform all-Q finite-time implication).** This is not a decimal infinite-orbit certificate, is not Lean-verified, and does not solve 196.

## The new all-Q theorem

Use the 12,800 closed 20-cell Markov carry tiles T on port (1,1,4) and the exact 39-cell root B0 from `AgentX22TwoStepCoalescence`. Given Q>=600 and any arbitrary tuple of Q tiles, form the canonical number with palindromic coefficient word B0 ++ t1 ++ ... ++ tQ ++ reverse(tQ) ++ ... ++ reverse(t1) ++ reverse(B0). The theorem is:

**For every Q>=600 and every tuple in T^Q, N_0, N_1, ..., N_20000 are all nonpalindromic. There are 12800^Q different canonical initial integers, each of length 78+40Q digits.**

This theorem has an exact **finite-horizon** conclusion, not an inference of infinitely many safe steps from a long trial.

## Proof (finite numerical premise, all-Q algebraic lift)

Previously proven in the X22 two-step theorem, at t=1 every tile tuple produces the same *pairword* for its Q: K ++ W1^Q ++ [8] ++ reverse(K ++ W1^Q), with K of length 39. Odd coefficients in B0 and K exclude palindromes at t=0 and t=1. The integer at t=2 is completely determined by that pairword.

The independently established universal periodic-lattice insertion theorem in `results/AgentN10UniversalPumpLemma.md` states: for the published eight-phase rooted B_t, W_t, if P is B_t ++ W_t^r ++ C ++ reverse(W_t^r) ++ reverse(B_t), r>=1, C **any** palindromic centre, inserting another W_t at both ends after the 39-position cap commutes *exactly* with a genuine decimal reverse-add step, including overflow. It is a one-step all-centres identity, not a finite approximation. Here use this existing lemma, do not attribute it to X22.

Our new independent guard computation uses the exact literal Q=600 seed, ordinary decimal digit arrays, and a second whole-integer GMP engine for every state at t=0..20000. At each t=1..20000 both independently find the exact rooted B_(t mod8) in the first 39 pair coefficients, and a **contiguous** W_(t mod8) word beginning at index 39 extending at least **7455 coefficients** before the first mismatch. Taking r=1 (or any number of full 20-column repeats within that prefix) gives an exact palindromic central remainder. Each of the eight B phases has at least one odd coefficient, and the reference never reaches a palindrome. Reference initial length: 24,078 digits; final: 34,078. All 11 reported reference length/anchored-prefix checkpoints agree exactly across independent engines; lowest anchored prefix is 7,455 coefficients.

At t=1, the expression for the first pairword of Q+1 is exactly the insertion I_1 of that for Q. By the universal insertion identity and the Q600 guard, induction proves that the Q+1 orbit pairword at **each** t=1..20000 is I_t applied to the Q orbit pairword, and remains guarded. Iterate this finite algebraic induction Q-600 times, preserving the odd-prefix nonpalindrome witness at every step. The central paired residual can be arbitrary and growing; no bounded centre or periodic centre is assumed. The t=0 witness B0 is independent of all tile choices. Thus the statement applies to all positive integers Q>=600 and **all** 12800^Q seed choices, not merely to tested examples.

Caution: neither the N10 insertion identity nor the finite reference guard says the reference stays in its guarded language for all time. There is no induction beyond t=20000 and no decimal Lychrel proof.

## Exact reproduction and controls

Run `sh calculation/new_structures/agent-X22/guard_run.sh` with Python3, g++ C++17 and libgmpxx. It deterministically regenerates the 24,078-digit mosaic seed (SHA256 `2b40b36c364423c31e886445b3a5f5244fa04991727d37123cdfe04620f2002d`), independently constructs eight B phases using ordinary Python big integers, runs two independent complete 20,000-step arithmetic engines, checks every B_t coefficient and *anchored* W_t prefix, rejects every palindrome, and compares checkpoints byte for byte. `guard_20k.json` gives compact guards. Separate ordinary Python big-integer differential check Q600 vs Q601 checked the entire 32 consecutive pairwords (t=0..31) against the published insertion map.

Search direction after this finite result: identify a **regeneration macrocycle** restoring or increasing the minimum anchored W-band length before the observed defect front consumes it. Positive-entropy backward fibres and forward pumping alone do not supply that missing central renewal.
