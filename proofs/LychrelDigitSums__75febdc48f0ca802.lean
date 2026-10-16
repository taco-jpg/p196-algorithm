import Std

/-! Standalone decimal digit-sum research continuation.
Checked with Lean 4.19.0 and Std only.
Main result: DecimalUnboundedMass.digitSum_unbounded_after.
No decimal Lychrel existence claim is made.
The base module is retained intact below, followed by five modules. -/


/- Source module: Lychrel196Research.lean -/

/-!
# Decimal Lychrel research: verified partial results

STATUS: This is NOT a proof or disproof of the decimal Lychrel conjecture.
The infinite orbit-avoidance assertion is left as an explicitly named
proposition; it is not assumed as an axiom and has no claimed proof.

Verified with Lean 4.19.0 (commit 6caaee842e94), using only Std.
To check this standalone file: lean Lychrel196Research.lean

Contents:
1. Executable decimal reversal, exact open statements, modulo-9 lemma,
   a general inductive-invariant principle, and a finite certificate for
   orbit indices 0 through 100.
2. Arithmetic carry lemmas in both length-preserving and overflow cases.
3. Canonical decimal representation, equivalence of positional reflection
   with executable reversal, verified column addition, and a complete
   characterization of which positive inputs produce a palindrome next.
4. An exact equivalence exposing the unresolved infinite avoidance claim.
5. Conditional proof certificates with variable block lengths, expanding
   families, and a verified finite-entry principle for the 196 orbit.
   These prove soundness of the method; no certificate witness is supplied.
6. Exact folded-column dynamics, center-tested carry-trace soundness,
   and constructive realization of every admissible symmetric q word.
   No closed invariant language or verified automaton witness is supplied.
7. An exact symbolic-language soundness theorem extracting a finite decimal
   Lychrel witness from explicit admissibility, nonemptiness, closure,
   and bad-pattern avoidance hypotheses. Those hypotheses are not instantiated.
8. A two-step terminating representative for every non-overflow carry word.
9. Exact one-column binary/quaternary-to-decimal carry encodings.
10. Full numeric semantics for a finite transducer certificate showing every
    complete decimal carry word has a same-width representative terminating
    within four steps, together with a proof that four is optimal.
11. Carry-history injectivity once five no-overflow steps have occurred,
    and unconditional twelve-step and sharper eleven-step bounds for recovering
    the initial q word.
12. Sharp all-time canonical decimal width bounds.
13. Residue recurrences modulo 99 and its divisors; every positive orbit
    is divisible by 11 by time six, a sharp uniform bound.
14. No consecutive zero units digits; large actual orbit states meet the
    compatibility conditions for exact-length palindrome residue saturation.
15. Even-width palindromic overflow requires divisibility by 121.
16. General complementary-column carry identities and exact counterexamples
    to two proposed persistent-defect families.

The all-moduli exact-length palindrome saturation theorem remains a paper
proof, not a theorem declared in this Lean source.

The carry criterion is existing mathematics, not a claim of novelty:
https://mathoverflow.net/questions/117104/status-of-the-196-conjecture
The linked problem and its proved binary contrast are discussed at:
https://www.mathpages.com/home/kmath004/kmath004.htm

All theorem declarations have complete proofs. Standard logical axioms
may appear in #print axioms; no sorry, custom axiom, native_decide,
or unverified external computation is used as a proof.
-/

/-!
# The decimal 196 conjecture: an exact statement and verified partial results

This file does NOT prove that 196 is a Lychrel number.
`Decimal196Conjecture` and `DecimalLychrelExistence` are definitions of open
propositions, not theorems or axioms. Every declaration labelled `theorem`
below has a complete proof. No `sorry` or unproved axiom is used.

Decimal reversal drops leading zeros in the reversed representation, so
reverse10 1200 = 21. The orbit includes its starting value at time zero.
-/

namespace Lychrel196

/-- Decimal reversal, consuming the least significant digit at each step. -/
def reverseAux (n acc : Nat) : Nat :=
  if h : n = 0 then acc
  else reverseAux (n / 10) (10 * acc + n % 10)
termination_by n
decreasing_by
  exact Nat.div_lt_self (Nat.pos_of_ne_zero h) (by decide)

/-- Structurally recursive implementation used by kernel evaluation. -/
def reverseFuel : Nat → Nat → Nat → Nat
  | 0, _, acc => acc
  | fuel + 1, n, acc =>
      if n = 0 then acc else reverseFuel fuel (n / 10) (10 * acc + n % 10)

/-- A budget at least n suffices to consume all of n's decimal digits. -/
theorem reverseFuel_correct (fuel n acc : Nat) (h : n ≤ fuel) :
    reverseFuel fuel n acc = reverseAux n acc := by
  induction fuel generalizing n acc with
  | zero =>
    have hn : n = 0 := by omega
    subst n
    simp [reverseFuel, reverseAux]
  | succ fuel ih =>
    by_cases hn : n = 0
    · subst n
      simp [reverseFuel, reverseAux]
    · rw [reverseAux]
      simp only [reverseFuel, hn, ↓reduceDIte, ↓reduceIte]
      apply ih
      have hd := Nat.div_lt_self (Nat.pos_of_ne_zero hn) (by decide : 1 < 10)
      omega

def reverse10 (n : Nat) : Nat := reverseFuel n n 0

def Palindrome (n : Nat) : Prop := reverse10 n = n

instance (n : Nat) : Decidable (Palindrome n) :=
  inferInstanceAs (Decidable (reverse10 n = n))

def step (n : Nat) : Nat := n + reverse10 n

/-- The value after exactly k reverse-and-add steps from n. -/
def orbit (n : Nat) : Nat → Nat
  | 0 => n
  | k + 1 => step (orbit n k)

/-- No iterate, including the starting value, is a decimal palindrome. -/
def IsLychrel (n : Nat) : Prop :=
  ∀ k : Nat, ¬ Palindrome (orbit n k)

/-- OPEN: no theorem asserting this proposition is supplied. -/
def Decimal196Conjecture : Prop := IsLychrel 196

/-- OPEN: the weaker existence question posed on the linked page. -/
def DecimalLychrelExistence : Prop := ∃ n : Nat, IsLychrel n

theorem reverseAux_mod9 (n acc : Nat) :
    reverseAux n acc % 9 = (n + acc) % 9 := by
  induction n using Nat.strongRecOn generalizing acc with
  | ind n ih =>
    by_cases hn : n = 0
    · subst n
      simp [reverseAux]
    · rw [reverseAux]
      simp only [hn, ↓reduceDIte, ↓reduceIte]
      rw [ih (n / 10) (Nat.div_lt_self (Nat.pos_of_ne_zero hn) (by decide))]
      have hd := Nat.mod_add_div n 10
      omega

/-- Digit reversal preserves the residue modulo 9. -/
theorem reverse10_mod9 (n : Nat) : reverse10 n % 9 = n % 9 := by
  rw [reverse10, reverseFuel_correct n n 0 (Nat.le_refl n)]
  simpa using reverseAux_mod9 n 0

/-- Each reverse-and-add step doubles the residue modulo 9. -/
theorem step_mod9 (n : Nat) : step n % 9 = (2 * n) % 9 := by
  simp only [step, Nat.add_mod, reverse10_mod9, Nat.mod_mod]
  omega

theorem conjecture196_implies_existence
    (h : Decimal196Conjecture) : DecimalLychrelExistence :=
  ⟨196, h⟩

/-- A genuine induction principle. Finding such a P for 196 is unresolved. -/
theorem lychrel_of_invariant (n : Nat) (P : Nat → Prop)
    (initial : P n)
    (closed : ∀ x, P x → P (step x))
    (excludes : ∀ x, P x → ¬ Palindrome x) : IsLychrel n := by
  intro k
  apply excludes
  induction k with
  | zero => exact initial
  | succ k ih => exact closed (orbit n k) ih

theorem orbit_from_step (n k : Nat) :
    orbit (step n) k = orbit n (k + 1) := by
  induction k with
  | zero => rfl
  | succ k ih =>
    change step (orbit (step n) k) = step (orbit n (k + 1))
    rw [ih]

/-- Every later point on a Lychrel orbit is itself Lychrel. -/
theorem lychrel_step {n : Nat} (h : IsLychrel n) :
    IsLychrel (step n) := by
  intro k
  rw [orbit_from_step]
  exact h (k + 1)

/-- A terminating Boolean check of the first count states (time 0 included). -/
def noPalindromeFor : Nat → Nat → Bool
  | 0, _ => true
  | count + 1, n =>
      if reverse10 n = n then false else noPalindromeFor count (step n)

/-- Soundness of the finite checker, proved for every input and bound. -/
theorem noPalindromeFor_sound (count n : Nat)
    (h : noPalindromeFor count n = true) :
    ∀ k, k < count → ¬ Palindrome (orbit n k) := by
  induction count generalizing n with
  | zero =>
    intro k hk
    omega
  | succ count ih =>
    simp only [noPalindromeFor] at h
    split at h
    · contradiction
    · rename_i hn
      intro k hk
      cases k with
      | zero => exact hn
      | succ k =>
        have hk' : k < count := by omega
        have hnext := ih (step n) h k hk'
        rw [orbit_from_step] at hnext
        exact hnext

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem reverse_examples :
    reverse10 0 = 0 ∧ reverse10 1200 = 21 ∧ reverse10 196 = 691 := by
  decide

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem first_steps :
    orbit 196 1 = 887 ∧ orbit 196 2 = 1675 ∧ orbit 196 3 = 7436 := by
  decide

/- Carries do not prevent a palindrome: 605 + 506 = 1111. -/
set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem carry_counterexample : step 605 = 1111 ∧ Palindrome 1111 := by
  decide

/- Finite evidence only: the states at times 0 through 100. -/
set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem finite_check_196 : noPalindromeFor 101 196 = true := by
  decide

theorem no_palindrome_through_100 :
    ∀ k : Nat, k ≤ 100 → ¬ Palindrome (orbit 196 k) := by
  intro k hk
  exact noPalindromeFor_sound 101 196 finite_check_196 k (by omega)

/-
The missing goal is:

  theorem decimal196 : Decimal196Conjecture := ...

It is deliberately NOT declared: no proof was found. A finite bound cannot
replace the quantifier over all natural numbers in IsLychrel.
-/

#print axioms no_palindrome_through_100
#print axioms lychrel_of_invariant

end Lychrel196


/-!
A conditional carry lemma for decimal reverse-and-add.

`q i` represents the sum of the two input digits in mirrored positions,
`c i` the incoming carry, and `s i` the output digit.  The hypotheses
explicitly assert symmetry of both `q` and `s`, as well as zero incoming
and outgoing carries.  This file does not assert the 196 conjecture.
-/

namespace DecimalCarry

/-- If adding a symmetric sequence of digit sums produces a palindrome
without increasing its length, every carry is zero.  This purely
arithmetic lemma needs neither digit bounds nor a bound on carries. -/
theorem no_overflow_palindrome_has_no_carries
    (L : Nat) (q c s : Nat → Nat)
    (_hL : 0 < L)
    (hq : ∀ i, i < L → q i = q (L - 1 - i))
    (hs : ∀ i, i < L → s i = s (L - 1 - i))
    (hadd : ∀ i, i < L → s i + 10 * c (i + 1) = q i + c i)
    (hc0 : c 0 = 0) (hcL : c L = 0) :
    (∀ i, i ≤ L → c i = 0) ∧ (∀ i, i < L → q i = s i) := by
  have hzero : ∀ i, i ≤ L → c i = 0 ∧ c (L - i) = 0 := by
    intro i
    induction i with
    | zero =>
        intro _
        simpa using And.intro hc0 hcL
    | succ i ih =>
        intro hi
        obtain ⟨hci, hcm⟩ := ih (by omega)
        have hiLt : i < L := by omega
        let j := L - 1 - i
        have hjLt : j < L := by dsimp [j]; omega
        have hjNext : j + 1 = L - i := by dsimp [j]; omega
        have hqi : q i = q j := hq i hiLt
        have hsi : s i = s j := hs i hiLt
        have haddi := hadd i hiLt
        have haddj := hadd j hjLt
        rw [hci] at haddi
        rw [hjNext, hcm] at haddj
        have hpair : c (i + 1) = 0 ∧ c j = 0 := by omega
        have hmirror : L - (i + 1) = j := by dsimp [j]; omega
        simpa only [Nat.succ_eq_add_one, hmirror] using hpair
  constructor
  · intro i hi
    exact (hzero i hi).1
  · intro i hi
    have hci := (hzero i (by omega)).1
    have hcnext := (hzero (i + 1) (by omega)).1
    have haddi := hadd i hi
    omega

#print axioms no_overflow_palindrome_has_no_carries

/-- A local compatibility condition used when the result gains a digit. -/
theorem overflow_carry_compatibility
    (a b incoming digit q : Nat)
    (_ha : a ≤ 1) (hb : b ≤ 1) (hincoming : incoming ≤ 1)
    (hdigit : digit ≤ 9)
    (hq : q = 10 * a + b)
    (hadd : digit + 10 * b = q + incoming) :
    a = b ∧ q = 11 * a := by
  omega

/-- If decimal addition of symmetric digit sums gains one digit and its
output is palindromic, the outer digit sum is 11 and every digit sum is
either 0 or 11.  `s 0 = 1` expresses equality with the leading carry. -/
theorem overflow_palindrome_digit_sums
    (L : Nat) (q c s : Nat → Nat)
    (hL : 0 < L)
    (hq : ∀ i, i < L → q i = q (L - 1 - i))
    (hs : ∀ i, 0 < i → i < L → s i = s (L - i))
    (hadd : ∀ i, i < L → s i + 10 * c (i + 1) = q i + c i)
    (hcarry : ∀ i, i ≤ L → c i ≤ 1)
    (hdigit : ∀ i, i < L → s i ≤ 9)
    (hc0 : c 0 = 0) (hcL : c L = 1) (hs0 : s 0 = 1) :
    q 0 = 11 ∧ (∀ i, i < L → q i = 0 ∨ q i = 11) := by
  have hlast : L - 1 < L := by omega
  have hlastNext : L - 1 + 1 = L := by omega
  have hq0 := hq 0 hL
  simp only [Nat.sub_zero] at hq0
  have hadd0 := hadd 0 hL
  simp only [Nat.zero_add] at hadd0
  have haddLast := hadd (L - 1) hlast
  rw [hlastNext, hcL] at haddLast
  have hc1 := hcarry 1 (by omega)
  have hcLast := hcarry (L - 1) (by omega)
  have hbase : q 0 = 11 ∧ c 1 = 1 := by omega
  have hchain : ∀ i, i < L →
      q i = 11 * c (i + 1) ∧ c (i + 1) = c (L - i) := by
    intro i
    induction i with
    | zero =>
        intro _
        simp [hbase.1, hbase.2, hcL]
    | succ i ih =>
        intro hi
        have hiLt : i < L := by omega
        obtain ⟨hqi, hci⟩ := ih hiLt
        let t := i + 1
        have htPos : 0 < t := by dsimp [t]; omega
        have htLt : t < L := by dsimp [t]; omega
        have hmLt : L - t < L := by omega
        have hqMirror : q (L - t) = q i := by
          have h := hq i hiLt
          have heq : L - 1 - i = L - t := by dsimp [t]; omega
          rw [heq] at h
          exact h.symm
        have hcMirror : c (L - t + 1) = c t := by
          have heq : L - t + 1 = L - i := by dsimp [t]; omega
          rw [heq]
          exact hci.symm
        have haddt := hadd t htLt
        have haddm := hadd (L - t) hmLt
        rw [hqMirror, hcMirror] at haddm
        have hpals := hs t htPos htLt
        have hqt : q t = 10 * c (t + 1) + c (L - t) := by
          change q i = 11 * c t at hqi
          omega
        let j := L - 1 - t
        have hjLt : j < L := by dsimp [j]; omega
        have hjNext : j + 1 = L - t := by dsimp [j]; omega
        have hqtj : q t = q j := hq t htLt
        have haddj := hadd j hjLt
        rw [hjNext, ← hqtj] at haddj
        obtain ⟨hcarryEq, hsum⟩ := overflow_carry_compatibility
          (c (t + 1)) (c (L - t)) (c j) (s j) (q t)
          (hcarry _ (by omega)) (hcarry _ (by omega))
          (hcarry _ (by omega)) (hdigit j hjLt) hqt haddj
        change q t = 11 * c (t + 1) ∧ c (t + 1) = c (L - t)
        exact ⟨hsum, hcarryEq⟩
  constructor
  · exact hbase.1
  · intro i hi
    obtain ⟨hqi, _⟩ := hchain i hi
    have hc := hcarry (i + 1) (by omega)
    omega

#print axioms overflow_palindrome_digit_sums

/-- If every mirrored digit sum is at most nine, addition has no carries
and its output digits are symmetric. -/
theorem small_digit_sums_give_palindrome
    (L : Nat) (q c s : Nat → Nat)
    (hq : ∀ i, i < L → q i = q (L - 1 - i))
    (hsmall : ∀ i, i < L → q i ≤ 9)
    (hadd : ∀ i, i < L → s i + 10 * c (i + 1) = q i + c i)
    (hc0 : c 0 = 0) :
    (∀ i, i ≤ L → c i = 0) ∧
    (∀ i, i < L → s i = s (L - 1 - i)) := by
  have hzero : ∀ i, i ≤ L → c i = 0 := by
    intro i
    induction i with
    | zero => intro _; exact hc0
    | succ i ih =>
        intro hi
        have hiLt : i < L := by omega
        have hci := ih (by omega)
        have haddi := hadd i hiLt
        have hqi := hsmall i hiLt
        have hnext : c (i + 1) = 0 := by omega
        exact hnext
  constructor
  · exact hzero
  · intro i hi
    let j := L - 1 - i
    have hj : j < L := by dsimp [j]; omega
    have hqi : q i = q j := hq i hi
    have haddi := hadd i hi
    have haddj := hadd j hj
    have hci := hzero i (by omega)
    have hciNext := hzero (i + 1) (by omega)
    have hcj := hzero j (by omega)
    have hcjNext := hzero (j + 1) (by omega)
    change s i = s j
    omega

/-- The converse overflow criterion, expressed in the same local
digit-and-carry representation as the necessity theorem. -/
theorem zero_or_eleven_digit_sums_give_palindrome
    (L : Nat) (q c s : Nat → Nat)
    (hL : 0 < L)
    (hq : ∀ i, i < L → q i = q (L - 1 - i))
    (hvalues : ∀ i, i < L → q i = 0 ∨ q i = 11)
    (hq0 : q 0 = 11)
    (hadd : ∀ i, i < L → s i + 10 * c (i + 1) = q i + c i)
    (hcarry : ∀ i, i ≤ L → c i ≤ 1)
    (hdigit : ∀ i, i < L → s i ≤ 9)
    (hc0 : c 0 = 0) :
    c L = 1 ∧ s 0 = 1 ∧ (∀ i, 0 < i → i < L → s i = s (L - i)) := by
  have hlocal : ∀ i, i < L →
      q i = 11 * c (i + 1) ∧ s i = c i + c (i + 1) := by
    intro i hi
    have hv := hvalues i hi
    have hc := hcarry i (by omega)
    have hd := hdigit i hi
    have ha := hadd i hi
    omega
  have hsymcarry : ∀ i, i < L → c (i + 1) = c (L - i) := by
    intro i hi
    let j := L - 1 - i
    have hj : j < L := by dsimp [j]; omega
    have hjNext : j + 1 = L - i := by dsimp [j]; omega
    have hqi : q i = q j := hq i hi
    have hiLocal := (hlocal i hi).1
    have hjLocal := (hlocal j hj).1
    rw [hjNext] at hjLocal
    omega
  have hlocal0 := hlocal 0 hL
  simp only [Nat.zero_add] at hlocal0
  have hsym0 := hsymcarry 0 hL
  simp only [Nat.zero_add, Nat.sub_zero] at hsym0
  have hcL : c L = 1 := by omega
  have hs0 : s 0 = 1 := by omega
  refine ⟨hcL, hs0, ?_⟩
  intro i hiPos hi
  have hm : L - i < L := by omega
  have hleft := (hlocal i hi).2
  have hright := (hlocal (L - i) hm).2
  have hout := hsymcarry i hi
  have hin := hsymcarry (i - 1) (by omega)
  have hiPrev : i - 1 + 1 = i := by omega
  have hmPrev : L - (i - 1) = L - i + 1 := by omega
  rw [hiPrev, hmPrev] at hin
  omega

#print axioms small_digit_sums_give_palindrome
#print axioms zero_or_eleven_digit_sums_give_palindrome

end DecimalCarry


/-!
# Concrete decimal digits and verified column addition

The carry sequence and output digits below are *computed* from the input
numeral. Consequently their local equations and bounds are theorems, not
assumptions about a proposed addition algorithm.

Digit position zero is the units position. `value d L` interprets exactly
L base-ten digits; `reflected d L` reverses those L positions. Leading zeros
are permitted by this representation.
-/

namespace DecimalDigits

/-- The natural number represented by the first L least-significant-first digits. -/
def value (d : Nat → Nat) : Nat → Nat
  | 0 => 0
  | L + 1 => value d L + d L * 10 ^ L

/-- Reflection within a fixed-width decimal numeral. -/
def reflected (d : Nat → Nat) (L : Nat) (i : Nat) : Nat :=
  d (L - 1 - i)

/-- The actual sum of the two input digits in a column. -/
def columnSum (d : Nat → Nat) (L : Nat) (i : Nat) : Nat :=
  d i + reflected d L i

/-- The incoming carry, calculated recursively by ordinary decimal addition. -/
def carry (q : Nat → Nat) : Nat → Nat
  | 0 => 0
  | i + 1 => (q i + carry q i) / 10

/-- The actual result digit in each column. -/
def output (q : Nat → Nat) (i : Nat) : Nat :=
  (q i + carry q i) % 10

theorem columnSum_symmetric (d : Nat → Nat) (L i : Nat) (hi : i < L) :
    columnSum d L i = columnSum d L (L - 1 - i) := by
  have h : L - 1 - (L - 1 - i) = i := by omega
  simp only [columnSum, reflected, h]
  omega

theorem columnSum_bounded (d : Nat → Nat) (L : Nat)
    (hd : ∀ i, i < L → d i ≤ 9) :
    ∀ i, i < L → columnSum d L i ≤ 18 := by
  intro i hi
  have ha := hd i hi
  have hb := hd (L - 1 - i) (by omega)
  simp only [columnSum, reflected]
  omega

theorem column_equation (q : Nat → Nat) (i : Nat) :
    output q i + 10 * carry q (i + 1) = q i + carry q i := by
  simp only [output, carry]
  exact Nat.mod_add_div _ _

theorem carry_bounded (q : Nat → Nat) (L : Nat)
    (hq : ∀ i, i < L → q i ≤ 18) :
    ∀ i, i ≤ L → carry q i ≤ 1 := by
  intro i
  induction i with
  | zero => intro _; simp [carry]
  | succ i ih =>
    intro hi
    have hc := ih (by omega)
    have hqi := hq i (by omega)
    simp only [carry]
    omega

theorem output_bounded (q : Nat → Nat) (i : Nat) : output q i ≤ 9 := by
  simp only [output]
  omega

/-- Evaluation respects pointwise digit addition, even before carrying. -/
theorem value_add (a b : Nat → Nat) (L : Nat) :
    value (fun i => a i + b i) L = value a L + value b L := by
  induction L with
  | zero => simp [value]
  | succ L ih =>
    simp only [value, ih, Nat.add_mul]
    omega

/-- The column algorithm computes the sum as a natural number. The final
carry is accounted for as one more leading digit. -/
theorem value_output (q : Nat → Nat) (L : Nat) :
    value (output q) L + carry q L * 10 ^ L = value q L := by
  induction L with
  | zero => simp [value, carry]
  | succ L ih =>
    have h := congrArg (fun x => x * 10 ^ L) (column_equation q L)
    simp only [Nat.add_mul] at h
    simp only [value, Nat.pow_succ]
    have hc : carry q (L + 1) * (10 ^ L * 10) =
        10 * carry q (L + 1) * 10 ^ L := by
      simp [Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc]
    rw [hc]
    omega

/-- An exact numeric reverse-and-add identity for any finite decimal numeral. -/
theorem reverse_add_value (d : Nat → Nat) (L : Nat) :
    value (output (columnSum d L)) L + carry (columnSum d L) L * 10 ^ L =
      value d L + value (reflected d L) L := by
  rw [value_output]
  exact value_add d (reflected d L) L

/-- The no-overflow palindrome criterion for the concrete computed digits. -/
theorem no_overflow_palindrome_iff (d : Nat → Nat) (L : Nat)
    (hL : 0 < L) (_hd : ∀ i, i < L → d i ≤ 9) :
    (carry (columnSum d L) L = 0 ∧
      ∀ i, i < L → output (columnSum d L) i =
        output (columnSum d L) (L - 1 - i)) ↔
    (∀ i, i < L → columnSum d L i ≤ 9) := by
  let q := columnSum d L
  have hq : ∀ i, i < L → q i = q (L - 1 - i) :=
    columnSum_symmetric d L
  constructor
  · intro ⟨hcL, hs⟩
    obtain ⟨_, heq⟩ := DecimalCarry.no_overflow_palindrome_has_no_carries
      L q (carry q) (output q) hL hq hs
      (fun i _ => column_equation q i) rfl hcL
    intro i hi
    change q i ≤ 9
    rw [heq i hi]
    exact output_bounded q i
  · intro hsmall
    obtain ⟨hc, hs⟩ := DecimalCarry.small_digit_sums_give_palindrome
      L q (carry q) (output q) hq hsmall
      (fun i _ => column_equation q i) rfl
    exact ⟨hc L (Nat.le_refl L), hs⟩

/-- The overflow palindrome criterion for the concrete computed digits. -/
theorem overflow_palindrome_iff (d : Nat → Nat) (L : Nat)
    (hL : 0 < L) (hd : ∀ i, i < L → d i ≤ 9) :
    (carry (columnSum d L) L = 1 ∧ output (columnSum d L) 0 = 1 ∧
      ∀ i, 0 < i → i < L → output (columnSum d L) i =
        output (columnSum d L) (L - i)) ↔
    (columnSum d L 0 = 11 ∧
      ∀ i, i < L → columnSum d L i = 0 ∨ columnSum d L i = 11) := by
  let q := columnSum d L
  have hq : ∀ i, i < L → q i = q (L - 1 - i) :=
    columnSum_symmetric d L
  have hc := carry_bounded q L (columnSum_bounded d L hd)
  constructor
  · intro ⟨hcL, hs0, hs⟩
    exact DecimalCarry.overflow_palindrome_digit_sums
      L q (carry q) (output q) hL hq hs
      (fun i _ => column_equation q i) hc
      (fun i _ => output_bounded q i) rfl hcL hs0
  · intro ⟨hq0, hvalues⟩
    exact DecimalCarry.zero_or_eleven_digit_sums_give_palindrome
      L q (carry q) (output q) hL hq hvalues hq0
      (fun i _ => column_equation q i) hc
      (fun i _ => output_bounded q i) rfl

#print axioms reverse_add_value
#print axioms no_overflow_palindrome_iff
#print axioms overflow_palindrome_iff

/-- Equality of all used positions implies equality of numeral values. -/
theorem value_congr (a b : Nat → Nat) (L : Nat)
    (h : ∀ i, i < L → a i = b i) : value a L = value b L := by
  induction L with
  | zero => rfl
  | succ L ih =>
    simp only [value, ih (fun i hi => h i (by omega)), h L (by omega)]

/-- Split a decimal numeral into its units digit and its remaining digits. -/
theorem value_shift (d : Nat → Nat) (L : Nat) :
    value d (L + 1) = d 0 + 10 * value (fun i => d (i + 1)) L := by
  induction L with
  | zero => simp [value]
  | succ L ih =>
    simp only [value, Nat.pow_succ] at ih ⊢
    have hmul : d (L + 1) * (10 ^ L * 10) =
        10 * (d (L + 1) * 10 ^ L) := by
      simp [Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc]
    rw [Nat.mul_add, hmul]
    omega

/-- Splitting the reflection exposes the original units digit at the top. -/
theorem reflected_value_shift (d : Nat → Nat) (L : Nat) :
    value (reflected d (L + 1)) (L + 1) =
      value (reflected (fun i => d (i + 1)) L) L + d 0 * 10 ^ L := by
  simp only [value]
  have h : value (reflected d (L + 1)) L =
      value (reflected (fun i => d (i + 1)) L) L := by
    apply value_congr
    intro i hi
    simp only [reflected]
    congr 1
    omega
  rw [h]
  simp [reflected]

/-- A nonzero leading digit makes a nonempty numeral positive. -/
theorem value_positive (d : Nat → Nat) (L : Nat)
    (hL : 0 < L) (hlead : 0 < d (L - 1)) : 0 < value d L := by
  obtain ⟨k, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : L ≠ 0)
  simp only [value, Nat.add_sub_cancel] at hlead ⊢
  have hp : 0 < 10 ^ k := Nat.pow_pos (by decide)
  have hlead2 : 0 < d k := by simpa using hlead
  have hm := Nat.mul_pos hlead2 hp
  omega

