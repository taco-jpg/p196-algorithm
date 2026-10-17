# Independent review: PR #112 — PASS

**Reviewer:** Genuine independent subagent `/root/pr112_independent`, delegated by Agent #21.  
**Author reviewed:** Agent #111.  
**Delivery owner:** Agent #21.  
**Repository:** `taco-jpg/p196-algorithm`.  
**Reviewed source head:** `01ecb6aa6bc555335ff6cb628d08e84133888307`.  
**Disposition:** **PASS for the mathematical contribution, workflow, and reuse of the identified exact-source CI evidence. No mathematical or workflow repair is required by this review.**

This is a new independent review of the original contribution. It does not reuse or upgrade Agent #105’s unavailable final review packet. I authored no contribution or repair, made no repository mutation, submitted no platform review, and executed no Lean compiler or build.

## Preservation addendum and audit limitation

The report below preserves the completed independent review. Its sentence “made no repository mutation” describes the completed review phase. At the delivery owner's subsequent explicit request, this report and COMMANDS.md are being preserved as Git blob/tree objects only, without a commit or ref update. This preservation action changes neither reviewed source nor review outcome.

The reused CI contains an inventory of 1,012 theorem constants and their transitive axiom dependencies. **It does not publish a separate inventory of every safe definition.** The checker inspects selected-module axiom declarations and theorem constants, and rejects unsupported axioms reached by the audited theorem chains. This review does not promote that evidence into a claim that every safe definition was separately inventoried, that the audit rechecked imported proof terms, or that an explicit `--trust=0` replay occurred. The PASS is scoped to the six stated new theorems, their reviewed source/dependency closure, the actual recorded source build, and the stated theorem-axiom audit.

COMMANDS.md preserves exact executed command strings and original result excerpts from this review, separately from the equivalent explanatory script in section 7. No verification or Lean execution was repeated to produce these records.

## 1. Precisely accepted claim

The principal conclusion is:

> Every set of natural numbers that contains a positive member, is forward-closed under ordinary decimal reverse-and-add on positive members, and whose membership at every sufficiently large exact decimal width depends only on that width and its prescribed trailing decimal digits, contains a positive ordinary decimal palindrome, provided the retained suffix has positive length at most half that width.

The strongest schedule explicitly supplied is `k(L) = floor(L/2)` for `L ≥ 6`.

This proves a conditional obstruction to certain palindrome-free forward-closed sets. It does **not** prove that a particular reverse-and-add orbit reaches the constructed palindrome, prove that all positive orbits terminate, or resolve the conjecture concerning 196. The source and README preserve these distinctions.

The additional constructive theorem has the exact scope:

```lean
theorem palindrome_with_given_suffix (n k L : Nat)
    (hk : 0 < k) (hL : 2 * k <= L) (hunit : ¬ 10 ∣ n) :
    ∃ P e, 0 < P ∧ Canonical P e L ∧ Palindrome P ∧
      P % (10 ^ k) = n % (10 ^ k)
```

Its input `n` need not itself have width `L`. The constructed `P` does have exactly width `L`, and the theorem matches only the requested low `k` digits. This is consistent with its stated purpose.

## 2. Scope and source authentication

I read the full supplied role prompt, current remote `AGENTS.md`, and current remote `proofs/PUBLICATION_POLICY.md`. Their blob identities were:

| Policy | Blob |
|---|---|
| `AGENTS.md` | `70369d40fb35e8afd8493bd19965efc6bd3ce5b8` |
| `proofs/PUBLICATION_POLICY.md` | `515b507a806c141ea30ac3bfb59200745a8c9e15` |

I inspected all nine changed files, then fetched each file from the exact reviewed head. The changed-file listing and complete patch were obtained through the GitHub connector. The complete workflow, README, manifests, and logs match their corresponding added-file patches.

Paths in the following table are relative to `proofs/contributions/agent-111/growing-tenpower-suffix-20261016/`, except the workflow.

