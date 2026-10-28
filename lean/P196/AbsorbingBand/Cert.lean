import P196.AbsorbingBand.Step
import P196.Drafts.Agent120NeutralBandCalibration.A120Certificate

/-!
# Certificates for absorbing-band templates

An edge records `(B, c) → (B2, c2)` and the number `u` of band-valued coefficients moved from the
end of the next block into the band.  `ledgeOK` checks one edge by evaluating the exact transition
of `Step.lean`; `lcycleOK` checks a closed cycle of edges whose band length never decreases.
`lychrel_of_lcycle`: a checked cycle certifies, for every initial band length `l ≥ minL`, the value of
the template as a Lychrel number for the ordinary base-`b` reverse-and-add map.

Band-length bookkeeping: an edge with overflow `gam` sends the band length `l` to
`l + gam + 2u - 2` and needs `2 ≤ l + gam`.
-/

namespace AbsorbingBand

open Agent120.Neutral

/-- One transition of interface states. -/
structure LEdge where
  B : List Nat
  c : Nat
  B2 : List Nat
  c2 : Nat
  u : Nat
  deriving DecidableEq, Repr

/-- Executable check of one edge. -/
def ledgeOK (b : Nat) (E : LEdge) : Bool :=
  decide (2 ≤ b) && decide (E.B ≠ []) && decide (E.B.head? ≠ some 0) &&
    E.B.all (fun v => decide (v ≤ 2 * (b - 1))) && decide (E.c ≤ 2 * (b - 1)) &&
    decide (E.c ≠ b - 1) && decide (Lw b E.B E.c ≠ (Rw b E.B E.c).reverse) &&
    decide (nextBa b E.B E.c = E.B2 ++ List.replicate E.u E.c2) &&
    decide (E.c2 = cnext b E.c)

theorem ledgeOK_sound {b : Nat} {E : LEdge} (h : ledgeOK b E = true) :
    LHyp b E.B E.c ∧ Lw b E.B E.c ≠ (Rw b E.B E.c).reverse ∧
      nextBa b E.B E.c = E.B2 ++ List.replicate E.u E.c2 ∧ E.c2 = cnext b E.c := by
  simp only [ledgeOK, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true] at h
  obtain ⟨⟨⟨⟨⟨⟨⟨⟨hb, hne⟩, hext⟩, hB⟩, hc⟩, hcne⟩, hnp⟩, hnB⟩, hc2⟩ := h
  exact ⟨⟨hb, hB, hc, hcne, hne, hext⟩, hnp, hnB, hc2⟩

/-- Overflow of an edge. -/
def lgam (b : Nat) (E : LEdge) : Nat := gama b E.B E.c

/-- One checked edge: exact step and palindrome freedom, for every band length with `2 ≤ l + gam`. -/
theorem ledge_step {b : Nat} {E : LEdge} (h : ledgeOK b E = true) (l : Nat)
    (hl : 2 ≤ l + lgam b E) :
    ¬ IsPal b (val b (ltmpl E.B E.c l)) ∧
      step b (val b (ltmpl E.B E.c l)) =
        val b (ltmpl E.B2 E.c2 (l + lgam b E + 2 * E.u - 2)) := by
  obtain ⟨hyp, hnp, hnB, hc2⟩ := ledgeOK_sound h
  refine ⟨not_isPal_ltmpl hyp l hl hnp, ?_⟩
  rw [step_ltmpl hyp l hl]
  have key : ltmpl (nextBa b E.B E.c) (cnext b E.c) (l + gama b E.B E.c - 2) =
      ltmpl E.B2 E.c2 (l + lgam b E + 2 * E.u - 2) := by
    rw [hnB, ← hc2, ltmpl_trim]
    have hl' : 2 ≤ l + gama b E.B E.c := hl
    have : E.u + (l + gama b E.B E.c - 2) + E.u = l + lgam b E + 2 * E.u - 2 := by
      unfold lgam; omega
    rw [this]
  rw [key]

/-- Chained edges starting at a given interface. -/
def lchainOK (b : Nat) : List LEdge → List Nat → Nat → Bool
  | [], _, _ => true
  | e :: es, B, c => decide (e.B = B) && decide (e.c = c) && ledgeOK b e && lchainOK b es e.B2 e.c2

/-- Final interface of a chain. -/
def endBL : List LEdge → List Nat → List Nat
  | [], B => B
  | e :: es, _ => endBL es e.B2

def endcL : List LEdge → Nat → Nat
  | [], c => c
  | e :: es, _ => endcL es e.c2

/-- Total overflow along a chain. -/
def sumGamL (b : Nat) : List LEdge → Nat
  | [] => 0
  | e :: es => lgam b e + sumGamL b es

/-- Total number of band-valued coefficients moved into the band along a chain. -/
def sumU : List LEdge → Nat
  | [] => 0
  | e :: es => e.u + sumU es

/-- Band length after running a chain. -/
def lend (b : Nat) : List LEdge → Nat → Nat
  | [], l => l
  | e :: es, l => lend b es (l + lgam b e + 2 * e.u - 2)

