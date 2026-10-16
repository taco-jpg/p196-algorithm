#!/usr/bin/env python3
"""Reproduce the pinned all-width maximum metadata without executing Lean.

The default creates the three generated metadata files if absent, and accepts
already-identical files. It never overwrites different existing files. --check
only compares. --check-published-commit additionally checks the bytes stored at
one exact Git commit, including source, verifier, provenance, and metadata.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[4]
PACKET = "proofs/contributions/agent-101/all-width-inverse-maximum-20261016"
SCRIPT = PACKET + "/make_registry.py"
REGISTRY = "proofs/Agent101AllWidthMaximum.registry.json"
EXPORTS = PACKET + "/PUBLIC_EXPORTS.json"
README = PACKET + "/REGISTRY.md"
PROJECT = "agent101-all-width-maximum"
TASK = "agent101-all-width-inverse-maximum-20261016"
ROOT_MODULE = "Agent101AllWidthMaximum"
ALLOWED = ["propext", "Classical.choice", "Quot.sound"]
BASE_REGISTRY = "proofs/Agent101Nonpalindromic.registry.json"
BASE_SHA256 = "dd4d34166a289a7b701acb5dec846ad66ebcd680f01a697e148923a336315c49"
VERIFIER = "proofs/verify_project__214bf7673efe116b.py"
VERIFIER_SHA256 = "c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a"
LEAN_SHA256 = "92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023"
AGENT2_PROVENANCE = PACKET + "/bounds/dependencies/agent2/PROVENANCE.json"
AGENT2_PROVENANCE_SHA256 = "19ab76d17f521e2e53dee1c9d95e5305cf56d2ae0099bfc74b9a666d38cbec9a"
AGENT105_PROVENANCE = "proofs/contributions/agent-101/all-width-max-scout-20261016/source-provenance.json"
AGENT105_PROVENANCE_SHA256 = "913c98039a3100d4d3cdcf53adc88f1a7859e6e2539e56d5cfc905b893cfcd5f"
AGENT2_COMMIT = "58afcada8047e015b8f4233b96c44c7c5b9c4162"
AGENT105_COMMIT = "5923015f86eb1ef898becd77ce2ee328ff338b69"

# The seven base records are preserved exactly from the pinned earlier registry.
# These ten records complete the actual selected root's transitive closure.
ADDED = {
    "Agent105WidthSupport9df76b": (
        "proofs/Agent105WidthSupport9df76b.lean",
        "3411c212f4c7c05d1d91cc7249f1d6520f9da1202da6721ca9b1764944ff3da7",
        ["Agent101NumericFibers"],
    ),
    "Agent105CrossWidth9df76b": (
        "proofs/Agent105CrossWidth9df76b.lean",
        "a8fe89a91d79809bb3452a39775eb0cc9a06241d37e37c7ef916bf20f265d7a2",
        ["Agent105WidthSupport9df76b"],
    ),
    "PeriodObstructions": (
        "proofs/PeriodObstructions__70ce034b31b5b218.lean",
        "83102a949036799a929ba72d74ce9d76bc2a11cb3adf61e0bc06b6013b22991a",
        ["Std"],
    ),
    "Agent2OverflowActual": (
        PACKET + "/bounds/dependencies/agent2/Agent2OverflowActual.lean",
        "ae8776a396c90286e303c16210fd036ab405c461796be48e5f384ff958fd5dc1",
        ["PeriodObstructions"],
    ),
    "Agent2OverflowLocal": (
        PACKET + "/bounds/dependencies/agent2/Agent2OverflowLocal.lean",
        "5fc0ef519aeb5a8f56d6a1aecfbcdd445ab85397f3cc31d3e0d8572425fb3f7d",
        ["Std"],
    ),
    "Agent2OverflowBound": (
        PACKET + "/bounds/dependencies/agent2/Agent2OverflowBound.lean",
        "d0d602d806e430babef7350d7c4ccfdb2ccd0c44f34cd700c2e18ec2a851c6be",
        ["Agent2OverflowActual", "Agent2OverflowLocal"],
    ),
    "Agent101ProfileExtraction": (
        "proofs/Agent101ProfileExtraction.lean",
        "fff6917b100aeec40e353abe4a3f8d27f6561d6859a1feeac9135c22cd8c836b",
        ["Agent101NumericFibers"],
    ),
    "Agent101WidthFiberBounds": (
        "proofs/Agent101WidthFiberBounds.lean",
        "bebc285185d2f15138980dc2720b31fb0cbf476d9a30b1155545aca0c96a1bb2",
        ["Agent101ProfileExtraction", "Agent2OverflowBound"],
    ),
    "Agent101MaximumWitnesses": (
        "proofs/Agent101MaximumWitnesses.lean",
        "d915b9df4e9ef3ab92ae9a33c3edd655b8567c40af7b88026e067408303182b7",
        ["Agent105CrossWidth9df76b"],
    ),
    "Agent101AllWidthMaximum": (
        "proofs/Agent101AllWidthMaximum.lean",
        "9bbdc9351ccb72d2502ca303a7963c1b2aa1e50afd0e9f5d3d095305b34983d9",
        ["Agent105CrossWidth9df76b", "Agent101NonpalindromicFibers",
         "Agent101WidthFiberBounds", "Agent101MaximumWitnesses"],
    ),
}

PUBLIC = {
    "Agent101ProfileExtraction": ("Agent101", [
        ("theorem", "reverse_wrapDigits"),
        ("theorem", "exists_coefficientWord_of_reverse"),
        ("theorem", "coefficientWord_half_length"),
        ("theorem", "digitFn_coefficientWord_cons_zero"),
        ("theorem", "digitPairSums_reverse"),
        ("theorem", "digitPairSums_profile"),
        ("theorem", "digitPairSums_profile_cons"),
    ]),
    "Agent101WidthFiberBounds": ("Agent101", [
        ("theorem", "mem_numericFiber_of_same_width_step"),
        ("theorem", "fixed_width_profile_length_le"),
        ("theorem", "profileCount_cons_outer_le"),
        ("theorem", "fixed_width_preimages_outer_bound"),
        ("theorem", "fixed_width_preimages_bound"),
        ("theorem", "one_digit_preimages_bound"),
    ]),
    "Agent101MaximumWitnesses": ("Agent101.MaximumWitnesses", [
        ("def", "maximumHalf"),
        ("def", "maximumCenter"),
        ("def", "maximumWord"),
        ("def", "maximumTarget"),
        ("def", "maximumPreimages"),
        ("theorem", "maximumHalf_cons"),
        ("theorem", "length_maximumWord"),
        ("theorem", "maximumWord_bounded"),
        ("theorem", "maximumWord_canonical"),
        ("theorem", "maximumWord_units"),
        ("theorem", "maximumTarget_width"),
        ("theorem", "maximumCenter_count"),
        ("theorem", "maximumPreimages_nodup"),
        ("theorem", "length_maximumPreimages"),
        ("theorem", "mem_maximumPreimages_fixed"),
        ("theorem", "maximumPreimages_nonempty"),
        ("theorem", "mem_maximumPreimages"),
        ("theorem", "all_width_maximum_witness"),
        ("theorem", "one_digit_preimages"),
        ("theorem", "one_digit_maximum_witness"),
    ]),
    "Agent101AllWidthMaximum": ("Agent101.Maximum", [
        ("theorem", "predecessor_width_cases"),
        ("theorem", "predecessor_one_digit_width"),
        ("theorem", "width_bound_mono"),
        ("theorem", "two_width_bound_arithmetic"),
        ("theorem", "all_width_preimages_bound"),
        ("theorem", "one_digit_target_preimages_bound"),
        ("theorem", "all_width_inverse_maximum"),
        ("theorem", "one_digit_inverse_maximum"),
    ]),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_pinned(path: str, expected: str) -> bytes:
    full = ROOT / path
    require(not Path(path).is_absolute() and full.resolve().is_relative_to(ROOT),
            "Unsafe repository-relative path: " + path)
    data = full.read_bytes()
    require(sha256(data) == expected, "Source/metadata hash mismatch: " + path)
    return data


def pin(path: str, data: bytes | None = None) -> dict:
    data = (ROOT / path).read_bytes() if data is None else data
    return {"path": path, "bytes": len(data), "sha256": sha256(data),
            "git_blob": git_blob(data)}


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def actual_imports(code: str) -> list[str]:
    return [dep for line in re.findall(r"^\s*import\s+([^\n]+)", code, re.M)
            for dep in line.split()]


def source_exports(module: str, record: dict, text: str, code: str) -> dict:
    namespace, expected = PUBLIC[module]
    require(re.findall(r"^namespace\s+(\S+)\s*$", code, re.M) == [namespace],
            "Unexpected namespace layout: " + module)
    require(re.findall(r"^end\s+(\S+)\s*$", code, re.M) == [namespace],
            "Unexpected namespace end: " + module)
    matches = list(re.finditer(r"^(theorem|def)\s+([A-Za-z_][\w']*)\b", code, re.M))
    require([(m[1], m[2]) for m in matches] == expected,
            "Public declaration inventory changed: " + module)
    require(not re.search(r"^(?:private|protected|noncomputable|opaque|axiom|lemma)\b", code, re.M),
            "Unexpected declaration modifier requires manual inventory review: " + module)
    printed = re.findall(r"^#print\s+axioms\s+(\S+)\s*$", code, re.M)
    require(printed == [name for _, name in expected],
            "All-public print-axioms inventory mismatch: " + module)
    entries = []
    for match in matches:
        body_at = code.find(":=", match.end())
        require(body_at >= 0, "Missing declaration body: " + module + "." + match[2])
        print_match = re.search(r"^#print\s+axioms\s+" + re.escape(match[2]) + r"\s*$", code, re.M)
        entries.append({
            "kind": match[1], "name": namespace + "." + match[2],
            "source_line_1_based": text.count("\n", 0, match.start()) + 1,
            "print_axioms_line_1_based": text.count("\n", 0, print_match.start()) + 1,
            "declaration_head": text[match.start():body_at].rstrip(),
        })
    return {**record, "namespace": namespace,
            "public_declaration_count": len(entries),
            "theorem_count": sum(e["kind"] == "theorem" for e in entries),
            "definition_count": sum(e["kind"] == "def" for e in entries),
            "public_declarations": entries}


def render_readme(registry_data: bytes, exports_data: bytes, registry: dict,
                  inventory: dict, order: list[str], script_pin: dict) -> bytes:
    records = registry["projects"][PROJECT]["modules"]
    rows = "\n".join(
        f"| `{m}` | {r['theorem_count']} | {r['definition_count']} | `{r['sha256']}` |"
        for m, r in inventory["modules"].items())
    source_rows = "\n".join(
        f"| `{m}` | `{records[m]['path']}` | `{records[m]['sha256']}` |" for m in order)
    text = f"""# All-width inverse maximum: pinned registry and reproduction

