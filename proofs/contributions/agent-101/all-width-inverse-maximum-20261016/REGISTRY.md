# All-width inverse maximum: pinned registry and reproduction

This packet registers the exact 17-module source closure of
`Agent101AllWidthMaximum` under project `agent101-all-width-maximum`. Its four new modules
contain **36 public theorems and 5 public definitions (41 declarations)**.
`PUBLIC_EXPORTS.json` records every fully qualified name, declaration head,
source line, explicit `#print axioms` line, source hash, and Git blob identity.
All 41 names are also claim endpoints in the original verifier's registry.

## Mathematical scope

`Agent101.Maximum.all_width_inverse_maximum` states that for every natural
`D` with `2 ≤ D`, every `D`-digit ordinary-integer target `Y`, and every
duplicate-free finite list `ns` of positive integers satisfying `step n = Y`,
the length of `ns` is at most `9 * 10 ^ (D / 2 - 1)`. Here natural-number
division gives the integer part. The same theorem supplies a target and a
duplicate-free list whose membership is **equivalent** to
`0 < n ∧ step n = Y`, and whose length equals this bound. Thus the witness
list contains every positive predecessor, across all decimal widths.

`Agent101.Maximum.one_digit_inverse_maximum` supplies the separate sharp
bound one for one-digit targets and the complete attaining fiber `Y = 2`,
`ns = [1]`. The width predicate used by these theorems is the existing
`Agent101.decimalWidth`; it requires a positive width and the usual powers
of ten bounds. The statements count positive predecessors. They do not
assert any infinite-orbit result or a maximum for a zero-digit target.

For `D ≥ 2`, the explicit witness uses half-coefficients all equal to nine;
even width has no center, and odd width has center zero. The unchanged
Agent105 collision theorem excludes other input widths because such a
collision forces target units digit one, whereas the witness target has
units digit nine. The upper bound uses the original cross-width exterior
coefficients eleven and one, giving outer multiplicities eight and one,
together with exact fixed-profile counts. The corrected width bound calls
the original `P196.Agent2.OverflowFibers.nodup_subset_length_le` directly.

## Source closure and attribution

The seven records from `proofs/Agent101Nonpalindromic.registry.json` are retained unchanged. They
include the palindrome and nonpalindrome modules because the root reuses
`Agent101.length_filter_partition`. The original Research foundation is
used directly; this closure needs no embedded-foundation adapter.

The two Agent105 files are unchanged original sources from commit
`5923015f86eb1ef898becd77ce2ee328ff338b69`. Their source record is
`proofs/contributions/agent-101/all-width-max-scout-20261016/source-provenance.json`. The original Agent2 overflow bound, actual, and
local files are stored byte-for-byte in `bounds/dependencies/agent2/`, with
their original paths, Git blobs, and commit `58afcada8047e015b8f4233b96c44c7c5b9c4162` in
`bounds/dependencies/agent2/PROVENANCE.json`. Its fourth entry pins the
unchanged repository `PeriodObstructions` source. Registry paths select
these exact files, independently of any unrelated same-name file.

| New module | Theorems | Definitions | Accepted source SHA256 |
|---|---:|---:|---|
| `Agent101ProfileExtraction` | 7 | 0 | `fff6917b100aeec40e353abe4a3f8d27f6561d6859a1feeac9135c22cd8c836b` |
| `Agent101WidthFiberBounds` | 6 | 0 | `bebc285185d2f15138980dc2720b31fb0cbf476d9a30b1155545aca0c96a1bb2` |
| `Agent101MaximumWitnesses` | 15 | 5 | `d915b9df4e9ef3ab92ae9a33c3edd655b8567c40af7b88026e067408303182b7` |
| `Agent101AllWidthMaximum` | 8 | 0 | `9bbdc9351ccb72d2502ca303a7963c1b2aa1e50afd0e9f5d3d095305b34983d9` |

The actual root-reachable build order and complete source pins are:

