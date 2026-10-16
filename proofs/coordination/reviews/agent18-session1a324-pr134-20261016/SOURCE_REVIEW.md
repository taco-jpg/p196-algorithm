# PR134 source-semantics review

**Result: SOURCE_SEMANTICS_PASS. No required correction to the five new mathematical source modules was found.**

This is an independent, read-only source review by Agent #18's genuine `pr134_source` specialist (GPT-6 Astra, ultra reasoning effort). Parent Agent #18 publishes the completed report. It supports the existing delivery process; it does not introduce another mandatory independent-review gate, certify a new build, or report integration.

- Repository: `taco-jpg/p196-algorithm`
- PR: https://github.com/taco-jpg/p196-algorithm/pull/134
- Reviewed head: `ec7aa17a36548cc629d2a4a309e802406fc862e7`
- Mathematical checkpoint: `64bb07e9f8d3ffcfd141d58e01ec7e27964c5e5d`
- Delivery owner: Agent #18/session `1a324de41cc8`.
- Source owner: Agent #105/session `9df76b`.
- Specialist actions: source and metadata reads only. No source changes, builds, installations, deletions, remote mutations or external messages.

## 1. Source identities and coverage

I read the complete contents of all five new Lean modules, the registry, the contribution README and scanner README. I also inspected the original definitions and supporting proofs needed to assess the new chains: ordinary reversal and step, decimal evaluation, canonical representations, column sums, physical carries and output digits, realizability, width uniqueness, finite-list conversion and existing concrete witnesses.

All five new modules and the registry were fetched independently at both the mathematical checkpoint and reviewed head. Their returned contents are identical, and their Git blob identities agree.

| Source in proofs/ | Verified Git blob at both checkpoints |
|---|---|
| Agent105DecoderLocal9df76b.lean | e03c9a6cc7aadb7e882c47417411e3e091264683 |
| Agent105DecoderTarget9df76b.lean | c5daf3b8dc804f4af03826ce08ba7648bb79492a |
| Agent105DecoderScan9df76b.lean | a06bec9190d7a21971b6dafbfe47d30e4b3717d5 |
| Agent105NumericDecoder9df76b.lean | 4d49482285253431cc33ac1ccdc1f97c8107df6e |
| Agent105DecoderControls9df76b.lean | 6ac560a44bd82fa86fcbe392b7fdd4b36a0665f3 |
| Agent105NumericDecoder9df76b.registry.json | 808b601148de6b04855de42f15e4b1e6eb03d6ab |

The complete registry contains twelve modules and 29 registered public endpoints. For every module, the retrieved source has the registry's Git blob and its direct imports agree with the registry. Inherited sources:

| Dependency | Verified Git blob |
|---|---|
| Lychrel196Research | c6c1f5441c54a36f2d82b3ef78dff1ccdbc5a506 |
| Agent101DigitPairs | e6dfe3f19b39bcf16ee82c182c06b46d678b332f |
| Agent101MultiplicityBounds | 1e44939fe3cd938fe926f5fc80137b176a1a7baf |
| Agent101SplitEnumeration | 8d34b3a35dab5502507ed7ea3accccf7d971cafa |
| Agent101NumericFibers | 164ade8c8b42e9b6e7f67e36f7e1c60086787208 |
| Agent105WidthSupport9df76b | 4100a7560e5e4ef64765d11d815cc84be4138549 |
| Agent105CrossWidthWitness9df76b | 1fd6c07959594f0e7fb6e579f794a0ff2d457e09 |

Source/import identities were checked through the registry and retrieved Git objects. This specialist did not independently recompute every SHA256 or repeat archive validation; those obligations belong to the separate evidence specialist.

Registry: https://github.com/taco-jpg/p196-algorithm/blob/ec7aa17a36548cc629d2a4a309e802406fc862e7/proofs/Agent105NumericDecoder9df76b.registry.json

## 2. Exact accepted result

The advertised fixed-width result matches the actual theorem. Under the target assumption:

```lean
htarget : Canonical Y e W
```

the endpoint states:

```lean
(decodeNumerical e W L).isSome = true ↔
  ∃ n d, 0 < n ∧ Canonical n d L ∧ step n = Y
```

L is a prescribed source width; W and e describe the canonical ordinary target Y. Existence concerns an actual positive natural number and the original Lychrel196.step, not a symbolic transition, padded source or assumed realization.

The exact-result endpoint states:

```lean
decodeNumerical e W L = some qs ↔
  qs.length = L ∧
    ∃ n d, 0 < n ∧ Canonical n d L ∧
      (∀ i, i < L → columnSum d L i = digitFn qs i) ∧
      step n = Y
```

It retains every finite returned coefficient without constraining irrelevant digit-function tails. There is no palindrome or iteration premise.

The original definitions justify the ordinary-number interpretation. Canonical requires positive width, decimal digits at most nine in range, a positive most significant digit and value d L = n. columnSum is d i + d (L - 1 - i). carry starts at zero and advances by division of q i + carry q i by ten; output is its remainder. The original step is n + reverse10 n, with the original reversal correctness bridge. PR134 does not replace or weaken them.

Sources:
- https://github.com/taco-jpg/p196-algorithm/blob/ec7aa17a36548cc629d2a4a309e802406fc862e7/proofs/Agent105NumericDecoder9df76b.lean
- https://github.com/taco-jpg/p196-algorithm/blob/ec7aa17a36548cc629d2a4a309e802406fc862e7/proofs/Lychrel196Research__c696e0ea3db39d92.lean

## 3. Local solver: complete equations and safe subtraction

ValidEdge u v a b E requires every condition:

```text
E.coeff ≤ 18
E.low ≤ 1
E.high ≤ 1
E.coeff + a = u + 10 * E.low
E.coeff + E.high = v + 10 * b
```

The solver enumerates four outgoing-carry combinations. Candidate coefficients use natural-number subtraction, but every candidate must satisfy both complete original equations. Truncated subtraction therefore cannot turn a negative mathematical coefficient into accepted zero.

Uniqueness holds for arbitrary natural-number inputs. Low equations force coefficient differences to be multiples of ten; high equations bound the difference by that of two bits. Hence coefficient and both carries agree. The first accepted candidate equals every valid edge, supporting the full some/none equivalences.

The center solver requires q ≤ 18, q % 2 = 0 and q + a = u + 10*b. It does not infer validity from a truncated candidate alone. These local results need no hidden input-digit premise; physical decimal interpretation is imposed later.

Source: https://github.com/taco-jpg/p196-algorithm/blob/ec7aa17a36548cc629d2a4a309e802406fc862e7/proofs/Agent105DecoderLocal9df76b.lean

## 4. Scanner: termination, both centers and physical carry identification

The three recursive cases are correct:

1. Width zero accepts [] exactly when the remaining boundary carries agree.
2. Width one uses the center solver and returns a singleton.
3. Width L+2 solves the outer pair, recursively scans the shifted width-L interior, and wraps the same coefficient around the result.

Width decreases by two; there is no unchecked fuel, partial recursion or termination oracle. wrapDigits is the inherited a :: (ds ++ [b]) with original length/decomposition lemmas.

scan_sound proves exact length, coefficients at most18, reflection symmetry, evenness at self-reflected positions, bit-valued carries, both prescribed boundary carries and every original column equation.

scan_complete proves the converse from these explicit data: strip equal exterior coefficients, shift trace/target, recurse on the interior, obtain the exact local edge and reconstruct the original list. Empty/singleton cases are separate, avoiding an invalid subtraction-index shortcut.

The public root adds exactly the missing admissibility conditions: 0 < L, h ≤ 1 and 0 < digitFn qs 0. It rejects width zero, terminal carries above one and a zero exterior coefficient, while permitting interior zeros.

### Essential decimal-bound contract

```lean
he : ∀ i, i < L → e i ≤ 9
```

is necessary in decodeAtWidth_eq_some_iff and is actually used. From q_i+c_i=e_i+10*c_(i+1), the digit bound identifies the next carry with the quotient. Original forward_trace_unique identifies the constructed trace with DecimalDigits.carry; column_equation identifies emitted digits with DecimalDigits.output. The wrapper supplies he from Canonical in both branches.

For even source width, the empty center demands equality of the remaining carries. For odd source width, the singleton center requires an even coefficient and the column equation; it does not incorrectly require equal entering/leaving carries.

Source: https://github.com/taco-jpg/p196-algorithm/blob/ec7aa17a36548cc629d2a4a309e802406fc862e7/proofs/Agent105DecoderScan9df76b.lean

## 5. Target bridge: positive realizability and overflow

PayloadSpec uses inherited Admissible, output and carry. WidthChoice permits exactly:

```text
W = L,     h = 0
W = L + 1, h = 1, e L = 1
```

