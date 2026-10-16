# Carry-aware encodings between bases

This research note proves exact local encoding identities. It does **not** prove a decimal Lychrel number exists. No novelty claim is made.

## 1. An affine encoder preserving carries

Let source base be b, target base be B, and let integers a≥1,u≥0 satisfy

    a(b−1)+2u=B−1.

Encode a source digit d as E(d)=ad+u. If the source pair sum is s and the incoming carry is c∈{0,1}, the outgoing carry is k=floor((s+c)/b). Then

    floor((as+2u+c)/B)=k.

Proof: if s≤b−2 the target sum is at most B−a≤B−1; if s=b−1 the target sum is B−1+c; and if s≥b it is at least B−1+a≥B. Both additions have carries in {0,1}.

Writing d′=s+c−bk for the source output digit, the target output digit is exactly

    D′=a d′+2u+(1−a)c+(ab−B)k.

For a whole word this formula applies at every old digit position. If there is a leading overflow, both outputs append 1. The separate leading position must not be assigned the affine encoder automatically.

## 2. Dilation and the precise two-step obstruction

If u=0 and a=(B−1)/(b−1), the difference from the encoded output is

    δ_i=(a−1)(c_{i+1}−c_i).

Let C(z)=Σ c_{i+1}z^i, and let M be the output length. Pad C to degree M−2. Including the leading overflow correction, δ(z)=(a−1)(1−z)C(z).

At the next reverse-add, the old defect contributes

    δ(z)+z^(M−1)δ(1/z)
      =(a−1)(1−z)[C(z)−z^(M−2)C(1/z)].

Thus that entire defect cancels precisely when this padded carry polynomial is palindromic.

For the proven binary family

    x_m = 10 · 1^m · 01 · 0^m,   m≥3,

one step has C(z)=z^m+...+z^(2m+1). Binary-to-decimal dilation a=9 therefore gives

    δ=8z^m−8z^(2m+2),
    δ+Rδ=8(z^m+z^(m+3)−z−z^(2m+2)).

These four interface charges do not cancel. In particular, the negative charge at index 1 changes a target mirrored sum from 9 to 1. This resets a decimal carry where the binary carry transmits through a neutral run, so simply retaining the source carry state at the second step is incorrect.

## 3. Centered encoders and carry tags

The choice a=1,u=(B−b)/2 is available when B−b is even. Its output simplifies to

    D′=d′+(B−b)(1−k).

Binary→decimal: E₀(d)=d+4, followed by E₁(d′,k)=d′+8(1−k).

Base4→decimal: E₀(d)=d+3, followed by E₁(d′,k)=d′+6(1−k).

At positions where the mirrored outgoing source carries are complementary, the two carry tags have constant total B−b. Consequently the next target mirrored sum agrees with the centered encoder's mirrored sum. A failure of complementarity contributes exactly

    (B−b)(1−k−k_reflected)

to that next mirrored sum. For the proven base4 family

    10 · 3^m · 323 · 0^m · 00,

whose six-step source evolution increases m by one, the carries are complementary throughout the long annuli. The exceptional exterior and central interfaces still have to be solved. This observation does not establish a closed encoding of the full finite word.

There is also an orientation-reversing local encoder d↦u−d, u=(B+b−2)/2, provided the incoming target carry is 1−c. Its outgoing carry is 1−k and its output digit is

    b−1−d′+(B−b)k.

This gives a possible domain state for an alternating encoder; a finite decimal word still needs an exterior interface producing the prescribed incoming carry.

## 4. Concrete candidates and what failed

The direct centered binary seed is not a Lychrel number:

    54554 → 100099 → 1090100 → 1101001 → 2102012.

The last word is a palindrome. The direct centered base4 seed likewise fails:

    4365633 → 7731267 → 15352644 → 59977995.

For a two-digit binary alphabet, the affine base100 encoders with exterior mirrored sum 8 are

    (0,1)↦(10,89), (21,78), (32,67), (43,56).

They share the same initial outer clock on the stable binary family:

    8 → 17 → 8 → 16 → 7 → 15 → 6 → 12 → 3 → 6 → 13.

Thus their uncorrected exterior interfaces leave the desired 8↔17 clock at the third transition. The experiments here did not find a two-step or four-step alternating full-word identity. A valid result would still need an explicit finite set of exterior and central interface states, a closed return-time transition for all m, and nonpalindromicity at every intermediate decimal step.

## 5. Verification

`novel_encoding_CarryEncoder.lean` contains ten kernel-checked local carry/output lemmas for centered, dilated, and orientation-reversing encoders. It compiles with Lean4.19.0 and `import Std`, without `sorry` or custom axioms. The audited output theorems use only `propext` and `Quot.sound`.

`novel_encoding_carry_conjugacy.py` checks the general affine identities against independent integer arithmetic for every nonzero source word of length at most six in bases2 and4, using every positive-slope affine digit encoder into decimal. It also checks the displayed binary defect identity for m=3,...,34, and the source base4 six-step identity for m=0,...,24. These computations validate implementation and examples; the general encoder proof is the case argument in section1.

