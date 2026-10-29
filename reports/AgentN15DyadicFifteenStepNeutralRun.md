# A 15-step all-height decimal dyadic construction using bounded-neutral carry transport

**PAPER PROOF**, exact finite scope: all h>=2 and only times 0..15. No Lean result, infinite certificate, or assertion about 196. A new uniform two-ended carry-locality format extends `AgentN15DyadicSevenEdgeLocality` through eight further temporal transitions, even though coefficient 9 occurs in the bulk.

## 1. All-height family and the new carry rule

Let `sigma(14)=14,16`, `sigma(16)=16,14`. With `w_h=sigma^h(14)` and `H=[4]++w_h`, define the palindromic decimal pairword `P_0(h)=H++reverse(H)` (least-significant coefficient first). Choose the positive genuine decimal N_0(h) whose first and final digits are 0,4 and whose other opposing digit pairs are `(w_i-9,9)`. Thus its initial pairword is exactly P_0(h). As previously established, three exact steps give a uniform `P_3(h)=G_h++reverse(G_h)`, with `G_h=[1,0,14,5]++` a 3-letter sliding-block code of w_h, plus one exceptional final coefficient. The exact formulas for those three steps are in `AgentN15DyadicSevenEdgeLocality` and independently reimplemented here in `ca_bounded.py`.

For an arbitrary base-b palindromic pair-coefficient word P of length n, normalisation emits a carry bit c_i into position i. A coefficient exactly b-1 transmits the incoming bit; any coefficient other than b-1 fixes the outgoing bit to `a(P_i)=floor(P_i/b)`. **Bounded-neutral carry lemma:** if no two consecutive coefficients equal b-1, then the carry into an interior cell depends only on the preceding one or two pair coefficients. By symmetry, the carry into the mirror-partner cell depends on the succeeding one or two coefficients, with a one-position shift if the output length increases. This statement is exact in every base and is proved directly from column arithmetic, not inferred by simulation.

For b=10, let `C_left(i)` be a(P_(i-1)) when P_(i-1)!=9, else a(P_(i-2)); define `C_right(i)` by checking P_(i+1), else P_(i+2), and `C_shift(i)` by checking P_i, else P_(i+1). For positions far from the ends and centre, if the normalised integer has **no final overflow** (`gamma=0`), the next lower pair coefficient is

```
Q_i = ((P_i+C_left(i)) mod 10) + ((P_i+C_right(i)) mod 10).
```

When **one new most-significant digit appears** (`gamma=1`), the reflected partner is the previous cell and

```
Q_i = ((P_i+C_left(i)) mod 10) + ((P_(i-1)+C_shift(i)) mod 10).
```

These identities remain correct when the current coefficient is 9. They are a finite-radius (`<=2` index dependence, with a safe 3-position truncation margin) time-inhomogeneous cellular transducer, not a stationary periodic-centre assumption. At the finite ends and centre the actual digit-normalisation formula is used; no bulk rule is extrapolated across the reflection seam.

## 2. Universal finite substitution-factor check

Our aim is to verify **for all h>=2** the fixed overflow schedule

```
gamma_0,...,gamma_14 = 0 1 1 0 0 0 0 1 0 1 0 1 0 0 1
```

and that no two consecutive neutral 9 coefficients occur in `P_t(h)` for every source time t=3,...,14. Once these conditions hold, the local rule gives each next exact pairword by induction. At step15 there can be **two consecutive 9s**; the theorem intentionally stops there, without excluding continuation by a radius-three rule.

For t=3 the interior of G_h is a three-letter sliding-block function `J(u,v,w)` of the Thue–Morse letters. Each application of the bounded-neutral rule reads at most two preceding and two succeeding coefficients. For certainty, our finite checker discards three coefficients at each end of a trial bulk window per step. From t3 to t15 are 12 steps, so a length-77 original w factor suffices (`77 - 2 - 6*12 = 3` interior output coefficients remain). Because 77<=128=2^7, every length-77 factor of `w_h=sigma^7(sigma^(h-7)(14))`, for **any h>=7**, lies across at most two adjacent 128-letter sigma^7 blocks. Therefore it appears in the union of the factors of `sigma^7(UV)` for U,V in {14,16}. The union has exactly **240 distinct length-77 factors**; the concrete code enumerates them all, derives P3 from the original three-letter coding, applies the gamma-specific two-ended local update, and checks that the input contains no adjacent 9s at every t3..t14. This is a complete universal factor test, **not a sample over h**.

