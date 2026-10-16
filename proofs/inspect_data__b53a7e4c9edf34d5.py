#!/usr/bin/env python3
"""Independently parse emitted Lean lookup trees and compare frozen certificate rows.

This does not import the data generator and is not a replacement for kernel
checking. It checks the generated files currently present, recording that set.
"""

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE.parent / "2026-10-14-component-specific-bound/component_certificates.json.gz"
CERTIFICATE_SHA256 = "ff7a70ee2a6ed677cb9176e212dc0a69acd14eed30425a42b543d7a50823b47e"
GENERATED = HERE.parent / "2026-10-15-scalar-finite-certificate-formal/generated"


def sha(blob):
    return hashlib.sha256(blob).hexdigest()


def parse_tree(expression):
    tokens = re.findall(r"if|then|else|i|\d+|[()<]", expression)
    assert "".join(tokens) == re.sub(r"\s", "", expression)
    position = 0

    def expect(token):
        nonlocal position
        assert tokens[position] == token, (tokens[position], token)
        position += 1

    def parse():
        nonlocal position
        if tokens[position] == "(":
            position += 1
            result = parse()
            expect(")")
            return result
        if tokens[position] == "if":
            position += 1
            expect("i")
            expect("<")
            split = int(tokens[position])
            position += 1
            expect("then")
            left = parse()
            expect("else")
            right = parse()
            return split, left, right
        result = int(tokens[position])
        position += 1
        return result

    result = parse()
    assert position == len(tokens)
    return result


def evaluate(tree, index):
    while isinstance(tree, tuple):
        split, left, right = tree
        tree = left if index < split else right
    return tree


