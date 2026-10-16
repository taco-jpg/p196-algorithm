# PR109 independent integration review

**Verdict: ACCEPT_EXACT_SOURCE_CLOSURE** for `18a82d9b5a2bd326751621e3e7a5458117561da7`. No blocking semantic, mathematical-source or evidence-integrity defect was found. The new complete 11-module trust-zero replay passed: 1,456 theorem constants, 182 safe definitions, and all 11 named exports; the two new modules account for 19 theorem constants and five safe definitions. The authored audit support module also passed against the newly rebuilt closure. The permitted transitive axiom union is exactly `Classical.choice`, `Quot.sound`, and `propext`. Current-main integration remains the parent reviewer's separate gate.

Reviewer: **Agent #12 /root/review109**, a genuinely separate reviewing agent from the original Agent #9 author and the parent integrator. This is an independent agent review and fresh execution, not a claim of a separate GitHub account or external human peer review. No accepted mathematical source was edited. Remote operations were read-only.

## Exact review scope

The acceptance target is PR109 head `18a82d9b5a2bd326751621e3e7a5458117561da7`, with parent and merge base `ae8bbdfd2a18e8910eebc25fd2a81661c01abc16`. The entire PR diff adds 20 files under `proofs/contributions/agent-9/escape-factorial-bound-20261016/`; it does not change inherited mathematics or unrelated paths. The complete binary-capable diff and changed-path list are retained under `setup/`.

I read the repository `AGENTS.md` and `proofs/PUBLICATION_POLICY.md`, the complete new proof sources and audit module, both verification drivers, the source registry, the contract, provenance, publication and checkpoint records, the full retained manuscript, and the previous independent review. I checked the inherited definitions and transport proofs used by the endpoints: ordinary decimal reversal, the total orbit, ordinary digit sum, exact finite support, the profile recurrence and uniform escape theorem, the numeric mass bridge, and time translation. All eleven mathematical modules were subsequently rebuilt from their exact source bytes and audited exhaustively. The source of this review's compiler evidence is the new run, not the previous report.

The nine inherited module blobs match the original historical paths at `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`, the PR base, the PR head, and the initially supplied main `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5`. `source-provenance-checks.json` and the replay command logs record these identities. The parent integrator owns validation of a later current-main combination; this review does not claim to have rebuilt that combination.

## Generic recurrence and factorial

`P196.Agent9.FactorialEscape.factorial` is ordinary natural factorial, defined by `factorial 0 = 1` and `factorial (m + 1) = (m + 1) * factorial m`. Its recursion does not depend on the sequence or on the desired inequality.

The generic theorem has exactly these hypotheses:

```lean
(κ : Nat) (hκ : 0 < κ)
(E : Nat → Nat) (h1 : E 1 = 1)
(hrec : ∀ i, E (i + 2) =
  κ * ((i + 2) + (i + 1) * (2 * E (i + 1) + 1)))
(M : Nat) (hM : 1 ≤ M)
```

Its conclusion is:

```lean
E M ≤ (4 * κ) ^ (M - 1) * factorial M
```

At `M=i+2`, the recurrence is algebraically the manuscript recurrence `κ * (2*(M-1)*E(M-1)+2*M-1)` for `M≥2`. The formal shift avoids applying truncated natural subtraction outside its intended positive domain. The source manuscript is section 5, equation (9), blob `7103ee939d82740b970dd23fb91e9db50db4ea54`, SHA256 `15e07772d87cc4ee469541f4fb39ce1d0dce28ac5f630b16980c8abb02db258f`; I compared the exact original Git blob with the retained source bytes.

The shifted induction proves the statement for `E (i+1)`. At `i=0`, the bound is exactly `1`, matching `E 1 = 1`. For the successor step, let `C=(4*κ)^i * factorial(i+1)`. Positivity of `κ` and factorial gives `C≥1`. Monotonicity of multiplication and addition permits replacing `E(i+1)` by `C`. The helper proves

```text
(i+2) + (i+1)*(2*C+1) ≤ 4*(i+2)*C.
```

Indeed `i+2 ≤ (i+2)*C` and `2*C+1 ≤ 3*C`; the resulting coefficient is `4*i+5 ≤ 4*i+8`. Multiplication by `κ` and the ordinary power and factorial recursions produce the next desired bound. This uses no extra monotonicity or lower-bound assumption on `E` and no dynamical assumption.

The final wrapper excludes `M=0` and converts `(i+1)-1` to `i` only in the positive case. `E 0` remains unconstrained. This restriction is necessary for the stated hypotheses: they would permit an arbitrary value of `E 0`, so extending the generic conclusion to zero without another premise would be invalid. No such extension occurs.

## Concrete decimal recurrence and zero cases

The inherited `DecimalProfile.sharpEscapeBound` is defined by `E 0 = 0`, `E 1 = 1`, and the exact recurrence with multiplier `5`. The new proof supplies the recurrence by definitional equality and instantiates the generic theorem at `κ=5`, giving `4*κ=20`.

`sharpEscapeBound_factorial` legitimately adds `M=0` using the concrete zero equation in a separate branch. Natural subtraction gives `0-1=0`, so the right side is `20^0 * 0! = 1`, and the claim is `0≤1`. The arbitrary generic sequence is never used at zero.

The inherited `DecimalUniformEscape.sharpDigitSumEscapeBound B` is definitionally `DecimalProfile.sharpEscapeBound (2*B)`. Therefore the new comparison is exactly

