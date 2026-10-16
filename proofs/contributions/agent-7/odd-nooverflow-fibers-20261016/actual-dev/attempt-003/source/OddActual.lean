import OddCenter
import ActualWords

/-
Agent #7: odd-center counterpart of the pinned Agent #9 scan/actual-word bridge.
The original scan, carry state, local column relation, normalizer, and stepWord
are imported unchanged. All source-center bounds and parity remain explicit.
Verification status is supplied by the accompanying actual-dev execution logs.
-/
namespace P196.Agent7.OddFibers

open P196.Agent9.InverseFibers

set_option maxRecDepth 100000
set_option maxHeartbeats 4000000

/-- Exact scan realization of an odd folded path, with both boundary carries.
The source center is a bounded even coefficient; the output center is a digit. -/
def OddRealizes (ss : List Symbol) (v : Fin 10) (p : State)
    (xs : List Nat) (z : Nat) : Prop :=
  xs.length = ss.length ∧ (∀ x ∈ xs, x < 19) ∧ z < 19 ∧ z % 2 = 0 ∧
  ∃ ds es : List Nat, ds.length = ss.length ∧ es.length = ss.length ∧
    scan (oddMirror xs z) (low p) = (ds ++ [v.val] ++ es.reverse, high p) ∧
    zipAdd ds es = ss.map Fin.val

theorem oddPath_realizes (ss : List Symbol) (v : Fin 10) (p : State)
    (xs : List Nat) (z : Nat) (h : OddPath ss v p xs z) :
    OddRealizes ss v p xs z := by
  induction ss generalizing p xs with
  | nil =>
    cases xs with
    | nil =>
      have hc : Center v p z := h
      refine ⟨rfl, by simp, hc.1, hc.2.1, [], [], rfl, rfl, ?_, rfl⟩
      simp [oddMirror, scan, hc.2.2.1, hc.2.2.2]
    | cons x xs => exact False.elim h
  | cons s ss ih =>
    cases xs with
    | nil => exact False.elim h
    | cons x xs =>
      obtain ⟨q, hl, hp⟩ := h
      obtain ⟨hlen, hb, hzb, hze, ds, es, hd, he, hs, hz⟩ := ih q xs hp
      refine ⟨by simp [hlen], ?_, hzb, hze,
        (x + low p) % 10 :: ds, (x + high q) % 10 :: es,
        by simp [hd], by simp [he], ?_, ?_⟩
      · intro y hy
        rcases List.mem_cons.mp hy with rfl | hy
        · exact hl.1
        · exact hb y hy
      · have hm : oddMirror (x :: xs) z = x :: (oddMirror xs z ++ [x]) := by
          simp [oddMirror, List.reverse_cons, List.append_assoc]
        rw [hm]
        simp only [scan, hl.2.1, scan_append, hs]
        simp [scan, hl.2.2.1, List.reverse_cons, List.append_assoc]
      · simp only [zipAdd, hz, hl.2.2.2, List.map_cons]

