import resume_renewal_certificate

namespace NormalizationReach
open OverflowNormalizationCertificate

def badPrefix (out : Nat → Nat) : Nat → Bool
  | 0 => false
  | k+1 => badPrefix out k || decide (out k > 9)

theorem badPrefix_eq_false_iff (out : Nat → Nat) (k : Nat) :
    badPrefix out k = false ↔ ∀ i, i < k → out i ≤ 9 := by
  induction k with
  | zero => simp [badPrefix]
  | succ k ih =>
    simp only [badPrefix, Bool.or_eq_false_iff, decide_eq_false_iff_not, Nat.not_lt, ih]
    constructor
    · rintro ⟨hprev, hlast⟩ i hi
      by_cases he : i = k
      · simpa [he] using hlast
      · exact hprev i (by omega)
    · intro h
      exact ⟨fun i hi => h i (by omega), h k (by omega)⟩

theorem initial_mem (first : Nat) (hs : List Nat) (ns : Nat)
    (tail : List Nat) (out : Nat)
    (hn : (first, ns) ∈ normEdges 2)
    (hf : (tail, out) ∈
      feed (hs.map fun h => 2*h + if h=1 then 4 else 0) first hs) :
    (⟨ns, tail, decide (out > 9)⟩ : State) ∈ initials first hs := by
  simp only [initials, List.mem_flatMap]
  refine ⟨(first, ns), hn, ?_⟩
  simp only [if_true, List.mem_map]
  exact ⟨(tail, out), hf, rfl⟩

theorem next_mem (hs : List Nat) (s ns q out : Nat) (layers tail : List Nat)
    (bad : Bool) (hn : (q, ns) ∈ normEdges s)
    (hf : (tail, out) ∈ feed layers q hs) :
    (⟨ns, tail, bad || decide (out > 9)⟩ : State) ∈ next hs ⟨s,layers,bad⟩ := by
  simp only [next, List.mem_flatMap]
  refine ⟨(q,ns),hn,?_⟩
  simp only [List.mem_map]
  exact ⟨(tail,out),hf,rfl⟩

theorem reach_of_traces (first : Nat) (hs : List Nat)
    (ns : Nat → Nat) (layers : Nat → List Nat) (q out : Nat → Nat) (k : Nat)
    (hns : ns 0 = 2)
    (hlayers : layers 0 = hs.map fun h => 2*h + if h=1 then 4 else 0)
    (hq : q 0 = first)
    (hn : ∀ i, i < k → (q i, ns (i+1)) ∈ normEdges (ns i))
    (hf : ∀ i, i < k → (layers (i+1), out i) ∈ feed (layers i) (q i) hs)
    (hk : 0 < k) :
    Reach first hs ⟨ns k, layers k, badPrefix out k⟩ := by
  induction k with
  | zero => omega
  | succ k ih =>
    cases k with
    | zero =>
      have hn0 := hn 0 (by omega)
      have hf0 := hf 0 (by omega)
      rw [hns, hq] at hn0
      rw [hlayers, hq] at hf0
      simpa [badPrefix] using Reach.initial (initial_mem first hs (ns 1) (layers 1) (out 0) hn0 hf0)
    | succ j =>
      have hr := ih (fun i hi => hn i (by omega)) (fun i hi => hf i (by omega)) (by omega)
      exact Reach.advance hr (next_mem hs (ns (j+1)) (ns (j+1+1)) (q (j+1))
        (out (j+1)) (layers (j+1)) (layers (j+1+1)) (badPrefix out (j+1))
        (hn (j+1) (by omega)) (hf (j+1) (by omega)))

theorem finals_mem_none (hs : List Nat) (s : State) (b : Bool)
    (he : s.norm % 2 = s.norm / 2)
    (hf : b ∈ finish s.layers none hs s.bad) : b ∈ finals hs s := by
  simp only [finals, he, if_true, List.mem_flatMap]
  exact ⟨none, by simp, hf⟩

theorem finals_mem_some (hs : List Nat) (s : State) (b : Bool)
    (hf : b ∈ finish s.layers (some (10*(s.norm/2))) hs s.bad) :
    b ∈ finals hs s := by
  simp only [finals, List.mem_flatMap]
  exact ⟨some (10*(s.norm/2)), by simp, hf⟩

theorem finishFuel_true (fuel : Nat) (layers : List Nat) (c : Option Nat)
    (hs : List Nat) (b : Bool)
    (hm : b ∈ finishFuel fuel layers c hs true) : b = true := by
  induction fuel generalizing layers c hs with
  | zero => simp [finishFuel] at hm
  | succ fuel ih =>
    cases layers with
    | nil => simpa [finishFuel] using hm
    | cons s ss =>
      cases hs with
      | nil => simp [finishFuel] at hm
      | cons h hs =>
        cases c with
        | none =>
          simp only [finishFuel] at hm
          split at hm
          · exact ih _ _ _ hm
          · simp at hm
        | some z =>
          simp only [finishFuel] at hm
          split at hm
          · split at hm
            · simp only [List.mem_flatMap] at hm
              obtain ⟨pair,_,hm⟩ := hm
              simp only [Bool.true_or] at hm
              exact ih _ _ _ hm
            · exact ih _ _ _ hm
          · simp at hm

theorem finish_false_implies_bad_false (layers : List Nat) (c : Option Nat)
    (hs : List Nat) (bad : Bool) (hm : false ∈ finish layers c hs bad) : bad = false := by
  cases bad with
  | false => rfl
  | true => have := finishFuel_true _ _ _ _ _ hm; contradiction

theorem finals_false_implies_bad_false (hs : List Nat) (s : State)
    (hm : false ∈ finals hs s) : s.bad = false := by
  simp only [finals, List.mem_flatMap] at hm
  obtain ⟨c,_,hm⟩ := hm
  exact finish_false_implies_bad_false _ _ _ _ hm

#print axioms badPrefix_eq_false_iff
#print axioms reach_of_traces
#print axioms finals_mem_none
#print axioms finals_mem_some
#print axioms finals_false_implies_bad_false
end NormalizationReach
