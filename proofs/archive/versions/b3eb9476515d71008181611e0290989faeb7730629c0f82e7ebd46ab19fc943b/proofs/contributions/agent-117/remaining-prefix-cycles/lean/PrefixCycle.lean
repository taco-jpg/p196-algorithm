import PrefixInverse
import FastInverse
import PrefixCertificate
import ActualPrefix

/-!
# Backward cycles in the finite-prefix abstraction (Agent #117)

Agent #104's prefix certificates (`SevenColumn.Certificate`) bound palindrome
ancestry by a rank tree whose rows are closed under the executable inverse
`SevenColumn.prefixPredecessors` with strict rank descent.  This file proves
the corresponding *impossibility* interface: if the backward closure of a word
`p` under that inverse contains a directed cycle, then no checked rank tree can
contain `p` at all.  The cycle and the entry path are supplied as explicit
witnesses checked by kernel evaluation of the *forward* map
`SevenColumnProjection.forwardPrefix` (two scans of the prefix), and a generic
lemma shows that every forward edge of that map is an edge of the executable
inverse, so the witness certifies genuine `prefixPredecessors` edges.

Nothing here is a statement about 196, about any palindrome class, or about
actual orbits: a cycle of the abstraction only shows that *this proof method*
cannot close the class, because the abstraction is an over-approximation.
-/

namespace Agent117

open SevenColumn SevenColumn.Certificate SevenColumnProjection

/-! ## Forward edges are inverse edges -/

theorem highDigits_carry_lt {s : List Nat} {e : Nat}
    (hs : ∀ a ∈ s, a < 19) (he : e < 2) : (highDigits s e).1 < 2 := by
  induction s with
  | nil => simpa [highDigits] using he
  | cons a s ih =>
      have ha : a < 19 := hs a (List.mem_cons_self ..)
      have hs' : ∀ b ∈ s, b < 19 := fun b hb => hs b (List.mem_cons_of_mem _ hb)
      have ht := ih hs'
      simp only [highDigits]
      exact carry_lt_two ha ht

