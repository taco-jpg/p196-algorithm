import P196.Agent2OverflowFibers.Agent2OverflowActual
import P196.Agent2OverflowFibers.Agent2OverflowLocal

/-!
Agent #2: actual overflow fibers inject into one Boolean carry per free pair.
The outer pair is fixed by the target; an odd central coefficient is fixed by
its even parity and the matching actual carries.
-/
namespace P196.Agent2.OverflowFibers

set_option maxRecDepth 10000
set_option maxHeartbeats 4000000

/-- The high outgoing carry of each free mirrored coefficient, excluding
the outer coefficient and, when present, the even central coefficient. -/
def carryCode (q : List Nat) : List Nat :=
  (List.range (q.length / 2 - 1)).map
    (fun j => carryAt q 0 (q.length - (j + 1)))

theorem carryCode_length (q : List Nat) :
    (carryCode q).length = q.length / 2 - 1 := by simp [carryCode]

theorem carryCode_get (q : List Nat) (j : Nat) (hj : j < q.length / 2 - 1) :
    (carryCode q)[j]! = carryAt q 0 (q.length - (j + 1)) := by
  simp only [carryCode, List.getElem!_eq_getElem?_getD,
    List.getElem?_map, List.getElem?_range hj]
  rfl

theorem carryCode_bound (q : List Nat) (hq : ∀ x ∈ q, x ≤ 18) :
    ∀ b ∈ carryCode q, b ≤ 1 := by
  intro b hb
  obtain ⟨j, hj, rfl⟩ := List.mem_map.mp hb
  exact carryAt_bound q 0 _ (by decide) hq

theorem carryCode_eq_carry (q r : List Nat) (hlen : q.length = r.length)
    (heq : carryCode q = carryCode r) (i : Nat)
    (h0 : 0 < i) (hi : i < q.length / 2) :
    carryAt q 0 (q.length - i) = carryAt r 0 (r.length - i) := by
  have h := congrArg (fun w : List Nat => w[i - 1]!) heq
  dsimp only at h
  rw [carryCode_get q (i - 1) (by omega),
    carryCode_get r (i - 1) (by omega)] at h
  simpa only [Nat.sub_add_cancel (by omega : 1 ≤ i)] using h

theorem canonical_coefficient_bound (q : List Nat) (hq : Canonical q)
    (i : Nat) (hi : i < q.length) : q[i]! ≤ 18 := by
  rw [getElemBang_eq q i hi]
  exact hq.2.1 _ (List.getElem_mem hi)

theorem overflow_outer_ge_nine (q : List Nat) (hq : Canonical q)
    (hn : 0 < q.length) (hc : carryAt q 0 q.length = 1) : 9 ≤ q[0]! := by
  have hi : q.length - 1 < q.length := by omega
  have hs := carryAt_succ q 0 (q.length - 1) hi
  have hb := carryAt_bound q 0 (q.length - 1) (by decide) hq.2.1
  have hm := symmetric_getElemBang q hq.1 0 hn
  simp only [Nat.sub_zero] at hm
  rw [hm, show q.length - 1 + 1 = q.length by omega, hc] at hs
  omega

