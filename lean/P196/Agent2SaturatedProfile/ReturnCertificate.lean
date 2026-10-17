import P196.Agent2SaturatedProfile.TemplateStep

/-!
Agent #109: soundness of finite *return certificates* for the complementary
two-gap template (conditional criterion of
`2026-10-15-complementary-bulk-quotient/METHOD_AND_PROOF.md`).

A certificate is a finite cyclic list of symbolic states `(c,B,A,C)` together
with explicit trimming data linking the exact successor `(2t_c, B_r, A_r, C_r)`
(identity (8), `Agent109.stepWord_template`) to the next listed state, lower
bounds for both band lengths, and a band-length-independent non-palindrome test.
Soundness: if the Boolean checker accepts, every ordinary integer realizing the
first state with long enough bands has an infinite palindrome-free orbit after
one step. **No certificate instance is known or supplied here.**

Core Lean 4.19.0 + Std only (see the token scan of the accompanying build).
-/

namespace Agent109.Cert

open Agent109

/-! ## Palindromicity of the nine-segment shape -/

theorem append_inj_left' {a b c d : Word} (h : a ++ b = c ++ d) (hl : a.length = c.length) :
    a = c ∧ b = d := List.append_inj h hl

theorem shape_reverse (X1 X2 X3 X4 X5 : Word) (m n p q : Nat) :
    (X1 ++ List.replicate m p ++ X2 ++ List.replicate n q ++ X3 ++
      List.replicate n q ++ X4 ++ List.replicate m p ++ X5).reverse =
    X5.reverse ++ List.replicate m p ++ X4.reverse ++ List.replicate n q ++ X3.reverse ++
      List.replicate n q ++ X2.reverse ++ List.replicate m p ++ X1.reverse := by
  simp [List.reverse_append, List.reverse_replicate, List.append_assoc]

/-- A nine-segment word with mirrored segment lengths is a palindrome iff its
three finite blocks are mirrored; the run lengths `m,n` are irrelevant. -/
theorem shape_palindrome_iff (X1 X2 X3 X4 X5 : Word) (m n p q : Nat)
    (h15 : X1.length = X5.length) (h24 : X2.length = X4.length) :
    (X1 ++ List.replicate m p ++ X2 ++ List.replicate n q ++ X3 ++
      List.replicate n q ++ X4 ++ List.replicate m p ++ X5).reverse =
    (X1 ++ List.replicate m p ++ X2 ++ List.replicate n q ++ X3 ++
      List.replicate n q ++ X4 ++ List.replicate m p ++ X5) ↔
    (X5.reverse = X1 ∧ X4.reverse = X2 ∧ X3.reverse = X3) := by
  rw [shape_reverse]
  simp only [List.append_assoc]
  constructor
  · intro h
    obtain ⟨e1, h⟩ := List.append_inj h (by simp [h15])
    obtain ⟨_, h⟩ := List.append_inj h (by simp)
    obtain ⟨e2, h⟩ := List.append_inj h (by simp [h24])
    obtain ⟨_, h⟩ := List.append_inj h (by simp)
    obtain ⟨e3, _⟩ := List.append_inj h (by simp)
    exact ⟨e1, e2, e3⟩
  · rintro ⟨e1, e2, e3⟩
    rw [e1, e2, e3]
    have e4 : X4 = X2.reverse := by rw [← e2, List.reverse_reverse]
    have e5 : X5 = X1.reverse := by rw [← e1, List.reverse_reverse]
    rw [e4, e5]

/-! ## The digit word of a template step in nine-segment form -/

/-- Band-length-independent palindrome test of the next ordinary integer. -/
def StepPal (c : Nat) (B A C : Word) : Prop :=
  if (data c B A C).γ = 0 then
    ([tOf c] ++ (data c B A C).DRB).reverse = (data c B A C).DB ++ [u0 c B A C] ∧
    ([tOf (18 - c)] ++ (data c B A C).DRA ++ [u3 c B A C]).reverse =
      [tOf c] ++ (data c B A C).DA ++ [u1 c B A C] ∧
    ([tOf (18 - c)] ++ (data c B A C).DC ++ [u2 c B A C]).reverse =
      [tOf (18 - c)] ++ (data c B A C).DC ++ [u2 c B A C]
  else
    ((data c B A C).DRB ++ [1]).reverse = (data c B A C).DB ++ [u0 c B A C] ∧
    ((data c B A C).DRA ++ [u3 c B A C]).reverse = (data c B A C).DA ++ [u1 c B A C] ∧
    ((data c B A C).DC ++ [u2 c B A C]).reverse = (data c B A C).DC ++ [u2 c B A C]

