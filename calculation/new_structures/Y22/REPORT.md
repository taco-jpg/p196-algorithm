# Y22: paper-folding U-word fixed-collar renewal

**Status: EXHAUSTED-NONE** for the stated architecture. **Label: PAPER PROOF** for the no-go theorem; **COMPUTED** only for the four finite integer controls. The decimal Lychrel problem remains UNDECIDED.

## Exact scope

Let `p_n` be the zero-indexed regular paper-folding word, equivalently `p_n=1` iff the odd part of `n+1` is `1 mod 4`. Code `0` by `A=(9,0,18)` and `1` by `B=(9,2,16)`, and let `V_k` be the first `k` coded motifs. Consider any canonical-admissible rooted p12/m9 pairword with half-word `H=B34 W9^q J V_k`, fixed finite `J` and palindromic finite `C`, and pairword `H C reverse(H)`. The target is an exact 120 ordinary-decimal-step return `V_k -> V_(k+5)` with the same `q,J,C` and physical epoch state and overflow clock `(1000)^30`, for every sufficiently large `k` (and hence for each fixed admissible `q`).

## Proof

The paper-folding bits are the coding of the fixed point of the 2-uniform substitution

`u -> vw, v -> vz, w -> uw, z -> uz`, started at `v`, with `u,w -> 0` and `v,z -> 1`. Its transition graph is strongly connected and has a self-loop, so the substitution is primitive. The paper-folding word and its three-coefficient coding are therefore uniformly recurrent.

The word is not ultimately periodic. Its defining identities include `p_(4n)=1`, `p_(4n+2)=0`, `p_(4n+1)=1` for even `n` and `0` for odd `n`, and `p_(4n+3)=p_n`. If an eventual period `r` were not divisible by four, comparing `p_(4n)=1` with `p_(4n+r)` contradicts one of these four residue-class identities. Comparing `p_(4n+1)` then forces `8 | r`. Writing `r=4s`, the identity `p_(4n+3)=p_n` and periodicity imply `p_(n+s)=p_n` eventually, contradicting minimality of `r`. Thus the word is aperiodic.

For one ordinary reverse-and-add step, the carry map at a pair coefficient `x` is `c -> floor((x+c)/10)` with `c in {0,1}`. It forgets the incoming carry whenever `x != 9`; only a 9 can transmit a carry. Hence a phase sequence with bounded 9-runs has a finite-radius two-sided carry update, including the one-column shift at an overflow phase. A local image of a uniformly recurrent word is uniformly recurrent. If any intermediate infinite bulk phase were periodic, every later phase would remain periodic: a non-all-9 periodic phase has bounded 9-runs and a local update, while an all-9 phase has constant interior carries and also maps to a periodic phase. It therefore could not return after 120 steps to the aperiodic paper-folding bulk. Under the hypothesized return, every one of the 120 bulk phases must consequently be nonperiodic and uniformly recurrent; each has a bounded 9-run. The full 120-step bulk update is thus finite-radius.

With `q,J,C` fixed and the same epoch/collar state restored, that finite-radius update makes the next five motifs adjacent to the centre a deterministic function of a finite suffix of `V_k` and a finite carry/phase state. There are finitely many such states. Iterating the macro therefore produces an ultimately periodic motif sequence. But the required sequence is the aperiodic paper-folding word. Contradiction. Thus no fixed finite collar can realize this literal-prefix `V_k -> V_(k+5)` return under the stated 120-clock.

## Independent genuine-decimal controls

`paperfolding.py` compares ordinary arbitrary-precision `N + reverse(N)` with an independent LSD-first schoolbook digit-array engine at every one of 120 steps for `(q,k)=(20,20),(40,40),(80,80),(160,160)`. In all four, the actual overflow clock is exactly `(1000)^30`, there are 30 overflows, no state at `t=0..120` is a palindrome, and the target pairword is not restored. These finite controls corroborate the setup only; the no-go is the finite-state proof above, not extrapolation from four widths.

## Finite-state collar extension

The same proof allows the collar/centre to vary among finitely many bounded-length modes, provided the epoch update of that mode is deterministic and the literal-prefix condition is retained: include the mode in the finite suffix state. The generated word is still ultimately periodic. Thus a finite periodic seam/centre cycle does not evade the obstruction.

## Not claimed

This excludes fixed finite collars and any bounded finite-state collar/centre family under the stated clock. It does not exclude genuinely growing or nonlocal collars, a non-finite-state seam law, another overflow clock, a different U-word mechanism, or decimal Lychrel existence.
