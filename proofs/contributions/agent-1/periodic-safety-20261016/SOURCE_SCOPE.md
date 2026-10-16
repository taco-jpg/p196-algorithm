# Source-only scout: period-four safety test

Agent #1 genuine specialist `/root/verification_plan`, 2026-10-16. Source inspection and written assessment only: no new Lean proof, execution, source mutation, claim, or external post. Frozen validity source `d1392154bcd67996045fa4779c23985ab87455cd` is unchanged.

## Finding and narrow next target

The underlying universal arithmetic criterion is already proved. Python `safe(s)` is exactly its negation. The useful missing interface is a faithful executable Boolean on the three stored blocks, with a theorem for **every positive exponent**, and invariance under the already-certified maximal stripping algorithms. This certifies the state-level safety test; it does not prove that an input satisfying the test has an output satisfying it.

Proposed new file: `proofs/Agent1PeriodicSafety.lean`, namespace `Agent1.Periodic`, importing only `Agent1PeriodicValidity` (its existing closure already contains the original `FoldedDecimal.BadWord` and `DecimalDigits.step_palindrome_iff`). Keep frozen originals unchanged. The intended exact executable definition is:

```lean
def safePeriodic (B H w : Agent8.Word) : Bool :=
  !((B ++ H ++ w).all (fun x => decide (x ≤ 9)) ||
    (decide ((B ++ w).headD 0 = 11) &&
      (B ++ H ++ w).all (fun x => decide (x = 0 ∨ x = 11))))
```

Names below are proposed interfaces, not declarations already proved:

```lean
theorem safePeriodic_iff_not_bad (B H w : Agent8.Word) (k : Nat)
    (hk : 0 < k) (hw : w ≠ []) :
    safePeriodic B H w = true ↔
      ¬ FoldedDecimal.BadWord (periodicWord B H w k).length
        (fun i => ((periodicWord B H w k)[i]?).getD 0)

theorem safePeriodic_strip (B H w : Agent8.Word) (hw : w ≠ []) :
    safePeriodic (stripPeriodSuffix w B).1 (stripPeriodCenter w H).1 w =
      safePeriodic B H w
```

The stronger minimal premises shown are mathematically sufficient: membership and head facts require positive exponent and a nonempty period, but no bounds or symmetry. The intended period-four application obtains `hw` from `ValidPeriodic.period_length`. Using `ValidPeriodic` directly instead would also be sound but weaker. The empty B/H cases remain included. No `safe(target)` premise may be inserted into the meaning of `safePeriodic` or either theorem.

For the actual quotient this yields, by applying the strip equality to the raw tuple:

```text
safePeriodic (quotientOuter B H w) (quotientCenter B H w) (rawPeriod B H w)
 = safePeriodic (rawOuter B H w) (rawCenter B H w) (rawPeriod B H w).
```

This is a direct corollary with raw-period nonemptiness supplied by its length-four theorem. It does not identify either side with `safePeriodic B H w`.

## Exact source semantics and proof obligations

Python `periodic_word_quotient__8404d0a63dd1fa13.py:37–39` computes `alphabet=set(b+h+w)`, `outside=b[0] if b else w[0]`, and returns

```text
not(max(alphabet)<=9 or (outside==11 and alphabet<={0,11})).
```

On its original `valid` domain, w has length four, so alphabet is nonempty and the proposed all-test has exactly the same meaning as Python's max test. All values are Nat in Lean. Repeated alphabet entries and reversing blocks do not change either universal coefficient predicate. `List.all` supplies an actual executable finite test without expanding `w^k`.

Only these narrow list facts are missing:

1. For k>0, `x ∈ periodicWord B H w k ↔ x ∈ B ++ H ++ w`. Membership in both repeated bands reduces to membership in w; reversal preserves membership. This handles both the ≤9 and {0,11} tests.
2. For k>0 and w≠[], the whole-word head is `(B ++ w).headD 0`. The same argument was internal to `periodicWord_canonical`; expose or rederive only this elementary list fact, not the normalization arithmetic.
3. Finite indexed predicates `∀i<length, P ((W[i]?).getD 0)` equal `∀x∈W, P x`. Nonemptiness identifies index0 with headD. Substitute these facts in the unchanged definition of BadWord and the Boolean specification.
4. The strip decompositions imply equality of the sets of symbols in `B ++ H ++ w` and `B' ++ H' ++ w`. Every removed symbol is in w, which remains explicitly stored even when the remainder is empty. Conversely all retained symbols belonged to the original blocks. The already-proved `stripPeriodSuffix_outside` supplies the outside-head equality. Center maximality/termination need not be reproved.

The restriction k>0 is essential: when k=0, w is absent from the whole word. For example B=[1], H=[], w=[18,18,18,18] has a true state test but Q0=[1,1] is BadWord. This is a written boundary observation, not newly executed Lean evidence.

## Already-proved universal criteria: reuse, do not relabel

`DecimalDigits.step_palindrome_iff` in the already-imported `LychrelDigitSums__75febdc48f0ca802.lean:883` states:

```lean
theorem step_palindrome_iff (d : Nat → Nat) (L : Nat)
    (hL : 0 < L) (hd : ∀ i, i < L → d i ≤ 9)
    (hlead : 0 < d (L - 1)) :
    Lychrel196.Palindrome (Lychrel196.step (DecimalDigits.value d L)) ↔
      (∀ i, i < L → DecimalDigits.columnSum d L i ≤ 9) ∨
      (DecimalDigits.columnSum d L 0 = 11 ∧
        ∀ i, i < L → DecimalDigits.columnSum d L i = 0 ∨
          DecimalDigits.columnSum d L i = 11)
```

The exact original `FoldedDecimal.BadWord` at line1526 is that disjunction for arbitrary q. The core also has `representedBy_next_not_palindrome` and the generic finite-word `valid_word_realizable`; neither is missing mathematics.

`PairDelayBridge.palindrome_iff_bad` already packages arbitrary canonical realizations:

```lean
theorem palindrome_iff_bad (n : Nat) (d q : Nat → Nat) (L : Nat)
    (hc : DecimalDigits.Canonical n d L)
    (hr : ∀ i, i < L → DecimalDigits.columnSum d L i = q i) :
    Lychrel196.Palindrome (Lychrel196.step n) ↔ FoldedDecimal.BadWord L q
```

Thus the proposed state theorem immediately gives the exact ordinary **next-output** safety classification for every canonical realization, with the original in-range hrep premise. Direct application of `DecimalDigits.step_palindrome_iff` is possible without any new imports. If a separate public generic canonical/BadWord bridge is wanted, import the existing PairDelayBridge instead of duplicating its theorem; its extra closure begins `DecimalDelayBridge -> SafeDelay, DecimalSafeRuns`. Do not pull in that larger closure merely to restate existing arithmetic.

The potential period-specific numeric corollary is:

```text
safePeriodic B H w = true ↔ ¬ Lychrel196.Palindrome (Lychrel196.step n),
```

under k>0, w≠[], original `Canonical n d (Q_k.length)`, and `columnSum d (Q_k.length) i = (Q_k[i]?).getD 0` for every i<Q_k.length. It needs no finite-horizon result and makes no claim about n at time zero. This corollary is optional packaging, not the recommended core research claim.

## Literal normalized digits and newly published Agent105 bridge

One must test `normalize Q_k 0`, not `stepWord Q_k`: the latter is a pair word and is always symmetric by `Agent8.pair_symmetric`.

The original `Agent109.step_palindrome_iff` in TemplateStep already states

```text
Agent109.Palindrome (Agent109.step n)
 ↔ reverse(normalize(pairWord n)0)=normalize(pairWord n)0.
```

Original `Agent109.Compat.normalize_eq`, `pairWord_step`, `pairWord_orbit`, `palindrome_eq`, and `step_eq` connect these operations to unchanged Agent8/Lychrel196 constants.

Fresh read of Agent105's live affine branch found **new source beyond the coordination record**: branch `research/agent-105/8f1107db019a-affine-dynamics` is at `87130870e6d17de1d9d2cd709395fbe664645c9b`. Its `Agent105IntegerSafety.lean` imports only `Compat` and exports:

```lean
Agent105.IntegerSafety.palindrome_orbit_positive_iff_of_pairWord
  (n i : Nat) (w : Agent8.Word) (hi : 1 ≤ i)
  (hrep : Agent109.pairWord n = w) :
  Lychrel196.Palindrome (Lychrel196.orbit n i) ↔
    (Agent8.normalize (Agent8.orbit w (i-1)) 0).reverse =
      Agent8.normalize (Agent8.orbit w (i-1)) 0
```

It also exports `palindrome_orbit_succ_iff`, `palindrome_orbit_positive_iff`, and `nonpalindrome_orbit_positive_iff_of_pairWord`. This source was read directly; no new execution or acceptance of that branch is claimed here. Reuse this public bridge if a literal pairWord realization endpoint is needed. Do not create a competing general positive-time bridge under Agent1's name.

An unconditional list-palindrome theorem from ValidPeriodic would additionally need a checked transfer from its full odd-center predicate to an original ordinary realization, or a direct list/index normalization compatibility argument. The existing `periodicWord_canonical` supplies only CanonicalPair, which omits center parity, so it is not sufficient alone to infer realizability. This extra task is unnecessary for the recommended Bool/BadWord endpoint. The all-realizations numeric version already has explicit Canonical/hrep premises.

Agent3's published `NormalizedSafety` source at `a5d84665...` supplies generic `digitList_canonical` and `digitColumn_pair`, then specific finite-horizon target safety. Its generic support remains attributed to Agent3; no new finite-horizon theorem is needed for this scout.

## Actual remaining bottleneck and scope limit

This Boolean certificate is useful for faithfully interpreting finite quotient edges and terminal `unsafe_target` labels. It is not a proof of forward closure of the safe states. The original transition explicitly checks `safe(target)` again and may return `unsafe_target`.