/-- Exact connection to the independent decimal-reversal algorithm.
The last digit must be nonzero, so the input has its claimed width. -/
theorem reverseAux_value (d : Nat → Nat) (L acc : Nat)
    (hd : ∀ i, i < L → d i ≤ 9)
    (hlead : L = 0 ∨ 0 < d (L - 1)) :
    Lychrel196.reverseAux (value d L) acc =
      acc * 10 ^ L + value (reflected d L) L := by
  induction L generalizing d acc with
  | zero => simp [value, Lychrel196.reverseAux]
  | succ L ih =>
    have hd0 := hd 0 (by omega)
    have hlead' : 0 < d L := by simpa using hlead
    have hpos := value_positive d (L + 1) (by omega) (by simpa using hlead')
    have hmod : value d (L + 1) % 10 = d 0 := by
      rw [value_shift]
      omega
    have hdiv : value d (L + 1) / 10 = value (fun i => d (i + 1)) L := by
      rw [value_shift]
      omega
    rw [Lychrel196.reverseAux]
    simp only [Nat.ne_of_gt hpos, ↓reduceDIte, ↓reduceIte, hmod, hdiv]
    rw [ih]
    · rw [reflected_value_shift, Nat.pow_succ, Nat.add_mul]
      have hmul : 10 * acc * 10 ^ L = acc * (10 ^ L * 10) := by
        simp [Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc]
      rw [hmul]
      omega
    · intro i hi
      apply hd
      omega
    · by_cases h : L = 0
      · exact Or.inl h
      · right
        have : L - 1 + 1 = L := by omega
        simpa only [this] using hlead'

/-- Canonical positional reflection agrees with actual natural-number reversal. -/
theorem reverse10_value (d : Nat → Nat) (L : Nat)
    (hd : ∀ i, i < L → d i ≤ 9)
    (hlead : L = 0 ∨ 0 < d (L - 1)) :
    Lychrel196.reverse10 (value d L) = value (reflected d L) L := by
  rw [Lychrel196.reverse10, Lychrel196.reverseFuel_correct _ _ _ (Nat.le_refl _)]
  simpa using reverseAux_value d L 0 hd hlead

/-- Concrete column addition computes the actual reverse-and-add map used
in the decimal 196 conjecture, rather than an unrelated digit process. -/
theorem step_value (d : Nat → Nat) (L : Nat)
    (hd : ∀ i, i < L → d i ≤ 9)
    (hlead : L = 0 ∨ 0 < d (L - 1)) :
    Lychrel196.step (value d L) =
      value (output (columnSum d L)) L + carry (columnSum d L) L * 10 ^ L := by
  rw [Lychrel196.step, reverse10_value d L hd hlead]
  exact (reverse_add_value d L).symm

#print axioms reverse10_value
#print axioms step_value

/-- Bounded decimal digits are uniquely determined by a fixed-width value. -/
theorem value_injective (a b : Nat → Nat) (L : Nat)
    (ha : ∀ i, i < L → a i ≤ 9) (hb : ∀ i, i < L → b i ≤ 9)
    (heq : value a L = value b L) : ∀ i, i < L → a i = b i := by
  induction L generalizing a b with
  | zero => intro i hi; omega
  | succ L ih =>
    have ha0 := ha 0 (by omega)
    have hb0 := hb 0 (by omega)
    rw [value_shift, value_shift] at heq
    have hz : a 0 = b 0 := by omega
    have ht : value (fun i => a (i + 1)) L = value (fun i => b (i + 1)) L := by omega
    intro i hi
    cases i with
    | zero => exact hz
    | succ i =>
      apply ih (fun j => a (j + 1)) (fun j => b (j + 1))
        (fun j hj => ha (j + 1) (by omega))
        (fun j hj => hb (j + 1) (by omega)) ht i (by omega)

/-- Natural-number palindromicity is exactly symmetry of canonical digits. -/
theorem palindrome_value_iff (d : Nat → Nat) (L : Nat)
    (hd : ∀ i, i < L → d i ≤ 9)
    (hlead : L = 0 ∨ 0 < d (L - 1)) :
    Lychrel196.Palindrome (value d L) ↔
      ∀ i, i < L → d i = d (L - 1 - i) := by
  unfold Lychrel196.Palindrome
  rw [reverse10_value d L hd hlead]
  constructor
  · intro h
    exact value_injective d (reflected d L) L hd
      (fun i hi => hd (L - 1 - i) (by omega)) h.symm
  · intro h
    exact (value_congr d (reflected d L) L h).symm

/-- In the no-overflow case the computed result retains a nonzero leading digit. -/
theorem output_leading_positive (d : Nat → Nat) (L : Nat)
    (hL : 0 < L) (hlead : 0 < d (L - 1))
    (hc : carry (columnSum d L) L = 0) :
    0 < output (columnSum d L) (L - 1) := by
  have h := column_equation (columnSum d L) (L - 1)
  have heq : L - 1 + 1 = L := by omega
  rw [heq, hc] at h
  simp only [columnSum, reflected] at h
  omega

/-- Exact non-overflow criterion stated for the natural-number step. -/
theorem step_palindrome_iff_no_overflow (d : Nat → Nat) (L : Nat)
    (hL : 0 < L) (hd : ∀ i, i < L → d i ≤ 9)
    (hlead : 0 < d (L - 1))
    (hc : carry (columnSum d L) L = 0) :
    Lychrel196.Palindrome (Lychrel196.step (value d L)) ↔
      ∀ i, i < L → columnSum d L i ≤ 9 := by
  rw [step_value d L hd (Or.inr hlead), hc]
  simp only [Nat.zero_mul, Nat.add_zero]
  rw [palindrome_value_iff (output (columnSum d L)) L
    (fun i _ => output_bounded _ i)
    (Or.inr (output_leading_positive d L hL hlead hc))]
  exact (and_iff_right hc).symm.trans (no_overflow_palindrome_iff d L hL hd)

/-- Extend the computed result with its final carry as a leading digit. -/
def extended (q : Nat → Nat) (L i : Nat) : Nat :=
  if i < L then output q i else carry q L

theorem value_extended (q : Nat → Nat) (L : Nat) :
    value (extended q L) (L + 1) =
      value (output q) L + carry q L * 10 ^ L := by
  simp only [value]
  have h : value (extended q L) L = value (output q) L := by
    apply value_congr
    intro i hi
    simp [extended, hi]
  rw [h]
  simp [extended]

theorem extended_symmetry_iff (q : Nat → Nat) (L : Nat)
    (hL : 0 < L) (hc : carry q L = 1) :
    (∀ i, i < L + 1 → extended q L i = extended q L (L + 1 - 1 - i)) ↔
    (output q 0 = 1 ∧ ∀ i, 0 < i → i < L → output q i = output q (L - i)) := by
  simp only [Nat.add_sub_cancel]
  constructor
  · intro hs
    constructor
    · have h := hs 0 (by omega)
      simpa [extended, hL, hc] using h
    · intro i hi0 hi
      have h := hs i (by omega)
      have hm : L - i < L := by omega
      simpa [extended, hi, hm] using h
  · intro ⟨hzero, hmiddle⟩ i hi
    by_cases hz : i = 0
    · subst i
      simp [extended, hL, hc, hzero]
    by_cases hl : i = L
    · subst i
      simp [extended, hL, hc, hzero]
    · have hiL : i < L := by omega
      have hm : L - i < L := by omega
      simpa [extended, hiL, hm] using hmiddle i (by omega) hiL

/-- Exact overflow criterion stated for the natural-number step. -/
theorem step_palindrome_iff_overflow (d : Nat → Nat) (L : Nat)
    (hL : 0 < L) (hd : ∀ i, i < L → d i ≤ 9)
    (hlead : 0 < d (L - 1))
    (hc : carry (columnSum d L) L = 1) :
    Lychrel196.Palindrome (Lychrel196.step (value d L)) ↔
      (columnSum d L 0 = 11 ∧
        ∀ i, i < L → columnSum d L i = 0 ∨ columnSum d L i = 11) := by
  rw [step_value d L hd (Or.inr hlead), ← value_extended]
  have heBound : ∀ i, i < L + 1 → extended (columnSum d L) L i ≤ 9 := by
    intro i _
    unfold extended
    split
    · exact output_bounded _ _
    · omega
  have heLead : 0 < extended (columnSum d L) L (L + 1 - 1) := by
    simp [extended, hc]
  rw [palindrome_value_iff _ _ heBound (Or.inr heLead)]
  rw [extended_symmetry_iff _ _ hL hc]
  exact (and_iff_right hc).symm.trans (overflow_palindrome_iff d L hL hd)

/-- Complete one-step criterion for the actual natural-number reverse-and-add map.
This says when a *single step* is palindromic. It does not claim that the
criterion is ever or never satisfied along the entire orbit of 196. -/
theorem step_palindrome_iff (d : Nat → Nat) (L : Nat)
    (hL : 0 < L) (hd : ∀ i, i < L → d i ≤ 9)
    (hlead : 0 < d (L - 1)) :
    Lychrel196.Palindrome (Lychrel196.step (value d L)) ↔
      (∀ i, i < L → columnSum d L i ≤ 9) ∨
      (columnSum d L 0 = 11 ∧
        ∀ i, i < L → columnSum d L i = 0 ∨ columnSum d L i = 11) := by
  have hbound := carry_bounded (columnSum d L) L (columnSum_bounded d L hd) L (by omega)
  constructor
  · intro hp
    by_cases hc : carry (columnSum d L) L = 0
    · exact Or.inl ((step_palindrome_iff_no_overflow d L hL hd hlead hc).mp hp)
    · have hc1 : carry (columnSum d L) L = 1 := by omega
      exact Or.inr ((step_palindrome_iff_overflow d L hL hd hlead hc1).mp hp)
  · intro h
    rcases h with hs | ho
    · have hc := ((no_overflow_palindrome_iff d L hL hd).mpr hs).1
      exact (step_palindrome_iff_no_overflow d L hL hd hlead hc).mpr hs
    · have hc := ((overflow_palindrome_iff d L hL hd).mpr ho).1
      exact (step_palindrome_iff_overflow d L hL hd hlead hc).mpr ho

#print axioms step_palindrome_iff

/-- A canonical decimal representation of a positive natural number. -/
def Canonical (n : Nat) (d : Nat → Nat) (L : Nat) : Prop :=
  0 < L ∧ (∀ i, i < L → d i ≤ 9) ∧ 0 < d (L - 1) ∧ value d L = n

/-- Every positive natural number has bounded decimal digits with a nonzero lead. -/
theorem canonical_exists (n : Nat) (hn : 0 < n) :
    ∃ d L, Canonical n d L := by
  induction n using Nat.strongRecOn with
  | ind n ih =>
    by_cases hsmall : n < 10
    · refine ⟨(fun _ => n), 1, by decide, ?_, ?_, ?_⟩
      · intro i hi
        change n ≤ 9
        omega
      · simpa using hn
      · simp [value]
    · have hquot : 0 < n / 10 := by omega
      have hlt := Nat.div_lt_self hn (by decide : 1 < 10)
      obtain ⟨d, L, hL, hd, hlead, hv⟩ := ih (n / 10) hlt hquot
      let e : Nat → Nat := fun i => match i with
        | 0 => n % 10
        | j + 1 => d j
      refine ⟨e, L + 1, by omega, ?_, ?_, ?_⟩
      · intro i hi
        cases i with
        | zero => dsimp [e]; omega
        | succ j => exact hd j (by omega)
      · have : e L = d (L - 1) := by
          cases L with
          | zero => omega
          | succ k => simp [e]
        simpa only [Nat.add_sub_cancel, this] using hlead
      · rw [value_shift]
        change n % 10 + 10 * value d L = n
        rw [hv]
        exact Nat.mod_add_div n 10

/-- The two and only two digit patterns whose next reverse-and-add step
is palindromic. Existence includes the canonical representation explicitly. -/
def PalindromePredecessor (n : Nat) : Prop :=
  ∃ d L, Canonical n d L ∧
    ((∀ i, i < L → columnSum d L i ≤ 9) ∨
      (columnSum d L 0 = 11 ∧
        ∀ i, i < L → columnSum d L i = 0 ∨ columnSum d L i = 11))

/-- The forbidden-pattern predicate is equivalent to an actual next-step
palindrome for every positive natural number. -/
theorem palindromePredecessor_iff (n : Nat) (hn : 0 < n) :
    PalindromePredecessor n ↔ Lychrel196.Palindrome (Lychrel196.step n) := by
  constructor
  · rintro ⟨d, L, ⟨hL, hd, hlead, hv⟩, hpattern⟩
    rw [← hv]
    exact (step_palindrome_iff d L hL hd hlead).mpr hpattern
  · intro hp
    obtain ⟨d, L, hcan⟩ := canonical_exists n hn
    refine ⟨d, L, hcan, ?_⟩
    obtain ⟨hL, hd, hlead, hv⟩ := hcan
    rw [← hv] at hp
    exact (step_palindrome_iff d L hL hd hlead).mp hp

theorem orbit_positive (n : Nat) (hn : 0 < n) (k : Nat) :
    0 < Lychrel196.orbit n k := by
  induction k with
  | zero => exact hn
  | succ k ih =>
    change 0 < Lychrel196.orbit n k + Lychrel196.reverse10 (Lychrel196.orbit n k)
    omega

/-- Exact global reduction, with the unresolved infinite quantifier intact. -/
theorem isLychrel_iff_avoids_predecessors (n : Nat) (hn : 0 < n) :
    Lychrel196.IsLychrel n ↔
      (¬ Lychrel196.Palindrome n ∧
        ∀ k, ¬ PalindromePredecessor (Lychrel196.orbit n k)) := by
  constructor
  · intro h
    refine ⟨h 0, ?_⟩
    intro k hk
    have hp := (palindromePredecessor_iff _ (orbit_positive n hn k)).mp hk
    exact h (k + 1) hp
  · rintro ⟨hzero, havoid⟩ k
    cases k with
    | zero => exact hzero
    | succ k =>
      intro hp
      exact havoid k ((palindromePredecessor_iff _ (orbit_positive n hn k)).mpr hp)

/-- The missing result is precisely that every 196 orbit state avoids
both predecessor patterns. This is a proved equivalence, not a proof of
its right-hand side or a solution of the decimal 196 conjecture. -/
theorem conjecture196_iff_avoids_predecessors :
    Lychrel196.Decimal196Conjecture ↔
      ∀ k, ¬ PalindromePredecessor (Lychrel196.orbit 196 k) := by
  have hnot : ¬ Lychrel196.Palindrome 196 := by
    change Lychrel196.reverse10 196 ≠ 196
    have h := Lychrel196.reverse_examples.2.2
    omega
  exact (isLychrel_iff_avoids_predecessors 196 (by decide)).trans (and_iff_right hnot)

#print axioms canonical_exists
#print axioms conjecture196_iff_avoids_predecessors

end DecimalDigits


/-!
# Conditional certificates for decimal Lychrel numbers

This file proves soundness of a possible proof method. It supplies NO
certificate witness, and it does NOT prove decimal Lychrel existence.

A certificate describes whole finite blocks of an infinite orbit. Its
state type may be a natural-number parameter, a tuple, or a finite graph
state paired with growth parameters. Block lengths may vary with state.
The hypotheses must hold for every valid state, not merely a finite set
of tested values.

This section is included in the standalone file. Check the whole file with:
  lean Lychrel196Research.lean
-/

namespace LychrelCertificates

open Lychrel196

/-- Splitting an orbit into two successive time intervals. -/
theorem orbit_add (n a b : Nat) :
    orbit n (a + b) = orbit (orbit n a) b := by
  induction b with
  | zero => simp [orbit]
  | succ b ih =>
    change step (orbit n (a + b)) = step (orbit (orbit n a) b)
    rw [ih]

/-- A verified block description. No instance is constructed in this file. -/
structure BlockCertificate (State : Type) where
  /-- Decode an abstract state as an actual decimal natural number. -/
  value : State → Nat
  /-- Select the state reached after one entire block. -/
  next : State → State
  /-- Positive number of actual reverse-and-add steps in that block. -/
  length : State → Nat
  /-- Which states satisfy the symbolic invariant. -/
  valid : State → Prop
  valid_next : ∀ s, valid s → valid (next s)
  length_pos : ∀ s, valid s → 0 < length s
  /-- Every state in a block, including its starting point, is nonpalindromic. -/
  avoids : ∀ s, valid s → ∀ j, j < length s →
    ¬ Palindrome (orbit (value s) j)
  /-- Exact equality of the full natural numbers at the block boundary. -/
  closes : ∀ s, valid s → orbit (value s) (length s) = value (next s)

/-- Soundness of arbitrary positive-length block certificates. -/
theorem BlockCertificate.sound {State : Type} (C : BlockCertificate State)
    (s : State) (hs : C.valid s) : IsLychrel (C.value s) := by
  intro k
  induction k using Nat.strongRecOn generalizing s with
  | ind k ih =>
    by_cases hshort : k < C.length s
    · exact C.avoids s hs k hshort
    · have hp := C.length_pos s hs
      have hreduce : k - C.length s < k := by omega
      have hsplit : C.length s + (k - C.length s) = k := by omega
      have hlater := ih (k - C.length s) hreduce (C.next s) (C.valid_next s hs)
      rw [← C.closes s hs, ← orbit_add, hsplit] at hlater
      exact hlater

/-- A single valid state in a proved certificate implies decimal existence. -/
theorem BlockCertificate.implies_existence {State : Type}
    (C : BlockCertificate State) (s : State) (hs : C.valid s) :
    DecimalLychrelExistence :=
  ⟨C.value s, C.sound s hs⟩

/-- Fixed-block families are a special case. The shift may be arbitrary;
strict growth is not needed for the logical soundness argument. -/
theorem lychrel_of_shifted_family (F : Nat → Nat) (p g : Nat)
    (hp : 0 < p)
    (havoid : ∀ N j, j < p → ¬ Palindrome (orbit (F N) j))
    (hclose : ∀ N, orbit (F N) p = F (N + g)) :
    ∀ N, IsLychrel (F N) := by
  let C : BlockCertificate Nat := {
    value := F
    next := fun N => N + g
    length := fun _ => p
    valid := fun _ => True
    valid_next := fun _ _ => True.intro
    length_pos := fun _ _ => hp
    avoids := fun N _ j hj => havoid N j hj
    closes := fun N _ => hclose N
  }
  intro N
  exact C.sound N True.intro

/-- An expanding family with p>0 and g>0 yields Lychrel numbers and
existence, if its universal safety and transition obligations are proved. -/
theorem expanding_family_certificate (F : Nat → Nat) (p g : Nat)
    (hp : 0 < p) (_hg : 0 < g)
    (havoid : ∀ N j, j < p → ¬ Palindrome (orbit (F N) j))
    (hclose : ∀ N, orbit (F N) p = F (N + g)) :
    (∀ N, IsLychrel (F N)) ∧ DecimalLychrelExistence := by
  have h := lychrel_of_shifted_family F p g hp havoid hclose
  exact ⟨h, F 0, h 0⟩

/-- Safe finite entry into a certified family also certifies the initial
number. This prevents the unsound omission of an early palindrome. -/
theorem lychrel_of_entry {State : Type} (C : BlockCertificate State)
    (n t : Nat) (s : State) (hs : C.valid s)
    (hprefix : ∀ j, j < t → ¬ Palindrome (orbit n j))
    (hentry : orbit n t = C.value s) : IsLychrel n := by
  intro k
  by_cases hshort : k < t
  · exact hprefix k hshort
  · have hsplit : t + (k - t) = k := by omega
    have htail := C.sound s hs (k - t)
    rw [← hentry, ← orbit_add, hsplit] at htail
    exact htail

/-- The exact additional obligations sufficient to prove the 196 conjecture.
No certificate or entry proof satisfying these obligations is provided. -/
theorem conjecture196_of_entry {State : Type} (C : BlockCertificate State)
    (t : Nat) (s : State) (hs : C.valid s)
    (hprefix : ∀ j, j < t → ¬ Palindrome (orbit 196 j))
    (hentry : orbit 196 t = C.value s) : Decimal196Conjecture :=
  lychrel_of_entry C 196 t s hs hprefix hentry

#print axioms BlockCertificate.sound
#print axioms expanding_family_certificate
#print axioms conjecture196_of_entry

end LychrelCertificates


/-!
# Exact folded-column dynamics of decimal reverse-and-add

This file proves arithmetic semantics for the finite transducer used in
the accompanying research. It does not supply an invariant language or
prove decimal Lychrel existence. Digits and columns are indexed from the
least significant end. The folded input reads symmetric column sums from
the ends towards the center.
-/

namespace FoldedDecimal

open DecimalDigits

/-- The next column-sum word, with the actual overflow-dependent width. -/
def nextColumns (q : Nat → Nat) (L : Nat) (i : Nat) : Nat :=
  if carry q L = 0 then columnSum (output q) L i
  else columnSum (extended q L) (L + 1) i

/-- In the no-overflow case the computed digits form the canonical
representation of the actual numeric reverse-and-add step. -/
theorem canonical_next_no_overflow (n : Nat) (d : Nat → Nat) (L : Nat)
    (h : Canonical n d L) (hc : carry (columnSum d L) L = 0) :
    Canonical (Lychrel196.step n) (output (columnSum d L)) L := by
  rcases h with ⟨hL, hd, hlead, hn⟩
  refine ⟨hL, fun i _ => output_bounded _ i,
    output_leading_positive d L hL hlead hc, ?_⟩
  rw [← hn, step_value d L hd (Or.inr hlead), hc]
  simp

/-- In the overflow case the appended carry is the nonzero leading digit
of the actual numeric step. -/
theorem canonical_next_overflow (n : Nat) (d : Nat → Nat) (L : Nat)
    (h : Canonical n d L) (hc : carry (columnSum d L) L = 1) :
    Canonical (Lychrel196.step n) (extended (columnSum d L) L) (L + 1) := by
  rcases h with ⟨hL, hd, hlead, hn⟩
  refine ⟨by omega, ?_, ?_, ?_⟩
  · intro i hi
    by_cases hil : i < L
    · simp only [extended, if_pos hil]
      exact output_bounded _ i
    · simp [extended, hil, hc]
  · simp [extended, hc]
  · rw [value_extended, ← hn, step_value d L hd (Or.inr hlead)]

/-- All genuine inputs choose exactly one of the two transition branches. -/
theorem actual_overflow_cases (d : Nat → Nat) (L : Nat)
    (hd : ∀ i, i < L → d i ≤ 9) :
    carry (columnSum d L) L = 0 ∨ carry (columnSum d L) L = 1 := by
  have hc := carry_bounded (columnSum d L) L (columnSum_bounded d L hd) L
    (Nat.le_refl L)
  omega

/-- Exact next-column equation without overflow. It is expressed without
natural-number subtraction, so the identity retains every carry term. -/
theorem next_column_no_overflow (q : Nat → Nat) (L i : Nat)
    (hi : i < L) (hs : ∀ j, j < L → q j = q (L - 1 - j))
    (hc : carry q L = 0) :
    nextColumns q L i + 10 * (carry q (i + 1) + carry q (L - i)) =
      2 * q i + carry q i + carry q (L - 1 - i) := by
  have hlow := column_equation q i
  have hhigh := column_equation q (L - 1 - i)
  have hind : L - 1 - i + 1 = L - i := by omega
  rw [hind, ← hs i hi] at hhigh
  simp only [nextColumns, hc, ite_true, columnSum, reflected]
  omega

/-- Overflow shifts the reflected alignment by one column. The new
outer pair consists of the low output digit and the appended carry 1. -/
theorem next_column_overflow_outer (q : Nat → Nat) (L : Nat)
    (hL : 0 < L) (hc : carry q L = 1) :
    nextColumns q L 0 + 10 * carry q 1 = q 0 + 1 := by
  have h := column_equation q 0
  have hc0 : carry q 0 = 0 := rfl
  rw [hc0] at h
  simp only [Nat.zero_add, Nat.add_zero] at h
  simp only [nextColumns, hc, Nat.one_ne_zero, if_false, columnSum,
    reflected, Nat.add_sub_cancel, Nat.sub_zero]
  simp only [extended, hL, if_pos, Nat.lt_irrefl, if_false, hc]
  omega

/-- Every interior column in the overflow branch combines two adjacent
old column sums, with the exact four carry contributions. -/
theorem next_column_overflow_interior (q : Nat → Nat) (L i : Nat)
    (hi0 : 0 < i) (hi : i < L)
    (hs : ∀ j, j < L → q j = q (L - 1 - j))
    (hc : carry q L = 1) :
    nextColumns q L i + 10 * (carry q (i + 1) + carry q (L - i + 1)) =
      q i + q (i - 1) + carry q i + carry q (L - i) := by
  have hm : L - i < L := by omega
  have hlow := column_equation q i
  have hhigh := column_equation q (L - i)
  have hind : L - 1 - (L - i) = i - 1 := by omega
  have hsym := hs (L - i) hm
  rw [hind] at hsym
  rw [hsym] at hhigh
  simp only [nextColumns, hc, Nat.one_ne_zero, if_false, columnSum,
    reflected, Nat.add_sub_cancel]
  simp only [extended, hi, hm, if_pos]
  omega

/-- The high carry can be read backwards when scanning the symmetric
column-sum word from the outside in. Together with the forward low carry,
this is the finite transducer's local consistency condition. -/
theorem folded_carry_transition (q : Nat → Nat) (L i : Nat)
    (hi : i < L) (hs : ∀ j, j < L → q j = q (L - 1 - j)) :
    carry q (i + 1) = (q i + carry q i) / 10 ∧
    carry q (L - i) = (q i + carry q (L - 1 - i)) / 10 := by
  constructor
  · rfl
  · have hind : L - i = (L - 1 - i) + 1 := by omega
    rw [hind, carry, ← hs i hi]

/-- Without overflow the emitted folded symbol is the sum of the two
digits calculated by the forward and backward carry states. -/
theorem folded_emission_no_overflow (q : Nat → Nat) (L i : Nat)
    (hi : i < L) (hs : ∀ j, j < L → q j = q (L - 1 - j))
    (hc : carry q L = 0) :
    nextColumns q L i =
      (q i + carry q i) % 10 + (q i + carry q (L - 1 - i)) % 10 := by
  simp only [nextColumns, hc, ite_true, columnSum, reflected, output]
  rw [← hs i hi]

/-- Overflow emission uses the previous high digit. At the first pair
that delayed digit is the appended carry 1. -/
theorem folded_emission_overflow (q : Nat → Nat) (L i : Nat)
    (hi : i < L) (hc : carry q L = 1) :
    nextColumns q L i =
      (q i + carry q i) % 10 + extended q L (L - i) := by
  simp only [nextColumns, hc, Nat.one_ne_zero, if_false, columnSum,
    reflected, Nat.add_sub_cancel, extended, hi, if_pos, output]

/-- The delayed high digit after reading a pair is precisely the one
computed from the guessed backward carry. -/
theorem folded_delay_update (q : Nat → Nat) (L i : Nat)
    (hi : i < L) (hs : ∀ j, j < L → q j = q (L - 1 - j)) :
    extended q L (L - (i + 1)) =
      (q i + carry q (L - 1 - i)) % 10 := by
  have hind : L - (i + 1) = L - 1 - i := by omega
  have hm : L - 1 - i < L := by omega
  rw [hind]
  simp only [extended, hm, if_pos, output, ← hs i hi]

/-- An even input reaches identical low and high carry states at the
center. This is the exact even-input terminal test. -/
theorem even_center_carry (q : Nat → Nat) (k : Nat) :
    carry q k = carry q (2 * k - k) := by
  congr 1
  omega

/-- An odd input's center column advances the low carry to the high
carry. This is the exact odd-input terminal test. -/
theorem odd_center_carry (q : Nat → Nat) (k : Nat) :
    carry q (2 * k + 1 - k) = (q k + carry q k) / 10 := by
  have hind : 2 * k + 1 - k = k + 1 := by omega
  rw [hind, carry]

/-- The central symbol of an odd genuine input is even. -/
theorem odd_center_input (d : Nat → Nat) (k : Nat) :
    columnSum d (2 * k + 1) k = 2 * d k := by
  have hind : 2 * k + 1 - 1 - k = k := by omega
  simp only [columnSum, reflected, hind]
  omega

/-- With no overflow, an odd input retains an odd output width and emits
twice the computed center digit as its terminal center symbol. -/
theorem odd_center_no_overflow (q : Nat → Nat) (k : Nat)
    (hc : carry q (2 * k + 1) = 0) :
    nextColumns q (2 * k + 1) k = 2 * ((q k + carry q k) % 10) := by
  have hind : 2 * k + 1 - 1 - k = k := by omega
  simp only [nextColumns, hc, ite_true, columnSum, reflected, hind, output]
  omega

/-- Overflow turns even width into odd width; the middle output symbol
is twice the last delayed high digit. -/
theorem even_center_overflow (q : Nat → Nat) (k : Nat)
    (hc : carry q (2 * k) = 1) :
    nextColumns q (2 * k) k = 2 * extended q (2 * k) k := by
  have hind : 2 * k + 1 - 1 - k = k := by omega
  simp only [nextColumns, hc, Nat.one_ne_zero, if_false, columnSum, reflected, hind]
  omega

/-- Overflow turns odd width into even width. Its final folded pair is
the old center output digit plus the last delayed high digit. -/
theorem odd_center_overflow (q : Nat → Nat) (k : Nat)
    (hc : carry q (2 * k + 1) = 1) :
    nextColumns q (2 * k + 1) k =
      (q k + carry q k) % 10 + extended q (2 * k + 1) (k + 1) := by
  have hi : k < 2 * k + 1 := by omega
  have hind : 2 * k + 1 - k = k + 1 := by omega
  simpa only [hind] using folded_emission_overflow q (2 * k + 1) k hi hc

/-- A forward carry trace beginning at zero is forced by the input. -/
theorem forward_trace_unique (q a : Nat → Nat) (k : Nat)
    (hzero : a 0 = 0)
    (hstep : ∀ i, i < k → a (i + 1) = (q i + a i) / 10) :
    ∀ i, i ≤ k → a i = carry q i := by
  intro i
  induction i with
  | zero => intro _; exact hzero
  | succ i ih =>
    intro hi
    rw [hstep i (by omega), ih (by omega), carry]

/-- Once a backwards trace meets the actual center carry, every guessed
high carry is forced. In particular, its initially guessed overflow is
the actual overflow. This is independent of any finite testing bound. -/
theorem backward_trace_unique (q b : Nat → Nat) (L k : Nat)
    (hk : k ≤ L)
    (hs : ∀ j, j < L → q j = q (L - 1 - j))
    (hstep : ∀ i, i < k → b i = (q i + b (i + 1)) / 10)
    (hcenter : b k = carry q (L - k)) :
    ∀ i, i ≤ k → b i = carry q (L - i) := by
  have hback : ∀ j, j ≤ k → b (k - j) = carry q (L - (k - j)) := by
    intro j
    induction j with
    | zero => intro _; simpa using hcenter
    | succ j ih =>
      intro hj
      have hsmall : k - (j + 1) < k := by omega
      have hbound : k - (j + 1) < L := by omega
      have hindex : k - (j + 1) + 1 = k - j := by omega
      have hreflect : L - 1 - (k - (j + 1)) = L - (k - j) := by omega
      have hsucc : L - (k - (j + 1)) = (L - (k - j)) + 1 := by omega
      rw [hstep _ hsmall, hindex, ih (by omega), hsucc, carry]
      rw [hs _ hbound, hreflect]
  intro i hi
  have hind : k - (k - i) = i := by omega
  simpa only [hind] using hback (k - i) (by omega)

/-- Full carry soundness for an accepting folded trace on an even-width
input. The guessed overflow `b 0` is certified by meeting in the middle. -/
theorem even_folded_trace_sound (q a b : Nat → Nat) (k : Nat)
    (hs : ∀ j, j < 2 * k → q j = q (2 * k - 1 - j))
    (hzero : a 0 = 0)
    (hlow : ∀ i, i < k → a (i + 1) = (q i + a i) / 10)
    (hhigh : ∀ i, i < k → b i = (q i + b (i + 1)) / 10)
    (hcenter : a k = b k) :
    (∀ i, i ≤ k → a i = carry q i) ∧
    (∀ i, i ≤ k → b i = carry q (2 * k - i)) ∧
    b 0 = carry q (2 * k) := by
  have ha := forward_trace_unique q a k hzero hlow
  have hmid : b k = carry q (2 * k - k) := by
    rw [← hcenter, ha k (Nat.le_refl k)]
    congr 1
    omega
  have hb := backward_trace_unique q b (2 * k) k (by omega) hs hhigh hmid
  exact ⟨ha, hb, by simpa using hb 0 (by omega)⟩

/-- Full carry soundness for an accepting folded trace on an odd-width
input. The center column links the low and high carry traces. -/
theorem odd_folded_trace_sound (q a b : Nat → Nat) (k : Nat)
    (hs : ∀ j, j < 2 * k + 1 → q j = q (2 * k + 1 - 1 - j))
    (hzero : a 0 = 0)
    (hlow : ∀ i, i < k → a (i + 1) = (q i + a i) / 10)
    (hhigh : ∀ i, i < k → b i = (q i + b (i + 1)) / 10)
    (hcenter : b k = (q k + a k) / 10) :
    (∀ i, i ≤ k → a i = carry q i) ∧
    (∀ i, i ≤ k → b i = carry q (2 * k + 1 - i)) ∧
    b 0 = carry q (2 * k + 1) := by
  have ha := forward_trace_unique q a k hzero hlow
  have hind : 2 * k + 1 - k = k + 1 := by omega
  have hmid : b k = carry q (2 * k + 1 - k) := by
    rw [hcenter, ha k (Nat.le_refl k), hind, carry]
  have hb := backward_trace_unique q b (2 * k + 1) k (by omega) hs hhigh hmid
  exact ⟨ha, hb, by simpa using hb 0 (by omega)⟩

/-- A canonical digit realization of a valid symmetric column-sum word.
The more significant member receives `min q 9`, ensuring a positive lead;
the less significant member receives the remaining amount. -/
def realizingDigit (q : Nat → Nat) (L i : Nat) : Nat :=
  if i < L - 1 - i then q i - 9
  else if L - 1 - i < i then min (q i) 9
  else q i / 2

theorem realizingDigit_bounded (q : Nat → Nat) (L : Nat)
    (hq : ∀ i, i < L → q i ≤ 18) :
    ∀ i, i < L → realizingDigit q L i ≤ 9 := by
  intro i hi
  have hqi := hq i hi
  unfold realizingDigit
  split
  · omega
  · split
    · exact Nat.min_le_right _ _
    · omega

/-- The realization reproduces every column sum exactly. The evenness
condition is imposed only on a self-reflected center position. -/
theorem realizingDigit_columns (q : Nat → Nat) (L : Nat)
    (hs : ∀ i, i < L → q i = q (L - 1 - i))
    (hcenter : ∀ i, i < L → i = L - 1 - i → q i % 2 = 0) :
    ∀ i, i < L → columnSum (realizingDigit q L) L i = q i := by
  intro i hi
  have hind : L - 1 - (L - 1 - i) = i := by omega
  have hsym := hs i hi
  simp only [columnSum, reflected, realizingDigit, hind, ← hsym]
  by_cases hlow : i < L - 1 - i
  · have hhigh : ¬ L - 1 - i < i := by omega
    simp only [hlow, hhigh, if_true, if_false]
    omega
  · by_cases hhigh : L - 1 - i < i
    · simp only [hlow, hhigh, if_true, if_false]
      omega
    · have heq : i = L - 1 - i := by omega
      have heven := hcenter i hi heq
      simp only [hlow, hhigh, if_true, if_false]
      omega

theorem realizingDigit_leading_positive (q : Nat → Nat) (L : Nat)
    (hL : 0 < L) (houter : 0 < q 0)
    (hs : ∀ i, i < L → q i = q (L - 1 - i))
    (hcenter : ∀ i, i < L → i = L - 1 - i → q i % 2 = 0) :
    0 < realizingDigit q L (L - 1) := by
  have hsym : q (L - 1) = q 0 := by
    simpa using (hs 0 hL).symm
  have hind : L - 1 - (L - 1) = 0 := by omega
  simp only [realizingDigit, hind, hsym]
  by_cases hlarge : 1 < L
  · have hlow : ¬ L - 1 < 0 := by omega
    have hhigh : 0 < L - 1 := by omega
    simp only [hlow, hhigh, if_false, if_true]
    omega
  · have hone : L = 1 := by omega
    have heven := hcenter 0 hL (by omega)
    subst L
    simp only [Nat.sub_self, Nat.lt_irrefl, if_false]
    omega

/-- Every valid finite folded word is the column-sum word of a positive
decimal integer. This makes extraction of a finite numeric witness from
any future nonempty regular invariant logically exact. -/
theorem valid_word_realizable (q : Nat → Nat) (L : Nat)
    (hL : 0 < L) (houter : 0 < q 0)
    (hq : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L - 1 - i))
    (hcenter : ∀ i, i < L → i = L - 1 - i → q i % 2 = 0) :
    ∃ n d, 0 < n ∧ Canonical n d L ∧
      ∀ i, i < L → columnSum d L i = q i := by
  let d := realizingDigit q L
  have hlead : 0 < d (L - 1) :=
    realizingDigit_leading_positive q L hL houter hs hcenter
  refine ⟨value d L, d, value_positive d L hL hlead,
    ⟨hL, realizingDigit_bounded q L hq, hlead, rfl⟩, ?_⟩
  exact realizingDigit_columns q L hs hcenter

