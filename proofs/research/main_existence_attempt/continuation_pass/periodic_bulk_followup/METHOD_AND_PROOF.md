# Periodic interiors and an exact guarded whole-word quotient

This follow-up gives an exact finite graph of period-four interior phases, two necessary boundary filters, and an all-exponent quotient for actual finite canonical words. It finds no finite-interface return cycle. Its eleven whole-word probes all stop at the stated path cap and remain **UNKNOWN**. Neither decimal Lychrel existence nor the status of 196 is settled.

The periodic calculations are separate from the frozen `safe_language/` four-state DFA exclusion and the frozen `safe_language_followup/` four-band calculation. No general exclusion of regular or recursive safe languages is claimed.

## 1. Whole-word semantics

Write a canonical numeral in least-significant-first digits as `d_0,...,d_(L-1)`, where `d_(L-1)>0`. Its full mirrored-sum word is

\[
q_i=d_i+d_{L-1-i}\quad(0\le i<L).
\]

Thus `q` is symmetric, takes values in `0,...,18`, has positive outer coefficient, and has an even central coefficient when its length is odd. Conversely, every word with these properties is realized by a canonical numeral: split each pair sum into two digits, choosing a positive most significant digit in the outer pair, and halve an odd-length center.

For the symmetric coefficient polynomial `Q(z)=sum_i q_i z^i`, the ordinary integer `Q(10)` is exactly the reverse-and-add of any numeral realizing `q`. Normalize `Q(10)` into decimal digits and take their mirrored sums; call the result `G(q)`. This is the actual induced whole-word map. Its length is `L+gamma`, with `gamma` in `{0,1}`. All whole-word computations below evaluate this map, including its actual overflow bit.

The exact palindrome-predecessor classification proved in `../../renewal_pass/seam_audit/STATUS.md` is used here: `Q(10)` is a palindrome precisely when either all coefficients of `q` are at most nine, or the outer coefficient is 11 and every coefficient belongs to `{0,11}`. A word outside this set is called **safe**. In particular, an infinite forward-closed family of safe canonical words gives an actual orbit whose subsequent reverse-and-add values are never palindromes. The initial numeral also needs to be nonpalindromic; the concrete probes have outer pair sum 17, which ensures that immediately.

## 2. Exact periodic interior rule

Let `p=(p_0,p_1,p_2,p_3)` be a coefficient block, indexed from the least significant side of a long left band. Indices in this section are modulo four. For a single coefficient `x`, the carry transfer is

\[
f_x(c)=\lfloor(x+c)/10\rfloor.
\]

It is constant zero if `x<=8`, the identity if `x=9`, and constant one if `x>=10`. If `p` contains a coefficient other than nine, the periodic incoming carries are forced independently of the distant boundaries. Let `a_i` be the high/low bit of the nearest preceding non-nine coefficient, and `b_i` the high/low bit of the nearest following non-nine coefficient. Set

\[
d_i=(p_i+a_i)\bmod10,\qquad u_i=(p_i+b_i)\bmod10.
\]

Far enough from either finite interface, the actual whole-word output for a given global overflow `gamma` is

\[
\Phi_\gamma(p)_i=d_i+u_{i-\gamma}.
\]

The one-column shift for `gamma=1` is forced by the appended leading decimal digit. It is not a freely chosen local carry. The graph temporarily retains both possible global clocks because the finite exterior has not yet been supplied.

For the all-nine block there is no non-nine reset. The incoming carry from each side, `a,b` in `{0,1}`, persists throughout the band. The output is the constant block with coefficient `18-9(a+b)`, for either global clock. Both bits are retained explicitly in each graph edge. They have not been shown simultaneously realizable with the exterior or center.

The phases stay indexed; rotations are not identified. Rotation commutes with each `Phi`. For reversal `R`, `Phi_0(Rp)=R(Phi_0(p))`, while `Phi_1(Rp)` is the right cyclic shift of `R(Phi_1(p))`. More directly, if the total old width is `L`, the reflected phase in global indices is

