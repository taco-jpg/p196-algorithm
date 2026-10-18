import P196.Drafts.Agent120NeutralBandCalibration.A120Template

/-!
# Agent #120: certificate soundness for neutral one-band templates

A certificate is a finite cyclic list of interface transitions. Each edge
records a source interface `(B, C)`, a target interface `(B2, C2)` and the
numbers `u, v` of neutral coefficients moved from the next exterior and the
next center into the band. `edgeOK` checks one edge by evaluating the exact
transition of `A120Template` (no search, no trusted data).

`lychrel_of_cycle`: if a nonempty cycle of checked edges has total moved
neutral coefficients at least its total number of overflows, then for every
initial gap `g ≥ 2 + (number of overflows in one cycle)` the value of the
template word has a palindrome-free ordinary base-`b` reverse-and-add orbit.

This is a conditional existence theorem for every base. Instances live in
separate modules. Nothing here concerns base ten or 196.
-/

namespace Agent120.Neutral

/-- One transition of interface states. -/
structure Edge where
  B : List Nat
  C : List Nat
  B2 : List Nat
  C2 : List Nat
  u : Nat
  v : Nat
  deriving DecidableEq, Repr

/-- Executable check of one edge. -/
def edgeOK (b : Nat) (E : Edge) : Bool :=
  decide (2 ≤ b) && E.B.all (fun v => decide (v ≤ 2 * (b - 1))) &&
    E.C.all (fun v => decide (v ≤ 2 * (b - 1))) && decide (E.B.head? ≠ some 0) &&
    decide (e1 b E.B ≠ e2 b E.B E.C) &&
    decide (nextB b E.B E.C = E.B2 ++ List.replicate E.u (b - 1)) &&
    decide (nextC b E.B E.C = List.replicate E.v (b - 1) ++ (E.C2 ++ List.replicate E.v (b - 1)))

theorem edgeOK_sound {b : Nat} {E : Edge} (h : edgeOK b E = true) :
    Hyp b E.B E.C ∧ nextB b E.B E.C = E.B2 ++ List.replicate E.u (b - 1) ∧
      nextC b E.B E.C = List.replicate E.v (b - 1) ++ (E.C2 ++ List.replicate E.v (b - 1)) := by
  simp only [edgeOK, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true] at h
  obtain ⟨⟨⟨⟨⟨⟨hb, hB⟩, hC⟩, hext⟩, hflip⟩, hnB⟩, hnC⟩ := h
  exact ⟨⟨hb, hB, hC, hext, hflip⟩, hnB, hnC⟩

/-- Moving neutral coefficients from the interfaces into the band. -/
theorem tmpl_trim (b : Nat) (B2 C2 : List Nat) (u v g : Nat) :
    tmpl b (B2 ++ List.replicate u (b - 1))
        (List.replicate v (b - 1) ++ (C2 ++ List.replicate v (b - 1))) g =
      tmpl b B2 C2 (g + u + v) := by
  unfold tmpl
  simp only [List.reverse_append, List.reverse_replicate, List.append_assoc]
  rw [← List.append_assoc (List.replicate u (b - 1)) (List.replicate g (b - 1)),
    List.replicate_append_replicate,
    ← List.append_assoc (List.replicate (u + g) (b - 1)) (List.replicate v (b - 1)),
    List.replicate_append_replicate,
    ← List.append_assoc (List.replicate v (b - 1)) (List.replicate g (b - 1)),
    List.replicate_append_replicate,
    ← List.append_assoc (List.replicate (v + g) (b - 1)) (List.replicate u (b - 1)),
    List.replicate_append_replicate]
  have h1 : u + g + v = g + u + v := by omega
  have h2 : v + g + u = g + u + v := by omega
  rw [h1, h2]

/-- One checked edge: exact step and palindrome freedom. -/
theorem edge_step {b : Nat} {E : Edge} (h : edgeOK b E = true) (g : Nat) (hg : 2 ≤ g) :
    ¬ IsPal b (val b (tmpl b E.B E.C g)) ∧
      step b (val b (tmpl b E.B E.C g)) =
        val b (tmpl b E.B2 E.C2 (g - gam b E.B E.C + E.u + E.v)) := by
  obtain ⟨hyp, hnB, hnC⟩ := edgeOK_sound h
  refine ⟨not_isPal_tmpl hyp g hg, ?_⟩
  rw [step_tmpl hyp g (by omega), hnB, hnC, tmpl_trim]

/-- Chained edges starting at a given interface. -/
def chainOK (b : Nat) : List Edge → List Nat → List Nat → Bool
  | [], _, _ => true
  | e :: es, B, C => decide (e.B = B) && decide (e.C = C) && edgeOK b e && chainOK b es e.B2 e.C2

/-- Final interface of a chain. -/
def endB : List Edge → List Nat → List Nat
  | [], B => B
  | e :: es, _ => endB es e.B2

def endC : List Edge → List Nat → List Nat
  | [], C => C
  | e :: es, _ => endC es e.C2

/-- Total number of overflows along a chain. -/
def sumGam (b : Nat) : List Edge → Nat
  | [] => 0
  | e :: es => gam b e.B e.C + sumGam b es