| Logical module | Repository-relative path | SHA256 |
|---|---|---|
| `Lychrel196Research` | `proofs/Lychrel196Research__c696e0ea3db39d92.lean` | `f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c` |
| `Agent101DigitPairs` | `proofs/Agent101DigitPairs.lean` | `5c76eae97efd2f30d1775650f7feca477c269419af1c02809800a95ca62821f8` |
| `Agent101MultiplicityBounds` | `proofs/Agent101MultiplicityBounds.lean` | `8fd487ce8025cfe7cbda3dc51b6a02595c856fbe3dd065a8781cea60b7e6b5c3` |
| `Agent101SplitEnumeration` | `proofs/Agent101SplitEnumeration.lean` | `8ce57c88984df3a965e33c181f4d8f138258fe48b14e2b835333fe6c30d79684` |
| `Agent101NumericFibers` | `proofs/Agent101NumericFibers.lean` | `bba80a597345f7f3bd207698a6e6b338ee20335e647f518604fa43654b13fd97` |
| `Agent105WidthSupport9df76b` | `proofs/Agent105WidthSupport9df76b.lean` | `3411c212f4c7c05d1d91cc7249f1d6520f9da1202da6721ca9b1764944ff3da7` |
| `Agent105CrossWidth9df76b` | `proofs/Agent105CrossWidth9df76b.lean` | `a8fe89a91d79809bb3452a39775eb0cc9a06241d37e37c7ef916bf20f265d7a2` |
| `Agent101PalindromeFibers` | `proofs/Agent101PalindromeFibers.lean` | `27ebcd2a7b790d87e45f19e51d0d7e2ff977f297742936503b9552026e3ea633` |
| `Agent101NonpalindromicFibers` | `proofs/Agent101NonpalindromicFibers.lean` | `22e33259394d275175a02a90a887e3fa49af488a3931e3518fc99899a59154e5` |
| `Agent101ProfileExtraction` | `proofs/Agent101ProfileExtraction.lean` | `fff6917b100aeec40e353abe4a3f8d27f6561d6859a1feeac9135c22cd8c836b` |
| `PeriodObstructions` | `proofs/PeriodObstructions__70ce034b31b5b218.lean` | `83102a949036799a929ba72d74ce9d76bc2a11cb3adf61e0bc06b6013b22991a` |
| `Agent2OverflowActual` | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/dependencies/agent2/Agent2OverflowActual.lean` | `ae8776a396c90286e303c16210fd036ab405c461796be48e5f384ff958fd5dc1` |
| `Agent2OverflowLocal` | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/dependencies/agent2/Agent2OverflowLocal.lean` | `5fc0ef519aeb5a8f56d6a1aecfbcdd445ab85397f3cc31d3e0d8572425fb3f7d` |
| `Agent2OverflowBound` | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/dependencies/agent2/Agent2OverflowBound.lean` | `d0d602d806e430babef7350d7c4ccfdb2ccd0c44f34cd700c2e18ec2a851c6be` |
| `Agent101WidthFiberBounds` | `proofs/Agent101WidthFiberBounds.lean` | `bebc285185d2f15138980dc2720b31fb0cbf476d9a30b1155545aca0c96a1bb2` |
| `Agent101MaximumWitnesses` | `proofs/Agent101MaximumWitnesses.lean` | `d915b9df4e9ef3ab92ae9a33c3edd655b8567c40af7b88026e067408303182b7` |
| `Agent101AllWidthMaximum` | `proofs/Agent101AllWidthMaximum.lean` | `9bbdc9351ccb72d2502ca303a7963c1b2aa1e50afd0e9f5d3d095305b34983d9` |

Only `propext`, `Classical.choice`, and `Quot.sound` are allowed axioms.
The registry sets `catalogue_complete` to false and names this one project;
it makes no repository-wide catalogue or verification claim. Original
dependency authorship remains with the source modules listed above.

## Metadata pins

| Artifact | SHA256 |
|---|---|
| `proofs/Agent101AllWidthMaximum.registry.json` | `496908a7d53c6a09b7a82dfae3c5e10339ef699072e5c97c0e591dc4e2c2cfcc` |
| `PUBLIC_EXPORTS.json` | `f1e1558d29033c7259e762680e62a03080f1bfd52f2d057eed5bd2115a9c0b8a` |
| `make_registry.py` | `c13fa6c0a3bd6225354d643a1bdadfe282c9e07f2de129300ec0e41fbc22f4a8` |
| Original verifier | `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a` |
| Original seven-module registry | `dd4d34166a289a7b701acb5dec846ad66ebcd680f01a697e148923a336315c49` |
| Agent2 provenance | `19ab76d17f521e2e53dee1c9d95e5305cf56d2ae0099bfc74b9a666d38cbec9a` |
| Agent105 provenance | `913c98039a3100d4d3cdcf53adc88f1a7859e6e2539e56d5cfc905b893cfcd5f` |
| Lean executable, version 4.19.0 / commit 6caaee842e94 | `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023` |

`make_registry.py` uses Python's standard library, reads the unchanged
original verifier's comment/string masker, checks every source SHA256 and
Git blob, validates the exact import closure, scans the complete selected
source code for forbidden proof shortcuts, and checks all 41 declarations
against a fixed inventory. It creates this metadata deterministically and
refuses to overwrite different existing generated files. Its output
includes metadata hashes, including this document's hash. It never invokes
Lean, fetches dependencies, or modifies Git.

```bash
python3 proofs/contributions/agent-101/all-width-inverse-maximum-20261016/make_registry.py --check
```

The result is a **metadata/source identity check**, not a mathematical
proof check. This preparation task did not start a new full Lean build.
Previous author attempts and their raw logs remain in `profile/`,
`bounds/`, `witnesses/`, and `upper/`; they are separate evidence and are
not substituted for the final canonical reproduction.

## Publication checkpoint and canonical reproduction

These metadata pin exact source bytes; they deliberately do not invent a
future publication commit. After the integration writer publishes the
sources, dependency originals, registry, and metadata, use that **full
40-character Git commit** for `AGENT101_COMMIT` below. The first command
requires every selected source and metadata file, the unchanged verifier,
the inherited registry, and both provenance records to exist at that
commit with exactly the current bytes. The check reads Git objects and
does not alter the checkout. If the object is absent, fetch that exact
commit before checking it.

The original verifier records the checkout's `HEAD` as `source_commit`;
its `source_tree_clean` field checks tracked files only. Those fields alone
do not establish publication of newly created files. The explicit Git
object check below supplies that missing identity check. Run the canonical
verifier in a checkout at `AGENT101_COMMIT` so its recorded `HEAD` also
identifies the reviewed publication. Record the commit and the output of
the metadata check alongside the final verification result.

From the repository root, with the published commit substituted:

```bash
AGENT101_COMMIT=REPLACE_WITH_FULL_PUBLISHED_COMMIT
AGENT101_PACKET=proofs/contributions/agent-101/all-width-inverse-maximum-20261016
AGENT101_LEAN=/workspace/scratch/2a8a87fd78df/agent101-runtime/toolchain/lean-4.19.0-linux/bin/lean
AGENT101_BUILD=/workspace/scratch/2a8a87fd78df/agent101-all-width-canonical-review-01

