# P8/rec0 T14 refund ledger

**Label: PAPER PROOF. Scope: necessary length ledger only; not a Lychrel certificate.**

Let q and k count 20-coefficient W and V blocks in the half-template, and let c be the total finite-collar length, excluding the fixed centre. Each 80-step p8 epoch has 40 genuine decimal length overflows, so the half-template grows by 20 coefficients. Therefore every such edge satisfies

20 Δq + 20 Δk + Δc = 20.

The known T14 160-step emitter, viewed as two 80-step edges, has net change

(Δq, Δk, Δc) = (+1, -8, +180).

Now suppose a subsequent 160-step recharger restores the exact collar length and does not produce another W20 copy: Δc_R = -180 and Δq_R = 0. Its half-template grows by 40 coefficients, hence

20 Δk_R - 180 = 40,

so **Δk_R = +11**. Thus a full-macro collar-returning recharger with fixed q must add eleven V20 copies, not merely eight. Combined with the emitter, the 320-step cycle would have net change (+1, +3, 0), consistent with the required half-template growth of 80 coefficients.

There is also a shorter, distinct repair target if the known path is interrupted after its first 80 steps. That first edge has (+1, -4, +80). A second 80-step edge with Δq = 0 that restores the collar length must satisfy 20 Δk_R - 80 = 20, so Δk_R = +5. The combined 160-step transition would then have net (+1, +1, 0).

These are necessary conditions, not sufficient constructions. The actual T14 second 80-step edge has (0, -4, +100), and no recharger satisfying either target has been found. A candidate must also reproduce the exact seam and centre, both carry ports, the clock, and a non-palindrome guard.