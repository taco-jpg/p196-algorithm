/-!
# K1Stationary -- finite transfer-graph emptiness for the stationary first-defect column (rec0, p8)

SCOPE (read before citing).  `results/Agent2K1BoundaryTransfer.md` / `Agent2K1StationaryWall18.md` are COMPUTED
results about a finite "k-column transfer graph" `G_k(j)`: nodes `(t, a_0..a_{k-1})` (time phase `t < 8`, the
`k` pair-word cells at columns `x .. x+k-1` with `x = 119 + j`, first cell off the lattice), edges =
`successors` of `agent2_boundary_check.py` (a necessary, over-approximate transition relation of the
reverse-and-add step when the first defect column stays at fixed `x`).  This file kernel-checks, for the
base-10 period-8 `rec0` lattice rows of `lattice_formats/p8_scc.txt` (the 20 spatial blocks of 8 phases),
that for `k = 2` the graph `G_2(j)` has NO directed path with `N` transitions (hence is acyclic, hence has no
infinite path), for the residues `j mod 5 in {0, 3}` -- the eight values j = 0,3,5,8,10,13,15,18 -- with
`N = longest+1 = 15` (j mod 5 = 0) resp. `21` (j mod 5 = 3), and also that a path with `N - 1` transitions
exists (sharpness: the check is not vacuous).

