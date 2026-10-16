import Agent1RepeatedBlock
import Agent102RunDefs
import Agent105AffineBasics

/-!
Agent #105, session 8f1107db019a: actual decimal normalization of affine run words.

The constant-run identities below specialize Agent #1's exact repeated-block
normalization; all digit and carry operations are the original Agent8 operations.
No arithmetic update is replaced by a model. The shared run representation is
Agent102.RunSpec, whose signed affine lengths are expanded using Int.toNat.
-/

namespace Agent105.AffineNormalize

open Agent8 Agent102
open Agent105.AffineDynamics

/-- A singleton block power is the ordinary list replicate. -/
theorem singleton_pow (x k : Nat) :
    Agent1.RepeatedBlock.pow [x] k = List.replicate k x := by
  induction k with
  | zero => rfl
  | succ k ih => simp [Agent1.RepeatedBlock.pow, ih, List.replicate_succ]

private theorem bounded_singleton (x : Nat) (hx : x ≤ 18) : Bounded [x] 18 := by
  intro y hy
  simp only [List.mem_singleton] at hy
  simpa only [hy] using hx

/-- Positive constant runs have the outgoing carry of their first column.
The symbol nine and its incoming-carry dependence are included. -/
theorem terminalCarry_replicate_succ (x e k : Nat) (hx : x ≤ 18) (he : e ≤ 1) :
    terminalCarry (List.replicate (k + 1) x) e = (x + e) / 10 := by
  have h := Agent1.RepeatedBlock.terminalCarry_pow_succ [x] e k
    (bounded_singleton x hx) he
  simpa only [singleton_pow, terminalCarry] using h

/-- The actual first digit is retained; the remaining digits use the stabilized
carry, by the existing repeated-block theorem. -/
theorem fixedDigits_replicate_succ (x e k : Nat) (hx : x ≤ 18) (he : e ≤ 1) :
    fixedDigits (List.replicate (k + 1) x) e =
      [(x + e) % 10] ++ List.replicate k ((x + (x + e) / 10) % 10) := by
  have h := Agent1.RepeatedBlock.fixedDigits_pow_succ [x] e k
    (bounded_singleton x hx) he
  simpa only [singleton_pow, fixedDigits, terminalCarry] using h

/-- Exact full constant-run normalization, with the original appended overflow. -/
theorem normalize_replicate_succ (x e k : Nat) (hx : x ≤ 18) (he : e ≤ 1) :
    normalize (List.replicate (k + 1) x) e =
      [(x + e) % 10] ++ List.replicate k ((x + (x + e) / 10) % 10) ++
        (if (x + e) / 10 = 0 then [] else [(x + e) / 10]) := by
  rw [normalize_decompose, fixedDigits_replicate_succ x e k hx he,
    terminalCarry_replicate_succ x e k hx he]

/-- This incoming-carry formula includes zero copies of nine. -/
theorem terminalCarry_replicate_nine (m e : Nat) (he : e ≤ 1) :
    terminalCarry (List.replicate m 9) e = e := by
  cases m with
  | zero => rfl
  | succ m =>
    rw [terminalCarry_replicate_succ 9 e m (by decide) he]
    omega

theorem fixedDigits_replicate_nine (m e : Nat) (he : e ≤ 1) :
    fixedDigits (List.replicate m 9) e = List.replicate m ((9 + e) % 10) := by
  cases m with
  | zero => rfl
  | succ m =>
    rw [fixedDigits_replicate_succ 9 e m (by decide) he]
    have hc : (9 + e) / 10 = e := by omega
    simp only [hc, List.singleton_append, List.replicate_succ]

/-- Empty neutral runs retain the input carry; nonempty neutral runs retain
its digit effect. Neither zero columns nor the final carry are removed. -/
theorem normalize_replicate_nine (m e : Nat) (he : e ≤ 1) :
    normalize (List.replicate m 9) e =
      List.replicate m ((9 + e) % 10) ++ (if e = 0 then [] else [e]) := by
  rw [normalize_decompose, fixedDigits_replicate_nine m e he,
    terminalCarry_replicate_nine m e he]

