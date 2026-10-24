import P196.Agent2SaturatedProfile.ReturnCertificate

/-!
Exact two-sided reframing for the complementary-band template.
Both sides use natural padding, so no truncated subtraction occurs.
This is a local equality and a representational extension, not a return cycle.
-/
namespace Agent218.CertificateAudit

open Agent109 Agent109.Cert

/-- Common padding permits band letters to move into or out of finite blocks.
The four old padding counts and four new padding counts are independent. -/
theorem template_reframe
    (c : Nat) (B A C B' A' C' : Word)
    (r r1 r2 rk j j1 j2 k u v : Nat)
    (hB : B ++ List.replicate r c = B' ++ List.replicate j c)
    (hA : List.replicate r1 c ++ A ++ List.replicate r2 (18 - c) =
      List.replicate j1 c ++ A' ++ List.replicate j2 (18 - c))
    (hC : List.replicate rk (18 - c) ++ C ++ List.replicate rk (18 - c) =
      List.replicate k (18 - c) ++ C' ++ List.replicate k (18 - c)) :
    template c B A C (u + r + r1) (v + r2 + rk) =
      template c B' A' C' (u + j + j1) (v + j2 + k) := by
  rw [← template_trim c B A C r r1 r2 rk u v,
    ← template_trim c B' A' C' j j1 j2 k u v]
  rw [hB, hA, hC]

/-- An exact actual-word step followed by common-padding reframing.
The equations for the intermediate lengths are explicit guards. -/
theorem stepWord_template_reframe
    (c : Nat) (B A C B' A' C' : Word)
    (g h r r1 r2 rk j j1 j2 k u v : Nat)
    (hc : Phase c) (hB : Bounded B) (hA : Bounded A) (hC : Bounded C)
    (hBr : Br c B A C ++ List.replicate r (tOf c + tOf c) =
      B' ++ List.replicate j (tOf c + tOf c))
    (hAr : List.replicate r1 (tOf c + tOf c) ++ Ar c B A C ++
        List.replicate r2 (18 - (tOf c + tOf c)) =
      List.replicate j1 (tOf c + tOf c) ++ A' ++
        List.replicate j2 (18 - (tOf c + tOf c)))
    (hCr : List.replicate rk (18 - (tOf c + tOf c)) ++ Cr c B A C ++
        List.replicate rk (18 - (tOf c + tOf c)) =
      List.replicate k (18 - (tOf c + tOf c)) ++ C' ++
        List.replicate k (18 - (tOf c + tOf c)))
    (hg : g + (data c B A C).γ = u + r + r1)
    (hh : h + (data c B A C).γ = v + r2 + rk) :
    stepWord (template c B A C (g + 2) (h + 2)) =
      template (tOf c + tOf c) B' A' C' (u + j + j1) (v + j2 + k) := by
  rw [stepWord_template c B A C g h hc hB hA hC, hg, hh]
  exact template_reframe _ _ _ _ _ _ _ r r1 r2 rk j j1 j2 k u v hBr hAr hCr

/-- A finite actual local step which one-sided suffix trimming cannot encode
using these exact source and target representatives. -/
theorem reframe_witness (g h : Nat) :
    stepWord (template 2 [] [] [] (g + 3) (h + 2)) =
      template 4 [4, 4] [5, 13] [14, 14] g h := by
  have hs := stepWord_template 2 [] [] [] (g + 1) h
    (by decide) (by simp [Bounded]) (by simp [Bounded]) (by simp [Bounded])
  have hr : template 4 [4] [5, 13] [14, 14] (g + 1) h =
      template 4 [4, 4] [5, 13] [14, 14] g h := by
    exact template_reframe 4 [4] [5, 13] [14, 14] [4, 4] [5, 13] [14, 14]
      1 0 0 0 0 0 0 0 g h (by decide) (by decide) (by decide)
  have he : tOf 2 + tOf 2 = 4 := by decide
  have hb : Br 2 [] [] [] = [4] := by decide
  have ha : Ar 2 [] [] [] = [5, 13] := by decide
  have hc : Cr 2 [] [] [] = [14, 14] := by decide
  have hz : (data 2 [] [] []).γ = 0 := by decide
  rw [he, hb, ha, hc, hz] at hs
  simpa only [Nat.add_zero, Nat.add_assoc] using hs.trans hr

/-- The old direction of trimming cannot add a letter to this raw block. -/
theorem reframe_witness_no_old_trim (j : Nat) :
    Br 2 [] [] [] ≠ [4, 4] ++ List.replicate j 4 := by
  intro h
  have hl := congrArg List.length h
  have hb : Br 2 [] [] [] = [4] := by decide
  rw [hb] at hl
  simp only [List.length_append, List.length_replicate, List.length_cons,
    List.length_nil] at hl
  omega

#print axioms template_reframe
#print axioms stepWord_template_reframe
#print axioms reframe_witness
#print axioms reframe_witness_no_old_trim

end Agent218.CertificateAudit