What the theorems say precisely: "`alive N (table2 j) = []`" where `table2 j` lists all `2736 = 8*18*19`
nodes with their (packed) successor lists computed by the function `succ2` defined below, and `alive n` keeps
exactly the nodes having a path of at least `n` transitions (by iterating "keep nodes with a successor
among the kept nodes", bitmask membership).

NOT proved here, and this is the important caveat:
* SOUNDNESS of `succ2` with respect to the real pair-word step (that `G_k(j)` over-approximates the genuine
  dynamics) is NOT formalised; it is only tested in Python (audit `agent2_sound.py`, 0 violations in 70k
  transitions).  So these theorems prove properties of the graph defined by the Lean function `succ2`
  (a transcription of the Python `successors`), not a theorem about the decimal dynamics.
* The residues j mod 5 in {1, 2} (which need k = 3: 51,984 nodes) and j mod 5 = 4 (k = 18, 525-state cyclic
  core) are not covered; the pinned-defect statement does not exclude moving defect fronts or centres.
* `lat`/`cup`/`dcarry` use only the periodic bulk rows (valid because `x - 60 >= 59 >= 39 =` exterior width).
-/
def Wt : List (List Nat) := [
  [17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13],
  [12,11,4,5,12,10,7,8,12,10,3,2,7,10,8,8,9,5,17,11],
  [6,3,9,11,5,1,15,17,5,1,7,4,15,0,17,16,18,11,15,4],
  [10,9,13,1,7,6,7,14,13,6,8,11,10,6,8,15,16,11,8,10],
  [2,0,7,3,14,12,15,9,7,13,17,3,1,13,17,11,14,3,18,1],
  [3,2,7,10,8,8,9,5,17,11,12,11,4,5,12,10,7,8,12,10],
  [7,4,15,0,17,16,18,11,15,4,6,3,9,11,5,1,15,17,5,1],
  [8,11,10,6,8,15,16,11,8,10,10,9,13,1,7,6,7,14,13,6]]

namespace K1Stationary

/-- lattice cell at phase `t`, column `x >= 39` (periodic bulk, spatial period 20) -/
def lat (t x : Nat) : Nat := (Wt.getD (t % 8) []).getD ((x - 39) % 20) 0

/-- first non-9 cell going down from column `z` (inclusive), within `f` steps: `1` if it is `>= 10`, else `0` -/
def carryBelow (t : Nat) : Nat → Nat → Nat
  | 0, _ => 0
  | f + 1, z => if lat t z != 9 then (if lat t z ≥ 10 then 1 else 0) else carryBelow t f (z - 1)

/-- first non-9 cell going up from column `z` (inclusive), within `f` steps -/
def carryAbove (t : Nat) : Nat → Nat → Nat
  | 0, _ => 0
  | f + 1, z => if lat t z != 9 then (if lat t z ≥ 10 then 1 else 0) else carryAbove t f (z + 1)

/-- overflow word of `rec0` is `10101010` -/
def gam (t : Nat) : Nat := if t % 2 = 0 then 1 else 0

/-- One transition of the 2-column graph at defect column `x`, phase `t`, window `(a, b)` (cells at columns `x`,
`x+1`), as a list of successor windows packed `n0 + 19 * n1`.  Transcription of `successors` of
`agent2_boundary_check.py` for `K = 2`:
* the window dies if its first cell equals the lattice cell `lx` at `x`;
* ascending pass from the lattice carry `asc0` gives digits `u0, u1`;
* for each guess `high in {0,1}` of the descending carry entering from above, the descending pass gives digits
  `dn0, dn1` and the carry `ds0` into column `x-1`; the guess is discarded if (`gam = 0` or the lattice cell
  `left` at `x-1` is 9) and `ds0` differs from the lattice descending carry `ld`;
* the new window is `u + partner`, where partner = `dn` (gam = 0) or `(left + ds0) % 10, dn0` (gam = 1);
* it is kept only if its first cell differs from the lattice cell `nx` at phase `t+1`. -/
def succ2 (lx left nx asc0 ld g a b : Nat) : List Nat :=
  if a == lx then [] else
  let u0 := (a + asc0) % 10
  let u1 := (b + (a + asc0) / 10) % 10
  let one : Nat → Option Nat := fun high =>
    let ds1 := (b + high) / 10
    let dn1 := (b + high) % 10
    let dn0 := (a + ds1) % 10
    let ds0 := (a + ds1) / 10
    if (g == 0 || left == 9) && ds0 != ld then none else
    let n0 := u0 + (if g == 0 then dn0 else (left + ds0) % 10)
    let n1 := u1 + (if g == 0 then dn1 else dn0)
    if n0 != nx then some (n0 + 19 * n1) else none
  [one 0, one 1].filterMap id

/-- the transfer graph `G_2(j)` at defect column `x = 119 + j`: for each phase `t < 8` and window `(a, b)` with
`a` off the lattice, the node key `t*361 + 19*b + a` and the keys of its successors. -/
def table2 (j : Nat) : List (Nat × List Nat) :=
  (List.range 8).flatMap fun t =>
    let x := 119 + j
    let lx := lat t x
    let left := lat t (x - 1)
    let nx := lat (t + 1) x
    let asc0 := carryBelow t 60 (x - 1)
    let ld := carryAbove t 60 x
    let g := gam t
    (List.range 19).flatMap fun b => (List.range 19).filterMap fun a =>
      if a == lx then none
      else some (t * 361 + 19 * b + a, (succ2 lx left nx asc0 ld g a b).map fun w => ((t + 1) % 8) * 361 + w)

/-- bitmask of the keys of a table -/
def maskOf (T : List (Nat × List Nat)) : Nat := T.foldl (fun m e => m ||| (1 <<< e.1)) 0

/-- keep the nodes having a successor among the current nodes -/
def aliveStep (T : List (Nat × List Nat)) : List (Nat × List Nat) :=
  let m := maskOf T
  T.filter fun e => e.2.any fun p => (m / 2 ^ p) % 2 == 1

/-- nodes with a path of at least `n` transitions -/
def alive : Nat → List (Nat × List Nat) → List (Nat × List Nat)
  | 0, T => T
  | n + 1, T => aliveStep (alive n T)

theorem k2_j0_acyclic : (alive 15 (table2 0)).isEmpty = true ∧ (alive 14 (table2 0)).isEmpty = false := by
  decide +kernel

theorem k2_j3_acyclic : (alive 21 (table2 3)).isEmpty = true ∧ (alive 20 (table2 3)).isEmpty = false := by
  decide +kernel

theorem k2_j5_acyclic : (alive 15 (table2 5)).isEmpty = true ∧ (alive 14 (table2 5)).isEmpty = false := by
  decide +kernel

theorem k2_j8_acyclic : (alive 21 (table2 8)).isEmpty = true ∧ (alive 20 (table2 8)).isEmpty = false := by
  decide +kernel

theorem k2_j10_acyclic : (alive 15 (table2 10)).isEmpty = true ∧ (alive 14 (table2 10)).isEmpty = false := by
  decide +kernel

theorem k2_j13_acyclic : (alive 21 (table2 13)).isEmpty = true ∧ (alive 20 (table2 13)).isEmpty = false := by
  decide +kernel

theorem k2_j15_acyclic : (alive 15 (table2 15)).isEmpty = true ∧ (alive 14 (table2 15)).isEmpty = false := by
  decide +kernel

theorem k2_j18_acyclic : (alive 21 (table2 18)).isEmpty = true ∧ (alive 20 (table2 18)).isEmpty = false := by
  decide +kernel

end K1Stationary

#print axioms K1Stationary.k2_j0_acyclic
#print axioms K1Stationary.k2_j3_acyclic
#print axioms K1Stationary.k2_j5_acyclic
#print axioms K1Stationary.k2_j8_acyclic
#print axioms K1Stationary.k2_j10_acyclic
#print axioms K1Stationary.k2_j13_acyclic
#print axioms K1Stationary.k2_j15_acyclic
#print axioms K1Stationary.k2_j18_acyclic