#print axioms canonical_next_no_overflow
#print axioms canonical_next_overflow
#print axioms next_column_no_overflow
#print axioms next_column_overflow_outer
#print axioms next_column_overflow_interior
#print axioms folded_carry_transition
#print axioms folded_emission_no_overflow
#print axioms folded_emission_overflow
#print axioms folded_delay_update
#print axioms odd_center_no_overflow
#print axioms even_center_overflow
#print axioms odd_center_overflow
#print axioms even_folded_trace_sound
#print axioms odd_folded_trace_sound
#print axioms valid_word_realizable

end FoldedDecimal


/-!
# Sound extraction from a symbolic column-sum invariant

This file proves the complete symbolic-to-numeric implication for the
exact column dynamics. All language hypotheses are explicit. No concrete
invariant language or verified DFA checker is supplied here.
-/

namespace FoldedDecimal

open DecimalDigits

/-- Width after the branch selected by the actual final carry. -/
def nextWidth (q : Nat → Nat) (L : Nat) : Nat :=
  if carry q L = 0 then L else L + 1

/-- The exact finite-word admissibility conditions. Values outside the
first L positions are irrelevant to digit representation. -/
def Admissible (L : Nat) (q : Nat → Nat) : Prop :=
  0 < L ∧ 0 < q 0 ∧ (∀ i, i < L → q i ≤ 18) ∧
  (∀ i, i < L → q i = q (L - 1 - i)) ∧
  (∀ i, i < L → i = L - 1 - i → q i % 2 = 0)

/-- The two exact predecessor patterns producing a palindrome next. -/
def BadWord (L : Nat) (q : Nat → Nat) : Prop :=
  (∀ i, i < L → q i ≤ 9) ∨
  (q 0 = 11 ∧ ∀ i, i < L → q i = 0 ∨ q i = 11)

theorem carry_congr_upto (q r : Nat → Nat) (L : Nat)
    (h : ∀ i, i < L → q i = r i) :
    ∀ i, i ≤ L → carry q i = carry r i := by
  intro i
  induction i with
  | zero => intro _; rfl
  | succ i ih =>
    intro hi
    simp only [carry, h i (by omega), ih (by omega)]

theorem output_congr_upto (q r : Nat → Nat) (L : Nat)
    (h : ∀ i, i < L → q i = r i) :
    ∀ i, i < L → output q i = output r i := by
  intro i hi
  simp only [output, h i hi, carry_congr_upto q r L h i (by omega)]

theorem extended_congr_upto (q r : Nat → Nat) (L : Nat)
    (h : ∀ i, i < L → q i = r i) :
    ∀ i, extended q L i = extended r L i := by
  intro i
  by_cases hi : i < L
  · simp only [extended, hi, if_true, output_congr_upto q r L h i hi]
  · simp only [extended, hi, if_false,
      carry_congr_upto q r L h L (Nat.le_refl L)]

/-- The q-word determines the actual next numeric value, regardless of
which canonical decimal digit realization was chosen. -/
theorem step_eq_word_value (n : Nat) (d q : Nat → Nat) (L : Nat)
    (hcan : Canonical n d L)
    (hrep : ∀ i, i < L → columnSum d L i = q i) :
    Lychrel196.step n = value q L := by
  rcases hcan with ⟨hL, hd, hlead, hn⟩
  rw [← hn, step_value d L hd (Or.inr hlead), value_output]
  exact value_congr (columnSum d L) q L hrep

/-- The concrete symbolic update represents the next actual decimal
integer. In particular, symbolic closure need not assume any numeric
invariance hypothesis or equality of irrelevant infinite tails. -/
theorem representation_next (n : Nat) (d q : Nat → Nat) (L : Nat)
    (hcan : Canonical n d L)
    (hrep : ∀ i, i < L → columnSum d L i = q i) :
    ∃ e, Canonical (Lychrel196.step n) e (nextWidth q L) ∧
      ∀ i, i < nextWidth q L → columnSum e (nextWidth q L) i = nextColumns q L i := by
  have hcarry := carry_congr_upto (columnSum d L) q L hrep L (Nat.le_refl L)
  rcases actual_overflow_cases d L hcan.2.1 with hc | hc
  · have hq : carry q L = 0 := hcarry.symm.trans hc
    have hw : nextWidth q L = L := by simp [nextWidth, hq]
    rw [hw]
    refine ⟨output (columnSum d L), canonical_next_no_overflow n d L hcan hc, ?_⟩
    intro i hi
    have hm : L - 1 - i < L := by omega
    simp only [nextColumns, hq, ite_true, columnSum, reflected]
    rw [output_congr_upto (columnSum d L) q L hrep i hi,
      output_congr_upto (columnSum d L) q L hrep (L - 1 - i) hm]
  · have hq : carry q L = 1 := hcarry.symm.trans hc
    have hw : nextWidth q L = L + 1 := by simp [nextWidth, hq]
    rw [hw]
    refine ⟨extended (columnSum d L) L, canonical_next_overflow n d L hcan hc, ?_⟩
    intro i _
    simp only [nextColumns, hq, Nat.one_ne_zero, if_false, columnSum, reflected]
    rw [extended_congr_upto (columnSum d L) q L hrep i,
      extended_congr_upto (columnSum d L) q L hrep (L + 1 - 1 - i)]

/-- Numeric membership induced by a symbolic language. Only finite-prefix
agreement is required, avoiding an implicit extensionality assumption. -/
def RepresentedBy (A : Nat → (Nat → Nat) → Prop) (n : Nat) : Prop :=
  ∃ L q d, Canonical n d L ∧
    (∀ i, i < L → columnSum d L i = q i) ∧ A L q

theorem representedBy_closed (A : Nat → (Nat → Nat) → Prop)
    (hclosed : ∀ L q, A L q → A (nextWidth q L) (nextColumns q L)) :
    ∀ n, RepresentedBy A n → RepresentedBy A (Lychrel196.step n) := by
  rintro n ⟨L, q, d, hcan, hrep, hmem⟩
  obtain ⟨e, he, hnext⟩ := representation_next n d q L hcan hrep
  exact ⟨nextWidth q L, nextColumns q L, e, he, hnext, hclosed L q hmem⟩

theorem representedBy_next_not_palindrome (A : Nat → (Nat → Nat) → Prop)
    (hsafe : ∀ L q, A L q → ¬ BadWord L q) :
    ∀ n, RepresentedBy A n → ¬ Lychrel196.Palindrome (Lychrel196.step n) := by
  rintro n ⟨L, q, d, hcan, hrep, hmem⟩ hp
  rcases hcan with ⟨hL, hd, hlead, hn⟩
  rw [← hn] at hp
  have hb := (step_palindrome_iff d L hL hd hlead).mp hp
  apply hsafe L q hmem
  rcases hb with hlo | ⟨hout, hex⟩
  · exact Or.inl (fun i hi => by simpa only [hrep i hi] using hlo i hi)
  · refine Or.inr ⟨?_, ?_⟩
    · simpa only [hrep 0 hL] using hout
    · intro i hi
      simpa only [hrep i hi] using hex i hi

/-- If a symbolic language is closed under the exact q-update and avoids
the exact bad language, then the next integer after any represented state
has an entirely nonpalindromic orbit. The original state itself may be a
palindrome, which is why the conclusion starts at its next value. -/
theorem representedBy_step_lychrel (A : Nat → (Nat → Nat) → Prop)
    (hclosed : ∀ L q, A L q → A (nextWidth q L) (nextColumns q L))
    (hsafe : ∀ L q, A L q → ¬ BadWord L q)
    (n : Nat) (hmem : RepresentedBy A n) :
    Lychrel196.IsLychrel (Lychrel196.step n) := by
  have horbit : ∀ k, RepresentedBy A (Lychrel196.orbit n k) := by
    intro k
    induction k with
    | zero => exact hmem
    | succ k ih => exact representedBy_closed A hclosed _ ih
  intro k hp
  rw [Lychrel196.orbit_from_step] at hp
  exact representedBy_next_not_palindrome A hsafe _ (horbit k) hp

/-- Explicit finite numeric witness extracted from an admissible symbolic
seed. The witness is `value q L`, not a limit of growing finite numerals.
All closure and avoidance assumptions remain explicit. -/
theorem symbolic_language_seed_sound (A : Nat → (Nat → Nat) → Prop)
    (hclosed : ∀ L q, A L q → A (nextWidth q L) (nextColumns q L))
    (hsafe : ∀ L q, A L q → ¬ BadWord L q)
    (L : Nat) (q : Nat → Nat) (hvalid : Admissible L q) (hseed : A L q) :
    Lychrel196.IsLychrel (value q L) := by
  rcases hvalid with ⟨hL, houter, hq, hs, hcenter⟩
  obtain ⟨n, d, _, hcan, hrep⟩ := valid_word_realizable q L hL houter hq hs hcenter
  have hmem : RepresentedBy A n := ⟨L, q, d, hcan, hrep, hseed⟩
  have hn := representedBy_step_lychrel A hclosed hsafe n hmem
  rwa [step_eq_word_value n d q L hcan hrep] at hn

/-- A nonempty admissible closed symbolic language avoiding the two bad
patterns implies the existence of a decimal Lychrel number. This theorem
does not claim that such a language has been found. -/
theorem symbolic_language_implies_decimal_existence
    (A : Nat → (Nat → Nat) → Prop)
    (hadmissible : ∀ L q, A L q → Admissible L q)
    (hnonempty : ∃ L q, A L q)
    (hclosed : ∀ L q, A L q → A (nextWidth q L) (nextColumns q L))
    (hsafe : ∀ L q, A L q → ¬ BadWord L q) :
    Lychrel196.DecimalLychrelExistence := by
  obtain ⟨L, q, hseed⟩ := hnonempty
  exact ⟨value q L,
    symbolic_language_seed_sound A hclosed hsafe L q (hadmissible L q hseed) hseed⟩

#print axioms representation_next
#print axioms representedBy_step_lychrel
#print axioms symbolic_language_seed_sound
#print axioms symbolic_language_implies_decimal_existence

end FoldedDecimal

/-!
# 8. Exact carry normalization and terminating representatives

Every realizable non-overflow carry word has a finite decimal representative whose second reverse-and-add iterate is a palindrome. This limits single-carry-word invariant proofs; it does not resolve decimal Lychrel existence.
-/

/- Every realizable non-overflow carry word has an admissible representative
whose next mirrored-sum word is entirely at most 9. This is an obstruction to
single-carry-word invariant proofs, not a proof of decimal Lychrel existence. -/
namespace CarryNormalization
open DecimalDigits FoldedDecimal

def norm (a b : Nat) : Nat := if a = b then if a = 0 then 2 else 10 else 9

theorem norm_local (x a b : Nat) (hx : x ≤ 18) (ha : a ≤ 1) (hb : b ≤ 1) :
    let u := (x + a) / 10
    let v := (x + b) / 10
    (norm u v + a) / 10 = u ∧
    (norm u v + b) / 10 = v ∧
    (norm u v + a) % 10 + (norm u v + b) % 10 ≤ 9 := by
  dsimp
  unfold norm
  split <;> rename_i h
  · split <;> omega
  · omega

theorem norm_symmetric (a b : Nat) : norm a b = norm b a := by
  unfold norm
  by_cases h : a = b
  · subst b; simp
  · simp [h, Ne.symm h]

theorem norm_range (a b : Nat) : 0 < norm a b ∧ norm a b ≤ 10 := by
  unfold norm
  split <;> simp_all
  split <;> omega

def normalized (q : Nat → Nat) (L i : Nat) : Nat :=
  norm (carry q (i + 1)) (carry q (L - i))

theorem normalized_preserves_carry (q : Nat → Nat) (L : Nat)
    (hq : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L - 1 - i)) :
    ∀ i, i ≤ L → carry (normalized q L) i = carry q i := by
  intro i
  induction i with
  | zero => intro _; rfl
  | succ i ih =>
    intro hi
    have him : L - 1 - i < L := by omega
    have hf : L - 1 - i + 1 = L - i := by omega
    have hlocal := norm_local (q i) (carry q i) (carry q (L - 1 - i))
      (hq i (by omega))
      (carry_bounded q L hq i (by omega))
      (carry_bounded q L hq (L - 1 - i) (by omega))
    have hout : (q i + carry q (L - 1 - i)) / 10 = carry q (L - i) := by
      rw [hs i (by omega), ← hf]
      rfl
    dsimp at hlocal
    rw [hout] at hlocal
    change (normalized q L i + carry (normalized q L) i) / 10 = carry q (i + 1)
    rw [ih (by omega)]
    exact hlocal.1

theorem normalized_symmetric (q : Nat → Nat) (L i : Nat) (hi : i < L) :
    normalized q L i = normalized q L (L - 1 - i) := by
  have h1 : L - 1 - i + 1 = L - i := by omega
  have h2 : L - (L - 1 - i) = i + 1 := by omega
  simp only [normalized, h1, h2]
  exact norm_symmetric _ _

theorem normalized_admissible (q : Nat → Nat) (L : Nat) (hL : 0 < L) :
    Admissible L (normalized q L) := by
  refine ⟨hL, (norm_range _ _).1, ?_, ?_, ?_⟩
  · intro i hi; have := (norm_range (carry q (i+1)) (carry q (L-i))).2
    exact Nat.le_trans this (by decide)
  · exact normalized_symmetric q L
  · intro i hi hm
    have heq : L - i = i + 1 := by omega
    simp only [normalized, heq, norm, if_true]
    split <;> decide

theorem normalized_next_low (q : Nat → Nat) (L : Nat)
    (hq : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L - 1 - i)) :
    ∀ i, i < L →
      output (normalized q L) i + output (normalized q L) (L - 1 - i) ≤ 9 := by
  intro i hi
  have him : L - 1 - i < L := by omega
  have hf : L - 1 - i + 1 = L - i := by omega
  have hlocal := norm_local (q i) (carry q i) (carry q (L - 1 - i))
    (hq i hi)
    (carry_bounded q L hq i (by omega))
    (carry_bounded q L hq (L - 1 - i) (by omega))
  have hout : (q i + carry q (L - 1 - i)) / 10 = carry q (L - i) := by
    rw [hs i hi, ← hf]
    rfl
  dsimp at hlocal
  rw [hout] at hlocal
  unfold output
  rw [normalized_preserves_carry q L hq hs i (by omega),
    normalized_preserves_carry q L hq hs (L - 1 - i) (by omega),
    ← normalized_symmetric q L i hi]
  exact hlocal.2.2

/-- Every complete non-overflow carry trace has a concrete positive decimal
representative reaching a palindrome after exactly two applications (possibly
earlier as well). In particular carry data alone cannot certify nontermination. -/
theorem same_carries_two_step_palindrome (q : Nat → Nat) (L : Nat)
    (hL : 0 < L)
    (hq : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L - 1 - i))
    (hover : carry q L = 0) :
    ∃ n d, 0 < n ∧ Canonical n d L ∧
      (∀ i, i ≤ L → carry (columnSum d L) i = carry q i) ∧
      Lychrel196.Palindrome (Lychrel196.step (Lychrel196.step n)) := by
  have had := normalized_admissible q L hL
  obtain ⟨n, d, hn, hcan, hrep⟩ := valid_word_realizable (normalized q L) L
    had.1 had.2.1 had.2.2.1 had.2.2.2.1 had.2.2.2.2
  have hcarry : ∀ i, i ≤ L → carry (columnSum d L) i = carry q i := by
    intro i hi
    exact (carry_congr_upto _ _ L hrep i hi).trans
      (normalized_preserves_carry q L hq hs i hi)
  have hncarry : carry (normalized q L) L = 0 :=
    (normalized_preserves_carry q L hq hs L (by omega)).trans hover
  have hwidth : nextWidth (normalized q L) L = L := by
    simp [nextWidth, hncarry]
  obtain ⟨e, hecan, herep⟩ := representation_next n d (normalized q L) L hcan hrep
  rw [hwidth] at hecan herep
  refine ⟨n, d, hn, hcan, hcarry, ?_⟩
  rcases hecan with ⟨heL, heb, hep, hev⟩
  rw [← hev]
  apply (step_palindrome_iff e L heL heb hep).mpr
  left
  intro i hi
  rw [herep i hi]
  simp only [nextColumns, hncarry, if_true, columnSum, reflected]
  exact normalized_next_low q L hq hs i hi

#print axioms same_carries_two_step_palindrome
#print axioms normalized_next_low
#print axioms normalized_admissible
end CarryNormalization

/-!
# 9. Exact local carry encoders for bases two and four

These are column-wise arithmetic identities. Their output correction terms remain explicit; no iteration-preserving decimal encoding or Lychrel witness is claimed.
-/

/-!
Exact local carry encoders from bases 2 and 4 into base 10.
These lemmas do not assert a decimal Lychrel number exists.
The source carry into a column is `c`; each theorem assumes it is 0 or 1.
-/
namespace AffineCarryEncoder

theorem centered_binary_carry (d e c : Nat)
    (hd : d ≤ 1) (he : e ≤ 1) (hc : c ≤ 1) :
    ((d + 4) + (e + 4) + c) / 10 = (d + e + c) / 2 := by
  omega

theorem centered_binary_output (d e c : Nat)
    (hd : d ≤ 1) (he : e ≤ 1) (hc : c ≤ 1) :
    ((d + 4) + (e + 4) + c) % 10 =
      (d + e + c) % 2 + 8 * (1 - (d + e + c) / 2) := by
  omega

theorem centered_quaternary_carry (d e c : Nat)
    (hd : d ≤ 3) (he : e ≤ 3) (hc : c ≤ 1) :
    ((d + 3) + (e + 3) + c) / 10 = (d + e + c) / 4 := by
  omega

theorem centered_quaternary_output (d e c : Nat)
    (hd : d ≤ 3) (he : e ≤ 3) (hc : c ≤ 1) :
    ((d + 3) + (e + 3) + c) % 10 =
      (d + e + c) % 4 + 6 * (1 - (d + e + c) / 4) := by
  omega

theorem dilated_binary_carry (d e c : Nat)
    (hd : d ≤ 1) (he : e ≤ 1) (hc : c ≤ 1) :
    (9 * d + 9 * e + c) / 10 = (d + e + c) / 2 := by
  omega

theorem dilated_binary_output (d e c : Nat)
    (hd : d ≤ 1) (he : e ≤ 1) (hc : c ≤ 1) :
    (((9 * d + 9 * e + c) % 10 : Nat) : Int) =
      9 * (((d + e + c) % 2 : Nat) : Int) +
      8 * ((((d + e + c) / 2 : Nat) : Int) - (c : Int)) := by
  omega

theorem dilated_quaternary_carry (d e c : Nat)
    (hd : d ≤ 3) (he : e ≤ 3) (hc : c ≤ 1) :
    (3 * d + 3 * e + c) / 10 = (d + e + c) / 4 := by
  omega

theorem dilated_quaternary_output (d e c : Nat)
    (hd : d ≤ 3) (he : e ≤ 3) (hc : c ≤ 1) :
    (((3 * d + 3 * e + c) % 10 : Nat) : Int) =
      3 * (((d + e + c) % 4 : Nat) : Int) +
      2 * ((((d + e + c) / 4 : Nat) : Int) - (c : Int)) := by
  omega

#print axioms centered_binary_output
#print axioms centered_quaternary_output
#print axioms dilated_binary_output
#print axioms dilated_quaternary_output
end AffineCarryEncoder

namespace AffineCarryEncoder

theorem reversed_centered_quaternary_carry (d e c : Nat)
    (hd : d ≤ 3) (he : e ≤ 3) (hc : c ≤ 1) :
    ((6 - d) + (6 - e) + (1 - c)) / 10 =
      1 - (d + e + c) / 4 := by
  omega

theorem reversed_centered_quaternary_output (d e c : Nat)
    (hd : d ≤ 3) (he : e ≤ 3) (hc : c ≤ 1) :
    ((6 - d) + (6 - e) + (1 - c)) % 10 =
      3 - (d + e + c) % 4 + 6 * ((d + e + c) / 4) := by
  omega

#print axioms reversed_centered_quaternary_output
end AffineCarryEncoder


/-!
# 10. Sharp four-step termination of complete carry-word representatives

Every positive decimal integer has a same-width representative with the same
complete first-step carry word that reaches a palindrome within four steps.
The bound is optimal. This is an auxiliary obstruction theorem, not a proof
or disproof of decimal Lychrel existence.
-/

/- Finite graph certificates for the overflow-normalization reduction.
   The finite graph certificates and their full numeric connection are
   kernel-checked below. The final numeric statement is
   CarryWordTermination.same_carry_word_palindrome_within_four. -/
namespace OverflowNormalizationCertificate
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
structure State where
  norm : Nat
  layers : List Nat
  bad : Bool
  deriving DecidableEq, Repr

def normEdges (s : Nat) : List (Nat × Nat) :=
  let a := s % 2
  let b := s / 2
  let reset := if b = 0 then [(0,0),(0,2)] else [(10,1),(10,3)]
  reset ++ if a = b then [] else [(9,s)]

def edge (s q h : Nat) : List (Nat × Nat) :=
  let a := s % 2
  let b := s / 2 % 2
  let t := s / 4
  [0,1].flatMap fun bn =>
    if (q+bn)/10 = b then
      let an := (q+a)/10
      let lo := (q+a)%10
      let hi := (q+bn)%10
      [(an+2*bn+(if h=1 then 4*hi else 0), if h=1 then lo+t else lo+hi)]
    else []

def feed : List Nat → Nat → List Nat → List (List Nat × Nat)
  | [], q, _ => [([],q)]
  | _::_, _, [] => []
  | s::ss, q, h::hs =>
    (edge s q h).flatMap fun (st,r) =>
      (feed ss r hs).map fun (tail,v) => (st::tail,v)

def finishFuel : Nat → List Nat → Option Nat → List Nat → Bool → List Bool
  | 0, _, _, _, _ => []
  | _+1, [], c, _, bad => [bad || match c with | none => false | some z => z > 9]
  | _+1, _::_, _, [], _ => []
  | fuel+1, s::ss, c, h::hs, bad =>
    let a := s%2
    let b := s/2%2
    let t := s/4
    match c with
    | none => if a=b then finishFuel fuel ss (if h=1 then some (2*t) else none) hs bad else []
    | some z =>
      if (z+a)/10=b then
        let r := (z+a)%10
        if h=1 then
          (feed ss (r+t) hs).flatMap fun (tail,v) => finishFuel fuel tail none hs (bad || v>9)
        else finishFuel fuel ss (some (2*r)) hs bad
      else []

def finish (layers : List Nat) (c : Option Nat) (hs : List Nat) (bad : Bool) : List Bool :=
  finishFuel (hs.length+1) layers c hs bad

def next (hs : List Nat) (st : State) : List State :=
  (normEdges st.norm).flatMap fun (q,ns) =>
    (feed st.layers q hs).map fun (tail,r) => ⟨ns,tail,st.bad || r>9⟩

def initials (first : Nat) (hs : List Nat) : List State :=
  let layers := hs.map fun h => 2*h + if h=1 then 4 else 0
  (normEdges 2).flatMap fun (q,ns) =>
    if q=first then
      (feed layers q hs).map fun (tail,r) => ⟨ns,tail,r>9⟩
    else []

def finals (hs : List Nat) (st : State) : List Bool :=
  let a := st.norm%2
  let b := st.norm/2
  let cs : List (Option Nat) := (if a=b then [none] else []) ++ [some (10*b)]
  cs.flatMap fun c => finish st.layers c hs st.bad

inductive Reach (first : Nat) (hs : List Nat) : State → Prop
  | initial {s} : s ∈ initials first hs → Reach first hs s
  | advance {s t} : Reach first hs s → t ∈ next hs s → Reach first hs t

theorem reach_subset (first : Nat) (hs : List Nat) (cert : List State)
    (hinit : ∀ s ∈ initials first hs, s ∈ cert)
    (hclosed : ∀ s ∈ cert, ∀ t ∈ next hs s, t ∈ cert) :
    ∀ s, Reach first hs s → s ∈ cert := by
  intro s hr
  induction hr with
  | initial h => exact hinit _ h
  | advance _ ht ih => exact hclosed _ ih _ ht

def cert10 : List State := [
  ⟨0, [0, 0], false⟩,
  ⟨0, [0, 2], false⟩,
  ⟨0, [0, 1], false⟩,
  ⟨0, [0, 3], false⟩,
  ⟨0, [6, 0], false⟩,
  ⟨0, [6, 2], false⟩,
  ⟨0, [6, 1], false⟩,
  ⟨0, [6, 3], false⟩,
  ⟨2, [0, 0], false⟩,
  ⟨2, [0, 2], false⟩,
  ⟨2, [0, 1], false⟩,
  ⟨2, [0, 3], false⟩,
  ⟨2, [36, 0], true⟩,
  ⟨2, [36, 2], false⟩,
  ⟨2, [36, 1], false⟩,
  ⟨2, [36, 1], true⟩,
  ⟨2, [36, 3], false⟩,
  ⟨2, [36, 3], true⟩,
  ⟨2, [2, 1], false⟩,
  ⟨2, [2, 3], false⟩,
  ⟨2, [6, 0], false⟩,
  ⟨2, [6, 2], false⟩,
  ⟨2, [6, 1], false⟩,
  ⟨2, [6, 3], false⟩,
  ⟨1, [1, 0], false⟩,
  ⟨1, [1, 2], false⟩,
  ⟨1, [37, 0], false⟩,
  ⟨1, [37, 0], true⟩,
  ⟨1, [37, 2], false⟩,
  ⟨1, [3, 0], false⟩,
  ⟨1, [3, 2], false⟩,
  ⟨1, [7, 0], false⟩,
  ⟨1, [7, 2], false⟩,
  ⟨3, [1, 0], false⟩,
  ⟨3, [1, 2], false⟩,
  ⟨3, [7, 0], false⟩,
  ⟨3, [7, 2], false⟩
]

def cert9 : List State := [
  ⟨0, [0, 0, 0], false⟩,
  ⟨0, [0, 0, 2], false⟩,
  ⟨0, [0, 4, 0], false⟩,
  ⟨0, [0, 4, 2], false⟩,
  ⟨0, [0, 6, 0], false⟩,
  ⟨0, [0, 6, 2], false⟩,
  ⟨0, [0, 10, 0], false⟩,
  ⟨0, [0, 10, 2], false⟩,
  ⟨0, [0, 1, 0], false⟩,
  ⟨0, [0, 1, 2], false⟩,
  ⟨0, [0, 7, 0], false⟩,
  ⟨0, [0, 7, 2], false⟩,
  ⟨0, [6, 0, 0], false⟩,
  ⟨0, [6, 0, 2], false⟩,
  ⟨0, [6, 4, 0], false⟩,
  ⟨0, [6, 4, 2], false⟩,
  ⟨0, [6, 6, 0], false⟩,
  ⟨0, [6, 6, 2], false⟩,
  ⟨0, [6, 10, 0], false⟩,
  ⟨0, [6, 10, 2], false⟩,
  ⟨0, [6, 1, 0], false⟩,
  ⟨0, [6, 1, 2], false⟩,
  ⟨0, [6, 7, 0], false⟩,
  ⟨0, [6, 7, 2], false⟩,
  ⟨2, [0, 0, 0], false⟩,
  ⟨2, [0, 0, 2], false⟩,
  ⟨2, [0, 4, 0], false⟩,
  ⟨2, [0, 4, 2], false⟩,
  ⟨2, [0, 6, 0], false⟩,
  ⟨2, [0, 6, 2], false⟩,
  ⟨2, [0, 10, 0], false⟩,
  ⟨2, [0, 10, 2], false⟩,
  ⟨2, [0, 1, 0], false⟩,
  ⟨2, [0, 1, 2], false⟩,
  ⟨2, [0, 7, 0], false⟩,
  ⟨2, [0, 7, 2], false⟩,
  ⟨2, [36, 36, 0], true⟩,
  ⟨2, [36, 36, 2], false⟩,
  ⟨2, [36, 36, 1], false⟩,
  ⟨2, [36, 36, 3], false⟩,
  ⟨2, [36, 2, 1], false⟩,
  ⟨2, [36, 2, 3], false⟩,
  ⟨2, [36, 33, 0], true⟩,
  ⟨2, [36, 33, 2], false⟩,
  ⟨2, [36, 33, 2], true⟩,
  ⟨2, [36, 33, 1], true⟩,
  ⟨2, [36, 33, 3], true⟩,
  ⟨2, [36, 37, 0], false⟩,
  ⟨2, [36, 37, 2], false⟩,
  ⟨2, [36, 3, 0], false⟩,
  ⟨2, [36, 3, 2], false⟩,
  ⟨2, [36, 39, 0], true⟩,
  ⟨2, [36, 39, 2], false⟩,
  ⟨2, [36, 39, 2], true⟩,
  ⟨2, [36, 39, 1], true⟩,
  ⟨2, [36, 39, 3], true⟩,
  ⟨2, [2, 1, 0], false⟩,
  ⟨2, [2, 1, 2], false⟩,
  ⟨2, [2, 37, 0], false⟩,
  ⟨2, [2, 37, 0], true⟩,
  ⟨2, [2, 37, 2], false⟩,
  ⟨2, [2, 3, 0], false⟩,
  ⟨2, [2, 3, 2], false⟩,
  ⟨2, [2, 7, 0], false⟩,
  ⟨2, [2, 7, 2], false⟩,
  ⟨2, [6, 0, 0], false⟩,
  ⟨2, [6, 0, 2], false⟩,
  ⟨2, [6, 4, 0], false⟩,
  ⟨2, [6, 4, 2], false⟩,
  ⟨2, [6, 6, 0], false⟩,
  ⟨2, [6, 6, 2], false⟩,
  ⟨2, [6, 10, 0], false⟩,
  ⟨2, [6, 10, 2], false⟩,
  ⟨2, [6, 1, 0], false⟩,
  ⟨2, [6, 1, 2], false⟩,
  ⟨2, [6, 7, 0], false⟩,
  ⟨2, [6, 7, 2], false⟩,
  ⟨1, [1, 0, 0], false⟩,
  ⟨1, [1, 0, 2], false⟩,
  ⟨1, [1, 0, 1], false⟩,
  ⟨1, [1, 0, 3], false⟩,
  ⟨1, [1, 4, 0], false⟩,
  ⟨1, [1, 4, 2], false⟩,
  ⟨1, [1, 8, 0], false⟩,
  ⟨1, [1, 8, 2], false⟩,
  ⟨1, [1, 6, 0], false⟩,
  ⟨1, [1, 6, 2], false⟩,
  ⟨1, [1, 6, 1], false⟩,
  ⟨1, [1, 6, 3], false⟩,
  ⟨1, [1, 10, 0], false⟩,
  ⟨1, [1, 10, 2], false⟩,
  ⟨1, [1, 14, 0], false⟩,
  ⟨1, [1, 14, 2], false⟩,
  ⟨1, [37, 0, 0], false⟩,
  ⟨1, [37, 0, 2], false⟩,
  ⟨1, [37, 36, 0], true⟩,
  ⟨1, [37, 36, 2], false⟩,
  ⟨1, [37, 36, 1], true⟩,
  ⟨1, [37, 36, 3], true⟩,
  ⟨1, [37, 2, 1], false⟩,
  ⟨1, [37, 2, 3], false⟩,
  ⟨1, [37, 6, 0], false⟩,
  ⟨1, [37, 6, 2], false⟩,
  ⟨1, [3, 0, 0], false⟩,
  ⟨1, [3, 0, 2], false⟩,
  ⟨1, [3, 4, 0], false⟩,
  ⟨1, [3, 4, 2], false⟩,
  ⟨1, [3, 6, 0], false⟩,
  ⟨1, [3, 6, 2], false⟩,
  ⟨1, [3, 10, 0], false⟩,
  ⟨1, [3, 10, 2], false⟩,
  ⟨1, [7, 0, 0], false⟩,
  ⟨1, [7, 0, 2], false⟩,
  ⟨1, [7, 0, 1], false⟩,
  ⟨1, [7, 0, 3], false⟩,
  ⟨1, [7, 4, 0], false⟩,
  ⟨1, [7, 4, 2], false⟩,
  ⟨1, [7, 8, 0], false⟩,
  ⟨1, [7, 8, 2], false⟩,
  ⟨1, [7, 6, 0], false⟩,
  ⟨1, [7, 6, 2], false⟩,
  ⟨1, [7, 6, 1], false⟩,
  ⟨1, [7, 6, 3], false⟩,
  ⟨1, [7, 10, 0], false⟩,
  ⟨1, [7, 10, 2], false⟩,
  ⟨1, [7, 14, 0], false⟩,
  ⟨1, [7, 14, 2], false⟩,
  ⟨3, [1, 0, 0], false⟩,
  ⟨3, [1, 0, 2], false⟩,
  ⟨3, [1, 0, 1], false⟩,
  ⟨3, [1, 0, 3], false⟩,
  ⟨3, [1, 4, 0], false⟩,
  ⟨3, [1, 4, 2], false⟩,
  ⟨3, [1, 8, 0], false⟩,
  ⟨3, [1, 8, 2], false⟩,
  ⟨3, [1, 6, 0], false⟩,
  ⟨3, [1, 6, 2], false⟩,
  ⟨3, [1, 6, 1], false⟩,
  ⟨3, [1, 6, 3], false⟩,
  ⟨3, [1, 10, 0], false⟩,
  ⟨3, [1, 10, 2], false⟩,
  ⟨3, [1, 14, 0], false⟩,
  ⟨3, [1, 14, 2], false⟩,
  ⟨3, [7, 0, 0], false⟩,
  ⟨3, [7, 0, 2], false⟩,
  ⟨3, [7, 0, 1], false⟩,
  ⟨3, [7, 0, 3], false⟩,
  ⟨3, [7, 4, 0], false⟩,
  ⟨3, [7, 4, 2], false⟩,
  ⟨3, [7, 8, 0], false⟩,
  ⟨3, [7, 8, 2], false⟩,
  ⟨3, [7, 6, 0], false⟩,
  ⟨3, [7, 6, 2], false⟩,
  ⟨3, [7, 6, 1], false⟩,
  ⟨3, [7, 6, 3], false⟩,
  ⟨3, [7, 10, 0], false⟩,
  ⟨3, [7, 10, 2], false⟩,
  ⟨3, [7, 14, 0], false⟩,
  ⟨3, [7, 14, 2], false⟩
]

