import WordBridge

/-!
# Exact odd-center arithmetic and inverse-word enumeration

Agent #7, claim agent7-odd-nooverflow-fibers-20261016.
The existing Agent #9 local arithmetic relation is reused unchanged.
Odd words have a single even middle pair coefficient; its normalized
middle digit is prescribed by `v`, with both computed boundary carries.
No assertion about infinite reverse-add orbits is made here.
-/

namespace P196.Agent7.OddFibers

open P196.Agent9.InverseFibers

set_option maxRecDepth 100000
set_option maxHeartbeats 4000000

def oddMirror (xs : List Nat) (z : Nat) : List Nat :=
  xs ++ [z] ++ xs.reverse

@[simp] theorem oddMirror_nil (z : Nat) : oddMirror [] z = [z] := rfl

theorem oddMirror_cons (x : Nat) (xs : List Nat) (z : Nat) :
    oddMirror (x :: xs) z = x :: (oddMirror xs z ++ [x]) := by
  simp [oddMirror, List.reverse_cons, List.append_assoc]

@[simp] theorem oddMirror_length (xs : List Nat) (z : Nat) :
    (oddMirror xs z).length = 2 * xs.length + 1 := by
  simp [oddMirror]
  omega

theorem oddMirror_reverse (xs : List Nat) (z : Nat) :
    (oddMirror xs z).reverse = oddMirror xs z := by
  simp [oddMirror, List.reverse_append, List.append_assoc]

/-- The source middle pair is even, bounded, and normalizes to digit `v`.
`p` stores the incoming and outgoing carries of this single actual column. -/
def Center (v : Fin 10) (p : State) (z : Nat) : Prop :=
  z < 19 ∧ z % 2 = 0 ∧
    (z + low p) / 10 = high p ∧ (z + low p) % 10 = v.val

instance (v : Fin 10) (p : State) (z : Nat) : Decidable (Center v p z) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _))

def centerValue (v : Fin 10) (p : State) : Nat :=
  v.val + 10 * high p - low p

/-- Exact terminal arithmetic: parity selects the low carry and the
coefficient is then uniquely determined, including the source value zero. -/
theorem center_iff (v : Fin 10) (p : State) (z : Nat) :
    Center v p z ↔ low p = v.val % 2 ∧ z = centerValue v p := by
  have hl := low_bound p
  have hh := high_bound p
  have hv := v.isLt
  unfold Center centerValue
  omega

theorem center_exists_iff (v : Fin 10) (p : State) :
    (∃ z, Center v p z) ↔ low p = v.val % 2 := by
  simp only [center_iff]
  constructor
  · rintro ⟨z, hp, _⟩; exact hp
  · intro hp; exact ⟨centerValue v p, hp, rfl⟩

theorem center_unique (v : Fin 10) (p : State) (z w : Nat)
    (hz : Center v p z) (hw : Center v p w) : z = w := by
  rw [center_iff] at hz hw
  exact hz.2.trans hw.2.symm

theorem centerValue_center (v : Fin 10) (p : State)
    (hp : low p = v.val % 2) : Center v p (centerValue v p) :=
  (center_iff v p _).mpr ⟨hp, rfl⟩

/-- Exact local paths with the actual odd-center boundary equation. -/
def OddPath : List Symbol → Fin 10 → State → List Nat → Nat → Prop
  | [], v, p, [], z => Center v p z
  | s :: ss, v, p, x :: xs, z => ∃ q : State, Local s p q x ∧ OddPath ss v q xs z
  | _, _, _, _, _ => False

theorem oddPath_length (ss : List Symbol) (v : Fin 10) (p : State)
    (xs : List Nat) (z : Nat) (h : OddPath ss v p xs z) :
    xs.length = ss.length := by
  induction ss generalizing p xs with
  | nil =>
    cases xs with
    | nil => rfl
    | cons x xs => exact False.elim h
  | cons s ss ih =>
    cases xs with
    | nil => exact False.elim h
    | cons x xs =>
      obtain ⟨q, _, hp⟩ := h
      simpa using congrArg Nat.succ (ih q xs hp)

theorem oddPath_bounds (ss : List Symbol) (v : Fin 10) (p : State)
    (xs : List Nat) (z : Nat) (h : OddPath ss v p xs z) :
    (∀ x ∈ xs, x < 19) ∧ z < 19 ∧ z % 2 = 0 := by
  induction ss generalizing p xs with
  | nil =>
    cases xs with
    | nil => exact ⟨by simp, h.1, h.2.1⟩
    | cons x xs => exact False.elim h
  | cons s ss ih =>
    cases xs with
    | nil => exact False.elim h
    | cons x xs =>
      obtain ⟨q, hl, hp⟩ := h
      obtain ⟨hb, hz, he⟩ := ih q xs hp
      refine ⟨?_, hz, he⟩
      intro y hy
      rcases List.mem_cons.mp hy with rfl | hy
      · exact hl.1
      · exact hb y hy

/-- Prepend one arithmetic label, preserving the single middle coefficient. -/
def oddExtend (ls : List Nat) (words : List (List Nat × Nat)) : List (List Nat × Nat) :=
  ls.flatMap (fun x => words.map (fun w => (x :: w.1, w.2)))