The only locations not represented by bulk windows lie in bounded exterior and mirrored-centre neighbourhoods. The total 12-step safe dependency radius is at most 36 original coefficient positions; including the P3 coding and an exterior margin of 44 requires at most 83 original Thue–Morse letters. For h>=10, the first 128 letters of w_h are always sigma^7(14); its last 128 letters are sigma^7(14) or sigma^7(16), depending solely on the parity of h-7 (since the final letter toggles under sigma). Therefore all exterior and centre source windows at **every h>=10** belong to exactly two finite classes, represented by h=10 and h=11. Their exact digit arithmetic establishes the gamma schedule, nonneutral roots and absence of consecutive 9s near each endpoint and the centre. The eight smaller heights h=2,...,9 are checked in full. The code additionally compares h12 and h13 against their boundary-parity representatives (redundant controls only). This is an elementary finite-cone induction for the entire unbounded family.

At each time the bulk and both boundary conditions together establish the next step's carry formula and the maximum neutral-run bound. The induction gives **15 exact ordinary decimal reverse-and-add pairword steps for every h>=2**. The finite-factor source is `ca_bounded.py`, the compact allowed-value tables, gamma schedule and digit witnesses are in `ca_bounded_data.json`.

## 3. Uniform nonpalindrome witnesses

N_0(h) has unequal least/most-significant digits 0 and 4 by construction. For N_t (1<=t<=15), compare its normalised decimal digit array with its reverse. Each t has an unequal pair within the first six positions, determined by exactly the same finite exterior carry windows (h>=10 two parity classes, h2..9 individual checks). The first mismatch triples `(lower-side index, low digit, high mirror digit)` for h>=3 are

```
t1  (0,4,5)   t2  (0,9,1)   t3  (0,0,1)
t4  (1,0,1)   t5  (2,8,9)   t6  (1,2,3)
t7  (1,5,6)   t8  (0,6,1)   t9  (0,7,8)
t10 (0,5,1)   t11 (1,5,6)  t12 (0,2,1)
t13 (5,7,8)   t14 (0,6,7)  t15 (0,3,1)
```

For h=2 only the t13 *first* mismatch changes (to `(3,6,7)`); it is still unequal. These are uniform digit-level witnesses, not an inference that nonpalindromicity extends indefinitely.

## 4. Independent arithmetic and reproducibility

A separate C++ implementation `ca_bounded_independent.cpp` constructs the N_0(h) digits and advances **ordinary decimal integers** by direct digit-vector `N+reverse(N)`, recomputing all pairwords at each step. For h=2,...,18 and 15 steps, it checks the complete overflow schedule, no palindromes, absence of consecutive neutral 9s in each P_t for t3..t14, and **6,290,677 actual interior coefficient identities** against a *separately implemented* bounded-carry rule. It also rejects 192 one-digit mutations of predicted coefficients. It does not import the Python symbolic engine or use any pre-saved orbit trajectory. The Python checker independently replays h2..11 as control and verifies all 240 universal substitution-factor windows. Thus both the universal finite-factor argument and a plain-integer independent implementation are available.

Run from repository root:

```
sh calculation/new_structures/agent-N15/run_bounded.sh
```

The runner regenerates and verifies the committed JSON evidence and executes the independent C++ digit-list checker, returning `AGENT_N15_15_STEP_ALL_LEVEL_LOCAL_CERT_PASS` and `INDEPENDENT_DECIMAL_BOUND_RUN_PASS`. This new **bounded-neutral transfer format** is a practical search ingredient for hierarchical bands. A future infinite proof would require a time-dependent renormalisation edge mapping one entire dyadic block to a next-scale template, preserving a nonpalindromic witness for *all* temporal blocks. No such infinite closure is established here.