theorem cert10_initial : ∀ s ∈ initials 10 [1,0], s ∈ cert10 := by decide
theorem cert10_closed : ∀ s ∈ cert10, ∀ t ∈ next [1,0] s, t ∈ cert10 := by decide
theorem cert10_safe : ∀ s ∈ cert10, ∀ b ∈ finals [1,0] s, b = false := by decide

theorem cert9_initial : ∀ s ∈ initials 9 [1,1,0], s ∈ cert9 := by decide
theorem cert9_closed : ∀ s ∈ cert9, ∀ t ∈ next [1,1,0] s, t ∈ cert9 := by decide
theorem cert9_safe : ∀ s ∈ cert9, ∀ b ∈ finals [1,1,0] s, b = false := by decide

theorem normalized10_graph_safe (s : State) (hr : Reach 10 [1,0] s) :
    ∀ b ∈ finals [1,0] s, b = false :=
  cert10_safe s (reach_subset 10 [1,0] cert10 cert10_initial cert10_closed s hr)

theorem normalized9_graph_safe (s : State) (hr : Reach 9 [1,1,0] s) :
    ∀ b ∈ finals [1,1,0] s, b = false :=
  cert9_safe s (reach_subset 9 [1,1,0] cert9 cert9_initial cert9_closed s hr)

#print axioms normalized10_graph_safe
#print axioms normalized9_graph_safe
end OverflowNormalizationCertificate


namespace OverflowCarryNormalization
open DecimalDigits FoldedDecimal

/-- Overflow normalization uses0,9,10; low2 from the older no-overflow
normalization does not have the same four-step termination property. -/
def normZero (a b : Nat) : Nat := if a = b then if a = 0 then 0 else 10 else 9

theorem normZero_local (x a b : Nat) (hx : x ≤ 18) (ha : a ≤ 1) (hb : b ≤ 1) :
    let u := (x + a) / 10
    let v := (x + b) / 10
    (normZero u v + a) / 10 = u ∧
    (normZero u v + b) / 10 = v := by
  dsimp
  unfold normZero
  split <;> rename_i h
  · split <;> omega
  · omega

theorem normZero_symmetric (a b : Nat) : normZero a b = normZero b a := by
  unfold normZero
  by_cases h : a = b
  · subst b; simp
  · simp [h, Ne.symm h]

theorem normZero_bounded (a b : Nat) : normZero a b ≤ 10 := by
  unfold normZero
  split <;> simp_all
  split <;> omega

def normalizedZero (q : Nat → Nat) (L i : Nat) : Nat :=
  normZero (carry q (i + 1)) (carry q (L - i))

theorem normalizedZero_preserves_carry (q : Nat → Nat) (L : Nat)
    (hq : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L - 1 - i)) :
    ∀ i, i ≤ L → carry (normalizedZero q L) i = carry q i := by
  intro i
  induction i with
  | zero => intro _; rfl
  | succ i ih =>
    intro hi
    have hf : L - 1 - i + 1 = L - i := by omega
    have hlocal := normZero_local (q i) (carry q i) (carry q (L - 1 - i))
      (hq i (by omega))
      (carry_bounded q L hq i (by omega))
      (carry_bounded q L hq (L - 1 - i) (by omega))
    have hout : (q i + carry q (L - 1 - i)) / 10 = carry q (L - i) := by
      rw [hs i (by omega), ← hf]
      rfl
    dsimp at hlocal
    rw [hout] at hlocal
    change (normalizedZero q L i + carry (normalizedZero q L) i) / 10 = carry q (i + 1)
    rw [ih (by omega)]
    exact hlocal.1

theorem normalizedZero_symmetric (q : Nat → Nat) (L i : Nat) (hi : i < L) :
    normalizedZero q L i = normalizedZero q L (L - 1 - i) := by
  have h1 : L - 1 - i + 1 = L - i := by omega
  have h2 : L - (L - 1 - i) = i + 1 := by omega
  simp only [normalizedZero, h1, h2]
  exact normZero_symmetric _ _

theorem normalizedZero_outer (q : Nat → Nat) (L : Nat)
    (hc : carry q L = 1) :
    normalizedZero q L 0 = 9 ∨ normalizedZero q L 0 = 10 := by
  by_cases h : carry q (0+1) = 1
  · simp [normalizedZero,h,hc,normZero]
  · simp [normalizedZero,h,hc,normZero]

theorem normalizedZero_admissible (q : Nat → Nat) (L : Nat)
    (hL : 0 < L) (hc : carry q L = 1) :
    Admissible L (normalizedZero q L) := by
  refine ⟨hL, ?_, ?_, ?_, ?_⟩
  · have := normalizedZero_outer q L hc; omega
  · intro i hi
    exact Nat.le_trans (normZero_bounded _ _) (by decide)
  · exact normalizedZero_symmetric q L
  · intro i hi hm
    have heq : L - i = i + 1 := by omega
    simp only [normalizedZero, heq, normZero, if_true]
    split <;> decide

/-- Every overflowing carryword has a genuine finite normalized integer.
The four-step palindrome claim is proved by the separate graph bridge. -/
theorem normalizedZero_realizable (q : Nat → Nat) (L : Nat)
    (hL : 0 < L)
    (hq : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L - 1 - i))
    (hc : carry q L = 1) :
    ∃ n d, 0 < n ∧ Canonical n d L ∧
      (∀ i, i < L → columnSum d L i = normalizedZero q L i) ∧
      (∀ i, i ≤ L → carry (columnSum d L) i = carry q i) := by
  have had := normalizedZero_admissible q L hL hc
  obtain ⟨n, d, hn, hcan, hrep⟩ := valid_word_realizable (normalizedZero q L) L
    had.1 had.2.1 had.2.2.1 had.2.2.2.1 had.2.2.2.2
  refine ⟨n,d,hn,hcan,hrep,?_⟩
  intro i hi
  exact (carry_congr_upto _ _ L hrep i hi).trans
    (normalizedZero_preserves_carry q L hq hs i hi)

/-- Local input-automaton edge. It justifies the certificate's four-state
recognizer directly from the two physical carry equations. -/
theorem normZero_input_edge (x a bn : Nat)
    (hx : x ≤ 18) (ha : a ≤ 1) (hb : bn ≤ 1) :
    let an := (x+a)/10
    let b := (x+bn)/10
    (normZero an b, an + 2*bn) ∈
      OverflowNormalizationCertificate.normEdges (a+2*b) := by
  have han : (x+a)/10 ≤ 1 := by omega
  have hbo : (x+bn)/10 ≤ 1 := by omega
  have ha' : a=0 ∨ a=1 := by omega
  have hb' : bn=0 ∨ bn=1 := by omega
  have hn' : (x+a)/10=0 ∨ (x+a)/10=1 := by omega
  have ho' : (x+bn)/10=0 ∨ (x+bn)/10=1 := by omega
  dsimp
  rcases ha' with ha'|ha' <;> rcases hb' with hb'|hb' <;>
    rcases hn' with hn'|hn' <;> rcases ho' with ho'|ho' <;>
    simp only [hn',ho',ha',hb',normZero,OverflowNormalizationCertificate.normEdges] <;>
    simp_all <;> omega

/-- A physical normalized folded pair follows exactly an input-automaton edge. -/
theorem normalizedZero_folded_edge (q : Nat → Nat) (L i : Nat)
    (hq : ∀ j, j < L → q j ≤ 18)
    (hs : ∀ j, j < L → q j = q (L - 1 - j))
    (hi : i < L) :
    (normalizedZero q L i,
      carry (normalizedZero q L) (i+1) +
        2*carry (normalizedZero q L) (L-(i+1))) ∈
      OverflowNormalizationCertificate.normEdges
        (carry (normalizedZero q L) i +
          2*carry (normalizedZero q L) (L-i)) := by
  have hf : L - 1 - i + 1 = L - i := by omega
  have hout : (q i + carry q (L-1-i))/10 = carry q (L-i) := by
    rw [hs i hi, ← hf]
    rfl
  have he := normZero_input_edge (q i) (carry q i) (carry q (L-1-i))
    (hq i hi) (carry_bounded q L hq i (by omega))
    (carry_bounded q L hq (L-1-i) (by omega))
  dsimp at he
  rw [hout] at he
  change (normalizedZero q L i, carry q (i+1) + 2*carry q (L-1-i)) ∈
    OverflowNormalizationCertificate.normEdges (carry q i + 2*carry q (L-i)) at he
  rw [normalizedZero_preserves_carry q L hq hs (i+1) (by omega),
    normalizedZero_preserves_carry q L hq hs (L-(i+1)) (by omega),
    normalizedZero_preserves_carry q L hq hs i (by omega),
    normalizedZero_preserves_carry q L hq hs (L-i) (by omega)]
  have hind : L-(i+1)=L-1-i := by omega
  simpa only [hind] using he

/-- The normalized odd center is exactly ten times its high carry. -/
theorem normalizedZero_odd_center (q : Nat → Nat) (k : Nat)
    (hq : ∀ j, j < 2*k+1 → q j ≤ 18)
    (hs : ∀ j, j < 2*k+1 → q j = q (2*k+1-1-j)) :
    normalizedZero q (2*k+1) k =
      10*carry (normalizedZero q (2*k+1)) (2*k+1-k) := by
  have hind : 2*k+1-k=k+1 := by omega
  rw [normalizedZero_preserves_carry q (2*k+1) hq hs _ (by omega)]
  simp only [normalizedZero,hind,normZero,if_true]
  have hc := carry_bounded q (2*k+1) hq (k+1) (by omega)
  split <;> omega


#print axioms normalizedZero_realizable
#print axioms normZero_input_edge
end OverflowCarryNormalization


namespace OverflowCarryNormalization
open DecimalDigits FoldedDecimal Lychrel196

/-- The exact pair-sum state after k operations, including changing width. -/
def iterPairs (q : Nat → Nat) (L : Nat) : Nat → Nat × (Nat → Nat)
  | 0 => (L,q)
  | k+1 =>
    let prev := iterPairs q L k
    (nextWidth prev.2 prev.1, nextColumns prev.2 prev.1)

/-- A numeric orbit realizes every iterated pair-sum state exactly. -/
theorem iterPairs_representation (n : Nat) (d q : Nat → Nat) (L k : Nat)
    (hcan : Canonical n d L)
    (hrep : ∀ i, i < L → columnSum d L i = q i) :
    ∃ e, Canonical (orbit n k) e (iterPairs q L k).1 ∧
      (∀ i, i < (iterPairs q L k).1 →
        columnSum e (iterPairs q L k).1 i = (iterPairs q L k).2 i) := by
  induction k with
  | zero => exact ⟨d,hcan,hrep⟩
  | succ k ih =>
    obtain ⟨e,he,hr⟩ := ih
    obtain ⟨f,hf,hfr⟩ := representation_next (orbit n k) e
      (iterPairs q L k).2 (iterPairs q L k).1 he hr
    exact ⟨f,hf,hfr⟩

/-- If an exact iterated pair-sum state is low, the following numeric iterate
is a palindrome. This transfers the finite graph conclusion to the orbit. -/
theorem iterPairs_low_palindrome (n : Nat) (d q : Nat → Nat) (L k : Nat)
    (hcan : Canonical n d L)
    (hrep : ∀ i, i < L → columnSum d L i = q i)
    (hlow : ∀ i, i < (iterPairs q L k).1 → (iterPairs q L k).2 i ≤ 9) :
    Palindrome (orbit n (k+1)) := by
  obtain ⟨e,he,hr⟩ := iterPairs_representation n d q L k hcan hrep
  rcases he with ⟨heL,heb,hep,hev⟩
  change Palindrome (step (orbit n k))
  rw [← hev]
  apply (step_palindrome_iff e (iterPairs q L k).1 heL heb hep).mpr
  left
  intro i hi
  rw [hr i hi]
  exact hlow i hi

/-- Numeric extraction once the normalized graph has established a low state.
No finite-digit or time-testing assumption is used here. -/
theorem normalizedZero_low_extraction (q : Nat → Nat) (L k : Nat)
    (hL : 0 < L)
    (hq : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L-1-i))
    (hc : carry q L = 1)
    (hlow : ∀ i, i < (iterPairs (normalizedZero q L) L k).1 →
      (iterPairs (normalizedZero q L) L k).2 i ≤ 9) :
    ∃ n d, 0 < n ∧ Canonical n d L ∧
      (∀ i, i ≤ L → carry (columnSum d L) i = carry q i) ∧
      Palindrome (orbit n (k+1)) := by
  obtain ⟨n,d,hn,hcan,hrep,hcarry⟩ := normalizedZero_realizable q L hL hq hs hc
  exact ⟨n,d,hn,hcan,hcarry,
    iterPairs_low_palindrome n d (normalizedZero q L) L k hcan hrep hlow⟩

/-- A reusable final extraction statement. The two low-state hypotheses are
supplied by the independent graph-to-numeric bridge. -/
theorem all_carry_words_terminate_by_four_of_low
    (h10 : ∀ q : Nat → Nat, ∀ L : Nat,
      0 < L → (∀ i, i < L → q i ≤ 18) →
      (∀ i, i < L → q i = q (L-1-i)) → carry q L = 1 →
      normalizedZero q L 0 = 10 →
      ∀ i, i < (iterPairs (normalizedZero q L) L 2).1 →
        (iterPairs (normalizedZero q L) L 2).2 i ≤ 9)
    (h9 : ∀ q : Nat → Nat, ∀ L : Nat,
      0 < L → (∀ i, i < L → q i ≤ 18) →
      (∀ i, i < L → q i = q (L-1-i)) → carry q L = 1 →
      normalizedZero q L 0 = 9 →
      ∀ i, i < (iterPairs (normalizedZero q L) L 3).1 →
        (iterPairs (normalizedZero q L) L 3).2 i ≤ 9)
    (q : Nat → Nat) (L : Nat)
    (hL : 0 < L)
    (hq : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L-1-i)) :
    ∃ n d k, 0 < n ∧ Canonical n d L ∧
      (∀ i, i ≤ L → carry (columnSum d L) i = carry q i) ∧
      0 < k ∧ k ≤ 4 ∧ Palindrome (orbit n k) := by
  have hc := carry_bounded q L hq L (by omega)
  have hh : carry q L=0 ∨ carry q L=1 := by omega
  rcases hh with hh|hh
  · obtain ⟨n,d,hn,hcan,hcarry,hpal⟩ :=
      CarryNormalization.same_carries_two_step_palindrome q L hL hq hs hh
    exact ⟨n,d,2,hn,hcan,hcarry,by omega,by omega,hpal⟩
  · rcases normalizedZero_outer q L hh with hfirst|hfirst
    · obtain ⟨n,d,hn,hcan,hcarry,hpal⟩ :=
        normalizedZero_low_extraction q L 3 hL hq hs hh (h9 q L hL hq hs hh hfirst)
      exact ⟨n,d,4,hn,hcan,hcarry,by omega,by omega,hpal⟩
    · obtain ⟨n,d,hn,hcan,hcarry,hpal⟩ :=
        normalizedZero_low_extraction q L 2 hL hq hs hh (h10 q L hL hq hs hh hfirst)
      exact ⟨n,d,3,hn,hcan,hcarry,by omega,by omega,hpal⟩

#print axioms normalizedZero_low_extraction
#print axioms all_carry_words_terminate_by_four_of_low
end OverflowCarryNormalization

namespace NormalizationBridge
open DecimalDigits FoldedDecimal OverflowNormalizationCertificate
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

def traceState (q : Nat → Nat) (L h i : Nat) : Nat :=
  carry q i + 2 * carry q (L-i) + if h=1 then 4*extended q L (L-i) else 0

theorem traceState_fields (q : Nat → Nat) (L h i : Nat)
    (hq : ∀ j, j < L → q j ≤ 18) (hi : i ≤ L) :
    traceState q L h i % 2 = carry q i ∧
    traceState q L h i / 2 % 2 = carry q (L-i) ∧
    traceState q L h i / 4 = if h=1 then extended q L (L-i) else 0 := by
  have ha := carry_bounded q L hq i hi
  have hb := carry_bounded q L hq (L-i) (by omega)
  unfold traceState
  split <;> omega

theorem traceState_initial (q : Nat → Nat) (L h : Nat)
    (hc : carry q L = h) : traceState q L h 0 = 2*h + if h=1 then 4 else 0 := by
  simp [traceState, carry, extended, hc]
  split <;> simp_all

theorem edge_trace (q : Nat → Nat) (L h i : Nat)
    (hq : ∀ j, j < L → q j ≤ 18)
    (hs : ∀ j, j < L → q j = q (L-1-j))
    (hi : i < L) (hh : h=0 ∨ h=1) (hc : carry q L = h) :
    (traceState q L h (i+1), nextColumns q L i) ∈ edge (traceState q L h i) (q i) h := by
  have hf := traceState_fields q L h i hq (by omega)
  have hn := traceState_fields q L h (i+1) hq (by omega)
  have hb := carry_bounded q L hq (L-1-i) (by omega)
  have hmem : carry q (L-1-i) ∈ [0,1] := by simp; omega
  have ht := folded_carry_transition q L i hi hs
  have hid : L-(i+1)=L-1-i := by omega
  simp only [edge, hf.1, hf.2.1, hf.2.2, List.mem_flatMap]
  refine ⟨carry q (L-1-i), hmem, ?_⟩
  rw [← ht.2]
  simp only [if_true, List.mem_singleton, Prod.mk.injEq]
  constructor
  · simp only [traceState, hid, ht.1]
    rcases hh with rfl | rfl
    · simp
    · simp only [if_true]
      rw [← folded_delay_update q L i hi hs, hid]
  · rcases hh with rfl | rfl
    · simp only [Nat.zero_ne_one, if_false]
      exact folded_emission_no_overflow q L i hi hs hc
    · simp only [if_true]
      exact folded_emission_overflow q L i hi hc

theorem feed_cons_mem (s q h st r : Nat) (ss hs tail : List Nat) (v : Nat)
    (he : (st,r) ∈ edge s q h) (hf : (tail,v) ∈ feed ss r hs) :
    (st::tail,v) ∈ feed (s::ss) q (h::hs) := by
  simp only [feed, List.mem_flatMap]
  exact ⟨(st,r),he, by simp only [List.mem_map]; exact ⟨(tail,v),hf,rfl⟩⟩

theorem canonical_admissible (n : Nat) (d : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) : Admissible L (columnSum d L) := by
  refine ⟨hc.1, ?_, columnSum_bounded d L hc.2.1, columnSum_symmetric d L, ?_⟩
  · have hl := hc.2.2.1
    simp only [columnSum, reflected, Nat.sub_zero]
    omega
  · intro i hi heq
    simp only [columnSum, reflected, ← heq]
    omega

theorem admissible_congr (L : Nat) (q r : Nat → Nat) (ha : Admissible L q)
    (he : ∀ i, i<L → q i=r i) : Admissible L r := by
  refine ⟨ha.1, by rw [←he 0 ha.1]; exact ha.2.1, ?_, ?_, ?_⟩
  · intro i hi; rw [←he i hi]; exact ha.2.2.1 i hi
  · intro i hi; rw [←he i hi, ←he (L-1-i) (by omega)]; exact ha.2.2.2.1 i hi
  · intro i hi hm; rw [←he i hi]; exact ha.2.2.2.2 i hi hm

theorem admissible_next (q : Nat → Nat) (L : Nat) (ha : Admissible L q) :
    Admissible (nextWidth q L) (nextColumns q L) := by
  obtain ⟨n,d,_,hc,hr⟩ := valid_word_realizable q L ha.1 ha.2.1 ha.2.2.1 ha.2.2.2.1 ha.2.2.2.2
  obtain ⟨e,he,hr'⟩ := representation_next n d q L hc hr
  exact admissible_congr _ _ _ (canonical_admissible _ _ _ he) hr'

theorem outer_small_no_overflow (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hsmall : q 0 ≤ 8) : carry q L=0 := by
  have hp := carry_bounded q L ha.2.2.1 (L-1) (by omega)
  have he : L=L-1+1 := by have := ha.1; omega
  have hs := ha.2.2.2.1 0 ha.1
  simp only [Nat.sub_zero] at hs
  have hf : carry q L = (q (L-1) + carry q (L-1))/10 := by
    exact (congrArg (carry q) he).trans (by rfl)
  rw [hf, ←hs]
  omega


theorem finish_even_overflow (s z : Nat) (ss hs : List Nat) (bad b : Bool)
    (hc : s%2=s/2%2) (hz : z=2*(s/4))
    (hf : b ∈ finish ss (some z) hs bad) :
    b ∈ finish (s::ss) none (1::hs) bad := by
  simpa [finish, finishFuel, hc, hz] using hf

theorem finish_even_no_overflow (s : Nat) (ss hs : List Nat) (bad b : Bool)
    (hc : s%2=s/2%2)
    (hf : b ∈ finish ss none hs bad) :
    b ∈ finish (s::ss) none (0::hs) bad := by
  simpa [finish, finishFuel, hc] using hf

theorem finish_odd_no_overflow (s z v : Nat) (ss hs : List Nat) (bad b : Bool)
    (hc : (z+s%2)/10=s/2%2) (hv : v=2*((z+s%2)%10))
    (hf : b ∈ finish ss (some v) hs bad) :
    b ∈ finish (s::ss) (some z) (0::hs) bad := by
  simpa [finish, finishFuel, hc, hv] using hf

theorem finish_odd_overflow (s z : Nat) (ss hs tail : List Nat) (v : Nat) (bad b : Bool)
    (hc : (z+s%2)/10=s/2%2)
    (he : (tail,v) ∈ feed ss ((z+s%2)%10+s/4) hs)
    (hf : b ∈ finish tail none hs (bad || decide (v>9))) :
    b ∈ finish (s::ss) (some z) (1::hs) bad := by
  simp only [finish, List.length_cons, Nat.add_comm hs.length 1, finishFuel,
    hc, if_true, List.mem_flatMap]
  refine ⟨(tail,v),he,?_⟩
  simpa only [finish, Nat.add_comm hs.length 1] using hf

theorem finish_empty_none (bad : Bool) : bad ∈ finish [] none [] bad := by
  simp [finish,finishFuel]

theorem finish_empty_some (bad : Bool) (z : Nat) :
    (bad || decide (z>9)) ∈ finish [] (some z) [] bad := by
  simp [finish,finishFuel]


theorem finish_trace_even_overflow (q : Nat → Nat) (k : Nat)
    (hq : ∀ j, j<2*k → q j≤18) (hc : carry q (2*k)=1)
    (tail hs : List Nat) (bad b : Bool)
    (hf : b ∈ finish tail (some (nextColumns q (2*k) k)) hs bad) :
    b ∈ finish (traceState q (2*k) 1 k::tail) none (1::hs) bad := by
  have hd := traceState_fields q (2*k) 1 k hq (by omega)
  apply finish_even_overflow _ (nextColumns q (2*k) k) tail hs bad b
  · rw [hd.1,hd.2.1]; congr 1; omega
  · rw [hd.2.2]; have hi : 2*k-k=k := by omega
    simpa only [if_true,hi] using even_center_overflow q k hc
  · exact hf

theorem finish_trace_even_no_overflow (q : Nat → Nat) (k : Nat)
    (hq : ∀ j, j<2*k → q j≤18)
    (tail hs : List Nat) (bad b : Bool)
    (hf : b ∈ finish tail none hs bad) :
    b ∈ finish (traceState q (2*k) 0 k::tail) none (0::hs) bad := by
  have hd := traceState_fields q (2*k) 0 k hq (by omega)
  apply finish_even_no_overflow _ tail hs bad b
  · rw [hd.1,hd.2.1]; congr 1; omega
  · exact hf

theorem finish_trace_odd_no_overflow (q : Nat → Nat) (k : Nat)
    (hq : ∀ j, j<2*k+1 → q j≤18) (hc : carry q (2*k+1)=0)
    (tail hs : List Nat) (bad b : Bool)
    (hf : b ∈ finish tail (some (nextColumns q (2*k+1) k)) hs bad) :
    b ∈ finish (traceState q (2*k+1) 0 k::tail) (some (q k)) (0::hs) bad := by
  have hd := traceState_fields q (2*k+1) 0 k hq (by omega)
  apply finish_odd_no_overflow _ (q k) (nextColumns q (2*k+1) k) tail hs bad b
  · rw [hd.1,hd.2.1]; exact (odd_center_carry q k).symm
  · rw [hd.1]; exact odd_center_no_overflow q k hc
  · exact hf

theorem finish_trace_odd_overflow (q : Nat → Nat) (k : Nat)
    (hq : ∀ j, j<2*k+1 → q j≤18) (hc : carry q (2*k+1)=1)
    (tail hs rest : List Nat) (v : Nat) (bad b : Bool)
    (he : (rest,v) ∈ feed tail (nextColumns q (2*k+1) k) hs)
    (hf : b ∈ finish rest none hs (bad || decide (v>9))) :
    b ∈ finish (traceState q (2*k+1) 1 k::tail) (some (q k)) (1::hs) bad := by
  have hd := traceState_fields q (2*k+1) 1 k hq (by omega)
  apply finish_odd_overflow _ (q k) tail hs rest v bad b
  · rw [hd.1,hd.2.1]; exact (odd_center_carry q k).symm
  · rw [hd.1,hd.2.2]
    have heq := odd_center_overflow q k hc
    have hi : 2*k+1-k=k+1 := by omega
    simp only [if_true,hi]
    rw [←heq]
    exact he
  · exact hf

#print axioms edge_trace
#print axioms admissible_next
end NormalizationBridge


namespace NormalizationReach
open OverflowNormalizationCertificate

def badPrefix (out : Nat → Nat) : Nat → Bool
  | 0 => false
  | k+1 => badPrefix out k || decide (out k > 9)

theorem badPrefix_eq_false_iff (out : Nat → Nat) (k : Nat) :
    badPrefix out k = false ↔ ∀ i, i < k → out i ≤ 9 := by
  induction k with
  | zero => simp [badPrefix]
  | succ k ih =>
    simp only [badPrefix, Bool.or_eq_false_iff, decide_eq_false_iff_not, Nat.not_lt, ih]
    constructor
    · rintro ⟨hprev, hlast⟩ i hi
      by_cases he : i = k
      · simpa [he] using hlast
      · exact hprev i (by omega)
    · intro h
      exact ⟨fun i hi => h i (by omega), h k (by omega)⟩

theorem initial_mem (first : Nat) (hs : List Nat) (ns : Nat)
    (tail : List Nat) (out : Nat)
    (hn : (first, ns) ∈ normEdges 2)
    (hf : (tail, out) ∈
      feed (hs.map fun h => 2*h + if h=1 then 4 else 0) first hs) :
    (⟨ns, tail, decide (out > 9)⟩ : State) ∈ initials first hs := by
  simp only [initials, List.mem_flatMap]
  refine ⟨(first, ns), hn, ?_⟩
  simp only [if_true, List.mem_map]
  exact ⟨(tail, out), hf, rfl⟩

theorem next_mem (hs : List Nat) (s ns q out : Nat) (layers tail : List Nat)
    (bad : Bool) (hn : (q, ns) ∈ normEdges s)
    (hf : (tail, out) ∈ feed layers q hs) :
    (⟨ns, tail, bad || decide (out > 9)⟩ : State) ∈ next hs ⟨s,layers,bad⟩ := by
  simp only [next, List.mem_flatMap]
  refine ⟨(q,ns),hn,?_⟩
  simp only [List.mem_map]
  exact ⟨(tail,out),hf,rfl⟩

theorem reach_of_traces (first : Nat) (hs : List Nat)
    (ns : Nat → Nat) (layers : Nat → List Nat) (q out : Nat → Nat) (k : Nat)
    (hns : ns 0 = 2)
    (hlayers : layers 0 = hs.map fun h => 2*h + if h=1 then 4 else 0)
    (hq : q 0 = first)
    (hn : ∀ i, i < k → (q i, ns (i+1)) ∈ normEdges (ns i))
    (hf : ∀ i, i < k → (layers (i+1), out i) ∈ feed (layers i) (q i) hs)
    (hk : 0 < k) :
    Reach first hs ⟨ns k, layers k, badPrefix out k⟩ := by
  induction k with
  | zero => omega
  | succ k ih =>
    cases k with
    | zero =>
      have hn0 := hn 0 (by omega)
      have hf0 := hf 0 (by omega)
      rw [hns, hq] at hn0
      rw [hlayers, hq] at hf0
      simpa [badPrefix] using Reach.initial (initial_mem first hs (ns 1) (layers 1) (out 0) hn0 hf0)
    | succ j =>
      have hr := ih (fun i hi => hn i (by omega)) (fun i hi => hf i (by omega)) (by omega)
      exact Reach.advance hr (next_mem hs (ns (j+1)) (ns (j+1+1)) (q (j+1))
        (out (j+1)) (layers (j+1)) (layers (j+1+1)) (badPrefix out (j+1))
        (hn (j+1) (by omega)) (hf (j+1) (by omega)))

theorem finals_mem_none (hs : List Nat) (s : State) (b : Bool)
    (he : s.norm % 2 = s.norm / 2)
    (hf : b ∈ finish s.layers none hs s.bad) : b ∈ finals hs s := by
  simp only [finals, he, if_true, List.mem_flatMap]
  exact ⟨none, by simp, hf⟩

theorem finals_mem_some (hs : List Nat) (s : State) (b : Bool)
    (hf : b ∈ finish s.layers (some (10*(s.norm/2))) hs s.bad) :
    b ∈ finals hs s := by
  simp only [finals, List.mem_flatMap]
  exact ⟨some (10*(s.norm/2)), by simp, hf⟩

theorem finishFuel_true (fuel : Nat) (layers : List Nat) (c : Option Nat)
    (hs : List Nat) (b : Bool)
    (hm : b ∈ finishFuel fuel layers c hs true) : b = true := by
  induction fuel generalizing layers c hs with
  | zero => simp [finishFuel] at hm
  | succ fuel ih =>
    cases layers with
    | nil => simpa [finishFuel] using hm
    | cons s ss =>
      cases hs with
      | nil => simp [finishFuel] at hm
      | cons h hs =>
        cases c with
        | none =>
          simp only [finishFuel] at hm
          split at hm
          · exact ih _ _ _ hm
          · simp at hm
        | some z =>
          simp only [finishFuel] at hm
          split at hm
          · split at hm
            · simp only [List.mem_flatMap] at hm
              obtain ⟨pair,_,hm⟩ := hm
              simp only [Bool.true_or] at hm
              exact ih _ _ _ hm
            · exact ih _ _ _ hm
          · simp at hm

theorem finish_false_implies_bad_false (layers : List Nat) (c : Option Nat)
    (hs : List Nat) (bad : Bool) (hm : false ∈ finish layers c hs bad) : bad = false := by
  cases bad with
  | false => rfl
  | true => have := finishFuel_true _ _ _ _ _ hm; contradiction

theorem finals_false_implies_bad_false (hs : List Nat) (s : State)
    (hm : false ∈ finals hs s) : s.bad = false := by
  simp only [finals, List.mem_flatMap] at hm
  obtain ⟨c,_,hm⟩ := hm
  exact finish_false_implies_bad_false _ _ _ _ hm