\[
R_L(p)_i=p_{L-1-i},\qquad
\Phi_\gamma(R_L(p))=R_{L+\gamma}(\Phi_\gamma(p)).
\]

The two carry labels are interchanged under reflection for an all-nine phase.

## 3. Complete necessary phase graphs

The initial phase is `V=(14,14,4,4)`. Its two immediate outputs are `(9,9,9,9)` without overflow and `(9,10,9,8)` with overflow. The first branch can retain a mixed-carry nine band or lose it to constant zero/eighteen. The second branch can return through nonconstant phases.

All reachable vertices and edges were enumerated to closure, with no runtime or state cutoff:

| Graph | Vertices | Edges | Strongly connected component sizes |
|---|---:|---:|---|
| Indexed interior phase | 59 | 124 | one of size 56; three singletons |
| Phase and outer coefficient | 878 | 1,458 | one of size 696; three of size 18; 128 singletons |
| Phase, outer coefficient, width modulo eight | 7,024 | 11,664 | four of size 1,392; three of size 144; 1,024 singletons |

The first graph lies in the finite universe of `19^4=130321` indexed phases. The second begins with every outer coefficient `1,...,18`; the third also begins with every width residue `0,...,7`. These are necessary-condition graphs, not orbit graphs of canonical finite words.

For outer coefficient `a` and incoming inner carry `b`, the exact outer rule is

\[
\gamma=\lfloor(a+b)/10\rfloor,\qquad
a'=a\bmod10+\begin{cases}1&\gamma=1,\\(a+b)\bmod10&\gamma=0.\end{cases}
\]

The second graph permits only pairs `(Phi_gamma(p),a')` allowed by this relation. The third also updates `L` to `L+gamma` modulo eight and checks the reflected phase equation. Modulo eight is appropriate for the proposed whole-word template: adding one four-coefficient period on each side adds eight columns when the interfaces return.

### An explicit rejected loop

The interior graph alone contains the seven-step loop

\[
\begin{aligned}
(0,0,18,18)&\xrightarrow{1}(9,0,9,18)
\xrightarrow{0}(9,2,9,16)
\xrightarrow{0}(9,6,9,12)\\
&\xrightarrow{0}(9,14,9,4)
\xrightarrow{1}(14,4,4,14)
\xrightarrow{1}(10,9,8,9)
\xrightarrow{1}(0,0,18,18).
\end{aligned}
\]

Its clock is `1000111`. Repetition forces four consecutive overflows across the join. The exact outer rule permits at most three: its unique three-overflow path is `18 -> 9 -> 10 -> 1`, after which overflow is impossible. Thus this interior loop cannot be a whole-word periodic clock. The failed loop and the complete outer-path calculation are retained as evidence.

### The surviving necessary loop

The following eight-step interior/outer loop survives the outer filter:

| Step | Indexed phase | Outer coefficient | Next overflow |
|---:|---|---:|---:|
| 0 | `(0,9,18,9)` | 17 | 1 |
| 1 | `(10,10,8,8)` | 8 | 0 |
| 2 | `(1,1,17,17)` | 17 | 1 |
| 3 | `(9,2,9,16)` | 8 | 0 |
| 4 | `(9,6,9,12)` | 17 | 1 |
| 5 | `(2,16,16,2)` | 8 | 0 |
| 6 | `(5,13,13,5)` | 17 | 1 |
| 7 | `(10,9,8,9)` | 8 | 0 |

It has four overflows, so two traversals return the total width residue modulo eight. The saved representative consequently has 16 steps and eight overflows. If a finite exterior and center returned with these phases, the repeated exponent would gain one. That hypothesis has not been met.

This loop must also obey the prior maximal-growth boundary restriction in `../../../novel_encoding_analysis.md` section 6, `../../../novel_projective_notes.md`, and `../../../exist_uniform_notes.txt` section 2. A periodic exterior with overflow density one half must follow the exact outer-three cycle