theorem actual_overflow_prefix_unique (L : Nat) (target q r : List Nat)
    (hL : 2 ≤ L) (hq : ActualOverflowFiber L target q)
    (hr : ActualOverflowFiber L target r) (hcode : carryCode q = carryCode r) :
    ∀ n : Nat, n ≤ (L + 1) / 2 →
      (∀ i, i < n → q[i]! = r[i]!) ∧ carryAt q 0 n = carryAt r 0 n := by
  obtain ⟨hql, hqc, hqf, hqt⟩ := hq
  obtain ⟨hrl, hrc, hrf, hrt⟩ := hr
  have hlen : q.length = r.length := hql.trans hrl.symm
  have hstep : Agent8.stepWord q = Agent8.stepWord r := hqt.trans hrt.symm
  intro n
  induction n with
  | zero => intro hn; exact ⟨by intro i hi; omega, by simp⟩
  | succ n ih =>
    intro hn
    obtain ⟨hprev, hlow⟩ := ih (by omega)
    have hnq : n < q.length := by omega
    have hnr : n < r.length := by omega
    have hxb : q[n]! ≤ 18 := canonical_coefficient_bound q hqc n hnq
    have hyb : r[n]! ≤ 18 := canonical_coefficient_bound r hrc n hnr
    have hcurrent : q[n]! = r[n]! := by
      by_cases hn0 : n = 0
      · subst n
        have htarget := congrArg (fun w : List Nat => w[0]!) hstep
        dsimp only at htarget
        rw [overflow_step_outer q (by omega) hqf,
          overflow_step_outer r (by omega) hrf] at htarget
        exact overflow_outer_injective _ _
          (overflow_outer_ge_nine q hqc (by omega) hqf) hxb
          (overflow_outer_ge_nine r hrc (by omega) hrf) hyb htarget
      · have hnpos : 0 < n := by omega
        have hp := hprev (n - 1) (by omega)
        have hqm : q[q.length - n]! = q[n - 1]! := by
          have h := symmetric_getElemBang q hqc.1 (n - 1) (by omega)
          have hj : q.length - 1 - (n - 1) = q.length - n := by omega
          simpa only [hj] using h
        have hrm : r[r.length - n]! = r[n - 1]! := by
          have h := symmetric_getElemBang r hrc.1 (n - 1) (by omega)
          have hj : r.length - 1 - (n - 1) = r.length - n := by omega
          simpa only [hj] using h
        have htarget := congrArg (fun w : List Nat => w[n]!) hstep
        dsimp only at htarget
        rw [overflow_step_inner q n hnpos hnq hqf,
          overflow_step_inner r n hnpos hnr hrf, hqm, hrm,
          ← hlow, ← hp] at htarget
        have hqmirror := symmetric_getElemBang q hqc.1 n hnq
        have hrmirror := symmetric_getElemBang r hrc.1 n hnr
        have hqcarr :
            (q[n]! + carryAt q 0 (q.length - 1 - n)) / 10 =
              carryAt q 0 (q.length - n) := by
          have h := carryAt_succ q 0 (q.length - 1 - n) (by omega)
          rw [hqmirror] at h
          have hj : q.length - 1 - n + 1 = q.length - n := by omega
          rw [hj] at h
          exact h.symm
        have hrcarr :
            (r[n]! + carryAt r 0 (r.length - 1 - n)) / 10 =
              carryAt r 0 (r.length - n) := by
          have h := carryAt_succ r 0 (r.length - 1 - n) (by omega)
          rw [hrmirror] at h
          have hj : r.length - 1 - n + 1 = r.length - n := by omega
          rw [hj] at h
          exact h.symm
        have hcx := carryAt_bound q 0 (q.length - 1 - n) (by decide) hqc.2.1
        have hcy := carryAt_bound r 0 (r.length - 1 - n) (by decide) hrc.2.1
        by_cases hnfree : n < L / 2
        · have hhigh := carryCode_eq_carry q r hlen hcode n hnpos (by omega)
          rw [← hhigh] at hrcarr htarget
          exact inward_fixed_high_injective _ _ _ _ _ _ _
            hxb hyb hcx hcy hqcarr hrcarr htarget
        · have hodd : L % 2 = 1 := by omega
          have hcenter : n = L / 2 := by omega
          have hqx : q[n]! % 2 = 0 := by
            have h := hqc.2.2.2 (by omega)
            simpa [hql, hcenter] using h
          have hry : r[n]! % 2 = 0 := by
            have h := hrc.2.2.2 (by omega)
            simpa [hrl, hcenter] using h
          have hboundary :
              carryAt q 0 (q.length - n + 1) =
                carryAt r 0 (r.length - n + 1) := by
            by_cases hn1 : n = 1
            · have hqi : q.length - n + 1 = q.length := by omega
              have hri : r.length - n + 1 = r.length := by omega
              rw [hqi, hri, hqf, hrf]
            · have hh := carryCode_eq_carry q r hlen hcode (n - 1)
                (by omega) (by omega)
              have hqi : q.length - (n - 1) = q.length - n + 1 := by omega
              have hri : r.length - (n - 1) = r.length - n + 1 := by omega
              simpa only [hqi, hri] using hh
          have hqprev := carryAt_succ q 0 (q.length - n) (by omega)
          have hrprev := carryAt_succ r 0 (r.length - n) (by omega)
          rw [hqm] at hqprev
          rw [hrm, ← hp] at hrprev
          have hcarryprev :
              (q[n - 1]! + carryAt q 0 (q.length - n)) / 10 =
                (q[n - 1]! + carryAt r 0 (r.length - n)) / 10 := by
            rw [← hqprev, ← hrprev]
            exact hboundary
          exact odd_center_injective _ _ _ _ _ _ _ _
            hxb hyb hcx hcy hqcarr hrcarr hqx hry hcarryprev htarget
    refine ⟨?_, ?_⟩
    · intro i hi
      by_cases hin : i = n
      · simpa [hin] using hcurrent
      · exact hprev i (by omega)
    · rw [carryAt_succ q 0 n hnq, carryAt_succ r 0 n hnr, hcurrent, hlow]

