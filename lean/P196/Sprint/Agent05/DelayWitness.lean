import P196.Agent117P2641.Agent124PrefixL

/-!
# Delay witnesses bound every prefix certificate from below (sprint agent 05)

Every Agent124 prefix certificate for a digit list `pre` delivers, through
`Agent124.PrefixL.ancestry_of_entries`, a uniform ancestry bound: if
`orbit A t` is a palindrome beginning with `pre` (any positive `A`, any `t`,
first hit or not) then `t ≤ b + 1`, where `b` is the entry's rank bound.

This module proves the converse obstruction. A single positive seed `A` and a
time `t` such that `orbit A t` is a palindrome beginning with `pre` force

* every uniform ancestry bound for `pre` to be at least `t`
  (`le_of_witness`);
* every entry `(pre, b)` accepted by `entryOK` to have `t ≤ b + 1`
  (`entry_bound_ge_of_witness`), for every width `k` and every rank function
  satisfying `RowsClosed`/`ShortClosed`;
* in particular, when `N < t`, no entry list that passes both checks of
  `no_196_of_entries` with base check `N` (bounds `b + 1 ≤ N`) contains `pre`
  (`not_mem_entries_of_witness`); the repository's `no_196_of_entries` uses
  `N = 100`.

Witnesses are given as data and checked by a Boolean function `witnessOK`
evaluated by the kernel; `witnessOK_sound` turns a passing check into the
real `PalStartsL` statement for the unchanged `orbit`.

Nothing here is about the orbit of 196 beyond limiting what the prefix method
can prove; nothing here asserts that 196 is or is not a Lychrel number.
-/

namespace Sprint.Agent05

open Lychrel196 DecimalDigits Agent124.PrefixR Agent124.PrefixL

/-- The conclusion delivered by a prefix certificate: uniform ancestry bound `B`. -/
def AncestryBound (pre : List Nat) (B : Nat) : Prop :=
  ∀ A P t, 0 < A → PalStartsL pre P → orbit A t = P → t ≤ B

/-- A realized delay is a lower bound for every uniform ancestry bound. -/
theorem le_of_witness {pre : List Nat} {B A t : Nat} (h : AncestryBound pre B)
    (hA : 0 < A) (hw : PalStartsL pre (orbit A t)) : t ≤ B :=
  h A (orbit A t) t hA hw rfl

/-- Any accepted certificate entry `(pre, b)` (any width `k`, any closed rank
function) satisfies `t ≤ b + 1` for every realized delay `t` to `pre`. -/
theorem entry_bound_ge_of_witness (k : Nat) (R : List Nat → Option Nat)
    (rows : RowsClosed k R) (short : ShortClosed k R) (pre : List Nat) (b : Nat)
    (hok : entryOK k R (pre, b) = true) {A t : Nat} (hA : 0 < A)
    (hw : PalStartsL pre (orbit A t)) : t ≤ b + 1 := by
  have hall : [(pre, b)].all (entryOK k R) = true := by simp [hok]
  exact ancestry_of_entries k R rows short [(pre, b)] hall (pre, b) (by simp)
    A (orbit A t) t hA hw rfl

/-- Base check `N`: an entry list passing `entryOK` and the bound check
`b + 1 ≤ N` (the two premises of `no_196_of_entries`, which uses `N = 100`)
cannot contain `pre` with any bound, once a delay `t > N` to `pre` is realized. -/
theorem not_mem_entries_of_witness (k : Nat) (R : List Nat → Option Nat)
    (rows : RowsClosed k R) (short : ShortClosed k R)
    (entries : List (List Nat × Nat)) (h : entries.all (entryOK k R) = true)
    (N : Nat) (hb : entries.all (fun e => Nat.ble (e.2 + 1) N) = true)
    (pre : List Nat) {A t : Nat} (hA : 0 < A) (hw : PalStartsL pre (orbit A t))
    (ht : N < t) : ∀ b, (pre, b) ∉ entries := by
  intro b hmem
  have h1 := List.all_eq_true.mp h _ hmem
  have h2 : b + 1 ≤ N := by
    simpa [Nat.ble_eq] using List.all_eq_true.mp hb _ hmem
  have := entry_bound_ge_of_witness k R rows short pre b h1 hA hw
  omega

