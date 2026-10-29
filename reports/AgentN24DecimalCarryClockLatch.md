# Agent N24: A two-column carry-clock certificate format for decimal reverse-and-add

**PAPER PROOF (conditional soundness); COMPUTED controls.** This is a NEW **projected carry-port FORMAT**, not a closed decimal certificate: the perpetual physical carry source remains unproved. It sharpens the hybrid objective by separating the non-palindromic boundary latch from all complex central/lattice dynamics. A complete finite certificate in this format would consist of a finite, sound proof/checker that a real decimal orbit supplies the required one-bit carry clock; the boundary nonpalindromicity would then be automatic. The proof does not assert that such a finite source checker has yet been found.

## The exact state projection

For a nonzero decimal number `N` of length `n >= 4`, write its symmetric *pair coefficients* `P_j = digit_j(N) + digit_{n-1-j}(N)` (least significant digit first, range 0..18). Reverse-and-add equals the ordinary base-10 normalization of this symmetric coefficient word. Let `u` be the incoming carry *at position n-2*, the second-most-significant pair coefficient when normalizing P from low to high. Let `p=P_0`, `x=P_1`, `c1=floor(p/10)`, `v=floor((x+u)/10)`, `gamma=floor((p+v)/10)`, `a0=p mod10`, `a1=(x+c1) mod10`, `h0=(p+v) mod10`, `h1=(x+u) mod10`. Then the next word's first two pair coefficients are EXACTLY

* If `gamma=0`: `(p',x')=(a0+h0,a1+h1)`.
* If `gamma=1`: `(p',x')=(a0+1,a1+h0)`.

This follows digit by digit: the uppermost new digit is `h0` for no overflow or the added leading `1` for overflow; the second mirrored partner is respectively `h1` or `h0`. No assumption about any intervening pair coefficient is required beyond the **actual** single carry `u`. Both formulas are valid for all `n>=4`, and `n` can increase.

## Decimal carry-clock latch theorem (PAPER PROOF)

Let `N_{t+1}=N_t+rev10(N_t)`, `len(N0)>=4`, and `(P_0(N0),P_1(N0))=(17,5)`. At every **odd** time `t=2k+1`, let `u_k` be the **actual carry into position len(N_t)-2** during normalization of the symmetric pair word of `N_t`. Assume the infinite carry source obeys

`u_k = (0,0,1,1)[k mod 4]` for all `k>=0`.

Then **every N_t is nonpalindromic**, so `N0` is a base-10 Lychrel number.

**Induction / finite table:** Define `x=(5,6,8,13)` and `y=(13,14,16,12)`. At time `2k`, `(P0,P1)=(17,x[k mod4])`. Either possible incoming upper carry has the same result at time `2k+1`: `(8,y[k mod4])`, with overflow `gamma=1`; actual new outermost digits (low,high) are `(7,1)`, so this odd-time number is not a palindrome. At odd times, `P0=8` and `P1=y>=10` forces no overflow and highmost normalized digit 9; the formula with `u_k` gives `(P0',P1')=(17,2(y-10)+u_k)=(17,x[(k+1) mod4])`. For even times, pair coefficient `P0=17` is odd, whereas any palindrome's paired digit sum must be even, hence even-time numbers are not palindromes. Lengths cannot shrink in reverse-and-add, so the assumption `n>=4` remains valid. QED. The four exact input/output rows are `x:5,6,8,13`, `y:13,14,16,12`, `u:0,0,1,1`, next `x:6,8,13,5`.

**Sound finite-source certificate rule:** An independently checked arithmetic transducer, finite grammar inclusion, or inductive template may prove the one-bit equality `u_k=(0011)[k mod4]` for **every** odd time of an explicit integer seed. Combining that finite source proof with the above fixed four-state latch proves an infinite decimal Lychrel orbit. Merely printing a long finite trace is **not** such a proof; in particular this report does NOT provide one. Compared to an exact whole-pairword cycle, the source obligation is only one physical carry bit each second step.

## Actual decimal trace + independent controls (COMPUTED)

Using the previously committed `p8_hybrid_data.json` seed, the **schoolbook digit-list oracle** computes full `N_t` for `t=0..20000`, and independently computes `u_k` by sequentially carrying the **actual** `P(N_{2k+1})` coefficients all the way from digit zero to the penultimate position. Exactly **10,000/10,000 actual odd-time carry ports** match `0011` periodic, and the projected `(P0,P1)` phase agrees at *all 20,001 checked times*, with no palindrome. The full final decimal SHA-256 is `e3e9530f676dbb4adb69d94ad127fa7079bfdf54251fcc839b7db55aa8cbfa71`, identical to the independent ordinary-bigint replay in `AgentN24P8HybridShortSeed`. For all the 20,000 computed steps, the earlier result shows that the rooted period-8 lattice remains intact for 256 coefficients, so this is a **finite-lived** physical carry source, not a closed perpetual clock.

A separate test constructs 30,000 random 10-digit nonzero decimal numbers with random `P0 in 1..18`, `P1 in 0..18`, carry bit `u in {0,1}` forced exactly by symmetric coefficient `P2=0` or `18`, and checks the projected formula against **independent full digit-list reverse-and-add**. All 30,000 trials pass. The positive controls also verify all eight halves of the four-state latch table directly with both choices of irrelevant even-phase input carry.

## Code and exact commands

`calculation/new_structures/agent-N24/carry_latch.py` contains the self-contained finite projected transducer, paper-theorem row checker, 30k physical controls, and the digit-list 20k physical carry-source replay. `carry_latch_evidence.json` records all checkpoints and final SHA. Source input is the existing `p8_hybrid_data.json` in the same directory. Reproduce from repo root:

```sh
cd calculation/new_structures/agent-N24
python3 carry_latch.py p8_hybrid_data.json 20000 > /tmp/carry_latch_evidence.json
python3 reproduce_p8.py 20000
```

No Lean proof is claimed. Lean sketch: define the projected two-cell `edgeStep` with `p,x,u`; prove `edgeStep_sound` from division/modulo of the full pairword normalization, including overflow; define `clock : Nat -> Bool` with period4; close `latch_even`/`latch_odd` by case splits and `decide`; the induction theorem takes as a premise an **actual orbit carry-source relation** at every odd time. That premise needs a separate, genuinely finite source certificate before applying it to an infinite decimal orbit.