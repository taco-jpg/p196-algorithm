import PeriodObstructions

namespace Agent8

/-- Normalize without appending the terminal carry. -/
def fixedDigits : Word → Nat → Word
  | [], _ => []
  | x :: xs, e => ((x + e) % 10) :: fixedDigits xs ((x + e) / 10)

def terminalCarry : Word → Nat → Nat
  | [], e => e
  | x :: xs, e => terminalCarry xs ((x + e) / 10)

def Bounded (w : Word) (b : Nat) : Prop := ∀ x ∈ w, x ≤ b

def CanonicalPair (w : Word) : Prop :=
  w ≠ [] ∧ w.reverse = w ∧ Bounded w 18 ∧ 0 < w.headD 0

theorem normalize_decompose (w : Word) (e : Nat) :
    normalize w e = fixedDigits w e ++
      (if terminalCarry w e = 0 then [] else [terminalCarry w e]) := by
  induction w generalizing e with
  | nil => rfl
  | cons x xs ih => simp [normalize, fixedDigits, terminalCarry, ih]

theorem fixedDigits_length (w : Word) (e : Nat) :
    (fixedDigits w e).length = w.length := by
  induction w generalizing e with
  | nil => rfl
  | cons x xs ih => simp [fixedDigits, ih]

theorem terminalCarry_le_one (w : Word) (e : Nat) (hw : Bounded w 18)
    (he : e ≤ 1) : terminalCarry w e ≤ 1 := by
  induction w generalizing e with
  | nil => exact he
  | cons x xs ih =>
    have hx := hw x (by simp)
    have hxs : Bounded xs 18 := by
      intro a ha; exact hw a (by simp [ha])
    exact ih ((x+e)/10) hxs (by omega)

theorem normalize_append (a b : Word) (e : Nat) :
    normalize (a ++ b) e = fixedDigits a e ++ normalize b (terminalCarry a e) := by
  induction a generalizing e with
  | nil => rfl
  | cons x xs ih => simp [normalize, fixedDigits, terminalCarry, ih]

theorem terminalCarry_append (a b : Word) (e : Nat) :
    terminalCarry (a ++ b) e = terminalCarry b (terminalCarry a e) := by
  induction a generalizing e with
  | nil => rfl
  | cons x xs ih => simp [terminalCarry, ih]

theorem normalize_length (w : Word) (e : Nat) (hw : Bounded w 18)
    (he : e ≤ 1) : (normalize w e).length = w.length + terminalCarry w e := by
  rw [normalize_decompose]
  have hc := terminalCarry_le_one w e hw he
  simp only [List.length_append, fixedDigits_length]
  split <;> simp_all <;> omega

theorem normalized_digits_bounded (w : Word) (e : Nat) (hw : Bounded w 18)
    (he : e ≤ 1) : Bounded (normalize w e) 9 := by
  induction w generalizing e with
  | nil =>
    simp only [normalize]
    split
    · intro a ha; simp at ha
    · intro a ha; simp only [List.mem_singleton] at ha; omega
  | cons x xs ih =>
    have hx := hw x (by simp)
    have hxs : Bounded xs 18 := by
      intro a ha; exact hw a (by simp [ha])
    have ht := ih ((x+e)/10) hxs (by omega)
    intro a ha
    simp only [normalize, List.mem_cons] at ha
    rcases ha with rfl | ha
    · omega
    · exact ht a ha

theorem zipAdd_eq_zipWith (a b : Word) : zipAdd a b = List.zipWith (·+·) a b := by
  induction a generalizing b with
  | nil => cases b <;> rfl
  | cons x xs ih => cases b <;> simp [zipAdd, List.zipWith, ih]

theorem pair_length (w : Word) : (pair w).length = w.length := by
  simp [pair, zipAdd_eq_zipWith, List.length_zipWith]

theorem pair_symmetric (w : Word) : (pair w).reverse = pair w := by
  simp only [pair, zipAdd_eq_zipWith]
  rw [List.reverse_zipWith (by simp), List.reverse_reverse, List.zipWith_comm]
  simp only [Nat.add_comm]