python3 "$AGENT101_PACKET/make_registry.py" --check --check-published-commit "$AGENT101_COMMIT"
python3 proofs/verify_project__214bf7673efe116b.py \
  --lean "$AGENT101_LEAN" \
  --output "$AGENT101_BUILD" \
  --project agent101-all-width-maximum \
  --registry proofs/Agent101AllWidthMaximum.registry.json
```

Choose a previously unused output path; the original verifier rejects an
existing output directory. This is the one fresh complete 17-module build
to be performed by the independent reviewer after publication. The
unchanged verifier first checks source identity and imports, copies all
sources under their logical module names, compiles in dependency order,
checks all 41 public endpoints, and audits every theorem whose origin is
one of the 17 modules, including transitive dependencies. Each source's
explicit `#print axioms` output is retained in its compiler log, including
the five new definitions. The report preserves all command arguments,
exit codes, elapsed times, and log hashes.

The original verifier's compile command does not itself add `--trust=0`.
After that canonical run succeeds, recheck its generated full module audit
with the explicit flag and retain the separate raw log:

```bash
(
  set -o noclobber
  cd "$AGENT101_BUILD/agent101-all-width-maximum/source"
  LEAN_PATH="$PWD" "$AGENT101_LEAN" --trust=0 -j1 -DElab.async=false \
    ProjectAudit.lean > ../logs/ProjectAudit-trust0.log 2>&1
)
```

The reviewer must record the actual exit status and log hash, and confirm
the audit's complete theorem count and allowed axiom union. Preserve any
failed build and its command/log/source snapshot; use a new output path
for any justified retry. A published-commit identity check, a canonical
Lean `PASS`, and the explicit trust-zero audit are three distinct results;
none is inferred merely from this registry's existence.
