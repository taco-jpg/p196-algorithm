# An exact all-time inductive complement-nine frontier law (Agent X07)

**Label: PAPER PROOF** for the following conditional arithmetic theorem. A small exhaustive control is **COMPUTED**, not a substitute for the proof. No Lean claim or decimal infinite Lychrel certificate.

## The new invariant format

Fix base 10, a nonempty low-first decimal word `A=(a_0,...,a_{m-1})`, `a_{m-1}<=8`, and any integer `L>=1`. Let `H=(9-a_0,...,9-a_{m-1})` in the **same index order** (not reversed) and let `D(A,L)=A ++ 9^L ++ H`. Require the boundary charge `S(A)=sum_i a_i ≡ 8 (mod 9)`. The high digit of `D` is `9-a_{m-1}>=1`, so this is a genuine canonical decimal integer. Denote reverse-and-add by `R` and total width by `n=2m+L`.

**Theorem (exact closure and safety while L>=1):** `R(D(A,L)) = D(A',L')` for a new word `A'` with `a'_{last}<=8`, `S(A')≡8 (mod 9)`, `H'=9-A'`, `m'=m+gamma`, and `L'=L-gamma>=0`, where `gamma∈{0,1}` is the actual decimal leading overflow. The output is **never a palindrome**, including when `L'=0`. As long as `L'>=1`, the theorem may be applied again without any numerical-length cap. Consequently `m_t-G_t` is *identically constant for all such steps*, not just for the previously computed 60,000 steps.

## Proof (elementary finite digit/carry identities)

At the low frontier, the symmetric pair coefficients are `B_i=a_i+(9-a_{m-1-i}) = 9+a_i-a_{m-1-i}`. At the high frontier they appear in reverse order, so their coefficient there is `B_{m-1-i}=18-B_i`. Let the incoming low-frontier carry be zero, and let its outgoing carry be `alpha`. Every central coefficient is 18. Since `(18+c)//10=1` for either `c=0` or `c=1`, the high frontier sees incoming carry **one** for any `L>=1`. Normalize the high coefficients with initial carry one; its outgoing carry is `gamma`.

Pair the two frontier normalizations at equal local indices. Their starting carries add to 1. If their incoming carries add to 1, their pre-normalized coefficients add to `B_i+(18-B_i)+1=19`; therefore their output decimal digits add to 9 and outgoing carries add to 1. Induction on `i=0..m-1` gives a low-output word `U`, high-output word `V=9-U`, and **`alpha+gamma=1`**.

If `alpha=0` (thus `gamma=1`), the first central normalized digit is 8, the remaining `L-1` central digits are 9, and a leading 1 is appended. Set `A'=U++[8]`, `H'=V++[1]`, `m'=m+1`, `L'=L-1`. If `alpha=1` (`gamma=0`), all `L` central output digits are 9 and no leading digit is appended; set `A'=U`, `H'=V`, `m'=m`, `L'=L`. This proves exact whole-word equality, complementarity, and the piston width/overflow law without a simulation.

To preserve the inward guard: in the first case the final digit of `A'` is 8. In the second case, its last digit is `U_{m-1}=B_{m-1}+c_{m-1}-10= a_{m-1}-a_0-1+c_{m-1}<=8`, because its outgoing carry is 1. For the charge, `sum_i B_i=9m`. Digit normalization starting with carry 0 gives `sum_i U_i ≡ -alpha (mod 9)` (each internal carry cancels modulo 9, leaving the final carry with coefficient -10). Thus `S(A')≡8` whether `alpha=1` and nothing is appended, or `alpha=0` and an 8 is appended.

Finally, suppose `D(A',L')` were a decimal palindrome, even if `L'=0`. Comparing its first and last `m'` digits yields `a'_i+(a'_{m'-1-i})=9` for every `i`; summing gives `2S(A')=9m'`. Modulo 9 this forces `S(A')≡0` because 2 is invertible mod 9, contradicting `S(A')≡8`. The input state is nonpalindromic by the same argument. QED.

## Concrete seed and exact scope

For `N_n=10^n-2908` (equivalently `9R_n-2907`), two explicit ordinary steps for all `n` large enough yield at time `t=2`: `A=(2,1,0,8,6)` and `H=(7,8,9,1,3)` (low-first, written as `21086` and `78913`), `L=n-9`, `G_2=1`, `m=5`. Both align indexwise as 9-complements; `S(A)=17≡8`, `a_last=6`. Therefore the theorem proves its complementary piston invariant **at every future step until the nine centre is exhausted**, independently of the 60k numerical observations. In particular it upgrades `AgentX07NinePiston`: the 60k scope is now only needed to calculate the explicit horizon threshold `n>=24884`, not to justify the carry-synchronization itself.

This **does not** prove infinite nonpalindromic evolution of any fixed `N_n`. Indeed `L` decreases by one at each leading overflow and cannot decrease forever; an unbounded strictly increasing integer orbit must acquire infinitely many overflows, so its finite nine core eventually disappears. The search therefore must target **collision/reentry** at `L=0`, where the incoming carry to the high frontier is no longer fixed to 1, or a separate centre-renewal device. The elementary theorem provides a rigorous and reusable pre-collision module for such a format.

## Independent computational control and Lean sketch

`calculation/new_structures/agent-X07/piston_induction_check.py` exhaustively tests all `A` of lengths 1..4 satisfying the charge and last-digit conditions, for `L=1,2,5`. It constructs actual ordinary decimal integers and checks an independent schoolbook addition and the full next complement/charge/size structure, then checks a conditional second transition. **3333** initial states, all passed (overflow 0: 1467, overflow 1: 1866). Reproduce `sh calculation/new_structures/agent-X07/piston_induction_run.sh`; compact counts in `piston_induction_data.json`.

A Lean checker/proof outline needs only a length-indexed digit-list normalization lemma: for coefficient word `B`, `norm(B,0)=(U,alpha)` and `norm(18-B,1)=(9-U,1-alpha)` by induction on list length. The digit-sum modulo 9 identity and two explicit output concatenation branches then prove the theorem. No `sorry`, `native_decide`, axioms beyond existing base arithmetic, or direct Lean build is asserted here.