theorem actual_overflow_code_injective (L : Nat) (target q r : List Nat)
    (hL : 2 ≤ L) (hq : ActualOverflowFiber L target q)
    (hr : ActualOverflowFiber L target r) (hcode : carryCode q = carryCode r) :
    q = r := by
  have hp := (actual_overflow_prefix_unique L target q r hL hq hr hcode
    ((L + 1) / 2) (Nat.le_refl _)).1
  have hlen : q.length = r.length := hq.1.trans hr.1.symm
  apply List.ext_getElem hlen
  intro i hi hj
  rw [← getElemBang_eq q i hi, ← getElemBang_eq r i hj]
  by_cases hsmall : i < (L + 1) / 2
  · exact hp i hsmall
  · have hmirror : L - 1 - i < (L + 1) / 2 := by omega
    have hh := hp (L - 1 - i) hmirror
    have hqs := symmetric_getElemBang q hq.2.1.1 i hi
    have hrs := symmetric_getElemBang r hr.2.1.1 i hj
    rw [← hqs, ← hrs]
    simpa only [hq.1, hr.1] using hh

/-- Explicit complete list of Boolean-valued words of a fixed length. -/
def binaryCodes : Nat → List (List Nat)
  | 0 => [[]]
  | n + 1 => (binaryCodes n).map (0 :: ·) ++ (binaryCodes n).map (1 :: ·)

theorem binaryCodes_length (n : Nat) : (binaryCodes n).length = 2 ^ n := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [binaryCodes, List.length_append, List.length_map, ih,
      Nat.pow_succ]; omega

theorem mem_binaryCodes (q : List Nat) (hq : ∀ x ∈ q, x ≤ 1) :
    q ∈ binaryCodes q.length := by
  induction q with
  | nil => simp [binaryCodes]
  | cons x xs ih =>
    have hx : x ≤ 1 := hq x (by simp)
    have ht := ih (by intro y hy; exact hq y (by simp [hy]))
    have hchoice : x = 0 ∨ x = 1 := by omega
    rcases hchoice with rfl | rfl
    · apply List.mem_append.mpr; left
      exact List.mem_map.mpr ⟨xs, ht, rfl⟩
    · apply List.mem_append.mpr; right
      exact List.mem_map.mpr ⟨xs, ht, rfl⟩

/-- Core list cardinality: distinct members cannot outnumber their cover. -/
theorem nodup_subset_length_le {α : Type} [DecidableEq α]
    (xs ys : List α) (hx : xs.Nodup) (hs : ∀ x ∈ xs, x ∈ ys) :
    xs.length ≤ ys.length := by
  induction xs generalizing ys with
  | nil => simp
  | cons x xs ih =>
    obtain ⟨hxnot, hxs⟩ := List.nodup_cons.mp hx
    have hxy : x ∈ ys := hs x (by simp)
    have hr : xs.length ≤ (ys.erase x).length := by
      apply ih (ys.erase x) hxs
      intro z hz
      apply (List.mem_erase_of_ne (show z ≠ x from by
        intro heq
        subst z
        exact hxnot hz)).2
      exact hs z (by simp [hz])
    have hpositive : 0 < ys.length := by
      cases ys with
      | nil => simp at hxy
      | cons => simp
    rw [List.length_erase_of_mem hxy] at hr
    simp only [List.length_cons]
    omega

/-- Every distinct finite family in the actual canonical overflow fiber
obeys the sharp universal bound, for both even and odd input widths. -/
theorem actual_overflow_fiber_bound (L : Nat) (target : List Nat)
    (qs : List (List Nat)) (hL : 2 ≤ L) (hqs : qs.Nodup)
    (hfiber : ∀ q ∈ qs, ActualOverflowFiber L target q) :
    qs.length ≤ 2 ^ (L / 2 - 1) := by
  have hcodes : (qs.map carryCode).Nodup := by
    apply List.pairwise_map.mpr
    apply List.Pairwise.imp_of_mem (p := hqs)
    intro q r hq hr hne heq
    exact hne (actual_overflow_code_injective L target q r hL
      (hfiber q hq) (hfiber r hr) heq)
  have hcover : ∀ c ∈ qs.map carryCode, c ∈ binaryCodes (L / 2 - 1) := by
    intro c hc
    obtain ⟨q, hq, rfl⟩ := List.mem_map.mp hc
    have hf := hfiber q hq
    have hh := mem_binaryCodes (carryCode q) (carryCode_bound q hf.2.1.2.1)
    simpa only [carryCode_length, hf.1] using hh
  have hb := nodup_subset_length_le (qs.map carryCode)
    (binaryCodes (L / 2 - 1)) hcodes hcover
  simpa only [List.length_map, binaryCodes_length] using hb

