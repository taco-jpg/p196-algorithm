# FORMALIZATION_K1 -- Lean 4 formalization of the K1 audit's finite checks

Work dir: `/tmp/claude-0/-home-claude/61279d55-9bc5-5e58-836c-ca6225d98f6f/scratchpad/audit/K1lean/`
Toolchain: Lean 4.19.0 (repo pin), core only (no Mathlib), no imports. Every file is standalone.
Compile: `export PATH=/root/.elan/bin:$PATH; cd /home/claude/p196-algorithm/lean; nice -n 10 lake env lean <file>`.
Rules respected: no `sorry`, no `native_decide`, no new axioms; the finite checks are `decide +kernel`.
`#print axioms` for every theorem is in the file's last lines and in `final/<file>.out`; every theorem depends only
on a subset of {propext, Classical.choice, Quot.sound} (the three axioms allowed by `AGENTS.md`); all `decide +kernel`
statements about data use at most `propext` / `Quot.sound` (the `Classical.choice` appears only in the two general
lemmas `step_value`, `realOK_reading`). Compile logs contain no errors or warnings.
Times / RSS are from the final run of each file (`final/*.out`; RSS = peak of the summed resident sets of the `lake`+`lean`
process group, polled every 0.4 s, `nice -n 10`, one process at a time).
Generators (kept for reproducibility, they only read the repo files): `gen_charges.py`, `gen_kernel2.py` (+`gen_kernel.py`,
`t_L.lean` = the lemma block), `gen_twist.py` (+`twist_lemmas.lean`), `gen_stationary.py` (+`a2gen.py`), `gen_common.py`.

Honesty rule used throughout: a theorem that compares a stored table with a definition written in the file says so, and the
link "definition <-> physical claim" is NOT claimed unless a Lean lemma proves it (only `step_value` does such a link).

Teeth (mutation tests, each fails as it should): changing one `W2` entry breaks `rec2_row_charges_zero` and
`rec2_bulk_step_consistent`; changing `tab 0 0` from 14 to 15 breaks `local_equations_give_table` and `cell_t0_n146`;
changing one `rec0` entry breaks `rec0_t0_table`; deleting the descending-carry filter in `succ2` breaks `k2_j0_acyclic`.

---------------------------------------------------------------------------------------------------------------------

## 1. Agent5 P12 one-site response kernel  (priority 1)

Source claim: `results/Agent5P12AllPhaseKernel.md` (PAPER PROOF), checker `classify_all_phase.py`.

Definitions (in every K1Kernel* file): `norm` (carry normalisation of a column-sum word to little-endian decimal digits, final
carry appended), `pairs v = [v_i + v_{L-1-i}]`, `pwStep P = pairs (norm 0 P)`; `lowRow t n` (exterior `B t` ++ periodic `W t`,
central cell made even for odd n), `mkP low n` (palindromic pair word), `tab t r` (the published +-9 table), and
`siteProp t n j := forall a<19, a /= low[j] -> (pwStep (mkP (low.set j a) n) = pwStep (mkP low n) <-> a in tab t ((j-34)%9))`
(the replacement changes BOTH symmetric coefficients j and n-1-j).

### K1Kernel.lean  (66.3 s, 2448 MB)
* `step_value` (general, all digit lists d with digits <= 9): `norm 0 (pairs d)` has all digits < 10 and value
  `toNat d + toNat d.reverse`, i.e. `pwStep` really is "add the digit reversal" (supporting lemmas `norm_cons`, `toNat_norm`,
  `norm_digits`, `toNat_zipWith_add`, `toNat_pairs`, `mem_zipWith_add`).
* `realOK_reading`: if the Boolean `realOK low n` holds (explicit digit witness `realize`, digits <= 9, nonzero top digit,
  `pairs (realize) = mkP low n`, `norm 0 (mkP low n)` has nonzero top digit) then `norm 0 (mkP low n)` is the canonical digit
  list of `N + rev N` for the integer `N = toNat (realize low n)` and `pwStep (mkP low n)` is its pair word.
* `base_realisable`: `realOK` holds for the unchanged words, all 12 phases, n = 146 and 147.
* `local_equations_give_table`: the structural hypotheses (overflow bit only at phases 0,4,8; `B t` leading cell >= 10 iff
  overflow; rows 0,4,8 contain no 9) hold, and for t in {0,4,8}, r < 9 the solutions `a<=18, a/=q` of the two local carry
  equations `A = B`, `a - q = 9A` (A,B outgoing-carry changes with the stored carries `cup`) are exactly `tab t r`.
  This is a table-vs-equations check; it does not by itself talk about `pwStep`.
* `cell_t{0,4,8}_n{146,147}`: for phases 0,4,8, n = 146 and 147 (even/odd), sites j = 52..60 (all nine residues mod 9; two periods
  above the exterior, > 1 period below the centre), every a <= 18: `pwStep` unchanged iff `a in tab t r`.

