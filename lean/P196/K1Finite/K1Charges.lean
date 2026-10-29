/-!
# K1Charges -- finite arithmetic facts behind `Agent3BulkLinearCharges` (rec2 lattice)

SCOPE (read before citing).  Everything below is a *kernel-checked finite computation* about the
stored data of the period-8, spatial-period-48 lattice `rec2` (`data/lat2.txt`: overflow word
`10101010`, 8 rows `W t` of 48 pair coefficients, 8 rows `A t` of ascending carries) and about small
modular arithmetic.  Nothing here proves the classification theorem of `Agent3BulkLinearCharges`
for general base / period / modulus, and nothing here is a statement about any actual orbit,
about carry correlations, or about a Lychrel certificate.

Proved here (all by `decide +kernel`, no `native_decide`, no `sorry`, no new axioms):

* `rec2_row_charges_zero`   : the charge `sum_j 10^j * W[t][j]` is `0 (mod 99)` for each of the 8 rows.
* `rec2_bulk_step_consistent`: the stored rows really are a cyclic bulk orbit: with the stored ascending
  carries `A t`, the derived descending carries `d` (0/1 valued) and the overflow word, the cyclic
  bulk update `P'[j] = (gamma=0) 2P[j]+a[j]+d[j]-10(a[j+1]+d[j-1])`, resp.
  `(gamma=1) P[j]+P[j-1]+a[j]+d[j-1]-10(a[j+1]+d[j-2])` maps row t to row t+1 (mod 8), and the carries
  satisfy their defining relations `a[j+1] = [P[j]+a[j] >= 10]`, `d[j-1] = [P[j]+d[j] >= 10]`.
  (This is a data-vs-definition check, it mirrors `step_cell` of `agent3_charge_invariants.py`.)
