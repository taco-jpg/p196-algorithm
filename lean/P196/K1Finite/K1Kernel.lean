/-!
# K1Kernel -- P12 one-site response kernel, overflow phases 0, 4, 8, plus semantics
SCOPE.  `results/Agent5P12AllPhaseKernel.md` (PAPER PROOF) classifies, for the p12/m9 lattice, all single
symmetric coefficient changes in the interior that leave the next pair word unchanged.  This file does NOT
prove that classification for all lengths.  It proves (kernel-checked, no `native_decide`, no `sorry`):

1. `step_value` (general, all digit lists): `pwStep` is exactly "add the reversal": for a list `d` of digits ≤ 9,
   `norm 0 (pairs d)` has digits < 10 and value `toNat d + toNat d.reverse` (and `realOK_reading` packages
   this for the concrete words, including nonzero top digit, so `pwStep` of the pair word of `N` is the pair
   word of `N + rev N`).
2. `local_equations_give_table`: the published +-9 replacement table is exactly the solution set of the two local
   carry equations of the note, for the three overflow phases, and the structural hypotheses hold
   (overflow only at phases 0, 4, 8; rows 0, 4, 8 contain no 9; `B t` leading cell ≥ 10 iff overflow).
   (A check of the table against equations written here; says nothing by itself about `pwStep`.)
3. `base_realisable`: the unchanged words (all 12 phases, n = 146 and 147) are pair words of explicit integers
   (digit witness, top digit nonzero).  `cell_t{0,4,8}_n{146,147}`: for phases 0, 4, 8 and lengths n = 146 and 147
   (even and odd), for the nine consecutive sites j = 52..60 (all nine residues mod 9; two full periods from the
   exterior of width 34, more than a period from the centre), for every replacement a ≤ 18: `pwStep` is unchanged
   iff `a` is the published value.  That is a finite statement about THESE explicit
   lists of length 146/147, not about arbitrary lengths or sites.

NOT proved: any statement for general length, for other sites or lengths (the Python checker covers lengths
400..419 and all interior sites), the carry-reset argument, anything about centres, or the orbit of 196.
The companion files `K1KernelNonOverflowA/B/C.lean` give the same cells (n = 146, 147) for the nine phases without
overflow (table empty = no invisible replacement); `K1KernelN400.lean`, `K1KernelN401.lean` give phases 0, 4, 8 at
lengths 400 and 401 (sites 178..186).
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

/-- little-endian base-10 value of a digit list -/
def toNat : List Nat → Nat
  | [] => 0
  | x :: xs => x + 10 * toNat xs

theorem norm_cons (c x : Nat) (xs : List Nat) :
    norm c (x :: xs) = ((x + c) % 10) :: norm ((x + c) / 10) xs := by
  simp only [norm]
  generalize (x + c) / 10 = k
  rcases k with _ | _ | k <;> rfl

theorem toNat_norm (xs : List Nat) : ∀ c, toNat (norm c xs) = c + toNat xs := by
  induction xs with
  | nil =>
    intro c
    by_cases h : c = 0
    · simp [norm, toNat, h]
    · simp [norm, toNat, h]
  | cons x xs ih =>
    intro c
    rw [norm_cons]
    simp only [toNat]
    rw [ih]
    omega

theorem norm_digits (xs : List Nat) (hx : ∀ y ∈ xs, y ≤ 18) :
    ∀ c, c ≤ 1 → ∀ y ∈ norm c xs, y < 10 := by
  induction xs with
  | nil =>
    intro c hc y hy
    by_cases h : c = 0
    · simp [norm, h] at hy
    · simp [norm, h] at hy; omega
  | cons x xs ih =>
    intro c hc y hy
    rw [norm_cons] at hy
    have hx0 : x ≤ 18 := hx x (by simp)
    have hxs : ∀ z ∈ xs, z ≤ 18 := fun z hz => hx z (by simp [hz])
    rcases List.mem_cons.mp hy with h | h
    · omega
    · exact ih hxs _ (by omega) y h

