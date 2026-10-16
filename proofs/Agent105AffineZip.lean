import Agent105AffineBasics
import Agent102AffineArithmetic

/-!
Agent #105, session 8f1107db019a. Exact run-prefix algebra for the original
`Agent8.zipAdd`, and its unconditional affine-run closure. The structural
helper keeps its two scalar interfaces explicit; the final theorem discharges
both using Agent #102's published affine comparison and positive-part results.
-/

namespace Agent105.AffineDynamics

open Agent102

theorem zipAdd_replicate_prefix_le (x y m n : Nat) (as bs : List Nat)
    (hle : m ≤ n) :
    Agent8.zipAdd (List.replicate m x ++ as) (List.replicate n y ++ bs) =
      List.replicate m (x + y) ++
        Agent8.zipAdd as (List.replicate (n - m) y ++ bs) := by
  induction m generalizing n with
  | zero => simp
  | succ m ih =>
    cases n with
    | zero => omega
    | succ n =>
      have hmn : m ≤ n := by omega
      simpa [List.replicate_succ, Agent8.zipAdd] using
        congrArg (List.cons (x + y)) (ih n hmn)

theorem zipAdd_replicate_prefix_ge (x y m n : Nat) (as bs : List Nat)
    (hle : n ≤ m) :
    Agent8.zipAdd (List.replicate m x ++ as) (List.replicate n y ++ bs) =
      List.replicate n (x + y) ++
        Agent8.zipAdd (List.replicate (m - n) x ++ as) bs := by
  induction n generalizing m with
  | zero => simp
  | succ n ih =>
    cases m with
    | zero => omega
    | succ m =>
      have hnm : n ≤ m := by omega
      simpa [List.replicate_succ, Agent8.zipAdd] using
        congrArg (List.cons (x + y)) (ih m hnm)

/-- Each scalar difference can be represented on a tail. This is an explicit
interface of the structural lemma, not an axiom or an established conclusion. -/
def AffineDifferenceClosure : Prop :=
  ∀ f g : Affine, ∃ d : Affine, ∃ K : Nat, ∀ k, K ≤ k →
    (d.eval k).toNat = (f.eval k).toNat - (g.eval k).toNat

/-- On a tail the two scalar lengths have a fixed weak ordering. -/
def AffineComparisonStable : Prop :=
  ∀ f g : Affine,
    (∃ K : Nat, ∀ k, K ≤ k → (f.eval k).toNat ≤ (g.eval k).toNat) ∨
    (∃ K : Nat, ∀ k, K ≤ k → (g.eval k).toNat ≤ (f.eval k).toNat)

theorem zipAdd_of_length_arithmetic
    (hdiff : AffineDifferenceClosure) (hcompare : AffineComparisonStable)
    (rs ss : List RunSpec) (M N : Nat)
    (hr : SpecBound rs M) (hs : SpecBound ss N) :
    ∃ ts : List RunSpec, SpecBound ts (M + N) ∧
      ∃ K : Nat, ∀ k, K ≤ k →
        Agent8.zipAdd (wordAt rs k) (wordAt ss k) = wordAt ts k := by
  have main : ∀ n : Nat, ∀ rs ss : List RunSpec,
      rs.length + ss.length ≤ n → SpecBound rs M → SpecBound ss N →
      ∃ ts : List RunSpec, SpecBound ts (M + N) ∧
        ∃ K : Nat, ∀ k, K ≤ k →
          Agent8.zipAdd (wordAt rs k) (wordAt ss k) = wordAt ts k := by
    intro n
    induction n using Nat.strongRecOn with
    | ind n ih =>
      intro rs ss hsize hrs hss
      cases rs with
      | nil =>
        exact ⟨[], specBound_nil _, 0, fun _ _ => rfl⟩
      | cons r rs =>
        cases ss with
        | nil =>
          refine ⟨[], specBound_nil _, 0, ?_⟩
          intro k hk
          simp [Agent8.zipAdd_eq_zipWith]
        | cons s ss =>
          have hrM : r.digit ≤ M := hrs r (by simp)
          have hsN : s.digit ≤ N := hss s (by simp)
          have hrs' : SpecBound rs M := fun a ha => hrs a (by simp [ha])
          have hss' : SpecBound ss N := fun a ha => hss a (by simp [ha])
          rcases hcompare r.length s.length with hc | hc
          · obtain ⟨Kc, hc⟩ := hc
            obtain ⟨d, Kd, hd⟩ := hdiff s.length r.length
            let residual : RunSpec := ⟨s.digit, d⟩
            have hres : SpecBound (residual :: ss) N :=
              specBound_cons hsN hss'
            have hlt : rs.length + (residual :: ss).length < n := by
              simp only [List.length_cons] at *
              omega
            obtain ⟨ts, hts, Kt, ht⟩ :=
              ih _ hlt rs (residual :: ss) (Nat.le_refl _) hrs' hres
            let first : RunSpec := ⟨r.digit + s.digit, r.length⟩
            refine ⟨first :: ts, specBound_cons (by dsimp [first]; omega) hts,
              max Kc (max Kd Kt), ?_⟩
            intro k hk
            have hkc : Kc ≤ k := Nat.le_trans (Nat.le_max_left _ _) hk
            have hkd : Kd ≤ k := Nat.le_trans
              (Nat.le_trans (Nat.le_max_left _ _) (Nat.le_max_right _ _)) hk
            have hkt : Kt ≤ k := Nat.le_trans
              (Nat.le_trans (Nat.le_max_right _ _) (Nat.le_max_right _ _)) hk
            rw [wordAt_cons, wordAt_cons,
              zipAdd_replicate_prefix_le _ _ _ _ _ _ (hc k hkc)]
            have htail := ht k hkt
            simp only [wordAt_cons, residual] at htail
            rw [hd k hkd] at htail
            rw [htail]
            simp [first]
          · obtain ⟨Kc, hc⟩ := hc
            obtain ⟨d, Kd, hd⟩ := hdiff r.length s.length
            let residual : RunSpec := ⟨r.digit, d⟩
            have hres : SpecBound (residual :: rs) M :=
              specBound_cons hrM hrs'
            have hlt : (residual :: rs).length + ss.length < n := by
              simp only [List.length_cons] at *
              omega
            obtain ⟨ts, hts, Kt, ht⟩ :=
              ih _ hlt (residual :: rs) ss (Nat.le_refl _) hres hss'
            let first : RunSpec := ⟨r.digit + s.digit, s.length⟩
            refine ⟨first :: ts, specBound_cons (by dsimp [first]; omega) hts,
              max Kc (max Kd Kt), ?_⟩
            intro k hk
            have hkc : Kc ≤ k := Nat.le_trans (Nat.le_max_left _ _) hk
            have hkd : Kd ≤ k := Nat.le_trans
              (Nat.le_trans (Nat.le_max_left _ _) (Nat.le_max_right _ _)) hk
            have hkt : Kt ≤ k := Nat.le_trans
              (Nat.le_trans (Nat.le_max_right _ _) (Nat.le_max_right _ _)) hk
            rw [wordAt_cons, wordAt_cons,
              zipAdd_replicate_prefix_ge _ _ _ _ _ _ (hc k hkc)]
            have htail := ht k hkt
            simp only [wordAt_cons, residual] at htail
            rw [hd k hkd] at htail
            rw [htail]
            simp [first]
  exact main _ rs ss (Nat.le_refl _) hr hs

