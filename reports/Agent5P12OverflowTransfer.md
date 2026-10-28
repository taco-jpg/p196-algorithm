# Overflow-phase complete bulk defect transfer for the decimal p12/m9 lattice

**PAPER PROOF.** This proves an all-bulk-width **one-step** finite-support classification for the three `gam=1` temporal phases `t=0,4,8` of the published base-10, p=12, m=9 absorbing lattice (`data/lat_p12m9.txt`). It is the overflow counterpart of `Agent5P12BulkCollisionTransfer`, which settled the nine `gam=0` phases. It neither constructs nor excludes a centre orbit or a decimal Lychrel certificate.

## Exact carry-transfer identity

A pair-coefficient word P is palindromic, with every coefficient between 0 and 18, and realizes an ordinary decimal numeral. Let O be its grade-school base-10 normalization with **final carry 1**, so O has length `n+1` when P has length n. The next pair coefficient at lower index i is

    S_i = O_i + O_(n-i).

The reflected partner of lower position i is original upper position `n-i`, which is the mirror of **lower i-1**, not of lower i. This one-place reflection shift is why the no-overflow transfer cannot be reused unchanged.

At lower site i, define `q_i=P_i`, spatial residue `r=(i-34) mod 9`, and baseline pair target S_i. Scan *from exterior toward centre*. A modified coefficient word Q must use the same symmetric replacement x at lower i and upper `n-1-i`; remember the **previous** modified coefficient `v=Q_(i-1)`. Let a be modified incoming lower carry into i and b be modified outgoing upper carry after normalizing the upper site `n-i` (that upper site has coefficient v). Guess its incoming carry u∈{0,1}. The exact constraints are:

```
b = floor((v+u)/10),
(x+a) % 10 + (v+u) % 10 = S_i,
a_next = floor((x+a)/10),
b_next = u,
v_next = x,
r_next = (r+1) mod 9.
```

Each edge chooses x∈{0,...,18} and u∈{0,1}, with no omitted cases. Thus the transfer graph has at most `9*2*2*19=684` states `(r,a,b,v)` per temporal phase. The row/carry targets are exactly periodic in r across the safe bulk: every lattice row has non-9 symbols resetting carry at most two cells from both boundaries; this is also independently checked against complete normalized words across both length parities and three 9-period translations.

A finite bulk-supported defect means the first changed symmetric site and all later changed sites lie safely inside the periodic bulk, with at least two unchanged cells before the centre and the original exterior unchanged. Start each residue at its original lower carry, original upper outgoing carry, and original preceding coefficient. Require the FIRST replacement x to differ from q_i; subsequent x may equal q_i. An accepting path is a return to the original `(a,b,v)` at a later cut. Acceptance constructs a valid whole-word collision because the lower/upper carry boundaries and previous coefficient align with the unchanged exterior/centre. Conversely, any such finite-support collision must reach an accepting baseline cut: after the last coefficient difference, the lattice's non-9 reset sites erase carry differences in at most two additional cells, and the previous-coefficient memory is already restored. Therefore exhaustive reachability of these at-most-684-state graphs decides the existence of a finite-support collision at EVERY compatible bulk width, not only at a sampled length.

## Complete decision

| Temporal phase | All impossible first-defect residues r | Viable first-defect residues r |
|---|---|---|
| t=0 | 7 | 0,1,2,3,4,5,6,8 |
| t=4 | 4 | 0,1,2,3,5,6,7,8 |
| t=8 | 1 | 0,2,3,4,5,6,7,8 |

Every positive start has a shortest accepting path of length **two**; only its first site is changed and its second selected coefficient equals the baseline. This recovers all 24 previously published one-site invisible substitutions from `Agent5P12AllPhaseKernel` as **controls**. The new all-width conclusion is the impossibility of *any finite collection of bulk-supported differences* beginning at residues (0,7), (4,4), or (8,1), even though more complicated multi-site replacements were allowed without a width cap.

The complete positive motifs for phase t=0 are the two-step selected coefficient sequences `(r:x_i,x_(i+1))`:

```
0:(14,18)  1:(9,4)  2:(13,8)  3:(17,1)
4:(10,15)  5:(6,4)  6:(13,0)  7: none  8:(14,5)
```

At t=4 and t=8 these motifs translate cyclically by three lattice positions per four time steps, as enumerated by the reproducer. They can be placed at arbitrarily translated sites in sufficiently long physical pair words with the published exterior and either parity of the centre. The three excluded start residues are proved impossible by the *complete graph reachability search*; the exclusion is stronger than the old result that no **single-site** change worked there. It does not assert the positive motifs are unique among longer paths.

## Reproduction and checks

Run from the repository root:

```
python3 calculation/decimal_frontier/lattice_kinks/code/k2_overflow_transfer.py
```

`k2_overflow_transfer.py` imports the sibling `k2_gate_extension.py` (already on main), reads the checked-in lattice data, and executes an uncapped complete BFS for all three phases and all nine spatial residues. It checks every one-step arithmetic edge, verifies periodic row/carry identities at lengths 400,401,418,419,490,491, and independently constructs realizable canonical decimal digits for every positive motif at lengths 200,201,210,211,400,401,418,419,700,701,1800,1801 with multiple spatial translations. Full next pairword equality is checked three ways: the coefficient normalizer with the *actual overflow digit*, independent schoolbook digit-list reverse-and-add, and separate Python big-integer conversion plus reverse-and-add at selected lengths 200,400,701,1800. All checks pass. For excluded starts the BFS exhausts all reachable states (one explored nonreturn state at each excluded residue) without any cap or timeout.

The claim is limited to the stated pure-p12 lattice and perturbations with finite support entirely inside a safe bulk segment (not centre-reaching or exterior differences). It is not a claim that no periodic centre exists or that the orbit of 196 avoids palindromes.