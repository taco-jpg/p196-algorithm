# Agent 101: complete enumeration of original digit splits

Status: **accepted source compiled with Lean 4.19.0; all 31 exports audited**.

## Accepted source and dependencies

- Source: `proofs/Agent101SplitEnumeration.lean`
- Namespace: `Agent101`
- Direct import: `Agent101MultiplicityBounds`
- Transitive project import: `Agent101DigitPairs`
- Source SHA-256: `8ce57c88984df3a965e33c181f4d8f138258fe48b14e2b835333fe6c30d79684`

The source defines seven objects and proves 24 theorems. It uses the already
verified pair and center enumerators from `Agent101DigitPairs`, and the
`natProduct` and `profileCount` definitions from `Agent101MultiplicityBounds`.
It does not reprove the numeric representation or fixed-width value
injectivity results used by the separate numeric bridge.

## Exact semantic result

Digit lists are written with the units digit first. For a half-profile `h`
and optional center coefficient `c`, define

```lean
coefficientWord h c = h ++ c.toList ++ h.reverse
digitPairSums ds = List.zipWith Nat.add ds ds.reverse
digitsBounded ds = (∀ d ∈ ds, d ≤ 9)
canonicalDigits ds = (digitsBounded ds ∧ 0 < ds.getLastD 0)
```

`rawWords` recursively enumerates every ordered pair of digits whose sum is
the next coefficient, allowing zero on either side. `canonicalWords` requires
the high digit of the outermost pair to be positive. A single center digit
is admitted only when it is positive and its doubled coefficient is even
and at most 18. The empty list is never canonical.

The accepted, nonrecursive membership specifications are:

```lean
mem_rawWords (h : List Nat) (c : Option Nat) (ds : List Nat) :
  ds ∈ rawWords h c ↔
    ds.length = (coefficientWord h c).length ∧
    digitsBounded ds ∧ digitPairSums ds = coefficientWord h c

mem_canonicalWords (h : List Nat) (c : Option Nat) (ds : List Nat) :
  ds ∈ canonicalWords h c ↔
    canonicalDigits ds ∧ digitPairSums ds = coefficientWord h c
```

`canonicalWords_length` also exports the width equality for each member.
The length hypothesis in the raw membership theorem is redundant once the
coefficient equality is known; it is retained for convenient decomposition.
The canonical membership theorem has no extra width hypothesis.

Both `rawWords_nodup` and `canonicalWords_nodup` are proved for every profile,
including profiles for which the enumeration is empty.

## Exact counts

For every `h` and `c`:

```lean
length_rawWords (h : List Nat) (c : Option Nat) :
  (rawWords h c).length =
    centerCount c * natProduct (h.map (pairCount false))

length_canonicalWords (h : List Nat) (c : Option Nat) :
  (canonicalWords h c).length = profileCount h c
```

The explicit nonempty-half case is:

```lean
length_canonicalWords_cons (s : Nat) (h : List Nat) (c : Option Nat) :
  (canonicalWords (s :: h) c).length =
    pairCount true s * centerCount c *
      natProduct (h.map (pairCount false))
```

For an internal pair coefficient `s`, `pairCount false s` is `s + 1` when
`s ≤ 9`, `19 - s` when `10 ≤ s ≤ 18`, and zero otherwise. For the outer
pair, the first branch is `s`, accounting exactly for the forbidden high
digit zero. `centerCount none` is one; `centerCount (some s)` is one exactly
when `s ≤ 18` and `s % 2 = 0`, and is zero otherwise. With an empty half,
`profileCount [] none = 0` and the single-center case additionally requires
`0 < s`.

Because the enumeration is complete and has no duplicates, these lengths
count all original digit lists with the specified profile. Transport to
ordinary natural numbers and reverse-add fibers belongs to
`Agent101NumericFibers.lean`.

## Proof structure

`wrapDigits a b ds = a :: (ds ++ [b])` exposes the outer low and high digits.
The file proves its injectivity, the exact pair-sum equation under wrapping,
and the corresponding boundedness and leading-digit conditions. Every list
of length at least two can be decomposed into this form. These facts give
both directions of the semantic specification by induction on `h`.

For no-duplicates, the same injectivity separates different outer pairs and
preserves distinct inner lists. A general `nodup_wrappedProduct` lemma handles
the `flatMap` of each pair's mapped inner enumeration. The analogous
`length_wrappedProduct` lemma gives the exact product count. No recursive
specification is used as a replacement for the final semantic theorem.

## Verification evidence

- `attempts/attempt-004.lean`: exact accepted source snapshot.
- `attempts/attempt-004.log`: successful source compilation output (empty).
- `attempts/attempt-004.json`: compiler command, `LEAN_PATH`, elapsed time,
  and Lean exit code zero.
- `Audit.lean`: `#print axioms` for every exported definition and theorem.
- `axioms.log`: all 31 axiom reports; the seven definitions use no axioms;
  theorem dependencies are subsets of `propext`, `Classical.choice`, and
  `Quot.sound`. There is no `sorryAx` or project axiom.
- `exports.json`: the 31 audited names.
- `verification.json`: exact compiler version, audit command and exit code,
  plus source and dependency artifact hashes.
- `source.sha256`: accepted source digest.

All failed source attempts and their actual diagnostics remain under
`attempts/`. `ListApi*.lean` and their logs are retained API probes, not
accepted proof modules. Attempts 001--003 were not accepted; attempt 004 is
the first successful complete build. The final correction expands natural
number multiplication over addition in the general product-length lemma.

The reusable compiled module was generated at:

```text
/workspace/scratch/2a8a87fd78df/agent101-runtime/enumeration-build/Agent101SplitEnumeration.olean
```

Its import path must also contain `agent101-runtime/pairs-build` and
`agent101-parent-build`. These scratch artifacts are a convenience; the
accepted source and verification evidence are the reproducible deliverable.