This packet registers the exact 17-module source closure of
`{ROOT_MODULE}` under project `{PROJECT}`. Its four new modules
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

The seven records from `{BASE_REGISTRY}` are retained unchanged. They
include the palindrome and nonpalindrome modules because the root reuses
`Agent101.length_filter_partition`. The original Research foundation is
used directly; this closure needs no embedded-foundation adapter.

The two Agent105 files are unchanged original sources from commit
`{AGENT105_COMMIT}`. Their source record is
`{AGENT105_PROVENANCE}`. The original Agent2 overflow bound, actual, and
local files are stored byte-for-byte in `bounds/dependencies/agent2/`, with
their original paths, Git blobs, and commit `{AGENT2_COMMIT}` in
`bounds/dependencies/agent2/PROVENANCE.json`. Its fourth entry pins the
unchanged repository `PeriodObstructions` source. Registry paths select
these exact files, independently of any unrelated same-name file.

| New module | Theorems | Definitions | Accepted source SHA256 |
|---|---:|---:|---|
{rows}

The actual root-reachable build order and complete source pins are:

| Logical module | Repository-relative path | SHA256 |
|---|---|---|
{source_rows}

Only `propext`, `Classical.choice`, and `Quot.sound` are allowed axioms.
The registry sets `catalogue_complete` to false and names this one project;
it makes no repository-wide catalogue or verification claim. Original
dependency authorship remains with the source modules listed above.