/-- Total number of neutral coefficients moved into the band along a chain. -/
def sumGain : List Edge → Nat
  | [] => 0
  | e :: es => e.u + e.v + sumGain es

/-- Running a checked chain: palindrome freedom and the exact final template. -/
theorem chain_run (b : Nat) :
    ∀ (es : List Edge) (B C : List Nat) (g : Nat), chainOK b es B C = true →
      2 + sumGam b es ≤ g →
        (∀ k, k < es.length → ¬ IsPal b (orbit b (val b (tmpl b B C g)) k)) ∧
        orbit b (val b (tmpl b B C g)) es.length =
          val b (tmpl b (endB es B) (endC es C) (g + sumGain es - sumGam b es))
  | [], B, C, g, _, _ => by
      refine ⟨fun k hk => by simp at hk, ?_⟩
      simp [orbit, endB, endC, sumGain, sumGam]
  | e :: es, B, C, g, hc, hg => by
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨hB, hC⟩, he⟩, hes⟩ := hc
      subst hB; subst hC
      simp only [sumGam] at hg
      obtain ⟨hnp, hstep⟩ := edge_step he g (by omega)
      have hg' : 2 + sumGam b es ≤ g - gam b e.B e.C + e.u + e.v := by omega
      obtain ⟨ihp, ihe⟩ := chain_run b es e.B2 e.C2 _ hes hg'
      refine ⟨?_, ?_⟩
      · intro k hk
        cases k with
        | zero => simpa [orbit] using hnp
        | succ k =>
            have hk' : k < es.length := by simpa using hk
            have := ihp k hk'
            rwa [show k + 1 = 1 + k by omega, orbit_add, show orbit b (val b (tmpl b e.B e.C g)) 1 =
              step b (val b (tmpl b e.B e.C g)) from rfl, hstep]
      · have hlen : (e :: es).length = 1 + es.length := by simp; omega
        rw [hlen, orbit_add, show orbit b (val b (tmpl b e.B e.C g)) 1 =
          step b (val b (tmpl b e.B e.C g)) from rfl, hstep, ihe]
        simp only [endB, endC, sumGain, sumGam]
        congr 2
        omega

/-- Executable check of a cycle certificate based at `(B, C)`. -/
def cycleOK (b : Nat) (es : List Edge) (B C : List Nat) : Bool :=
  decide (es ≠ []) && chainOK b es B C && decide (endB es B = B) && decide (endC es C = C) &&
    decide (sumGam b es ≤ sumGain es)

/-- Conditional existence in base `b`: a checked cycle certificate gives a base-`b` integer
whose ordinary reverse-and-add orbit never reaches a palindrome. -/
theorem lychrel_of_cycle (b : Nat) (es : List Edge) (B C : List Nat)
    (hcert : cycleOK b es B C = true) (g : Nat) (hg : 2 + sumGam b es ≤ g) :
    Lychrel b (val b (tmpl b B C g)) := by
  simp only [cycleOK, Bool.and_eq_true, decide_eq_true_eq] at hcert
  obtain ⟨⟨⟨⟨hne, hch⟩, hB⟩, hC⟩, hgain⟩ := hcert
  have hlen : 0 < es.length := List.length_pos_iff.mpr hne
  -- after n full cycles the state is back at (B, C) with gap at least g
  have rounds : ∀ n : Nat, ∃ G, g ≤ G ∧
      orbit b (val b (tmpl b B C g)) (n * es.length) = val b (tmpl b B C G) := by
    intro n
    induction n with
    | zero => exact ⟨g, Nat.le_refl g, by simp [orbit]⟩
    | succ n ih =>
        obtain ⟨G, hG, hEq⟩ := ih
        obtain ⟨_, hrun⟩ := chain_run b es B C G hch (by omega)
        refine ⟨G + sumGain es - sumGam b es, by omega, ?_⟩
        rw [Nat.succ_mul, orbit_add, hEq, hrun, hB, hC]
  intro t
  -- write t = n * p + r with r < p
  have hdiv := Nat.div_add_mod t es.length
  obtain ⟨G, hG, hEq⟩ := rounds (t / es.length)
  have hr : t % es.length < es.length := Nat.mod_lt _ hlen
  obtain ⟨hnp, _⟩ := chain_run b es B C G hch (by omega)
  have := hnp (t % es.length) hr
  rw [← hdiv, Nat.mul_comm, orbit_add, hEq]
  exact this

/-- Safe finite entry into a certified template certifies the original seed. -/
theorem lychrel_of_entry (b N t M : Nat) (hprefix : ∀ k, k < t → ¬ IsPal b (orbit b N k))
    (hentry : orbit b N t = M) (hM : Lychrel b M) : Lychrel b N := by
  intro k
  by_cases hk : k < t
  · exact hprefix k hk
  · have := hM (k - t)
    rw [← hentry, ← orbit_add, show t + (k - t) = k by omega] at this
    exact this

end Agent120.Neutral

#print axioms Agent120.Neutral.edge_step
#print axioms Agent120.Neutral.chain_run
#print axioms Agent120.Neutral.lychrel_of_cycle
#print axioms Agent120.Neutral.lychrel_of_entry
