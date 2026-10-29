# A 32-state exact dyadic spatial renormalization after fifteen decimal reverse-and-add steps

**PAPER PROOF** (all spatial heights h>=7, at temporal step **exactly t=15**, for an explicitly bounded interior region). The proof uses the previously established all-height 15-step bounded-neutral carry theorem of `AgentN15DyadicFifteenStepNeutralRun`, finite substitution-factor closure, and a new minimal quotient calculation. It neither proves a time-periodic return nor a decimal Lychrel number.

## 1. Defining a height-independent state and its output

Set `A=14`, `B=16`, `sigma(A)=AB`, `sigma(B)=BA`, and `w_h=sigma^h(A)`, L=2^h. Begin with the genuine positive decimal integer N_0(h) whose palindromic *pair-coefficient* word is `P_0(h)=([4]++w_h)++reverse([4]++w_h)`. By the exact all-height result mentioned above, after 15 ordinary reverse-and-add steps its true pairword P_15(h) is obtained by a bounded-neutral local carry transducer applied to the whole dyadic hierarchy, with known decimal overflow sequence `011000010101001`.

Form F, the set of **all length-77 factors** in the four words `sigma^7(UV)`, for U,V in {A,B}. Direct exhaustive construction yields exactly **240 distinct factors**. Since 77<=128=2^7, these factors contain every interior length-77 window of w_h at every h>=7: each window crosses at most two successive sigma^7 letter-blocks, and all four ordered two-letter block types have been admitted.

For a factor f=(f_0,...,f_76) in F, produce a length-75 G segment by the exact third-time bulk coding

```
d(x,y) = 2*(x+y-27)
G_i(f) = d(f_i,f_(i+1)) + d(f_(i+1),f_(i+2))
         - 9*( [d(f_i,f_(i+1))>=10] + [d(f_(i+1),f_(i+2))>=10] ),
          i=0,...,74.
```

Apply the exact bounded-neutral gamma-specific local rule (defined in the earlier paper) at each temporal transition t3,...,t14. To avoid any reliance on unknown neighbours, discard three cells at both ends after *each* transfer. The segment lengths are therefore 75,69,...,3. Every stage has neutral-9 runs of length at most one, as proved by the 240-factor exhaustive check with edge/centre parity classes in the prior theorem. The final length-3 segment's centre is an unambiguous **single decimal coefficient**; denote it `Phi(f)`.

A fixed w_h factor `f = w_h[c-38 : c+39]` is centred at w position c. Its source G segment is aligned to pairword coordinates c-35,...,c+39. Twelve 3-cell shrinks on each side leave P_15 coordinates c+1,c+2,c+3, so the retained centre is **P_15(h)[c+2]**. Thus for every h>=7 and every 38<=c<=L-39, the all-height identity is

```
P_15(h)[c+2] = Phi(w_h[c-38 : c+39]).                 (1)
```

This is an exact level-independent finite-state description, not a fitted similarity between finite trajectories.

## 2. Exact binary substitution on 240 states

For every f in F, let sigma(f) be its literal length-154 substituted word. Define

```
S_0(f) = sigma(f)[38:115]  # 77 letters, centred at output position 2*38
S_1(f) = sigma(f)[39:116]  # 77 letters, centred at output position 2*38+1.
```

The finite checker enumerates all 240 source states and verifies `S_0(f),S_1(f)` both belong to F. Applying sigma to an actual `w_h` window centred at c makes these children precisely the next-height windows centred at `2c` and `2c+1`. Combining this fact with (1) gives, for every h>=7 and every 40<=i<=2^h-37, the exact **spatial scale-doubling equation**

```
(P_15(h+1)[2*i-2], P_15(h+1)[2*i-1])
    = ( Phi(S_0(f_i)), Phi(S_1(f_i)) ),
f_i = w_h[i-40 : i+37].                            (2)
```

Here the spatial offset `-2` in the doubled coordinates is essential; suppressing it would be a false identity. This is a genuine substitution conjugacy for the **time-15 bulk** across successive spatial heights, and is compatible with aperiodic Thue–Morse periods doubling at each level.

## 3. 240 -> 32 finite Moore-machine minimization

The 240 states have only eight output values: `{5,7,8,9,10,12,16,17}`. Regard each state as a Moore machine whose two input letters 0/1 choose child S_0/S_1, and whose observed output is Phi. Two states are equivalent iff their outputs agree after every finite binary child-path. Compute the standard coarsest right-congruence by repeated partition refinement, splitting states with different current output or different child classes. The exact partition counts are

```
initial partition by Phi:                8 classes
first child-aware refinement:           32 classes
second refinement:                      32 classes (fixed point)
```

Therefore the machine has a **minimal 32-state quotient** (with respect to all 240 admissible windows and all binary descendant paths); equality of each quotient class's output and two child classes is checked exhaustively. The resulting `renorm32_quotient.json` includes the *entire* 32-state deterministic 2-uniform substitution: each class has a coefficient label, left-child class and right-child class. `renorm32_states.tsv` gives the complete 240-state source-to-quotient map, 77-letter factor and original child IDs. Both files are regenerated bit-for-bit by `renorm32.py --check`.

For context, the minimal state count at each fixed time t3,...,t15 using this same 240-window factor basis is **6, 10, 10, 10, 10, 14, 17, 20, 22, 22, 27, 28, 32**. These are exact finite-state complexities of the corresponding interior codings; there is no proved bound as t tends to infinity.

## 4. Independently checking the machine on actual decimal integers

The separate C++ source `renorm32_independent.cpp` does *not* use the symbolic pairword step operator: it creates canonical real decimal N_0(h), performs 15 direct digit-vector additions `N+reverse(N)`, then recomputes P_15(h) from opposite decimal digits. For h7,...,h14 it checks **32,032** actual interior P_15 coefficients against Phi of the 77-factor at the correct shifted position. For h7,...,h12 it additionally verifies **15,216 child identities** from the genuine `P_15(h+1)` digits, not just from a symbolic substitution. It independently checks 240 child-factor transitions and every quotient class's well-defined output and descendants. Every admissible factor is observed in genuine h>=9 words; replacing any one source-state output with a different coefficient is detected against its recorded true integer value (240 mutation witnesses).

From the repo root run:

```
sh calculation/new_structures/agent-N15/run_renorm32.sh
```

The runner verifies the existing all-height bounded-neutral carry premise, regenerates the 240-state and 32-state tables exactly, compiles the independent integer checker, and prints both `DYADIC_SPATIAL_SUBSTITUTION_COMPOSITION_PASS` and `RENORM_ORDINARY_DECIMAL_PASS`.

## 5. Precisely what remains missing

Equation (2) is a **spatial** renormalization relating the time-15 words of different initial heights. It is not a time-block renormalization from one single natural-number orbit to itself. A true decimal finite certificate would still need a *temporal macrostep identity* `P_{T(h)}(h) = a translated/phase-corrected copy of P_0(h+1)` (or a more general finite set of template types) with a uniform, mechanically checkable boundary-carry and nonpalindrome condition. Direct equality of arbitrary phase-matched raw words is not supported by pilot data, so the search should target a coupled phase/overflow/centre automaton on these compact 32-state spatial descriptors. This result supplies an exact finite alphabet for that next construction, not a proof that it exists.