instance (x : Nat) : Decidable (Phase x) :=
  inferInstanceAs (Decidable (1 ≤ x ∧ x ≤ 17 ∧ x ≠ 9))

instance (w : Word) : Decidable (Bounded w) :=
  inferInstanceAs (Decidable (∀ x ∈ w, x ≤ 18))

instance (c : Nat) (B A C : Word) : Decidable (StepPal c B A C) := by
  unfold StepPal; exact inferInstance

/-- For all band lengths `g+2, h+2`, the next ordinary integer of a realized
template is a palindrome iff `StepPal` holds. -/
theorem step_palindrome_template (n c : Nat) (B A C : Word) (g h : Nat) (hc : Phase c)
    (hB : Bounded B) (hA : Bounded A) (hC : Bounded C)
    (hn : pairWord n = template c B A C (g + 2) (h + 2)) :
    Palindrome (step n) ↔ StepPal c B A C := by
  rw [actual_template_palindrome_iff n c B A C (g + 1) (h + 1) hc hB hA hC hn]
  have hlB : (data c B A C).DB.length = B.length := norm_length _ _
  have hlRB : (data c B A C).DRB.length = B.length := by simp [data, norm_length]
  have hlA : (data c B A C).DA.length = A.length := norm_length _ _
  have hlRA : (data c B A C).DRA.length = A.length := by simp [data, norm_length]
  have hγ1 := gamma_le c B A C hB
  unfold StepPal
  rcases (by omega : (data c B A C).γ = 0 ∨ (data c B A C).γ = 1) with hγ | hγ
  · have hw : digitWord c B A C (g + 1) (h + 1) ++ carryWord (data c B A C).γ =
        ((data c B A C).DB ++ [u0 c B A C]) ++ List.replicate g (tOf c) ++
        ([tOf c] ++ (data c B A C).DA ++ [u1 c B A C]) ++ List.replicate h (tOf (18 - c)) ++
        ([tOf (18 - c)] ++ (data c B A C).DC ++ [u2 c B A C]) ++
        List.replicate h (tOf (18 - c)) ++
        ([tOf (18 - c)] ++ (data c B A C).DRA ++ [u3 c B A C]) ++
        List.replicate g (tOf c) ++ ([tOf c] ++ (data c B A C).DRB) := by
      simp only [digitWord, carryWord, hγ, if_true, List.append_nil,
        List.replicate_succ', List.append_assoc, List.cons_append, List.singleton_append,
        List.nil_append]
    rw [hw, shape_palindrome_iff _ _ _ _ _ _ _ _ _ (by simp [hlB, hlRB]) (by simp [hlA, hlRA])]
    simp only [hγ, if_true]
  · have hw : digitWord c B A C (g + 1) (h + 1) ++ carryWord (data c B A C).γ =
        ((data c B A C).DB ++ [u0 c B A C]) ++ List.replicate (g + 1) (tOf c) ++
        ((data c B A C).DA ++ [u1 c B A C]) ++ List.replicate (h + 1) (tOf (18 - c)) ++
        ((data c B A C).DC ++ [u2 c B A C]) ++
        List.replicate (h + 1) (tOf (18 - c)) ++
        ((data c B A C).DRA ++ [u3 c B A C]) ++
        List.replicate (g + 1) (tOf c) ++ ((data c B A C).DRB ++ [1]) := by
      simp only [digitWord, carryWord, hγ, List.append_assoc, List.cons_append,
        List.singleton_append, List.nil_append]
      simp
    rw [hw, shape_palindrome_iff _ _ _ _ _ _ _ _ _ (by simp [hlB, hlRB]) (by simp [hlA, hlRA])]
    simp only [hγ]
    simp

/-! ## Moving band letters out of the finite blocks -/

