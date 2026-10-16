import Agent9FiniteProducts
import Agent101SplitEnumeration

/-!
All ordinary decimal digit choices for the selected mirrored markers.
An allowed block excludes the single simultaneous all-nine filling.
Agent101's unchanged digit wrapping interfaces are reused throughout.
-/

namespace P196.Agent9.Ensemble

open Agent101

def pairAlphabet : List (Nat × Nat) :=
  (List.range 10).flatMap fun a => (List.range 10).map fun b => (a, b)

def outerAlphabet : List (Nat × Nat) :=
  (List.range 10).flatMap fun a => (List.range' 1 9).map fun b => (a, b)

theorem mem_pairAlphabet (p : Nat × Nat) :
    p ∈ pairAlphabet ↔ p.1 ≤ 9 ∧ p.2 ≤ 9 := by
  rcases p with ⟨a, b⟩
  simp [pairAlphabet, List.mem_flatMap, List.mem_map]
  omega

theorem mem_outerAlphabet (p : Nat × Nat) :
    p ∈ outerAlphabet ↔ p.1 ≤ 9 ∧ p.2 ≤ 9 ∧ 0 < p.2 := by
  rcases p with ⟨a, b⟩
  simp [outerAlphabet, List.mem_flatMap, List.mem_map]
  omega

theorem pairAlphabet_nodup : pairAlphabet.Nodup := by decide
theorem outerAlphabet_nodup : outerAlphabet.Nodup := by decide
theorem length_pairAlphabet : pairAlphabet.length = 100 := by decide
theorem length_outerAlphabet : outerAlphabet.length = 90 := by decide

def goodBlocks (r : Nat) : List (List (Nat × Nat)) :=
  (wordChoices pairAlphabet r).erase (List.replicate r (9, 9))

theorem nines_mem_wordChoices (r : Nat) :
    List.replicate r (9, 9) ∈ wordChoices pairAlphabet r := by
  apply (mem_wordChoices _ _ _).mpr
  refine ⟨by simp, ?_⟩
  intro p hp
  have hp' := (List.mem_replicate.mp hp).2
  subst p
  exact (mem_pairAlphabet _).mpr ⟨by decide, by decide⟩

theorem mem_goodBlocks (r : Nat) (ps : List (Nat × Nat)) :
    ps ∈ goodBlocks r ↔ ps.length = r ∧
      (∀ p ∈ ps, p ∈ pairAlphabet) ∧ ps ≠ List.replicate r (9, 9) := by
  rw [goodBlocks, (wordChoices_nodup pairAlphabet pairAlphabet_nodup r).mem_erase_iff,
    mem_wordChoices]
  simp only [and_assoc, and_left_comm, and_comm]

theorem goodBlocks_nodup (r : Nat) : (goodBlocks r).Nodup :=
  List.Nodup.erase _ (wordChoices_nodup _ pairAlphabet_nodup r)

theorem goodBlocks_word_length (r : Nat) (ps : List (Nat × Nat))
    (hp : ps ∈ goodBlocks r) : ps.length = r :=
  ((mem_goodBlocks r ps).mp hp).1

theorem length_goodBlocks (r : Nat) : (goodBlocks r).length = 10 ^ (2 * r) - 1 := by
  rw [goodBlocks, List.length_erase_of_mem (nines_mem_wordChoices r),
    length_wordChoices, length_pairAlphabet, Nat.pow_mul]

def wrapPairs : List (Nat × Nat) → List Nat → List Nat
  | [], ds => ds
  | p :: ps, ds => wrapDigits p.1 p.2 (wrapPairs ps ds)

theorem length_wrapPairs (ps : List (Nat × Nat)) (ds : List Nat) :
    (wrapPairs ps ds).length = 2 * ps.length + ds.length := by
  induction ps with
  | nil => simp [wrapPairs]
  | cons p ps ih =>
    rw [wrapPairs, length_wrapDigits, ih, List.length_cons]
    omega

theorem wrapPairs_append (ps qs : List (Nat × Nat)) (ds : List Nat) :
    wrapPairs (ps ++ qs) ds = wrapPairs ps (wrapPairs qs ds) := by
  induction ps with
  | nil => rfl
  | cons p ps ih => simp only [List.cons_append, wrapPairs, ih]

theorem wrapPairs_injective (ps qs : List (Nat × Nat)) (ds es : List Nat)
    (hlen : ps.length = qs.length) (heq : wrapPairs ps ds = wrapPairs qs es) :
    ps = qs ∧ ds = es := by
  induction ps generalizing qs with
  | nil =>
    have hq : qs = [] := List.length_eq_zero_iff.mp hlen.symm
    subst qs
    exact ⟨rfl, heq⟩
  | cons p ps ih =>
    cases qs with
    | nil => simp at hlen
    | cons q qs =>
      obtain ⟨ha, hb, hi⟩ := wrapDigits_injective _ _ _ _ _ _ heq
      obtain ⟨hp, hd⟩ := ih qs (by simpa using hlen) hi
      have hpq : p = q := Prod.ext ha hb
      exact ⟨by rw [hpq, hp], hd⟩

theorem digitsBounded_wrapPairs (ps : List (Nat × Nat)) (ds : List Nat) :
    digitsBounded (wrapPairs ps ds) ↔
      (∀ p ∈ ps, p ∈ pairAlphabet) ∧ digitsBounded ds := by
  induction ps with
  | nil => simp [wrapPairs]
  | cons p ps ih =>
    simp only [wrapPairs, digitsBounded_wrapDigits, ih, List.mem_cons,
      forall_eq_or_imp, mem_pairAlphabet]
    simp only [and_assoc, and_left_comm, and_comm]

theorem wrapPairs_low (ps : List (Nat × Nat)) (ds : List Nat)
    (i : Nat) (hi : i < ps.length) :
    (wrapPairs ps ds)[i]? = some ps[i].1 := by
  induction ps generalizing i with
  | nil => simp at hi
  | cons p ps ih =>
    cases i with
    | zero => simp [wrapPairs, wrapDigits]
    | succ i =>
      have hip : i < ps.length := by simpa using hi
      simp only [wrapPairs, wrapDigits, List.getElem?_cons_succ, List.getElem_cons_succ]
      rw [List.getElem?_append_left (by rw [length_wrapPairs]; omega)]
      exact ih i hip

theorem wrapPairs_high (ps : List (Nat × Nat)) (ds : List Nat)
    (i : Nat) (hi : i < ps.length) :
    (wrapPairs ps ds)[(wrapPairs ps ds).length - 1 - i]? = some ps[i].2 := by
  induction ps generalizing i with
  | nil => simp at hi
  | cons p ps ih =>
    cases i with
    | zero =>
      rw [show (wrapPairs (p :: ps) ds).length - 1 - 0 =
        (wrapPairs ps ds).length + 1 by rw [length_wrapPairs, length_wrapPairs]; simp; omega]
      simp [wrapPairs, wrapDigits]
    | succ i =>
      have hip : i < ps.length := by simpa using hi
      rw [show (wrapPairs (p :: ps) ds).length - 1 - (i + 1) =
        ((wrapPairs ps ds).length - 1 - i) + 1 by
          rw [length_wrapPairs, length_wrapPairs]; simp only [List.length_cons]; omega]
      simp only [wrapPairs, wrapDigits, List.getElem?_cons_succ, List.getElem_cons_succ]
      rw [List.getElem?_append_left (by rw [length_wrapPairs]; omega)]
      exact ih i hip

theorem exists_wrapPairs (ds : List Nat) (m e : Nat)
    (hlen : ds.length = 2 * m + e) :
    ∃ ps cs, ps.length = m ∧ cs.length = e ∧ ds = wrapPairs ps cs := by
  induction m generalizing ds with
  | zero => exact ⟨[], ds, rfl, by simpa using hlen, rfl⟩
  | succ m ih =>
    obtain ⟨a, b, inner, rfl⟩ := exists_wrapDigits ds (by omega)
    have hi : inner.length = 2 * m + e := by
      rw [length_wrapDigits] at hlen
      omega
    obtain ⟨ps, cs, hp, hc, heq⟩ := ih inner hi
    exact ⟨(a, b) :: ps, cs, by simp [hp], hc, by simp [wrapPairs, ← heq]⟩

def wrappedPairsProduct (frames : List (List (Nat × Nat))) (centers : List (List Nat)) :
    List (List Nat) := frames.flatMap fun ps => centers.map (wrapPairs ps)

theorem wrappedPairsProduct_nodup (frames : List (List (Nat × Nat)))
    (centers : List (List Nat)) (m : Nat) (hf : frames.Nodup) (hc : centers.Nodup)
    (hl : ∀ ps ∈ frames, ps.length = m) : (wrappedPairsProduct frames centers).Nodup := by
  apply nodup_flatMap_map frames centers wrapPairs hf hc
  intro ps hp qs hq ds _ es _ heq
  exact wrapPairs_injective ps qs ds es ((hl ps hp).trans (hl qs hq).symm) heq

theorem length_wrappedPairsProduct (frames : List (List (Nat × Nat)))
    (centers : List (List Nat)) :
    (wrappedPairsProduct frames centers).length = frames.length * centers.length :=
  length_flatMap_map frames centers wrapPairs

end P196.Agent9.Ensemble