theorem mem_oddExtend (ls : List Nat) (words : List (List Nat × Nat))
    (w : List Nat × Nat) :
    w ∈ oddExtend ls words ↔
      ∃ x ∈ ls, ∃ u ∈ words, (x :: u.1, u.2) = w := by
  simp [oddExtend]

theorem length_oddExtend (ls : List Nat) (words : List (List Nat × Nat)) :
    (oddExtend ls words).length = ls.length * words.length := by
  induction ls with
  | nil => simp [oddExtend]
  | cons x xs ih =>
    change ((words.map (fun w => (x :: w.1, w.2))) ++ oddExtend xs words).length =
      (xs.length + 1) * words.length
    rw [List.length_append, List.length_map, ih, Nat.add_mul]
    omega

/-- A finite enumerator of distinct half-word/middle-coefficient pairs. -/
def oddPreimages : List Symbol → Fin 10 → State → List (List Nat × Nat)
  | [], v, p => if low p = v.val % 2 then [([], centerValue v p)] else []
  | s :: ss, v, p => states.flatMap (fun q => oddExtend (labels s p q) (oddPreimages ss v q))

theorem mem_oddPreimages (ss : List Symbol) (v : Fin 10) (p : State)
    (xs : List Nat) (z : Nat) :
    (xs, z) ∈ oddPreimages ss v p ↔ OddPath ss v p xs z := by
  induction ss generalizing p xs with
  | nil =>
    cases xs with
    | nil => simp [oddPreimages, OddPath, center_iff]
    | cons x xs => simp [oddPreimages, OddPath]
  | cons s ss ih =>
    cases xs with
    | nil => simp [oddPreimages, mem_oddExtend, OddPath]
    | cons x xs =>
      simp only [oddPreimages, List.mem_flatMap, mem_oddExtend, mem_labels, OddPath]
      constructor
      · rintro ⟨q, _, y, hy, ⟨ys, w⟩, hys, he⟩
        obtain ⟨he1, he2⟩ := Prod.mk.inj he
        obtain ⟨rfl, rfl⟩ := List.cons.inj he1
        change w = z at he2
        subst w
        exact ⟨q, hy, (ih q ys).mp hys⟩
      · rintro ⟨q, hq, hp⟩
        exact ⟨q, mem_states q, x, hq, (xs, z), (ih q xs).mpr hp, rfl⟩

theorem oddExtend_nodup (ls : List Nat) (words : List (List Nat × Nat))
    (hl : ls.Nodup) (hw : words.Nodup) : (oddExtend ls words).Nodup := by
  apply List.pairwise_flatMap.mpr
  constructor
  · intro x hx
    apply List.Pairwise.map (fun w => (x :: w.1, w.2)) _ hw
    intro a b hab he
    apply hab
    have he' : (x :: a.1, a.2) = (x :: b.1, b.2) := he
    have hh := Prod.mk.inj he'
    exact Prod.ext (List.cons.inj hh.1).2 hh.2
  · apply List.Pairwise.imp (l := ls) (R := fun a b => a ≠ b) _ hl
    intro a b hab x hx y hy he
    obtain ⟨xs, _, rfl⟩ := List.mem_map.mp hx
    obtain ⟨ys, _, rfl⟩ := List.mem_map.mp hy
    exact hab (List.cons.inj (congrArg Prod.fst he)).1

/-- Enumeration has no duplicates even when different carry states are
tried: the existing actual local equation determines the next state. -/
theorem oddPreimages_nodup (ss : List Symbol) (v : Fin 10) (p : State) :
    (oddPreimages ss v p).Nodup := by
  induction ss generalizing p with
  | nil => simp [oddPreimages]; split <;> simp
  | cons s ss ih =>
    apply List.pairwise_flatMap.mpr
    constructor
    · intro q hq
      apply oddExtend_nodup _ _ _ (ih q)
      exact List.Pairwise.filter _ List.nodup_range
    · apply List.Pairwise.imp (l := states) (R := fun a b => a ≠ b) _ (by decide)
      intro q r hqr x hx y hy he
      obtain ⟨a, ha, xs, _, rfl⟩ := (mem_oddExtend _ _ _).mp hx
      obtain ⟨b, hb, ys, _, rfl⟩ := (mem_oddExtend _ _ _).mp hy
      have hab : a = b := (List.cons.inj (congrArg Prod.fst he)).1
      subst b
      exact hqr (local_next_unique s p q r a ((mem_labels _ _ _ _).mp ha)
        ((mem_labels _ _ _ _).mp hb))

#print axioms oddMirror_nil
#print axioms oddMirror_cons
#print axioms oddMirror_length
#print axioms oddMirror_reverse
#print axioms center_iff
#print axioms center_exists_iff
#print axioms center_unique
#print axioms centerValue_center
#print axioms oddPath_length
#print axioms oddPath_bounds
#print axioms mem_oddExtend
#print axioms length_oddExtend
#print axioms mem_oddPreimages
#print axioms oddExtend_nodup
#print axioms oddPreimages_nodup

end P196.Agent7.OddFibers
