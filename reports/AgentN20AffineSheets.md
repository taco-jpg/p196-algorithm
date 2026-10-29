# Agent N20: affine-strip space-time certificates for growing centres

**PAPER PROOF** for the new finite soundness format; base-9 controls are **COMPUTED**. No base-10 certificate and no Lean-verified claim are made.

## Format and exact theorem

Fix integer base b>=2, temporal period T, and common per-cycle length gain G>=0. At time t=qT+p, 0<=p<T and q>=0, a number is given by least-significant-first digits D_p(q,i), 0<=i<n_p(q), with n_p(q)=n_p(0)+Gq. Supply a separate carry-bit word C_p(q,0..n_p(q)).

Each D or C is an ordered finite list of **affine strips**. Strip j occupies a_j*q+b_j <= i < a_(j+1)*q+b_(j+1), with a finite word W_j repeated as W_j[(i-a_j*q-b_j) mod |W_j|]. Every strip boundary has integral slope; adjacent boundaries agree, and slopes and intercepts are nondecreasing. Initial boundary is 0; final boundary n_p(q) for D and n_p(q)+1 for C. Different internal slopes permit two or more expanding centre sectors and moving interfaces, instead of assuming a fixed finite centre between mirrored bands.

For edge p->(p+1) mod T, put q'=q+[p=T-1], n=n_p(q), m=n_(p+1)(q'), gamma=m-n. Require gamma in {0,1} and for every q>=0:
1. C_p(q,0)=0 and D_p(q,n-1)>0;
2. for all 0<=i<n, s=D_p(q,i)+D_p(q,n-1-i)+C_p(q,i) satisfies D_(p+1)(q',i)=s mod b and C_p(q,i+1)=s div b;
3. C_p(q,n)=gamma; if gamma=1 then D_(p+1)(q',n)=1;
4. a fixed integer witness k_p<n_p(0)/2 has D_p(q,k_p) != D_p(q,n-1-k_p).

**Soundness theorem (PAPER PROOF):** If these conditions hold for every phase and length, the numbers defined by D form a real base-b reverse-and-add orbit, and none is a palindrome. Proof: multiply (2) by b^i and sum i from 0 to n-1. Carry terms telescope because C(0)=0; the remaining high term C(n)*b^n is exactly the extra digit prescribed by (3). Therefore val(D_next)=val(D)+val(reverse(D)); (1) preserves canonical leading digits, and (4) makes palindromicity impossible. Induct over temporal phases and q.

## Finite checker proof

All universal checks above reduce to finitely many integer arithmetic cases, including when internal strip widths grow unboundedly. For each edge collect the affine breakpoints f(q)=a*q+b in the source index i from the D and C strip boundaries, reflection of D boundaries n-f, one-index shift of C boundaries f-1, shifted destination-D boundaries at q', endpoints 0 and n, and the witness positions k_p and n-1-k_p.

Let M = lcm of all digit/carry pattern lengths. Define exactly (integer ceiling):

    Q = max(0, max over pairs f,g with f.a<g.a
                  ceil((M + f.b - g.b)/(g.a-f.a)) ).

The checker tests every source index at q=0,1,...,Q+M-1 and every phase. This suffices for ALL q>=0, not merely for the sampled orbit.

Proof of the **affine-boundary residue lemma**: for q>=Q, whenever two breakpoint slopes differ, the higher-slope breakpoint is at least M greater than the lower-slope one. Thus all breakpoint orders stabilize. An interval between adjacent equal-slope breakpoints has constant length. Every interval between different-slope adjacent breakpoints has length at least M and expands (and hence contains every residue class modulo M). Under q->q+M, every breakpoint translates by its integer slope times M, preserving residues of its fixed-width intervals; growing intervals always contain all residues. A strip's symbol depends only on index modulo its word length and the affine left boundary modulo that length. The reflection index n(q)-1-i, carry index i+1, and target-q' shift are affine with integral slopes, so each local predicate depends only on this stabilized interval ordering and index/q residues mod M. Every predicate that could fail at q>=Q therefore has an identical residue/region witness at one of q=Q,...,Q+M-1. The finite check includes q<Q too. The witness positions are explicitly included among breakpoints, so nonpalindromicity and leading-digit conditions receive the same all-q guarantee.

The format accepts only finite affine strips with nondecreasing slopes/intercepts and explicit periodic patterns; it does **not** claim to decide arbitrary morphic/nonlinear centres, retreating boundaries, or arbitrary reverse-and-add orbits. It is an extension beyond fixed-width centres precisely because independent centre-internal moving boundaries are allowed.

## Reproducible controls

Run from the repository root:

    python3 -m py_compile calculation/new_structures/agent-N20/affine_sheet.py
    python3 calculation/new_structures/agent-N20/affine_sheet.py --self-test --control-b9 --replay 20000

The script reads the existing in-repository b9 controls from
calculation/decimal_frontier/lattice_formats/cert_b9_rec0.json and cert_b9_rec1.json; it does NOT duplicate their contents. It derives ordinary normalized digit lists for 3 cycle lengths at every phase from B_t and w_t, independently obtains their integer addition carry words, and infers a stationary cut at index 62 with exactly G=4 new digits/carries inserted per T=10 steps. Both undergo the exact finite arithmetic checker and independent full-digit, ordinary-addition replay, checking the complete predicted digit word and nonpalindromicity at EVERY step.

| Published control | Q | M | q values | exact local digit equations | independent full-digit replay | final digits |
| --- | ---: | ---: | ---: | ---: | --- | ---: |
| base-9 rec0 | 3 | 4 | 7 | 9,716 | 20,000 steps PASS | 8,125 |
| base-9 rec1 | 3 | 4 | 7 | 9,856 | 20,000 steps PASS | 8,127 |

Negative controls: a false stationary base-10 orbit at 21 is rejected; changing one symbol in the expanding digit strip of each base-9 control is rejected. These controls demonstrate that the checker is usable and falsifiable; they do not constitute a new base-9 or decimal Lychrel finding.

## Lean-first roadmap and open decimal direction

The Lean kernel is not available in the local execution environment, so **no Lean files** or Lean-verification claim are submitted. Proposed theorem structure: define structures Aff, Strip, Phase, and functions digit/carry; prove finite_cutoff_sound by the affine-boundary residue lemma; prove step_of_carries by weighted Finset telescoping; prove nonpal_of_witness; combine by induction into lychrel_of_affine_sheet. No sorry, custom axioms, or native_decide are needed in principle, but this sketch is not claimed compiled.

The next constructive task is to infer internal affine velocities and periodic digit/carry phases from a true decimal orbit, including a centre widening at multiple speeds. This result asserts neither existence nor nonexistence of a decimal certificate; a decimal candidate must separately satisfy the full finite checker. tools/verify.py --changed could not be run without a local checkout; code was directly syntax-checked and each control was run locally.