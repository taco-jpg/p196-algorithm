# N28: paired-insertion pump contracts with independent drifting joints

Label: PAPER PROOF (soundness of the conditional finite format), with separately reported COMPUTED experiments. **Not a decimal Lychrel certificate.** No eventual periodicity, infinite nonpalindromicity or Lean verification is claimed.

## Exact state and edge contract
Use least-significant-first palindromic pair coefficients P (each 0..18). Normalize P with carry c starting at zero to get decimal digits D of N+reverse(N), of length |P|+gamma, gamma in {0,1}. Write Q=pairs(D). For r disjoint paired slots i_j in the left half of P and N-i_j in the reflected half, define P(delta) by inserting delta_j copies of a local period w_j at i_j and its reverse at N-i_j; additions commute under ordered shifts. This represents arbitrarily large, independently drifting joins, not a single centre width.

At a reference P, check for each j, m_j=|w_j|, h_j=|D|-i_j:
1. i_j and h_j are inside their respective periodic segments; the low word at i_j is w_j and the symmetric high word at |P|-i_j is reverse(w_j).
2. The shifted insertion at h_j (the gamma-dependent high cut) creates **the same entire coefficient word** as insertion at the symmetric high cut. The high inserted word u_j is read directly at h_j.
3. Normalization carries c(i_j), c(h_j) are loops through w_j, u_j respectively: f_w(c)=c. (Every carry is 0 or 1.)
4. Normalizing the doubly inserted input matches exact insertion of emitted digit words at both cuts. The resulting Q insertion word is v_j[t]=digit_low[t]+digit_high[m_j-1-t]; check that Q grows by v_j at i_j and reverse(v_j) at |Q|-i_j.
5. To certify nonpalindromicity of D for **all** delta, exhibit an index e<min_j i_j with D[e] != D[|D|-1-e]. This mismatch is outside all inserts.

## Soundness (PAPER PROOF)
An insertion of a coefficient period that returns the entering carry to itself emits a fixed digit block and changes neither later normalization digits nor the final carry. This is proved by induction on the unchanged suffix of the standard radix-10 carry recurrence. Applying this at two non-overlapping cuts, with the reflected cut shifted by gamma, shows D(delta+unit_j) is D(delta) with exactly two digit blocks inserted at reflected positions. Because the two insertions are aligned about the full normalized digit string of length |D|, forming pair sums inserts exactly v_j and its reverse in Q and leaves other pair sums unchanged. Property (2) ensures the *actual symmetric input family* is identical to the shifted insertion description even for gamma=1. Inserted copies remain periods, and their carry loops preserve both cut states, so the same argument can be iterated for all delta_j >= 0. Disjoint cuts commute: an insertion in another band merely shifts the coordinates of both cuts without changing their local words or entering carries. Induction on sum(delta) proves the edge for all independent band counts. The external mismatch e survives, proving nonpalindromicity of every resulting number.

**Conditional infinite certificate criterion:** if finitely many such checked edges close Q_t(delta)=P_(t+1)(delta+a_t), and the aggregate displacement vector after one cycle has every component >= 0, with all edge domains maintained and a nonpalindromicity anchor at each phase, then iterating the closed cycle yields a base-10 Lychrel number. Induct on cycles; the nonnegative aggregate shift prevents any domain count from decreasing under repeats. A complete cycle has **not** been found.

## Positive decimal mechanism, exact scope
For L=(18,7,18,12), bands w1=(2), w2=(6,12), w3=(18), central coefficient 8, define P(k)=L ++ w1^k1 ++ w2^k2 ++ w3^k3 ++ (8) ++ reverse(left half). The seed is obtained by splitting each paired coefficient x as floor(x/2)+ceil(x/2), with central digit 4. At baseline k=(240,240,240), |P|=1929; slots i=(124,484,844). The finite-loop contracts checked for each of the first **232** transitions; each emitted full pairword is exactly a three-independent-pump template for **every** k_j >= 240, and the next number is nonpalindromic for those 232 steps (plus the initial constructed number). The surviving insertion words include a rotating non-neutral period-one w1, period-two w2 turning into (0,0), and stationary (18) w3. Thus the three large bulk regions persist while two interfacial transition regions advance; no narrow-centre hypothesis is used.

At transition 233 (t=232, zero-based), the w1 high-side carry becomes 0 rather than its incoming 1, so the chosen fixed-slot pumping witness fails. This is **not** evidence that the orbit becomes palindromic or that all possible moving slots fail. At k=120,240,480,960 the first failure occurs after respectively 114,232,442,909 certified edges (the last two due to gamma-shift incompatibility at j0). These growing horizons motivate a next test with reanchored sliding cuts and renewal of consumed bulk.

## Reproduction (no third-party packages)
Run from repo root:
- python3 calculation/new_structures/agent-N28/paired_pump.py
- python3 calculation/new_structures/agent-N28/paired_pump.py --mode survey --k 240 --steps 300
- python3 calculation/new_structures/agent-N28/paired_pump.py --mode seed --k 240 > /tmp/n28.seed
- g++ -O3 -std=c++17 calculation/new_structures/agent-N28/replay_int.cpp -o /tmp/n28_replay
- /tmp/n28_replay /tmp/n28.seed 20000

Python bigint checks: 5 distinct independent count increments, 233 states each, **1165** pairword equalities and nonpalindrome checks, through t=232. Independent C++ digit-list orbit: 20,000 steps with no palindrome for k=(240,240,240), |N_20000|=10188 digits; FNV64 7968309113495131358, carry-induced length increases 8259. The 20,000-step replay is only a *finite observation*: the parametric pairword contract was not certified beyond t=231->232. Checks in data.json. The Lean proof path is to encode normalize_insert_loop, pairs_insert_sym, commute_pumps, and a decidable finite-edge checker, followed by a cycle induction.
