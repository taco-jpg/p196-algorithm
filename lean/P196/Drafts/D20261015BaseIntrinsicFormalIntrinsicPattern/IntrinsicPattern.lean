import P196.Drafts.D20261015BaseIntrinsicFormalIntrinsicCarry.IntrinsicCarry

namespace IntrinsicPattern
open BaseReflection ResetNormalization PhysicalWidth SeamSafety IntrinsicCarry

def WordBounded (b : Int) (qs : List Int) : Prop :=
  ∀ q ∈ qs, 0 ≤ q ∧ q ≤ 2*b-2

def StartsNeutral (b : Int) : List Int → Prop
  | [] => False
  | q::_ => q=b-1

def HighNeutral (b : Int) : List Int → Prop
  | [] => False
  | q::rest => (b ≤ q ∧ StartsNeutral b rest) ∨ HighNeutral b rest

def HasDefect (b i : Int) : List Int → Prop
  | [] => False
  | q::rest => (q+i)/b ≠ q/b ∨ HasDefect b ((q+i)/b) rest

theorem defect_iff_initial_or_highNeutral (b i : Int) (qs : List Int)
    (hb : 2 ≤ b) (hi : 0 ≤ i ∧ i ≤ 1) (hq : WordBounded b qs) :
    HasDefect b i qs ↔ (i=1 ∧ StartsNeutral b qs) ∨ HighNeutral b qs := by
  induction qs generalizing i with
  | nil => simp [HasDefect,StartsNeutral,HighNeutral]
  | cons q qs ih =>
    have hq0 := hq q (by simp)
    have ht : WordBounded b qs := by
      intro q hmem; exact hq q (by simp [hmem])
    have hc := carry_bit b q i hb hq0 hi
    have hci : 0 ≤ (q+i)/b ∧ (q+i)/b ≤ 1 := by omega
    rw [HasDefect,local_defect_iff b q i hb hq0 hi,ih _ hci ht,
      carry_one_iff b q i hb hq0 hi]
    simp only [StartsNeutral,HighNeutral]
    constructor
    · intro h
      rcases h with h | ⟨h,hs⟩ | h
      · exact Or.inl ⟨h.2,h.1⟩
      · rcases h with hh | hn
        · exact Or.inr (Or.inl ⟨hh,hs⟩)
        · exact Or.inl ⟨hn.2,hn.1⟩
      · exact Or.inr (Or.inr h)
    · intro h
      rcases h with h | ⟨hh,hs⟩ | h
      · exact Or.inl ⟨h.2,h.1⟩
      · exact Or.inr (Or.inl ⟨Or.inl hh,hs⟩)
      · exact Or.inr (Or.inr h)

theorem defect_iff_highNeutral (b : Int) (qs : List Int)
    (hb : 2 ≤ b) (hq : WordBounded b qs) :
    HasDefect b 0 qs ↔ HighNeutral b qs := by
  simpa using defect_iff_initial_or_highNeutral b 0 qs hb (by omega) hq

def tags (qs : List Int) (flag : Bool) : List (Int × Bool) := qs.map (fun q => (q,flag))

theorem singleton_initial_irrelevant (b i j : Int) (xs : List (Int × Bool)) (k : Nat) :
    out b i (singletonTags xs) k = out b j (singletonTags xs) k := by
  cases xs with
  | nil => rfl
  | cons p xs =>
    rcases p with ⟨q,r⟩
    cases k <;> rfl

theorem tags_initial_irrelevant (b i j : Int) (qs : List Int) (k : Nat) :
    out b i (tags qs true) k = out b j (tags qs true) k := by
  cases qs with
  | nil => rfl
  | cons q qs => cases k <;> rfl

theorem defect_iff_out_witness (b i : Int) (qs : List Int) :
    HasDefect b i qs ↔ ∃ k,
      out b i (tags qs false) k ≠ out b 0 (tags qs true) k := by
  induction qs generalizing i with
  | nil => simp [HasDefect,tags,out]
  | cons q qs ih =>
    constructor
    · intro h
      rcases h with hh | ht
      · refine ⟨0,?_⟩
        simpa only [tags,List.map_cons,out,Bool.false_eq_true,↓reduceIte,Int.add_zero] using hh
      · obtain ⟨k,hk⟩ := (ih _).mp ht
        refine ⟨k+1,?_⟩
        change out b ((q+i)/b) (tags qs false) k ≠ out b ((q+0)/b) (tags qs true) k
        rw [tags_initial_irrelevant b ((q+0)/b) 0 qs k]
        exact hk
    · rintro ⟨k,hk⟩
      cases k with
      | zero =>
        left
        simpa only [tags,List.map_cons,out,Bool.false_eq_true,↓reduceIte,Int.add_zero] using hk
      | succ k =>
        right
        apply (ih _).mpr
        refine ⟨k,?_⟩
        change out b ((q+i)/b) (tags qs false) k ≠ out b ((q+0)/b) (tags qs true) k at hk
        rwa [tags_initial_irrelevant b ((q+0)/b) 0 qs k] at hk

theorem ordinaryTags_eq_tags (xs : List (Int × Bool)) :
    ordinaryTags xs = tags (xs.map Prod.fst) false := by
  simp [ordinaryTags,tags,List.map_map,Function.comp_def]

theorem singletonTags_eq_tags (xs : List (Int × Bool)) :
    singletonTags xs = tags (xs.map Prod.fst) true := by
  simp [singletonTags,tags,List.map_map,Function.comp_def]

theorem wordBounded_projection (b : Int) (xs : List (Int × Bool))
    (h : Bounded b xs) : WordBounded b (xs.map Prod.fst) := by
  intro q hq
  obtain ⟨p,hp,rfl⟩ := List.mem_map.mp hq
  exact h p hp