## 6. A stronger obstruction, and a corrected constructive target

The later exact prefix calculation is more informative than the uncorrected encoders.

Restrict the outer mirrored-sum clock to8→17→8. For the first three mirrored sums q=(q0,q1,q2), allow the carry from the entire unobserved interior to be either0 or1 at every step. This gives a graph of722 states. Successive deletion of states with no remaining successor leaves99 states. Its only cyclic strongly connected component has the following eight states, in forward order:

    (17,13,14), (8,12,9), (17,5,0), (8,13,5),
    (17,6,11), (8,14,8), (17,8,17), (8,16,16).

The maximum distance along any infinite path to that cycle is15. Each state in the cycle has one viable successor. Thus an indefinitely maintained outer8↔17 clock eventually forces this entire three-pair clock. In particular, a periodic maximum-speed exterior must have period divisible by8. The executable exact finite-graph analysis is `novel_encoding_critical_clock.py`. This graph result is not yet a Lean theorem in this package.

Using the critical outer clock also completely settles two specified neutral-band searches:

* Period12, six overflows: the full exterior graph has576 states,64 at spatial depth1 and512 at depth2, with no transition to depth3. Its temporal-rotation quotient has106 states and192 edges.
* Period8, four overflows: the full exterior graph has244,768 states and263,552 edges; no neutral-band connector is reachable. Independently, the exact temporal-rotation quotient has61,242 states and66,060 edges, again with no connector.

The quotient uses cyclic permutation of identical two-step time segments, an automorphism preserving both transitions and the neutral accepting predicate. These results apply to the specified periodic exterior ansatz, not to every decimal orbit.

The next compatible concrete positive target combines an8-step exterior with a12-step three-letter bulk/center cycle, giving a24-step return and growth by two bulk repetitions on each side. There are30 eligible bulk phases in the earlier exact central-interface data after imposing the digit-sum congruence. The new bounded exterior search `novel_encoding_phase24_boundary.py` gives:

* Maximum boundary width8 at every phase: all30 instances UNSAT.
* Maximum boundary width16 at every phase: all30 instances UNKNOWN at a1.5-second solver limit.

No candidate was produced. The local boundary rule was independently checked against full exact q arithmetic on2,000 random words. An UNKNOWN result supplies no mathematical impossibility evidence.

One width16 case was subsequently resolved: for bulk(2,8,8), direct CaDiCaL bit blasting gave UNSAT in4.08seconds (13,653 Boolean variables,59,603 clauses). The original Z3 batch still consists of30 recorded UNKNOWN responses; this additional run resolves one of those instances, not all30. No larger-width search was run.

## 7. Reproduction and dependencies

Use Python3 and Lean4.19.0. The first three Python checks below use the standard library. The bounded24-step search additionally requires `z3-solver` (tested with5.1.0). Run from the directory containing these files.

```sh
lean-runtime/lean novel_encoding_CarryEncoder.lean
python3 novel_encoding_carry_conjugacy.py
python3 novel_encoding_critical_clock.py
python3 novel_encoding_critical_exterior.py --segments 6
python3 novel_encoding_critical_exterior.py --segments 6 --no-quotient
python3 novel_encoding_critical_exterior.py --segments 4
python3 novel_encoding_critical_exterior.py --segments 4 --no-quotient --states 300000
python3 novel_encoding_phase24_boundary.py --validate
python3 novel_encoding_phase24_boundary.py --width 8 --timeout 1500
python3 novel_encoding_phase24_boundary.py --width 16 --timeout 1500
```

The critical exterior graph imports `continuation_theory_multigrowth.py`, which imports `continuation_theory_graph.py`. The24-step search imports `continuation_brown_boolean.py` and `family_search_bulk_periods.py`, and reads `carry_invariant_research_centers_results.json`. Its `--validate` mode reconstructs canonical decimal numerals from randomly generated mirrored-sum words, performs ordinary integer reverse-add, and compares the entire needed prefix with the local boundary formula.

The optional command `python3 novel_encoding_phase24_cadical.py` reproduces the single additional SAT-backend check. It imports `outer_invariant_cadical.py` and `outer_invariant_brown72.py`, and uses `cadical` on PATH, or the executable specified by the `CADICAL` environment variable. For example, set `CADICAL=/absolute/path/to/cadical` when running the command. Its runtime limit is30seconds.

Proof status must remain separated:

1. **Lean checked:** ten local encoder carry/output identities only.
2. **Exact finite computations in ordinary Python:** critical-clock graph and its15-step transient bound; complete period8/12 neutral-interface graph closures. These are not yet kernel-certified theorems.
3. **Bounded SMT/SAT:** width8 UNSAT, width16 mostly unresolved, with one width16 UNSAT case from CaDiCaL. No independently checked UNSAT proof certificate was generated.
4. **Original decimal existence question:** unresolved. There is no full finite-word alternating encoder or surviving finite decimal seed with an all-time proof in this work.