theorem zipAdd_bounded (a b : Word) (ha : Bounded a 9) (hb : Bounded b 9) :
    Bounded (zipAdd a b) 18 := by
  induction a generalizing b with
  | nil => intro x hx; simp [zipAdd] at hx
  | cons x xs ih =>
    cases b with
    | nil => intro z hz; simp [zipAdd] at hz
    | cons y ys =>
      have hx := ha x (by simp)
      have hy := hb y (by simp)
      have hxs : Bounded xs 9 := by intro z hz; exact ha z (by simp [hz])
      have hys : Bounded ys 9 := by intro z hz; exact hb z (by simp [hz])
      intro z hz
      simp only [zipAdd, List.mem_cons] at hz
      rcases hz with rfl | hz
      · omega
      · exact ih ys hxs hys z hz

theorem pair_bounded (w : Word) (h : Bounded w 9) : Bounded (pair w) 18 := by
  apply zipAdd_bounded w w.reverse h
  intro x hx
  exact h x (by simpa using hx)

theorem pair_head (w : Word) (p q : Nat) (hh : w.head? = some p)
    (hl : w.getLast? = some q) : (pair w).head? = some (p+q) := by
  simp only [pair, zipAdd_eq_zipWith, List.head?_zipWith, List.head?_reverse, hh, hl]

theorem normalize_singleton (p e : Nat) (hp : p ≤ 18) (he : e ≤ 1) :
    normalize [p] e = if p+e<10 then [p+e] else [(p+e)%10, 1] := by
  by_cases h : p+e<10
  · have hd : (p+e)/10=0 := by omega
    have hr : (p+e)%10=p+e := by omega
    simp [normalize, hd, hr, h]
  · have hd : (p+e)/10=1 := by omega
    simp [normalize, hd, h]

/-- The actual carry entering the final column. -/
def lastInput (w : Word) : Nat := terminalCarry w.dropLast 0