#print axioms badPrefix_eq_false_iff
#print axioms reach_of_traces
#print axioms finals_mem_none
#print axioms finals_mem_some
#print axioms finals_false_implies_bad_false
end NormalizationReach

namespace NormalizationTen
open DecimalDigits FoldedDecimal OverflowNormalizationCertificate OverflowCarryNormalization
open NormalizationBridge NormalizationReach
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

theorem normalized10_low_after_two (q : Nat → Nat) (L : Nat)
    (hL : 0<L) (hq : ∀ i, i<L → q i≤18)
    (hs : ∀ i, i<L → q i=q (L-1-i)) (hc : carry q L=1)
    (hfirst : normalizedZero q L 0=10) :
    ∀ i, i<(iterPairs (normalizedZero q L) L 2).1 →
      (iterPairs (normalizedZero q L) L 2).2 i≤9 := by
  let r := normalizedZero q L
  let u := nextColumns r L
  let v := nextColumns u (L+1)
  change r 0=10 at hfirst
  have ar : Admissible L r := normalizedZero_admissible q L hL hc
  have cr : carry r L=1 := (normalizedZero_preserves_carry q L hq hs L (by omega)).trans hc
  have wr : nextWidth r L=L+1 := by simp [nextWidth,cr]
  have au : Admissible (L+1) u := by simpa only [wr] using admissible_next r L ar
  have u0 : u 0=1 := by
    have he := next_column_overflow_outer r L hL cr
    have c1 : carry r 1=1 := by change (r 0+0)/10=1; rw [hfirst]
    change u 0+10*carry r 1=r 0+1 at he
    rw [c1,hfirst] at he
    omega
  have cu : carry u (L+1)=0 := outer_small_no_overflow u (L+1) au (by omega)
  have wu : nextWidth u (L+1)=L+1 := by simp [nextWidth,cu]
  have av : Admissible (L+1) v := by simpa only [wu] using admissible_next u (L+1) au
  have hiw : iterPairs r L 2=(L+1,v) := by
    simp only [iterPairs,wr]
    change (nextWidth u (L+1),v)=(L+1,v)
    rw [wu]
  change ∀ i, i<(iterPairs r L 2).1 → (iterPairs r L 2).2 i≤9
  rw [hiw]
  simp only
  by_cases hsmall : L=1
  · subst L
    intro i hi
    have ui : u i=1 := by
      have us := au.2.2.2.1 i hi
      have hi' : i=0 ∨ i=1 := by omega
      rcases hi' with rfl | rfl
      · exact u0
      · simpa using us.trans u0
    have he := next_column_no_overflow u 2 i hi au.2.2.2.1 cu
    have c0 := carry_bounded u 2 au.2.2.1 i (by omega)
    have cm := carry_bounded u 2 au.2.2.1 (2-1-i) (by omega)
    change v i+10*(carry u (i+1)+carry u (2-i))=2*u i+carry u i+carry u (2-1-i) at he
    rw [ui] at he
    omega
  · let k := L/2
    have hk : 0<k := by dsimp [k]; omega
    let ns := fun i => carry r i+2*carry r (L-i)
    let layers := fun i => [traceState r L 1 i,traceState u (L+1) 0 i]
    have hr : Reach 10 [1,0] ⟨ns k,layers k,badPrefix v k⟩ := by
      apply reach_of_traces 10 [1,0] ns layers r v k
      · dsimp [ns]; simp [carry,cr]
      · simp only [layers,traceState_initial r L 1 cr,traceState_initial u (L+1) 0 cu]
        decide
      · exact hfirst
      · intro i hi
        exact normalizedZero_folded_edge q L i hq hs (by dsimp [k] at hi; omega)
      · intro i hi
        have hir : i<L := by dsimp [k] at hi; omega
        have hiu : i<L+1 := by omega
        apply feed_cons_mem
        · exact edge_trace r L 1 i ar.2.2.1 ar.2.2.2.1 hir (Or.inr rfl) cr
        · apply feed_cons_mem
          · exact edge_trace u (L+1) 0 i au.2.2.1 au.2.2.2.1 hiu (Or.inl rfl) cu
          · simp [feed,v]
      · exact hk
    have hcases : L=2*k ∨ L=2*k+1 := by dsimp [k]; omega
    rcases hcases with heven | hodd
    · have huwid : L+1=2*k+1 := by omega
      have fm : (badPrefix v k || decide (v k>9)) ∈ finals [1,0] ⟨ns k,layers k,badPrefix v k⟩ := by
        apply finals_mem_none
        · change (carry r k+2*carry r (L-k))%2=(carry r k+2*carry r (L-k))/2
          have cb := carry_bounded r L ar.2.2.1 k (by omega)
          have hind : L-k=k := by omega
          rw [hind]; omega
        · change (badPrefix v k || decide (v k>9)) ∈
            finish [traceState r L 1 k,traceState u (L+1) 0 k] none [1,0] (badPrefix v k)
          have f0 := finish_empty_some (badPrefix v k) (v k)
          have f1 := finish_trace_odd_no_overflow u k (by simpa only [←huwid] using au.2.2.1)
            (by simpa only [←huwid] using cu) [] [] (badPrefix v k) _ (by simpa only [←huwid] using f0)
          have f2 := finish_trace_even_overflow r k (by simpa only [←heven] using ar.2.2.1)
            (by simpa only [←heven] using cr) [traceState u (L+1) 0 k] [0]
            (badPrefix v k) _ (by simpa only [←heven,←huwid] using f1)
          simpa only [←heven] using f2
      have hz := normalized10_graph_safe _ hr _ fm
      have hb : badPrefix v k=false := by simp only [Bool.or_eq_false_iff] at hz; exact hz.1
      have hmid : v k≤9 := by simp only [Bool.or_eq_false_iff,decide_eq_false_iff_not] at hz; omega
      have hp := (badPrefix_eq_false_iff v k).mp hb
      intro i hi
      by_cases hil : i<k
      · exact hp i hil
      · by_cases hie : i=k
        · simpa [hie] using hmid
        · have hs' := av.2.2.2.1 i hi
          rw [hs']
          exact hp (L+1-1-i) (by omega)
    · have huwid : L+1=2*(k+1) := by omega
      have fm : (badPrefix v k || decide (v k>9)) ∈ finals [1,0] ⟨ns k,layers k,badPrefix v k⟩ := by
        apply finals_mem_some
        have cb := carry_bounded r L ar.2.2.1 k (by omega)
        have db := carry_bounded r L ar.2.2.1 (L-k) (by omega)
        have nsfield : ns k/2=carry r (L-k) := by dsimp [ns]; omega
        have center : r k=10*(ns k/2) := by
          rw [nsfield]
          have hh := normalizedZero_odd_center q k (by simpa only [←hodd] using hq)
            (by simpa only [←hodd] using hs)
          simpa only [←hodd] using hh
        change (badPrefix v k || decide (v k>9)) ∈
          finish [traceState r L 1 k,traceState u (L+1) 0 k] (some (10*(ns k/2))) [1,0] (badPrefix v k)
        rw [←center]
        have he : ([traceState u (L+1) 0 (k+1)],v k) ∈ feed [traceState u (L+1) 0 k] (u k) [0] := by
          apply feed_cons_mem
          · exact edge_trace u (L+1) 0 k au.2.2.1 au.2.2.2.1 (by omega) (Or.inl rfl) cu
          · simp [feed,v]
        have f0 := finish_empty_none (badPrefix v k || decide (v k>9))
        have f1 := finish_trace_even_no_overflow u (k+1) (by simpa only [←huwid] using au.2.2.1)
          [] [] (badPrefix v k || decide (v k>9)) _ f0
        have f2 := finish_trace_odd_overflow r k (by simpa only [←hodd] using ar.2.2.1)
          (by simpa only [←hodd] using cr) [traceState u (L+1) 0 k] [0]
          [traceState u (L+1) 0 (k+1)] (v k) (badPrefix v k) _
          (by simpa only [←hodd] using he) (by simpa only [←huwid] using f1)
        simpa only [←hodd] using f2
      have hz := normalized10_graph_safe _ hr _ fm
      have hb : badPrefix v (k+1)=false := by simpa only [badPrefix] using hz
      have hp := (badPrefix_eq_false_iff v (k+1)).mp hb
      intro i hi
      by_cases hil : i<k+1
      · exact hp i hil
      · have hs' := av.2.2.2.1 i hi
        rw [hs']
        exact hp (L+1-1-i) (by omega)

#print axioms normalized10_low_after_two
end NormalizationTen


namespace OverflowNormalizationNine
open DecimalDigits FoldedDecimal OverflowNormalizationCertificate
open OverflowCarryNormalization NormalizationBridge NormalizationReach
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

theorem outer_large_overflow (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hlarge : 10 ≤ q 0) : carry q L = 1 := by
  have hp := carry_bounded q L ha.2.2.1 (L-1) (by omega)
  have he : L=L-1+1 := by have := ha.1; omega
  have hs := ha.2.2.2.1 0 ha.1
  simp only [Nat.sub_zero] at hs
  have hf : carry q L = (q (L-1) + carry q (L-1))/10 := by
    exact (congrArg (carry q) he).trans (by rfl)
  have hq := ha.2.2.1 0 ha.1
  rw [hf, ←hs]
  omega

theorem normalized9_low_after_three (q : Nat → Nat) (L : Nat)
    (hL : 0 < L)
    (hq : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L-1-i))
    (hc : carry q L = 1)
    (ho : normalizedZero q L 0 = 9) :
    let r := normalizedZero q L
    let s := nextColumns r L
    let t := nextColumns s (L+1)
    let u := nextColumns t (L+2)
    ∀ i, i < L+2 → u i ≤ 9 := by
  let r := normalizedZero q L
  let s := nextColumns r L
  let t := nextColumns s (L+1)
  let u := nextColumns t (L+2)
  change ∀ i, i < L+2 → u i ≤ 9
  have ar : Admissible L r := normalizedZero_admissible q L hL hc
  have cr : carry r L=1 := (normalizedZero_preserves_carry q L hq hs L (by omega)).trans hc
  have os : s 0=10 := by
    have he := next_column_overflow_outer r L hL cr
    have hr : carry r 1=0 := by simp [carry, r, ho]
    change r 0 = 9 at ho
    change s 0 + 10*carry r 1 = r 0+1 at he
    omega
  have as' := admissible_next r L ar
  have as_ : Admissible (L+1) s := by simpa [nextWidth,cr] using as'
  have cs : carry s (L+1)=1 := outer_large_overflow s (L+1) as_ (by omega)
  have ot : t 0=1 := by
    have he := next_column_overflow_outer s (L+1) (by omega) cs
    have hs1 : carry s 1=1 := by simp [carry,os]
    change t 0 + 10*carry s 1 = s 0+1 at he
    omega
  have at' := admissible_next s (L+1) as_
  have at_ : Admissible (L+2) t := by simpa [nextWidth,cs,Nat.add_assoc] using at'
  have ct : carry t (L+2)=0 := outer_small_no_overflow t (L+2) at_ (by omega)
  have au' := admissible_next t (L+2) at_
  have au : Admissible (L+2) u := by simpa [nextWidth,ct] using au'
  let ns := fun i => carry r i + 2*carry r (L-i)
  let layers := fun i => [traceState r L 1 i, traceState s (L+1) 1 i,
    traceState t (L+2) 0 i]
  have hns0 : ns 0=2 := by simp [ns,carry,cr]
  have hlay0 : layers 0 = [1,1,0].map (fun h => 2*h + if h=1 then 4 else 0) := by
    simp only [layers, traceState_initial r L 1 cr,
      traceState_initial s (L+1) 1 cs, traceState_initial t (L+2) 0 ct]
    rfl
  have hn : ∀ i, i<L → (r i,ns (i+1)) ∈ normEdges (ns i) := by
    intro i hi
    exact normalizedZero_folded_edge q L i hq hs hi
  have hfeed : ∀ i, i<L → (layers (i+1), u i) ∈ feed (layers i) (r i) [1,1,0] := by
    intro i hi
    exact feed_cons_mem _ _ _ _ _ _ _ _ _
      (edge_trace r L 1 i ar.2.2.1 ar.2.2.2.1 hi (Or.inr rfl) cr)
      (feed_cons_mem _ _ _ _ _ _ _ _ _
        (edge_trace s (L+1) 1 i as_.2.2.1 as_.2.2.2.1 (by omega) (Or.inr rfl) cs)
        (feed_cons_mem _ _ _ _ _ _ _ _ _
          (edge_trace t (L+2) 0 i at_.2.2.1 at_.2.2.2.1 (by omega) (Or.inl rfl) ct)
          (by simp [feed,u])))
  let k := L/2
  have hkL : L=2*k ∨ L=2*k+1 := by omega
  have hk : 0<k := by
    by_cases h : k=0
    · have hl1 : L=1 := by omega
      have he := ar.2.2.2.2 0 hL (by omega)
      change r 0=9 at ho
      omega
    · omega
  have hrch : Reach 9 [1,1,0] ⟨ns k,layers k,badPrefix u k⟩ :=
    reach_of_traces 9 [1,1,0] ns layers r u k hns0 hlay0 ho
      (fun i hi => hn i (by omega)) (fun i hi => hfeed i (by omega)) hk
  have hsafe := normalized9_graph_safe _ hrch
  rcases hkL with hEven | hOdd
  · have hf3 : badPrefix u (k+1) ∈
        finish [traceState t (L+2) 0 (k+1)] none [0] (badPrefix u (k+1)) := by
      have he : L+2=2*(k+1) := by omega
      rw [he]
      exact finish_trace_even_no_overflow t (k+1) (by simpa [←he] using at_.2.2.1)
        [] [] _ _ (finish_empty_none _)
    have hfeed3 : ([traceState t (L+2) 0 (k+1)],u k) ∈
        feed [traceState t (L+2) 0 k] (t k) [0] := by
      exact feed_cons_mem _ _ _ _ _ _ _ _ _
        (edge_trace t (L+2) 0 k at_.2.2.1 at_.2.2.2.1 (by omega) (Or.inl rfl) ct)
        (by simp [feed,u])
    have hf2 : badPrefix u (k+1) ∈
        finish [traceState s (L+1) 1 k, traceState t (L+2) 0 k]
          (some (s k)) [1,0] (badPrefix u k) := by
      have he : L+1=2*k+1 := by omega
      rw [he]
      apply finish_trace_odd_overflow s k (by simpa [←he] using as_.2.2.1)
        (by simpa [←he] using cs) [traceState t (L+2) 0 k] [0]
        [traceState t (L+2) 0 (k+1)] (u k) (badPrefix u k) (badPrefix u (k+1))
      · simpa only [←he] using hfeed3
      · exact hf3
    have hf1 : badPrefix u (k+1) ∈ finish (layers k) none [1,1,0] (badPrefix u k) := by
      change badPrefix u (k+1) ∈ finish
        (traceState r L 1 k :: [traceState s (L+1) 1 k, traceState t (L+2) 0 k])
        none [1,1,0] (badPrefix u k)
      rw [hEven]
      apply finish_trace_even_overflow r k (by simpa [←hEven] using ar.2.2.1)
        (by simpa [←hEven] using cr)
      simpa only [←hEven] using hf2
    have hneq : ns k%2=ns k/2 := by
      have hb := carry_bounded r L ar.2.2.1 k (by omega)
      have he : L-k=k := by omega
      simp only [ns,he]
      omega
    have hb := hsafe _ (finals_mem_none [1,1,0] ⟨ns k,layers k,badPrefix u k⟩
      _ hneq hf1)
    have hp := (badPrefix_eq_false_iff u (k+1)).mp hb
    intro i hi
    by_cases hil : i<k+1
    · exact hp i hil
    · rw [au.2.2.2.1 i hi]
      exact hp _ (by omega)
  · have hf3 : badPrefix u (k+2) ∈
        finish [traceState t (L+2) 0 (k+1)] (some (t (k+1))) [0] (badPrefix u (k+1)) := by
      have he : L+2=2*(k+1)+1 := by omega
      rw [he]
      apply finish_trace_odd_no_overflow t (k+1) (by simpa [←he] using at_.2.2.1)
        (by simpa [←he] using ct) [] []
      simpa only [←he] using finish_empty_some (badPrefix u (k+1)) (u (k+1))
    have hf2 : badPrefix u (k+2) ∈
        finish [traceState s (L+1) 1 (k+1),traceState t (L+2) 0 (k+1)]
          none [1,0] (badPrefix u (k+1)) := by
      have he : L+1=2*(k+1) := by omega
      rw [he]
      apply finish_trace_even_overflow s (k+1) (by simpa [←he] using as_.2.2.1)
        (by simpa [←he] using cs)
      simpa only [←he] using hf3
    have hfeed23 : ([traceState s (L+1) 1 (k+1),traceState t (L+2) 0 (k+1)],u k) ∈
        feed [traceState s (L+1) 1 k,traceState t (L+2) 0 k] (s k) [1,0] := by
      exact feed_cons_mem _ _ _ _ _ _ _ _ _
        (edge_trace s (L+1) 1 k as_.2.2.1 as_.2.2.2.1 (by omega) (Or.inr rfl) cs)
        (feed_cons_mem _ _ _ _ _ _ _ _ _
          (edge_trace t (L+2) 0 k at_.2.2.1 at_.2.2.2.1 (by omega) (Or.inl rfl) ct)
          (by simp [feed,u]))
    have hf1 : badPrefix u (k+2) ∈ finish (layers k) (some (r k)) [1,1,0] (badPrefix u k) := by
      change badPrefix u (k+2) ∈ finish
        (traceState r L 1 k :: [traceState s (L+1) 1 k,traceState t (L+2) 0 k])
        (some (r k)) [1,1,0] (badPrefix u k)
      rw [hOdd]
      apply finish_trace_odd_overflow r k (by simpa [←hOdd] using ar.2.2.1)
        (by simpa [←hOdd] using cr) _ _ _ (u k)
      · simpa only [←hOdd] using hfeed23
      · simpa only [←hOdd] using hf2
    have hcenter : r k=10*(ns k/2) := by
      have ha := carry_bounded r L ar.2.2.1 k (by omega)
      have hb := carry_bounded r L ar.2.2.1 (L-k) (by omega)
      have hnsc : ns k/2=carry r (L-k) := by simp only [ns]; omega
      rw [hnsc]
      change normalizedZero q L k = 10*carry (normalizedZero q L) (L-k)
      rw [hOdd]
      exact normalizedZero_odd_center q k (by simpa [←hOdd] using hq) (by simpa [←hOdd] using hs)
    rw [hcenter] at hf1
    have hb := hsafe _ (finals_mem_some [1,1,0] ⟨ns k,layers k,badPrefix u k⟩ _ hf1)
    have hp := (badPrefix_eq_false_iff u (k+2)).mp hb
    intro i hi
    by_cases hil : i<k+2
    · exact hp i hil
    · rw [au.2.2.2.1 i hi]
      exact hp _ (by omega)

#print axioms normalized9_low_after_three

theorem normalized9_iterPairs_low_after_three (q : Nat → Nat) (L : Nat)
    (hL : 0 < L)
    (hq : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L-1-i))
    (hc : carry q L = 1)
    (ho : normalizedZero q L 0 = 9) :
    ∀ i, i < (iterPairs (normalizedZero q L) L 3).1 →
      (iterPairs (normalizedZero q L) L 3).2 i ≤ 9 := by
  let r := normalizedZero q L
  let s := nextColumns r L
  let t := nextColumns s (L+1)
  let u := nextColumns t (L+2)
  have ar : Admissible L r := normalizedZero_admissible q L hL hc
  have cr : carry r L=1 := (normalizedZero_preserves_carry q L hq hs L (by omega)).trans hc
  have wr : nextWidth r L=L+1 := by simp [nextWidth,cr]
  have os : s 0=10 := by
    have he := next_column_overflow_outer r L hL cr
    have hr : carry r 1=0 := by simp [carry,r,ho]
    change r 0=9 at ho
    change s 0+10*carry r 1=r 0+1 at he
    omega
  have as_ : Admissible (L+1) s := by simpa only [wr] using admissible_next r L ar
  have cs : carry s (L+1)=1 := outer_large_overflow s (L+1) as_ (by omega)
  have ws : nextWidth s (L+1)=L+2 := by simp [nextWidth,cs,Nat.add_assoc]
  have ot : t 0=1 := by
    have he := next_column_overflow_outer s (L+1) (by omega) cs
    have hs1 : carry s 1=1 := by simp [carry,os]
    change t 0+10*carry s 1=s 0+1 at he
    omega
  have at_ : Admissible (L+2) t := by simpa only [ws] using admissible_next s (L+1) as_
  have ct : carry t (L+2)=0 := outer_small_no_overflow t (L+2) at_ (by omega)
  have wt : nextWidth t (L+2)=L+2 := by simp [nextWidth,ct]
  have hiw : iterPairs r L 3=(L+2,u) := by
    simp only [iterPairs,wr]
    change (nextWidth (nextColumns s (L+1)) (nextWidth s (L+1)),
      nextColumns (nextColumns s (L+1)) (nextWidth s (L+1)))=(L+2,u)
    rw [ws]
    change (nextWidth t (L+2),u)=(L+2,u)
    rw [wt]
  change ∀ i, i < (iterPairs r L 3).1 → (iterPairs r L 3).2 i ≤ 9
  rw [hiw]
  exact normalized9_low_after_three q L hL hq hs hc ho

#print axioms normalized9_iterPairs_low_after_three
end OverflowNormalizationNine


namespace CarryWordTermination
open DecimalDigits FoldedDecimal Lychrel196

/-- Every realizable complete decimal carry word is also the complete carry
word of a positive integer whose reverse-and-add orbit reaches a palindrome
within four steps. The normalization retains the whole first carry word,
including overflow, but changes the digit pair sums. -/
theorem same_carry_word_palindrome_within_four
    (q : Nat → Nat) (L : Nat)
    (hL : 0 < L)
    (hq : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L-1-i)) :
    ∃ n d k, 0 < n ∧ Canonical n d L ∧
      (∀ i, i ≤ L → carry (columnSum d L) i = carry q i) ∧
      0 < k ∧ k ≤ 4 ∧ Palindrome (orbit n k) := by
  exact OverflowCarryNormalization.all_carry_words_terminate_by_four_of_low
    NormalizationTen.normalized10_low_after_two
    OverflowNormalizationNine.normalized9_iterPairs_low_after_three
    q L hL hq hs

/-- Numeric form of the theorem: every positive input has a same-width,
same-complete-carry-word representative terminating in at most four steps. -/
theorem every_positive_integer_has_fast_same_carry_representative
    (a : Nat) (ha : 0 < a) :
    ∃ L da n dn k, Canonical a da L ∧ 0 < n ∧ Canonical n dn L ∧
      (∀ i, i ≤ L → carry (columnSum dn L) i = carry (columnSum da L) i) ∧
      0 < k ∧ k ≤ 4 ∧ Palindrome (orbit n k) := by
  obtain ⟨da,L,hcan⟩ := canonical_exists a ha
  have hq : ∀ i, i < L → columnSum da L i ≤ 18 := by
    intro i hi
    have h1 := hcan.2.1 i hi
    have h2 := hcan.2.1 (L-1-i) (by omega)
    simp only [columnSum,reflected]
    omega
  have hs : ∀ i, i < L → columnSum da L i = columnSum da L (L-1-i) := by
    intro i hi
    have hind : L-1-(L-1-i)=i := by omega
    simp only [columnSum,reflected,hind,Nat.add_comm]
  obtain ⟨n,dn,k,hn,hncan,hcarry,hk,hk4,hpal⟩ :=
    same_carry_word_palindrome_within_four (columnSum da L) L hcan.1 hq hs
  exact ⟨L,da,n,dn,k,hcan,hn,hncan,hcarry,hk,hk4,hpal⟩

#print axioms same_carry_word_palindrome_within_four
#print axioms every_positive_integer_has_fast_same_carry_representative
end CarryWordTermination

namespace CarryNormalizationSharpness
open DecimalDigits FoldedDecimal Lychrel196
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

/-- The complete five-digit carry trace is 0,0,0,1,1,1. -/
def slowCarry (i : Nat) : Nat := if i<3 then 0 else 1

/-- This carry trace forces only five possible first reverse-and-add values. -/
theorem five_first_values (n : Nat) (d : Nat → Nat)
    (hcan : Canonical n d 5)
    (hc : ∀ i, i≤5 → carry (columnSum d 5) i=slowCarry i) :
    step n=100099 ∨ step n=100299 ∨ step n=100499 ∨
      step n=100699 ∨ step n=100899 := by
  let q := columnSum d 5
  have c1 : carry q 1=0 := hc 1 (by decide)
  have c2 : carry q 2=0 := hc 2 (by decide)
  have c3 : carry q 3=1 := hc 3 (by decide)
  have c4 : carry q 4=1 := hc 4 (by decide)
  have c5 : carry q 5=1 := hc 5 (by decide)
  have q4 : q 4=q 0 := by simp [q,columnSum,reflected,Nat.add_comm]
  have q3 : q 3=q 1 := by simp [q,columnSum,reflected,Nat.add_comm]
  have q2 : q 2=2*d 2 := by simp [q,columnSum,reflected]; omega
  have e1 : (q 0+0)/10=0 := c1
  have e2 : (q 1+carry q 1)/10=0 := c2
  have e3 : (q 2+carry q 2)/10=1 := c3
  have e4 : (q 3+carry q 3)/10=1 := c4
  have e5 : (q 4+carry q 4)/10=1 := c5
  rw [c1] at e2
  rw [c2,q2] at e3
  rw [c3,q3] at e4
  rw [c4,q4] at e5
  have q0 : q 0=9 := by omega
  have q1 : q 1=9 := by omega
  have dc : d 2≤9 := hcan.2.1 2 (by decide)
  have sv := step_eq_word_value n d q 5 hcan (fun _ _ => rfl)
  have sn : step n=99099+200*d 2 := by
    rw [sv]
    simp only [value]
    rw [q4,q3,q2,q1,q0]
    omega
  omega

theorem five_values_checked :
    noPalindromeFor 3 100099=true ∧ noPalindromeFor 3 100299=true ∧
    noPalindromeFor 3 100499=true ∧ noPalindromeFor 3 100699=true ∧
    noPalindromeFor 3 100899=true := by decide

/-- Every positive five-digit integer with this carry trace avoids a palindrome
for its first three positive-time reverse-and-add iterates. -/
theorem slow_carry_requires_at_least_four (n : Nat) (d : Nat → Nat)
    (hcan : Canonical n d 5)
    (hc : ∀ i, i≤5 → carry (columnSum d 5) i=slowCarry i) :
    ∀ k, 0<k → k≤3 → ¬ Palindrome (orbit n k) := by
  have hv := five_first_values n d hcan hc
  have hf : noPalindromeFor 3 (step n)=true := by
    rcases hv with h|h|h|h|h <;> rw [h]
    · exact five_values_checked.1
    · exact five_values_checked.2.1
    · exact five_values_checked.2.2.1
    · exact five_values_checked.2.2.2.1
    · exact five_values_checked.2.2.2.2
  intro k hk hmax
  have hn := noPalindromeFor_sound 3 (step n) hf (k-1) (by omega)
  rw [orbit_from_step] at hn
  have he : k-1+1=k := by omega
  simpa only [he] using hn

def witnessDigit (i : Nat) : Nat := if i=2 then 5 else if 3≤i then 9 else 0

theorem witness_canonical : Canonical 99500 witnessDigit 5 := by
  refine ⟨by decide, ?_, by decide, by decide⟩
  intro i hi
  unfold witnessDigit
  split
  · omega
  · split <;> omega

 theorem witness_carries : ∀ i, i≤5 → carry (columnSum witnessDigit 5) i=slowCarry i := by
  intro i hi
  have he : i=0 ∨ i=1 ∨ i=2 ∨ i=3 ∨ i=4 ∨ i=5 := by omega
  rcases he with rfl|rfl|rfl|rfl|rfl|rfl <;> decide

theorem witness_reaches_at_four :
    orbit 99500 1=100099 ∧ orbit 99500 2=1090100 ∧
    orbit 99500 3=1101001 ∧ orbit 99500 4=2102012 ∧
    Palindrome (orbit 99500 4) := by decide

theorem four_is_optimal :
    (∃ n d, 0<n ∧ Canonical n d 5 ∧
      (∀ i, i≤5 → carry (columnSum d 5) i=slowCarry i) ∧
      Palindrome (orbit n 4)) ∧
    (∀ n d, Canonical n d 5 →
      (∀ i, i≤5 → carry (columnSum d 5) i=slowCarry i) →
      ∀ k, 0<k → k≤3 → ¬ Palindrome (orbit n k)) := by
  exact ⟨⟨99500,witnessDigit,by decide,witness_canonical,witness_carries,
    witness_reaches_at_four.2.2.2.2⟩,slow_carry_requires_at_least_four⟩

#print axioms five_first_values
#print axioms slow_carry_requires_at_least_four
#print axioms four_is_optimal
end CarryNormalizationSharpness


namespace CarryHistory
open DecimalDigits FoldedDecimal

/-- When complete carries agree, the first differing pair-sum coefficient
is doubled by non-overflow and unchanged by overflow. -/
theorem next_first_difference (q r : Nat → Nat) (L m : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hm : m < L)
    (hlow : ∀ j, j < m → q j = r j)
    (hc : ∀ j, j ≤ L → carry q j = carry r j) :
    (nextColumns q L m : Int) - nextColumns r L m =
      (if carry q L=0 then 2 else 1) * ((q m : Int)-r m) := by
  have hcm := hc L (by omega)
  by_cases ho : carry q L=0
  · have hor : carry r L=0 := by omega
    have hqnext := next_column_no_overflow q L m hm hq.2.2.2.1 ho
    have hrnext := next_column_no_overflow r L m hm hr.2.2.2.1 hor
    rw [←hc (m+1) (by omega), ←hc (L-m) (by omega),
      ←hc m (by omega), ←hc (L-1-m) (by omega)] at hrnext
    simp only [ho,if_true]
    omega
  · have hoq : carry q L=1 := by
      have := carry_bounded q L hq.2.2.1 L (by omega)
      omega
    have hor : carry r L=1 := by omega
    simp only [ho,if_false,Int.one_mul]
    by_cases hz : m=0
    · subst m
      have hqnext := next_column_overflow_outer q L hq.1 hoq
      have hrnext := next_column_overflow_outer r L hr.1 hor
      rw [←hc 1 (by omega)] at hrnext
      omega
    · have hqnext := next_column_overflow_interior q L m (by omega) hm hq.2.2.2.1 hoq
      have hrnext := next_column_overflow_interior r L m (by omega) hm hr.2.2.2.1 hor
      rw [←hc (m+1) (by omega), ←hc (L-m+1) (by omega),
        ←hc m (by omega), ←hc (L-m) (by omega), ←hlow (m-1) (by omega)] at hrnext
      omega

/-- No earlier difference is introduced when the carry words agree. -/
theorem next_lower_equal (q r : Nat → Nat) (L m : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hm : m < L)
    (hlow : ∀ j, j < m → q j = r j)
    (hc : ∀ j, j ≤ L → carry q j = carry r j) :
    ∀ j, j < m → nextColumns q L j = nextColumns r L j := by
  intro j hj
  have he := next_first_difference q r L j hq hr (by omega)
    (fun k hk => hlow k (by omega)) hc
  rw [hlow j hj] at he
  simp only [Int.sub_self,Int.mul_zero] at he
  omega

def noOverflowCount (left : Nat → Nat → Nat) (width : Nat → Nat) : Nat → Nat
  | 0 => 0
  | k+1 => noOverflowCount left width k + if carry (left k) (width k)=0 then 1 else 0

/-- This statement concerns genuine exact pair-sum dynamics with a shared
width and identical complete carry words, not an approximate model. -/
theorem first_difference_over_time
    (left right : Nat → Nat → Nat) (width : Nat → Nat) (K m : Nat)
    (ha : ∀ t, t ≤ K → Admissible (width t) (left t))
    (hb : ∀ t, t ≤ K → Admissible (width t) (right t))
    (hw : ∀ t, t < K → width (t+1)=nextWidth (left t) (width t))
    (hl : ∀ t, t < K → ∀ i, i < width (t+1) →
      left (t+1) i = nextColumns (left t) (width t) i)
    (hr : ∀ t, t < K → ∀ i, i < width (t+1) →
      right (t+1) i = nextColumns (right t) (width t) i)
    (hc : ∀ t, t < K → ∀ i, i ≤ width t → carry (left t) i = carry (right t) i)
    (hm : m < width 0)
    (hfirst : ∀ j, j < m → left 0 j = right 0 j) :
    m < width K ∧ (∀ j, j < m → left K j=right K j) ∧
      (left K m : Int)-right K m =
        (2:Int)^(noOverflowCount left width K) * ((left 0 m : Int)-right 0 m) := by
  have hind : ∀ t, t ≤ K → m < width t ∧
      (∀ j, j < m → left t j=right t j) ∧
      (left t m : Int)-right t m =
        (2:Int)^(noOverflowCount left width t) * ((left 0 m : Int)-right 0 m) := by
    intro t
    induction t with
    | zero => intro _; simpa [noOverflowCount] using And.intro hm hfirst
    | succ t ih =>
      intro ht
      obtain ⟨hmt,hlo,hdelta⟩ := ih (by omega)
      have hgt : width t ≤ width (t+1) := by
        rw [hw t (by omega)]
        unfold nextWidth
        split <;> omega
      have hmnext : m < width (t+1) := by omega
      refine ⟨hmnext,?_,?_⟩
      · intro j hj
        rw [hl t (by omega) j (by omega),hr t (by omega) j (by omega)]
        exact next_lower_equal (left t) (right t) (width t) m
          (ha t (by omega)) (hb t (by omega)) hmt hlo (hc t (by omega)) j hj
      · rw [hl t (by omega) m hmnext,hr t (by omega) m hmnext]
        rw [next_first_difference (left t) (right t) (width t) m
          (ha t (by omega)) (hb t (by omega)) hmt hlo (hc t (by omega)),hdelta]
        by_cases ho : carry (left t) (width t)=0
        · simp [noOverflowCount,ho,Int.pow_succ,Int.mul_assoc,Int.mul_comm,Int.mul_left_comm]
        · simp [noOverflowCount,ho]
  exact hind K (by omega)

