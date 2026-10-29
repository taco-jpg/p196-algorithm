# Two-strip physical pumping lemma

**Label: PAPER PROOF** (finite controls: COMPUTED; not Lean-verified).
For any base b >= 2, symmetric pair-coefficient word P, and lower-half cut (i,w), exact carry equalities c_i=c_(i+w) and c_(n-i-w)=c_(n-i) make insertion of the strip and its mirror commute with one genuine reverse-and-add pairword step. On overflow (gamma=1), also require the lagged normalized digit equality d_(n-i)=d_(n-i-w). For two disjoint cuts these identities compose, so a complete T-step return at one physical width extends to all larger independent repetition counts, provided every one of the T+1 phase rows satisfies both gates and each phase retains an odd pair coefficient outside the cuts. Proof: carry resets reproduce both inserted digit strips; the lag equality repairs the one-place upper shift caused by overflow; induction gives the phasewise commute and preserves the odd witness.

Reproduce with python3 calculation/new_structures/R20/two_strip_pumping.py. Scope: pumping criterion only; no rooted decimal return, Lychrel number, or Lean result is claimed.