* `mult_eight_steps`, `mult_192_steps`: `(2^4 * 11^4) % 99 = 22`, `22^4 % 99 = 22`, `22^96 % 99 = 55`
  (the note's multiplier arithmetic: factor 2 per gamma=0 step, factor 1+10 = 11 per gamma=1 step).
* `classify_b10_M33_m2`, `classify_b10_M9_m3`, `classify_b10_M11_m3`: exhaustive classification of ALL
  charge vectors `q in (Z/M)^m` satisfying the carry-cancelling coefficient equations of the note
  (gamma=0 and gamma=1 simultaneously), for those three (b, M, m): they are exactly the vectors
  `q[i] = 10^i z (mod M)` with `(b^2-1) z = 0 = (b^m-1) z (mod M)`.  Only these three small cases.

NOT proved: the general-(b, m, M) classification and gcd count; the multiplier laws as theorems about
arbitrary rows (only the arithmetic of the numbers 22^k mod 99); that carries are "formally
independent" in any real orbit; any consequence for K1.
-/

namespace K1Charges

/-- overflow word of rec2 -/
def gam : List Nat := [1,0,1,0,1,0,1,0]

def W2 : List (List Int) := [
  [4,4,14,1,5,11,7,1,15,12,7,9,9,12,14,4,0,6,5,17,13,9,7,3,13,10,4,13,5,1,9,4,11,6,16,3,7,7,12,4,2,13,2,15,10,10,9,3],
  [7,8,9,6,6,7,9,8,7,9,10,17,9,2,8,9,4,6,11,13,12,3,17,10,7,5,5,8,9,6,10,13,6,8,13,10,10,14,10,7,6,6,6,8,7,2,0,13],
  [15,16,18,12,12,14,18,16,15,9,1,15,9,5,16,18,8,13,3,8,5,8,15,1,15,10,10,16,18,13,1,7,13,17,7,2,2,10,1,15,12,12,12,16,14,4,1,6],
  [12,13,16,12,6,8,14,16,13,5,11,7,5,15,12,16,17,12,7,11,13,13,14,7,7,7,2,8,16,13,5,8,11,12,15,9,4,3,2,7,9,6,6,10,12,9,5,7],
  [5,8,14,5,13,17,9,14,7,12,2,15,11,11,6,14,16,5,16,3,8,8,9,15,14,14,4,17,13,7,11,17,3,6,11,9,9,6,4,14,18,12,13,1,5,9,11,15],
  [11,13,13,10,9,12,8,5,12,10,5,8,8,4,8,11,12,12,12,10,11,16,18,5,11,10,9,12,12,11,9,10,11,9,8,1,9,16,10,9,14,12,7,5,6,15,1,8],
  [3,8,8,2,0,5,17,11,5,1,11,16,16,8,17,3,6,6,6,2,4,14,17,12,3,2,0,6,6,4,0,2,3,9,17,3,9,13,2,0,10,5,15,10,13,10,3,17],
  [11,11,16,10,2,5,13,10,7,6,3,9,14,15,16,11,9,12,12,8,6,9,13,11,6,5,2,6,12,10,4,2,5,13,7,11,13,3,6,2,1,6,11,7,5,5,4,11]]

def A2 : List (List Int) := [
  [0,0,0,1,0,0,1,0,0,1,1,0,0,0,1,1,0,0,0,0,1,1,1,0,0,1,1,0,1,0,0,0,0,1,0,1,0,0,0,1,0,0,1,0,1,1,1,1],
  [1,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,1,0,1,1,0,0,0,0,0,0,1,1,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0],
  [0,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,0,1,0,0,0,0,1,0,1,1,1,1,1,1,0,0,1,1,0,0,0,1,0,1,1,1,1,1,1,0,0],
  [0,1,1,1,1,0,0,1,1,1,0,1,0,0,1,1,1,1,1,0,1,1,1,1,0,0,0,0,0,1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,1,1,1,0],
  [1,0,0,1,0,1,1,1,1,0,1,0,1,1,1,0,1,1,0,1,0,0,0,0,1,1,1,0,1,1,0,1,1,0,0,1,1,1,0,0,1,1,1,1,0,0,0,1],
  [0,1,1,1,1,1,1,0,0,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,1,0],
  [1,0,0,0,0,0,0,1,1,0,0,1,1,1,0,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,1,1,1,1,0],
  [1,1,1,1,1,0,0,1,1,0,0,0,0,1,1,1,1,1,1,1,0,0,0,1,1,0,0,0,0,1,1,0,0,0,1,0,1,1,0,0,0,0,0,1,0,0,0,0]]

/-- charge `sum_j 10^j * w_j` of a row (as an Int) -/
def chargeAux : Nat → List Int → Int
  | _, [] => 0
  | j, x :: xs => (10 : Int) ^ j * x + chargeAux (j + 1) xs

def charge (r : List Int) : Int := chargeAux 0 r

theorem rec2_row_charges_zero : W2.length = 8 ∧ (∀ r ∈ W2, r.length = 48) ∧ ∀ r ∈ W2, charge r % 99 = 0 := by
  decide +kernel

/-! ### bulk-step consistency of the stored rows -/

def at' (r : List Int) (i : Int) : Int := r.getD (i % 48).toNat 0

/-- derived descending carries for row t (0/1 valued by the checks below). -/
def dOf (old nxt a : List Int) (g : Nat) : List Int :=
  (List.range 48).map fun j =>
    if g = 0 then (nxt.getD j 0 - a.getD j 0) % 2
    else (nxt.getD ((j + 1) % 48) 0 - old.getD ((j + 1) % 48) 0 - old.getD j 0 - a.getD ((j + 1) % 48) 0) % 2

def stepCell (old a d : List Int) (g : Nat) : List Int :=
  (List.range 48).map fun (j : Nat) =>
    let J : Int := (j : Int)
    if g = 0 then 2 * at' old J + at' a J + at' d J - 10 * (at' a (J + 1) + at' d (J - 1))
    else at' old J + at' old (J - 1) + at' a J + at' d (J - 1) - 10 * (at' a (J + 1) + at' d (J - 2))

def stepOK (t : Nat) : Bool :=
  let old := W2.getD t []
  let nxt := W2.getD ((t + 1) % 8) []
  let a := A2.getD t []
  let g := gam.getD t 0
  let d := dOf old nxt a g
  decide (stepCell old a d g = nxt) &&
  (List.range 48).all (fun j =>
    decide (at' a (j + 1 : Int) = if old.getD j 0 + a.getD j 0 ≥ 10 then 1 else 0) &&
    decide (at' d (j - 1 : Int) = if old.getD j 0 + d.getD j 0 ≥ 10 then 1 else 0) &&
    decide (a.getD j 0 = 0 ∨ a.getD j 0 = 1) && decide (d.getD j 0 = 0 ∨ d.getD j 0 = 1))

theorem rec2_bulk_step_consistent : ∀ t, t < 8 → stepOK t = true := by decide +kernel

/-! ### multiplier arithmetic -/

theorem mult_eight_steps : (2 ^ 4 * 11 ^ 4) % 99 = 22 := by decide +kernel
theorem mult_192_steps : 22 ^ 4 % 99 = 22 ∧ 22 ^ 96 % 99 = 55 := by decide +kernel

/-! ### exhaustive small-case classification of carry-cancelling charges -/

/-- `allQ M m acc p`: predicate `p` holds for every vector `x_1 :: ... :: x_m :: acc` with entries in `{0..M-1}`. -/
def allQ (M : Nat) : Nat → List Nat → (List Nat → Bool) → Bool
  | 0, acc, p => p acc
  | m + 1, acc, p => (List.range M).all fun x => allQ M m (x :: acc) p

def good (b M m : Nat) (q : List Nat) : Bool :=
  let nb := M - b % M            -- (-b) mod M, so  x - b*y  ==  x + nb*y  (mod M)
  let Q : Nat → Nat := fun i => q.getD (i % m) 0
  (List.range m).all fun i =>
    (Q i + nb * Q (i + m - 1)) % M == 0 &&
    (Q i + nb * Q (i + 1)) % M == 0 &&          -- gamma = 0 descending coefficient
    (Q (i + 1) + nb * Q (i + 2)) % M == 0       -- gamma = 1 descending coefficient

/-- `q[i] = b^i * z (mod M)` with `z = q[0]`, `(b^2-1) z = 0` and `(b^m-1) z = 0` (mod M). -/
def shape (b M m : Nat) (q : List Nat) : Bool :=
  let z := q.getD 0 0
  ((b * b - 1) * z) % M == 0 && ((b ^ m - 1) * z) % M == 0 &&
    q == (List.range m).map fun i => b ^ i * z % M

theorem classify_b10_M33_m2 : allQ 33 2 [] (fun q => good 10 33 2 q == shape 10 33 2 q) = true := by decide +kernel
theorem classify_b10_M9_m3 : allQ 9 3 [] (fun q => good 10 9 3 q == shape 10 9 3 q) = true := by decide +kernel
theorem classify_b10_M11_m3 : allQ 11 3 [] (fun q => good 10 11 3 q == shape 10 11 3 q) = true := by decide +kernel

end K1Charges

#print axioms K1Charges.rec2_row_charges_zero
#print axioms K1Charges.rec2_bulk_step_consistent
#print axioms K1Charges.mult_eight_steps
#print axioms K1Charges.mult_192_steps
#print axioms K1Charges.classify_b10_M33_m2
#print axioms K1Charges.classify_b10_M9_m3
#print axioms K1Charges.classify_b10_M11_m3