/-- Smallest starting band length for which the chain is runnable at every edge. -/
def minL (b : Nat) : List LEdge → Nat
  | [] => 0
  | e :: es => max (2 - lgam b e) (minL b es + 2 - (lgam b e + 2 * e.u))

theorem lend_spec (b : Nat) :
    ∀ (es : List LEdge) (l : Nat), minL b es ≤ l →
      lend b es l + 2 * es.length = l + sumGamL b es + 2 * sumU es
  | [], l, _ => by simp [lend, sumGamL, sumU]
  | e :: es, l, hl => by
      simp only [minL] at hl
      have h1 : 2 ≤ l + lgam b e := by omega
      have h2 : minL b es ≤ l + lgam b e + 2 * e.u - 2 := by omega
      have ih := lend_spec b es _ h2
      simp only [lend, sumGamL, sumU, List.length_cons]
      omega

/-- Running a checked chain: palindrome freedom and the exact final template. -/
theorem lchain_run (b : Nat) :
    ∀ (es : List LEdge) (B : List Nat) (c l : Nat), lchainOK b es B c = true → minL b es ≤ l →
      (∀ k, k < es.length → ¬ IsPal b (orbit b (val b (ltmpl B c l)) k)) ∧
      orbit b (val b (ltmpl B c l)) es.length =
        val b (ltmpl (endBL es B) (endcL es c) (lend b es l))
  | [], B, c, l, _, _ => by
      refine ⟨fun k hk => by simp at hk, ?_⟩
      simp [orbit, endBL, endcL, lend]
  | e :: es, B, c, l, hc, hl => by
      simp only [lchainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨hB, hc'⟩, he⟩, hes⟩ := hc
      subst hB; subst hc'
      simp only [minL] at hl
      have h1 : 2 ≤ l + lgam b e := by omega
      have h2 : minL b es ≤ l + lgam b e + 2 * e.u - 2 := by omega
      obtain ⟨hnp, hstep⟩ := ledge_step he l h1
      obtain ⟨ihp, ihe⟩ := lchain_run b es e.B2 e.c2 _ hes h2
      refine ⟨?_, ?_⟩
      · intro k hk
        cases k with
        | zero => simpa [orbit] using hnp
        | succ k =>
            have hk' : k < es.length := by simpa using hk
            have := ihp k hk'
            rwa [show k + 1 = 1 + k by omega, orbit_add,
              show orbit b (val b (ltmpl e.B e.c l)) 1 = step b (val b (ltmpl e.B e.c l)) from rfl,
              hstep]
      · have hlen : (e :: es).length = 1 + es.length := by simp <;> omega
        rw [hlen, orbit_add,
          show orbit b (val b (ltmpl e.B e.c l)) 1 = step b (val b (ltmpl e.B e.c l)) from rfl,
          hstep, ihe]
        simp only [endBL, endcL, lend]

/-- Executable check of a cycle certificate based at `(B, c)`. -/
def lcycleOK (b : Nat) (es : List LEdge) (B : List Nat) (c : Nat) : Bool :=
  decide (es ≠ []) && lchainOK b es B c && decide (endBL es B = B) && decide (endcL es c = c) &&
    decide (2 * es.length ≤ sumGamL b es + 2 * sumU es)

/-- A checked cycle certifies the template value for every band length `l ≥ minL`. -/
theorem lychrel_of_lcycle (b : Nat) (es : List LEdge) (B : List Nat) (c : Nat)
    (hcert : lcycleOK b es B c = true) (l : Nat) (hl : minL b es ≤ l) :
    Lychrel b (val b (ltmpl B c l)) := by
  simp only [lcycleOK, Bool.and_eq_true, decide_eq_true_eq] at hcert
  obtain ⟨⟨⟨⟨hne, hch⟩, hB⟩, hC⟩, hgain⟩ := hcert
  have hlen : 0 < es.length := List.length_pos_iff.mpr hne
  have rounds : ∀ n : Nat, ∃ G, l ≤ G ∧
      orbit b (val b (ltmpl B c l)) (n * es.length) = val b (ltmpl B c G) := by
    intro n
    induction n with
    | zero => exact ⟨l, Nat.le_refl l, by simp [orbit]⟩
    | succ n ih =>
        obtain ⟨G, hG, hEq⟩ := ih
        have hGm : minL b es ≤ G := by omega
        obtain ⟨_, hrun⟩ := lchain_run b es B c G hch hGm
        have hsp := lend_spec b es G hGm
        refine ⟨lend b es G, by omega, ?_⟩
        rw [Nat.succ_mul, orbit_add, hEq, hrun, hB, hC]
  intro t
  have hdiv := Nat.div_add_mod t es.length
  obtain ⟨G, hG, hEq⟩ := rounds (t / es.length)
  have hr : t % es.length < es.length := Nat.mod_lt _ hlen
  obtain ⟨hnp, _⟩ := lchain_run b es B c G hch (by omega)
  have := hnp (t % es.length) hr
  rw [← hdiv, Nat.mul_comm, orbit_add, hEq]
  exact this

end AbsorbingBand

#print axioms AbsorbingBand.ledge_step
#print axioms AbsorbingBand.lchain_run
#print axioms AbsorbingBand.lychrel_of_lcycle