### K1KernelNonOverflowA/B/C.lean  (57.6 s / 2288 MB, 57.2 s / 2258 MB, 55.2 s / 2261 MB)
Same definitions; `cell_t{1,2,3}`, `cell_t{5,6,7}`, `cell_t{9,10,11}` x n in {146,147}, same sites: for the nine phases with overflow
bit 0, NO replacement a <= 18 leaves `pwStep` unchanged (`tab t r = []`, the iff gives "pwStep differs for every a/=q").

### K1KernelN400.lean (74.6 s, 2417 MB) and K1KernelN401.lean (85.5 s, 2415 MB)
`cell_t{0,4,8}_n400_{a,b,c}` / `cell_t{0,4,8}_n401_{a,b,c}`: the same statement at the checker's lengths 400 / 401 for sites
j = 178..186 (nine residues, deep bulk), split into three 3-site theorems each only to bound kernel memory (one 9-site theorem
peaked at 3.9 GB; splitting gives 2.4 GB for the whole file).

NOT proved (Agent5): the statement for arbitrary length / arbitrary site (the carry-reset argument is not formalised; only
the concrete lists above, i.e. 12 phases x n in {146,147} x 9 sites and phases 0,4,8 x n in {400,401} x 9 sites, plus
`step_value`); realisability of the CHANGED words (a replaced) as pair words of integers (only the unchanged words are
checked via `realOK`); phases 1,2,3,5,6,7,9,10,11 at n = 400/401; any statement about centres, defects that persist, or 196.
The Python checker's range (every interior site, k = 0,1 i.e. n = 400, 401, 418, 419) is wider than what is in Lean.

---------------------------------------------------------------------------------------------------------------------

## 2. Agent3 bulk linear charges, rec2  (priority 2)

Source: `results/Agent3BulkLinearCharges.md` (PAPER PROOF), `agent3_charge_invariants.py`, data `lat2.txt` (= 3rd record of
`p8_scc.txt`, checked equal).

### K1Charges.lean  (13.4 s, 1000 MB)
* `rec2_row_charges_zero`: the stored rec2 matrix has 8 rows of 48 entries and `sum_j 10^j W[t][j] = 0 (mod 99)` for each row t.
* `rec2_bulk_step_consistent`: with the stored ascending carries `A t`, derived descending carries (0/1 valued) and overflow word
  `10101010`, the cyclic bulk update (gamma=0: `2P_j+a_j+d_j-10(a_{j+1}+d_{j-1})`; gamma=1: `P_j+P_{j-1}+a_j+d_{j-1}-10(a_{j+1}+d_{j-2})`)
  maps row t to row t+1 (mod 8), and `a_{j+1} = [P_j+a_j >= 10]`, `d_{j-1} = [P_j+d_j >= 10]`.
* `mult_eight_steps`: `(2^4 * 11^4) % 99 = 22`; `mult_192_steps`: `22^4 % 99 = 22` and `22^96 % 99 = 55`.
* `classify_b10_M33_m2`, `classify_b10_M9_m3`, `classify_b10_M11_m3`: for (b, M, m) = (10,33,2), (10,9,3), (10,11,3), EVERY
  vector q in (Z/M)^m satisfies the three carry-cancelling coefficient equations (ascending, gamma=0 descending, gamma=1 descending)
  iff it is `q[i] = 10^i z (mod M)` with `(b^2-1) z = 0 = (b^m-1) z (mod M)`.

NOT proved (Agent3): the general classification and gcd count (any b, m, M), the claim that these are the only charges for
M = 99, m = 48 (only 3 small instances are exhaustive), the multiplier laws as theorems about arbitrary rows (only the numbers
22^k mod 99 and the rec2 data consistency), "formally independent carries" being the right model, any K1 consequence. (Attempts at the
general ZMod-style proof need sum re-indexing lemmas; not done.)

---------------------------------------------------------------------------------------------------------------------

## 3. Agent14 complement-twist mismatch table  (priority 3)

Source: `results/Agent14ComplementTwist.md` (labelled PAPER PROOF; auditor: effectively COMPUTED), `agent14_complement_twist.py`,
`agent14_parity_flip.py`. Rows: rec0, rec1, rec2 from `p8_scc.txt`, p12m9 from `lat_p12m9.txt`.

