#!/usr/bin/env python3
"""Check every retained capped-probe artifact against its original hash."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    report = dict(status="COMPLETED_CAPPED_PROBES_RETAINED",
                  source_sha256=hashlib.sha256((HERE / "scalar_clock.py").read_bytes()).hexdigest(),
                  scope="The seven_4 clock is independently audited separately. These two clocks remain UNKNOWN. A cap is neither an exclusion nor evidence of an actual infinite integer orbit.",
                  probes={})
    for name in ("primitive14", "seven_1"):
        path = HERE / name / "scalar_clock.json"
        data = json.loads(path.read_text())
        assert data["status"] == "UNKNOWN_CAP"
        last = data["completed_graphs"][-1]
        probe = dict(status=data["status"], last_completed_width=last["width"],
                     last_retained_vertices=last["retained_vertices"],
                     last_retained_edges=last["retained_edges"],
                     next_lift=data["next_lift"], caps=data["caps"],
                     report_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                     completed_graph_files=[])
        for graph in data["completed_graphs"]:
            for kind in ("raw_artifact", "retained_artifact"):
                artifact = graph[kind]
                file = HERE / name / artifact["filename"]
                digest = hashlib.sha256(file.read_bytes()).hexdigest()
                assert digest == artifact["sha256"], str(file)
                assert file.stat().st_size == artifact["compressed_bytes"], str(file)
                probe["completed_graph_files"].append(dict(
                    path=str(file.relative_to(HERE)), bytes=file.stat().st_size,
                    sha256=digest))
        report["probes"][name] = probe
    (HERE / "CAPPED_PROBES.json").write_text(json.dumps(report, indent=2) + "\n")
    print("PASS_ALL_CAPPED_PROBE_HASHES")


if __name__ == "__main__":
    main()
