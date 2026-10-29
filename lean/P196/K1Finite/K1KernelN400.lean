/-!
# K1KernelN400 -- P12 one-site response kernel at length n = 400, overflow phases 0, 4, 8
SCOPE.  Companion of `K1Kernel.lean` (same definitions, copied so the file compiles standalone) at the length
used by the Python checker `classify_all_phase.py` (n = 400).  Proved (`cell_t{0,4,8}_n400_{a,b,c}`, three theorems of three sites each, split only to bound kernel memory): for phases 0, 4, 8,
length n = 400, the nine consecutive sites j = 178..186 (all nine residues mod 9, deep in the bulk: 144 cells
above the exterior of width 34, more than 12 cells below the centre) and every replacement a <= 18, a != low[j]:
`pwStep` of the pair word with BOTH symmetric coefficients j and n-1-j replaced by a equals `pwStep` of the
unchanged word iff a is the published value.  Finite statement about these explicit length-400 lists only; NOT the
all-length theorem; no claim about centres or the orbit of 196.
Common set-up (all `K1Kernel*.lean` files).  `pwStep P` is an explicit, decidable reverse-and-add step on
column-sum ("pair") words: `norm 0 P` carry-normalises `P` to decimal digits (little-endian), and
`pairs v = [v_i + v_{L-1-i}]` is the mirrored digit sum.  The lattice data are the stored p12/m9
lattice of `calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt` (overflow word 100010001000,
spatial period 9, exterior width 34, 12 temporal phases).  `lowRow t n` is the lower half of the pair
word at phase `t`, length `n` (exterior `B t`, then the periodic bulk `W t`; for odd `n` the central cell
is made even), `mkP low n` the palindromic pair word.  `siteProp t n j` says: for EVERY replacement value
`a ≤ 18`, `a ≠ low[j]`, of both symmetric coefficients `j` and `n-1-j`, `pwStep` of the changed word equals
`pwStep` of the unchanged word IF AND ONLY IF `a` is the published replacement `tab t ((j - 34) % 9)` (the +-9 table of `results/Agent5P12AllPhaseKernel.md`; empty list = no
invisible replacement).

-/
namespace K1Kernel

/-- carry normalisation of a column-sum word (little-endian): digit `(x+c) % 10`, carry `(x+c)/10`
(the `match` only forces the carry to a small literal, which keeps kernel terms small); a nonzero final
carry is appended as a last digit. -/
def norm : Nat → List Nat → List Nat
  | c, [] => if c = 0 then [] else [c]
  | c, x :: xs =>
    ((x + c) % 10) :: (match (x + c) / 10 with
      | 0 => norm 0 xs
      | 1 => norm 1 xs
      | k + 2 => norm (k + 2) xs)

/-- `pairs v = [v_i + v_{L-1-i}]`: the pair word (mirrored digit sums) of a digit list. -/
def pairs (v : List Nat) : List Nat := List.zipWith (· + ·) v v.reverse

/-- one reverse-and-add step on pair words (see `step_value`: if `P = pairs d` for a digit list `d` of an
integer `N`, then `norm 0 P` is a digit list of `N + rev N` and `pwStep P` its pair word). -/
def pwStep (P : List Nat) : List Nat := pairs (norm 0 P)

/-- overflow word of the p12 lattice -/
def gam : List Nat := [1,0,0,0,1,0,0,0,1,0,0,0]

/-- rows `W t` (spatial period 9), `t = 0..11` -/
def Wrows : List (List Nat) := [
  [5,18,4,8,1,15,4,0,5],
  [10,14,13,12,9,7,10,4,5],
  [1,10,8,5,9,16,0,9,11],
  [4,0,17,11,9,12,2,9,2],
  [8,1,15,4,0,5,5,18,4],
  [12,9,7,10,4,5,10,14,13],
  [5,9,16,0,9,11,1,10,8],
  [11,9,12,2,9,2,4,0,17],
  [4,0,5,5,18,4,8,1,15],
  [10,4,5,10,14,13,12,9,7],
  [0,9,11,1,10,8,5,9,16],
  [2,9,2,4,0,17,11,9,12]]

/-- exterior rows `B t` (34 cells), `t = 0..11` -/
def Brows : List (List Nat) := [
  [10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5],
  [1,5,10,12,13,10,3,7,14,11,4,2,3,9,15,7,9,15,11,14,13,13,14,5,5,13,11,11,9,5,10,10,4,5],
  [2,11,1,6,8,1,7,15,9,3,9,4,7,9,10,16,9,11,4,10,8,8,9,11,11,7,4,3,9,12,1,1,9,11],
  [5,2,3,12,16,2,15,10,9,7,18,8,15,9,1,14,0,3,10,0,17,17,9,3,3,15,8,7,9,4,3,3,9,2],
  [10,4,7,5,13,6,11,1,9,16,16,18,10,9,4,8,1,7,0,2,15,15,9,7,7,10,17,14,18,8,6,6,18,4],
  [1,5,11,12,9,10,8,3,11,6,14,16,10,0,14,12,9,8,7,2,8,12,5,17,14,8,9,13,14,17,14,12,15,13],
  [2,11,3,6,0,1,17,7,2,14,9,14,1,2,9,5,9,17,14,4,17,4,12,15,9,18,9,7,10,16,10,6,12,8],
  [5,2,7,12,0,3,14,15,5,9,0,9,3,4,18,11,9,15,9,10,14,10,5,12,0,17,9,16,1,14,1,14,4,17],
  [10,4,15,4,1,7,9,11,11,18,0,18,6,9,17,4,0,12,0,2,10,1,12,4,2,15,0,13,4,8,4,8,10,15],
  [1,5,10,10,5,8,17,1,4,11,9,9,15,16,7,12,4,3,3,2,3,2,4,7,6,8,6,4,8,12,12,12,9,7],
  [2,11,1,1,11,17,14,3,9,3,0,0,12,13,16,4,9,6,6,4,6,4,8,14,12,16,12,8,17,5,6,5,9,16],
  [5,2,3,3,3,16,9,7,18,6,0,1,5,8,13,9,18,12,12,8,12,8,17,9,6,14,5,18,14,11,12,11,9,12]]

