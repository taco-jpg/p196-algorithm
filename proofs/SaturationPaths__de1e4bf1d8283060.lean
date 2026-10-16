import SaturationCertificate
import PrefixSemantics

namespace Agent8.Saturation

theorem edge_certificate (q : Triple) (e : Nat) (hv : valid q) (he : e ≤ 1) :
    Certificate q e := by
  rcases q with ⟨p,a,b⟩
  simp only [valid, Prod.fst, Prod.snd] at hv
  rcases hv with ⟨hp,hp18,ha,hb⟩
  have hh := finite_certificate ⟨p-1, by omega⟩ ⟨a, by omega⟩ ⟨b, by omega⟩ ⟨e, by omega⟩
  have hp' : p-1+1=p := by omega
  simpa only [hp'] using hh

theorem total_congr (f g : Nat → Int) (n : Nat)
    (h : ∀ i, i < n → f i = g i) : total f n = total g n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [total]
    rw [ih (by intro i hi; exact h i (by omega)), h n (by omega)]

theorem total_nonneg (f : Nat → Int) (n : Nat)
    (h : ∀ i, i < n → 0 ≤ f i) : 0 ≤ total f n := by
  induction n with
  | zero => simp [total]
  | succ n ih =>
    have ha := ih (by intro i hi; exact h i (by omega))
    have hb := h n (by omega)
    simp only [total]
    omega

theorem zero_total_each_zero (f : Nat → Int) (n : Nat)
    (h : ∀ i, i < n → 0 ≤ f i) (hz : total f n = 0) :
    ∀ i, i < n → f i = 0 := by
  induction n with
  | zero => intro i hi; omega
  | succ n ih =>
    have hprev : ∀ i, i < n → 0 ≤ f i := by intro i hi; exact h i (by omega)
    have ht := total_nonneg f n hprev
    have hn := h n (by omega)
    simp only [total] at hz
    have ht0 : total f n=0 := by omega
    have hn0 : f n=0 := by omega
    intro i hi
    by_cases hi' : i<n
    · exact ih hprev ht0 i hi'
    · have : i=n := by omega
      simpa only [this] using hn0

theorem slack_telescope (q : Nat → Triple) (e : Nat → Nat) (n : Nat)
    (evolves : ∀ i, i<n → q (i+1)=next (q i) (e i)) :
    total (fun i => slack (q i) (e i)) n =
      (n : Int)+upperPotential (q 0).1-upperPotential (q n).1-
        2*total (fun i => (overflow3 (q i) (e i) : Int)) n := by
  induction n with
  | zero => simp [total]
  | succ n ih =>
    have hh := ih (by intro i hi; exact evolves i (by omega))
    have heq := evolves n (by omega)
    simp only [total]
    rw [hh]
    simp only [slack]
    rw [← heq]
    omega

theorem rank_telescope (q : Nat → Triple) (n : Nat) :
    total (fun i => (rank (q i) : Int)-(rank (q (i+1)) : Int)) n =
      (rank (q 0) : Int)-(rank (q n) : Int) := by
  induction n with
  | zero => simp [total]
  | succ n ih => simp only [total]; omega

theorem saturated_closed_path_phase (q : Nat → Triple) (e : Nat → Nat) (n : Nat)
    (hv : ∀ i, i<n → valid (q i) ∧ e i ≤ 1)
    (evolves : ∀ i, i<n → q (i+1)=next (q i) (e i))
    (closed : q n=q 0)
    (sat : 2*total (fun i => (overflow3 (q i) (e i) : Int)) n = (n : Int)) :
    ∀ i, i<n → phase (q (i+1)) = (phase (q i)+1)%8 := by
  have hcert : ∀ i, i<n → Certificate (q i) (e i) := by
    intro i hi
    exact edge_certificate _ _ (hv i hi).1 (hv i hi).2
  have hsnonneg : ∀ i, i<n → 0 ≤ slack (q i) (e i) := by
    intro i hi; exact (hcert i hi).2.1
  have ht := slack_telescope q e n evolves
  rw [closed] at ht
  have hsz : total (fun i => slack (q i) (e i)) n=0 := by omega
  have hszero := zero_total_each_zero _ n hsnonneg hsz
  have hrle : ∀ i, i<n → rank (q (i+1)) ≤ rank (q i) := by
    intro i hi
    rw [evolves i hi]
    exact ((hcert i hi).2.2 (hszero i hi)).1
  have hrnonneg : ∀ i, i<n → 0 ≤ (rank (q i) : Int)-(rank (q (i+1)) : Int) := by
    intro i hi; have h := hrle i hi; omega
  have hrt := rank_telescope q n
  rw [closed] at hrt
  have hrz : total (fun i => (rank (q i) : Int)-(rank (q (i+1)) : Int)) n=0 := by omega
  have hrevery := zero_total_each_zero _ n hrnonneg hrz
  intro i hi
  have heq := evolves i hi
  have hr : rank (next (q i) (e i))=rank (q i) := by
    have h := hrevery i hi
    rw [← heq]
    omega
  rw [heq]
  exact ((hcert i hi).2.2 (hszero i hi)).2 hr

theorem phase_walk (q : Nat → Triple) (n : Nat)
    (h : ∀ i, i<n → phase (q (i+1))=(phase (q i)+1)%8) :
    phase (q n)%8=(phase (q 0)+n)%8 := by
  induction n with
  | zero => simp
  | succ n ih =>
    have hh := ih (by intro i hi; exact h i (by omega))
    have hn := h n (by omega)
    rw [hn]
    omega

theorem saturated_closed_path_period (q : Nat → Triple) (e : Nat → Nat) (n : Nat)
    (hv : ∀ i, i<n → valid (q i) ∧ e i ≤ 1)
    (evolves : ∀ i, i<n → q (i+1)=next (q i) (e i))
    (closed : q n=q 0)
    (sat : 2*total (fun i => (overflow3 (q i) (e i) : Int)) n = (n : Int)) :
    n%8=0 := by
  have hp := saturated_closed_path_phase q e n hv evolves closed sat
  have h := phase_walk q n hp
  rw [closed] at h
  omega


#print axioms edge_certificate
#print axioms total_congr
#print axioms total_nonneg
#print axioms zero_total_each_zero
#print axioms slack_telescope
#print axioms rank_telescope
#print axioms saturated_closed_path_phase
#print axioms phase_walk
#print axioms saturated_closed_path_period

end Agent8.Saturation

namespace Agent8

theorem prefix_next_compat (q : Triple3) (e : Nat) :
    prefixNext q e = Saturation.next q e := by rfl

theorem prefix_overflow_compat (q : Triple3) (e : Nat) :
    prefixOverflow q e = Saturation.overflow3 q e := by rfl

theorem saturated_actual_prefix_return (w : Word) (hw : CanonicalPair w)
    (hl : 6 ≤ w.length) (n : Nat)
    (closed : firstThree (orbit w n)=firstThree w)
    (sat : 2*actualOverflows w n=(n : Int)) : n%8=0 := by
  let q := fun i => firstThree (orbit w i)
  let e := fun i => inputThree (orbit w i)
  have hlen : ∀ i, 6 ≤ (orbit w i).length := by
    intro i; have h := canonical_orbit_length_mono w hw i; omega
  have hc : ∀ i, CanonicalPair (orbit w i) := canonical_orbit w hw
  have hstep := fun i => prefix_step_of_canonical (orbit w i) (hc i) (hlen i)
  have hvalid : ∀ i, Saturation.valid (q i) ∧ e i ≤ 1 := by
    intro i
    exact ⟨firstThree_valid (orbit w i) (hc i) (by have h := hlen i; omega), (hstep i).2.1⟩
  have hevol : ∀ i, q (i+1)=Saturation.next (q i) (e i) := by
    intro i
    exact (hstep i).1
  have htotal : total (fun i => (Saturation.overflow3 (q i) (e i) : Int)) n = actualOverflows w n := by
    apply Saturation.total_congr
    intro i _
    exact congrArg (fun a : Nat => (a : Int)) (hstep i).2.2
  apply Saturation.saturated_closed_path_period q e n
    (fun i _ => hvalid i) (fun i _ => hevol i) closed
  rw [htotal]
  exact sat

theorem no_saturated_36_step_prefix_return (w : Word) (hw : CanonicalPair w)
    (hl : 6 ≤ w.length) (hH : actualOverflows w 36=18) :
    firstThree (orbit w 36) ≠ firstThree w := by
  intro hr
  have h := saturated_actual_prefix_return w hw hl 36 hr (by omega)
  omega

theorem saturated_actual_width_return (w : Word) (hw : CanonicalPair w)
    (hl : 6 ≤ w.length) (n : Nat)
    (closed : firstThree (orbit w n)=firstThree w)
    (hWidth : 2*((orbit w n).length-w.length)=n) : n%8=0 := by
  have hm := canonical_orbit_length_mono w hw n
  have hwid := actual_width w hw n
  apply saturated_actual_prefix_return w hw hl n closed
  omega


#print axioms prefix_next_compat
#print axioms prefix_overflow_compat
#print axioms saturated_actual_prefix_return
#print axioms no_saturated_36_step_prefix_return
#print axioms saturated_actual_width_return

end Agent8
