# X07: an exact scalar repunit-quotient renewal format

Labels: **PAPER PROOF** for the arbitrary-`h` scalar recurrence and nonpalindrome safety domain; **COMPUTED** for exhaustive ordinary-integer controls (`h<=6`), the shared `31988` quotient, and all 136 previously discovered renewal bridges. **UNDECIDED** for a self-replicating renewal ladder. Not Lean-verified and not a fixed-seed infinite Lychrel certificate.

## Base-10 arithmetic format (no pairword transducer required)

For any integer `h>=1` and any integer `q` with `0<q<10^h` and `q=2 (mod 9)`, define

    P(h,q) := (10^h - 1) q .

Let `m` be the number of ordinary decimal digits of `q`. Since any power of ten is `1 (mod 9)`, the strict upper bound `q<10^h` and `q=2 (mod 9)` imply `1<=m<=h`, `10^(m-1)<q<10^m`. Put `A=10^m-q` and `R=reverse_m(A)`, where `reverse_m` reverses **exactly m digits including leading zeroes**. The low-first digits of `P(h,q)` are exactly

    digits_m(A) ++ 9^(h-m) ++ (9 - digits_m(A)).

Thus the innermost digit of `A` is `<=8` and its digit sum is `1-q=8 (mod 9)`. A decimal palindrome would force `A_i+A_(m-1-i)=9` for all i, hence `2 sum(A)=9m`; this contradicts `sum(A)=8 (mod 9)`. Therefore **P(h,q) is never a palindrome** for every `h,q` in the stated domain.

Reversing the actual full integer (not merely a digit coefficient word) gives the exact identity

    reverse(P(h,q)) = (10^h - 1) * (1 + reverse_m(10^m - q)).

Consequently **one entire decimal reverse-and-add step is a scalar recurrence**

    F(q) = q + 1 + reverse_m(10^m - q),
    P(h,q) + reverse(P(h,q)) = P(h,F(q)).

This is a **PAPER PROOF for every h, without any minimum-band-width assumption**. Moreover `F(q)>q` and `F(q)=q (mod 9)` (because digit reversal preserves digit sum modulo 9 and `10^m-q=1-q=8 (mod9)`). Therefore if `F(q)<10^h`, the next state remains protected. If `m<h`, then `F(q)<2*10^m<=10^h`, so no transition can leave the format before `m=h`. At `m=h`, compute the scalar guard `F(q)<10^h`. At the first failed guard the format says **nothing** about palindrome safety (e.g. `P(1,2)=18` goes to palindrome `99`). This guard is crucial and prevents an invalid infinite inference.

## One universal quotient for arbitrarily long finite decimal orbits

For every `n>=9`, two ordinary reverse-and-add steps on `10^n - 2908` give exactly

    N_2 = (10^(n-4) - 1) * 31988,
    h = n-4, q_2 = 31988.

Explicitly, with `9^r` denoting a run of r digit characters `9` (not exponentiation), the successive **decimal digit strings** for every `n>=9` are `9^(n-4) ++ "7092"`, `"12907" ++ 9^(n-8) ++ "7091"`, and `"31987" ++ 9^(n-9) ++ "68012"`. Reversing and adding either displayed string gives the next by ordinary column carries. The final string evaluates to `(10^(n-4)-1)*31988`. This proves the uniform two-step entry, not just a sampled pattern. From that point on, **the quotient sequence is independent of n**: `q_(t+1)=F(q_t)` while `q_t<10^(n-4)`. Thus no palindrome can appear in any protected step, including all 20,000 steps of the earlier `n=8297` witness. The initial two states are independently checked directly. For fixed n, strict increase of q means the scalar protected phase is finite; this does NOT prove an infinite orbit.

Independent bigint-versus-quotient checks find the **first unprotected indices** `t=35,106,236` for `n=20,50,100` respectively. They match the previously measured collision times. The exact first exit is a guard failure, not necessarily a palindrome.

## A concrete modular renewal ladder: h=4,6 -> h=8

The `AgentX07CollisionRepair` exhaustive census starts with `h=m=4` or `h=m=6` and an empty central 9-run, then loses the protected format. **All 136 independent positive repairs (not merely the two controls)** re-enter at **h=8** with the quotient still equal to `2 (mod9)`:

| starting h | repairs | recovered h | recovered quotient length m | recovered inner-9 count |
|---|---:|---:|---:|---:|
| 4 | 26 | 8 | 7 | 1 |
| 6 | 73 | 8 | 7 | 1 |
| 6 | 37 | 8 | 6 | 2 |

Two explicit **factor births** after real nonpalindromic bridge sequences:

    94780521 --(19 steps)--> 838016291619837 = (10^8-1)*8380163;
    996508003491 --(7 steps)--> 75454399245456 = (10^8-1)*754544.

Both quotients are `2 (mod9)`. Before the bridge, the seeds have h=4 and h=6; the new larger factor `10^8-1` appears at the protected return, an arithmetic renormalization event not implied by the one-piston recurrence. The bridge safety and every transition were checked by independent ordinary-integer arithmetic in the earlier `AgentX07CollisionRepair` result. **This is not a repeated ladder:** no second valid repair was found in its 200-step exhaustive window; 300,000 random width-8 control starts also showed none through their 100-step pilot, but no global exclusion follows.

## Soundness criterion for an eventual infinite certificate (PAPER PROOF)

A *repunit-quotient renewal certificate* is a family of guarded stage descriptions `P(h_i,q_i)`, one-step scalar dynamics `F` until the first failed guard, and a finite set of **exact, all-parameter decimal bridge identities** mapping each failed-guard state into the next protected stage with `h_(i+1)>h_i`. Every bridge must explicitly certify that all intermediate decimal numbers (including the failed-guard state) are nonpalindromes. If the finite bridge cases cover every reachable residue/state and form a total cycle that strictly increases h, then **the initial integer is Lychrel**: by induction each protected stage is safe, each bridge is safe, and infinitely many stages occur because h strictly grows. This is a sound certificate FORMAT; we have concrete bridges h=4,6 ->8 but **no all-h, indefinitely iterable bridge**, so the decimal instance remains UNDECIDED. A Lean proof could define `padRev m A`, show the reversal identity by `Nat.ofDigits`, and prove the nonpal charge lemma, then check bridge morphisms by a decidable Boolean transfer checker. No unchecked Lean claims are made.

## Reproducibility and exact coverage

Run `sh calculation/new_structures/agent-X07/quotient_run.sh`. `quotient_kernel.py` independently checks **all** guarded q for h=1..6 (123,456 states), including actual decimal reversal identities and short-step palindrome safety; it separately compares scalar and ordinary big-integer orbits for n=20,50,100 through the first failed guard and independently rechecks the h=8 quotient/factor for all 136 earlier repair events. Compact counts and control quotients: `calculation/new_structures/agent-X07/quotient_measurements.json`; it imports the previously committed `renewal_events.json` rather than duplicating 136 records.

Next concrete search direction: synthesize a **second** exact bridge h=8 -> h'>8 by solving an arithmetic quotient and carry-constrained inverse problem. A one-off h=4/6 ->8 bridge is insufficient to prove any decimal Lychrel orbit.
