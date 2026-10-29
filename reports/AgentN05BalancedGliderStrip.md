# Translating-defect strip certificates (agent-N05)

**PAPER PROOF of a conditional certificate-format theorem and the length-budget identity.** Not LEAN-VERIFIED. No base-10 glider cycle or Lychrel number is asserted.

## 1. A glider strip, not a fixed central kink
All words use LSB-first *pair coefficients* in 0..2b-2 (base b), and tilde means reversal. A phase state has the palindromic word
```
P_t(a,c) = A_t ++ U_t^a ++ D_t ++ V_t^c ++ C_t ++
           rev(V_t^c) ++ rev(D_t) ++ rev(U_t^a) ++ rev(A_t)
```
where C_t is a finite palindromic cap, U_t and V_t are whole repeat blocks, and D_t is a finite, *translated* defect/front. In the decimal same-lattice construction, U and V are phase-aligned periods of the same spatial lattice (m=9 or 20 or 48), so the two repeat counts encode the defect's moving location and its independent distance from the centre. The format also permits different U,V and nonzero phase residues tracked in the finite state. A cap may itself be a separately certified symmetric filler; the cap's existence is not assumed or claimed for the decimal instance. This is a *target* format, not a discovered instance.

An edge t -> t+1 specifies gamma_t in {0,1}, integer counter updates a'=a+alpha_t, c'=c+beta_t, finite data of the next state, and a finite two-sided carry-window witness. The finite blocks may change over an edge but return after T edges. Negative intermediate alpha/beta are allowed only when every intermediate buffer remains above its certified cutoff. The net counter gains after the cycle are nonnegative.

## 2. Exact finite carry tiles
For a coefficient p_x, the lower and upper mirrored carry bits ell_x, h_x and their normalized digits satisfy
```
ell_(x+1) = floor((p_x+ell_x)/b),  u_x = p_x+ell_x-b*ell_(x+1)
h_(x-1)   = floor((p_x+h_x)/b),    v_x = p_x+h_x-b*h_(x-1).
```
At interior cells, if the length overflow is gamma in {0,1}, the next pair coefficient is exactly
```
p'_(x) = u_x + v_(x-gamma).
```
At the finitely many endpoint/centre cells, use ordinary full-word normalization; do NOT apply the interior formula past its domain. Each tile checks the two carries, both emitted digits and the next coefficient, with the true leading overflow and centre parity.

For any repeat word W, its forward one-bit carry map f_W is either the identity (all symbols b-1) or a constant (at least one symbol not b-1); the same holds for rev(W). Proof: each one-cell carry map is identity for p=b-1, constant 0 for p<=b-2, or constant 1 for p>=b, and compositions of constants/identities are constant or identity. Therefore a repeated band has a finite stabilizing boundary carry after at most one whole period. Its interior digit output is periodic after the first copy.

## 3. Finite strip acceptance and soundness
Require (A) one exact seed edge P_t(a0,c0)->P_(t+1)(a0+alpha,c0+beta), including overflow, and explicit endpoint validity; (B) for insertion of **one full repeat period** in either buffer and its mirrored copy, a finite carry tile whose input and output carries agree outside the insertion neighbourhood and whose emitted pairword is exactly the corresponding next-state insertion, for BOTH possible input carry bits wherever they are not forced; and (C) the same insertion commutation after either or both buffers have been pumped once. The insertion is placed in the stable interior, with at least two complete periods guarding every finite boundary. These are finite checks: all carry alphabets have two states, and one-period source/target words are finite; test the gamma=0/1 partner alignment explicitly. Conditions (B,C) are stronger than merely checking four isolated lengths.

**Strip pumping lemma (PAPER PROOF).** Under (A-C), every edge identity holds for ALL a>=a0,c>=c0 (respecting intermediate-cut bounds). Proof: decompose normalization into sequential one-bit carry transducers. Insertion at a stabilized periodic cut has the same incoming/outgoing carries in both word orientations, so all digits outside the inserted intervals are unchanged except index translation. The gamma-shifted mirrored partner has the checked periodic output tile inside the insertion. Thus normalization followed by pair formation commutes with adding a period to either buffer. Apply this commuting-square identity repeatedly from (A), independently in the two counters. The full-word finite endpoints were checked in (A).

**Cycle theorem (PAPER PROOF).** Suppose every edge of a finite strip cycle is accepted as above, the finite phase state returns, both total counter gains are >=0, intermediate counters stay above cutoffs, every phase template has an odd coefficient (therefore no represented number can be palindromic), and the initial palindromic coefficient word has a positive leading coefficient and even centre coefficient when its length is odd. Then the first represented positive integer is Lychrel in base b. Proof: realize each coefficient as a sum of two digits with a nonzero leading digit; at an odd centre use half its even coefficient. The pumping lemma proves each step of the real reverse-and-add orbit has the next accepted template. Repeat cycles indefinitely using nondecreasing counters. If a number were a palindrome, every pair coefficient would be twice one digit, contradicting the phase's odd coefficient. This makes an exact finite certificate format; existence of accepted edges is UNDECIDED for base 10.

Lean sketch: define `PairWord`, `CarryTile`, `InsertLeft/Right`; prove `norm_append`, `band_carry_sync` by the 2x2 Boolean carry cases; prove `tile_commutes_insert` on the finite tile, then `edge_pump_left` and `edge_pump_right` by induction; use `lychrel_of_cycle`-style chain induction and an odd-coefficient nonpalindrome lemma. No Lean theorem was written, compiled, or verified.

## 4. Exact length budget, a constructive SAT search target
For m-digit U and V, a cycle whose finite blocks return and whose counters gain (delta_a,delta_c) obeys
```
Gamma=sum_t gamma_t = |P_T|-|P_0| = 2*m*(delta_a+delta_c).
```
This is an exact integer identity, irrespective of carries. A **balanced moving glider** pumps both buffers once (delta_a=delta_c=1), so Gamma=4m and the defect travels m digits inward while the centre advances 2m digits. The outer buffer behind the glider and the inner buffer ahead both grow. This is not the stationary-centre update (1,0).

Decimal p12/m9 g=100010001000 has Gamma=3 per 12 steps: first balanced horizon T=144, Gamma=36, defect drift +9, centre drift +18. Decimal p8/m20 g=10101010 has Gamma=4 per 8: first balanced T=160, Gamma=80, drift +20. Decimal p8/m48: first balanced T=384, Gamma=192, drift +48. Shorter cycles may exist with phase residues or nonuniform counter gains; these numbers concern precisely the full-block balanced format.

In the independently replayed N05 p12 packet (COMPUTED, distinct result `AgentN05DecimalMovingPacket`), the changed support has already expanded to 78 occupied sites in offsets [-23,59] at step 144. It therefore fails to be the desired 144-step returning finite-width glider. This redirects the SAT search toward a **wider but recurrent diagonal strip** rather than a fixed central window, and does NOT exclude such strips.

## 5. Reproduce necessary arithmetic
```sh
python3 calculation/new_structures/agent-N05/balanced_glider_periods.py
```
Expected outputs are the three horizons in `calculation/new_structures/agent-N05/balanced_horizons.json`; the script independently compares two literal pair-word length formulas over nine buffer-count controls. This script checks the necessary length budget only, not the finite carry tile witnesses or any full certificate.
