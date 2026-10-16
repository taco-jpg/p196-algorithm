import Agent15FourthColumn

/-! Agent #418: cross-block carry restriction for the saturated eight-state
skeleton. Uses the unchanged Agent15 fourth-column step, not a new model.
The ordinary-integer specialization is in a separate module. -/
namespace Agent418.CarrySuppression
open P196.Agent4.Saturation Agent15.FourthColumn
set_option maxRecDepth 10000
set_option maxHeartbeats 4000000

def windowPrefix : Nat → Prefix
  | 0 => ⟨17,8,17⟩
  | 1 => ⟨8,16,16⟩
  | 2 => ⟨17,13,14⟩
  | 3 => ⟨8,12,9⟩
  | _ => ⟨17,5,0⟩

def walk (s : Quad) (es : List Nat) : Quad :=
  es.foldl (fun q e => (step q e).1) s

def windowMatches (d e0 e1 e2 e3 : Nat) : Prop :=
  (walk ⟨windowPrefix 0,d⟩ [e0]).p = windowPrefix 1 ∧
  (walk ⟨windowPrefix 0,d⟩ [e0,e1]).p = windowPrefix 2 ∧
  (walk ⟨windowPrefix 0,d⟩ [e0,e1,e2]).p = windowPrefix 3 ∧
  (walk ⟨windowPrefix 0,d⟩ [e0,e1,e2,e3]).p = windowPrefix 4

instance (d e0 e1 e2 e3 : Nat) : Decidable (windowMatches d e0 e1 e2 e3) := by
  unfold windowMatches
  infer_instance

/-- Exhaustive kernel reduction over 19 * 2^4 local boundary choices. -/
theorem four_step_bound_finite : ∀ d : Fin 19, ∀ e0 e1 e2 e3 : Fin 2,
    windowMatches d.val e0.val e1.val e2.val e3.val →
    (walk ⟨windowPrefix 0,d.val⟩ [e0.val,e1.val,e2.val,e3.val]).d ≤ 8 := by
  decide +kernel

theorem four_step_bound (d e0 e1 e2 e3 : Nat)
    (hd : d ≤ 18) (h0 : e0 ≤ 1) (h1 : e1 ≤ 1)
    (h2 : e2 ≤ 1) (h3 : e3 ≤ 1)
    (hm : windowMatches d e0 e1 e2 e3) :
    (walk ⟨windowPrefix 0,d⟩ [e0,e1,e2,e3]).d ≤ 8 :=
  four_step_bound_finite ⟨d,by omega⟩ ⟨e0,by omega⟩ ⟨e1,by omega⟩
    ⟨e2,by omega⟩ ⟨e3,by omega⟩ hm

/-- Every bounded fourth-column lift of the window has a forced zero next
three-column input, independently of the next hidden bit. -/
theorem four_step_carry_zero (d e0 e1 e2 e3 e4 : Nat)
    (hd : d ≤ 18) (h0 : e0 ≤ 1) (h1 : e1 ≤ 1)
    (h2 : e2 ≤ 1) (h3 : e3 ≤ 1) (h4 : e4 ≤ 1)
    (hm : windowMatches d e0 e1 e2 e3) :
    innerCarry (walk ⟨windowPrefix 0,d⟩ [e0,e1,e2,e3]) e4 = 0 := by
  have hb := four_step_bound d e0 e1 e2 e3 hd h0 h1 h2 h3 hm
  unfold innerCarry
  omega

/-- Sequence interface: the transitions and prefix observations imply the
bound. No saturation-count or input-balance premise is required. -/
theorem path_bound (s : Nat → Quad) (e : Nat → Nat)
    (hd : (s 0).d ≤ 18)
    (he : ∀ i < 4, e i ≤ 1)
    (hs : ∀ i < 4, (step (s i) (e i)).1 = s (i+1))
    (hp : ∀ i ≤ 4, (s i).p = windowPrefix i) :
    (s 4).d ≤ 8 := by
  have hinit : s 0 = ⟨windowPrefix 0,(s 0).d⟩ := by
    calc s 0 = ⟨(s 0).p,(s 0).d⟩ := rfl
         _ = ⟨windowPrefix 0,(s 0).d⟩ := by rw [hp 0 (by decide)]
  have h0 := hs 0 (by decide)
  have h1 := hs 1 (by decide)
  have h2 := hs 2 (by decide)
  have h3 := hs 3 (by decide)
  have hm : windowMatches (s 0).d (e 0) (e 1) (e 2) (e 3) := by
    unfold windowMatches
    rw [← hinit]
    simp only [walk, List.foldl_cons, List.foldl_nil]
    rw [h0, h1, h2, h3]
    exact ⟨hp 1 (by decide), hp 2 (by decide), hp 3 (by decide), hp 4 (by decide)⟩
  have hb := four_step_bound (s 0).d (e 0) (e 1) (e 2) (e 3) hd
    (he 0 (by decide)) (he 1 (by decide)) (he 2 (by decide)) (he 3 (by decide)) hm
  rw [← hinit] at hb
  simp only [walk, List.foldl_cons, List.foldl_nil] at hb
  rw [h0, h1, h2, h3] at hb
  exact hb

#print axioms four_step_bound_finite
#print axioms four_step_bound
#print axioms four_step_carry_zero
#print axioms path_bound
end Agent418.CarrySuppression