def lookup_functions(source):
    return {name: parse_tree(body) for name, body in re.findall(
        r"^def (\w+) \(i : Nat\) : Nat := ([^\n]+)$", source, re.M)
        if re.fullmatch(r"(?:bounds|widths|(?:meta|components|nextCodes|ranks|members|inverse)\d+)", name)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generated", type=Path, default=GENERATED)
    parser.add_argument("--report", type=Path, default=HERE / "data_review.json")
    args = parser.parse_args()
    payload = CERTIFICATE.read_bytes()
    assert sha(payload) == CERTIFICATE_SHA256
    jobs = json.loads(gzip.decompress(payload))["jobs"][:16]
    assert [j["id"] for j in jobs] == list(range(16))
    assert all(j["hierarchy"] == "scalar" for j in jobs)
    parent_links = {}
    for parent in jobs:
        for link in parent["children"]:
            identity = link["child_job"]
            assert identity not in parent_links
            parent_links[identity] = parent, link
    records, source_hashes, parsed_jobs = [], {}, {}
    paths = [args.generated / "JobCatalog.lean"] + sorted(
        args.generated.glob("JobData*.lean"), key=lambda p: int(p.stem[7:]))
    for path in paths:
        blob = path.read_bytes()
        source_hashes[path.name] = sha(blob)
        source = blob.decode()
        compact = re.sub(r"\s", "", source)
        trees = lookup_functions(source)
        if path.stem == "JobCatalog":
            expected = {
                "bounds": [j["max_path_vertices_bound"] for j in jobs],
                "widths": [j["width"] for j in jobs],
            }
            assert "defjobBound(j:Nat):Nat:=boundsj" in compact
            assert "defjobWidth(j:Nat):Nat:=widthsj" in compact
            identity = None
        else:
            identity = int(path.stem[7:])
            job = jobs[identity]
            vertices = job["vertices"]
            raw_to_local = {row[0]: i for i, row in enumerate(vertices)}
            assert len(raw_to_local) == len(vertices)
            components = [None] * len(vertices)
            for component, group in enumerate(job["components"]):
                for raw in group:
                    at = raw_to_local[raw]
                    assert components[at] is None
                    components[at] = component
            assert None not in components
            transitions = [0] * (2 * len(vertices))
            for source_raw, target_raw, carry in job["edges"]:
                assert carry in (0, 1)
                at = 2 * raw_to_local[source_raw] + carry
                assert transitions[at] == 0
                transitions[at] = raw_to_local[target_raw] + 1
            expected = {
                f"meta{identity}": [phase + 7 * last + 133 * low
                    for _, phase, last, low, _ in vertices],
                f"components{identity}": components,
                f"nextCodes{identity}": transitions,
                f"ranks{identity}": job["weighted_sink_ranks"],
            }
            for declaration in [
                f"defcomponent{identity}(v:Nat):Nat:=components{identity}v",
                f"phasev:=(meta{identity}v)%7",
                f"lastv:=(meta{identity}v)/7%19",
                f"lowv:=(meta{identity}v)/133",
                f"nextubit:=nextCodes{identity}(2*u+bit)",
                f"component:=component{identity}",
                f"cyclicc:=decide(childCode{identity}c≠0)",
                f"weightc:=ifchildCode{identity}c=0then1elsejobBound(childCode{identity}c-1)",
                f"rankc:=ranks{identity}c",
                f"bound:=jobBound{identity}",
            ]:
                assert declaration in compact, (path.name, declaration)
            assert all(0 <= phase < 7 and 0 <= last < 19 and low in (0, 1)
                       for _, phase, last, low, _ in vertices)
            assert f"  size := {len(vertices)}\n" in source
            if identity in parent_links:
                parent, link = parent_links[identity]
                parent_local = {row[0]: i for i, row in enumerate(parent["vertices"])}
                projection = dict(link["child_to_parent_raw"])
                assert len(vertices) % 19 == 0
                members = []
                for ordinal in range(len(vertices) // 19):
                    group = vertices[19 * ordinal:19 * ordinal + 19]
                    parent_raw = projection[group[0][0]]
                    assert all(projection[row[0]] == parent_raw and row[2] == coefficient
                        for coefficient, row in enumerate(group))
                    members.append(parent_local[parent_raw])
                assert len(members) == len(set(members))
                selected_members = {parent_local[v] for v in parent["components"][link["component"]]}
                assert set(members) == selected_members
                inverse = [0] * len(parent["vertices"])
                for ordinal, member in enumerate(members):
                    inverse[member] = ordinal
                expected[f"members{identity}"] = members
                expected[f"inverse{identity}"] = inverse
                assert f"defmember{identity}(i:Nat):Nat:=members{identity}i" in compact
                assert f"defmemberIndex{identity}(u:Nat):Nat:=inverse{identity}u" in compact
            child_codes = re.search(rf"^def childCode{identity} \(c : Nat\) : Nat := (.+)$",
                                    source, re.M).group(1)
            clauses = [(int(c), int(code)) for c, code in re.findall(
                r"if c=(\d+) then (\d+) else", child_codes)]
            assert clauses == [(link["component"], link["child_job"] + 1)
                               for link in job["children"]]
            assert child_codes.endswith("0")
            parsed_jobs[identity] = dict(trees=trees, size=len(vertices), children=dict(clauses))
        assert set(trees) == set(expected), (path.name, set(trees), set(expected))
        comparisons = 0
        for name, values in expected.items():
            for index, value in enumerate(values):
                assert evaluate(trees[name], index) == value, (path.name, name, index)
            assert evaluate(trees[name], len(values)) == 0
            assert evaluate(trees[name], len(values) + 100000) == 0
            comparisons += len(values) + 2
        records.append(dict(file=path.name, job=identity, tables=len(expected),
                            value_comparisons=comparisons))
    row_counts = dict(vertex=0, edge=0, coverage=0, field=0, lift=0)
    bounds = [j["max_path_vertices_bound"] for j in jobs]

    def value(job, name, index):
        return evaluate(parsed_jobs[job]["trees"][f"{name}{job}"], index)

    def fields(job, index):
        meta = value(job, "meta", index)
        return meta % 7, meta // 7 % 19, meta // 133

    def next_code(job, vertex, bit):
        return value(job, "nextCodes", 2 * vertex + bit)

    for identity, data in parsed_jobs.items():
        for u in range(data["size"]):
            component = value(identity, "components", u)
            child_code = data["children"].get(component, 0)
            weight = 1 if child_code == 0 else bounds[child_code - 1]
            rank = value(identity, "ranks", component)
            assert weight <= rank <= bounds[identity]
            row_counts["vertex"] += 1
            for bit in (0, 1):
                code = next_code(identity, u, bit)
                if code and code - 1 < data["size"]:
                    target_component = value(identity, "components", code - 1)
                    if component == target_component:
                        assert child_code != 0
                    else:
                        assert weight + value(identity, "ranks", target_component) <= rank
                row_counts["edge"] += 1
        if identity not in parent_links:
            continue
        parent, link = parent_links[identity]
        parent_id, selected = parent["id"], link["component"]
        if parent_id not in parsed_jobs:
            continue
        parent_size = parsed_jobs[parent_id]["size"]
        count = data["size"] // 19
        for u in range(parent_size):
            if value(parent_id, "components", u) == selected:
                ordinal = value(identity, "inverse", u)
                assert ordinal < count and value(identity, "members", ordinal) == u
            row_counts["coverage"] += 1
        for z in range(data["size"]):
            parent_vertex = value(identity, "members", z // 19)
            coefficient = z % 19
            phase, previous, low = fields(parent_id, parent_vertex)
            assert fields(identity, z) == (phase, coefficient, (coefficient + low) // 10)
            row_counts["field"] += 1
            for bit in (0, 1):
                gamma = (coefficient + bit) // 10
                code = next_code(parent_id, parent_vertex, gamma)
                target = max(0, code - 1)
                overflow = int(phase in (2, 4, 6))
                emitted = (coefficient + low) % 10 + (
                    (coefficient + bit) % 10 if overflow == 0 else (previous + gamma) % 10)
                if code and target < parent_size and value(parent_id, "components", target) == selected and emitted < 19:
                    assert next_code(identity, z, bit) == 19 * value(identity, "inverse", target) + emitted + 1
                row_counts["lift"] += 1
    assert all(sha((args.generated / name).read_bytes()) == digest
               for name, digest in source_hashes.items()), "Source changed during review"
    report = dict(status="PASS", certificate_sha256=CERTIFICATE_SHA256,
                  inspected_jobs=[record["job"] for record in records if record["job"] is not None],
                  generated_source_sha256=source_hashes, records=records,
                  finite_row_predicate_counts=row_counts,
                  checker_sha256=sha(Path(__file__).read_bytes()),
                  scope="Independent syntax-tree evaluation of present generated Lean data against exact frozen scalar certificate, plus direct evaluation of all five finite row predicates; not a kernel proof or the94/98 theorem.")
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(dict(status="PASS", jobs=report["inspected_jobs"],
                         value_comparisons=sum(r["value_comparisons"] for r in records))))


if __name__ == "__main__":
    main()
