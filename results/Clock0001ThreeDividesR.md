# Clock0001ThreeDividesR

**Claim (PAPER PROOF + COMPUTED, 2026-11-02).** In the Agent120 decimal exterior system (`calculation/neutral_band_search.py`, nextB
with e2 = 1 - e1, trailing 9s trimmed), a B-cycle with overflow word (0001)^r exists only if 3 | r. Equivalently: chain 1's
branches r = 1, 2 (mod 3) are closed for every r and every width (this supersedes the thresholds r >= 19 / r >= 38 of
`Chain1PortCells`; P = 88, 112, 136, 152, 160, ... are closed).
**Proof.** Padding by 9s does not change the map (A1); the low K columns of a padded exterior follow the K-head graph G_K of
EXTERIOR.md section 2.5 (A2); projecting G_{K+1} -> G_K keeps closed walks and their lengths (A3). So a closed walk of length 4r with
12 not dividing 4r lies, for every K, in S_K = union of cyclic SCCs of period not divisible by 12 above S_{K-1} (A4). Computation:
S_K is nonempty up to K = 36 (from K = 21 only period-76 SCCs survive: the 19 | r of the old thresholds) and S_37 is empty (A5).
**Checks.** A1/A2 against the exact mirror: 1,285,962 cases, 0 mismatches. A5 by three implementations with identical counts at every K
(C++ `khead4.cpp`, numpy/scipy `khead_not12_np.py`, and the repo's own `khead_family.py` with a 2-line period filter run on the
Studio); positive controls base 11 (001) and base 26 (10), negative control base 10 (01). bx: (0001)^r EXHAUSTED for r = 1,2,4,5,7,8.
**Not claimed:** the case 3 | r. P(3): only N12 (bx, COMPUTED); P(6): only N12 twice (ReachDiskRounds6to8, premise (B));
r = 9, 12, ... UNDECIDED. Missing lemma: for k >= 3, Phi^12 on clock (0001)^3 has no period-k orbit besides N12; the K-head method
cannot give it (N12 is a closed 12-walk at every K). Not Lean-checked.
Side note: `exterior_census/py/verify_ext.py` calls `bx -w -first`, whose witness is wrong for p12 (only `-w -nosym` is right);
verdicts are unaffected. Files: `calculation/decimal_frontier/exterior_census/three_divides_r/` (PROOF.md).