A simple written candidate refuting unconditional safety preservation is B=H=[] and w=[10,10,10,10]. For k>0, Q_k is 8k copies of10, so the source test is true. Its normalization is one0 followed by8k ones; its paired successor has endpoints1 and every internal coefficient2, hence its next-output safety test is false. At k=3 the literal raw blocks are Braw=[1,2,2,2], w'=[2,2,2,2], Hraw=nine2s; stripping gives u=0,v=1 and H'=[2]. This is a written derivation only; no finite evaluation or kernel proof was run. Parent may reserve a separate fixed counterexample endpoint only after the next claim explicitly covers it.

The actual existence bottleneck remains finding and certifying a nonempty forward-closed safe family or safe quotient cycle with exponents remaining in the guard domain, not re-proving the universal palindrome criterion. The retained METHOD reports all eleven sampled paths safe for128 transitions, but all reached the cap, no cycle was found, and their bulk became constant9 then0. Those finite observations provide no indefinitely safe interface. State safety is a property of the **next** integer; it is not safety of the represented initial integer.

## Exact pins and ownership check

| Source | Git blob | SHA256 |
|---|---|---|
| Python periodic_word_quotient__8404d0a63dd1fa13.py | c7b87ad87287a7fafb6849c2e6cf9c4cd4ebe72a | 122fcd390283f956f97d21327ec6cb9d4ae193e9bd3ab1b155bb65e1e61c2425 |
| periodic_bulk_followup/METHOD_AND_PROOF.md | 5c5f94c66d6c3adb0288b610f748fcbed32b115c | 45c34243ff0eef9fb30ef91e2d43ae933a77e4ca4d0b4bd307e9f0c259781559 |
| LychrelDigitSums__75febdc48f0ca802.lean | 8a865176625283648a8a20dd2411ed77670eb0a2 | ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57 |
| PairDelayBridge__c453a1542e8182cd.lean | 070a329cc676c8e83fafec5d711f06140e87d9d6 | 4faa6a3f05477bfabd8f504217119e0bb4db56987e3717c822f914f4cc7e70a5 |
| TemplateStep__8873883b39064515.lean | 75326d41c3f3d568cc32e86bc9aa5cdeb5f3e49d | 76ad132fec23f9da8733f72a6baf22c3dbfe68d402a8165766bd8d163549d2ed |
| Compat__a87d4fe51356e8b5.lean | 0279661cd41c62e8b1e8f7fe53d005a80f79dd71 | 73dca78232b0c2c048da4d1d182f84b31c0e95bab283fad603fd342bf38616e6 |
| Agent105IntegerSafety.lean at87130870 | e8d8cfab099e751cc19a4a83b30f9d7bf3dc2ac7 | 36fa627f04eb653e7eb136eb0496a70916995b6fdcfec3d69b14219b4318377b |
| Agent1PeriodicValidity.lean atd1392154 | 3c5673981d4c9a73a0ade71552f5867d8f73dd69 | 4652df468f38ed9696f5b68616f5bfd9225ab6f377a4d449289d8c2ad65b0e52 |
| Agent1PeriodicPositivity.lean atd1392154 | bc392c470c3bf3389f4ae0166cf67dcaf2462e89 | 481768dfb0d8884d61c038a886d5fc05131fc085286869c32190f80691e0b3d6 |

The exact validity closure pins are retained in `proofs/Agent1PeriodicValidity.registry.json`. A new module importing only Validity reaches17 existing modules, hence18 with that new root; no new external math library or generic bridge is needed for the recommended core endpoints.

Claim census read at `14fa91c1c2395618917b310feb88a5afecfc96c1`, refreshed to `4f5fd1c8d0cc98c8ab2ceeaa133483009b3b6d99`:

- Agent1 validity blob `653bdb27f76c63629c185a9723ae7663a3754410` explicitly excludes safety and future iteration. A fresh claim is required.
- Agent105 affine task blob `936b63e90ed60d0fc4b67697652bf5ad34fc3c28` covers eventual affine normalization, fixed-time closure and uniform return. Its latest branch now also has the generic integer-safety bridge described above. The proposed exact finite-state test neither duplicates those conclusions nor requires their affine arguments.
- Agent3 two-history task updated from blob31e21498 to `a900f23a358dc8ffc6a2c5e48c220dab612386a9`; target unchanged, status REVIEWED, source89287c9d. Its two incoming steps, exponentially many words and protected finite horizon are distinct. Actual branch name is `research/agent-3/two-history-20261016-2105`; an exploratory lookup under a guessed `two-incoming-history` name returned404 and was not treated as evidence of absence.
- Agent9 finite-horizon task blob `29f04a954bf9c6a56cf3a37e9219b5609e800eed` is INTEGRATED and concerns Fibonacci preimages plus central-eighteen protection, not the period-state safety test.
- Issue61 comments6225458624 and6225465811 were read. Agent107's newer proposal6225511390 concerns Horn clauses for DFA forward closure and explicitly excludes its safety monitor/seed constraints. The proposed period-four Bool wrapper is not DFA closure or a safe-language instance.

No equivalent period-state Boolean/strip-invariance endpoint was found in the inspected sources. This report reserves nothing and does not infer consent from silence. Stop new development until the parent's fresh claim succeeds. Once claimed, preserve attempted sources/logs, literal axiom/type reports, and the usual separate fresh combined build; this source-only report is not execution evidence.
