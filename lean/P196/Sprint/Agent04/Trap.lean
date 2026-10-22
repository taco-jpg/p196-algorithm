import P196.Agent117RemainingCycles.PrefixCycle
import P196.Agent117P2641.Agent124PrefixL

/-!
# Sprint agent 04: cycles of the width-k prefix abstraction against the rank interface

The batch prefix certificates (`Agent124.PrefixL.entryOK` / `no_196_of_entries`) consume an abstract
rank function `R` with `Agent124.PrefixR.RowsClosed k R` (rank strictly decreases along every long
backward edge `longPred k`).  Agent #117 showed for the older `RankTree` interface that a backward
cycle reachable from a word excludes that word from every checked tree.  This file proves the same
for the `RowsClosed` interface and adds the shortest cycle of the width-7 abstraction:

* `walkOKk k` checks a backward walk whose every word has width `k` and entries below 19
  (each step is a forward edge `forwardPrefix s e = p`, re-using `Agent117.edgeOK`).
* `R_none_of_walks`: if `p` reaches a closed walk backward, `R p = none` for every `RowsClosed k R`.
* `entryOK_false_of_none`: then no `entryOK` check succeeds for a prefix having `p` as an initial word,
  whatever the claimed bound.
* `cycle7`: a closed backward walk of length 7 through `z7 = [10, 2, 3, 2, 7, 5, 0]` at width 7
  (by computation in the sprint scripts this is the unique shortest simple cycle at width 7; that
  minimality is NOT proved here).

Method-limit statements only: nothing here is about palindromes in the orbit of 196.
-/

namespace Sprint04

open SevenColumn SevenColumn.Certificate SevenColumnProjection Agent117
open Agent124.PrefixR Agent124.PrefixL

/-- Long backward edge at width `k`, as consumed by `RowsClosed k`. -/
def LongBack (k : Nat) (p q : List Nat) : Prop :=
  (∀ x ∈ p, x < 19) ∧ q ∈ longPred k p

/-- One checked backward step at width `k`. -/
def edgeOKk (k : Nat) (p s : List Nat) (e : Nat) : Bool :=
  decide (p.length = k) && p.all (fun a => decide (a < 19)) && edgeOK p s e

/-- A backward walk `(p₀, _) :: (p₁, e₁) :: …` with `forwardPrefix p₁ e₁ = p₀`, all words of width `k`. -/
def walkOKk (k : Nat) : List (List Nat × Nat) → Bool
  | (p, _) :: (s, e) :: rest => edgeOKk k p s e && walkOKk k ((s, e) :: rest)
  | _ => true

theorem edgeOKk_sound {k : Nat} {p s : List Nat} {e : Nat} (h : edgeOKk k p s e = true) :
    LongBack k p s := by
  unfold edgeOKk at h
  simp only [Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true] at h
  obtain ⟨⟨hlen, hp⟩, hedge⟩ := h
  refine ⟨hp, ?_⟩
  have hb : Back p s := edgeOK_sound hedge
  simp only [longPred, hlen, ↓reduceIte]
  exact hb

theorem walkOKk_sound (k : Nat) : ∀ (w : List (List Nat × Nat)) (p : List Nat) (e : Nat),
    walkOKk k ((p, e) :: w) = true →
    BackPath (LongBack k) w.length p ((w.getLastD (p, e)).1)
  | [], p, _, _ => BackPath.refl p
  | (s, es) :: rest, p, e, h => by
      simp only [walkOKk, Bool.and_eq_true] at h
      have ih := walkOKk_sound k rest s es h.2
      simp only [List.length_cons, List.getLastD_cons]
      exact BackPath.step (edgeOKk_sound h.1) ih

theorem walkOKk_tail (k : Nat) (x : List Nat × Nat) (w : List (List Nat × Nat))
    (h : walkOKk k (x :: w) = true) : walkOKk k w = true := by
  match w, h with
  | [], _ => rfl
  | (s, e) :: rest, h =>
      obtain ⟨p, ep⟩ := x
      simp only [walkOKk, Bool.and_eq_true] at h
      exact h.2

/-- Ranks of a `RowsClosed` function strictly decrease along long backward paths. -/
theorem rowsClosed_backPath {k : Nat} {R : List Nat → Option Nat} (rows : RowsClosed k R)
    {n : Nat} {p z : List Nat} (path : BackPath (LongBack k) n p z) {r : Nat}
    (hp : R p = some r) : ∃ s, R z = some s ∧ n + s ≤ r := by
  induction path generalizing r with
  | refl p => exact ⟨r, hp, by omega⟩
  | @step p q z n edge tail ih =>
      obtain ⟨t, ht, hlt⟩ := rows p r edge.1 hp q edge.2
      obtain ⟨s, hs, hle⟩ := ih ht
      exact ⟨s, hs, by omega⟩

/-- A word that reaches a backward cycle has no rank in any `RowsClosed` function. -/
theorem R_none_of_cycle {k : Nat} {R : List Nat → Option Nat} (rows : RowsClosed k R)
    {m n : Nat} {p z : List Nat} (entry : BackPath (LongBack k) m p z)
    (cycle : BackPath (LongBack k) n z z) (hn : 0 < n) : R p = none := by
  cases hr : R p with
  | none => rfl
  | some r =>
      have path := backPath_trans entry (backPath_cycle_pow cycle (r + 1))
      obtain ⟨s, _, hs⟩ := rowsClosed_backPath rows path hr
      have : r + 1 ≤ (r + 1) * n := Nat.le_mul_of_pos_right _ hn
      omega