theorem toNat_zipWith_add (a : List Nat) : ∀ b, a.length = b.length →
    toNat (List.zipWith (· + ·) a b) = toNat a + toNat b := by
  induction a with
  | nil => intro b h; cases b <;> simp_all [toNat, List.zipWith]
  | cons x xs ih =>
    intro b h
    cases b with
    | nil => simp at h
    | cons y ys =>
      simp only [List.length_cons, Nat.add_right_cancel_iff] at h
      simp only [List.zipWith_cons_cons, toNat]
      rw [ih ys h]
      omega

theorem toNat_pairs (d : List Nat) : toNat (pairs d) = toNat d + toNat d.reverse := by
  unfold pairs
  exact toNat_zipWith_add d d.reverse (by simp)

theorem mem_zipWith_add (a : List Nat) : ∀ b y, y ∈ List.zipWith (· + ·) a b →
    ∃ x ∈ a, ∃ z ∈ b, y = x + z := by
  induction a with
  | nil => intro b y h; cases b <;> simp [List.zipWith] at h
  | cons x xs ih =>
    intro b y h
    cases b with
    | nil => simp [List.zipWith] at h
    | cons z zs =>
      simp only [List.zipWith_cons_cons, List.mem_cons] at h
      rcases h with h | h
      · exact ⟨x, by simp, z, by simp, h⟩
      · obtain ⟨x', hx', z', hz', e⟩ := ih zs y h
        exact ⟨x', by simp [hx'], z', by simp [hz'], e⟩

/-- `norm 0 (pairs d)` is a list of decimal digits whose value is `N + rev N`, where `N = toNat d` and
`rev N = toNat d.reverse` (digit reversal). -/
theorem step_value (d : List Nat) (hd : ∀ x ∈ d, x ≤ 9) :
    toNat (norm 0 (pairs d)) = toNat d + toNat d.reverse ∧ ∀ y ∈ norm 0 (pairs d), y < 10 := by
  refine ⟨?_, ?_⟩
  · rw [toNat_norm, toNat_pairs]; omega
  · apply norm_digits _ _ 0 (by omega)
    intro y hy
    unfold pairs at hy
    obtain ⟨a, ha, b, hb, rfl⟩ := mem_zipWith_add _ _ _ hy
    have h1 := hd a ha
    have h2 := hd b (List.mem_reverse.mp hb)
    omega


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

/-- steady ascending carries `cup t r` entering column `r` of row `W t` -/
def Crows : List (List Nat) := [
  [0,0,1,0,0,0,1,0,0],
  [0,1,1,1,1,1,0,1,0],
  [1,0,1,0,0,0,1,0,0],
  [0,0,0,1,1,1,1,0,0],
  [0,0,0,1,0,0,0,0,1],
  [1,1,1,0,1,0,0,1,1],
  [0,0,0,1,0,0,1,0,1],
  [1,1,1,1,0,0,0,0,0],
  [1,0,0,0,0,1,0,0,0],
  [0,1,0,0,1,1,1,1,1],
  [1,0,0,1,0,1,0,0,0],
  [1,0,0,0,0,0,1,1,1]]

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


/-! ### the two local carry equations (derived check, NOT about `pwStep`)

For an overflow phase (`gam t = 1`) and a row without any coefficient 9, replacing the symmetric pair `q → a`
changes the outgoing carry at the lower site by `A = [a+lc ≥ 10] - [q+lc ≥ 10]` (`lc = cup t r`) and at the
upper site by `B = [a+hc ≥ 10] - [q+hc ≥ 10]` (`hc = [W t (r+1) ≥ 10]`); the paper shows invisibility forces
`A = B` and `a - q = 9 A`.  `localCands` enumerates the solutions of exactly these equations; the theorem
says they are the published table.  Whether these equations are the right ones is what the concrete
`siteProp` cells test against the real step. -/

def Wc (t r : Nat) : Nat := (Wrows.getD t []).getD (r % 9) 0
def Cc (t r : Nat) : Nat := (Crows.getD t []).getD (r % 9) 0