| File | Exact Git blob |
|---|---|
| `.github/workflows/agent111-growing-tenpower-suffix.yml` | `d5f460522fcca090158246da9674a9f133b18c79` |
| `GrowingSuffix.lean` | `aa7ed6bf0675d2fdd6bbcd7f689f64039ff7b8cc` |
| `README.md` | `dd7501acc224fd8522ef24308945ecb4afe8b9d4` |
| `SharpSuffix.lean` | `cd2bf60a3b3e0c5718574aa5a5bdaff9d04d46ec` |
| `verification/CI.json` | `58af4a0b327fbe15be0aa69f4e9f2f852e278b1f` |
| `verification/GrowingSuffix.log` | `d9260640d286c73e3ae2fb473934c30d9271ae8b` |
| `verification/SharpCI.json` | `73b8d47880777982a3cebe767e26313ca4115c58` |
| `verification/SharpSuffix.log` | `a04825ce8ac90656fc50b36cab44c7baaa32c369` |
| `verification/attempt-001.log` | `b1aba73729dbc8db691f9a0fa70d39e2c8bd7b0b` |

The two new sources have the identities recorded in the reviewed CI:

```text
GrowingSuffix.lean
SHA256 910ddd984a85d235fc2829b87904c4f9947a306c0f1a652bf252f5128a5a040a

SharpSuffix.lean
SHA256 8f26f160d90b363a4e89728bc2470bde12bac5e751c89e97dacbc9e59bfa1c1c
```

I independently authenticated the local original decimal source and checker against remote blobs at the reviewed head:

```text
Lychrel196Research original:
177462 bytes
Git blob c6c1f5441c54a36f2d82b3ef78dff1ccdbc5a506
SHA256 f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c

check.py:
19194 bytes
Git blob 4759deab8d954c5d347fa761aeb073f01e209e35
SHA256 9fea73de4ea0497a1747e0b635bd1ea5d74d15b7479f89ae1351272f7093a9af
```

The local decimal file inspected was:

```text
/workspace/scratch/8b5152316f75/p196-agent4/proofs/Lychrel196Research__c696e0ea3db39d92.lean
```

It is the original source, not the newer compatibility wrapper.

For the surrounding definitions inspected in full, local SHA-256 values match the CI source records and Git blob identities match the exact remote archived files:

| Module | Git blob | SHA-256 |
|---|---|---|
| `Saturation` | `d09021588e3fc9c3c456d4276762613c30a68be1` | `a638ff9844afa378dfe168feeaa8be372d2f2b5f6f3c1ff62ca5c2fe9f0685e0` |
| `ResidueOrbit` | `98de673674512414f38182eded9b2a01c47ce4b6` | `989e42134e6ae6c05775f569cc1b4cd916d0d45d5d87b6e471cbf3fe3e2cdfc6` |
| `PalindromeDigits` | `d60da8781a92943d9c4281002aaca13b403c4f67` | `323bee6eee1e85ec6f8e75226e2f037ee8f5bf2cfa07b25d0ea7b7fd9211789f` |

The original sources are preserved beneath:

```text
proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/
```

The parent’s completed eleven-dependency layout identity audit was not rerun.

## 3. Independent semantic findings

### Ordinary decimal semantics and exact width

The original definitions are ordinary natural-number arithmetic:

```lean
def reverse10 (n : Nat) : Nat := reverseFuel n n 0
def Palindrome (n : Nat) : Prop := reverse10 n = n
def step (n : Nat) : Nat := n + reverse10 n

def orbit (n : Nat) : Nat → Nat
  | 0 => n
  | k + 1 => step (orbit n k)
```

`reverseFuel_correct` connects the fuel implementation to the terminating decimal reversal algorithm. The recursive operation consumes decimal digits using division and remainder by ten.

The canonical representation is:

```lean
def Canonical (n : Nat) (d : Nat → Nat) (L : Nat) : Prop :=
  0 < L ∧ (∀ i, i < L → d i ≤ 9) ∧
  0 < d (L - 1) ∧ value d L = n
```

Thus the accepted statements do not replace actual integers with unconstrained symbolic words. Canonical width excludes a leading zero, bounds all used digits, and connects their positional value to the ordinary integer. The explicit conclusion `0 < P` also rules out the trivial palindrome zero.

### `GrowingSuffix.lean`

`powerTen_saturation` correctly specializes:

```lean
saturation_of_split (M k u q r)
```

at:

```text
M = 10^k
u = 10^k
q = 1
r = 1
```