theorem oddRealizes_path (ss : List Symbol) (v : Fin 10) (p : State)
    (xs : List Nat) (z : Nat) (h : OddRealizes ss v p xs z) :
    OddPath ss v p xs z := by
  induction ss generalizing p xs with
  | nil =>
    obtain ⟨hlen, hb, hzb, hze, ds, es, hd, he, hs, hz⟩ := h
    have hx : xs = [] := List.length_eq_zero_iff.mp hlen
    have hd' : ds = [] := List.length_eq_zero_iff.mp hd
    have he' : es = [] := List.length_eq_zero_iff.mp he
    subst xs; subst ds; subst es
    have hc : (z + low p) / 10 = high p := by
      simpa [oddMirror, scan] using congrArg Prod.snd hs
    have hv : (z + low p) % 10 = v.val := by
      simpa [oddMirror, scan] using congrArg Prod.fst hs
    exact ⟨hzb, hze, hc, hv⟩
  | cons s ss ih =>
    obtain ⟨hlen, hb, hzb, hze, ds, es, hd, he, hs, hz⟩ := h
    cases xs with
    | nil => simp at hlen
    | cons x xs =>
      cases ds with
      | nil => simp at hd
      | cons d ds =>
        cases es with
        | nil => simp at he
        | cons e es =>
          have hx : x < 19 := hb x (by simp)
          have hxs : ∀ y ∈ xs, y < 19 := by
            intro y hy; exact hb y (by simp [hy])
          have ha : (x + low p) / 10 < 2 := by have := low_bound p; omega
          have hmBound : ∀ y ∈ oddMirror xs z, y < 19 := by
            intro y hy
            simp only [oddMirror, List.mem_append, List.mem_singleton,
              List.mem_reverse] at hy
            rcases hy with (hy | rfl) | hy
            · exact hxs y hy
            · exact hzb
            · exact hxs y hy
          let a := (x + low p) / 10
          let inner := scan (oddMirror xs z) a
          have hc : inner.2 < 2 := scan_carry_bound (oddMirror xs z) a ha hmBound
          let q := mkState a inner.2 ha hc
          have qlow : low q = a := low_mkState _ _ _ _
          have qhigh : high q = inner.2 := high_mkState _ _ _ _
          have hm : oddMirror (x :: xs) z = x :: (oddMirror xs z ++ [x]) := by
            simp [oddMirror, List.reverse_cons, List.append_assoc]
          rw [hm] at hs
          simp only [scan, scan_append, List.reverse_cons, List.cons_append,
            Prod.mk.injEq, List.cons.injEq] at hs
          have hdigit : (x + low p) % 10 = d := hs.1.1
          have hlast : (x + inner.2) % 10 = e := by
            have htail : inner.1 ++ [(x + inner.2) % 10] =
                (ds ++ [v.val] ++ es.reverse) ++ [e] := by
              simpa [inner, a, List.append_assoc] using hs.1.2
            simpa only [List.getLast?_concat, Option.some.injEq] using
              congrArg List.getLast? htail
          have hinner : inner.1 = ds ++ [v.val] ++ es.reverse := by
            apply List.append_cancel_right (bs := [e])
            simpa [inner, a, hlast, List.append_assoc] using hs.1.2
          have hcarry : (x + inner.2) / 10 = high p := hs.2
          have hem : d + e = s.val ∧ zipAdd ds es = ss.map Fin.val := by
            simpa [zipAdd] using hz
          refine ⟨q, ?_, ih q xs ?_⟩
          · refine ⟨hx, qlow.symm, ?_, ?_⟩
            · simpa [qhigh] using hcarry
            · rw [qhigh, hdigit, hlast]; exact hem.1
          · refine ⟨by simpa using hlen, hxs, hzb, hze, ds, es,
              by simpa using hd, by simpa using he, ?_, hem.2⟩
            rw [qlow, qhigh]
            exact Prod.ext hinner rfl

/-- The folded odd path omits no bounded even-center arithmetic realization. -/
theorem oddPath_iff_realizes (ss : List Symbol) (v : Fin 10) (p : State)
    (xs : List Nat) (z : Nat) :
    OddPath ss v p xs z ↔ OddRealizes ss v p xs z :=
  ⟨oddPath_realizes ss v p xs z, oddRealizes_path ss v p xs z⟩

/-- Pairing an odd digit word doubles its center and sums opposite outer digits. -/
theorem pair_odd_halves (ds es : List Nat) (v : Nat)
    (h : ds.length = es.length) :
    Agent8.pair (ds ++ [v] ++ es.reverse) = oddMirror (zipAdd ds es) (2 * v) := by
  simp only [Agent8.pair, zipAdd_repository, List.reverse_append,
    List.reverse_reverse, List.reverse_cons, List.reverse_nil,
    List.nil_append, List.append_assoc]
  rw [zipAdd_append _ _ _ _ h]
  simp only [List.singleton_append, zipAdd]
  rw [zipAdd_reverse _ _ h.symm, zipAdd_comm es ds]
  simp [oddMirror, Nat.two_mul]

/-- Both the outside half and center are determined by the complete odd word. -/
theorem oddMirror_injective (xs ys : List Nat) (z w : Nat)
    (h : oddMirror xs z = oddMirror ys w) : xs = ys ∧ z = w := by
  have hlen : xs.length = ys.length := by
    have hh := congrArg List.length h
    simp only [oddMirror, List.length_append, List.length_singleton,
      List.length_reverse] at hh
    omega
  have hxs : xs = ys := by
    have hh := congrArg (List.take xs.length) h
    simpa [oddMirror, List.take_append, hlen] using hh
  subst ys
  have htail : [z] ++ xs.reverse = [w] ++ xs.reverse := by
    apply List.append_cancel_left (as := xs)
    simpa [oddMirror] using h
  have hc : [z] = [w] := List.append_cancel_right htail
  exact ⟨rfl, by simpa using hc⟩

/-- The existing no-overflow pair-word transition, with odd source and target.
This concerns coefficient words; it does not assert an all-time integer lift. -/
def OddActualFiber (ss : List Symbol) (v : Fin 10) (xs : List Nat) (z : Nat) : Prop :=
  xs.length = ss.length ∧ (∀ x ∈ xs, x < 19) ∧ z < 19 ∧ z % 2 = 0 ∧
  (scan (oddMirror xs z) 0).2 = 0 ∧
  Agent8.stepWord (oddMirror xs z) = oddMirror (ss.map Fin.val) (2 * v.val)