/-- Five non-overflow steps in identical complete carry histories determine
the whole initial pair-sum word. This does not claim uniqueness of the
initial integer, whose individual digit splits are invisible to q. -/
theorem five_nonoverflows_determine_pair_sums
    (left right : Nat → Nat → Nat) (width : Nat → Nat) (K : Nat)
    (ha : ∀ t, t ≤ K → Admissible (width t) (left t))
    (hb : ∀ t, t ≤ K → Admissible (width t) (right t))
    (hw : ∀ t, t < K → width (t+1)=nextWidth (left t) (width t))
    (hl : ∀ t, t < K → ∀ i, i < width (t+1) →
      left (t+1) i = nextColumns (left t) (width t) i)
    (hr : ∀ t, t < K → ∀ i, i < width (t+1) →
      right (t+1) i = nextColumns (right t) (width t) i)
    (hc : ∀ t, t < K → ∀ i, i ≤ width t → carry (left t) i = carry (right t) i)
    (hfive : 5 ≤ noOverflowCount left width K) :
    ∀ i, i < width 0 → left 0 i=right 0 i := by
  have hpow : ∀ n : Nat, (1:Int) ≤ (2:Int)^n := by
    intro n
    induction n with
    | zero => decide
    | succ n ih => rw [Int.pow_succ]; omega
  have hp : (32:Int) ≤ (2:Int)^(noOverflowCount left width K) := by
    have hsum : noOverflowCount left width K = (noOverflowCount left width K-5) + 5 := by omega
    rw [hsum]
    have := hpow (noOverflowCount left width K-5)
    change 32 ≤ ((((((2:Int)^(noOverflowCount left width K-5))*2)*2)*2)*2)*2
    omega
  intro i
  induction i using Nat.strongRecOn with
  | ind i ih =>
    intro hi
    have hfirst : ∀ j, j < i → left 0 j=right 0 j := by
      intro j hj
      exact ih j hj (by omega)
    obtain ⟨hiK,_,hd⟩ := first_difference_over_time left right width K i
      ha hb hw hl hr hc hi hfirst
    have hleft := (ha K (by omega)).2.2.1 i hiK
    have hright := (hb K (by omega)).2.2.1 i hiK
    by_cases he : left 0 i=right 0 i
    · exact he
    · have hz : (left 0 i : Int)-right 0 i ≤ -1 ∨
          1 ≤ (left 0 i : Int)-right 0 i := by omega
      rcases hz with hz|hz
      · have hmul := Int.mul_le_mul_of_nonneg_left hz
          (by omega : (0:Int) ≤ (2:Int)^noOverflowCount left width K)
        simp only [Int.mul_neg,Int.mul_one] at hmul
        omega
      · have hmul := Int.mul_le_mul_of_nonneg_left hz
          (by omega : (0:Int) ≤ (2:Int)^noOverflowCount left width K)
        simp only [Int.mul_one] at hmul
        omega

open OverflowCarryNormalization

theorem iterPairs_admissible (q : Nat → Nat) (L k : Nat) (ha : Admissible L q) :
    Admissible (iterPairs q L k).1 (iterPairs q L k).2 := by
  induction k with
  | zero => exact ha
  | succ k ih => exact NormalizationBridge.admissible_next _ _ ih

/-- Direct exact-orbit version: equal complete carries through a horizon with
five non-overflows force equality of the initial q words. -/
theorem iterPairs_carry_history_injective (q r : Nat → Nat) (L K : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hc : ∀ t, t < K → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i)
    (hfive : 5 ≤ noOverflowCount (fun t => (iterPairs q L t).2)
      (fun t => (iterPairs q L t).1) K) :
    ∀ i, i < L → q i = r i := by
  have hw : ∀ t, t ≤ K → (iterPairs q L t).1=(iterPairs r L t).1 := by
    intro t
    induction t with
    | zero => intro _; rfl
    | succ t ih =>
      intro ht
      have he := ih (by omega)
      have hcarry := hc t (by omega) (iterPairs q L t).1 (by omega)
      simp only [iterPairs]
      change nextWidth (iterPairs q L t).2 (iterPairs q L t).1 =
        nextWidth (iterPairs r L t).2 (iterPairs r L t).1
      rw [←he]
      unfold nextWidth
      rw [hcarry]
  apply five_nonoverflows_determine_pair_sums
    (fun t => (iterPairs q L t).2) (fun t => (iterPairs r L t).2)
    (fun t => (iterPairs q L t).1) K
  · intro t _; exact iterPairs_admissible q L t hq
  · intro t ht; rw [hw t ht]; exact iterPairs_admissible r L t hr
  · intro t _; rfl
  · intro t _ i _; rfl
  · intro t ht i _
    change nextColumns (iterPairs r L t).2 (iterPairs r L t).1 i =
      nextColumns (iterPairs r L t).2 (iterPairs q L t).1 i
    rw [hw t (by omega)]
  · exact hc
  · exact hfive


#print axioms next_first_difference
#print axioms first_difference_over_time
#print axioms five_nonoverflows_determine_pair_sums
#print axioms iterPairs_carry_history_injective
end CarryHistory



namespace CarryHistory
open DecimalDigits FoldedDecimal OverflowCarryNormalization

/-- A finite outer-digit potential controlling the total number of overflows. -/
def outerPotential : Nat → Nat
  | 4 | 6 | 7 | 8 | 10 | 11 | 12 | 14 => 1
  | 9 | 13 | 15 | 16 | 17 => 2
  | 18 => 3
  | _ => 0

theorem outerPotential_bounded (a : Nat) : outerPotential a ≤ 3 := by
  unfold outerPotential
  split <;> omega

private theorem finite_no_overflow :
    ∀ a ∈ List.range 19, ∀ b ∈ [0,1], 0<a → a+b<10 →
      outerPotential (2*a+b)+1 ≤ outerPotential a+2 := by decide

private theorem finite_overflow :
    ∀ a ∈ List.range 19, ∀ b ∈ [0,1], 0<a → 10≤a+b →
      outerPotential (a+1-10*(a/10))+1 ≤ outerPotential a := by decide

/-- Every exact step satisfies the potential inequality, including the
neutral outer symbol9 and both possible incoming carries from the interior. -/
theorem outer_potential_step (q : Nat → Nat) (L : Nat) (ha : Admissible L q) :
    outerPotential (nextColumns q L 0)+1 ≤ outerPotential (q 0)+
      2*(if carry q L=0 then 1 else 0) := by
  have hL := ha.1
  have houter := ha.2.1
  have hbound := ha.2.2.1 0 hL
  have hs := ha.2.2.2.1 0 hL
  simp only [Nat.sub_zero] at hs
  have hb := carry_bounded q L ha.2.2.1 (L-1) (by omega)
  have hfinal := carry_bounded q L ha.2.2.1 L (by omega)
  have hind : L=(L-1)+1 := by omega
  have hlast : carry q L=(q 0+carry q (L-1))/10 := by
    calc
      carry q L = carry q ((L-1)+1) := congrArg (carry q) hind
      _ = (q (L-1)+carry q (L-1))/10 := rfl
      _ = (q 0+carry q (L-1))/10 := by rw [←hs]
  have hmem : q 0 ∈ List.range 19 := by simp; omega
  have hbmem : carry q (L-1) ∈ [0,1] := by simp; omega
  by_cases hover : carry q L=0
  · have hsmall : q 0+carry q (L-1)<10 := by omega
    have hfirst : carry q 1=0 := by simp only [carry]; omega
    have he := next_column_no_overflow q L 0 hL ha.2.2.2.1 hover
    simp only [Nat.zero_add,Nat.sub_zero,carry,hover,hfirst] at he
    have hv := finite_no_overflow (q 0) hmem (carry q (L-1)) hbmem houter hsmall
    have hout : nextColumns q L 0=2*q 0+carry q (L-1) := by omega
    simpa only [hout,hover,if_true] using hv
  · have hsmall : 10≤q 0+carry q (L-1) := by omega
    have hc : carry q L=1 := by omega
    have he := next_column_overflow_outer q L hL hc
    have hf : carry q 1=q 0/10 := by simp [carry]
    rw [hf] at he
    have hout : nextColumns q L 0=q 0+1-10*(q 0/10) := by omega
    have hv := finite_overflow (q 0) hmem (carry q (L-1)) hbmem houter hsmall
    simpa only [hout,hover,if_false,Nat.mul_zero,Nat.add_zero] using hv

/-- Telescoping the potential bounds the number of non-overflows from below. -/
theorem nonoverflow_growth_bound (q : Nat → Nat) (L K : Nat) (ha : Admissible L q) :
    K ≤ 2*noOverflowCount (fun t => (iterPairs q L t).2)
      (fun t => (iterPairs q L t).1) K + 3 := by
  have hp : ∀ k : Nat,
      outerPotential ((iterPairs q L k).2 0)+k ≤ outerPotential (q 0)+
        2*noOverflowCount (fun t => (iterPairs q L t).2)
          (fun t => (iterPairs q L t).1) k := by
    intro k
    induction k with
    | zero => simp [iterPairs,noOverflowCount]
    | succ k ih =>
      have had := iterPairs_admissible q L k ha
      have hs := outer_potential_step (iterPairs q L k).2 (iterPairs q L k).1 had
      simp only [iterPairs,noOverflowCount]
      omega
  have h := hp K
  have hb := outerPotential_bounded (q 0)
  omega

/-- Twelve complete consecutive carry words determine the initial pair-sum
word. This is a fully numeric exact-dynamics statement, with no unproved
growth assumption and no bound on the number of initial digits. -/
theorem twelve_carry_words_determine_pair_sums (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hc : ∀ t, t < 12 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    ∀ i, i < L → q i=r i := by
  apply iterPairs_carry_history_injective q r L 12 hq hr hc
  have h := nonoverflow_growth_bound q L 12 hq
  omega

#print axioms outer_potential_step
#print axioms nonoverflow_growth_bound
#print axioms twelve_carry_words_determine_pair_sums
end CarryHistory

namespace CarryHistory
open DecimalDigits FoldedDecimal OverflowCarryNormalization

theorem four_nonoverflows_and_endpoint_determine_pair_sums
    (left right : Nat → Nat → Nat) (width : Nat → Nat) (K : Nat)
    (ha : ∀ t, t ≤ K → Admissible (width t) (left t))
    (hb : ∀ t, t ≤ K → Admissible (width t) (right t))
    (hw : ∀ t, t < K → width (t+1)=nextWidth (left t) (width t))
    (hl : ∀ t, t < K → ∀ i, i < width (t+1) →
      left (t+1) i = nextColumns (left t) (width t) i)
    (hr : ∀ t, t < K → ∀ i, i < width (t+1) →
      right (t+1) i = nextColumns (right t) (width t) i)
    (hc : ∀ t, t ≤ K → ∀ i, i ≤ width t → carry (left t) i = carry (right t) i)
    (hfour : 4 ≤ noOverflowCount left width K) :
    ∀ i, i < width 0 → left 0 i=right 0 i := by
  have hpow : ∀ n : Nat, (1:Int) ≤ (2:Int)^n := by
    intro n
    induction n with
    | zero => decide
    | succ n ih => rw [Int.pow_succ]; omega
  have hp : (16:Int) ≤ (2:Int)^(noOverflowCount left width K) := by
    have hsum : noOverflowCount left width K = (noOverflowCount left width K-4) + 4 := by omega
    rw [hsum]
    have := hpow (noOverflowCount left width K-4)
    change 16 ≤ (((((2:Int)^(noOverflowCount left width K-4))*2)*2)*2)*2
    omega
  intro i
  induction i using Nat.strongRecOn with
  | ind i ih =>
    intro hi
    have hfirst : ∀ j, j < i → left 0 j=right 0 j := by
      intro j hj
      exact ih j hj (by omega)
    obtain ⟨hiK,_,hd⟩ := first_difference_over_time left right width K i
      ha hb hw hl hr (fun t ht => hc t (by omega)) hi hfirst
    have hleft := output_bounded (left K) i
    have hright := output_bounded (right K) i
    have hle := column_equation (left K) i
    have hre := column_equation (right K) i
    rw [←hc K (by omega) i (by omega), ←hc K (by omega) (i+1) (by omega)] at hre
    by_cases he : left 0 i=right 0 i
    · exact he
    · have hz : (left 0 i : Int)-right 0 i ≤ -1 ∨
          1 ≤ (left 0 i : Int)-right 0 i := by omega
      rcases hz with hz|hz
      · have hmul := Int.mul_le_mul_of_nonneg_left hz
          (by omega : (0:Int) ≤ (2:Int)^noOverflowCount left width K)
        simp only [Int.mul_neg,Int.mul_one] at hmul
        omega
      · have hmul := Int.mul_le_mul_of_nonneg_left hz
          (by omega : (0:Int) ≤ (2:Int)^noOverflowCount left width K)
        simp only [Int.mul_one] at hmul
        omega

theorem iterPairs_endpoint_carry_history_injective (q r : Nat → Nat) (L K : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hc : ∀ t, t ≤ K → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i)
    (hfour : 4 ≤ noOverflowCount (fun t => (iterPairs q L t).2)
      (fun t => (iterPairs q L t).1) K) :
    ∀ i, i < L → q i = r i := by
  have hw : ∀ t, t ≤ K → (iterPairs q L t).1=(iterPairs r L t).1 := by
    intro t
    induction t with
    | zero => intro _; rfl
    | succ t ih =>
      intro ht
      have he := ih (by omega)
      have hcarry := hc t (by omega) (iterPairs q L t).1 (by omega)
      simp only [iterPairs]
      change nextWidth (iterPairs q L t).2 (iterPairs q L t).1 =
        nextWidth (iterPairs r L t).2 (iterPairs r L t).1
      rw [←he]
      unfold nextWidth
      rw [hcarry]
  apply four_nonoverflows_and_endpoint_determine_pair_sums
    (fun t => (iterPairs q L t).2) (fun t => (iterPairs r L t).2)
    (fun t => (iterPairs q L t).1) K
  · intro t _; exact iterPairs_admissible q L t hq
  · intro t ht; rw [hw t ht]; exact iterPairs_admissible r L t hr
  · intro t _; rfl
  · intro t _ i _; rfl
  · intro t ht i _
    change nextColumns (iterPairs r L t).2 (iterPairs r L t).1 i =
      nextColumns (iterPairs r L t).2 (iterPairs q L t).1 i
    rw [hw t (by omega)]
  · exact hc
  · exact hfour


/-- Eleven complete carry words determine the pair-sum state. The endpoint
carry word narrows each possible difference to[-9,9], sharpening the
previous twelve-word bound. This statement does not claim optimality. -/
theorem eleven_carry_words_determine_pair_sums (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hc : ∀ t, t < 11 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    ∀ i, i < L → q i=r i := by
  apply iterPairs_endpoint_carry_history_injective q r L 10 hq hr
  · intro t ht i hi
    exact hc t (by omega) i hi
  · have h := nonoverflow_growth_bound q L 10 hq
    omega

#print axioms four_nonoverflows_and_endpoint_determine_pair_sums
#print axioms eleven_carry_words_determine_pair_sums
end CarryHistory


/-!
Fixed-width numerical injectivity of symmetric reverse-and-add column words.

This concerns `DecimalDigits.value q L`, the numerical value after adding
the original integer to its reversal. It does not claim injectivity of the
autonomous map `FoldedDecimal.nextColumns`, which has large fibers.
-/

namespace ReverseAddInverse

open DecimalDigits FoldedDecimal

/-- Equal bounded output digits and equal final carries determine every carry
when the two input column words are symmetric. The initial carries are zero
by the definition of `carry`. -/
theorem carries_equal_of_symmetric_output_equal
    (q r : Nat → Nat) (L : Nat)
    (hq : ∀ i, i < L → q i ≤ 18)
    (hr : ∀ i, i < L → r i ≤ 18)
    (hqs : ∀ i, i < L → q i = q (L - 1 - i))
    (hrs : ∀ i, i < L → r i = r (L - 1 - i))
    (hout : ∀ i, i < L → output q i = output r i)
    (hend : carry q L = carry r L) :
    ∀ i, i ≤ L → carry q i = carry r i := by
  have hp : ∀ k, k ≤ L →
      carry q k = carry r k ∧ carry q (L-k) = carry r (L-k) := by
    intro k
    induction k with
    | zero =>
      intro _
      exact ⟨rfl, by simpa using hend⟩
    | succ k ih =>
      intro hk
      obtain ⟨hl, hh⟩ := ih (by omega)
      have hkL : k < L := by omega
      have hjL : L-1-k < L := by omega
      have hjnext : L-1-k+1 = L-k := by omega
      have hj : L-1-k = L-(k+1) := by omega
      have hqi := column_equation q k
      have hri := column_equation r k
      have hqj := column_equation q (L-1-k)
      have hrj := column_equation r (L-1-k)
      have hoi := hout k hkL
      have hoj := hout (L-1-k) hjL
      have hsq := hqs k hkL
      have hsr := hrs k hkL
      have hbq := carry_bounded q L hq (L-1-k) (by omega)
      have hbr := carry_bounded r L hr (L-1-k) (by omega)
      rw [hjnext] at hqj hrj
      constructor
      · omega
      · rw [←hj]
        omega
  intro i hi
  exact (hp i hi).1

/-- Fixed-width numerical evaluation is injective on symmetric column words
with coefficients at most 18. No positivity or center-parity assumption is
needed for this stronger algebraic statement. -/
theorem symmetric_value_injective
    (q r : Nat → Nat) (L : Nat)
    (hq : ∀ i, i < L → q i ≤ 18)
    (hr : ∀ i, i < L → r i ≤ 18)
    (hqs : ∀ i, i < L → q i = q (L - 1 - i))
    (hrs : ∀ i, i < L → r i = r (L - 1 - i))
    (heq : value q L = value r L) :
    ∀ i, i < L → q i = r i := by
  have hext : value (extended q L) (L+1) =
      value (extended r L) (L+1) := by
    rw [value_extended, value_extended, value_output, value_output]
    exact heq
  have hqb : ∀ i, i < L+1 → extended q L i ≤ 9 := by
    intro i _
    unfold extended
    split
    · exact output_bounded q i
    · have := carry_bounded q L hq L (Nat.le_refl L)
      omega
  have hrb : ∀ i, i < L+1 → extended r L i ≤ 9 := by
    intro i _
    unfold extended
    split
    · exact output_bounded r i
    · have := carry_bounded r L hr L (Nat.le_refl L)
      omega
  have hd := value_injective (extended q L) (extended r L) (L+1)
    hqb hrb hext
  have hout : ∀ i, i < L → output q i = output r i := by
    intro i hi
    have := hd i (by omega)
    simpa only [extended, if_pos hi] using this
  have hend : carry q L = carry r L := by
    have := hd L (by omega)
    simpa [extended] using this
  have hc := carries_equal_of_symmetric_output_equal q r L hq hr hqs hrs hout hend
  intro i hi
  have hqi := column_equation q i
  have hri := column_equation r i
  have ho := hout i hi
  have hci := hc i (by omega)
  have hcn := hc (i+1) (by omega)
  omega

/-- Actual positive decimal integers of the same width have the same first
reverse-and-add value exactly when their symmetric digit-pair sums agree.
This does not determine the original digit split: for example 196 and 295
have the same pair-sum word and the same first value 887. -/
theorem same_width_step_eq_iff_pair_sums
    (n m : Nat) (d e : Nat → Nat) (L : Nat)
    (hn : Canonical n d L) (hm : Canonical m e L) :
    Lychrel196.step n = Lychrel196.step m ↔
      ∀ i, i < L → columnSum d L i = columnSum e L i := by
  have hnval := step_eq_word_value n d (columnSum d L) L hn
    (fun _ _ => rfl)
  have hmval := step_eq_word_value m e (columnSum e L) L hm
    (fun _ _ => rfl)
  constructor
  · intro hstep
    apply symmetric_value_injective (columnSum d L) (columnSum e L) L
      (columnSum_bounded d L hn.2.1) (columnSum_bounded e L hm.2.1)
      (columnSum_symmetric d L) (columnSum_symmetric e L)
    omega
  · intro hp
    rw [hnval, hmval]
    exact value_congr _ _ L hp

#print axioms carries_equal_of_symmetric_output_equal
#print axioms symmetric_value_injective
#print axioms same_width_step_eq_iff_pair_sums

end ReverseAddInverse


/-! All-time decimal width bounds, including an actual-orbit specialization to196.
These are growth bounds and do not assert palindrome avoidance. -/

namespace DecimalWidthGrowth
open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory

/-- A lower-growth potential for the exact outer-column automaton. -/
def lowerPotential : Nat → Nat
  | 1 => 4
  | 2 => 3
  | 3 | 4 | 5 => 2
  | 6 | 7 | 8 | 9 | 10 => 1
  | _ => 0

theorem lowerPotential_bounded (a : Nat) : lowerPotential a ≤ 4 := by
  unfold lowerPotential
  split <;> omega

private theorem finite_no_overflow :
    ∀ a ∈ List.range 19, ∀ b ∈ [0,1], 0<a → a+b<10 →
      lowerPotential (2*a+b)+1 ≤ lowerPotential a := by decide

private theorem finite_overflow :
    ∀ a ∈ List.range 19, ∀ b ∈ [0,1], 0<a → 10≤a+b →
      lowerPotential (a+1-10*(a/10))+1 ≤ lowerPotential a+4 := by decide

/-- Every actual addition pays for one unit of time with four units per overflow. -/
theorem lower_potential_step (q : Nat → Nat) (L : Nat) (ha : Admissible L q) :
    lowerPotential (nextColumns q L 0)+1+4*L ≤
      lowerPotential (q 0)+4*nextWidth q L := by
  have hL := ha.1
  have houter := ha.2.1
  have hbound := ha.2.2.1 0 hL
  have hs := ha.2.2.2.1 0 hL
  simp only [Nat.sub_zero] at hs
  have hb := carry_bounded q L ha.2.2.1 (L-1) (by omega)
  have hfinal := carry_bounded q L ha.2.2.1 L (by omega)
  have hind : L=(L-1)+1 := by omega
  have hlast : carry q L=(q 0+carry q (L-1))/10 := by
    calc
      carry q L = carry q ((L-1)+1) := congrArg (carry q) hind
      _ = (q (L-1)+carry q (L-1))/10 := rfl
      _ = (q 0+carry q (L-1))/10 := by rw [←hs]
  have hmem : q 0 ∈ List.range 19 := by simp; omega
  have hbmem : carry q (L-1) ∈ [0,1] := by simp; omega
  by_cases hover : carry q L=0
  · have hsmall : q 0+carry q (L-1)<10 := by omega
    have hfirst : carry q 1=0 := by simp only [carry]; omega
    have he := next_column_no_overflow q L 0 hL ha.2.2.2.1 hover
    simp only [Nat.zero_add,Nat.sub_zero,carry,hover,hfirst] at he
    have hv := finite_no_overflow (q 0) hmem (carry q (L-1)) hbmem houter hsmall
    have hout : nextColumns q L 0=2*q 0+carry q (L-1) := by omega
    rw [hout, nextWidth, if_pos hover]
    omega
  · have hsmall : 10≤q 0+carry q (L-1) := by omega
    have hc : carry q L=1 := by omega
    have he := next_column_overflow_outer q L hL hc
    have hf : carry q 1=q 0/10 := by simp [carry]
    rw [hf] at he
    have hout : nextColumns q L 0=q 0+1-10*(q 0/10) := by omega
    have hv := finite_overflow (q 0) hmem (carry q (L-1)) hbmem houter hsmall
    rw [hout, nextWidth, if_neg hover]
    omega

/-- The sharper lower bound retains the initial outer-column potential. -/
theorem width_lower_potential (q : Nat → Nat) (L K : Nat) (ha : Admissible L q) :
    K+4*L ≤ 4*(iterPairs q L K).1+lowerPotential (q 0) := by
  have hp : ∀ k : Nat,
      lowerPotential ((iterPairs q L k).2 0)+k+4*L ≤
        lowerPotential (q 0)+4*(iterPairs q L k).1 := by
    intro k
    induction k with
    | zero => simp [iterPairs]
    | succ k ih =>
      have hs := lower_potential_step (iterPairs q L k).2
        (iterPairs q L k).1 (iterPairs_admissible q L k ha)
      simp only [iterPairs]
      omega
  have h := hp K
  omega

/-- A uniform all-time lower bound: width increases at least (K-4)/4. -/
theorem width_lower_bound (q : Nat → Nat) (L K : Nat) (ha : Admissible L q) :
    K+4*L ≤ 4*(iterPairs q L K).1+4 := by
  have h := width_lower_potential q L K ha
  have hb := lowerPotential_bounded (q 0)
  omega

theorem width_count_identity (q : Nat → Nat) (L K : Nat) :
    (iterPairs q L K).1+
      noOverflowCount (fun t => (iterPairs q L t).2)
        (fun t => (iterPairs q L t).1) K = L+K := by
  induction K with
  | zero => simp [iterPairs,noOverflowCount]
  | succ K ih =>
    simp only [iterPairs,noOverflowCount,nextWidth]
    split <;> omega

/-- The pre-existing nonoverflow potential gives the matching upper bound. -/
theorem width_upper_bound (q : Nat → Nat) (L K : Nat) (ha : Admissible L q) :
    2*(iterPairs q L K).1 ≤ 2*L+K+3 := by
  have hc := width_count_identity q L K
  have hn := nonoverflow_growth_bound q L K ha
  omega

/-- The sharper upper bound retains the initial outer-column potential. -/
theorem width_upper_potential (q : Nat → Nat) (L K : Nat) (ha : Admissible L q) :
    2*(iterPairs q L K).1 ≤ 2*L+K+outerPotential (q 0) := by
  have hp : ∀ k : Nat,
      outerPotential ((iterPairs q L k).2 0)+k ≤ outerPotential (q 0)+
        2*noOverflowCount (fun t => (iterPairs q L t).2)
          (fun t => (iterPairs q L t).1) k := by
    intro k
    induction k with
    | zero => simp [iterPairs,noOverflowCount]
    | succ k ih =>
      have hs := outer_potential_step (iterPairs q L k).2
        (iterPairs q L k).1 (iterPairs_admissible q L k ha)
      simp only [iterPairs,noOverflowCount]
      omega
  have h := hp K
  have hc := width_count_identity q L K
  omega

/-- Numeric orbit version, with W the actual canonical decimal width. -/
theorem numeric_width_bounds (n : Nat) (d : Nat → Nat) (L K : Nat)
    (hc : Canonical n d L) :
    ∃ e W, Canonical (Lychrel196.orbit n K) e W ∧
      K+4*L ≤ 4*W+4 ∧ 2*W ≤ 2*L+K+3 := by
  have ha := NormalizationBridge.canonical_admissible n d L hc
  obtain ⟨e, he, _⟩ := iterPairs_representation n d (columnSum d L) L K hc
    (fun _ _ => rfl)
  exact ⟨e, (iterPairs (columnSum d L) L K).1, he,
    width_lower_bound (columnSum d L) L K ha,
    width_upper_bound (columnSum d L) L K ha⟩

def digits196 (i : Nat) : Nat := if i=0 then 6 else if i=1 then 9 else 1

private theorem canonical196 : Canonical 196 digits196 3 := by
  refine ⟨by decide, ?_, by decide, by decide⟩
  intro i hi
  have he : i=0 ∨ i=1 ∨ i=2 := by omega
  rcases he with rfl | rfl | rfl <;> decide

/-- For 196 specifically, the actual decimal width W satisfies
    (K+11)/4 ≤ W ≤ (K+7)/2 for every K. These are growth bounds only. -/
theorem numeric196_width_bounds (K : Nat) :
    ∃ e W, Canonical (Lychrel196.orbit 196 K) e W ∧
      K+11 ≤ 4*W ∧ 2*W ≤ K+7 := by
  let q := columnSum digits196 3
  have ha : Admissible 3 q := NormalizationBridge.canonical_admissible
    196 digits196 3 canonical196
  obtain ⟨e, he, _⟩ := iterPairs_representation 196 digits196 q 3 K canonical196
    (fun _ _ => rfl)
  have hl := width_lower_potential q 3 K ha
  have hu := width_upper_potential q 3 K ha
  have hlp : lowerPotential (q 0)=1 := by decide
  have hup : outerPotential (q 0)=1 := by decide
  refine ⟨e, (iterPairs q 3 K).1, he, ?_, ?_⟩ <;> omega

#print axioms lower_potential_step
#print axioms width_lower_bound
#print axioms width_upper_bound
#print axioms numeric_width_bounds
#print axioms numeric196_width_bounds
end DecimalWidthGrowth


/-! Astra research pass: independently checked modular ingredients. -/

/-!
Unconditional decimal modular theorems, connected to the executable ordinary
reversal and canonical numeral semantics in `Lychrel196Research`.

This file does not formalize arbitrary-modulus palindrome residue saturation,
and does not prove a decimal Lychrel existence statement.
-/

namespace AstraModular

set_option maxRecDepth 10000

open Lychrel196 DecimalDigits FoldedDecimal OverflowCarryNormalization

theorem ten_pow_mod99 (L : Nat) :
    10 ^ L % 99 = if L % 2 = 0 then 1 else 10 := by
  induction L with
  | zero => decide
  | succ L ih =>
    rw [Nat.pow_succ, Nat.mul_mod, ih]
    by_cases h : L % 2 = 0
    · have hs : (L + 1) % 2 ≠ 0 := by omega
      simp [h, hs]
    · have hs : (L + 1) % 2 = 0 := by omega
      simp [h, hs]

/-- Exact reflection arithmetic; no bounded-digit assumption is needed. -/
theorem reflected_mod99 (d : Nat → Nat) (L : Nat) :
    value (reflected d L) L % 99 =
      ((if L % 2 = 0 then 10 else 1) * value d L) % 99 := by
  induction L generalizing d with
  | zero => simp [value]
  | succ L ih =>
    have ht := ih (fun i => d (i + 1))
    have hp := ten_pow_mod99 L
    rw [reflected_value_shift, value_shift]
    by_cases h : L % 2 = 0
    · have hs : (L + 1) % 2 ≠ 0 := by omega
      simp only [h, hs, ↓reduceIte] at ht hp ⊢
      simp only [Nat.add_mod, Nat.mul_mod, hp, ht, Nat.mod_mod,
        Nat.one_mul, Nat.mul_one]
      simp only [Nat.reduceMod] at *
      omega
    · have hs : (L + 1) % 2 = 0 := by omega
      simp only [h, hs, ↓reduceIte] at ht hp ⊢
      simp only [Nat.add_mod, Nat.mul_mod, hp, ht, Nat.mod_mod,
        Nat.one_mul, Nat.mul_one]
      simp only [Nat.reduceMod] at *
      omega

/-- Ordinary reversal is determined modulo 99 by residue and exact width. -/
theorem reverse10_mod99 (n : Nat) (d : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) :
    reverse10 n % 99 = ((if L % 2 = 0 then 10 else 1) * n) % 99 := by
  rcases hc with ⟨hL, hd, hp, rfl⟩
  rw [reverse10_value d L hd (Or.inr hp)]
  exact reflected_mod99 d L

/-- Each even-width step multiplies the residue by 11; each odd-width step
multiplies it by 2. This statement concerns actual finite decimal integers. -/
theorem step_mod99 (n : Nat) (d : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) :
    step n % 99 = ((if L % 2 = 0 then 11 else 2) * n) % 99 := by
  have hr := reverse10_mod99 n d L hc
  change (n + reverse10 n) % 99 = _
  rw [Nat.add_mod, hr]
  by_cases h : L % 2 = 0
  · simp only [if_pos h]
    omega
  · simp only [if_neg h, Nat.one_mul]
    omega

theorem reverse10_mod_of_dvd99 (M n : Nat) (d : Nat → Nat) (L : Nat)
    (hM : M ∣ 99) (hc : Canonical n d L) :
    reverse10 n % M = ((if L % 2 = 0 then 10 else 1) * n) % M := by
  have h := congrArg (fun x => x % M) (reverse10_mod99 n d L hc)
  simpa only [Nat.mod_mod_of_dvd _ hM] using h

theorem step_mod_of_dvd99 (M n : Nat) (d : Nat → Nat) (L : Nat)
    (hM : M ∣ 99) (hc : Canonical n d L) :
    step n % M = ((if L % 2 = 0 then 11 else 2) * n) % M := by
  have h := congrArg (fun x => x % M) (step_mod99 n d L hc)
  simpa only [Nat.mod_mod_of_dvd _ hM] using h

theorem even_width_step_dvd11 (n : Nat) (d : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) (he : L % 2 = 0) : 11 ∣ step n := by
  have h := step_mod_of_dvd99 11 n d L (by decide) hc
  simp only [if_pos he] at h
  exact Nat.dvd_of_mod_eq_zero (by omega)

theorem step_preserves_dvd11 (n : Nat) (h : 11 ∣ n) : 11 ∣ step n := by
  by_cases hn : n = 0
  · subst n
    decide
  · obtain ⟨d, L, hc⟩ := canonical_exists n (by omega)
    have hr := step_mod_of_dvd99 11 n d L (by decide) hc
    have hz := Nat.mod_eq_zero_of_dvd h
    apply Nat.dvd_of_mod_eq_zero
    by_cases he : L % 2 = 0
    · simp only [if_pos he] at hr
      omega
    · simp only [if_neg he] at hr
      omega

theorem orbit_preserves_dvd11 (n k : Nat) (h : 11 ∣ n) :
    11 ∣ orbit n k := by
  induction k with
  | zero => exact h
  | succ k ih => exact step_preserves_dvd11 (orbit n k) ih

/-- If all widths seen so far are odd, width cannot yet have increased. -/
theorem all_odd_widths_constant (q : Nat → Nat) (L K : Nat)
    (h : ∀ k, k ≤ K → (iterPairs q L k).1 % 2 ≠ 0) :
    (iterPairs q L K).1 = L := by
  induction K with
  | zero => rfl
  | succ K ih =>
    have hi := ih (fun k hk => h k (by omega))
    have ho := h K (by omega)
    have hn := h (K + 1) (by omega)
    simp only [iterPairs, nextWidth] at hn ⊢
    by_cases hb : carry (iterPairs q L K).2 (iterPairs q L K).1 = 0
    · simp only [if_pos hb] at hn ⊢
      omega
    · simp only [if_neg hb] at hn ⊢
      omega

/-- Every admissible decimal orbit encounters an even input width by time 5. -/
theorem exists_even_width_by_five (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) :
    ∃ k, k ≤ 5 ∧ (iterPairs q L k).1 % 2 = 0 := by
  apply Classical.byContradiction
  intro h
  have ho : ∀ k, k ≤ 5 → (iterPairs q L k).1 % 2 ≠ 0 := by
    intro k hk he
    exact h ⟨k, hk, he⟩
  have hc := all_odd_widths_constant q L 5 ho
  have hg := DecimalWidthGrowth.width_lower_bound q L 5 ha
  omega

/-- Uniform numeric theorem: after six reverse-and-add steps every positive
integer is divisible by 11, and this remains true at every later time. -/
theorem orbit_six_dvd11 (n : Nat) (hn : 0 < n) : 11 ∣ orbit n 6 := by
  obtain ⟨d, L, hc⟩ := canonical_exists n hn
  have ha := NormalizationBridge.canonical_admissible n d L hc
  obtain ⟨k, hk, he⟩ := exists_even_width_by_five (columnSum d L) L ha
  obtain ⟨e, hec, _⟩ := iterPairs_representation n d (columnSum d L) L k hc
    (fun _ _ => rfl)
  have hd : 11 ∣ orbit n (k + 1) := even_width_step_dvd11
    (orbit n k) e (iterPairs (columnSum d L) L k).1 hec he
  have ht := orbit_preserves_dvd11 (orbit n (k + 1)) (5 - k) hd
  rw [← LychrelCertificates.orbit_add] at ht
  have hi : k + 1 + (5 - k) = 6 := by omega
  rwa [hi] at ht

theorem orbit_eventually_dvd11 (n k : Nat) (hn : 0 < n) :
    11 ∣ orbit n (6 + k) := by
  have h := orbit_preserves_dvd11 (orbit n 6) k (orbit_six_dvd11 n hn)
  simpa only [← LychrelCertificates.orbit_add] using h

theorem orbit_mod11_eq_zero_of_six_le (n k : Nat) (hn : 0 < n)
    (hk : 6 ≤ k) : orbit n k % 11 = 0 := by
  have h := orbit_eventually_dvd11 n (k - 6) hn
  have he : 6 + (k - 6) = k := by omega
  rw [he] at h
  exact Nat.mod_eq_zero_of_dvd h

set_option maxHeartbeats 0 in
/-- Six cannot be replaced by five in the uniform theorem. -/
theorem six_step_bound_sharp :
    (∀ k ∈ List.range 6, ¬ 11 ∣ orbit 100 k) ∧ 11 ∣ orbit 100 6 := by
  decide

/-- The units digit of an ordinary reversal is its nonzero original lead. -/
theorem reverse10_mod10 (n : Nat) (d : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) : reverse10 n % 10 = d (L - 1) := by
  rcases hc with ⟨hL, hd, hp, rfl⟩
  rw [reverse10_value d L hd (Or.inr hp)]
  obtain ⟨k, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : L ≠ 0)
  rw [value_shift]
  have hb := hd k (by omega)
  simp only [reflected, Nat.add_sub_cancel, Nat.succ_sub_one, Nat.sub_zero]
  omega

/-- A zero units digit cannot persist for two successive positive iterates. -/
theorem zero_units_step_nonzero (n : Nat) (hn : 0 < n)
    (hz : n % 10 = 0) : step n % 10 ≠ 0 := by
  obtain ⟨d, L, hc⟩ := canonical_exists n hn
  have hr := reverse10_mod10 n d L hc
  have hp := hc.2.2.1
  have hL := hc.1
  have hb := hc.2.1 (L - 1) (by omega)
  change (n + reverse10 n) % 10 ≠ 0
  omega

theorem no_consecutive_zero_units (n : Nat) (hn : 0 < n) (k : Nat) :
    ¬ (10 ∣ orbit n k ∧ 10 ∣ orbit n (k + 1)) := by
  intro h
  have hpos := DecimalDigits.orbit_positive n hn k
  have hh := zero_units_step_nonzero (orbit n k) hpos
    (Nat.mod_eq_zero_of_dvd h.1)
  exact hh (Nat.mod_eq_zero_of_dvd h.2)

/-- At every sufficiently late time, one of two consecutive iterates meets
both local compatibility conditions of fixed-modulus palindrome saturation. -/
theorem late_compatible_state (n k : Nat) (hn : 0 < n) :
    ∃ j, 6 + k ≤ j ∧ j ≤ 7 + k ∧
      11 ∣ orbit n j ∧ ¬ 10 ∣ orbit n j := by
  by_cases hz : 10 ∣ orbit n (6 + k)
  · refine ⟨7 + k, by omega, by omega, ?_, ?_⟩
    · have h := orbit_eventually_dvd11 n (k + 1) hn
      have hi : 6 + (k + 1) = 7 + k := by omega
      rwa [hi] at h
    · intro hb
      apply no_consecutive_zero_units n hn (6 + k)
      refine ⟨hz, ?_⟩
      have hi : 6 + k + 1 = 7 + k := by omega
      rwa [hi]
  · exact ⟨6 + k, by omega, by omega, orbit_eventually_dvd11 n k hn, hz⟩

/-- Actual orbit states satisfy all the arithmetic compatibility conditions
at arbitrarily large canonical widths, with an explicit linear time bound.
This is not a palindrome-existence or palindrome-avoidance theorem. -/
theorem large_width_compatible_state (n B : Nat) (hn : 0 < n) :
    ∃ j e W, 6 + 4 * B ≤ j ∧ j ≤ 7 + 4 * B ∧
      Canonical (orbit n j) e W ∧ B ≤ W ∧
      11 ∣ orbit n j ∧ ¬ 10 ∣ orbit n j := by
  obtain ⟨d, L, hc⟩ := canonical_exists n hn
  obtain ⟨j, hjlo, hjhi, h11, h10⟩ := late_compatible_state n (4 * B) hn
  obtain ⟨e, W, he, hg, _⟩ := DecimalWidthGrowth.numeric_width_bounds n d L j hc
  refine ⟨j, e, W, hjlo, hjhi, he, ?_, h11, h10⟩
  omega

/-- The preceding orbit state also meets the compatibility conditions after
reduction modulo any fixed M, including the even-width factor gcd(M,11). -/
theorem large_width_compatible_residue (M n B : Nat) (hn : 0 < n) :
    ∃ j e W, 6 + 4 * B ≤ j ∧ j ≤ 7 + 4 * B ∧
      Canonical (orbit n j) e W ∧ B ≤ W ∧
      ¬ (10 ∣ M ∧ 10 ∣ (orbit n j % M)) ∧
      (W % 2 = 0 → Nat.gcd M 11 ∣ (orbit n j % M)) := by
  obtain ⟨j, e, W, hjlo, hjhi, hc, hB, h11, h10⟩ :=
    large_width_compatible_state n B hn
  refine ⟨j, e, W, hjlo, hjhi, hc, hB, ?_, ?_⟩
  · intro h
    exact h10 ((Nat.dvd_mod_iff h.1).mp h.2)
  · intro _
    exact (Nat.dvd_mod_iff (Nat.gcd_dvd_left M 11)).mpr
      (Nat.dvd_trans (Nat.gcd_dvd_right M 11) h11)

/-- Every symmetric even-width coefficient word has value divisible by 11;
coefficients can be arbitrary natural numbers, not just decimal digits. -/
theorem even_symmetric_value_dvd11 (d : Nat → Nat) (L : Nat)
    (he : L % 2 = 0) (hs : ∀ i, i < L → d i = d (L - 1 - i)) :
    11 ∣ value d L := by
  have hv : value (reflected d L) L = value d L := by
    apply value_congr
    intro i hi
    exact (hs i hi).symm
  have hr := reflected_mod99 d L
  rw [hv, if_pos he] at hr
  apply Nat.dvd_of_mod_eq_zero
  omega

theorem value_scale (a : Nat) (d : Nat → Nat) (L : Nat) :
    value (fun i => a * d i) L = a * value d L := by
  induction L with
  | zero => simp [value]
  | succ L ih => simp only [value, ih, Nat.mul_add, Nat.mul_assoc]

/-- An overflow to a palindrome from an even input width forces a second
factor of 11, beyond the universal eventual single factor. -/
theorem even_width_palindromic_overflow_dvd121
    (n : Nat) (d : Nat → Nat) (L : Nat) (hc : Canonical n d L)
    (he : L % 2 = 0) (ho : carry (columnSum d L) L = 1)
    (hp : Palindrome (step n)) : 121 ∣ step n := by
  have hpc : Palindrome (step (value d L)) := by rwa [hc.2.2.2]
  have hq := (step_palindrome_iff_overflow d L hc.1 hc.2.1 hc.2.2.1 ho).mp hpc
  let b : Nat → Nat := fun i => columnSum d L i / 11
  have hb : ∀ i, i < L → b i = b (L - 1 - i) := by
    intro i hi
    exact congrArg (fun x => x / 11) (columnSum_symmetric d L i hi)
  have hd := even_symmetric_value_dvd11 b L he hb
  have hscale : value (columnSum d L) L = 11 * value b L := by
    rw [← value_scale]
    apply value_congr
    intro i hi
    have hqi := hq.2 i hi
    dsimp [b]
    omega
  have hstep := FoldedDecimal.step_eq_word_value n d (columnSum d L) L hc
    (fun _ _ => rfl)
  rcases hd with ⟨k, hk⟩
  refine ⟨k, ?_⟩
  rw [hstep, hscale, hk]
  omega

theorem even_width_overflow_not_palindrome_of_not_dvd121
    (n : Nat) (d : Nat → Nat) (L : Nat) (hc : Canonical n d L)
    (he : L % 2 = 0) (ho : carry (columnSum d L) L = 1)
    (h : ¬ 121 ∣ step n) : ¬ Palindrome (step n) := by
  intro hp
  exact h (even_width_palindromic_overflow_dvd121 n d L hc he ho hp)

#print axioms reverse10_mod99
#print axioms step_mod99
#print axioms orbit_eventually_dvd11
#print axioms orbit_mod11_eq_zero_of_six_le
#print axioms six_step_bound_sharp
#print axioms no_consecutive_zero_units
#print axioms late_compatible_state
#print axioms large_width_compatible_residue
#print axioms even_width_palindromic_overflow_dvd121

end AstraModular


/-! Astra research pass: correlated-column identities and counterexamples. -/

/-!
Exact local carry-complement identities and a checked obstruction to a
correlated folded-word candidate.  This file does not prove a Lychrel number
exists.  It imports no unproved research hypotheses.
-/

namespace AstraLanguages

def carry (q : Nat → Nat) : Nat → Nat
  | 0 => 0
  | i + 1 => (q i + carry q i) / 10

def digit (q : Nat → Nat) (i : Nat) : Nat :=
  (q i + carry q i) % 10

theorem complementary_column (q r a b : Nat)
    (hq : q + r = 18) (ha : a + b = 1) :
    (q + a) / 10 + (r + b) / 10 = 1 ∧
    (q + a) % 10 + (r + b) % 10 = 9 := by
  omega

/-- Equal zero incoming carries are repaired at the first non-neutral
complementary pair.  At that pair the output digits sum to eight. -/
theorem mismatched_column_repair (q r : Nat)
    (hq : q + r = 18) (hne : q ≠ 9) :
    q / 10 + r / 10 = 1 ∧ q % 10 + r % 10 = 8 := by
  omega

theorem neutral_column_preserves_mismatch :
    9 / 10 + 9 / 10 = 0 ∧ 9 % 10 + 9 % 10 = 18 := by
  decide

/-- A half-word carry of one makes an anti-complementary q word produce
complementary digit halves, at every finite width. -/
theorem half_complement_carries (q : Nat → Nat) (s : Nat)
    (hp : ∀ i, i < s → q i + q (s + i) = 18)
    (hm : carry q s = 1) :
    ∀ i, i ≤ s → carry q i + carry q (s + i) = 1 := by
  intro i
  induction i with
  | zero =>
      intro _
      simpa [carry] using hm
  | succ i ih =>
      intro hi
      have ha := ih (by omega)
      have hx := (complementary_column (q i) (q (s + i))
        (carry q i) (carry q (s + i)) (hp i (by omega)) ha).1
      have hs : s + (i + 1) = (s + i) + 1 := by omega
      simpa only [hs, carry] using hx

theorem half_complement_digits (q : Nat → Nat) (s : Nat)
    (hp : ∀ i, i < s → q i + q (s + i) = 18)
    (hm : carry q s = 1) :
    ∀ i, i < s → digit q i + digit q (s + i) = 9 := by
  intro i hi
  exact (complementary_column (q i) (q (s + i))
    (carry q i) (carry q (s + i)) (hp i hi)
    (half_complement_carries q s hp hm i (by omega))).2

theorem half_complement_no_overflow (q : Nat → Nat) (s : Nat)
    (hp : ∀ i, i < s → q i + q (s + i) = 18)
    (hm : carry q s = 1) : carry q (2 * s) = 0 := by
  have hx := half_complement_carries q s hp hm s (by omega)
  have hs : s + s = 2 * s := by omega
  rw [hm, hs] at hx
  omega

def addColumns : List Nat → Nat → List Nat
  | [], 0 => []
  | [], c => [c]
  | q :: qs, c => (q + c) % 10 :: addColumns qs ((q + c) / 10)

def qstep (q : List Nat) : List Nat :=
  let d := addColumns q 0
  List.zipWith (fun a b => a + b) d d.reverse

def lowOnly (q : List Nat) : Prop := ∀ x ∈ q, x ≤ 9

/-- An anti-complementary folded seed with a nonzero marked adjacency
defect loses that defect and reaches the low-only bad language in four
exact q transitions. -/
theorem correlated_seed_counterexample :
    qstep [2,3,15,16,16,15,3,2] = [4,7,11,14,14,11,7,4] ∧
    qstep [4,7,11,14,14,11,7,4] = [8,15,3,10,10,3,15,8] ∧
    qstep [8,15,3,10,10,3,15,8] = [17,10,8,1,1,8,10,17] ∧
    qstep [17,10,8,1,1,8,10,17] = [8,9,9,9,2,9,9,9,8] ∧
    lowOnly [8,9,9,9,2,9,9,9,8] := by
  refine ⟨by decide, by decide, by decide, by decide, ?_⟩
  simp [lowOnly]

/-- Even in the odd-width correlated phase, a marked non-nine symbol
can disappear in a single non-overflow step. -/
theorem odd_marked_defect_counterexample :
    qstep [3,4,9,14,12,14,9,4,3] = [6,9,9,9,6,9,9,9,6] ∧
    lowOnly [6,9,9,9,6,9,9,9,6] := by
  refine ⟨by decide, ?_⟩
  simp [lowOnly]

#print axioms complementary_column
#print axioms mismatched_column_repair
#print axioms half_complement_carries
#print axioms half_complement_digits
#print axioms half_complement_no_overflow
#print axioms correlated_seed_counterexample
#print axioms odd_marked_defect_counterexample

end AstraLanguages


/- Source module: MassCriterion.lean -/

/-!
# Decimal digit-sum obstruction to a palindromic reverse-and-add output

This file is a sidecar to `Lychrel196Research.lean`, checked using Lean 4.19
and Std only. `digitSum` is the usual terminating decimal digit-sum
algorithm. Its connection to bounded positional decimal digits is proved.

If the actual reverse-and-add output is a palindrome, its digit sum is
either twice the input digit sum, or four elevenths of it. In particular,
a positive step preserving digit sum cannot output a palindrome.

The all-time consequences are CONDITIONAL: no integer with the required
all-time digit-sum invariant is exhibited or asserted to exist. The later
unbounded-digit-sum theorem in this continuation rules out that invariant
for every positive finite seed. These implications remain valid but cannot
supply an existence witness. Because
`IsLychrel` includes time zero, the unconditional starting-state conclusion
from that invariant is `IsLychrel (step n)`, not `IsLychrel n`.
-/

namespace DecimalMass

open DecimalDigits Lychrel196

/-- Ordinary decimal digit sum, including `digitSum 0 = 0`. -/
def digitSum (n : Nat) : Nat :=
  if h : n = 0 then 0 else n % 10 + digitSum (n / 10)
termination_by n
decreasing_by
  exact Nat.div_lt_self (Nat.pos_of_ne_zero h) (by decide)

theorem digitSum_zero : digitSum 0 = 0 := by
  rw [digitSum]
  simp

/-- The decimal recursion is valid at zero as well. -/
theorem digitSum_mod_div (n : Nat) :
    digitSum n = n % 10 + digitSum (n / 10) := by
  by_cases hn : n = 0
  · subst n
    simp
  · rw [digitSum]
    simp [hn]

/-- Sum of a finite positional word. The coefficients need not be digits. -/
def wordSum (d : Nat → Nat) : Nat → Nat
  | 0 => 0
  | L + 1 => wordSum d L + d L

theorem wordSum_congr (a b : Nat → Nat) (L : Nat)
    (h : ∀ i, i < L → a i = b i) : wordSum a L = wordSum b L := by
  induction L with
  | zero => rfl
  | succ L ih =>
    simp only [wordSum, ih (fun i hi => h i (by omega)), h L (by omega)]

theorem wordSum_add (a b : Nat → Nat) (L : Nat) :
    wordSum (fun i => a i + b i) L = wordSum a L + wordSum b L := by
  induction L with
  | zero => rfl
  | succ L ih => simp only [wordSum, ih]; omega

theorem wordSum_mul (a : Nat → Nat) (L c : Nat) :
    wordSum (fun i => c * a i) L = c * wordSum a L := by
  induction L with
  | zero => simp [wordSum]
  | succ L ih => simp [wordSum, ih, Nat.mul_add]

theorem wordSum_zero (L : Nat) : wordSum (fun _ => 0) L = 0 := by
  induction L with
  | zero => rfl
  | succ L ih => simp [wordSum, ih]

theorem wordSum_shift (d : Nat → Nat) (L : Nat) :
    wordSum d (L + 1) = d 0 + wordSum (fun i => d (i + 1)) L := by
  induction L with
  | zero => simp [wordSum]
  | succ L ih => simp only [wordSum] at ih ⊢; omega

/-- Positional reflection preserves the unweighted digit sum. -/
theorem wordSum_reflected (d : Nat → Nat) (L : Nat) :
    wordSum (reflected d L) L = wordSum d L := by
  induction L generalizing d with
  | zero => rfl
  | succ L ih =>
    have hr : wordSum (reflected d (L + 1)) L =
        wordSum (reflected (fun i => d (i + 1)) L) L := by
      apply wordSum_congr
      intro i hi
      simp only [reflected]
      congr 1
      omega
    rw [wordSum, hr, ih, wordSum_shift]
    simp [reflected, Nat.add_comm]

/-- The mirrored pair-sum word has twice the ordinary digit sum. -/
theorem wordSum_columns (d : Nat → Nat) (L : Nat) :
    wordSum (columnSum d L) L = 2 * wordSum d L := by
  unfold columnSum
  rw [wordSum_add, wordSum_reflected]
  omega

/-- The recursive decimal sum agrees with every bounded positional
representation, even one containing additional leading zeroes. -/
theorem digitSum_value (d : Nat → Nat) (L : Nat)
    (hd : ∀ i, i < L → d i ≤ 9) :
    digitSum (value d L) = wordSum d L := by
  induction L generalizing d with
  | zero => exact digitSum_zero
  | succ L ih =>
    have hd0 := hd 0 (by omega)
    have hm : value d (L + 1) % 10 = d 0 := by
      rw [value_shift]
      omega
    have hv : value d (L + 1) / 10 = value (fun i => d (i + 1)) L := by
      rw [value_shift]
      omega
    rw [digitSum_mod_div, hm, hv, ih, wordSum_shift]
    intro i hi
    exact hd (i + 1) (by omega)

theorem digitSum_positive (n : Nat) (hn : 0 < n) : 0 < digitSum n := by
  obtain ⟨d, L, hL, hd, hlead, hv⟩ := canonical_exists n hn
  rw [← hv, digitSum_value d L hd]
  obtain ⟨k, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : L ≠ 0)
  have hlead' : 0 < d k := by simpa using hlead
  simp only [wordSum]
  omega

