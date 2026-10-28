# Exponentially many decimal one-step pair-word preimages

**PAPER PROOF.** For each k>=1 and each parity e∈{0,1}, let n=200+18k+e. This note constructs at least 2^k distinct positive, canonical, n-digit ordinary decimal seeds whose first reverse-and-add successors all share exactly the **same complete palindromic coefficient/pair word**. Their successor integers need not be equal, and no statement about subsequent iterates, a periodic centre, the existence of a Lychrel number, or the orbit of 196 follows. This is stronger than the previously published existence of a single seven-site local collision at any shifted position: it establishes an explicit exponential lower bound on collision-fibre multiplicity at ONE fixed length n.

## Original pair word and local switch

Read the phase `t=1` exterior B and spatial-period-9 row W from `calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt` (base b=10, p=12, m=9, `g=100010001000`). Form a symmetric coefficient word P_n of length n, with low half given by B followed by the cyclic W row and high half its reflection. For odd n, if necessary choose an even centre coefficient by changing only the central unbounded core cell. Every coefficient is in 0..18, and the exterior coefficient at each end is positive and less than 9, so the word can be realized by an ordinary canonical n-digit integer and its normalization has no final carry.

At every lower index j with `j≡59 (mod 9)` sufficiently far from the centre, the seven consecutive bulk coefficients are

    A = [4,5,10,14,13,12,9].

Define a **switch** at j that replaces them, and simultaneously replaces their reflected seven positions, with

    A' = [9,5,0,15,3,12,14].

The published `Agent5P12BulkCollisionTransfer` two-sided carry equations provide an accepting seven-edge path: both the lower incoming and reversed-upper outgoing carries at the inward cut equal those of the original lattice; all seven next pair coefficients agree; no difference leaks into either side of the switch. The reproducible arithmetic checker from that result verifies every edge. Thus this local switch is an exact, self-contained invisible substitution for the ONE-step pair-word map, not a heuristic.

## Independent switches and the all-k lower bound

Place k switches at the positions

    j_a = 59+9a,  for a=0,...,k-1.

The seven-site intervals `[j_a,j_a+6]` are pairwise disjoint, with exactly two untouched lattice sites separating neighbouring intervals. At n=200+18k+e, the last modified lower position is `j_(k-1)+6=56+9k`, whereas the lower centre boundary is at least `100+9k`. There are therefore at least 43 unchanged positions between the final switch and centre, independently of k, and the mirrored patches are disjoint. All patches lie after the 34-site exterior.

For each subset S of `{0,...,k-1}`, independently apply the switch at j_a if and only if `a∈S`, obtaining the symmetric coefficient word Q_S. In the exact two-sided carry transducer, each selected switch starts and ends at the **same original carry state**, and each unselected interval follows the original path. Hence concatenating arbitrarily many selected/unselected transitions preserves the original complete next pair word, including both exterior ends and the centre. The terminal carry stays zero. This proof applies for all k, with no width, SAT, time, or state cap.

The map S→Q_S is injective: the FIRST coefficient at j_a changes by +5 exactly when a∈S, and no other switch touches that coordinate. Therefore the family contains precisely 2^k distinct coefficient words. Each has a deterministic realization as the pair sums of the decimal digits of some canonical positive n-digit integer N_S (put a positive high digit at the leading pair and split every other pair coefficient into two digits in 0..9; halve the even central coefficient for odd n). Different pair words force different source integers. Ordinary reverse-and-add on every N_S yields the same complete next pair word as on N_empty, as claimed.

Equivalently, along the infinite even-length progression n=218,236,254,... the one-step pair-word map has a fibre of size at least `2^((n-200)/18)`, and the odd-length progression n=219,237,255,... has the same lower bound. The fibre statement concerns **pair words of successor numbers**, not equality of the successor numbers themselves.

## Reproduction and independent controls

Run from the repository root:

```
python3 calculation/decimal_frontier/lattice_kinks/code/k2_multi_fiber.py
```

The checker imports the already committed independent digit-splitting and ordinary grade-school reverse-and-add routines from `k2_gate_extension.py`; it constructs Q_S for every S at k=1,...,10 and k=12, for both centre parities through k=10. At k=12 it checks all 4096 distinct words and their exact complete successor pair words. It additionally uses a separate Python big-integer conversion and arithmetic (`N+reverse(N)`) for selected masks through k=7, agreeing with the digit-list routine. All subset masks pass. The finite tests validate the explicit construction; the proof for **all k** is the exact carry-boundary concatenation argument above.

The theorem does not assert a repeated temporal centre, a Lychrel number, or any result about base 10 beyond this stated one-step pair-word fibre.