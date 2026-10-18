import P196.Drafts.Agent3TwoHistory.InverseFibers

namespace P196.Agent9.InverseFibers

set_option maxRecDepth 100000
set_option maxHeartbeats 4000000

def states : List State := [0,1,2,3]
theorem mem_states (p : State) : p ∈ states := by
  have : ∀ p : State, p ∈ states := by decide
  exact this p

def labels (s : Symbol) (p q : State) : List Nat :=
  (List.range 19).filter (fun x => decide (Local s p q x))

theorem mem_labels (s : Symbol) (p q : State) (x : Nat) :
    x ∈ labels s p q ↔ Local s p q x := by
  simp only [labels, List.mem_filter, List.mem_range, decide_eq_true_eq]
  constructor
  · exact And.right
  · intro h; exact ⟨h.1, h⟩

def extend (ls : List Nat) (words : List (List Nat)) : List (List Nat) :=
  ls.flatMap (fun x => words.map (fun xs => x :: xs))

theorem mem_extend (ls : List Nat) (words : List (List Nat)) (xs : List Nat) :
    xs ∈ extend ls words ↔ ∃ x ∈ ls, ∃ ys ∈ words, x :: ys = xs := by
  simp [extend]

theorem length_extend (ls : List Nat) (words : List (List Nat)) :
    (extend ls words).length = ls.length * words.length := by
  induction ls with
  | nil => simp [extend]
  | cons x xs ih =>
    change (words.map (List.cons x) ++ extend xs words).length = (xs.length+1) * words.length
    rw [List.length_append, List.length_map, ih, Nat.add_mul]
    omega

/-- Exact inverse label words for a prescribed target and boundary carries. -/
def preimages : List Symbol → State → List (List Nat)
  | [], p => if low p = high p then [[]] else []
  | s :: ss, p => states.flatMap (fun q => extend (labels s p q) (preimages ss q))

/-- The actual arithmetic path predicate, including even-center carry matching. -/
def Path : List Symbol → State → List Nat → Prop
  | [], p, [] => low p = high p
  | s :: ss, p, x :: xs => ∃ q : State, Local s p q x ∧ Path ss q xs
  | _, _, _ => False

theorem mem_preimages (ss : List Symbol) (p : State) (xs : List Nat) :
    xs ∈ preimages ss p ↔ Path ss p xs := by
  induction ss generalizing p xs with
  | nil =>
    cases xs with
    | nil => simp [preimages, Path]
    | cons x xs => simp [preimages, Path]
  | cons s ss ih =>
    cases xs with
    | nil => simp [preimages, mem_extend, Path]
    | cons x xs =>
      simp only [preimages, List.mem_flatMap, mem_extend, mem_labels,
        List.cons.injEq, Path]
      constructor
      · rintro ⟨q, _, y, hy, ys, hys, he⟩
        obtain ⟨rfl, rfl⟩ := he
        exact ⟨q, hy, (ih q ys).mp hys⟩
      · rintro ⟨q, hq, hp⟩
        exact ⟨q, mem_states q, x, hq, xs, (ih q xs).mpr hp, rfl, rfl⟩

def suffixCounts (ss : List Symbol) : Counts :=
  ⟨(preimages ss 0).length, (preimages ss 1).length,
   (preimages ss 2).length, (preimages ss 3).length⟩

def dot (v w : Counts) : Nat := v.a*w.a + v.b*w.b + v.c*w.c + v.d*w.d

/-- Forward path propagation is dual to the exact backward enumeration. -/
theorem dot_suffix (s : Symbol) (ss : List Symbol) (v : Counts) :
    dot v (suffixCounts (s :: ss)) = dot (advance s v) (suffixCounts ss) := by
  simp only [dot, suffixCounts, preimages, states, List.flatMap_cons, List.flatMap_nil,
    List.append_nil, List.length_append, length_extend, advance]
  change _ = _
  simp only [weight, labels, Nat.mul_add, Nat.add_mul, Nat.mul_assoc]
  ac_rfl

