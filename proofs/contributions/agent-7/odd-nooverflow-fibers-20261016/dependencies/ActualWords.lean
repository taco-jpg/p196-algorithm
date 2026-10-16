import WordBridge
import PeriodObstructions

/- Exact imported dependency: Agent8's PeriodObstructions.lean, original Git
blob a89dda20e9a9b3452f7d0272b4fbd28f7d6ce119 at source snapshot
2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5. No theorem is redefined. -/
namespace P196.Agent9.InverseFibers

set_option maxRecDepth 100000
set_option maxHeartbeats 4000000

/-- Agreement with the existing repository normalizer, including overflow. -/
theorem normalize_scan (xs : List Nat) (e : Nat) :
    Agent8.normalize xs e = (scan xs e).1 ++
      if (scan xs e).2 = 0 then [] else [(scan xs e).2] := by
  induction xs generalizing e with
  | nil => simp [Agent8.normalize, scan]
  | cons x xs ih => simp [Agent8.normalize, scan, ih]

theorem zipAdd_repository (xs ys : List Nat) :
    Agent8.zipAdd xs ys = zipAdd xs ys := by
  induction xs generalizing ys with
  | nil => cases ys <;> rfl
  | cons x xs ih => cases ys <;> simp [Agent8.zipAdd, zipAdd, ih]

theorem zipAdd_length (xs ys : List Nat) (h : xs.length = ys.length) :
    (zipAdd xs ys).length = xs.length := by
  induction xs generalizing ys with
  | nil => rfl
  | cons x xs ih =>
    cases ys with
    | nil => simp at h
    | cons y ys => simp [zipAdd, ih ys (by simpa using h)]

theorem zipAdd_append (xs ys us vs : List Nat) (h : xs.length = ys.length) :
    zipAdd (xs ++ us) (ys ++ vs) = zipAdd xs ys ++ zipAdd us vs := by
  induction xs generalizing ys with
  | nil =>
    have hy : ys = [] := by simpa using h.symm
    subst ys
    rfl
  | cons x xs ih =>
    cases ys with
    | nil => simp at h
    | cons y ys => simp [zipAdd, ih ys (by simpa using h)]

theorem zipAdd_comm (xs ys : List Nat) : zipAdd xs ys = zipAdd ys xs := by
  induction xs generalizing ys with
  | nil => cases ys <;> rfl
  | cons x xs ih => cases ys <;> simp [zipAdd, ih, Nat.add_comm]

theorem zipAdd_reverse (xs ys : List Nat) (h : xs.length = ys.length) :
    zipAdd xs.reverse ys.reverse = (zipAdd xs ys).reverse := by
  induction xs generalizing ys with
  | nil =>
    have hy : ys = [] := by simpa using h.symm
    subst ys
    rfl
  | cons x xs ih =>
    cases ys with
    | nil => simp at h
    | cons y ys =>
      simp only [List.reverse_cons, zipAdd]
      rw [zipAdd_append _ _ _ _ (by simpa using h)]
      simp [zipAdd, ih ys (by simpa using h)]

theorem pair_halves (ds es : List Nat) (h : ds.length = es.length) :
    Agent8.pair (ds ++ es.reverse) = mirror (zipAdd ds es) := by
  simp only [Agent8.pair, zipAdd_repository, List.reverse_append, List.reverse_reverse]
  rw [zipAdd_append _ _ _ _ h, zipAdd_reverse _ _ h.symm, zipAdd_comm es ds]
  rfl

/-- The existing repository transition, with its actual no-overflow condition.
Input and target are even mirrored coefficient words, not individual integers. -/
def ActualFiber (ss : List Symbol) (xs : List Nat) : Prop :=
  xs.length = ss.length ∧ (∀ x ∈ xs, x < 19) ∧
  (scan (mirror xs) 0).2 = 0 ∧
  Agent8.stepWord (mirror xs) = mirror (ss.map Fin.val)

theorem realizes_actual (ss : List Symbol) (xs : List Nat)
    (h : Realizes ss 0 xs) : ActualFiber ss xs := by
  obtain ⟨hlen, hb, ds, es, hd, he, hs, hz⟩ := h
  change scan (mirror xs) 0 = (ds ++ es.reverse, 0) at hs
  refine ⟨hlen, hb, by rw [hs], ?_⟩
  unfold Agent8.stepWord
  rw [normalize_scan, hs]
  simp only [Nat.zero_eq, ↓reduceIte, List.append_nil]
  rw [pair_halves _ _ (hd.trans he.symm), hz]