## Metadata pins

| Artifact | SHA256 |
|---|---|
| `{REGISTRY}` | `{sha256(registry_data)}` |
| `PUBLIC_EXPORTS.json` | `{sha256(exports_data)}` |
| `make_registry.py` | `{script_pin['sha256']}` |
| Original verifier | `{VERIFIER_SHA256}` |
| Original seven-module registry | `{BASE_SHA256}` |
| Agent2 provenance | `{AGENT2_PROVENANCE_SHA256}` |
| Agent105 provenance | `{AGENT105_PROVENANCE_SHA256}` |
| Lean executable, version 4.19.0 / commit 6caaee842e94 | `{LEAN_SHA256}` |

`make_registry.py` uses Python's standard library, reads the unchanged
original verifier's comment/string masker, checks every source SHA256 and
Git blob, validates the exact import closure, scans the complete selected
source code for forbidden proof shortcuts, and checks all 41 declarations
against a fixed inventory. It creates this metadata deterministically and
refuses to overwrite different existing generated files. Its output
includes metadata hashes, including this document's hash. It never invokes
Lean, fetches dependencies, or modifies Git.

```bash
python3 {SCRIPT} --check
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
AGENT101_PACKET={PACKET}
AGENT101_LEAN=/workspace/scratch/2a8a87fd78df/agent101-runtime/toolchain/lean-4.19.0-linux/bin/lean
AGENT101_BUILD=/workspace/scratch/2a8a87fd78df/agent101-all-width-canonical-review-01

python3 "$AGENT101_PACKET/make_registry.py" --check --check-published-commit "$AGENT101_COMMIT"
python3 {VERIFIER} \\
  --lean "$AGENT101_LEAN" \\
  --output "$AGENT101_BUILD" \\
  --project {PROJECT} \\
  --registry {REGISTRY}
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
  cd "$AGENT101_BUILD/{PROJECT}/source"
  LEAN_PATH="$PWD" "$AGENT101_LEAN" --trust=0 -j1 -DElab.async=false \\
    ProjectAudit.lean > ../logs/ProjectAudit-trust0.log 2>&1
)
```