/-- Finite universe of coefficient words, retaining all nineteen possible
pair-sum coefficients at each position. -/
def coefficientWords : Nat → List (List Nat)
  | 0 => [[]]
  | n + 1 => (List.range 19).flatMap
      (fun x => (coefficientWords n).map (x :: ·))

theorem coefficientWords_membership (L : Nat) (q : List Nat) :
    q ∈ coefficientWords L ↔ q.length = L ∧ (∀ x ∈ q, x ≤ 18) := by
  induction L generalizing q with
  | zero =>
    cases q <;> simp [coefficientWords]
  | succ n ih =>
    constructor
    · intro hq
      obtain ⟨x, hx, hq⟩ := List.mem_flatMap.mp hq
      obtain ⟨xs, hxs, rfl⟩ := List.mem_map.mp hq
      obtain ⟨hlen, hb⟩ := (ih xs).mp hxs
      refine ⟨by simp [hlen], ?_⟩
      intro y hy
      rcases List.mem_cons.mp hy with rfl | hy
      · have h := List.mem_range.mp hx; omega
      · exact hb y hy
    · intro hq
      cases q with
      | nil => simp at hq
      | cons x xs =>
        have hx : x ≤ 18 := hq.2 x (by simp)
        have hxs : xs ∈ coefficientWords n := (ih xs).mpr
          ⟨by simpa using hq.1, by intro y hy; exact hq.2 y (by simp [hy])⟩
        apply List.mem_flatMap.mpr
        refine ⟨x, List.mem_range.mpr (by omega), ?_⟩
        exact List.mem_map.mpr ⟨xs, hxs, rfl⟩

theorem coefficientWords_nodup (L : Nat) : (coefficientWords L).Nodup := by
  induction L with
  | zero => simp [coefficientWords]
  | succ n ih =>
    apply List.pairwise_flatMap.mpr
    constructor
    · intro x hx
      exact List.Pairwise.map (x :: ·)
        (fun a b hne he => hne (List.cons.inj he).2) ih
    · refine List.Pairwise.imp ?_ List.nodup_range
      intro x y hne a ha b hb
      obtain ⟨xs, hxs, rfl⟩ := List.mem_map.mp ha
      obtain ⟨ys, hys, rfl⟩ := List.mem_map.mp hb
      intro he
      exact hne (List.cons.inj he).1

instance (q : List Nat) : Decidable (Canonical q) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _))

instance (L : Nat) (target q : List Nat) : Decidable (ActualOverflowFiber L target q) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _))

/-- Literal complete canonical coefficient-word fiber of Agent8.stepWord,
with its actual final carry required to be one. -/
def actualOverflowPreimages (L : Nat) (target : List Nat) : List (List Nat) :=
  (coefficientWords L).filter (fun q => decide (ActualOverflowFiber L target q))

theorem actualOverflowPreimages_membership (L : Nat) (target q : List Nat) :
    q ∈ actualOverflowPreimages L target ↔ ActualOverflowFiber L target q := by
  rw [actualOverflowPreimages, List.mem_filter, decide_eq_true_eq]
  constructor
  · exact And.right
  · intro h
    exact ⟨(coefficientWords_membership L q).mpr ⟨h.1, h.2.1.2.1⟩, h⟩

theorem actualOverflowPreimages_nodup (L : Nat) (target : List Nat) :
    (actualOverflowPreimages L target).Nodup :=
  List.Pairwise.filter _ (coefficientWords_nodup L)

/-- Complete actual fiber upper bound for every L≥2, including odd widths
and their required even central coefficient. -/
theorem actualOverflowPreimages_bound (L : Nat) (target : List Nat) (hL : 2 ≤ L) :
    (actualOverflowPreimages L target).length ≤ 2 ^ (L / 2 - 1) := by
  exact actual_overflow_fiber_bound L target (actualOverflowPreimages L target)
    hL (actualOverflowPreimages_nodup L target)
    (fun q hq => (actualOverflowPreimages_membership L target q).mp hq)

#print axioms carryCode_length
#print axioms carryCode_get
#print axioms carryCode_bound
#print axioms carryCode_eq_carry
#print axioms canonical_coefficient_bound
#print axioms overflow_outer_ge_nine
#print axioms actual_overflow_prefix_unique
#print axioms actual_overflow_code_injective
#print axioms binaryCodes_length
#print axioms mem_binaryCodes
#print axioms nodup_subset_length_le
#print axioms actual_overflow_fiber_bound
#print axioms coefficientWords_membership
#print axioms coefficientWords_nodup
#print axioms actualOverflowPreimages_membership
#print axioms actualOverflowPreimages_nodup
#print axioms actualOverflowPreimages_bound

end P196.Agent2.OverflowFibers
