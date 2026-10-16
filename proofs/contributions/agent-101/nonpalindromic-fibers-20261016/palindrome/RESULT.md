# Initial palindromes in complete numeric profile fibers

## Status and ownership

**PASS.** `proofs/Agent101PalindromeFibers.lean` compiled with Lean 4.19.0, and all 14 exported theorems passed an explicit `--trust=0` import and axiom audit.

The accepted source SHA-256 is:

```text
27ebcd2a7b790d87e45f19e51d0d7e2ff977f297742936503b9552026e3ea633
```

This work belongs to `agent101-nonpalindromic-fiber-count-20261016`, coordination commit `5020db13f2d5dc3bef8a8074248c9873e1404ec5`, scope `issue6224940248`. The research-inventory worker authored this module and its evidence. The four existing Agent101 foundation modules were left unchanged. The parent owns the separate filtering and exact subtraction module.

## Complete result

For every half-profile `h : List Nat`, optional central sum `c : Option Nat`, and ordinary natural number `n`, the main theorem is:

```lean
palindrome_mem_numericFiber_iff (h : List Nat) (c : Option Nat) (n : Nat) :
  (n ∈ numericFiber h c ∧ Lychrel196.Palindrome n) ↔
    0 < profileCount h c ∧
      (∀ s ∈ coefficientWord h c, s % 2 = 0) ∧
      n = natValue ((coefficientWord h c).map (fun s => s / 2))
```

Thus the complete fiber contains an initially palindromic ordinary integer precisely when its exact multiplicity is positive and every prescribed pair sum is even. In that case the unique initial palindrome is obtained by halving every entry of the complete symmetric coefficient word and reading the resulting canonical decimal digits.

The theorem uses the repository's original `Lychrel196.Palindrome`, which is equality with actual decimal reversal. The public endpoint has no coefficient-bound hypothesis and no additional chosen-realization hypothesis. It covers all natural-number profiles, including unrealizable profiles, empty profiles, zero singletons, odd centers, and entries exceeding the decimal pair-sum range.

Other principal exports are:

```lean
palindrome_natValue_iff_reverse (ds : List Nat) (hd : canonicalDigits ds) :
  Lychrel196.Palindrome (natValue ds) ↔ ds.reverse = ds

half_coefficientWord_mem_numericFiber (h : List Nat) (c : Option Nat)
    (hp : 0 < profileCount h c)
    (he : ∀ s ∈ coefficientWord h c, s % 2 = 0) :
  natValue ((coefficientWord h c).map (fun s => s / 2)) ∈ numericFiber h c ∧
    Lychrel196.Palindrome
      (natValue ((coefficientWord h c).map (fun s => s / 2)))

palindrome_numericFiber_exists_iff (h : List Nat) (c : Option Nat) :
  (∃ n, n ∈ numericFiber h c ∧ Lychrel196.Palindrome n) ↔
    0 < profileCount h c ∧
      (∀ s ∈ coefficientWord h c, s % 2 = 0)

palindrome_numericFiber_unique (h : List Nat) (c : Option Nat) (n m : Nat)
    (hn : n ∈ numericFiber h c ∧ Lychrel196.Palindrome n)
    (hm : m ∈ numericFiber h c ∧ Lychrel196.Palindrome m) : n = m
```

`palindrome_numericFiber_eq_half` gives the explicit-value consequence for an individual member. `exports.json` lists every public theorem, including the digit-list lemmas used in the proof.

## Why the existence and uniqueness conditions are complete

For a canonical digit list, the original decimal palindrome theorem identifies numerical palindromicity with reflection symmetry of the list. A symmetric digit list has pair sums `d + d` in every position, so each sum is even and dividing the complete pair-sum word by two recovers the original digit list exactly. Consequently two palindromic members of the same complete profile have the same explicit value.

For the converse, positive `profileCount` and `length_canonicalWords` supply a canonical realization of the profile. Its pair sums are at most 18. Their halves are therefore decimal digits. At the most significant position, the pair sum is positive because the original most significant digit is positive; evenness then makes its half positive. This proves that the halved profile itself is canonical, including the leading-digit condition. Symmetry of `coefficientWord` and evenness recover precisely the original profile under `digitPairSums`. The complete digit-level membership theorem then supplies membership in `numericFiber`, and the original palindrome equivalence supplies actual numerical palindromicity.

This argument handles invalid profiles through their exact zero multiplicity instead of adding a separate profile-validity premise. For the empty profile or a zero single-digit profile, `profileCount` is zero and the right-hand side is false. For a valid single-digit profile, the unique halved digit is positive and is its own reverse. Internal zero digits remain allowed.

## Verification and retained attempts

- `attempts/attempt-006.lean` is byte-for-byte identical to the accepted source. Its actual Lean return code is 0; source compilation took approximately 0.516 seconds.
- `compile.py` records each attempted source, exact command, actual Lean return code, elapsed time, and source hash. Attempts 001 through 006 and all their logs and JSON metadata remain present. Failed attempts were not overwritten.
- `Audit.lean` imports the compiled module and applies `#print axioms` to all 14 exports. `audit.py` ran this with `--trust=0`; the return code is 0.
- The union of reported theorem dependencies is `propext`, `Classical.choice`, and `Quot.sound`. One structural theorem has no axioms; no export reports any additional axiom.
- The accepted source contains no `sorry`, `admit`, `axiom`, or `native_decide` token.
- `verification.json` pins the accepted source, generated `.olean`, Lean version, audit command, import path, every imported source and `.olean` hash, and the agreement of the four frozen Agent101 source copies with their canonical repository files.

The usable module artifact is `build/Agent101PalindromeFibers.olean`. Its imports resolve with:

```text
LEAN_PATH=<this evidence directory>/build:/workspace/scratch/2a8a87fd78df/agent101-numeric-build
```

This report records author verification. It does not describe the author's own proof as an independent semantic review. Independent review and any later integration are separate activities.

## Exact scope boundary

The result characterizes initial palindromes in a complete fixed-profile numeric fiber. It does not assert that a following iterate is nonpalindromic, and it does not itself count a safe subset requiring that additional property. The separate parent module can use existence and uniqueness to remove exactly zero or one initial palindrome; a safety statement also needs the relevant later-iterate hypotheses.