theorem template_trim (c : Nat) (B A C : Word) (j j1 j2 k g h : Nat) :
    template c (B ++ List.replicate j c)
        (List.replicate j1 c ++ A ++ List.replicate j2 (18 - c))
        (List.replicate k (18 - c) ++ C ++ List.replicate k (18 - c)) g h =
      template c B A C (g + j + j1) (h + j2 + k) := by
  simp only [template, List.reverse_append, List.reverse_replicate, List.append_assoc]
  have r1 : ∀ (l : Word), List.replicate j c ++ (List.replicate g c ++
      (List.replicate j1 c ++ l)) = List.replicate (g + j + j1) c ++ l := by
    intro l
    rw [← List.append_assoc, ← List.append_assoc, List.replicate_append_replicate,
      List.replicate_append_replicate]
    congr 2; omega
  have r2 : ∀ (l : Word), List.replicate j2 (18 - c) ++ (List.replicate h (18 - c) ++
      (List.replicate k (18 - c) ++ l)) = List.replicate (h + j2 + k) (18 - c) ++ l := by
    intro l
    rw [← List.append_assoc, ← List.append_assoc, List.replicate_append_replicate,
      List.replicate_append_replicate]
    congr 2; omega
  have r3 : ∀ (l : Word), List.replicate k (18 - c) ++ (List.replicate h (18 - c) ++
      (List.replicate j2 (18 - c) ++ l)) = List.replicate (h + j2 + k) (18 - c) ++ l := by
    intro l
    rw [← List.append_assoc, ← List.append_assoc, List.replicate_append_replicate,
      List.replicate_append_replicate]
    congr 2; omega
  have r4 : ∀ (l : Word), List.replicate j1 c ++ (List.replicate g c ++
      (List.replicate j c ++ l)) = List.replicate (g + j + j1) c ++ l := by
    intro l
    rw [← List.append_assoc, ← List.append_assoc, List.replicate_append_replicate,
      List.replicate_append_replicate]
    congr 2; omega
  rw [r1, r2, r3, r4]

/-! ## Certificates -/

structure State where
  c : Nat
  B : Word
  A : Word
  C : Word
deriving DecidableEq, Repr, Inhabited

/-- Trimming data: `B_r = B' ++ c'^j`, `A_r = c'^j1 ++ A' ++ d'^j2`,
`C_r = d'^k ++ C' ++ d'^k`, and lower bounds `lo`, `lo'` for the band
lengths at this state. -/
structure Link where
  j : Nat
  j1 : Nat
  j2 : Nat
  k : Nat
  lo : Nat
  lo' : Nat
deriving DecidableEq, Repr, Inhabited

structure Certificate where
  states : List State
  links : List Link
deriving Repr

def gam (s : State) : Nat := (data s.c s.B s.A s.C).γ