theorem highNeutral_iff_singleton_defect (b : Int) (xs : List (Int × Bool))
    (hb : 2 ≤ b) (hbound : Bounded b xs) :
    HighNeutral b (xs.map Prod.fst) ↔ ∃ k,
      outgoing b (ordinaryTags xs) k ≠ outgoing b (singletonTags xs) k := by
  rw [← defect_iff_highNeutral b _ hb (wordBounded_projection b xs hbound),
    defect_iff_out_witness]
  simp only [ordinaryTags_eq_tags,singletonTags_eq_tags,out_zero_eq_outgoing]

theorem any_defect_implies_highNeutral (b : Int) (xs : List (Int × Bool)) (k : Nat)
    (hb : 2 ≤ b) (hbound : Bounded b xs)
    (hdef : outgoing b xs k ≠ outgoing b (ordinaryTags xs) k) :
    HighNeutral b (xs.map Prod.fst) := by
  apply (highNeutral_iff_singleton_defect b xs hb hbound).mpr
  refine ⟨k,?_⟩
  have hmax := singleton_defect_maximal b xs k hb hbound
  omega

theorem singleton_projection (xs : List (Int × Bool)) :
    (singletonTags xs).map Prod.fst = xs.map Prod.fst := by
  simp [singletonTags,List.map_map,Function.comp_def]

theorem ordinary_singleton (xs : List (Int × Bool)) :
    ordinaryTags (singletonTags xs) = ordinaryTags xs := by
  simp [ordinaryTags,singletonTags,List.map_map,Function.comp_def]

/-- Partition search is eliminated: some reset pattern has a nonzero
carry defect exactly when an adjacent high/neutral pair occurs. -/
theorem exists_partition_defect_iff (b : Int) (qs : List Int)
    (hb : 2 ≤ b) (hbound : WordBounded b qs) :
    (∃ xs k, xs.map Prod.fst = qs ∧
      outgoing b xs k ≠ outgoing b (ordinaryTags xs) k) ↔ HighNeutral b qs := by
  constructor
  · rintro ⟨xs,k,hqs,hd⟩
    have hbxs : Bounded b xs := by
      intro p hp
      apply hbound p.1
      rw [← hqs]
      exact List.mem_map.mpr ⟨p,hp,rfl⟩
    simpa only [hqs] using any_defect_implies_highNeutral b xs k hb hbxs hd
  · intro hh
    let xs := tags qs false
    have hxs : xs.map Prod.fst = qs := by simp [xs,tags,List.map_map,Function.comp_def]
    have hbxs : Bounded b xs := by
      intro p hp
      apply hbound p.1
      rw [← hxs]
      exact List.mem_map.mpr ⟨p,hp,rfl⟩
    obtain ⟨k,hk⟩ := (highNeutral_iff_singleton_defect b xs hb hbxs).mp (by rwa [hxs])
    exact ⟨singletonTags xs,k,by rw [singleton_projection,hxs],by
      rw [ordinary_singleton]
      exact Ne.symm hk⟩

/-- All-base local-pattern output safety. The symmetry premise is needed
here, not in the preceding partition-free combinatorial characterization. -/
theorem highNeutral_output_safe (b : Int) (xs : List (Int × Bool))
    (hb : 3 ≤ b) (hbound : Bounded b xs)
    (hsym : (xs.map Prod.fst).reverse = xs.map Prod.fst)
    (hh : HighNeutral b (xs.map Prod.fst)) :
    (actualDigits b xs).reverse ≠ actualDigits b xs := by
  obtain ⟨k,hk⟩ := (highNeutral_iff_singleton_defect b xs (by omega) hbound).mp hh
  have hbSingle : Bounded b (singletonTags xs) := by
    intro p hp
    obtain ⟨a,ha,rfl⟩ := List.mem_map.mp hp
    exact hbound a ha
  have hsSingle : ((singletonTags xs).map Prod.fst).reverse = (singletonTags xs).map Prod.fst := by
    simpa only [singleton_projection] using hsym
  have hd : outgoing b (singletonTags xs) k ≠ outgoing b (ordinaryTags (singletonTags xs)) k := by
    rw [ordinary_singleton]
    exact Ne.symm hk
  have hsafe := outgoing_defect_nonpalindromic b (singletonTags xs) k hb hbSingle hsSingle hd
  simpa only [actualDigits,ordinary_singleton] using hsafe

/-- Explicit low-to-high adjacent-pair meaning of the recursive pattern. -/
theorem highNeutral_iff_adjacent (b : Int) (qs : List Int) :
    HighNeutral b qs ↔ ∃ front high tail,
      qs = front ++ high :: (b-1) :: tail ∧ b ≤ high := by
  induction qs with
  | nil =>
    constructor
    · intro h; contradiction
    · rintro ⟨front,high,tail,he,_⟩
      cases front <;> simp at he
  | cons q qs ih =>
    constructor
    · intro h
      rcases h with ⟨hh,hs⟩ | ht
      · cases qs with
        | nil => contradiction
        | cons a tail =>
          change a=b-1 at hs
          subst a
          exact ⟨[],q,tail,rfl,hh⟩
      · obtain ⟨front,high,tail,he,hh⟩ := ih.mp ht
        exact ⟨q::front,high,tail,by simp [he],hh⟩
    · rintro ⟨front,high,tail,he,hh⟩
      cases front with
      | nil =>
        have hc : q=high ∧ qs=(b-1)::tail := List.cons.inj he
        rw [hc.1,hc.2]
        exact Or.inl ⟨hh,rfl⟩
      | cons a front =>
        have hc : q=a ∧ qs=front++high::(b-1)::tail := List.cons.inj he
        exact Or.inr (ih.mpr ⟨front,high,tail,hc.2,hh⟩)

end IntrinsicPattern