The reviewer must record the actual exit status and log hash, and confirm
the audit's complete theorem count and allowed axiom union. Preserve any
failed build and its command/log/source snapshot; use a new output path
for any justified retry. A published-commit identity check, a canonical
Lean `PASS`, and the explicit trust-zero audit are three distinct results;
none is inferred merely from this registry's existence.
"""
    return text.encode()


def generate() -> tuple[dict[str, bytes], dict, list[str]]:
    base = json.loads(read_pinned(BASE_REGISTRY, BASE_SHA256))
    read_pinned(VERIFIER, VERIFIER_SHA256)
    agent2 = json.loads(read_pinned(AGENT2_PROVENANCE, AGENT2_PROVENANCE_SHA256))
    agent105 = json.loads(read_pinned(AGENT105_PROVENANCE, AGENT105_PROVENANCE_SHA256))
    spec = importlib.util.spec_from_file_location("agent101_original_verifier", ROOT / VERIFIER)
    require(spec is not None and spec.loader is not None, "Cannot load original verifier")
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    records = copy.deepcopy(base["projects"]["agent101-nonpalindromic-fibers"]["modules"])
    require(len(records) == 7, "Pinned base must contain exactly seven modules")
    for module, (path, expected_sha, deps) in ADDED.items():
        require(module not in records, "Repeated module: " + module)
        data = read_pinned(path, expected_sha)
        records[module] = {"path": path, "sha256": expected_sha,
                           "git_blob": git_blob(data), "imports": deps}
    require(len(records) == 17, "Expected 17 modules")
    provenance = {
        module: {"kind": "unchanged_inherited_registry_record",
                 "registry": BASE_REGISTRY, "registry_sha256": BASE_SHA256}
        for module in base["projects"]["agent101-nonpalindromic-fibers"]["modules"]
    }
    for rec in agent2:
        module = rec.get("module", Path(rec["original_path"]).stem)
        actual = records[module]
        require(rec["source_commit"] == AGENT2_COMMIT
                and all(actual[k] == rec[k] for k in ("path", "sha256", "git_blob")),
                "Agent2 original provenance mismatch: " + module)
        provenance[module] = {"kind": "unchanged_original_source",
                              "source_commit": AGENT2_COMMIT,
                              "original_path": rec["original_path"],
                              "provenance_path": AGENT2_PROVENANCE,
                              "provenance_sha256": AGENT2_PROVENANCE_SHA256}
    require(agent105["source_commit"] == AGENT105_COMMIT, "Agent105 provenance commit changed")
    for rec in agent105["source_files"]:
        module = Path(rec["display_title"]).stem
        require(records[module]["git_blob"] == rec["sha"], "Agent105 original blob mismatch")
        provenance[module] = {"kind": "unchanged_original_source",
                              "source_commit": AGENT105_COMMIT,
                              "original_path": "proofs/" + rec["display_title"],
                              "source_url": rec["display_url"],
                              "provenance_path": AGENT105_PROVENANCE,
                              "provenance_sha256": AGENT105_PROVENANCE_SHA256}
    public_modules = {}
    for module, rec in records.items():
        data = read_pinned(rec["path"], rec["sha256"])
        require(git_blob(data) == rec["git_blob"], "Git blob mismatch: " + module)
        code = verifier.code_only(data.decode())
        require(not re.search(r"(?<![\w'])\b(?:sorry|admit|axiom|sorryAx|native_decide|ofReduceBool|skipKernelTC)\b(?![\w'])", code),
                "Forbidden source token: " + module)
        require(actual_imports(code) == rec["imports"], "Exact import mismatch: " + module)
        for dep in rec["imports"]:
            require(dep in records or dep.split(".")[0] in {"Init", "Std", "Lean"},
                    "Unregistered source import: " + dep)
        if module in PUBLIC:
            public_modules[module] = source_exports(module, rec, data.decode(), code)
            provenance[module] = {"kind": "new_claimed_contribution_exact_source_pin",
                                  "task_id": TASK, "publication_commit": None}
    require(set(provenance) == set(records), "Incomplete source provenance coverage")
    order, active, seen = [], set(), set()

    def visit(module: str) -> None:
        if module not in records or module in seen:
            return
        require(module not in active, "Import cycle: " + module)
        active.add(module)
        for dep in records[module]["imports"]:
            visit(dep)
        active.remove(module)
        seen.add(module)
        order.append(module)

    visit(ROOT_MODULE)
    require(seen == set(records), "Registry contains a module outside the root closure")
    endpoints = [entry["name"] for rec in public_modules.values()
                 for entry in rec["public_declarations"]]
    require(len(endpoints) == len(set(endpoints)) == 41, "Expected 41 distinct public declarations")
    require(sum(rec["theorem_count"] for rec in public_modules.values()) == 36,
            "Expected 36 new public theorems")
    require(sum(rec["definition_count"] for rec in public_modules.values()) == 5,
            "Expected five new public definitions")
    script_pin = pin(SCRIPT)
    registry = {
        "schema_version": 1,
        "toolchain": {"version": "4.19.0", "release_commit": "6caaee842e94",
                      "allowed_axioms": ALLOWED},
        "catalogue_complete": False,
        "catalogue_blockers": [
            "This registry covers only the exact 17-module Agent101 all-width inverse-maximum contribution, not the repository-wide accepted catalogue."
        ],
        "projects": {PROJECT: {
            "scope": "Sharp maximum cardinality of complete positive ordinary-integer reverse-add predecessor fibers across all decimal input widths: 9 * 10 ^ (D / 2 - 1) for every target width D >= 2, and one for target width one; arbitrary duplicate-free predecessor-list upper bounds and explicit complete attaining fibers.",
            "roots": [ROOT_MODULE], "modules": records,
        }},
        "claims": [{"project": PROJECT, "task_id": TASK, "endpoints": endpoints}],
        "provenance": {
            "coordination_commit": "302e8608f98060ea07738c25f00476238975d9dd",
            "coordination_claim_blob": "baf4f026e28a11b79dc3de04904876c37d6b1aeb",
            "source_identity": "Exact per-module SHA256 and Git-blob pins; publication must additionally be checked at the integration writer's published commit.",
            "generator": script_pin,
            "unchanged_original_verifier": pin(VERIFIER),
            "modules": provenance,
        },
    }
    registry_data = json_bytes(registry)
    inventory = {
        "schema_version": 1, "task_id": TASK, "project": PROJECT,
        "root_module": ROOT_MODULE,
        "scope": "All public theorem and def declarations in the four new claimed modules, excluding generated auxiliary declarations and declarations inherited from dependencies.",
        "registry": pin(REGISTRY, registry_data), "generator": script_pin,
        "original_verifier": pin(VERIFIER),
        "axiom_policy": {"allowed_axioms": ALLOWED,
                         "audit_status": "This is a source inventory. Actual axiom results must be read from the retained Lean compiler and full module-audit logs."},
        "source_module_count": 17, "new_module_count": 4,
        "public_declaration_count": 41, "theorem_count": 36, "definition_count": 5,
        "canonical_verification_performed_by_metadata_generator": False,
        "modules": public_modules,
    }
    exports_data = json_bytes(inventory)
    readme_data = render_readme(registry_data, exports_data, registry, inventory, order, script_pin)
    return {REGISTRY: registry_data, EXPORTS: exports_data, README: readme_data}, registry, order


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Compare generated metadata without writing")
    parser.add_argument("--check-published-commit", metavar="FULL_COMMIT",
                        help="Require identical sources and metadata in this exact Git commit; implies --check")
    args = parser.parse_args()
    generated, registry, order = generate()
    check = args.check or args.check_published_commit is not None
    for path, data in generated.items():
        full = ROOT / path
        if full.exists():
            require(full.read_bytes() == data, "Existing metadata differs; refusing to overwrite: " + path)
        else:
            require(not check, "Missing generated metadata: " + path)
    if not check:
        for path, data in generated.items():
            full = ROOT / path
            if not full.exists():
                with full.open("xb") as stream:
                    stream.write(data)
    published_files = []
    if args.check_published_commit is not None:
        commit = args.check_published_commit
        require(re.fullmatch(r"[0-9a-f]{40}", commit) is not None,
                "Use a full lowercase 40-character published commit")
        resolved = subprocess.check_output(["git", "rev-parse", commit + "^{commit}"], cwd=ROOT, text=True).strip()
        require(resolved == commit, "Published commit did not resolve exactly")
        records = registry["projects"][PROJECT]["modules"]
        paths = {rec["path"] for rec in records.values()} | set(generated) | {
            SCRIPT, BASE_REGISTRY, VERIFIER, AGENT2_PROVENANCE, AGENT105_PROVENANCE}
        for path in sorted(paths):
            data = subprocess.check_output(["git", "show", commit + ":" + path], cwd=ROOT)
            require(data == (ROOT / path).read_bytes(), "Published bytes differ or are absent: " + path)
            published_files.append(pin(path, data))
    print(json.dumps({
        "status": "METADATA_AND_SOURCE_IDENTITY_CHECK_ONLY",
        "mathematical_proof_check": False, "lean_invoked": False,
        "project": PROJECT, "source_modules": len(order), "build_order": order,
        "new_public_declarations": 41, "new_public_theorems": 36, "new_public_definitions": 5,
        "metadata": [pin(path) for path in [SCRIPT, REGISTRY, EXPORTS, README]],
        "published_commit_checked": args.check_published_commit,
        "published_files_checked": published_files,
    }, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print("METADATA_CHECK_FAILED: " + str(exc), file=sys.stderr)
        raise SystemExit(1)