### K1Twist.lean  (46.2 s, 2287 MB)
Definitions: `G t d` (overflow count), `L = p * (2m / gcd(2m, S))`, `mis t d s` (complement mismatches
`#{j<m | W[(t+d)%p][(j+s)%m] + W[t][j] /= 18}`), `ordMis`, a scan table over `1 <= d <= L`.
* `<lat>_shape` (lat in rec0, rec1, rec2, p12m9): shape of the data (p rows of m entries <= 18) and `L = 80, 80, 192, 72`.
* `<lat>_t<t>_table` (one theorem per start phase t < p, 8/8/8/12 per lattice): number of even-G advances d<=L at that phase, a lower bound on
  `mis` attained exactly, the ordinary returns (positive control: only `(t, L)`), and the odd-G exact complement coincidences
  `(t,parity,d,G,shift=(G+1-parity)/2)`. Summed: eligible pairs 320/320/768/432, minimum mismatches 16/16/39/7 (= published).
  Parity-flip coincidences: rec0 and rec1 each have 16, namely `(t,0,18,9,5)` and `(t,1,62,31,15)` for every t<8; rec2 and p12m9 have none
  (the auditor's remark that rec0/rec1 have odd-G exact complement returns is confirmed; the auditor's "32 triples" is 16 quintuples
  by this file's counting).
* General lemmas (any `Lat`): `G_add`, `G_mod`, `G_period`, `reduce` (every advance d >= 1 has d0 in [1,L] with the same row and
  `G t d = G t d0 + 2 m X`, using S-periodicity and `2m | (L/p) S`), `mis_congr`, `scan_complete`, `no_complement_all_d`.
* `<lat>_no_complement_all_d`: for ALL t < p and ALL d >= 1 with `G t d` even, `1 <= mis t d (G t d / 2)`: no exact complement
  return with the parity-preserving displacement `G/2`, for every positive advance (the reduction to d <= L, which the note states in
  words, is thereby formalised).

NOT proved (Agent14): that the table question is the right translation of "complement-twisted centre return" (the note's one-line
complement conjugacy `s* = 2b-1-s` and the centre-displacement argument are paper); the carry part (`complement_carry_glides`);
the odd-G / parity-flip and ordinary lists are for d <= L only (no all-d reduction for odd G); other lattices; any dynamical claim.

---------------------------------------------------------------------------------------------------------------------

## 4. Agent2 stationary transfer graph, j mod 5 in {0,3}  (priority 4)

Source: `results/Agent2K1BoundaryTransfer.md`, `Agent2K1StationaryWall18.md`, `agent2_boundary_check.py`, `agent2_stationary_bicore.cpp`.

### K1Stationary.lean  (84.4 s, 2454 MB)
Definitions: `lat`, `carryBelow`, `carryAbove`, `gam` (rec0 rows, spatial period 20, periodic bulk only), `succ2` (transcription of
`successors` for K = 2 columns), `table2 j` (all 2736 = 8*18*19 nodes `(t, a, b)`, `a` off the lattice at column x = 119+j, with
successor keys), `alive n` (nodes with a path of >= n transitions: iterate "keep nodes with a successor among the kept nodes",
bitmask membership).
* `k2_j<j>_acyclic` for j in {0, 3, 5, 8, 10, 13, 15, 18} (= all j<20 with j mod 5 in {0,3}): `alive N (table2 j) = []` with N = 15
  (j mod 5 = 0) resp. 21 (j mod 5 = 3), AND `alive (N-1) (table2 j) /= []`. So the 2-column graph has no path of N transitions (hence is
  acyclic, no infinite path), and its longest path has exactly N-1 = 14 / 20 transitions, matching the Python values (14; 20).

NOT proved (Agent2): (i) SOUNDNESS: that `succ2`/the graph over-approximates the real reverse-and-add dynamics. This is the hard
part named in the audit and is only tested in Python (`agent2_sound.py`); these theorems are about the graph defined by the Lean
function, not about decimal integers. (ii) j mod 5 in {1,2} (needs K = 3: 51,984 nodes per j; measured kernel memory here is
about 0.45-0.7 MB per node for the K=2 table, i.e. >15 GB, so not attempted) and j mod 5 = 4 (K = 18, 525-state lifted core).
(iii) the exterior (`x - 60 >= 59 >= 39`, so only periodic bulk rows are used). (iv) anything about moving defect fronts, actual
centres, or 196: the pinned-defect caveat of the audit applies unchanged.

---------------------------------------------------------------------------------------------------------------------

## Compile summary (final runs)

| file | time | peak RSS | theorems (axioms) |
|---|---|---|---|
| K1Charges.lean | 13.4 s | 1000 MB | 7, none |
| K1Kernel.lean | 66.3 s | 2448 MB | 10 (2 with propext+Classical.choice+Quot.sound, rest propext+Quot.sound / none) |
| K1KernelNonOverflowA/B/C.lean | 57.6 / 57.2 / 55.2 s | 2288 / 2258 / 2261 MB | 6 each (propext, Quot.sound) |
| K1KernelN400.lean | 74.6 s | 2417 MB | 9 (propext, Quot.sound) |
| K1KernelN401.lean | 85.5 s | 2415 MB | 9 (propext, Quot.sound) |
| K1Twist.lean | 46.2 s | 2287 MB | 44 listed in `#print axioms` (propext, Quot.sound) |
| K1Stationary.lean | 84.4 s | 2454 MB | 8 (propext) |

Engineering notes: kernel memory is roughly proportional to the work of ONE declaration (cache is dropped between declarations
but the allocator does not return it), so large checks are split into several theorems (9 sites -> 3+3+3 cut a 3.9 GB peak to 1.8 GB);
`List.getD`-heavy code and `Nat.rec`-recursive helpers cost ~100 B per reduction step; the carry `match` in `norm` keeps terms small.