def nB : Nat := 34
def mP : Nat := 9

/-- lower half of the pair word at phase `t`, length `n`: exterior `B t` then the periodic bulk `W t`;
for odd `n` the central cell is made even (so that a palindromic pair word is realisable). -/
def lowRow (t n : Nat) : List Nat :=
  let h := (n + 1) / 2
  let low := (Brows.getD t []) ++ (((List.replicate (h / mP + 1) (Wrows.getD t [])).flatten).take (h - nB))
  if n % 2 = 1 ∧ low.getD (h - 1) 0 % 2 = 1 then low.set (h - 1) (low.getD (h - 1) 0 - 1) else low

/-- the palindromic pair word with lower half `low` and length `n` -/
def mkP (low : List Nat) (n : Nat) : List Nat :=
  if n % 2 = 1 then low ++ low.dropLast.reverse else low ++ low.reverse

/-- explicit digit witness for the palindromic pair word `mkP low n` (digits `min(P_i, 9)` on the lower half,
`P_i - min(P_i,9)` on the upper half, first/last digit `P_0 - 1` / `1`, centre `P_c / 2`). -/
def realize (low : List Nat) (n : Nat) : List Nat :=
  let dl0 := (low.headD 1 - 1) :: (low.tail.map fun x => min x 9)
  let dl := if n % 2 = 1 then dl0.dropLast ++ [low.getLast?.getD 0 / 2] else dl0
  let dh := List.zipWith (· - ·) low dl
  if n % 2 = 1 then dl ++ dh.dropLast.reverse else dl ++ dh.reverse

/-- `realOK low n`: `realize` is a genuine decimal digit list (digits ≤ 9, nonzero top digit, length `n`) whose
pair word is `mkP low n`, and the carry-normalisation `norm 0 (mkP low n)` has nonzero top digit (so it is the
canonical digit list of `N + rev N`). -/
def realOK (low : List Nat) (n : Nat) : Bool :=
  let d := realize low n
  decide (d.length = n) && decide (pairs d = mkP low n) && d.all (fun x => decide (x ≤ 9)) &&
    decide (d.getLast? ≠ some 0) && decide ((norm 0 (mkP low n)).getLast? ≠ some 0)

/-- the published kernel: replacement value making the one-site change invisible (`[]` = none) -/
def tab (t r : Nat) : List Nat :=
  match t with
  | 0 => [[14],[9],[13],[17],[10],[6],[13],[],[14]].getD r []
  | 4 => [[17],[10],[6],[13],[],[14],[14],[9],[13]].getD r []
  | 8 => [[13],[],[14],[14],[9],[13],[17],[10],[6]].getD r []
  | _ => []

/-- For phase `t`, length `n`, site `j`: for every `a ≤ 18`, `a ≠ low[j]`, replacing BOTH symmetric coefficients
`j` and `n-1-j` by `a` gives a word whose `pwStep` equals that of the unchanged word iff
`a ∈ tab t r`, `r = (j - 34) % 9`.  (Realisability of the CHANGED words as pair words of integers is not
formalised; for them `a ≤ 18`, palindromic, first cell and centre unchanged, which is what the paper's
canonical realisation uses.) -/
abbrev siteProp (t n j : Nat) : Prop :=
  ∀ a, a < 19 → a ≠ (lowRow t n).getD j 0 →
    (pwStep (mkP ((lowRow t n).set j a) n) = pwStep (mkP (lowRow t n) n) ↔ a ∈ tab t ((j - nB) % mP))

theorem cell_t0_n400_a : ∀ k, k < 3 → siteProp 0 400 (178 + k) := by decide +kernel
theorem cell_t0_n400_b : ∀ k, k < 3 → siteProp 0 400 (181 + k) := by decide +kernel
theorem cell_t0_n400_c : ∀ k, k < 3 → siteProp 0 400 (184 + k) := by decide +kernel
theorem cell_t4_n400_a : ∀ k, k < 3 → siteProp 4 400 (178 + k) := by decide +kernel
theorem cell_t4_n400_b : ∀ k, k < 3 → siteProp 4 400 (181 + k) := by decide +kernel
theorem cell_t4_n400_c : ∀ k, k < 3 → siteProp 4 400 (184 + k) := by decide +kernel
theorem cell_t8_n400_a : ∀ k, k < 3 → siteProp 8 400 (178 + k) := by decide +kernel
theorem cell_t8_n400_b : ∀ k, k < 3 → siteProp 8 400 (181 + k) := by decide +kernel
theorem cell_t8_n400_c : ∀ k, k < 3 → siteProp 8 400 (184 + k) := by decide +kernel

end K1Kernel

#print axioms K1Kernel.cell_t0_n400_a
#print axioms K1Kernel.cell_t0_n400_b
#print axioms K1Kernel.cell_t0_n400_c
#print axioms K1Kernel.cell_t4_n400_a
#print axioms K1Kernel.cell_t4_n400_b
#print axioms K1Kernel.cell_t4_n400_c
#print axioms K1Kernel.cell_t8_n400_a
#print axioms K1Kernel.cell_t8_n400_b
#print axioms K1Kernel.cell_t8_n400_c
