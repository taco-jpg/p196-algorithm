# N03: a parameterized eight-step centre bridge for aperiodic decimal pair words

**Claim label: PAPER PROOF (finite-state composition).** The explicit witnesses, concrete whole-integer replays and corrupted-data controls are **COMPUTED**. This is a *finite-horizon constructive result*, **not** a base-10 Lychrel certificate.

## New format: a root path, substitution loops, and a centre bridge

Let \(g=(1,0,1,0,1,0,1,0)\). A column is an eight-tuple \(x_t\in\{0,\ldots,18\}^8\), listing pair coefficients through eight time phases (phase 8 repeats phase 0). Each spatial-cut state \(q=(L,H,Y)\) stores eight lower carries, eight upper carries, and four upper output digits at the overflow-one phases. The full exact schoolbook transition is implemented from scratch in \`bridge_certificate.py\`: for each phase \(t\), choose an upper input carry \(h_t\in\{0,1\}\) and demand

\[
H_t=\lfloor(x_t+h_t)/10\rfloor,\quad
L'_t=\lfloor(x_t+L_t)/10\rfloor,\quad
H'_t=h_t,\quad
Y'_t=(x_t+h_t)\bmod 10\quad(g_t=1),
\]
\[
x_{t+1}=((x_t+L_t)\bmod10)+
\begin{cases}Y_t&g_t=1,\\(x_t+h_t)\bmod10&g_t=0.\end{cases}
\]

The exact root is \(q_{\rm root}=(0,85,4369)\). Our two root paths \(R_0,R_1\), with lengths 45 and 68, reach two distinct boundary cut states:

| seed ID (graph index only) | \(q=(L,H,Y)\) | loop lengths \(|A|,|B|\) | common six-column suffix |
|---|---|---|---|
| 98791 | (89,145,20576) | (92,97) | yes: same in \(R,A,B\) |
| 199884 | (166,110,18745) | (97,92) | yes: same in \(R,A,B\) |

For each row, the two explicit distinct words \(A,B\) are exact return paths \(q\xrightarrow{A}q\) and \(q\xrightarrow{B}q\). There are thus infinitely many legal rooted coefficient half-words \(R\,w_1\cdots w_k\), \(w_i\in\{A,B\}\). The first two columns \(E\) of both loops are also the *centre extension* for one eight-step cycle: \(E_0=(9006D48E,C366D8GF)\), \(E_1=(9IIC5EA4,6FCC5A23)\). Letters A..I encode coefficients 10..18, **not** decimal digits.

## Explicit finite-horizon soundness theorem

Fix either row. For **every** finite word \(w\in\{A,B\}^*\), form the row-0 lower half \(a=[R\,w]_0\) and palindromic pair-coefficient word \(P=a++\operatorname{reverse}(a)\). Split each coefficient \(a_i\) into the two ordinary decimal digits \(\lfloor a_i/2\rfloor\) and \(a_i-\lfloor a_i/2\rfloor\), placing the latter in reverse order on the high side; call the resulting actual integer \(N(w)\). It has \(2|a|\) decimal digits and a nonzero leading digit.

**Theorem (PAPER PROOF, conditional on the finite witness transition identities, all checked by the independent program).** For each \(0\le t\le8\), the *complete* palindromic pair-coefficient word of \(T^t N(w)\), where \(T(n)=n+\operatorname{reverse}_{10}(n)\), is the symmetric completion of the initial \(\lceil(2|a|+s_t)/2\rceil\) columns from time row \(t\bmod8\) of the fixed infinite extension \(R\,w\,E\), where
\(s_t=(0,1,1,2,2,3,3,4,4)_t\). The eight overflow bits are exactly \(10101010\), and none of \(N(w),\ldots,T^8N(w)\) is a palindrome.

**Proof.** The independently checked finite root/loop paths preserve the same full carry state \(q\) after each inserted loop. The written schoolbook equations then prove *every exterior column* simultaneously for all concatenations, including propagation from the actual low-end root. Both loops and the root have the same last six columns, so the central folded carry interface, parities, and the at-most-two newly exposed half-columns during this eight-step interval are *identical*. The central interface is checked on the length-45 and length-68 empty-word seeds by independent decimal digit-list arithmetic; it is preserved under any insertion of whole state-return loops. Since the outside two ordinary decimal digits of the successive numbers are respectively (8,9) for even phases and (7,1) for odd phases, none is palindromic. Induction on \(|w|\) yields the stated identity for arbitrary finite \(w\). No claim is made after phase 8.

This format is more flexible than a single periodic band: the two macros \(U=AB\) and \(V=BA\) have equal length 189, return to the same state and are distinct, hence Fibonacci or Thue–Morse order of \(U,V\) yields genuinely spatially non-ultimately-periodic coefficient bands with an exact **entire-number** eight-step centre bridge at every finite truncation.

## Independent controls and break point

\`bridge_certificate.py\` does not import the original graph engine, nor does it assume any edge exists. It enumerates all admissible high carries for every witness column and checks root/loop closure. Separately it constructs real decimal digit lists and checks the *entire* pairword for all steps 0..8, palindromicity, and all eight overflow bits. It exercises **26 whole-integer controls** (both seeds × 13 empty, periodic, Fibonacci, Thue–Morse, random and equal-length macro arrangements), including seeds 22,000+ digits long. The checker rejects a changed first coefficient of loop B and a wrong boundary carry state for each seed.

The attempted same-format extension through step16 fails consistently at the *first* new central mismatch \(k=|R\,w|+1\), leaving three unchecked half-word columns at that step for each of the 26 controls. That is an exact, local **second-period boundary defect**, not a failure of the aperiodic bulk or a proof that all larger centres are impossible. The next search target is a two-phase (or morphic) **centre defect-state transducer** that can absorb this +1-column mismatch while returning its interface state.

## Reproduction from the repository alone

\`\`\`sh
cd calculation/new_structures/agent-N03
python3 bridge_certificate.py bridge_witness.txt
# Expected: ALL CHECKS PASSED ... 26 independent decimal whole-word tests
\`\`\`

All witness columns are in \`bridge_witness.txt\`. There is **no** claim of a 20,000-step *full* pairword match in this result (the earlier N03 20,000-step runs check a long **exterior prefix** only), and no claim that 196 or any other decimal number has been proved Lychrel.