theorem canonical_step (w : Word) (hw : CanonicalPair w) :
    CanonicalPair (stepWord w) ∧
    (stepWord w).headD 0 = nextExterior (w.headD 0) (lastInput w) ∧
    (stepWord w).length = w.length + overflow (w.headD 0) (lastInput w) ∧
    lastInput w ≤ 1 := by
  cases w with
  | nil => exact False.elim (hw.1 rfl)
  | cons p xs =>
    rcases hw with ⟨hne, hrev, hbound, hpos⟩
    have hp : 0 < p := by simpa using hpos
    have hp18 : p ≤ 18 := hbound p (by simp)
    have hxs : Bounded xs.reverse 18 := by
      intro a ha
      have ha' : a ∈ xs := by simpa using ha
      exact hbound a (by simp [ha'])
    have hsnoc : p :: xs = xs.reverse ++ [p] := by
      simpa only [List.reverse_cons] using hrev.symm
    have hdrop : (p :: xs).dropLast = xs.reverse := by
      calc
        (p :: xs).dropLast = (p :: xs).reverse.dropLast := congrArg List.dropLast hrev.symm
        _ = xs.reverse := by simp
    let e := terminalCarry xs.reverse 0
    have he : e ≤ 1 := terminalCarry_le_one xs.reverse 0 hxs (by decide)
    have hn : normalize (p :: xs) 0 = fixedDigits xs.reverse 0 ++ normalize [p] e := by
      rw [hsnoc, normalize_append]
    have hh : (normalize (p :: xs) 0).head? = some (p % 10) := by
      simp [normalize]
    have hl : (normalize (p :: xs) 0).getLast? = some (if p+e<10 then p+e else 1) := by
      rw [hn, normalize_singleton p e hp18 he]
      split <;> simp
    have hformula : p % 10 + (if p+e<10 then p+e else 1) = nextExterior p e := by
      by_cases h : p+e<10
      · simp only [nextExterior, if_pos h]
        omega
      · simp [nextExterior, h]
    have hhead : (stepWord (p :: xs)).head? = some (nextExterior p e) := by
      simpa only [stepWord, hformula] using pair_head _ _ _ hh hl
    have hheadD : (stepWord (p :: xs)).headD 0 = nextExterior p e := by
      simp [List.headD_eq_head?_getD, hhead]
    have hcert := finite_exterior_certificate ⟨p, by omega⟩ ⟨e, by omega⟩ hp
    have hcanon : CanonicalPair (stepWord (p :: xs)) := by
      refine ⟨?_, pair_symmetric _, pair_bounded _ (normalized_digits_bounded _ 0 hbound (by decide)), ?_⟩
      · intro hnil
        simp [hnil] at hhead
      · rw [hheadD]
        exact hcert.1
    have hcarry : terminalCarry (p :: xs) 0 = overflow p e := by
      rw [hsnoc, terminalCarry_append]
      change (p+e)/10 = overflow p e
      simp only [overflow]
      split <;> omega
    have hlen : (stepWord (p :: xs)).length = (p :: xs).length + overflow p e := by
      rw [stepWord, pair_length, normalize_length _ 0 hbound (by decide), hcarry]
    have hin : lastInput (p :: xs) = e := by simp [lastInput, hdrop, e]
    exact ⟨hcanon, by simpa [hin] using hheadD, by simpa [hin] using hlen, by simpa [hin] using he⟩

theorem canonical_orbit (w : Word) (hw : CanonicalPair w) (n : Nat) :
    CanonicalPair (orbit w n) := by
  induction n with
  | zero => exact hw
  | succ n ih => exact (canonical_step (orbit w n) ih).1

theorem canonical_head_bounds (w : Word) (hw : CanonicalPair w) :
    0 < w.headD 0 ∧ w.headD 0 ≤ 18 := by
  cases w with
  | nil => exact False.elim (hw.1 rfl)
  | cons p xs => exact ⟨hw.2.2.2, hw.2.2.1 p (by simp)⟩

def actualExterior (w : Word) (i : Nat) : Nat := (orbit w i).headD 0

def actualInput (w : Word) (i : Nat) : Nat := lastInput (orbit w i)

def actualOverflows (w : Word) (n : Nat) : Int :=
  total (fun i => (overflow (actualExterior w i) (actualInput w i) : Int)) n

theorem actual_path_valid (w : Word) (hw : CanonicalPair w) (i : Nat) :
    0 < actualExterior w i ∧ actualExterior w i ≤ 18 ∧ actualInput w i ≤ 1 := by
  have hc := canonical_orbit w hw i
  have hh := canonical_head_bounds (orbit w i) hc
  have hi := (canonical_step (orbit w i) hc).2.2.2
  exact ⟨hh.1, hh.2, hi⟩

theorem actual_path_evolves (w : Word) (hw : CanonicalPair w) (i : Nat) :
    actualExterior w (i+1) = nextExterior (actualExterior w i) (actualInput w i) := by
  exact (canonical_step (orbit w i) (canonical_orbit w hw i)).2.1

theorem actual_width (w : Word) (hw : CanonicalPair w) (n : Nat) :
    ((orbit w n).length : Int) = (w.length : Int) + actualOverflows w n := by
  induction n with
  | zero => simp [orbit, actualOverflows, total]
  | succ n ih =>
    have hl := (canonical_step (orbit w n) (canonical_orbit w hw n)).2.2.1
    change (orbit w (n+1)).length = (orbit w n).length +
      overflow (actualExterior w n) (actualInput w n) at hl
    simp only [actualOverflows, total] at *
    omega

theorem actual_return_bounds (w : Word) (hw : CanonicalPair w) (n : Nat)
    (hc : actualExterior w n = actualExterior w 0) :
    (n : Int) ≤ 4 * actualOverflows w n ∧ 2 * actualOverflows w n ≤ (n : Int) := by
  exact closed_path_bounds (actualExterior w) (actualInput w) n
    (fun i _ => actual_path_valid w hw i) (fun i _ => actual_path_evolves w hw i) hc

theorem template_length (c : Nat) (B A C : Word) (g h : Nat) :
    (template c B A C g h).length = 2*B.length + 2*A.length + C.length + 2*g + 2*h := by
  simp only [template, List.length_append, List.length_replicate, List.length_reverse]
  omega

theorem template_head (c : Nat) (B A C : Word) (g h : Nat) (hg : 0 < g) :
    (template c B A C g h).headD 0 = if B = [] then c else B.headD 0 := by
  cases B with
  | nil =>
    cases g with
    | zero => omega
    | succ g => simp [template, List.replicate_succ]
  | cons b bs => simp [template]

theorem canonical_template_return_data (c : Nat) (B A C : Word)
    (g0 h0 g1 h1 n : Nat) (hg0 : 0 < g0) (hg1 : 0 < g1)
    (hw : CanonicalPair (template c B A C g0 h0))
    (hr : orbit (template c B A C g0 h0) n = template c B A C g1 h1) :
    let H := actualOverflows (template c B A C g0 h0) n
    (n : Int) ≤ 4*H ∧ 2*H ≤ (n : Int) ∧
      H = 2*(((g1 : Int)-(g0 : Int))+((h1 : Int)-(h0 : Int))) := by
  have hclosed : actualExterior (template c B A C g0 h0) n =
      actualExterior (template c B A C g0 h0) 0 := by
    simp only [actualExterior, orbit, hr]
    rw [template_head c B A C g1 h1 hg1, template_head c B A C g0 h0 hg0]
  have hb := actual_return_bounds _ hw n hclosed
  have hl := actual_width _ hw n
  rw [hr, template_length, template_length] at hl
  refine ⟨hb.1, hb.2, ?_⟩
  omega

theorem no_two_step_canonical_template_return (c : Nat) (B A C : Word)
    (g0 h0 g1 h1 : Nat) (hg0 : 0 < g0) (hg1 : 0 < g1)
    (hw : CanonicalPair (template c B A C g0 h0)) :
    orbit (template c B A C g0 h0) 2 ≠ template c B A C g1 h1 := by
  intro hr
  have hd := canonical_template_return_data c B A C g0 h0 g1 h1 2 hg0 hg1 hw hr
  exact no_two_step_return _ _ _ hd.1 hd.2.1 hd.2.2

theorem no_repeatable_six_step_canonical_template_return (c : Nat) (B A C : Word)
    (g0 h0 g1 h1 : Nat) (hc : SixPhase c) (hg0 : 0 < g0)
    (hw : CanonicalPair (template c B A C g0 h0))
    (hg : g0 ≤ g1) (hh : h0 ≤ h1) :
    orbit (template c B A C g0 h0) 6 ≠ template c B A C g1 h1 := by
  intro hr
  have hd := canonical_template_return_data c B A C g0 h0 g1 h1 6 hg0 (by omega) hw hr
  have hm := returned_template_mass_congruence c B A C g0 h0 g1 h1 1 hc hr
  exact no_repeatable_six_step_return _ _ _ hd.1 hd.2.1 hd.2.2 hm (by omega) (by omega)

#print axioms normalize_decompose
#print axioms fixedDigits_length
#print axioms terminalCarry_le_one
#print axioms normalize_append
#print axioms terminalCarry_append
#print axioms normalize_length
#print axioms normalized_digits_bounded
#print axioms zipAdd_eq_zipWith
#print axioms pair_length
#print axioms pair_symmetric
#print axioms zipAdd_bounded
#print axioms pair_bounded
#print axioms pair_head
#print axioms normalize_singleton
#print axioms canonical_step
#print axioms canonical_orbit
#print axioms canonical_head_bounds
#print axioms actual_path_valid
#print axioms actual_path_evolves
#print axioms actual_width
#print axioms actual_return_bounds
#print axioms template_length
#print axioms template_head
#print axioms canonical_template_return_data
#print axioms no_two_step_canonical_template_return
#print axioms no_repeatable_six_step_canonical_template_return

end Agent8