theorem actual_realizes (ss : List Symbol) (xs : List Nat)
    (h : ActualFiber ss xs) : Realizes ss 0 xs := by
  obtain ⟨hlen, hb, hc, ht⟩ := h
  let first := scan xs 0
  let second := scan xs.reverse first.2
  have hs : scan (mirror xs) 0 = (first.1 ++ second.1, second.2) := scan_append xs xs.reverse 0
  have hc' : second.2 = 0 := by simpa [hs] using hc
  have hd : first.1.length = ss.length := (scan_length xs 0).trans hlen
  have he : second.1.reverse.length = ss.length := by
    simpa [second, hlen] using scan_length xs.reverse first.2
  have hn : Agent8.normalize (mirror xs) 0 = first.1 ++ second.1 := by
    rw [normalize_scan, hs, hc']; simp
  have hpair : mirror (zipAdd first.1 second.1.reverse) = mirror (ss.map Fin.val) := by
    have hp := pair_halves first.1 second.1.reverse (hd.trans he.symm)
    simp only [List.reverse_reverse] at hp
    simpa [Agent8.stepWord, hn, hp] using ht
  have hzlen : (zipAdd first.1 second.1.reverse).length = ss.length :=
    (zipAdd_length _ _ (hd.trans he.symm)).trans hd
  have hz : zipAdd first.1 second.1.reverse = ss.map Fin.val := by
    have hh := congrArg (List.take ss.length) hpair
    simpa [mirror, List.take_append, hzlen] using hh
  refine ⟨hlen, hb, first.1, second.1.reverse, hd, he, ?_, hz⟩
  change scan (mirror xs) 0 = _
  simpa [hc'] using hs

/-- Exact enumerator membership for the repository's actual pair-word map. -/
theorem mem_preimages_iff_actual (ss : List Symbol) (xs : List Nat) :
    xs ∈ preimages ss 0 ↔ ActualFiber ss xs :=
  (mem_preimages_iff_realizes ss 0 xs).trans ⟨realizes_actual ss xs, actual_realizes ss xs⟩

/-- Positive outer coefficient is the remaining canonical-input restriction
for an even mirrored pair word; no odd center is silently included. -/
def canonicalPreimages (ss : List Symbol) : List (List Nat) :=
  (preimages ss 0).filter (fun xs => decide (0 < xs.headD 0))

theorem canonical_membership (ss : List Symbol) (xs : List Nat) :
    xs ∈ canonicalPreimages ss ↔ ActualFiber ss xs ∧ 0 < xs.headD 0 := by
  simp [canonicalPreimages, mem_preimages_iff_actual]

theorem canonical_nodup (ss : List Symbol) : (canonicalPreimages ss).Nodup :=
  List.Pairwise.filter _ (preimages_nodup ss 0)

theorem canonical_bound (s t : Symbol) (ss : List Symbol) :
    (canonicalPreimages (s :: t :: ss)).length ≤ fib (ss.length+1) := by
  have hf := List.length_filter_le (fun xs => decide (0 < xs.headD 0))
    (preimages (s :: t :: ss) 0)
  exact Nat.le_trans hf (by rw [preimages_length]; exact inverseCount_bound s t ss)

theorem leading_eleven_positive (ss : List Symbol) (xs : List Nat)
    (h : xs ∈ preimages (11 :: ss) 0) : 0 < xs.headD 0 := by
  have hp := (mem_preimages _ _ _).mp h
  cases xs with
  | nil => exact False.elim hp
  | cons x xs =>
    obtain ⟨q, hx, hp⟩ := hp
    have hh := (leading_eleven_labels q ⟨x, hx.1⟩).mp hx
    have hx5 : x = 5 := hh.2
    simp [hx5]

theorem canonical_sharp (n : Nat) :
    (canonicalPreimages (11 :: List.replicate n 9)).length = fib n := by
  have heq : canonicalPreimages (11 :: List.replicate n 9) =
      preimages (11 :: List.replicate n 9) 0 := by
    apply List.filter_eq_self.mpr
    intro xs hx
    exact decide_eq_true (leading_eleven_positive _ _ hx)
  rw [heq, preimages_length, leading_eleven_exact]

#print axioms normalize_scan
#print axioms mem_preimages_iff_actual
#print axioms canonical_membership
#print axioms canonical_bound
#print axioms canonical_sharp

end P196.Agent9.InverseFibers