/-- A palindrome beginning with `pre ++ more` begins with `pre`. -/
theorem palStartsL_of_append {pre more : List Nat} {P : Nat}
    (h : PalStartsL (pre ++ more) P) : PalStartsL pre P := by
  obtain ⟨hp, e, W, hc, hW, hd⟩ := h
  refine ⟨hp, e, W, hc, by simp at hW; omega, ?_⟩
  intro i hi
  have h' := hd i (by simp; omega)
  rw [h']
  simp only [List.getD_eq_getElem?_getD, List.getElem?_append_left hi]

/-- A palindrome beginning with `pre` begins with every prefix `pre.take j`. -/
theorem palStartsL_take {pre : List Nat} {P : Nat} (j : Nat)
    (h : PalStartsL pre P) : PalStartsL (pre.take j) P := by
  rw [← List.take_append_drop j pre] at h
  exact palStartsL_of_append h

/-! ## Kernel-checked witness data -/

/-- A delay witness: positive `seed`, time `t`, and the expected iterate `P`
of exact width `W`. All fields are untrusted data checked by `witnessOK`. -/
structure Witness where
  pre : List Nat
  seed : Nat
  t : Nat
  P : Nat
  W : Nat

/-- Decimal digit `i` (units = 0). -/
def digitAt (P i : Nat) : Nat := P / 10 ^ i % 10

/-- Boolean check: positive seed, `orbit seed t = P`, `P` a palindrome with
exact width `W` and leading digits `pre`. -/
def witnessOK (w : Witness) : Bool :=
  Nat.ble 1 w.seed && (orbit w.seed w.t == w.P) && (reverse10 w.P == w.P) &&
    Nat.ble 1 w.W && Nat.ble 1 (digitAt w.P (w.W - 1)) &&
    (value (digitAt w.P) w.W == w.P) && Nat.ble w.pre.length w.W &&
    (List.range w.pre.length).all (fun i => digitAt w.P (w.W - 1 - i) == w.pre.getD i 0)

/-- Soundness of the witness check. -/
theorem witnessOK_sound (w : Witness) (h : witnessOK w = true) :
    0 < w.seed ∧ PalStartsL w.pre (orbit w.seed w.t) := by
  simp only [witnessOK, Bool.and_eq_true, Nat.ble_eq, beq_iff_eq, List.all_eq_true,
    List.mem_range] at h
  obtain ⟨⟨⟨⟨⟨⟨⟨h1, h2⟩, h3⟩, h4⟩, h5⟩, h6⟩, h7⟩, h8⟩ := h
  refine ⟨by omega, ?_⟩
  rw [h2]
  refine ⟨h3, digitAt w.P, w.W, ⟨by omega, ?_, by omega, h6⟩, h7, ?_⟩
  · intro i _
    exact Nat.le_of_lt_succ (Nat.mod_lt _ (by decide))
  · intro i hi
    exact h8 i hi

/-- A checked witness bounds every accepted entry for its prefix from below. -/
theorem entry_bound_ge_of_witnessOK (w : Witness) (hw : witnessOK w = true)
    (k : Nat) (R : List Nat → Option Nat) (rows : RowsClosed k R)
    (short : ShortClosed k R) (b : Nat) (hok : entryOK k R (w.pre, b) = true) :
    w.t ≤ b + 1 := by
  obtain ⟨hA, hP⟩ := witnessOK_sound w hw
  exact entry_bound_ge_of_witness k R rows short w.pre b hok hA hP

/-- The same for every shorter prefix `w.pre.take j` (e.g. the three- and
two-digit parents of a four-digit witness). -/
theorem not_mem_entries_take_of_witnessOK (w : Witness) (hw : witnessOK w = true)
    (k : Nat) (R : List Nat → Option Nat) (rows : RowsClosed k R)
    (short : ShortClosed k R) (entries : List (List Nat × Nat))
    (h : entries.all (entryOK k R) = true) (N : Nat)
    (hb : entries.all (fun e => Nat.ble (e.2 + 1) N) = true) (ht : N < w.t) (j : Nat) :
    ∀ b, (w.pre.take j, b) ∉ entries := by
  obtain ⟨hA, hP⟩ := witnessOK_sound w hw
  exact not_mem_entries_of_witness k R rows short entries h N hb (w.pre.take j) hA
    (palStartsL_take j hP) ht

/-- A checked witness with `N < t` keeps its prefix out of every entry list
that passes the premises of `no_196_of_entries` with base check `N`. -/
theorem not_mem_entries_of_witnessOK (w : Witness) (hw : witnessOK w = true)
    (k : Nat) (R : List Nat → Option Nat) (rows : RowsClosed k R)
    (short : ShortClosed k R) (entries : List (List Nat × Nat))
    (h : entries.all (entryOK k R) = true) (N : Nat)
    (hb : entries.all (fun e => Nat.ble (e.2 + 1) N) = true) (ht : N < w.t) :
    ∀ b, (w.pre, b) ∉ entries := by
  obtain ⟨hA, hP⟩ := witnessOK_sound w hw
  exact not_mem_entries_of_witness k R rows short entries h N hb w.pre hA hP ht

end Sprint.Agent05

#print axioms Sprint.Agent05.le_of_witness
#print axioms Sprint.Agent05.entry_bound_ge_of_witness
#print axioms Sprint.Agent05.not_mem_entries_of_witness
#print axioms Sprint.Agent05.palStartsL_of_append
#print axioms Sprint.Agent05.witnessOK_sound
#print axioms Sprint.Agent05.entry_bound_ge_of_witnessOK
#print axioms Sprint.Agent05.not_mem_entries_of_witnessOK
#print axioms Sprint.Agent05.palStartsL_take
#print axioms Sprint.Agent05.not_mem_entries_take_of_witnessOK