/-- The local condition at index `i` (successor index `i+1 mod P`). -/
def LocalOK (s s' : State) (L L' : Link) : Prop :=
  Phase s.c ∧ Bounded s.B ∧ Bounded s.A ∧ Bounded s.C ∧
  tOf s.c + tOf s.c = s'.c ∧
  Br s.c s.B s.A s.C = s'.B ++ List.replicate L.j s'.c ∧
  Ar s.c s.B s.A s.C =
    List.replicate L.j1 s'.c ++ s'.A ++ List.replicate L.j2 (18 - s'.c) ∧
  Cr s.c s.B s.A s.C =
    List.replicate L.k (18 - s'.c) ++ s'.C ++ List.replicate L.k (18 - s'.c) ∧
  ¬ StepPal s.c s.B s.A s.C ∧
  2 ≤ L.lo ∧ 2 ≤ L.lo' ∧
  L'.lo + 2 ≤ L.lo + gam s + L.j + L.j1 ∧
  L'.lo' + 2 ≤ L.lo' + gam s + L.j2 + L.k

instance (s s' : State) (L L' : Link) : Decidable (LocalOK s s' L L') := by
  unfold LocalOK; exact inferInstance

def Certificate.P (cert : Certificate) : Nat := cert.states.length
def Certificate.st (cert : Certificate) (i : Nat) : State := cert.states.getD i default
def Certificate.lk (cert : Certificate) (i : Nat) : Link := cert.links.getD i default

/-- Proposition-level validity. -/
def Valid (cert : Certificate) : Prop :=
  0 < cert.P ∧ ∀ i, i < cert.P →
    LocalOK (cert.st i) (cert.st ((i + 1) % cert.P)) (cert.lk i) (cert.lk ((i + 1) % cert.P))

/-- Boolean checker (kernel-evaluable by `decide`). -/
def check (cert : Certificate) : Bool :=
  decide (0 < cert.P) &&
    (List.range cert.P).all fun i =>
      decide (LocalOK (cert.st i) (cert.st ((i + 1) % cert.P)) (cert.lk i)
        (cert.lk ((i + 1) % cert.P)))

theorem check_sound (cert : Certificate) (h : check cert = true) : Valid cert := by
  unfold check at h
  simp only [Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true, List.mem_range] at h
  exact ⟨h.1, fun i hi => h.2 i hi⟩

/-! ## Soundness -/

/-- The orbit invariant: `m` is the successor of an integer realizing some
certificate state with band lengths above that state's bounds. -/
def Inv (cert : Certificate) (m : Nat) : Prop :=
  ∃ i, i < cert.P ∧ ∃ G H n, m = step n ∧
    pairWord n = template (cert.st i).c (cert.st i).B (cert.st i).A (cert.st i).C G H ∧
    (cert.lk i).lo ≤ G ∧ (cert.lk i).lo' ≤ H

theorem inv_not_palindrome (cert : Certificate) (hv : Valid cert) (m : Nat)
    (hm : Inv cert m) : ¬ Palindrome m := by
  obtain ⟨i, hi, G, H, n, rfl, hn, hG, hH⟩ := hm
  have hl := hv.2 i hi
  obtain ⟨hc, hB, hA, hC, -, -, -, -, hnp, h2, h2', -, -⟩ := hl
  obtain ⟨g, rfl⟩ : ∃ g, G = g + 2 := ⟨G - 2, by omega⟩
  obtain ⟨h, rfl⟩ : ∃ h, H = h + 2 := ⟨H - 2, by omega⟩
  rw [step_palindrome_template n _ _ _ _ g h hc hB hA hC hn]
  exact hnp

theorem inv_step (cert : Certificate) (hv : Valid cert) (m : Nat)
    (hm : Inv cert m) : Inv cert (step m) := by
  obtain ⟨i, hi, G, H, n, rfl, hn, hG, hH⟩ := hm
  have hl := hv.2 i hi
  obtain ⟨hc, hB, hA, hC, hc', hBr, hAr, hCr, -, h2, h2', hlo, hlo'⟩ := hl
  obtain ⟨g, rfl⟩ : ∃ g, G = g + 2 := ⟨G - 2, by omega⟩
  obtain ⟨h, rfl⟩ : ∃ h, H = h + 2 := ⟨H - 2, by omega⟩
  have hs := actual_template_step n _ _ _ _ g h hc hB hA hC hn
  rw [hc', hBr, hAr, hCr, template_trim] at hs
  refine ⟨(i + 1) % cert.P, Nat.mod_lt _ hv.1, _, _, step n, rfl, hs, ?_, ?_⟩
  · unfold gam at hlo; omega
  · unfold gam at hlo'; omega

/-- **Certificate soundness.** If `check cert = true`, then for every ordinary
integer `n` whose mirrored pair word is the template of the first state with
band lengths at least the first bounds, no iterate of `step n` is a palindrome. -/
theorem certificate_sound (cert : Certificate) (hc : check cert = true) (n G H : Nat)
    (hn : pairWord n = template (cert.st 0).c (cert.st 0).B (cert.st 0).A (cert.st 0).C G H)
    (hG : (cert.lk 0).lo ≤ G) (hH : (cert.lk 0).lo' ≤ H) :
    ∀ k, ¬ Palindrome (orbit (step n) k) := by
  have hv := check_sound cert hc
  have hinv : ∀ k, Inv cert (orbit (step n) k) := by
    intro k
    induction k with
    | zero => exact ⟨0, hv.1, G, H, n, rfl, hn, hG, hH⟩
    | succ k ih => exact inv_step cert hv _ ih
  exact fun k => inv_not_palindrome cert hv _ (hinv k)

/-! ## Realizability of admissible templates by ordinary integers -/

/-- Mirrored pair-word shape: symmetric, with an even middle coefficient. -/
inductive Mirr : Word → Prop
  | nil : Mirr []
  | single (m : Nat) : m % 2 = 0 → Mirr [m]
  | wrap (a : Nat) (q : Word) : Mirr q → Mirr ([a] ++ q ++ [a])

theorem realize (q : Word) (hq : Mirr q) (hb : Bounded q) :
    ∃ D : Word, pair D = q ∧ (∀ y ∈ D, y < 10) ∧ (LastPos q → LastPos D) := by
  induction hq with
  | nil => exact ⟨[], rfl, by simp, fun _ => fun x hx => by simp at hx⟩
  | single m hm =>
    have hm18 := hb m (by simp)
    refine ⟨[m / 2], ?_, ?_, ?_⟩
    · simp [pair, zipAdd]; omega
    · simp; omega
    · intro hl x hx
      have := hl m (by simp)
      simp at hx; omega
  | wrap a q hq ih =>
    have ha := hb a (by simp)
    obtain ⟨D, hD, hd, -⟩ := ih (fun x hx => hb x (by simp [hx]))
    refine ⟨[a - min 9 a] ++ D ++ [min 9 a], ?_, ?_, ?_⟩
    · have hrev : ([a - min 9 a] ++ D ++ [min 9 a]).reverse =
          [min 9 a] ++ D.reverse ++ [a - min 9 a] := by simp
      rw [pair, hrev, List.append_assoc, List.append_assoc,
        zipAdd_append _ _ _ _ (by simp),
        zipAdd_append _ _ _ _ (by simp : D.length = D.reverse.length)]
      have : pair D = zipAdd D D.reverse := rfl
      rw [← this, hD]
      simp [zipAdd]
      constructor <;> omega
    · intro y hy
      simp only [List.mem_append, List.mem_singleton] at hy
      rcases hy with (hy | hy) | hy
      · omega
      · exact hd y hy
      · omega
    · intro hl x hx
      have h1 : ([a] ++ q ++ [a]).getLast? = some a := by
        rw [List.getLast?_append]; simp
      have hpos := hl a h1
      have h2 : ([a - min 9 a] ++ D ++ [min 9 a]).getLast? = some (min 9 a) := by
        rw [List.getLast?_append]; simp
      rw [h2] at hx
      have hx' : min 9 a = x := Option.some.inj hx
      omega

theorem mirr_wrap (X C : Word) (hC : Mirr C) : Mirr (X ++ C ++ X.reverse) := by
  induction X with
  | nil => simpa using hC
  | cons x X ih =>
    have : x :: X ++ C ++ (x :: X).reverse = [x] ++ (X ++ C ++ X.reverse) ++ [x] := by simp
    rw [this]; exact Mirr.wrap x _ ih

theorem template_mirr (c : Nat) (B A C : Word) (g h : Nat) (hC : Mirr C) :
    Mirr (template c B A C g h) := by
  have := mirr_wrap (B ++ List.replicate g c ++ A ++ List.replicate h (18 - c)) C hC
  have e : template c B A C g h =
      (B ++ List.replicate g c ++ A ++ List.replicate h (18 - c)) ++ C ++
        (B ++ List.replicate g c ++ A ++ List.replicate h (18 - c)).reverse := by
    simp [template, List.reverse_append, List.reverse_replicate]
  rw [e]; exact this

theorem template_lastPos (c : Nat) (B A C : Word) (g h : Nat) (hc : Phase c) (hg : 0 < g)
    (hB : ∀ b, B.head? = some b → 0 < b) : LastPos (template c B A C g h) := by
  intro x hx
  unfold template at hx
  rw [List.getLast?_append] at hx
  cases hBe : B with
  | nil =>
    rw [hBe] at hx
    simp at hx
    obtain ⟨g', rfl⟩ : ∃ g', g = g' + 1 := ⟨g - 1, by omega⟩
    rw [List.getLast?_replicate] at hx
    simp at hx
    unfold Phase at hc; omega
  | cons b B' =>
    rw [hBe] at hx
    simp [List.getLast?_reverse] at hx
    exact hx ▸ hB b (by simp [hBe])

theorem template_bounded (c : Nat) (B A C : Word) (g h : Nat) (hc : Phase c)
    (hB : Bounded B) (hA : Bounded A) (hC : Bounded C) :
    Bounded (template c B A C g h) := by
  unfold Phase at hc
  intro x hx
  simp only [template, List.mem_append, List.mem_reverse, List.mem_replicate] at hx
  rcases hx with ((((((((h1 | h1) | h1) | h1) | h1) | h1) | h1) | h1) | h1)
  · exact hB x h1
  · omega
  · exact hA x h1
  · omega
  · exact hC x h1
  · omega
  · exact hA x h1
  · omega
  · exact hB x h1

/-- Every admissible template is the mirrored pair word of an ordinary integer. -/
theorem template_realized (c : Nat) (B A C : Word) (g h : Nat) (hc : Phase c) (hg : 0 < g)
    (hB : Bounded B) (hA : Bounded A) (hC : Bounded C) (hCm : Mirr C)
    (hB0 : ∀ b, B.head? = some b → 0 < b) :
    ∃ n, pairWord n = template c B A C g h := by
  obtain ⟨D, hD, hd, hl⟩ := realize _ (template_mirr c B A C g h hCm)
    (template_bounded c B A C g h hc hB hA hC)
  have hcan : Canon D := (canon_iff D).mpr ⟨hd, hl (template_lastPos c B A C g h hc hg hB0)⟩
  exact ⟨evalL D, by rw [pairWord, digits_evalL D hcan, hD]⟩

/-! ## Existence from a certificate -/

/-- Admissibility of the first state: `C₀ = H ++ M ++ rev H` with `M` empty or
one even coefficient, and a positive exterior if `B₀` is nonempty. -/
def Admissible0 (cert : Certificate) (H M : Word) : Prop :=
  (cert.st 0).C = H ++ M ++ H.reverse ∧ M.length ≤ 1 ∧ (∀ m ∈ M, m % 2 = 0) ∧
  (∀ b, (cert.st 0).B.head? = some b → 0 < b)

instance (cert : Certificate) (H M : Word) : Decidable (Admissible0 cert H M) := by
  unfold Admissible0; exact inferInstance

theorem mirr_of_split (H M : Word) (hM : M.length ≤ 1) (he : ∀ m ∈ M, m % 2 = 0) :
    Mirr (H ++ M ++ H.reverse) := by
  apply mirr_wrap
  cases M with
  | nil => exact Mirr.nil
  | cons m M' =>
    cases M' with
    | nil => exact Mirr.single m (he m (by simp))
    | cons _ _ => simp at hM

/-- **Conditional existence.** An accepted certificate with an admissible first
state yields an ordinary integer none of whose iterates (including itself) is a
palindrome. -/
theorem certificate_existence (cert : Certificate) (hc : check cert = true)
    (H M : Word) (hadm : decide (Admissible0 cert H M) = true) :
    ∃ m, ∀ k, ¬ Palindrome (orbit m k) := by
  have hv := check_sound cert hc
  have ha : Admissible0 cert H M := of_decide_eq_true hadm
  obtain ⟨hCe, hM, hev, hB0⟩ := ha
  obtain ⟨hph, hB, hA, hC, -, -, -, -, -, h2, h2', -, -⟩ := hv.2 0 hv.1
  have hCm : Mirr (cert.st 0).C := by rw [hCe]; exact mirr_of_split H M hM hev
  obtain ⟨n, hn⟩ := template_realized _ _ _ _ (cert.lk 0).lo (cert.lk 0).lo' hph
    (by omega) hB hA hC hCm hB0
  exact ⟨step n, certificate_sound cert hc n _ _ hn (Nat.le_refl _) (Nat.le_refl _)⟩

end Agent109.Cert

#print axioms Agent109.Cert.shape_palindrome_iff
#print axioms Agent109.Cert.step_palindrome_template
#print axioms Agent109.Cert.template_trim
#print axioms Agent109.Cert.check_sound
#print axioms Agent109.Cert.certificate_sound
#print axioms Agent109.Cert.template_realized
#print axioms Agent109.Cert.certificate_existence
