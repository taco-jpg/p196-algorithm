import PathCounts

namespace P196.Agent9.InverseFibers

set_option maxRecDepth 100000
set_option maxHeartbeats 4000000

/-- Ordinary decimal normalization, retaining final carry separately. -/
def scan : List Nat → Nat → List Nat × Nat
  | [], e => ([], e)
  | x :: xs, e =>
    let (ds, f) := scan xs ((x + e) / 10)
    (((x + e) % 10) :: ds, f)

def mirror (xs : List Nat) : List Nat := xs ++ xs.reverse

def zipAdd : List Nat → List Nat → List Nat
  | x :: xs, y :: ys => (x+y) :: zipAdd xs ys
  | _, _ => []

/-- Exact ordinary normalization of the symmetric coefficient word.
The two halves of the result are read from opposite ends; their digit
sums are the target symbols. Both boundary carries remain explicit. -/
def Realizes (ss : List Symbol) (p : State) (xs : List Nat) : Prop :=
  xs.length = ss.length ∧ (∀ x ∈ xs, x < 19) ∧
  ∃ ds es : List Nat, ds.length = ss.length ∧ es.length = ss.length ∧
    scan (mirror xs) (low p) = (ds ++ es.reverse, high p) ∧
    zipAdd ds es = ss.map Fin.val

theorem scan_append (xs ys : List Nat) (e : Nat) :
    scan (xs ++ ys) e =
      let first := scan xs e
      let second := scan ys first.2
      (first.1 ++ second.1, second.2) := by
  induction xs generalizing e with
  | nil => simp [scan]
  | cons x xs ih => simp [scan, ih]

theorem scan_length (xs : List Nat) (e : Nat) :
    (scan xs e).1.length = xs.length := by
  induction xs generalizing e with
  | nil => rfl
  | cons x xs ih => simp [scan, ih]

theorem scan_carry_bound (xs : List Nat) (e : Nat)
    (he : e < 2) (hx : ∀ x ∈ xs, x < 19) : (scan xs e).2 < 2 := by
  induction xs generalizing e with
  | nil => exact he
  | cons x xs ih =>
    apply ih
    · have hh := hx x (by simp); omega
    · intro y hy; exact hx y (by simp [hy])

theorem low_bound (p : State) : low p < 2 := by unfold low; omega
theorem high_bound (p : State) : high p < 2 := Nat.mod_lt _ (by decide)

theorem path_realizes (ss : List Symbol) (p : State) (xs : List Nat)
    (h : Path ss p xs) : Realizes ss p xs := by
  induction ss generalizing p xs with
  | nil =>
    cases xs with
    | nil =>
      refine ⟨rfl, by simp, [], [], rfl, rfl, ?_, rfl⟩
      simpa [scan, mirror] using congrArg (Prod.mk ([] : List Nat)) h
    | cons x xs => exact False.elim h
  | cons s ss ih =>
    cases xs with
    | nil => exact False.elim h
    | cons x xs =>
      obtain ⟨q, hl, hp⟩ := h
      obtain ⟨hlen, hbound, ds, es, hd, he, hscan, hzip⟩ := ih q xs hp
      refine ⟨by simp [hlen], ?_, (x+low p)%10 :: ds,
          (x+high q)%10 :: es, by simp [hd], by simp [he], ?_, ?_⟩
      · intro y hy
        rcases List.mem_cons.mp hy with rfl | hy
        · exact hl.1
        · exact hbound y hy
      · have hm : mirror (x :: xs) = x :: (mirror xs ++ [x]) := by
          simp [mirror, List.reverse_cons, List.append_assoc]
        rw [hm]
        simp only [scan, hl.2.1, scan_append, hscan]
        simp [scan, hl.2.2.1, List.reverse_cons, List.append_assoc]
      · simp only [zipAdd, hzip, hl.2.2.2, List.map_cons]

/-- Encode the two Boolean carries without losing either component. -/
def mkState (a b : Nat) (ha : a < 2) (hb : b < 2) : State :=
  ⟨2*a+b, by omega⟩

theorem low_mkState (a b : Nat) (ha : a < 2) (hb : b < 2) :
    low (mkState a b ha hb) = a := by simp only [low, mkState]; omega

theorem high_mkState (a b : Nat) (ha : a < 2) (hb : b < 2) :
    high (mkState a b ha hb) = b := by simp only [high, mkState]; omega

/-- No arithmetic preimage is omitted by the folded path predicate. -/
theorem realizes_path (ss : List Symbol) (p : State) (xs : List Nat)
    (h : Realizes ss p xs) : Path ss p xs := by
  induction ss generalizing p xs with
  | nil =>
    obtain ⟨hlen, hb, ds, es, hd, he, hs, hz⟩ := h
    have hx : xs = [] := List.length_eq_zero_iff.mp hlen
    have hd' : ds = [] := List.length_eq_zero_iff.mp hd
    have he' : es = [] := List.length_eq_zero_iff.mp he
    subst xs; subst ds; subst es
    simpa [Path, scan, mirror] using congrArg Prod.snd hs
  | cons s ss ih =>
    obtain ⟨hlen, hb, ds, es, hd, he, hs, hz⟩ := h
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
          have ha : (x + low p)/10 < 2 := by have := low_bound p; omega
          have hmBound : ∀ y ∈ mirror xs, y < 19 := by
            intro y hy
            apply hxs y
            simpa [mirror] using hy
          let a := (x + low p) / 10
          let inner := scan (mirror xs) a
          have hc : inner.2 < 2 := scan_carry_bound (mirror xs) a ha hmBound
          let q := mkState a inner.2 ha hc
          have qlow : low q = a := low_mkState _ _ _ _
          have qhigh : high q = inner.2 := high_mkState _ _ _ _
          have hm : mirror (x :: xs) = x :: (mirror xs ++ [x]) := by
            simp [mirror, List.reverse_cons, List.append_assoc]
          rw [hm] at hs
          simp only [scan, scan_append, List.reverse_cons, List.cons_append,
            Prod.mk.injEq, List.cons.injEq] at hs
          have hdigit : (x + low p)%10 = d := hs.1.1
          have hlast : (x + inner.2)%10 = e := by
            have ht := congrArg List.getLast? hs.1.2
            simpa [inner, a] using ht
          have hinner : inner.1 = ds ++ es.reverse := by
            apply List.append_cancel_right (bs := [e])
            simpa [inner, a, hlast, List.append_assoc] using hs.1.2
          have hcarry : (x + inner.2)/10 = high p := hs.2
          have hem : d + e = s.val ∧ zipAdd ds es = ss.map Fin.val := by
            simpa [zipAdd] using hz
          refine ⟨q, ?_, ih q xs ?_⟩
          · refine ⟨hx, qlow.symm, ?_, ?_⟩
            · simpa [qhigh] using hcarry
            · rw [qhigh, hdigit, hlast]; exact hem.1
          · refine ⟨by simpa using hlen, hxs, ds, es,
              by simpa using hd, by simpa using he, ?_, hem.2⟩
            rw [qlow, qhigh]
            exact Prod.ext hinner rfl

/-- Complete equivalence with full decimal normalization, not just local tests. -/
theorem mem_preimages_iff_realizes (ss : List Symbol) (p : State) (xs : List Nat) :
    xs ∈ preimages ss p ↔ Realizes ss p xs :=
  (mem_preimages ss p xs).trans ⟨path_realizes ss p xs, realizes_path ss p xs⟩

#print axioms path_realizes
#print axioms realizes_path
#print axioms mem_preimages_iff_realizes

end P196.Agent9.InverseFibers