/-- A positive input run contributes a first digit and an affine remainder.
The remainder may have length zero; signed affine intercepts are retained. -/
def fixedRunSpec (r : RunSpec) (e : Nat) : List RunSpec :=
  [constRun ((r.digit + e) % 10) 1,
    ⟨(r.digit + (r.digit + e) / 10) % 10, minusOne r.length⟩]

theorem fixedRunSpec_bound (r : RunSpec) (e : Nat) :
    SpecBound (fixedRunSpec r e) 9 := by
  apply specBound_cons
  · simp only [constRun]
    omega
  · apply specBound_cons
    · dsimp
      omega
    · exact specBound_nil 9

/-- Exact expansion of a positive affine run at one parameter, before
the terminal carry is appended. -/
theorem fixedDigits_carry_positive_run (r : RunSpec) (e k : Nat)
    (hr : r.digit ≤ 18) (he : e ≤ 1)
    (hpos : 0 < (r.length.eval k).toNat) :
    fixedDigits (List.replicate (r.length.eval k).toNat r.digit) e =
        wordAt (fixedRunSpec r e) k ∧
      terminalCarry (List.replicate (r.length.eval k).toNat r.digit) e =
        (r.digit + e) / 10 := by
  have hn : (r.length.eval k).toNat - 1 + 1 = (r.length.eval k).toNat := by omega
  have hd := fixedDigits_replicate_succ r.digit e
    ((r.length.eval k).toNat - 1) hr he
  have hc := terminalCarry_replicate_succ r.digit e
    ((r.length.eval k).toNat - 1) hr he
  rw [hn] at hd hc
  constructor
  · rw [hd]
    simp only [fixedRunSpec, wordAt_cons, wordAt_nil, List.append_nil,
      minusOne_toNat]
    simp [constRun, Affine.eval]
  · exact hc

/-- The only scalar input needed to normalize a fixed finite run list:
each affine length is eventually either absent or strictly positive. -/
def LengthDichotomy (f : Affine) : Prop :=
  (∃ K : Nat, ∀ k, K ≤ k → (f.eval k).toNat = 0) ∨
    (∃ K : Nat, ∀ k, K ≤ k → 0 < (f.eval k).toNat)

/-- Structural normalization with a stable outgoing carry. The scalar
length dichotomy is separated from the actual decimal calculation. -/
theorem fixedDigits_carry_of_length_dichotomy
    (rs : List RunSpec) (e : Nat) (hrs : SpecBound rs 18) (he : e ≤ 1)
    (hlen : ∀ r ∈ rs, LengthDichotomy r.length) :
    ∃ ds : List RunSpec, ∃ c K : Nat,
      SpecBound ds 9 ∧ c ≤ 1 ∧
        ∀ k, K ≤ k →
          fixedDigits (wordAt rs k) e = wordAt ds k ∧
          terminalCarry (wordAt rs k) e = c := by
  induction rs generalizing e with
  | nil =>
    exact ⟨[], e, 0, specBound_nil 9, he, fun _ _ => ⟨rfl, rfl⟩⟩
  | cons r rs ih =>
    have hr : r.digit ≤ 18 := hrs r (by simp)
    have hs : SpecBound rs 18 := fun s h => hrs s (by simp [h])
    have hls : ∀ s ∈ rs, LengthDichotomy s.length :=
      fun s h => hlen s (by simp [h])
    rcases hlen r (by simp) with hz | hp
    · obtain ⟨K₀, hzero⟩ := hz
      obtain ⟨ds, c, K₁, hb, hc, hd⟩ := ih e hs he hls
      refine ⟨ds, c, max K₀ K₁, hb, hc, ?_⟩
      intro k hk
      have hz := hzero k (Nat.le_trans (Nat.le_max_left _ _) hk)
      have ht := hd k (Nat.le_trans (Nat.le_max_right _ _) hk)
      simpa [wordAt_cons, hz] using ht
    · obtain ⟨K₀, hpos⟩ := hp
      have hc₀ : (r.digit + e) / 10 ≤ 1 := by omega
      obtain ⟨ds, c, K₁, hb, hc, hd⟩ := ih ((r.digit + e) / 10) hs hc₀ hls
      refine ⟨fixedRunSpec r e ++ ds, c, max K₀ K₁, ?_, hc, ?_⟩
      · intro s hs'
        rcases List.mem_append.mp hs' with hs' | hs'
        · exact fixedRunSpec_bound r e s hs'
        · exact hb s hs'
      · intro k hk
        have hp := hpos k (Nat.le_trans (Nat.le_max_left _ _) hk)
        obtain ⟨hdf, hdc⟩ := fixedDigits_carry_positive_run r e k hr he hp
        obtain ⟨htf, htc⟩ := hd k (Nat.le_trans (Nat.le_max_right _ _) hk)
        constructor
        · rw [wordAt_cons, fixedDigits_append, hdf, hdc, htf, wordAt_append]
        · rw [wordAt_cons, terminalCarry_append, hdc, htc]