/-- Total count of the actual carries out of the first `L` columns. -/
def carryCount (q : Nat → Nat) (L : Nat) : Nat :=
  wordSum (fun i => carry q (i + 1)) L

/-- Summing all actual decimal column equations includes the final carry.
No coefficient bounds or palindrome assumption are required. -/
theorem wordSum_output (q : Nat → Nat) (L : Nat) :
    wordSum (output q) L + carry q L + 9 * carryCount q L = wordSum q L := by
  induction L with
  | zero => simp [wordSum, carry, carryCount]
  | succ L ih =>
    have hc := column_equation q L
    simp only [carryCount, wordSum] at ih ⊢
    omega

theorem wordSum_extended (q : Nat → Nat) (L : Nat) :
    wordSum (extended q L) (L + 1) = wordSum (output q) L + carry q L := by
  rw [wordSum]
  have h : wordSum (extended q L) L = wordSum (output q) L := by
    apply wordSum_congr
    intro i hi
    simp [extended, hi]
  rw [h]
  simp [extended]

/-- Exact general mass balance for the actual decimal reverse-and-add map.
Every outgoing carry removes nine from the input pair-sum total. -/
theorem digitSum_step_balance (d : Nat → Nat) (L : Nat)
    (hd : ∀ i, i < L → d i ≤ 9)
    (hlead : L = 0 ∨ 0 < d (L - 1)) :
    digitSum (step (value d L)) + 9 * carryCount (columnSum d L) L =
      2 * digitSum (value d L) := by
  have hc := carry_bounded (columnSum d L) L (columnSum_bounded d L hd) L
    (Nat.le_refl L)
  have he : ∀ i, i < L + 1 → extended (columnSum d L) L i ≤ 9 := by
    intro i hi
    unfold extended
    split
    · exact output_bounded _ _
    · omega
  rw [step_value d L hd hlead, ← value_extended, digitSum_value _ _ he,
    wordSum_extended, digitSum_value d L hd]
  rw [← wordSum_columns d L]
  exact wordSum_output _ _

/-- In the low-column predecessor branch all actual carries vanish. -/
theorem carryCount_zero_of_small (d : Nat → Nat) (L : Nat)
    (hsmall : ∀ i, i < L → columnSum d L i ≤ 9) :
    carryCount (columnSum d L) L = 0 := by
  obtain ⟨hz, _⟩ := DecimalCarry.small_digit_sums_give_palindrome
    L (columnSum d L) (carry (columnSum d L)) (output (columnSum d L))
    (columnSum_symmetric d L) hsmall
    (fun i _ => column_equation _ i) rfl
  unfold carryCount
  calc
    wordSum (fun i => carry (columnSum d L) (i + 1)) L =
        wordSum (fun _ => 0) L := wordSum_congr _ _ L (fun i hi => hz _ (by omega))
    _ = 0 := wordSum_zero L

/-- In the exceptional palindrome branch each column sum is eleven
times its actual outgoing carry. -/
theorem columns_eq_eleven_carry (d : Nat → Nat) (L : Nat)
    (hd : ∀ i, i < L → d i ≤ 9)
    (hvalues : ∀ i, i < L → columnSum d L i = 0 ∨ columnSum d L i = 11) :
    ∀ i, i < L → columnSum d L i = 11 * carry (columnSum d L) (i + 1) := by
  intro i hi
  have hv := hvalues i hi
  have hc := carry_bounded (columnSum d L) L (columnSum_bounded d L hd) i
    (by omega)
  have ho := output_bounded (columnSum d L) i
  have ha := column_equation (columnSum d L) i
  omega

/-- Sharp necessary digit-sum alternatives for every positive actual input.
The disjunction is necessary, not a sufficient palindrome test. -/
theorem palindrome_step_digitSum (n : Nat) (hn : 0 < n)
    (hp : Palindrome (step n)) :
    digitSum (step n) = 2 * digitSum n ∨
      11 * digitSum (step n) = 4 * digitSum n := by
  obtain ⟨d, L, hL, hd, hlead, hv⟩ := canonical_exists n hn
  subst n
  have hb := digitSum_step_balance d L hd (Or.inr hlead)
  rcases (step_palindrome_iff d L hL hd hlead).mp hp with hsmall | hspecial
  · left
    rw [carryCount_zero_of_small d L hsmall] at hb
    simpa using hb
  · right
    have hlocal := columns_eq_eleven_carry d L hd hspecial.2
    have hsum : wordSum (columnSum d L) L = 11 * carryCount (columnSum d L) L := by
      calc
        wordSum (columnSum d L) L =
            wordSum (fun i => 11 * carry (columnSum d L) (i + 1)) L :=
          wordSum_congr _ _ L hlocal
        _ = 11 * carryCount (columnSum d L) L := wordSum_mul _ _ _
    rw [wordSum_columns, ← digitSum_value d L hd] at hsum
    omega

/-- Zero also obeys the same alternatives; no positivity assumption is
needed for the sharp necessary transition itself. -/
theorem palindrome_step_digitSum_all (n : Nat)
    (hp : Palindrome (step n)) :
    digitSum (step n) = 2 * digitSum n ∨
      11 * digitSum (step n) = 4 * digitSum n := by
  by_cases hn : n = 0
  · subst n
    left
    simp [step, reverse10, reverseFuel, digitSum_zero]
  · exact palindrome_step_digitSum n (by omega) hp

/-- A positive reverse-and-add step preserving digit sum has a
nonpalindromic output. -/
theorem nonpalindrome_of_digitSum_preserved (n : Nat) (hn : 0 < n)
    (hs : digitSum (step n) = digitSum n) : ¬ Palindrome (step n) := by
  intro hp
  have hpos := digitSum_positive n hn
  rcases palindrome_step_digitSum n hn hp with h | h <;> omega

/-- A positive all-time constant-digit-sum orbit yields a Lychrel witness
at its first output. The invariant remains an explicit hypothesis. -/
theorem step_isLychrel_of_constant_digitSum (n : Nat) (hn : 0 < n)
    (hs : ∀ k, digitSum (orbit n k) = digitSum n) : IsLychrel (step n) := by
  intro k
  rw [orbit_from_step]
  apply nonpalindrome_of_digitSum_preserved (orbit n k) (orbit_positive n hn k)
  change digitSum (orbit n (k + 1)) = digitSum (orbit n k)
  rw [hs, hs]

/-- Including a nonpalindromic starting value yields the time-zero version. -/
theorem isLychrel_of_constant_digitSum (n : Nat) (hn : 0 < n)
    (hzero : ¬ Palindrome n)
    (hs : ∀ k, digitSum (orbit n k) = digitSum n) : IsLychrel n := by
  intro k
  cases k with
  | zero => exact hzero
  | succ k =>
    have h := step_isLychrel_of_constant_digitSum n hn hs k
    rwa [orbit_from_step] at h

/-- This is a conditional extraction theorem, not an existence assertion. -/
theorem existence_of_constant_digitSum_orbit
    (h : ∃ n, 0 < n ∧ ∀ k, digitSum (orbit n k) = digitSum n) :
    DecimalLychrelExistence := by
  obtain ⟨n, hn, hs⟩ := h
  exact ⟨step n, step_isLychrel_of_constant_digitSum n hn hs⟩

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
/-- The doubling alternative is attained by an actual palindrome output. -/
theorem doubling_ratio_attained :
    step 12 = 33 ∧ Palindrome (step 12) ∧
      digitSum 12 = 3 ∧ digitSum (step 12) = 6 := by
  have hs : step 12 = 33 := by decide
  refine ⟨hs, ?_, ?_, ?_⟩
  · rw [hs]; decide
  · simp [digitSum]
  · rw [hs]; simp [digitSum]

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
/-- The four-elevenths alternative is also attained, so the exceptional
branch cannot be omitted or replaced by strict digit-sum growth. -/
theorem exceptional_ratio_attained :
    step 605 = 1111 ∧ Palindrome (step 605) ∧
      digitSum 605 = 11 ∧ digitSum (step 605) = 4 := by
  have hs : step 605 = 1111 := by decide
  refine ⟨hs, ?_, ?_, ?_⟩
  · rw [hs]; decide
  · simp [digitSum]
  · rw [hs]; simp [digitSum]

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
/-- The scalar disjunction is only a necessary test: its exceptional
equality can hold even when the actual output is not a palindrome. -/
theorem exceptional_ratio_not_sufficient :
    step 119 = 1030 ∧ ¬ Palindrome (step 119) ∧
      11 * digitSum (step 119) = 4 * digitSum 119 := by
  have hs : step 119 = 1030 := by decide
  refine ⟨hs, ?_, ?_⟩
  · rw [hs]; decide
  · rw [hs]; simp [digitSum]

#print axioms digitSum_value
#print axioms digitSum_positive
#print axioms digitSum_step_balance
#print axioms palindrome_step_digitSum
#print axioms palindrome_step_digitSum_all
#print axioms nonpalindrome_of_digitSum_preserved
#print axioms step_isLychrel_of_constant_digitSum
#print axioms isLychrel_of_constant_digitSum
#print axioms existence_of_constant_digitSum_orbit
#print axioms doubling_ratio_attained
#print axioms exceptional_ratio_attained
#print axioms exceptional_ratio_not_sufficient

end DecimalMass


/- Source module: ZeroGap.lean -/

/-!
# A bound on zero gaps is preserved by actual decimal reverse-and-add

The update here is `FoldedDecimal.nextColumns`, including its actual final
carry and width. No orbit hypothesis or finite search is used.
-/

namespace DecimalZeroGap

open DecimalDigits FoldedDecimal DecimalMass

/-- Every nonempty interval of zero coefficients has length at most `K`. -/
def ZeroBound (q : Nat → Nat) (L K : Nat) : Prop :=
  ∀ a k, 0 < k → a + k ≤ L →
    (∀ i, a ≤ i → i < a + k → q i = 0) → k ≤ K

/-- The input word itself always supplies an initial zero-gap bound. -/
theorem zeroBound_length (q : Nat → Nat) (L : Nat) : ZeroBound q L L := by
  intro a k _ hk _
  omega

/-- Reflection of the actual carries, indexed at column boundaries. -/
def backCarry (q : Nat → Nat) (L i : Nat) : Nat := carry q (L - i)

/-- Reflection of the actual output digits. -/
def backOutput (q : Nat → Nat) (L i : Nat) : Nat := output q (L - 1 - i)

theorem back_column_equation (q : Nat → Nat) (L i : Nat)
    (hs : ∀ j, j < L → q j = q (L - 1 - j)) (hi : i < L) :
    backOutput q L i + 10 * backCarry q L i = q i + backCarry q L (i + 1) := by
  have he := column_equation q (L - 1 - i)
  have h₁ : L - 1 - i + 1 = L - i := by omega
  have h₂ : L - (i + 1) = L - 1 - i := by omega
  simpa only [backOutput, backCarry, h₁, h₂, ← hs i hi] using he

