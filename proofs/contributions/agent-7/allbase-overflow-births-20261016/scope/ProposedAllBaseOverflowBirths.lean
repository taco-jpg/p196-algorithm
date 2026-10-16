/-
READ-ONLY SCOPE PROPOSAL, NOT A CLAIM OR AN ESTABLISHED THEOREM.
No proof implementation has begun. Root must publish the exact remote claim.

Existing notation to reuse:
  b : Int, xs : List (Int × Bool), L := xs.length,
  q_j := xs[j].1 for j < L,
  c_j := ActualBaseBirths.incoming b xs j,
  out := PhysicalWidth.actualDigits b xs,
  Q := ReverseAdd.pairs out.

Core hypotheses:
  2 ≤ b;
  ResetNormalization.Bounded b xs;
  (xs.map Prod.fst).reverse = xs.map Prod.fst;
  PhysicalWidth.terminal b 0 (ResetNormalization.ordinaryTags xs) = 1.

Desired actual-width/index interface:
  out = PhysicalWidth.body b 0 (ResetNormalization.ordinaryTags xs) ++ [1];
  out.length = L + 1;
  for j < L, out[j] = (q_j + c_j) % b;
  for j < L, c_(j+1) = (q_j + c_j) / b;
  for 0 < i < L,
    Q[i] = (q_i + c_i) % b + (q_(i-1) + c_(L-i)) % b.

Desired complete interior zero classification, for 0 < i < L:
  Q[i] = 0 iff
    (q_(i-1)=0 ∧ q_i=0) OR
    (q_(i-1)=b-1 ∧ q_i=b-1 ∧ c_i=1 ∧ c_(L-i)=1) OR
    (q_(i-1)=b-1 ∧ q_i=b ∧ c_i=0) OR
    (q_(i-1)=b ∧ q_i=b-1 ∧ c_(L-i)=0).

Desired complete interior maximum classification, for 0 < i < L:
  Q[i] = 2*b-2 iff
    (q_(i-1)=2*b-2 ∧ q_i=2*b-2) OR
    (q_(i-1)=b-1 ∧ q_i=b-1 ∧ c_i=0 ∧ c_(L-i)=0) OR
    (q_(i-1)=b-1 ∧ q_i=b-2 ∧ c_i=1) OR
    (q_(i-1)=b-2 ∧ q_i=b-1 ∧ c_(L-i)=1).

Consequent one-step birth statement to include if scope permits:
  any new interior zero or maximum, excluding the corresponding old
  homogeneous adjacent pair, has q_(i-1)=b-1 OR q_i=b-1.

Desired endpoint interface, deriving L>0 from the computed carry:
  Q[0] = Q[L] = 1 + q_0 % b.
  For b≥3, neither endpoint is zero or 2*b-2.
  At b=2, an endpoint is maximal exactly when q_0=1; zero remains impossible.
  The binary case must not be silently discarded or assigned the decimal
  endpoint nonextremality statement.

Canonical specialization:
  Add digits : List Int, ReverseAdd.DigitBounds b digits,
  PhysicalWidth.PositiveLast digits, xs.map Prod.fst = ReverseAdd.pairs digits.
  Reuse ReverseAdd.reverse_add_normalization to assert output digit bounds,
  positive final digit, and eval b out = eval b digits + reversedValue b digits,
  together with the above computed-overflow classifications.

All formulas above are proposed targets, not completed Lean declarations.
No global ancestry, population growth, recurrence, or palindrome-avoidance
conclusion is included.
-/
