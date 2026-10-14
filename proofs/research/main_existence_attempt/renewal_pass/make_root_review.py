#!/usr/bin/env python3
"""Bind the completed review to exact sources, audits and retained archives.

This assembles existing verification evidence; it is not a substitute for
the branch checkers or a new proof of the main existence statement.
"""
from pathlib import Path
import gzip
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(rel):
    return json.loads((HERE / rel).read_text())


def main():
    modules = [
        ("lean", "DelayedOverlapGate.lean"),
        ("lean/prefix", "PrefixObstruction.lean"),
        ("lean/incoming_carry", "IncomingCarrySensitivity.lean"),
        ("lean/raw_symmetry", "RawSymmetryObstruction.lean"),
    ]
    formal = []
    for folder, filename in modules:
        source = HERE / folder / filename
        fresh = read(folder + "/verification.json")
        root = read(folder + "/root_verification.json")
        assert fresh["status"] == root["status"] == "PASS", folder
        sha = digest(source)
        assert fresh["source_sha256"][filename] == root["source_sha256"] == sha
        names = re.findall(r"^theorem\s+(\w+)", source.read_text(), re.M)
        assert len(names) == fresh["new_theorems_audited"] == root["new_theorems_audited"]
        assert fresh["theorem_axioms"] == root["theorem_axioms"]
        assert all(set(a) <= ALLOWED for a in root["theorem_axioms"].values())
        formal.append({"source": folder + "/" + filename, "sha256": sha,
                       "declarations": len(names), "fresh_source_build": True,
                       "independent_root_module_and_axiom_rebuild": True,
                       "root_rebuilt_dependencies_again": False})
    external = read("external_review/root_verification.json")
    assert external["status"] == "PASS" and external["theorem_count"] == 24
    assert external["fresh_dependency_rebuild"]
    assert all(set(a) <= ALLOWED for a in external["axiom_audit"].values())

    certificate_checks = [
        ("tails/symbolic_tail_audit.json", "tails/symbolic_tail_certificates.json"),
        ("language/inverse_ladder_audit.json", "language/inverse_ladder_certificate.json"),
        ("language/prefix_obstruction_audit.json", "language/prefix_obstruction_certificate.json"),
        ("seam_audit/overflow_local_audit.json", "seam_audit/overflow_local_certificate.json"),
    ]
    for report, certificate in certificate_checks:
        assert read(report)["certificate_sha256"] == digest(HERE / certificate), report
    archive_audit = read("language/exploration_archive_audit.json")
    assert archive_audit["status"] == "INDEPENDENT_FINITE_ARCHIVE_REPLAY_PASS"
    assert archive_audit["archive_sha256"] == digest(HERE / "language/exploration_archive.json.gz")
    assert archive_audit["safe_inverse_edges"] == 2659

    witnesses = read("constructive/capture_witnesses.json")
    total = 0
    for row in witnesses["archives"]:
        path = HERE / "constructive" / row["archive"]
        data = gzip.decompress(path.read_bytes())
        assert digest(path) == row["archive_sha256"]
        assert hashlib.sha256(data).hexdigest() == row["uncompressed_sha256"]
        assert len(json.loads(data)) == row["comparison_records"]
        original = read("constructive/" + row["source"].replace(".py", ".json"))
        assert original["uniform_comparison_certificate"]["witness_stream_sha256"] == row["uncompressed_sha256"]
        total += row["comparison_records"]
    assert total == witnesses["total_records"] == 5204
    seam = read("constructive/collision_response/seam_response.json")
    data = gzip.decompress((HERE / "constructive/collision_response" / seam["full_record_archive"]).read_bytes())
    assert hashlib.sha256(data).hexdigest() == seam["full_record_sha256"]
    assert len(json.loads(data)) == seam["total_cases"] == 2737
    independent_seam = read("seam_audit/seam_audit.json")
    assert independent_seam["status"] == "INDEPENDENT_SEAM_AND_VACUITY_AUDIT_PASS"
    assert independent_seam["canonical_partitions"] == 58221
    assert independent_seam["canonical_symmetric_E_nonzero_K_antecedent"] == "IMPOSSIBLE_BY_UNRESTRICTED_PROOF"
    positive = read("seam_audit/positive_safety_audit.json")
    assert positive["status"] == "ALL_CANONICAL_ACTIVE_SEAMS_SAFE"
    assert positive["checked_cases"] == 2495
    positive_archive = HERE / "seam_audit/positive_safety_controls.json.gz"
    positive_bytes = gzip.decompress(positive_archive.read_bytes())
    assert hashlib.sha256(positive_bytes).hexdigest() == positive["content_sha256"]
    assert positive_archive.stat().st_size == positive["compressed_bytes"]
    assert len(json.loads(positive_bytes)["cases"]) == positive["checked_cases"]
    closure_examples = read("external_review/collision_safety_examples.json")
    assert closure_examples["status"] == "PASS" and len(closure_examples["records"]) == 4
    assert not any(r["next_is_palindrome"] for r in closure_examples["records"][:3])
    assert closure_examples["records"][0]["independent_closure"] is False
    assert closure_examples["records"][0]["active_seam"] is False
    assert closure_examples["records"][2]["independent_closure"] is True
    assert closure_examples["records"][3]["canonical_core"] is False
    assert closure_examples["records"][3]["next_is_palindrome"] is True
    graph_dir = HERE / "external_review/seven_step_graph"
    graph_audit = read("external_review/seven_step_graph/graph_verification.json")
    assert graph_audit["status"] == "INDEPENDENT_LITERAL_INTEGER_AND_RANK_VERIFICATION_PASS"
    assert graph_audit["vertices"] == 48013
    assert graph_audit["labeled_controls_recomputed"] == 96026
    assert graph_audit["accepted_labeled_edges"] == 61731
    assert graph_audit["rank_max_by_phase"][0] == 26
    graph_data = gzip.decompress((graph_dir / "six_prefix_graph.json.gz").read_bytes())
    assert digest(graph_dir / "six_prefix_graph.json.gz") == graph_audit["compressed_sha256"]
    assert hashlib.sha256(graph_data).hexdigest() == graph_audit["decoded_sha256"]
    assert len(json.loads(graph_data)["rank"]) == 48013
    assert graph_audit["prefix_controls_independently_checked"] == 128
    assert graph_audit["returning_control_words"] == 4
    sharp = read("external_review/seven_step_graph/sharp_example.json")
    assert sharp["status"] == "PASS" and sharp["initial_phase_clock_transitions"] == 26
    assert sharp["three_consecutive_safe_returns"] == [7,14,21]

    # Keep the recorded manual proof review separate from automatic integrity
    # checks. Source placeholders and theorem axioms were checked by the
    # referenced fresh-build and independent-recompile programs.
    reviewed_written_proofs = [
        "constructive/STATUS.md", "constructive/collision_response/SEAM_RESPONSE.md",
        "language/METHOD_AND_PROOF.md", "tails/STATUS.md", "seam_audit/METHOD_AND_PROOF.md",
        "external_review/COLLISION_SAFETY_COROLLARY.md",
        "external_review/seven_step_graph/ACTUAL_ORBIT_INCLUSION.md",
    ]
    for path in reviewed_written_proofs:
        assert (HERE / path).is_file(), path
    omitted = {"fresh_build", "root_build", "__pycache__"}
    hashes = {}
    for path in sorted(HERE.rglob("*")):
        if not path.is_file() or any(part in omitted for part in path.relative_to(HERE).parts):
            continue
        if path.name == "ROOT_REVIEW.json":
            continue
        hashes[str(path.relative_to(HERE))] = digest(path)
    report = {
        "status": "COMPLETED_SUPPORTING_RESULT_REVIEW",
        "main_decimal_lychrel_existence_proved": False,
        "assertion_for_196_proved": False,
        "infinitely_repeatable_safe_return_found": False,
        "formal_modules": formal,
        "renewal_supporting_declarations": sum(row["declarations"] for row in formal),
        "independently_rebuilt_external_declarations": 24,
        "external_source_commit": external["source_commit"],
        "written_proofs_manually_reviewed": reviewed_written_proofs,
        "all_parameter_certificate_hashes_verified": certificate_checks,
        "full_comparison_records_retained": total,
        "full_seam_controls_retained": seam["total_cases"],
        "independent_canonical_partition_controls": independent_seam["canonical_partitions"],
        "independent_active_canonical_controls": positive["checked_cases"],
        "safe_inverse_edges_independently_replayed": archive_audit["safe_inverse_edges"],
        "raw_symmetry_shortcut": "Impossible for canonical pair words; original attempt retained",
        "positive_seam_safety": "Nonzero actual carry defect alone certifies an ordinary nonpalindromic next step; full Lean bridge audited",
        "combined_closure_safety": "Written all-length proof: failed independent BHB closure certifies safety, including unequal isolated overflow bits with zero seam defect",
        "external_collision_source_commit": "a3914ba08e5facb59699d066fcb69f1bd37b6e6a",
        "external_full_driver_trace_replayed_by_root": False,
        "independent_seven_step_graph_reconstruction": {
            "external_announcement_commit": "8a42fe14262fee12ce1c8b40bf25e97b94044742",
            "vertices": 48013, "controls": 96026, "edges": 61731,
            "phase_zero_rank": 26, "four_consecutive_returns_excluded": True,
            "written_actual_orbit_inclusion_all_widths_at_least_six": True,
            "kernel_checked_rank_proof": False,
        },
        "artifact_sha256": hashes,
        "infrastructure_exclusion_categories": sorted(omitted),
        "scope": "Supporting finite, all-parameter and structural results; no solution of the main existence problem.",
    }
    (HERE / "ROOT_REVIEW.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["status"], "reviewed_artifacts": len(hashes),
                      "renewal_supporting_declarations": report["renewal_supporting_declarations"],
                      "independently_rebuilt_external_declarations": 24}, sort_keys=True))


if __name__ == "__main__":
    main()