theorem backCarry_bounded (q : Nat → Nat) (L i : Nat)
    (hq : ∀ j, j < L → q j ≤ 18) : backCarry q L i ≤ 1 := by
  exact carry_bounded q L hq (L - i) (by omega)

/-- Simultaneous zero digits interchange the two binary carry states. -/
theorem simultaneous_zero_carries (q : Nat → Nat) (L i : Nat)
    (ha : Admissible L q) (hi : i < L)
    (hr : output q i = 0) (hu : backOutput q L i = 0) :
    carry q (i + 1) = backCarry q L i ∧
      carry q i = backCarry q L (i + 1) := by
  have hf := column_equation q i
  have hb := back_column_equation q L i ha.2.2.2.1 hi
  have hci := carry_bounded q L ha.2.2.1 i (by omega)
  have hcn := carry_bounded q L ha.2.2.1 (i + 1) (by omega)
  have hbi := backCarry_bounded q L i ha.2.2.1
  have hbn := backCarry_bounded q L (i + 1) ha.2.2.1
  omega

/-- Two adjacent simultaneous zero digits have identical old coefficients,
which must be zero or nine. An isolated simultaneous zero is insufficient. -/
theorem adjacent_zero_columns (q : Nat → Nat) (L i : Nat)
    (ha : Admissible L q) (hi : i + 1 < L)
    (hr : output q i = 0) (hu : backOutput q L i = 0)
    (hrn : output q (i + 1) = 0) (hun : backOutput q L (i + 1) = 0) :
    q i = q (i + 1) ∧ (q i = 0 ∨ q i = 9) := by
  have h₁ := simultaneous_zero_carries q L i ha (by omega) hr hu
  have h₂ := simultaneous_zero_carries q L (i + 1) ha hi hrn hun
  have he₁ := column_equation q i
  have he₂ := column_equation q (i + 1)
  have hci := carry_bounded q L ha.2.2.1 i (by omega)
  have hcn := carry_bounded q L ha.2.2.1 (i + 1) (by omega)
  omega

/-- A simultaneous zero interval of length at least two is entirely zero
or entirely nine in the old pair-sum word. -/
theorem simultaneous_zero_interval (q : Nat → Nat) (L a k : Nat)
    (ha : Admissible L q) (hk : 2 ≤ k) (hbound : a + k ≤ L)
    (hz : ∀ i, a ≤ i → i < a + k → output q i = 0 ∧ backOutput q L i = 0) :
    (∀ i, a ≤ i → i < a + k → q i = 0) ∨
      (∀ i, a ≤ i → i < a + k → q i = 9) := by
  have hadj : ∀ i, a ≤ i → i + 1 < a + k →
      q i = q (i + 1) ∧ (q i = 0 ∨ q i = 9) := by
    intro i hia hik
    have h₁ := hz i hia (by omega)
    have h₂ := hz (i + 1) (by omega) hik
    exact adjacent_zero_columns q L i ha (by omega) h₁.1 h₁.2 h₂.1 h₂.2
  have heq : ∀ j, j < k → q (a + j) = q a := by
    intro j
    induction j with
    | zero => intro _; simp
    | succ j ih =>
      intro hj
      have he := (hadj (a + j) (by omega) (by omega)).1
      have hp := ih (by omega)
      simpa only [Nat.add_assoc] using he.symm.trans hp
  rcases (hadj a (by omega) (by omega)).2 with hzero | hnine
  · left
    intro i hia hik
    have he := heq (i - a) (by omega)
    have hind : a + (i - a) = i := by omega
    rw [hind] at he
    exact he.trans hzero
  · right
    intro i hia hik
    have he := heq (i - a) (by omega)
    have hind : a + (i - a) = i := by omega
    rw [hind] at he
    exact he.trans hnine


theorem wordSum_mono_length (q : Nat → Nat) (a b : Nat) (hab : a ≤ b) :
    wordSum q a ≤ wordSum q b := by
  induction b generalizing a with
  | zero =>
    have ha : a = 0 := by omega
    subst a
    exact Nat.le_refl _
  | succ b ih =>
    by_cases h : a ≤ b
    · have he := ih a h
      simp only [wordSum]
      omega
    · have he : a = b + 1 := by omega
      subst a
      exact Nat.le_refl _

/-- Every interval of positive coefficients costs at least its length. -/
theorem interval_length_le_mass (q : Nat → Nat) (L a k : Nat)
    (hbound : a + k ≤ L)
    (hpos : ∀ i, a ≤ i → i < a + k → 0 < q i) :
    k ≤ wordSum q L := by
  have hp : k ≤ wordSum q (a + k) := by
    induction k with
    | zero => omega
    | succ k ih =>
      have hb : a + k ≤ L := by omega
      have hi := ih hb (fun i hia hik => hpos i hia (by omega))
      have hlast := hpos (a + k) (by omega) (by omega)
      simpa only [Nat.add_assoc, wordSum] using (by omega : k + 1 ≤ wordSum q (a + k) + q (a + k))
  exact Nat.le_trans hp (wordSum_mono_length q (a + k) L hbound)

/-- Without overflow a new zero is precisely a simultaneous old output zero. -/
theorem next_zero_no_overflow (q : Nat → Nat) (L i : Nat)
    (hc : carry q L = 0) (hz : nextColumns q L i = 0) :
    output q i = 0 ∧ backOutput q L i = 0 := by
  simpa only [nextColumns, hc, if_true, columnSum, reflected, backOutput,
    Nat.add_eq_zero_iff] using hz

/-- Every zero in an overflowing next word is strictly internal; its two
vanishing output digits have the one-column shifted alignment. -/
theorem next_zero_overflow (q : Nat → Nat) (L i : Nat)
    (hL : 0 < L) (hc : carry q L = 1) (hi : i < L + 1)
    (hz : nextColumns q L i = 0) :
    0 < i ∧ i < L ∧ output q i = 0 ∧ backOutput q L (i - 1) = 0 := by
  have hzero : i ≠ 0 := by
    intro he
    subst i
    simp [nextColumns, hc, columnSum, reflected, extended, hL] at hz
  have hlast : i ≠ L := by
    intro he
    subst i
    simp [nextColumns, hc, columnSum, reflected, extended, hL] at hz
  have hil : i < L := by omega
  have hmir : L - i < L := by omega
  have hind : L - 1 - (i - 1) = L - i := by omega
  simp only [nextColumns, hc, Nat.one_ne_zero, if_false, columnSum,
    reflected, Nat.add_sub_cancel, extended, hil, hmir, if_true] at hz
  refine ⟨by omega, hil, by omega, ?_⟩
  simp only [backOutput, hind]
  omega

/-- A zero input column with two zero output digits has four zero carries. -/
theorem zero_column_carries (q : Nat → Nat) (L i : Nat)
    (ha : Admissible L q) (hi : i < L)
    (hq : q i = 0) (hr : output q i = 0) (hu : backOutput q L i = 0) :
    carry q i = 0 ∧ carry q (i + 1) = 0 ∧
      backCarry q L i = 0 ∧ backCarry q L (i + 1) = 0 := by
  have hs := simultaneous_zero_carries q L i ha hi hr hu
  have he := column_equation q i
  have hb := carry_bounded q L ha.2.2.1 i (by omega)
  omega

/-- In the overflowing alignment, an all-zero core extends by one old
zero column at each end. This prevents merging unrelated old gaps. -/
theorem zero_core_extends (q : Nat → Nat) (L a k : Nat)
    (ha : Admissible L q) (ha0 : 0 < a) (hk : 0 < k) (hbound : a + k < L)
    (hcore : ∀ i, a ≤ i → i < a + k → q i = 0)
    (hz : ∀ i, a ≤ i → i < a + k → output q i = 0 ∧ backOutput q L i = 0)
    (hleft : backOutput q L (a - 1) = 0) (hright : output q (a + k) = 0) :
    ∀ i, a - 1 ≤ i → i < a + k + 1 → q i = 0 := by
  have hca := zero_column_carries q L a ha (by omega)
    (hcore a (by omega) (by omega))
    (hz a (by omega) (by omega)).1 (hz a (by omega) (by omega)).2
  have hcb := zero_column_carries q L (a + k - 1) ha (by omega)
    (hcore (a + k - 1) (by omega) (by omega))
    (hz (a + k - 1) (by omega) (by omega)).1
    (hz (a + k - 1) (by omega) (by omega)).2
  have hlind : a - 1 + 1 = a := by omega
  have hrind : a + k - 1 + 1 = a + k := by omega
  rw [hrind] at hcb
  have hql : q (a - 1) = 0 := by
    have hf := column_equation q (a - 1)
    have hb := back_column_equation q L (a - 1) ha.2.2.2.1 (by omega)
    have hd := output_bounded q (a - 1)
    rw [hlind] at hf hb
    omega
  have hqr : q (a + k) = 0 := by
    have hf := column_equation q (a + k)
    have hb := back_column_equation q L (a + k) ha.2.2.2.1 hbound
    have hd : backOutput q L (a + k) ≤ 9 := output_bounded q _
    omega
  intro i hia hik
  by_cases hi₁ : i = a - 1
  · exact hi₁ ▸ hql
  by_cases hi₂ : i = a + k
  · exact hi₂ ▸ hqr
  exact hcore i (by omega) (by omega)


/-- A uniform input mass bound and an initial zero-gap bound propagate
through the actual overflow-dependent pair-sum update. The deliberately
coarse condition `M + 2 ≤ K` handles every short-run exception. -/
theorem zeroBound_next (q : Nat → Nat) (L M K : Nat)
    (ha : Admissible L q) (hm : wordSum q L ≤ M)
    (hz : ZeroBound q L K) (hK : M + 2 ≤ K) :
    ZeroBound (nextColumns q L) (nextWidth q L) K := by
  intro a k hk hbound hzero
  by_cases hshort : k ≤ K
  · exact hshort
  have hlong : 3 ≤ k := by omega
  by_cases hc : carry q L = 0
  · have hb : a + k ≤ L := by simpa only [nextWidth, hc, if_true] using hbound
    have hboth : ∀ i, a ≤ i → i < a + k →
        output q i = 0 ∧ backOutput q L i = 0 := by
      intro i hia hik
      exact next_zero_no_overflow q L i hc (hzero i hia hik)
    rcases simultaneous_zero_interval q L a k ha (by omega) hb hboth with ho | hn
    · exact hz a k hk hb ho
    · have hmass := interval_length_le_mass q L a k hb
        (fun i hia hik => by rw [hn i hia hik]; decide)
      omega
  · have hcb := carry_bounded q L ha.2.2.1 L (by omega)
    have hc1 : carry q L = 1 := by omega
    have hb : a + k ≤ L + 1 := by
      simpa only [nextWidth, hc, if_false] using hbound
    have hout : ∀ i, a ≤ i → i < a + k →
        0 < i ∧ i < L ∧ output q i = 0 ∧ backOutput q L (i - 1) = 0 := by
      intro i hia hik
      exact next_zero_overflow q L i ha.1 hc1 (by omega) (hzero i hia hik)
    have hfirst := hout a (by omega) (by omega)
    have hlast := hout (a + k - 1) (by omega) (by omega)
    have ha0 : 0 < a := hfirst.1
    have hbk : a + k ≤ L := by omega
    have hcore : ∀ i, a ≤ i → i < a + (k - 1) →
        output q i = 0 ∧ backOutput q L i = 0 := by
      intro i hia hik
      have hr := (hout i hia (by omega)).2.2.1
      have hu := (hout (i + 1) (by omega) (by omega)).2.2.2
      exact ⟨hr, by simpa only [Nat.add_sub_cancel] using hu⟩
    rcases simultaneous_zero_interval q L a (k - 1) ha (by omega) (by omega) hcore
      with ho | hn
    · have hright : output q (a + (k - 1)) = 0 :=
        (hout (a + (k - 1)) (by omega) (by omega)).2.2.1
      have hext := zero_core_extends q L a (k - 1) ha ha0 (by omega)
        (by omega) ho hcore hfirst.2.2.2 hright
      have hold : k + 1 ≤ K := hz (a - 1) (k + 1) (by omega) (by omega)
        (fun i hia hik => hext i hia (by omega))
      omega
    · have hmass := interval_length_le_mass q L a (k - 1) (by omega)
        (fun i hia hik => by rw [hn i hia hik]; decide)
      omega

#print axioms simultaneous_zero_interval
#print axioms zero_core_extends
#print axioms zeroBound_next

end DecimalZeroGap


/- Source module: UnboundedMass.lean -/

/-!
# Unbounded digit sums in every positive decimal reverse-and-add orbit

The combinatorial estimate says that bounded mass and a uniform bound on
zero runs force a finite word to have bounded length. Combined with exact
zero-run propagation and the existing quantitative width growth theorem,
this rules out bounded digit sums along any positive orbit.
-/

namespace DecimalUnboundedMass

open DecimalDigits DecimalMass FoldedDecimal OverflowCarryNormalization
  CarryHistory Lychrel196

/-- Splitting an unweighted finite word sum at any position. -/
theorem wordSum_split (q : Nat → Nat) (a k : Nat) :
    wordSum q (a + k) =
      wordSum q a + wordSum (fun i => q (a + i)) k := by
  induction k with
  | zero => simp [wordSum]
  | succ k ih =>
    change wordSum q (a + k) + q (a + k) =
      wordSum q a + (wordSum (fun i => q (a + i)) k + q (a + k))
    rw [ih]
    omega

/-- A finite word with no zero run longer than `K` has length at most
`(mass + 1) * (K + 1)`. Endpoint assumptions are unnecessary. -/
theorem length_le_of_zero_runs (q : Nat → Nat) (L K : Nat)
    (hz : ∀ a k, 0 < k → a + k ≤ L →
      (∀ i, a ≤ i → i < a + k → q i = 0) → k ≤ K) :
    L ≤ (wordSum q L + 1) * (K + 1) := by
  induction L using Nat.strongRecOn generalizing q with
  | ind L ih =>
    by_cases hshort : L ≤ K
    · have hm := Nat.mul_le_mul_right (K + 1)
        (show 1 ≤ wordSum q L + 1 by omega)
      simp only [Nat.one_mul] at hm
      omega
    · have hnonzero : ∃ i, i ≤ K ∧ 0 < q i := by
        apply Classical.byContradiction
        intro hn
        have hzprefix : ∀ i, 0 ≤ i → i < 0 + (K + 1) → q i = 0 := by
          intro i _ hi
          have hnot : ¬ 0 < q i := by
            intro hpos
            exact hn ⟨i, by omega, hpos⟩
          omega
        have hbad := hz 0 (K + 1) (by omega) (by omega) hzprefix
        omega
      obtain ⟨i, hi, hqi⟩ := hnonzero
      let a := i + 1
      let R := L - a
      have ha : 0 < a := by dsimp [a]; omega
      have haL : a ≤ L := by dsimp [a]; omega
      have hR : R < L := by dsimp [R]; omega
      have hsplit : a + R = L := by dsimp [R]; omega
      have htail : ∀ b k, 0 < k → b + k ≤ R →
          (∀ j, b ≤ j → j < b + k → (fun x => q (a + x)) j = 0) →
          k ≤ K := by
        intro b k hk hbk hzero
        apply hz (a + b) k hk (by omega)
        intro j hjlo hjhi
        have heq : a + (j - a) = j := by omega
        have hh := hzero (j - a) (by omega) (by omega)
        simpa only [heq] using hh
      have hbound := ih R hR (fun j => q (a + j)) htail
      have hmass : wordSum (fun j => q (a + j)) R + 1 ≤ wordSum q L := by
        have hs := wordSum_split q a R
        rw [hsplit] at hs
        have hp : wordSum q a = wordSum q i + q i := by rfl
        omega
      have hmul := Nat.mul_le_mul_right (K + 1) hmass
      have halim : a ≤ K + 1 := by dsimp [a]; omega
      rw [Nat.add_mul, Nat.one_mul]
      omega

/-- The mass of each exact pair-sum state is twice the ordinary decimal
digit sum of the actual numeric iterate. -/
theorem iterPairs_wordSum (n : Nat) (d q : Nat → Nat) (L t : Nat)
    (hc : Canonical n d L)
    (hr : ∀ i, i < L → columnSum d L i = q i) :
    wordSum (iterPairs q L t).2 (iterPairs q L t).1 =
      2 * digitSum (orbit n t) := by
  obtain ⟨e, he, hrep⟩ := iterPairs_representation n d q L t hc hr
  calc
    wordSum (iterPairs q L t).2 (iterPairs q L t).1 =
        wordSum (columnSum e (iterPairs q L t).1) (iterPairs q L t).1 :=
      (wordSum_congr _ _ _ hrep).symm
    _ = 2 * wordSum e (iterPairs q L t).1 := wordSum_columns _ _
    _ = 2 * digitSum (orbit n t) := by
      rw [← digitSum_value e _ he.2.1, he.2.2.2]

/-- A bounded mass sharpens the purely combinatorial length estimate. -/
theorem length_le_of_mass_zero_runs (q : Nat → Nat) (L M K : Nat)
    (hm : wordSum q L ≤ M)
    (hz : ∀ a k, 0 < k → a + k ≤ L →
      (∀ i, a ≤ i → i < a + k → q i = 0) → k ≤ K) :
    L ≤ (M + 1) * (K + 1) := by
  apply Nat.le_trans (length_le_of_zero_runs q L K hz)
  exact Nat.mul_le_mul_right (K + 1) (by omega)

/-- The already established growth theorem excludes a uniform width
bound on an exact admissible pair-sum orbit. -/
theorem iterPairs_width_unbounded (q : Nat → Nat) (L H : Nat)
    (ha : Admissible L q) : ∃ t, H < (iterPairs q L t).1 := by
  refine ⟨4 * H + 5, ?_⟩
  have hg := DecimalWidthGrowth.width_lower_bound q L (4 * H + 5) ha
  omega

/-- The last argument is the local zero-run propagation theorem. This
auxiliary statement isolates the numeric connection and iteration. -/
theorem digitSum_unbounded_of_zero_run_propagation
    (hnext : ∀ (q : Nat → Nat) (L M K : Nat),
      Admissible L q → wordSum q L ≤ M →
      (∀ a k, 0 < k → a + k ≤ L →
        (∀ i, a ≤ i → i < a + k → q i = 0) → k ≤ K) →
      M + 2 ≤ K →
      (∀ a k, 0 < k → a + k ≤ nextWidth q L →
        (∀ i, a ≤ i → i < a + k → nextColumns q L i = 0) → k ≤ K))
    (n : Nat) (hn : 0 < n) (B : Nat) :
    ∃ t, B < digitSum (orbit n t) := by
  apply Classical.byContradiction
  intro hnone
  have hs : ∀ t, digitSum (orbit n t) ≤ B := by
    intro t
    have hnot : ¬ B < digitSum (orbit n t) := by
      intro hgt
      exact hnone ⟨t, hgt⟩
    omega
  obtain ⟨d, L, hc⟩ := canonical_exists n hn
  let q := columnSum d L
  let K := max L (2 * B + 2)
  let H := (2 * B + 1) * (K + 1)
  have ha : Admissible L q := NormalizationBridge.canonical_admissible n d L hc
  have hK : 2 * B + 2 ≤ K := Nat.le_max_right _ _
  have hLK : L ≤ K := Nat.le_max_left _ _
  have hm : ∀ t, wordSum (iterPairs q L t).2 (iterPairs q L t).1 ≤ 2 * B := by
    intro t
    rw [iterPairs_wordSum n d q L t hc (fun _ _ => rfl)]
    exact Nat.mul_le_mul_left 2 (hs t)
  have hz : ∀ t a k, 0 < k → a + k ≤ (iterPairs q L t).1 →
      (∀ i, a ≤ i → i < a + k → (iterPairs q L t).2 i = 0) → k ≤ K := by
    intro t
    induction t with
    | zero =>
      intro a k _ hlen _
      change a + k ≤ L at hlen
      omega
    | succ t ih =>
      exact hnext (iterPairs q L t).2 (iterPairs q L t).1 (2 * B) K
        (iterPairs_admissible q L t ha) (hm t) ih hK
  have hw : ∀ t, (iterPairs q L t).1 ≤ H := by
    intro t
    exact length_le_of_mass_zero_runs (iterPairs q L t).2
      (iterPairs q L t).1 (2 * B) K (hm t) (hz t)
  obtain ⟨t, ht⟩ := iterPairs_width_unbounded q L H ha
  have hb := hw t
  omega

/-- Every positive decimal reverse-and-add orbit has unbounded ordinary
digit sums. This is unconditional and concerns the actual numeric orbit. -/
theorem digitSum_unbounded (n : Nat) (hn : 0 < n) (B : Nat) :
    ∃ t, B < digitSum (orbit n t) :=
  digitSum_unbounded_of_zero_run_propagation DecimalZeroGap.zeroBound_next n hn B

/-- In particular, a positive reverse-and-add orbit cannot have constant
digit sum at every time. -/
theorem not_constant_digitSum (n : Nat) (hn : 0 < n) :
    ¬ (∀ t, digitSum (orbit n t) = digitSum n) := by
  intro hconstant
  obtain ⟨t, ht⟩ := digitSum_unbounded n hn (digitSum n)
  rw [hconstant t] at ht
  omega

#print axioms length_le_of_zero_runs
#print axioms iterPairs_wordSum
#print axioms digitSum_unbounded
#print axioms not_constant_digitSum

end DecimalUnboundedMass


/- Source module: MassConsequences.lean -/

namespace DecimalUnboundedMass

open DecimalMass DecimalDigits Lychrel196

/-- The digit sums exceed any bound arbitrarily late in every positive
ordinary decimal reverse-and-add orbit. -/
theorem digitSum_unbounded_after (n : Nat) (hn : 0 < n) (B start : Nat) :
    ∃ t, start ≤ t ∧ B < digitSum (orbit n t) := by
  obtain ⟨k, hk⟩ := digitSum_unbounded (orbit n start)
    (orbit_positive n hn start) B
  refine ⟨start + k, by omega, ?_⟩
  rw [LychrelCertificates.orbit_add]
  exact hk

/-- No positive orbit can eventually remain below a fixed digit-sum bound. -/
theorem not_eventually_bounded_digitSum (n : Nat) (hn : 0 < n) :
    ¬ ∃ start B, ∀ t, start ≤ t → digitSum (orbit n t) ≤ B := by
  rintro ⟨start, B, hb⟩
  obtain ⟨t, ht, hgt⟩ := digitSum_unbounded_after n hn B start
  have hle := hb t ht
  omega

/-- A genuine all-time statement about 196, independent of whether its
orbit ever reaches a palindrome. -/
theorem digitSum_196_unbounded_after (B start : Nat) :
    ∃ t, start ≤ t ∧ B < digitSum (orbit 196 t) :=
  digitSum_unbounded_after 196 (by decide) B start

#print axioms digitSum_unbounded_after
#print axioms not_eventually_bounded_digitSum
#print axioms digitSum_196_unbounded_after

end DecimalUnboundedMass


/- Source module: QuantitativeMass.lean -/

/-!
# Effective digit-sum escape and running-maximum bounds

This continuation uses only Lean 4.19 and Std. It supplies a computable
decimal length, an explicit finite-time escape bound for the ordinary
decimal reverse-and-add orbit, and an exact inequality for its running
maximum digit sum. All carry propagation and numeric representation
hypotheses are discharged using the imported theorems.
-/

namespace DecimalQuantitativeMass

open DecimalDigits DecimalMass FoldedDecimal OverflowCarryNormalization
  CarryHistory Lychrel196 DecimalZeroGap DecimalUnboundedMass

/-- Canonical decimal length; zero has length zero. -/
def decimalLength (n : Nat) : Nat :=
  if h : n = 0 then 0 else decimalLength (n / 10) + 1
termination_by n
decreasing_by
  exact Nat.div_lt_self (Nat.pos_of_ne_zero h) (by decide)

theorem decimalLength_zero : decimalLength 0 = 0 := by
  rw [decimalLength]
  simp

/-- The ordinary division algorithm counts the length of every decimal
representation whose leading digit is nonzero. -/
theorem decimalLength_value (d : Nat → Nat) (L : Nat)
    (hd : ∀ i, i < L → d i ≤ 9)
    (hlead : L = 0 ∨ 0 < d (L - 1)) :
    decimalLength (value d L) = L := by
  induction L generalizing d with
  | zero => exact decimalLength_zero
  | succ L ih =>
    have hlead' : 0 < d L := by simpa using hlead
    have hp : 0 < value d (L + 1) :=
      value_positive d (L + 1) (by omega) (by simpa using hlead')
    have hd0 := hd 0 (by omega)
    have hdiv : value d (L + 1) / 10 = value (fun i => d (i + 1)) L := by
      rw [value_shift]
      omega
    have htail : L = 0 ∨ 0 < (fun i => d (i + 1)) (L - 1) := by
      by_cases hL : L = 0
      · exact Or.inl hL
      · right
        have heq : L - 1 + 1 = L := by omega
        simpa only [heq] using hlead'
    rw [decimalLength]
    simp only [Nat.ne_of_gt hp, ↓reduceDIte]
    rw [hdiv, ih (fun i => d (i + 1)) (fun i hi => hd (i + 1) (by omega)) htail]

theorem decimalLength_of_canonical (n : Nat) (d : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) : decimalLength n = L := by
  rw [← hc.2.2.2]
  exact decimalLength_value d L hc.2.1 (Or.inr hc.2.2.1)

/-- Uniform zero-run budget for a digit-sum ceiling `B`. -/
def gapBound (L B : Nat) : Nat := max L (2 * B + 2)

/-- A coarse width bound whenever all digit sums remain at most `B`. -/
def widthBound (L B : Nat) : Nat := (2 * B + 1) * (gapBound L B + 1)

/-- The guaranteed digit-sum escape horizon, retaining the initial width. -/
def escapeBound (L B : Nat) : Nat := 4 * (widthBound L B - L) + 5

theorem initial_le_widthBound (L B : Nat) : L ≤ widthBound L B := by
  have hgap : L ≤ gapBound L B := Nat.le_max_left _ _
  have hm := Nat.mul_le_mul_right (gapBound L B + 1)
    (show 1 ≤ 2 * B + 1 by omega)
  simp only [Nat.one_mul] at hm
  unfold widthBound
  omega

/-- A digit-sum bound through a finite horizon gives the same uniform
width bound at every time up to that horizon. -/
theorem bounded_prefix_width (n : Nat) (d : Nat → Nat) (L B N : Nat)
    (hc : Canonical n d L)
    (hs : ∀ t, t ≤ N → digitSum (orbit n t) ≤ B) :
    ∀ t, t ≤ N → (iterPairs (columnSum d L) L t).1 ≤ widthBound L B := by
  let q := columnSum d L
  let K := gapBound L B
  have ha : Admissible L q := NormalizationBridge.canonical_admissible n d L hc
  have hK : 2 * B + 2 ≤ K := Nat.le_max_right _ _
  have hLK : L ≤ K := Nat.le_max_left _ _
  have hm : ∀ t, t ≤ N →
      wordSum (iterPairs q L t).2 (iterPairs q L t).1 ≤ 2 * B := by
    intro t ht
    rw [iterPairs_wordSum n d q L t hc (fun _ _ => rfl)]
    exact Nat.mul_le_mul_left 2 (hs t ht)
  have hz : ∀ t, t ≤ N → ZeroBound (iterPairs q L t).2 (iterPairs q L t).1 K := by
    intro t
    induction t with
    | zero =>
      intro _ a k _ hlen _
      change a + k ≤ L at hlen
      omega
    | succ t ih =>
      intro ht
      exact zeroBound_next (iterPairs q L t).2 (iterPairs q L t).1 (2 * B) K
        (iterPairs_admissible q L t ha) (hm t (by omega)) (ih (by omega)) hK
  intro t ht
  exact length_le_of_mass_zero_runs (iterPairs q L t).2
    (iterPairs q L t).1 (2 * B) K (hm t ht) (hz t ht)

/-- A finite digit-sum ceiling constrains the elapsed time. -/
theorem bounded_prefix_time (n : Nat) (d : Nat → Nat) (L B N : Nat)
    (hc : Canonical n d L)
    (hs : ∀ t, t ≤ N → digitSum (orbit n t) ≤ B) :
    N + 4 * L ≤ 4 * widthBound L B + 4 := by
  have ha := NormalizationBridge.canonical_admissible n d L hc
  have hg := DecimalWidthGrowth.width_lower_bound (columnSum d L) L N ha
  have hw := bounded_prefix_width n d L B N hc hs N (Nat.le_refl N)
  omega

/-- Explicit escape for every canonical positive input. No initial
digit-sum bound is needed: if it already exceeds `B`, time zero works. -/
theorem digitSum_escape_of_canonical (n : Nat) (d : Nat → Nat) (L B : Nat)
    (hc : Canonical n d L) :
    ∃ t, t ≤ escapeBound L B ∧ B < digitSum (orbit n t) := by
  apply Classical.byContradiction
  intro hnone
  have hs : ∀ t, t ≤ escapeBound L B → digitSum (orbit n t) ≤ B := by
    intro t ht
    have hnot : ¬ B < digitSum (orbit n t) := by
      intro hgt
      exact hnone ⟨t, ht, hgt⟩
    omega
  have hh := bounded_prefix_time n d L B (escapeBound L B) hc hs
  have hinit := initial_le_widthBound L B
  unfold escapeBound at hh
  omega

/-- Fully numeric finite-time escape: a positive ordinary integer orbit
exceeds every digit-sum ceiling by an explicit computable horizon. -/
theorem digitSum_escape (n : Nat) (hn : 0 < n) (B : Nat) :
    ∃ t, t ≤ escapeBound (decimalLength n) B ∧ B < digitSum (orbit n t) := by
  obtain ⟨d, L, hc⟩ := canonical_exists n hn
  have hlength := decimalLength_of_canonical n d L hc
  rw [hlength]
  exact digitSum_escape_of_canonical n d L B hc

/-- The slightly simpler coarse horizon requested without a subtraction. -/
theorem digitSum_escape_coarse (n : Nat) (hn : 0 < n) (B : Nat) :
    ∃ t, t ≤ 4 * widthBound (decimalLength n) B + 5 ∧
      B < digitSum (orbit n t) := by
  obtain ⟨t, ht, hgt⟩ := digitSum_escape n hn B
  refine ⟨t, ?_, hgt⟩
  unfold escapeBound at ht
  omega

/-- The maximum ordinary digit sum among the first `N + 1` orbit states. -/
def runningMax (n : Nat) : Nat → Nat
  | 0 => digitSum n
  | N + 1 => max (runningMax n N) (digitSum (orbit n (N + 1)))

theorem digitSum_le_runningMax (n N t : Nat) (ht : t ≤ N) :
    digitSum (orbit n t) ≤ runningMax n N := by
  induction N with
  | zero =>
    have heq : t = 0 := by omega
    subst t
    exact Nat.le_refl _
  | succ N ih =>
    by_cases htN : t ≤ N
    · exact Nat.le_trans (ih htN) (Nat.le_max_left _ _)
    · have heq : t = N + 1 := by omega
      subst t
      exact Nat.le_max_right _ _

/-- The recursively computed running maximum is attained by an actual
state within the claimed finite horizon. -/
theorem runningMax_attained (n N : Nat) :
    ∃ t, t ≤ N ∧ digitSum (orbit n t) = runningMax n N := by
  induction N with
  | zero => exact ⟨0, Nat.le_refl _, rfl⟩
  | succ N ih =>
    by_cases hnew : runningMax n N ≤ digitSum (orbit n (N + 1))
    · refine ⟨N + 1, Nat.le_refl _, ?_⟩
      simp only [runningMax, Nat.max_eq_right hnew]
    · obtain ⟨t, ht, heq⟩ := ih
      refine ⟨t, by omega, ?_⟩
      have hold : digitSum (orbit n (N + 1)) ≤ runningMax n N := by omega
      simpa only [runningMax, Nat.max_eq_left hold] using heq

/-- Exact lower-growth constraint on the running maximum. For fixed
initial length its right side is quadratic in the maximum digit sum. -/
theorem runningMax_lower_bound (n : Nat) (hn : 0 < n) (N : Nat) :
    N + 4 * decimalLength n ≤
      4 * ((2 * runningMax n N + 1) *
        (max (decimalLength n) (2 * runningMax n N + 2) + 1)) + 4 := by
  obtain ⟨d, L, hc⟩ := canonical_exists n hn
  have hlength := decimalLength_of_canonical n d L hc
  rw [hlength]
  exact bounded_prefix_time n d L (runningMax n N) N hc
    (fun t ht => digitSum_le_runningMax n N t ht)

#print axioms decimalLength_of_canonical
#print axioms bounded_prefix_time
#print axioms digitSum_escape
#print axioms digitSum_escape_coarse
#print axioms runningMax_attained
#print axioms runningMax_lower_bound

end DecimalQuantitativeMass
