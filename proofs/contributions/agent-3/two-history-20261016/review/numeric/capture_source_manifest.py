#!/usr/bin/env python3
"""Record source identities for the independent numeric semantic review.

This utility hashes source bytes only. It does not execute Lean, audit axioms,
or establish any mathematical proposition.
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


REVIEW = Path(__file__).resolve().parent
CONTRIBUTION = REVIEW.parents[1]
PROOFS = CONTRIBUTION.parents[2]
REPOSITORY = PROOFS.parent
WORKSPACE = REPOSITORY.parent
BUILD = WORKSPACE / "agent3-history-build"
PROTECTED = CONTRIBUTION.parent / "finite-horizon-overflow-20261016"

SOURCES = [
    ("IntegerInterfaces", CONTRIBUTION / "IntegerInterfaces.lean", "primary subject"),
    ("HistorySafety", CONTRIBUTION / "HistorySafety.lean", "primary subject"),
    ("NormalizedSafety", PROTECTED / "NormalizedSafety.lean", "inherited numeric interface"),
    ("FiniteHorizonTheorem", PROTECTED / "FiniteHorizonTheorem.lean", "inherited numeric interface"),
    ("SafetyBridge", PROTECTED / "SafetyBridge.lean", "inherited finite safety interface"),
    ("ActualHistories", CONTRIBUTION / "ActualHistories.lean", "history interfaces inspected"),
    ("HistoryInterfaces", CONTRIBUTION / "HistoryInterfaces.lean", "whole-word bridge inspected"),
    ("LychrelDigitSums", PROOFS / "LychrelDigitSums__cee9857896191714.lean", "original arithmetic; cited definitions and lemmas inspected"),
    ("DecimalSafeRuns", PROOFS / "DecimalSafeRuns__aaaac5a66315c5e2.lean", "original finite safety; complete source inspected"),
    ("Compat", PROOFS / "Compat__a87d4fe51356e8b5.lean", "original-name compatibility; complete source inspected"),
    ("TemplateStep", PROOFS / "TemplateStep__8a161b4553714264.lean", "list value, normalization, and canonical-digit lemmas inspected"),
    ("ActualWordBridge", PROOFS / "ActualWordBridge__7f032d27940694a8.lean", "canonical-pair definition and preservation interface inspected"),
    ("PeriodObstructions", PROOFS / "PeriodObstructions__70ce034b31b5b218.lean", "original normalize, pair, and stepWord definitions inspected"),
]

# These identities bind the recorded manual review to the inspected revision.
# A changed source requires a new review, not merely rerunning this utility.
REVIEWED_SHA256 = {
    "IntegerInterfaces": "bc6d2926cd16c43de990ede025b9ba69e50d1e7e2a578044ad65bdf348e8b4fe",
    "HistorySafety": "16ea25b00f12eed305519eb8de73b564bae5ff3a5ddd255895d5485bebfd33ff",
    "NormalizedSafety": "6c344b93df1f8574dcf8ecf60c9db09d3f798c3df1b13831713af010c71652c1",
    "FiniteHorizonTheorem": "3316df9f3ce5baeac971faff53cfe5d6616beebf50c116c5662476c261f0d697",
    "SafetyBridge": "18079ba07cccf1bcc9098320ae62f887ba080896be11bead43de6e7f26573e5e",
    "ActualHistories": "b72d9a6ef082c3d980b3f6f2a9dee64835d38ed32fb7d040abb39b9ea02c6ec4",
    "HistoryInterfaces": "c30d29782c8e68bf49d75bd4c969e04570556fe230f980bc579395d8deb8f60c",
    "LychrelDigitSums": "ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57",
    "DecimalSafeRuns": "2d0e44adfbfa2592b1eaedfb46d2dff3f62db0a2ca05171bb2a7c1a66ec03f22",
    "Compat": "73dca78232b0c2c048da4d1d182f84b31c0e95bab283fad603fd342bf38616e6",
    "TemplateStep": "76ad132fec23f9da8733f72a6baf22c3dbfe68d402a8165766bd8d163549d2ed",
    "ActualWordBridge": "3123e8f86fe751e61307ea528390bd265515a8d69c731f51e2808fb78d0a6ec6",
    "PeriodObstructions": "83102a949036799a929ba72d74ce9d76bc2a11cb3adf61e0bc06b6013b22991a",
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


records = []
for module, source, scope in SOURCES:
    source_sha = digest(source)
    if source_sha != REVIEWED_SHA256[module]:
        raise RuntimeError(f"Reviewed source changed for {module}; semantic re-review required")
    record = {
        "module": module,
        "repository_path": str(source.relative_to(REPOSITORY)),
        "sha256": source_sha,
        "bytes": source.stat().st_size,
        "review_scope": scope,
    }
    staged = BUILD / f"{module}.lean"
    if staged.exists():
        staged_sha = digest(staged)
        record["staged_source"] = str(staged)
        record["staged_sha256"] = staged_sha
        record["staged_matches_repository"] = staged_sha == record["sha256"]
        if not record["staged_matches_repository"]:
            raise RuntimeError(f"Source mismatch for {module}")
    records.append(record)

manifest = {
    "recorded_utc": datetime.now(timezone.utc).isoformat(),
    "reviewer": "Agent #3 / family_cardinality specialist",
    "review_result": "PASS",
    "verification_level": "independent semantic source review with source identity checks",
    "kernel_compile_performed_for_this_review": False,
    "axiom_audit_performed_for_this_review": False,
    "numeric_simulation_performed_for_this_review": False,
    "execution_scope": "Python hashlib over the listed source bytes; no mathematical verification is attributed to this script.",
    "independence": "Reviewer did not author IntegerInterfaces.lean or HistorySafety.lean. Reviewer authored TwoLayerCertificate.lean and HistoryFamily.lean; those modules are not subjects of this independent review.",
    "clean_build": "A separate runtime specialist owns the independent Lean rebuild; no result from that execution is asserted in this manifest.",
    "review_rationale": "semantic_review.md",
    "blocking_findings": [],
    "source_records": records,
}
(REVIEW / "source_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
for record in records:
    print(f"{record['module']}: {record['sha256']}")
print("Metadata capture complete; Lean execution was not performed by this review.")