def localCands (t r : Nat) : List Nat :=
  let q := Wc t r
  let lc := Cc t r
  let hc := if Wc t (r + 1) ≥ 10 then 1 else 0
  (List.range 19).filter fun a =>
    a != q &&
      decide ((if a + lc ≥ 10 then (1 : Int) else 0) - (if q + lc ≥ 10 then 1 else 0)
        = (if a + hc ≥ 10 then (1 : Int) else 0) - (if q + hc ≥ 10 then 1 else 0)) &&
      decide ((a : Int) - q = 9 * ((if a + lc ≥ 10 then (1 : Int) else 0) - (if q + lc ≥ 10 then 1 else 0)))

theorem local_equations_give_table :
    (∀ t, t < 12 → (gam.getD t 0 = 1 ↔ t = 0 ∨ t = 4 ∨ t = 8)) ∧
    (∀ t, t < 12 → ((Brows.getD t []).headD 0 ≥ 10 ↔ gam.getD t 0 = 1)) ∧
    (∀ t, t < 12 → (t = 0 ∨ t = 4 ∨ t = 8) → ∀ x ∈ Wrows.getD t [], x ≠ 9) ∧
    (∀ t, t < 12 → (t = 0 ∨ t = 4 ∨ t = 8) → ∀ r, r < 9 → localCands t r = tab t r) := by
  decide +kernel


/-- Reading of `pwStep` as integer arithmetic.  If `realOK low n` then, with `d = realize low n`, `N = toNat d`:
`pairs d = mkP low n`; `e = norm 0 (mkP low n)` is the canonical decimal digit list (digits < 10, top digit
nonzero) of `N + rev N` (`rev N = toNat d.reverse`); and `pwStep (mkP low n) = pairs e` is its pair word. -/
theorem realOK_reading (low : List Nat) (n : Nat) (h : realOK low n = true) :
    pairs (realize low n) = mkP low n ∧ (∀ x ∈ realize low n, x ≤ 9) ∧ (realize low n).getLast? ≠ some 0 ∧
    toNat (norm 0 (mkP low n)) = toNat (realize low n) + toNat (realize low n).reverse ∧
    (∀ y ∈ norm 0 (mkP low n), y < 10) ∧ (norm 0 (mkP low n)).getLast? ≠ some 0 ∧
    pwStep (mkP low n) = pairs (norm 0 (mkP low n)) := by
  simp only [realOK, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true] at h
  obtain ⟨⟨⟨⟨hl, hp⟩, hd⟩, hz⟩, hz2⟩ := h
  have hd9 : ∀ x ∈ realize low n, x ≤ 9 := fun x hx => by simpa using hd x hx
  obtain ⟨hv, hdig⟩ := step_value (realize low n) hd9
  rw [hp] at hv hdig
  exact ⟨hp, hd9, hz, hv, hdig, hz2, rfl⟩

/-- sanity: the base words (all 12 phases, both parities) are realisable pair words -/
theorem base_realisable :
    ∀ t, t < 12 → realOK (lowRow t 146) 146 = true ∧ realOK (lowRow t 147) 147 = true := by decide +kernel

theorem cell_t0_n146 : ∀ k, k < 9 → siteProp 0 146 (52 + k) := by decide +kernel
theorem cell_t0_n147 : ∀ k, k < 9 → siteProp 0 147 (52 + k) := by decide +kernel
theorem cell_t4_n146 : ∀ k, k < 9 → siteProp 4 146 (52 + k) := by decide +kernel
theorem cell_t4_n147 : ∀ k, k < 9 → siteProp 4 147 (52 + k) := by decide +kernel
theorem cell_t8_n146 : ∀ k, k < 9 → siteProp 8 146 (52 + k) := by decide +kernel
theorem cell_t8_n147 : ∀ k, k < 9 → siteProp 8 147 (52 + k) := by decide +kernel

end K1Kernel

#print axioms K1Kernel.step_value
#print axioms K1Kernel.realOK_reading
#print axioms K1Kernel.local_equations_give_table
#print axioms K1Kernel.base_realisable
#print axioms K1Kernel.cell_t0_n146
#print axioms K1Kernel.cell_t0_n147
#print axioms K1Kernel.cell_t4_n146
#print axioms K1Kernel.cell_t4_n147
#print axioms K1Kernel.cell_t8_n146
#print axioms K1Kernel.cell_t8_n147