theorem dot_run (ss : List Symbol) (v : Counts) :
    dot v (suffixCounts ss) = (run ss v).U := by
  induction ss generalizing v with
  | nil =>
    simp [dot, suffixCounts, preimages, low, high, run, Counts.U,
      show (3 : State).val = 3 from rfl]
  | cons s ss ih => rw [dot_suffix, ih]; rfl

/-- No postulated cardinality: the DP equals the explicit enumerator length. -/
theorem preimages_length (ss : List Symbol) :
    (preimages ss 0).length = inverseCount ss := by
  have h := dot_run ss initial
  simpa [dot, suffixCounts, initial, inverseCount] using h

/-- Distinct guessed interior carry states cannot have the same input label. -/
theorem local_next_unique (s : Symbol) (p q r : State) (x : Nat)
    (hq : Local s p q x) (hr : Local s p r x) : q = r := by
  apply Fin.ext
  have h1 := Nat.mod_add_div (x + high q) 10
  have h2 := Nat.mod_add_div (x + high r) 10
  have h3 := Nat.mod_add_div q.val 2
  have h4 := Nat.mod_add_div r.val 2
  simp only [Local, low, high] at hq hr h1 h2
  omega

theorem extend_nodup (ls : List Nat) (words : List (List Nat))
    (hl : ls.Nodup) (hw : words.Nodup) : (extend ls words).Nodup := by
  apply List.pairwise_flatMap.mpr
  constructor
  · intro x hx
    exact List.Pairwise.map (List.cons x) (fun a b hab he => hab (List.cons.inj he).2) hw
  · apply List.Pairwise.imp (l := ls) (R := fun a b => a ≠ b) _ hl
    intro a b hab x hx y hy he
    obtain ⟨xs, _, rfl⟩ := List.mem_map.mp hx
    obtain ⟨ys, _, rfl⟩ := List.mem_map.mp hy
    exact hab (List.cons.inj he).1

/-- Thus the counted objects are distinct input half-words, not duplicate paths. -/
theorem preimages_nodup (ss : List Symbol) (p : State) : (preimages ss p).Nodup := by
  induction ss generalizing p with
  | nil => simp [preimages]; split <;> simp
  | cons s ss ih =>
    apply List.pairwise_flatMap.mpr
    constructor
    · intro q hq
      apply extend_nodup _ _ _ (ih q)
      exact List.Pairwise.filter _ List.nodup_range
    · apply List.Pairwise.imp (l := states) (R := fun a b => a ≠ b) _ (by decide)
      intro q r hqr x hx y hy he
      obtain ⟨a, ha, xs, _, rfl⟩ := (mem_extend _ _ _).mp hx
      obtain ⟨b, hb, ys, _, rfl⟩ := (mem_extend _ _ _).mp hy
      obtain ⟨rfl, _⟩ := List.cons.inj he
      exact hqr (local_next_unique s p q r a ((mem_labels _ _ _ _).mp ha)
        ((mem_labels _ _ _ _).mp hb))

theorem exact_fiber_bound (s t : Symbol) (ss : List Symbol) :
    (preimages (s :: t :: ss) 0).Nodup ∧
    (preimages (s :: t :: ss) 0).length ≤ fib (ss.length + 1) :=
  ⟨preimages_nodup _ _, by rw [preimages_length]; exact inverseCount_bound s t ss⟩

theorem exact_sharp_family (n : Nat) :
    (preimages (11 :: List.replicate n 9) 0).Nodup ∧
    (preimages (11 :: List.replicate n 9) 0).length = fib n :=
  ⟨preimages_nodup _ _, by rw [preimages_length]; exact leading_eleven_exact n⟩

#print axioms mem_preimages
#print axioms preimages_length
#print axioms preimages_nodup
#print axioms exact_fiber_bound
#print axioms exact_sharp_family

end P196.Agent9.InverseFibers
