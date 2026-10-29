# Z48 target

Audit the rooted base-10 p12/m9 phase-0 pairword family:

- B = [10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
- W = [5,18,4,8,1,15,4,0,5]
- U = (10,9,8)
- P(q,k) = H ++ C ++ reverse(H), H = B ++ W^q ++ J ++ U^k
- Reference parameters: q=14, k=100, phase 0, every J in {0,...,18}^3 or {0,...,18}^4.

The endpoint test is whether the 120-step image restores the required B ++ W^14 prefix. Check an odd palindromic centre C=[0,0,0] and an even palindromic centre C=[8,8], without applying any odd-centre mod-11 prefilter.

The intended scoped conclusion is an EXHAUSTED-NONE cell audit. Any transfer to all q>=14,k>=100 relies on the existing T12 reset-cone/paired-insertion theorem; this census does not re-prove that theorem and is not a global decimal Lychrel result.
