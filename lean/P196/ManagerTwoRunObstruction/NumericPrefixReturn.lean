import P196.Agent2SaturatedProfile.WholeWordBridge
import P196.Agent104P620Witness.PalindromeBridge

/-!
Numeric consequences of returning the first three decimal pair columns.
The actual reverse-and-add semantics and the finite prefix certificate are
imported unchanged. No return, cycle, or Lychrel number is constructed.
-/

namespace P196.ManagerTwoRun

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open P196.Agent4.Saturation P196.Agent4.WholeWord

/-- An actual returned prefix obeys the finite certificate's width bound. -/
theorem actual_prefix_return_width_bound (q : Nat → Nat) (L P : Nat)
    (ha : Admissible L q) (hL : 3 ≤ L)
    (hreturn : prefix3 (iterPairs q L P).2 = prefix3 q) :
    2 * (iterPairs q L P).1 ≤ 2 * L + P := by
  let s := fun i => prefix3 (iterPairs q L i).2
  let e := fun i => carry (iterPairs q L i).2 ((iterPairs q L i).1 - 3)
  have hv : ∀ i < P, Valid (s i) := by
    intro i hi
    have had := CarryHistory.iterPairs_admissible q L i ha
    have hw := iterPairs_width_ge q L i
    exact ⟨had.2.1, had.2.2.1 0 (by omega), had.2.2.1 1 (by omega),
      had.2.2.1 2 (by omega)⟩
  have he : ∀ i < P, e i ≤ 1 := by
    intro i hi
    have had := CarryHistory.iterPairs_admissible q L i ha
    exact carry_bounded (iterPairs q L i).2 (iterPairs q L i).1
      had.2.2.1 ((iterPairs q L i).1 - 3) (by omega)
  have hs : ∀ i < P, (advance (s i) (e i)).1 = s (i + 1) := by
    intro i hi
    exact congrArg Prod.fst (iterPairs_prefix_evolution q L i ha hL)
  have hg : (fun i => (advance (s i) (e i)).2) = overflowAt q L := by
    funext i
    exact congrArg Prod.snd (iterPairs_prefix_evolution q L i ha hL)
  have hclose : s P = s 0 := by simpa [s, iterPairs] using hreturn
  have hb := (closed_prefix_overflow_bounds s e P hv he hs hclose).1
  rw [hg] at hb
  have hw := actual_width_overflow_identity q L P ha
  omega

/-- Canonical uniqueness also identifies every available pair-prefix column.
Trailing zero digits are permitted by `Canonical`. -/
theorem canonical_prefix_unique {n : Nat} {d e : Nat → Nat} {L W : Nat}
    (hd : Canonical n d L) (he : Canonical n e W) (hL : 3 ≤ L) :
    L = W ∧ prefix3 (columnSum d L) = prefix3 (columnSum e W) := by
  obtain ⟨hwidth, hdigit⟩ := SevenColumnKernel.PalindromeBridge.canonical_unique hd he
  refine ⟨hwidth, ?_⟩
  subst W
  have hp (i : Nat) (hi : i < 3) : columnSum d L i = columnSum e L i := by
    unfold columnSum reflected
    rw [hdigit i (by omega), hdigit (L - 1 - i) (by omega)]
  unfold prefix3
  rw [hp 0 (by decide), hp 1 (by decide), hp 2 (by decide)]

/-- Any specified canonical target of an actual orbit has the same width and
pair prefix as the canonical representation supplied by the dynamics theorem. -/
theorem numeric_prefix_return_constraints
    (n : Nat) (d e : Nat → Nat) (L W P : Nat)
    (hsource : Canonical n d L)
    (htarget : Canonical (Lychrel196.orbit n P) e W)
    (hL : 3 ≤ L)
    (hreturn : prefix3 (columnSum e W) = prefix3 (columnSum d L)) :
    2 * W ≤ 2 * L + P ∧ (2 * W = 2 * L + P → P % 8 = 0) := by
  let q := columnSum d L
  have ha := NormalizationBridge.canonical_admissible n d L hsource
  obtain ⟨f, hf, hr⟩ := iterPairs_representation n d q L P hsource (fun _ _ => rfl)
  have hge := iterPairs_width_ge q L P
  obtain ⟨hwidth, hpref⟩ := canonical_prefix_unique hf htarget (by omega)
  have hrp : prefix3 (columnSum f (iterPairs q L P).1) =
      prefix3 (iterPairs q L P).2 := by
    unfold prefix3
    rw [hr 0 (by omega), hr 1 (by omega), hr 2 (by omega)]
  have hactual : prefix3 (iterPairs q L P).2 = prefix3 q := by
    rw [← hrp, hpref]
    exact hreturn
  constructor
  · have hb := actual_prefix_return_width_bound q L P ha hL hactual
    omega
  · intro hsat
    apply actual_saturated_prefix_return q L P ha hL hactual
    omega

#print axioms actual_prefix_return_width_bound
#print axioms canonical_prefix_unique
#print axioms numeric_prefix_return_constraints

end P196.ManagerTwoRun