/-- The no-overflow column equations hold along both deterministic scans. -/
theorem noOverflow_of_scans (s : List Nat) (x e : Nat)
    (hs : ∀ a ∈ s, a < 19) (he : e < 2) :
    NoOverflow (List.zipWith (· + ·) (lowDigits s x) (highDigits s e).2) s x
      (highDigits s e).1 := by
  induction s generalizing x with
  | nil => exact NoOverflow.nil x e
  | cons a s ih =>
      have ha : a < 19 := hs a (List.mem_cons_self ..)
      have hs' : ∀ b ∈ s, b < 19 := fun b hb => hs b (List.mem_cons_of_mem _ hb)
      have ht := highDigits_carry_lt hs' he
      simp only [lowDigits, highDigits, List.zipWith_cons_cons]
      exact NoOverflow.cons ha ht rfl rfl (ih (carry a x) hs')

/-- The shifted overflow column equations hold along both scans. -/
theorem overflowTail_of_scans (s : List Nat) (prev x e : Nat)
    (hs : ∀ a ∈ s, a < 19) (he : e < 2) :
    OverflowTail (List.zipWith (· + ·) (lowDigits s x)
        (lowDigit prev (highDigits s e).1 :: (highDigits s e).2)) s prev x
      (carry prev (highDigits s e).1) := by
  induction s generalizing prev x with
  | nil => exact OverflowTail.nil ⟨e, he, rfl⟩
  | cons a s ih =>
      have ha : a < 19 := hs a (List.mem_cons_self ..)
      have hs' : ∀ b ∈ s, b < 19 := fun b hb => hs b (List.mem_cons_of_mem _ hb)
      have ht := highDigits_carry_lt hs' he
      simp only [lowDigits, highDigits, List.zipWith_cons_cons]
      exact OverflowTail.cons ha (carry_lt_two ha ht) rfl rfl (ih a (carry a x) hs')

theorem highDigits_cons (a : Nat) (s : List Nat) (e : Nat) :
    highDigits (a :: s) e =
      (carry a (highDigits s e).1, lowDigit a (highDigits s e).1 :: (highDigits s e).2) := rfl

theorem lowDigits_cons (a : Nat) (s : List Nat) (x : Nat) :
    lowDigits (a :: s) x = lowDigit a x :: lowDigits s (carry a x) := rfl

/-- Every edge of the forward prefix map with a boundary carry `e < 2` is an
edge of the executable inverse: the semantic relation `ForwardAdmitted` is
contained in `prefixPredecessors` membership. -/
theorem forwardPrefix_longCompatible {s : List Nat} {e : Nat}
    (hs : ∀ a ∈ s, a < 19) (hpos : 0 < s.headD 0) (he : e < 2) :
    LongCompatible (forwardPrefix s e) s := by
  cases s with
  | nil => simp at hpos
  | cons a s =>
      have ha : a < 19 := hs a (List.mem_cons_self ..)
      have hs' : ∀ b ∈ s, b < 19 := fun b hb => hs b (List.mem_cons_of_mem _ hb)
      have hpos' : 0 < a := by simpa using hpos
      have ht := highDigits_carry_lt hs' he
      have hall := noOverflow_of_scans (a :: s) 0 e hs he
      have htail := overflowTail_of_scans s a (carry a 0) e hs' he
      rw [highDigits_cons] at hall
      simp only [forwardPrefix]
      rw [highDigits_cons, lowDigits_cons]
      dsimp only at hall ⊢
      by_cases hg : carry a (highDigits s e).1 = 0
      · rw [if_pos hg]
        rw [hg] at hall
        rw [lowDigits_cons] at hall
        exact LongCompatible.noOverflow hpos' hall
      · rw [if_neg hg]
        have hg1 : carry a (highDigits s e).1 = 1 := by
          have := carry_lt_two ha ht; omega
        rw [hg1] at htail
        rw [List.zipWith_cons_cons]
        exact LongCompatible.overflow hpos' ha (Nat.add_comm _ _) htail

theorem forwardPrefix_mem_prefixPredecessors {s : List Nat} {e : Nat}
    (hs : ∀ a ∈ s, a < 19) (hpos : 0 < s.headD 0) (he : e < 2) :
    s ∈ prefixPredecessors (forwardPrefix s e) :=
  longCompatible_mem_prefixPredecessors (forwardPrefix_longCompatible hs hpos he)

theorem forwardAdmitted_mem_prefixPredecessors {s p : List Nat}
    (hs : ∀ a ∈ s, a < 19) (hpos : 0 < s.headD 0) (h : ForwardAdmitted s p) :
    s ∈ prefixPredecessors p := by
  obtain ⟨e, he, rfl⟩ := h
  exact forwardPrefix_mem_prefixPredecessors hs hpos (by omega)

/-! ## Executable witness checker -/

/-- One backward step of a witness: the next word `s` reaches the current
word `p` under the forward map with boundary carry `e`. -/
def edgeOK (p s : List Nat) (e : Nat) : Bool :=
  decide (e < 2) && s.all (fun a => decide (a < 19)) && decide (0 < s.headD 0) &&
    forwardPrefix s e == p

/-- A backward walk `p₀, p₁, …` given with the carries of its forward edges:
`(p₀, e₀), (p₁, e₁), …` where `forwardPrefix p₁ e₁ = p₀`, and so on.
The carry stored with the last word is unused. -/
def walkOK : List (List Nat × Nat) → Bool
  | (p, _) :: (s, e) :: rest => edgeOK p s e && walkOK ((s, e) :: rest)
  | _ => true

/-- The backward relation certified by the rank-tree machinery. -/
def Back (p q : List Nat) : Prop := q ∈ prefixPredecessors p

theorem edgeOK_sound {p s : List Nat} {e : Nat} (h : edgeOK p s e = true) :
    Back p s := by
  unfold edgeOK at h
  simp only [Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true, beq_iff_eq] at h
  obtain ⟨⟨⟨he, hs⟩, hpos⟩, hp⟩ := h
  rw [← hp]
  exact forwardPrefix_mem_prefixPredecessors hs hpos he

/-- A verified walk gives a `BackPath` of its length from its first word to
its last word. -/
theorem walkOK_sound : ∀ (w : List (List Nat × Nat)) (p : List Nat) (e : Nat),
    walkOK ((p, e) :: w) = true →
    BackPath Back w.length p ((w.getLastD (p, e)).1)
  | [], p, e, _ => BackPath.refl p
  | (s, es) :: rest, p, e, h => by
      simp only [walkOK, Bool.and_eq_true] at h
      have ih := walkOK_sound rest s es h.2
      simp only [List.length_cons, List.getLastD_cons]
      exact BackPath.step (edgeOK_sound h.1) ih

theorem backPath_trans {R : Word → Word → Prop} {m n : Nat} {p q z : Word}
    (h1 : BackPath R m p q) (h2 : BackPath R n q z) :
    BackPath R (m + n) p z := by
  induction h1 with
  | refl p => simpa using h2
  | step edge _ ih =>
      have := BackPath.step edge (ih h2)
      simpa [Nat.add_right_comm] using this

/-- Pumping a closed backward walk. -/
theorem backPath_cycle_pow {R : Word → Word → Prop} {n : Nat} {z : Word}
    (h : BackPath R n z z) : ∀ m, BackPath R (m * n) z z
  | 0 => by simpa using BackPath.refl z
  | m + 1 => by
      have := backPath_trans h (backPath_cycle_pow h m)
      simpa [Nat.succ_mul, Nat.add_comm] using this

/-! ## No checked rank tree contains a word with a reachable backward cycle -/

/-- If `p` reaches `z` backward and `z` lies on a backward cycle of positive
length, then `p` is absent from every tree all of whose rows are checked
against the executable inverse. -/
theorem lookup_none_of_cycle {tree : RankTree}
    (checked : CheckedRows tree prefixPredecessors)
    {m n : Nat} {p z : Word} (entry : BackPath Back m p z)
    (cycle : BackPath Back n z z) (hn : 0 < n) :
    lookup tree p = none := by
  cases hl : lookup tree p with
  | none => rfl
  | some r =>
      have path := backPath_trans entry (backPath_cycle_pow cycle (r + 1))
      obtain ⟨s, _, hs⟩ := backPath_rank checked (fun _ _ h => h) path hl
      have : r + 1 ≤ (r + 1) * n := Nat.le_mul_of_pos_right _ hn
      omega

/-- Consequently no initial check can succeed for such a word, whatever the
claimed bound. -/
theorem checkInitial_false_of_cycle {tree : RankTree}
    (checked : CheckedRows tree prefixPredecessors)
    {m n : Nat} {p z : Word} (entry : BackPath Back m p z)
    (cycle : BackPath Back n z z) (hn : 0 < n) (bound : Nat) :
    checkInitial tree bound p = false := by
  unfold checkInitial
  rw [lookup_none_of_cycle checked entry cycle hn]

/-- Witness form: an entry walk `(p, _) :: … :: (z, _)` and a closed walk
`(z, _) :: … :: (z, _)` of positive length, both verified by `walkOK`. -/
theorem lookup_none_of_walks {tree : RankTree}
    (checked : CheckedRows tree prefixPredecessors)
    (entry cycle : List (List Nat × Nat)) (p z : List Nat) (ep ez : Nat)
    (hentry : walkOK ((p, ep) :: entry) = true)
    (hz : (entry.getLastD (p, ep)).1 = z)
    (hcycle : walkOK ((z, ez) :: cycle) = true)
    (hclose : (cycle.getLastD (z, ez)).1 = z)
    (hpos : 0 < cycle.length) :
    lookup tree p = none := by
  have h1 := walkOK_sound entry p ep hentry
  have h2 := walkOK_sound cycle z ez hcycle
  rw [hz] at h1
  rw [hclose] at h2
  exact lookup_none_of_cycle checked h1 h2 hpos

end Agent117

#print axioms Agent117.forwardPrefix_mem_prefixPredecessors
#print axioms Agent117.forwardAdmitted_mem_prefixPredecessors
#print axioms Agent117.walkOK_sound
#print axioms Agent117.lookup_none_of_cycle
#print axioms Agent117.checkInitial_false_of_cycle
#print axioms Agent117.lookup_none_of_walks

namespace Agent117

/-- Base-19 little-endian unpacking of `k` pair sums. -/
def unpackWord : Nat → Nat → List Nat
  | 0, _ => []
  | i + 1, m => m % 19 :: unpackWord i (m / 19)

/-- A packed witness row: the forward carry is the low bit, the word above it. -/
def unpack (k n : Nat) : List Nat × Nat := (unpackWord k (n / 2), n % 2)

end Agent117