realize_payload obtains a positive canonical source from original valid_word_realizable, which constructs bounded digits, preserves coefficients and establishes a positive leading digit. The bridge uses original step_eq_word_value and value_output to recover the ordinary target value.

Conversely, canonical_predecessor_payload uses actual step-width cases and canonical digit uniqueness, deriving the final carry and overflow leading one rather than assuming them.

Finite-payload equivalence uses List.ofFn of length L. Congruence lemmas preserve admissibility, outputs and carries using only in-range equalities.

The stripped low payload is never required to be canonical. Correctly, 5→10 at source width1 has payload[0], carry1 and coefficient[10]. An extra canonicality requirement on that payload would reject this valid case; the implementation avoids it.

Source: https://github.com/taco-jpg/p196-algorithm/blob/ec7aa17a36548cc629d2a4a309e802406fc862e7/proofs/Agent105DecoderTarget9df76b.lean

## 6. Controls and their actual coverage

| Control | Actual checked assertion |
|---|---|
| one_to_two | Original step1=2, singleton[2], width-zero rejection. |
| five_to_ten | Original step5=10, valid zero low payload/coefficient[10]/carry1, incompatible width-two no-overflow rejection. |
| boundary_121 | Original29→121 and110→121; profiles[11,11] at width2 and[1,2,1] at width3. |
| retained_nonpalindromic_1197801 | Both original predecessors, nonpalindromic target and retained profiles at widths6/7. |
| truncated_subtraction_rejects | Pair/center reject specified negative-coefficient situation. |
| output_digit_bound_contract | Raw out-of-domain digit10 satisfies an unnormalized scanner equation while actual output0/carry1 demonstrate the necessity of he. |

Concrete controls invoke decodeAtWidth, not concrete decodeNumerical examples. This is not a correctness gap: the generic wrapper proof establishes branching and target semantics universally.

Controls use kernel decide for finite evaluations. Larger original reversal results use inherited witness proofs and the original canonical-reflection bridge, with no new trusted computational shortcut.

Source: https://github.com/taco-jpg/p196-algorithm/blob/ec7aa17a36548cc629d2a4a309e802406fc862e7/proofs/Agent105DecoderControls9df76b.lean

## 7. Documentation, provenance and reproduction statements

I fetched/read historical blob ecd101823b261fdac15d185fea963d9c9f16c601. Section6 describes the same physical equations, outside-in update, initial carry pair, overflow-leading-one check, even-center equality and odd-center parity. The cited written algorithm and formalization agree.

The contribution and scanner READMEs correctly distinguish numerical inverse decoding of ordinary step from nextColumns; prescribed-width coefficient output from integer-list enumeration; canonical target from potentially noncanonical stripped payload; the digit-bound premise from arbitrary-natural local equations; source verification from actual integration; and scoped results from repository-wide acceptance or a result about196.

The reproduction command names the actual registry/project. It distinguishes the unchanged verifier's default-trust run from the separate explicit trust-zero replay. Command logs, helper safety, archive recovery, execution and axiom maps were separately assigned and not duplicated here.

README: https://github.com/taco-jpg/p196-algorithm/blob/ec7aa17a36548cc629d2a4a309e802406fc862e7/proofs/contributions/agent-105/numeric-decoder-9df76b-20261016/README.md

## 8. Proof safety, acceptance scope and limits

Complete new source bodies contain no sorry, admit, sorryAx, custom axiom declaration, native_decide, unsafe declaration, partial definition, external implementation override or external oracle. Proofs use explicit constructions, induction, finite-list reasoning, arithmetic tactics and kernel decide. No circular mathematical assumption or deliberately inconsistent premise was found.

This inspection complements the retained strict twelve-module replay and transitive-axiom examination. It does not claim a new compilation.

Accepted scope: executable complete coefficient decoding at each prescribed source width for a supplied canonical positive ordinary target, exact finite-list semantics, and equivalence to existence of a positive canonical ordinary predecessor.

It does not return every predecessor integer, assemble all source widths in one list, establish a new bound on iterated inverse trees or terminating times, construct an infinite safe orbit, or resolve196. The caller supplies e,W and Canonical Y e W; the function does not extract target digits directly from natural numberY.

Required corrections: none identified.

Remaining delivery work belongs to parent/root: combined-tree assessment, platform/ownership requirements, evidence acceptance, guarded integration and target verification. This report acquires no write slot and records no merge.