/-- Appending the stable carry preserves the affine-run representation
and the actual decimal digit bound. -/
theorem normalize_of_length_dichotomy
    (rs : List RunSpec) (e : Nat) (hrs : SpecBound rs 18) (he : e ≤ 1)
    (hlen : ∀ r ∈ rs, LengthDichotomy r.length) :
    ∃ ds : List RunSpec, ∃ c K : Nat,
      SpecBound ds 9 ∧ c ≤ 1 ∧
        ∀ k, K ≤ k →
          normalize (wordAt rs k) e = wordAt ds k ∧
          terminalCarry (wordAt rs k) e = c := by
  obtain ⟨ds, c, K, hb, hc, hd⟩ :=
    fixedDigits_carry_of_length_dichotomy rs e hrs he hlen
  by_cases hz : c = 0
  · refine ⟨ds, c, K, hb, hc, ?_⟩
    intro k hk
    obtain ⟨hf, ht⟩ := hd k hk
    constructor
    · rw [normalize_decompose, hf, ht]
      simp [hz]
    · exact ht
  · refine ⟨ds ++ [constRun c 1], c, K, ?_, hc, ?_⟩
    · intro r hr
      rcases List.mem_append.mp hr with hr | hr
      · exact hb r hr
      · have hr' : r = constRun c 1 := List.mem_singleton.mp hr
        subst r
        simp only [constRun]
        omega
    · intro k hk
      obtain ⟨hf, ht⟩ := hd k hk
      constructor
      · rw [normalize_decompose, hf, ht, wordAt_append, wordAt_constRun]
        simp [hz]
      · exact ht

/-- Tail representations are enough: the input word may differ at any
finite number of parameters below its representation cutoff. -/
theorem hasAffineRuns_normalize_of_length_dichotomy
    (hlen : ∀ f : Affine, LengthDichotomy f)
    (w : Nat → List Nat) (hw : HasAffineRuns w 18) (e : Nat) (he : e ≤ 1) :
    HasAffineRuns (fun k => normalize (w k) e) 9 := by
  obtain ⟨rs, hrs, K₀, hword⟩ := hw
  obtain ⟨ds, c, K₁, hb, _, hd⟩ :=
    normalize_of_length_dichotomy rs e hrs he (fun r _ => hlen r.length)
  refine ⟨ds, hb, max K₀ K₁, ?_⟩
  intro k hk
  rw [hword k (Nat.le_trans (Nat.le_max_left _ _) hk)]
  exact (hd k (Nat.le_trans (Nat.le_max_right _ _) hk)).1

end Agent105.AffineNormalize

#print axioms Agent105.AffineNormalize.terminalCarry_replicate_succ
#print axioms Agent105.AffineNormalize.fixedDigits_replicate_succ
#print axioms Agent105.AffineNormalize.normalize_replicate_nine
#print axioms Agent105.AffineNormalize.fixedDigits_carry_of_length_dichotomy
#print axioms Agent105.AffineNormalize.normalize_of_length_dichotomy
#print axioms Agent105.AffineNormalize.hasAffineRuns_normalize_of_length_dichotomy