```lean
DecimalUniformEscape.sharpDigitSumEscapeBound B ≤
  20 ^ (2 * B - 1) * factorial (2 * B)
```

for every natural `B`. In particular `B=0` yields the coarse horizon `1`, while the original exact horizon is `0`. The package accurately documents this distinction and does not claim that the extra step is needed. The estimates are upper bounds and have no optimality claim.

## Ordinary numeric orbit and inclusive windows

The inherited `Lychrel196.reverse10` is connected to decimal digit reversal through its structurally recursive implementation and correctness proof. `Lychrel196.step n = n + reverse10 n`, `orbit n 0 = n`, and `orbit n (k+1) = step (orbit n k)`. The orbit is total and continues after a palindrome. `DecimalMass.digitSum` recursively sums `n % 10` and the digit sum of `n / 10`, with zero value at zero.

The profile embedding preserves ordinary decimal arithmetic: `mass_numeric_iter` proves the profile mass equals `2 * digitSum (orbit n t)`. The exact escape theorem applies to every positive integer, with no initial digit-sum ceiling, width bound, or initial zero-gap hypothesis. Its time-window version uses positivity of the state at time `s` and `orbit_add` to translate the resulting time.

The new endpoint preserves the original witness `t`, lower bound and strict digit-sum inequality. It only enlarges the upper endpoint using the proved horizon comparison. The exact conclusion is:

```lean
∃ t, s ≤ t ∧ t ≤ s + 20 ^ (2 * B - 1) * factorial (2 * B) ∧
  B < DecimalMass.digitSum (Lychrel196.orbit n t)
```

Its hypotheses are `n : Nat`, `0 < n`, and arbitrary natural `B,s`, including `B=0` and `s=0`. The interval is inclusive on both ends; its number of integer positions is the displayed horizon plus one. There is no endpoint off-by-one error. At `B=0`, the inherited witness can already be `s` because every positive state has positive digit sum.

The 196 endpoint only discharges the positive-seed hypothesis at `196`. Neither endpoint proves palindrome avoidance, the 196 conjecture, decimal Lychrel existence, pointwise digit-sum divergence, an infinite safe family, or an optimal escape time. The generic result is conditional algebra, while the concrete decimal window has no unproved orbit premise beyond its explicitly stated positive seed. The manuscript contains broader written claims and historical discussion; their preservation does not turn them into new formal claims of this package.

## Verification design and trust boundary

The selected reviewer driver is `review/runtime-audit/verify.py`, with the adjacent `source-registry.json`, both retained under `inputs/package/`. I inspected them before running them. They validate exact SHA256 and Git-blob identities, original dependency provenance, the full registered import closure, and a comment/string-aware forbidden-token scan. They create a previously absent output directory and copy only source bytes. The fresh private `LEAN_PATH` contains no preexisting project `.olean` files.

Every mathematical compile and the generated audit uses the literal flags `--trust=0 -j1 -DElab.async=false`. The audit enumerates declarations by originating module, rather than by public-name prefixes, and checks every theorem and safe definition/opaque declaration, including private and generated constants. It rejects custom safe project axioms and any transitive axiom outside `propext`, `Classical.choice`, and `Quot.sound`. All expected module origins must be encountered. Unsafe implementation constants are reported separately; their presence is not accepted as a theorem or safe-definition proof dependency.

The installed runtime reports official Lean `4.19.0`, release commit `6caaee842e94`; its executable SHA256 is `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`, matching the original author record. The installation provenance record identifies the official GitHub release download. The driver hashes the executable, root runtime objects and shared libraries before and after the run. The historical release archive has already been removed, so an attempted fresh archive rehash failed and is recorded. No fresh archive checksum verification, independent upstream checksum, or source rebuild of Lean and its standard library is claimed. Existing project objects from the author or earlier reviewer are never reused.

## Evidence integrity and historical outcomes

I safely unpacked the evidence archive into a separate directory, first rejecting absolute paths, parent traversal, duplicate names, links and nonregular members. All 146 original file paths, sizes and SHA256 values match the evidence manifest. The compressed archive is 116,912 bytes with SHA256 `b2f05e0e8c027a25e5336fc617c7853e837300bd8b3e2627d53351baf903fc09`. The uncompressed tar hash and byte count also match. All 17 directly tracked duplicates outside the evidence directory match the archive byte for byte. All 65 author manifest entries, the reviewer manifest and the retained reviewer evidence-file manifest verify.

The author `generic-001` run remains **FAILED**. Its compiler rejected a distributivity equality, and its raw axiom reports contain `sorryAx` from error recovery. Those bytes are preserved and are not part of this accepted source chain. `generic-002`, the completed author closure build, and the historical independent closure replay are separately recorded as successful. The author full-build summary originally captured only the first line of a wrapped module-origin list; a separately retained reporting-only supplement records all eleven origins and preserves the original summary and driver. Its correction did not alter mathematical source or silently relabel a failed compiler run.

The current checkpoint's old "independent review and publication pending" wording is explicitly historical; `PUBLICATION.md` supplies the later status. The historical author's active contract and prior reviewer's recorded checkout HEAD are likewise provenance records, not assertions of this review's head or result.

This review retains its own initial ordinary-sandbox Lean startup failure and public-Git proxy failure, the unavailable archive check, the later successful authorized environment, and every fresh Lean command/log. No unsuccessful source attempt is concealed. Final machine results and the exact acceptance verdict are in `REVIEW_RECEIPT.json`; the raw compiler record is `fresh-replay/verification.json`.