\[
\begin{aligned}
(8,16,16)&\to(17,13,14)\to(8,12,9)\to(17,5,0)\\
&\to(8,13,5)\to(17,6,11)\to(8,14,8)\to(17,8,17)\to(8,16,16).
\end{aligned}
\]

In particular, temporal period must be divisible by eight. Our retained loop meets this divisibility condition and has four temporal alignments with the four states whose outer coefficient is 17. The independent replay checks the eight required prefix edges directly by integer arithmetic and checks those four alignments. It does not infer a finite interface from this compatibility. The previous growth bound and boundary classification are prior work, not new results of this bundle.

## 4. An exact whole-word quotient for arbitrary exponents

For finite blocks `B,H` and a length-four block `w`, define

\[
Q(B,H,w;k)=B\,w^k\,H\,\operatorname{rev}(w)^k\,\operatorname{rev}(B),\qquad k\ge3.
\]

Here `H` is symmetric; an odd-length center has even coefficient. Every coefficient is in `0,...,18`. The first coefficient of `B` is positive when `B` is nonempty; otherwise the first coefficient of `w` is positive. Empty `B` or `H` is allowed. These conditions make every member canonical. The minimal period of `w` need not be four; constant phases are included.

Safety for the whole family is exact and independent of `k>=3`: apply the classification in section 1 to the alphabet of `B,H,w` and the outer coefficient. Every block appears for every such exponent.

### Guard-period lemma

For every state `(B,H,w)` satisfying these conditions, there are blocks `B_raw,H_raw,w'`, computed by the single actual transition at `k=3`, such that for every `k>=3`,