/-- Difference of the eventual nonnegative affine representatives. Truncation
is applied before taking the difference, through the original positivePart. -/
def affineDifference (f g : Affine) : Affine :=
  ⟨f.positivePart.slope - g.positivePart.slope,
    f.positivePart.intercept - g.positivePart.intercept⟩

theorem affineDifference_eval (f g : Affine) (k : Nat) :
    (affineDifference f g).eval k =
      f.positivePart.eval k - g.positivePart.eval k := by
  simp only [affineDifference, Affine.eval, Int.sub_mul]
  omega

/-- Adapter from Agent102's proved positive-part identity. -/
theorem affineDifferenceClosure : AffineDifferenceClosure := by
  intro f g
  refine ⟨affineDifference f g, max f.cutoff g.cutoff, ?_⟩
  intro k hk
  have hf : f.cutoff ≤ k := Nat.le_trans (Nat.le_max_left _ _) hk
  have hg : g.cutoff ≤ k := Nat.le_trans (Nat.le_max_right _ _) hk
  rw [affineDifference_eval, Affine.eval_positivePart f k hf,
    Affine.eval_positivePart g k hg]
  omega

/-- Adapter from Agent102's proved affine weak-comparison stability. -/
theorem affineComparisonStable : AffineComparisonStable := by
  intro f g
  let K := Affine.compareCutoff f g
  by_cases h : f.eval K ≤ g.eval K
  · left
    refine ⟨K, ?_⟩
    intro k hk
    have he := (Affine.eval_le_stable f g K k (Nat.le_refl _) hk).mpr h
    omega
  · right
    refine ⟨K, ?_⟩
    intro k hk
    have he := Affine.eval_le_stable f g K k (Nat.le_refl _) hk
    have hn : ¬ f.eval k ≤ g.eval k := fun hh => h (he.mp hh)
    omega

theorem zipAdd_wordAt_eventually (rs ss : List RunSpec) (M N : Nat)
    (hr : SpecBound rs M) (hs : SpecBound ss N) :
    ∃ ts : List RunSpec, SpecBound ts (M + N) ∧
      ∃ K : Nat, ∀ k, K ≤ k →
        Agent8.zipAdd (wordAt rs k) (wordAt ss k) = wordAt ts k :=
  zipAdd_of_length_arithmetic affineDifferenceClosure affineComparisonStable
    rs ss M N hr hs

end Agent105.AffineDynamics

#print axioms Agent105.AffineDynamics.zipAdd_replicate_prefix_le
#print axioms Agent105.AffineDynamics.zipAdd_replicate_prefix_ge
#print axioms Agent105.AffineDynamics.zipAdd_of_length_arithmetic
#print axioms Agent105.AffineDynamics.affineDifference_eval
#print axioms Agent105.AffineDynamics.affineDifferenceClosure
#print axioms Agent105.AffineDynamics.affineComparisonStable
#print axioms Agent105.AffineDynamics.zipAdd_wordAt_eventually