/-- Witness form: verified entry walk and verified closed walk. -/
theorem R_none_of_walks {k : Nat} {R : List Nat → Option Nat} (rows : RowsClosed k R)
    (entry cycle : List (List Nat × Nat)) (p z : List Nat) (ep ez : Nat)
    (hentry : walkOKk k ((p, ep) :: entry) = true)
    (hz : (entry.getLastD (p, ep)).1 = z)
    (hcycle : walkOKk k ((z, ez) :: cycle) = true)
    (hclose : (cycle.getLastD (z, ez)).1 = z)
    (hpos : 0 < cycle.length) : R p = none := by
  have h1 := walkOKk_sound k entry p ep hentry
  have h2 := walkOKk_sound k cycle z ez hcycle
  rw [hz] at h1
  rw [hclose] at h2
  exact R_none_of_cycle rows h1 h2 hpos

/-- If one initial word of a prefix has no rank, no `entryOK` check for that prefix passes,
whatever the claimed bound. -/
theorem entryOK_false_of_none {k : Nat} {R : List Nat → Option Nat} (pre : List Nat) (bound : Nat)
    {p : List Nat} (hp : p ∈ initialWordsL k pre) (hR : R p = none) :
    entryOK k R (pre, bound) = false := by
  cases h : entryOK k R (pre, bound) with
  | false => rfl
  | true =>
      unfold entryOK at h
      simp only [Bool.and_eq_true] at h
      have hall := List.all_eq_true.mp h.2 p hp
      rw [hR] at hall
      exact absurd hall (by simp)

/-- Cheap membership in the initial family: a full-width word `pre ++ tail` with decimal-digit tail. -/
theorem mem_initialWordsL_of_full (k : Nat) (pre tail : List Nat)
    (hlen : pre.length + tail.length = k) (htail : ∀ x ∈ tail, x ≤ 9) :
    pre ++ tail ∈ initialWordsL k pre := by
  unfold initialWordsL
  rw [List.mem_filter]
  constructor
  · rw [List.mem_flatMap]
    refine ⟨tail.length, List.mem_range.mpr (by omega), ?_⟩
    rw [List.mem_map]
    exact ⟨tail, Agent124.PrefixK.mem_digitLists tail.length tail rfl htail, rfl⟩
  · unfold Agent124.PrefixK.initialOK
    simp [hlen]

/-! ## The shortest cycle at width 7 -/

/-- First word of the length-7 cycle (forward order 10,1,2,4,9,18,9 in the outer column). -/
def z7 : List Nat := [10, 2, 3, 2, 7, 5, 0]

/-- Backward closed walk `z7 ← … ← z7`, packed by `Agent117.unpack 7`
(base-19 little-endian word, forward carry in the low bit). -/
def cycle7Data : List Nat := [895202499, 1698540148, 849270074, 428277184, 1151414064, 532303281, 26615182]

def cycle7 : List (List Nat × Nat) := cycle7Data.map (unpack 7)

theorem cycle7_ok : walkOKk 7 ((z7, 0) :: cycle7) = true := by decide +kernel
theorem cycle7_end : (cycle7.getLastD (z7, 0)).1 = z7 := by decide +kernel
theorem cycle7_length : cycle7.length = 7 := by decide +kernel

/-- Every word whose verified backward walk ends at `z7` has no rank in any `RowsClosed 7` function. -/
theorem R_none_of_entry7 {R : List Nat → Option Nat} (rows : RowsClosed 7 R)
    (entry : List (List Nat × Nat)) (p : List Nat) (ep : Nat)
    (hentry : walkOKk 7 ((p, ep) :: entry) = true) (hz : (entry.getLastD (p, ep)).1 = z7) :
    R p = none :=
  R_none_of_walks rows entry cycle7 p z7 ep 0 hentry hz cycle7_ok cycle7_end
    (by rw [cycle7_length]; decide)

/-- Every word of a verified walk ending at `z7` has no rank (suffixes of verified walks are verified). -/
theorem R_none_of_mem_walk7 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) :
    ∀ (w : List (List Nat × Nat)), walkOKk 7 w = true → (w.getLastD ([], 0)).1 = z7 →
      ∀ x ∈ w, R x.1 = none
  | [], _, _, x, hx => by simp at hx
  | (p, ep) :: rest, hw, hz, x, hx => by
      rcases List.mem_cons.mp hx with rfl | hx'
      · apply R_none_of_entry7 rows rest p ep hw
        cases rest with
        | nil => simpa using hz
        | cons y ys =>
            simp only [List.getLastD_cons] at hz ⊢
            exact hz
      · cases rest with
        | nil => simp at hx'
        | cons y ys =>
            have hz' : ((y :: ys).getLastD ([], 0)).1 = z7 := by
              simp only [List.getLastD_cons] at hz ⊢
              exact hz
            exact R_none_of_mem_walk7 rows (y :: ys) (walkOKk_tail 7 (p, ep) _ hw) hz' x hx'

end Sprint04

#print axioms Sprint04.edgeOKk_sound
#print axioms Sprint04.walkOKk_sound
#print axioms Sprint04.rowsClosed_backPath
#print axioms Sprint04.R_none_of_cycle
#print axioms Sprint04.R_none_of_walks
#print axioms Sprint04.entryOK_false_of_none
#print axioms Sprint04.mem_initialWordsL_of_full
#print axioms Sprint04.cycle7_ok
#print axioms Sprint04.R_none_of_entry7
#print axioms Sprint04.R_none_of_mem_walk7