theorem oddRealizes_actual (ss : List Symbol) (v : Fin 10)
    (xs : List Nat) (z : Nat) (h : OddRealizes ss v 0 xs z) :
    OddActualFiber ss v xs z := by
  obtain ⟨hlen, hb, hzb, hze, ds, es, hd, he, hs, hz⟩ := h
  change scan (oddMirror xs z) 0 = (ds ++ [v.val] ++ es.reverse, 0) at hs
  refine ⟨hlen, hb, hzb, hze, by rw [hs], ?_⟩
  unfold Agent8.stepWord
  rw [normalize_scan, hs]
  simp only [Nat.zero_eq, ↓reduceIte, List.append_nil]
  rw [pair_odd_halves _ _ _ (hd.trans he.symm), hz]

theorem oddActual_realizes (ss : List Symbol) (v : Fin 10)
    (xs : List Nat) (z : Nat) (h : OddActualFiber ss v xs z) :
    OddRealizes ss v 0 xs z := by
  obtain ⟨hlen, hb, hzb, hze, hc, ht⟩ := h
  let first := scan xs 0
  let c := (z + first.2) % 10
  let second := scan xs.reverse ((z + first.2) / 10)
  have hs : scan (oddMirror xs z) 0 =
      (first.1 ++ [c] ++ second.1, second.2) := by
    simp [oddMirror, scan_append, scan, first, c, second]
  have hc' : second.2 = 0 := by simpa [hs] using hc
  have hd : first.1.length = ss.length := (scan_length xs 0).trans hlen
  have he : second.1.reverse.length = ss.length := by
    simpa [second, hlen] using scan_length xs.reverse ((z + first.2) / 10)
  have hn : Agent8.normalize (oddMirror xs z) 0 = first.1 ++ [c] ++ second.1 := by
    rw [normalize_scan, hs, hc']; simp
  have hpair : oddMirror (zipAdd first.1 second.1.reverse) (2 * c) =
      oddMirror (ss.map Fin.val) (2 * v.val) := by
    have hp := pair_odd_halves first.1 second.1.reverse c (hd.trans he.symm)
    simp only [List.reverse_reverse] at hp
    have ht' : Agent8.pair (first.1 ++ [c] ++ second.1) =
        oddMirror (ss.map Fin.val) (2 * v.val) := by
      simpa only [Agent8.stepWord, hn] using ht
    exact hp.symm.trans ht'
  obtain ⟨hz, hv⟩ := oddMirror_injective _ _ _ _ hpair
  have hcval : c = v.val := by omega
  refine ⟨hlen, hb, hzb, hze, first.1, second.1.reverse, hd, he, ?_, hz⟩
  change scan (oddMirror xs z) 0 = _
  simpa [hc', hcval] using hs

/-- Exact equivalence with the repository's actual odd no-overflow transition. -/
theorem oddPath_iff_actual (ss : List Symbol) (v : Fin 10)
    (xs : List Nat) (z : Nat) :
    OddPath ss v 0 xs z ↔ OddActualFiber ss v xs z :=
  (oddPath_iff_realizes ss v 0 xs z).trans
    ⟨oddRealizes_actual ss v xs z, oddActual_realizes ss v xs z⟩

/-- The actual normalizer exposes the prescribed digit center before pairing. -/
theorem oddPath_normalize (ss : List Symbol) (v : Fin 10)
    (xs : List Nat) (z : Nat) (h : OddPath ss v 0 xs z) :
    ∃ ds es : List Nat, ds.length = ss.length ∧ es.length = ss.length ∧
      Agent8.normalize (oddMirror xs z) 0 = ds ++ [v.val] ++ es.reverse ∧
      zipAdd ds es = ss.map Fin.val := by
  obtain ⟨hlen, hb, hzb, hze, ds, es, hd, he, hs, hz⟩ :=
    oddPath_realizes ss v 0 xs z h
  refine ⟨ds, es, hd, he, ?_, hz⟩
  change scan (oddMirror xs z) 0 = (ds ++ [v.val] ++ es.reverse, 0) at hs
  rw [normalize_scan, hs]
  simp

#print axioms oddPath_realizes
#print axioms oddRealizes_path
#print axioms oddPath_iff_realizes
#print axioms pair_odd_halves
#print axioms oddMirror_injective
#print axioms oddRealizes_actual
#print axioms oddActual_realizes
#print axioms oddPath_iff_actual
#print axioms oddPath_normalize

end P196.Agent7.OddFibers