\[
G(Q(B,H,w;k))=Q(B_{\rm raw},H_{\rm raw},w';k-2).
\]

To compute them, let `b=|B|`, `h=|H|`, and let `gamma` be the actual overflow of `Q(B,H,w;3)`. Take the first `b+4` coefficients of its image as `B_raw`, the next four as `w'`, and the central `h+8+gamma` coefficients as `H_raw`. Symmetry supplies the remaining right blocks.

**Proof.** A carry through one copy of `w` is a composition of constant maps and identities. It is therefore either constant or the identity, hence idempotent. The same holds for `rev(w)`. Thus the carry leaving any positive number of copies of a block is independent of that number. In particular, all carries entering the fixed center and exterior blocks, and the final overflow, are independent of `k>=1`.

After a single period from either end of a repeated band, the incoming carry has stabilized. All subsequent complete periods away from the other interface have the same decimal digit pattern. In the mirrored-sum image, no overflow pairs equal original positions and overflow shifts the opposite position by exactly one column. Retaining one complete four-column guard period at each end of each band absorbs both the possible initial carry transient and this one-column displacement. The remaining `k-2` periods have the same indexed four-column image `w'`. Every coefficient in the two guarded exterior regions and in the guarded central region depends only on the fixed blocks and the stabilized carries, not on `k`. Their widths are `b+4` on each side and `h+8+gamma` in the center. These are exactly the regions read at `k=3`, proving the identity. The identity-map case `w=9^4` is included: the boundary carry travels unchanged, so the guards are sufficient there as well. ∎

### Normalization of the quotient state

Strip `u` complete copies of `w'` from the end of `B_raw`. Strip `v` mirrored pairs, `w'` on the left and `rev(w')` on the right, from the boundary of `H_raw`. Denote the remaining blocks by `B',H'`. Then

\[
G(Q(B,H,w;k))=Q(B',H',w';k+\delta),\qquad
\delta=u+v-2,
\]

for every `k>=3`. The exact width balance is

\[
2|B'|+|H'|+8\delta=2|B|+|H|+\gamma.
\]

The exponent on the right is at least one. To iterate the same guard-period lemma, choose the starting exponent large enough that every visited source exponent remains at least three.

This is an actual whole-word quotient. It computes the overflow from the entire canonical word at `k=3` and does not select any interior carries independently. The finite controls at exponents `3,4,7,31` validate the implementation. The proof above, rather than those finite controls, supplies the all-exponent statement.

### A positive criterion, not an instantiated example

Suppose a directed cycle of these normalized states were found, all states safe. Summing the width balance around the cycle gives

\[
8\sum\delta=\sum\gamma.
\]

The overflow sum must be positive. Otherwise the positive outer coefficient strictly increases at every step (`a'=2a+b` without overflow), which prevents a state cycle. Consequently the cycle has positive integer exponent gain. Taking `k` at least three minus the minimum prefix sum of the exponent changes keeps every transition in the lemma's domain; repeated cycles then increase the exponent and remain safe. This would produce an infinite safe canonical family with actual whole-word semantics. No such cycle was found here.

## 5. The eleven recorded whole-word probes

Only the following initial states were examined:

\[
B=(17),\quad w=(0,9,18,9),\quad H=\varnothing\text{ or }(c),\ c\in\{0,2,4,6,8,10,12,14,16,18\}.
\]

The configured limits were 50,000 graph states, 128 transitions per initial path, and `|B|+|H|<=512`. Every path reached exactly the 128-transition limit. Neither the state nor interface limit was reached. All 1,408 stored transitions lead to safe states; no normalized state cycle occurs. The largest stored outer and central blocks have lengths 65 and 85. Initial exponents between 13 and 23 suffice for the entire respective recorded path.

These paths do not preserve the proposed nonconstant bulk indefinitely. Every path reaches constant nine at time 21. Those with centers 0, 2, or 4 reach constant zero at time 22; the other eight reach constant zero at time 26. Constant zero remains the bulk phase for the rest of each recorded path. The finite interfaces still supply safety during the recorded steps. These facts establish finite trajectories only, not an indefinitely protected bulk or an infinite safe language.

The saved symbolic path status `UNKNOWN_INTERFACE_OR_PATH_CAP` is a generic code label; in all eleven actual outcomes the path cap alone was reached. No terminating continuation was sought after this cap. The full states, every transition, exact exponent floor, and terminal state are preserved in `periodic_word_quotient_controls.json.gz`.

The independent checker additionally constructs an ordinary canonical decimal numeral for each initial state at its exact recorded exponent floor. It performs all 128 literal integer reverse-and-add steps, compares every resulting mirrored-sum word with the quotient, and checks nonpalindromicity. All eleven complete decimal trajectories are preserved in `ordinary_trajectories.json.gz`. Their outcome remains **UNKNOWN_PATH_CAP**.

## 6. Independent verification and preservation

`verify_periodic.py` imports no discovery module. It reconstructs each interior edge by decimal normalization scans from both ends of five copies of the phase, trying every exterior carry combination. It reconstructs the outer relation by evaluating canonical three-coefficient polynomials with center 0 or 18. It then checks every saved edge, full reachability from the stated initial set, and all strongly connected components using a separate Tarjan implementation.

The checker also verifies 496 rotation relations, 992 width/reflection relations, all retained cycle witnesses, the rejected clock, and the compatibility with the existing outer-three cycle. It independently evaluates the symmetric coefficient polynomials as ordinary integers for 5,632 controls: 1,408 states at four exponents. Finally it replays 1,408 literal additions across the eleven ordinary trajectories. All checks passed.

Sources, complete compressed graphs, ordinary trajectories, outcome JSON, original run logs, and the independent verification JSON/log are retained. Gzip files use deterministic timestamp zero; result JSON records decoded payload hashes. `MANIFEST.json` records the final files and SHA-256 hashes. No proof of general regular-language emptiness or a Lychrel witness is attached to a capped run or to a necessary-condition cycle.

Reproduce from this directory with Python 3 and its standard library:

```sh
python3 bulk_phases.py
python3 outer_filter.py
python3 width_phase_filter.py
python3 periodic_word_quotient.py
python3 verify_periodic.py
```

The discovery runs overwrite their own result files. To audit a frozen copy without rerunning discovery, use only the final command; it recreates the deterministic ordinary-trajectory archive and verification report. The sibling `../periodic_interface_followup/` owns the subsequent finite exterior/center lift attempt and is outside this bundle.