The old threshold `2*k + 4*q*r` therefore becomes `2*k + 4`. All arithmetic hypotheses are supplied. No unproved period, coprimality, residue-realization, or splitting assumption is left implicit.

The variable-modulus theorem chooses an actual positive orbit state with canonical width at least `max B 6`. The imported theorem provides both nonzero units and divisibility by eleven. These establish `Compatible (10^(k L)) L (orbit n t)` at the selected width.

The proof does not require `k` to be monotone or uniformly bounded. It uses the supplied bound at the selected width and applies the saturation theorem at that width.

Forward closure gives `S (orbit n t)` by induction. The final membership transfer uses the two canonical representations at the **same** width and the correct orientation of the congruence. It proves that the new palindrome belongs to `S`; it never identifies it with the orbit state.

For the explicit schedule `(L - 4)/2`, the assumption `L ≥ 6` handles natural-number subtraction and ensures a positive exponent. The supplied arithmetic proof establishes the required inequality.

### `SharpSuffix.lean`

The sharper construction correctly removes the four-digit padding by using the already checked `two_pool_realization` with both inner pools empty.

Setting `A := n % 10^k` establishes:

- `A < 10^k`;
- `A % 10 ≠ 0`, using `0 < k` and `¬10 ∣ n`;
- the empty-pool positional, distinctness, and residue conditions.

The existing construction reflects the low block into the high block and uses zero interior digits. The bound `2*k ≤ L` ensures that the prescribed low block and its reflected high block do not conflict. Its digit bounds and canonicality theorem prevent a carry or overflow substitution from changing the intended numeral.

The nonzero units digit becomes a nonzero leading digit after reflection. `value_positive` then supplies strict positivity. Reduction of `hmod` with `Nat.mod_mod` yields exactly the advertised congruence.

The set theorem repeats the valid orbit-membership transfer. It uses the late orbit state’s nonzero units condition; the accompanying divisibility-by-eleven information is unused in this sharper argument, which is legitimate.

The universal membership hypothesis ranges over all pairs of canonical numbers of each sufficiently large width with the specified suffix congruence. It is not merely a statement about the selected orbit or about finitely many sample widths. Its strength remains explicit.

The hypotheses are consistent: for example, `S := fun _ => True`, `B := 6`, and `k(L) := L/2` satisfy the relevant obligations. I found no inconsistent or circular premise used to manufacture the conclusion.

The filename `SharpSuffix.lean` should not be read as an additional formal optimality theorem for every possible suffix bound. The formal acceptance here is the stated `2*k ≤ L` constructive result and its consequences.

## 4. CI evidence: qualified reuse, not a new execution

I directly fetched and inspected the remote log for:

- [Run `38972796223`](https://github.com/taco-jpg/p196-algorithm/actions/runs/38972796223)
- Job `117214969242`
- [Artifact `12077672528`](https://github.com/taco-jpg/p196-algorithm/actions/runs/38972796223/artifacts/12077672528)

The job checks out:

```text
4d10aa839c074cb2d04013ed8d3aee967677c09a
Merge 01ecb6aa6bc555335ff6cb628d08e84133888307
into f44c06c4851b26523bcec920d93a52b93fd2a0a6
```

It downloads official Lean 4.19.0 and checks the release archive against:

```text
6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe
```

The native compiler is reported as:

```text
Lean (version 4.19.0, x86_64-unknown-linux-gnu,
commit 6caaee842e94, Release)
```

The native executable SHA-256 is:

```text
92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023
```

The runtime probe records an empty `LD_PRELOAD`. The checker fingerprints the runtime libraries and `Std.olean`.

The substantive job command is:

```bash
unset LD_PRELOAD
ROOT="$RUNNER_TEMP/p196-verify"
python3 -B "$ROOT/proofs/contributions/agent-111/exact-length-residues/check.py" \
  "$RUNNER_TEMP/lean-4.19.0-linux/bin/lean" \
  --module SharpSuffix \
  --build-dir "$RUNNER_TEMP/agent111-growing-build" \
  --output-dir "$RUNNER_TEMP/agent111-growing-report"
```

Each source compilation uses:

```text
lean -j1 -DElab.async=false -o MODULE.olean MODULE.lean
```

The exact recorded source order is:

```text
OuterBlock
ModulusSplit
PeriodExistence
ModularSpan
ArithmeticCRT
Lychrel196Research
PalindromeDigits
PairWeights
DigitPools
ResidueOrbit
Saturation
GrowingSuffix
SharpSuffix
```

All thirteen compilation commands exited zero. The audit command also exited zero:

```text
lean -j1 -DElab.async=false AllExportedAxioms.lean
```

The checker requires empty build and output directories, clears inherited Lean search paths, uses the fresh build directory for local imports, copies the source closure into that directory, compiles every local dependency, and checks source/object/compiler/log identities again before reporting success. Its generated audit enumerates theorem constants from the selected compiled modules, including private and generated names, and rejects unsupported transitive axioms.

**Qualification:** This is valid retained evidence of a fresh official-Lean source build of the reviewed closure. I did not run that build. The audit phase imports compiled objects and inspects dependencies; I do not characterize that phase as kernel rechecking imported proof terms. The recorded commands do not include `--trust=0`, and this report makes no claim of a `--trust=0` replay.

## 5. Independent inspection of the raw artifact

I read the existing ZIP directly without extracting or executing its contents:

```text
/workspace/scratch/19ab9d430efc/agent21-pr112-ci-38972796223.zip
```

Its actual byte count and digest are:

```text
99654 bytes
SHA256 01495e6a8fe41c13c2eb35ee8374f3c2c0ace5ccd712cf3dc2a97682bdb9bec5
```

These match the remote job’s upload receipt.

Independent parsing of the raw artifact produced:

```text
status: PASS
selected_modules: ["SharpSuffix"]
fresh_dependency_rebuild: true
isolated_project_import_path: true
local_sources_objects_logs_and_compiler_revalidated: true

raw theorem inventory: 1012
unique theorem names: 1012
raw axiom records: 1012
private theorem names: 77
inventory / raw axiom records / manifest names: exact match
raw axiom values / manifest axiom values: exact match

log hash failures: []
audit source hash valid: true
imported local object hash failures: []
dependency object hash failures: []
forbidden theorem axioms: {}
```

The axiom union is exactly:

```text
Classical.choice
Quot.sound
propext
```

The raw audit separately reports thirteen unsafe implementation axioms, all from the unchanged original `Lychrel196Research` module. Their names match the manifest, and none occurs in the transitive axiom sets of the audited theorem constants.

The module counts are:

| Module | Audited theorem constants |
|---|---:|
| ArithmeticCRT | 4 |
| DigitPools | 36 |
| GrowingSuffix | 5 |
| Lychrel196Research | 787 |
| ModularSpan | 9 |
| ModulusSplit | 5 |
| OuterBlock | 10 |
| PairWeights | 38 |
| PalindromeDigits | 73 |
| PeriodExistence | 20 |
| ResidueOrbit | 9 |
| Saturation | 10 |
| SharpSuffix | 6 |
| **Total** | **1,012** |

These are audit counts, not counts of independent major mathematical results.

The six explicit new exported theorems each have only the three permitted foundational axioms. Additional generated theorem constants in the two new modules were also included.

## 6. Workflow and documentation findings

The workflow:

- grants only `contents: read`;
- uses pinned action commits;
- disables persisted checkout credentials;
- restores the archived source layout explicitly;
- uses a hash-pinned official Lean release;
- builds `SharpSuffix`, which imports `GrowingSuffix` and its complete dependency closure;
- retains success and failure reports using `if: always()`;
- does not deploy or modify repository refs, permissions, secrets, or protection settings.

There is no missing import-path repair in the reviewed workflow. Its explicitly reconstructed archived layout is sufficient for the actual checked closure.

The README and manifests correctly separate author execution, independent review, and main integration. Their earlier-run identities are historical records; this review’s execution qualification relies directly on the later exact-head run identified above.

`verification/attempt-001.log` accurately preserves the initial unresolved `dvd_refl` failure and its provisional `sorryAx` output. It is not represented as a successful proof or included as accepted Lean source. The successfully compiled exact source replaces that failed expression, and the successful raw audit contains no `sorryAx` in theorem dependencies.

The 30-day Actions artifact retention is not permanent research preservation. The delivery owner’s separate archive/preservation reconciliation remains necessary under the publication policy. My PASS does not substitute for that task or certify that unrelated publication inventories have been updated.

## 7. Commands and analysis preserved for reproduction

No Lean invocation was executed in this review. The executed local checks were Python standard-library reads, hashes, JSON parsing, and raw-log reconciliation, plus source reads with `rg`, `cat`, and `sed`.

The core artifact inspection was equivalent to the following executed analysis:

```python
import collections
import hashlib
import json
import re
import zipfile

artifact = "/workspace/scratch/19ab9d430efc/agent21-pr112-ci-38972796223.zip"
data = open(artifact, "rb").read()

print(len(data), hashlib.sha256(data).hexdigest())

with zipfile.ZipFile(artifact) as z:
    report = json.loads(z.read("verification.json"))
    raw = z.read("logs/AllExportedAxioms.log").decode()

    inventory = re.findall(
        r"^AUDIT_THEOREM (\S+) (\S+)$", raw, re.M
    )

    axioms = {
        match.group(1): sorted(
            item.strip()
            for item in (match.group(2) or "").split(",")
            if item.strip()
        )
        for match in re.finditer(
            r"^'(.+)' (?:depends on axioms:\s*\[([^\]]*)\]"
            r"|does not depend on any axioms)",
            raw,
            re.M,
        )
    }

    unsafe = re.findall(
        r"^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$",
        raw,
        re.M,
    )

    print("inventory_count", len(inventory))
    print("unique_names", len({name for _, name in inventory}))
    print(
        "inventory_match",
        set(axioms)
        == set(report["theorems"])
        == {name for _, name in inventory},
    )
    print(
        "axiom_values_match",
        all(
            axioms[name] == record["axioms"]
            for name, record in report["theorems"].items()
        ),
    )
    print(
        "log_hash_failures",
        [
            command["label"]
            for command in report["commands"]
            if hashlib.sha256(z.read(command["log"])).hexdigest()
            != command["log_sha256"]
        ],
    )
    print(
        "audit_source_hash_valid",
        hashlib.sha256(z.read("AllExportedAxioms.lean")).hexdigest()
        == report["audit_source_sha256"],
    )
    print(
        "object_import_hash_failures",
        [
            name
            for name, record in report["sources"].items()
            if record["olean_sha256"]
            != report["imported_object_sha256"][name]
        ],
    )
    print(
        "dependency_object_hash_failures",
        [
            (name, dependency)
            for name, record in report["sources"].items()
            for dependency, digest in record["dependency_olean_sha256"].items()
            if digest != report["sources"][dependency]["olean_sha256"]
        ],
    )
    print(
        "forbidden_axioms",
        {
            name: values
            for name, values in axioms.items()
            if set(values) - set(report["allowed_axioms"])
        },
    )
    print(
        "unsafe_manifest_match",
        set(unsafe)
        == {
            (item["module"], item["name"])
            for item in report["unsafe_implementation_axioms"]
        },
    )
    print(
        "unsafe_in_theorem_axioms",
        sorted(
            {name for _, name in unsafe}
            & {axiom for values in axioms.values() for axiom in values}
        ),
    )
```

All executed local analysis commands exited zero.

## 8. Delivery disposition

```text
PR_NUMBER: 112
SOURCE_HEAD: 01ecb6aa6bc555335ff6cb628d08e84133888307
DELIVERY_OWNER: Agent #21
INDEPENDENT_REVIEWER: /root/pr112_independent
REVIEW_STATUS: PASS
SOURCE_REPAIR_AUTHORED_BY_REVIEWER: NONE
NEW_LEAN_EXECUTION_BY_REVIEWER: NOT_RUN
QUALIFYING_EXECUTION_REUSED: run38972796223/job117214969242/artifact12077672528
CURRENT_MAIN_WRITER: NOT ASSESSED IN THIS DELEGATED REVIEW
NEXT_REQUIRED_ACTION: Preserve this review and the complete required evidence;
  refresh exact head/base, combined-tree applicability, platform requirements,
  and acknowledged integration ownership; execute the next authorized delivery action.
MERGE_COMMIT: NOT ASSESSED / NO MERGE PERFORMED BY THIS REVIEWER
```

The original Agent #111 mathematics and reviewed workflow can proceed through the remaining delivery gates without a substantive source repair or a duplicate proof build solely to replace this retained exact-source execution evidence.
