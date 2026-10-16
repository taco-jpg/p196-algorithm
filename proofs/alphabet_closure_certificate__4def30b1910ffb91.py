"""Solver-free closure exhaustion and replay for mixed periodic bulk codes.

The implication premises contain two selected motifs.  Their conclusions
list all tile sets compatible with one short cyclic input's actual outputs.
Starting from each pair, forced additions and exhaustive finite branching
either produce a compatible alphabet or a violated implication.  Thus an
exhausted UNSAT result excludes arbitrary alphabet sizes in this model.
"""
from itertools import combinations
from pathlib import Path
import json, time


def mask_of(xs):
    return sum(1 << i for i in set(xs))


def run(name):
    path = Path(__file__).with_name(name+"_alphabet_constraints.json")
    d = json.loads(path.read_text())
    rows = [(mask_of(word), [mask_of(a) for a in options])
            for word, options in d["constraints"]]
    by_pair = {}
    for row_id, (premise, options) in enumerate(rows):
        by_pair.setdefault(premise, []).append(row_id)
    nodes = []
    memo = {}
    started = time.monotonic()

    def search(initial):
        if initial in memo:
            return memo[initial]
        node_id = len(nodes)
        node = {"initial": hex(initial), "forced": []}
        nodes.append(node)
        memo[initial] = node_id
        state = initial
        while True:
            added = False
            branch = None
            active = [i for i in range(len(d["motifs"])) if state & (1 << i)]
            active_rows = [row for a,b in combinations(active, 2)
                           for row in by_pair[(1 << a) | (1 << b)]]
            for i in active_rows:
                premise, options = rows[i]
                if any(o & state == o for o in options):
                    continue
                if not options:
                    node["reject"] = i
                    return node_id
                if len(options) == 1:
                    node["forced"].append(i)
                    state |= options[0]
                    added = True
                elif branch is None:
                    branch = i
            if added:
                continue
            if branch is None:
                node["satisfying_alphabet"] = hex(state)
                return node_id
            node["branch"] = branch
            node["children"] = [search(state | o) for o in rows[branch][1]]
            return node_id

    roots = []
    for i, j in combinations(range(len(d["motifs"])), 2):
        roots.append([i, j, search((1 << i) | (1 << j))])
    successes = [n for n in nodes if "satisfying_alphabet" in n]
    result = {"name": name, "status": "SAT" if successes else "EXHAUSTED",
              "motif_count": len(d["motifs"]), "roots": roots, "nodes": nodes,
              "seconds": time.monotonic()-started}
    dest = Path(__file__).with_name(name+"_closure_certificate.json")
    dest.write_text(json.dumps(result, indent=2)+"\n")
    replay(d, result)
    print(json.dumps({"name": name, "status": result["status"],
                      "initial_pairs": len(roots), "certificate_nodes": len(nodes),
                      "forced_additions": sum(len(n["forced"]) for n in nodes),
                      "branch_nodes": sum("branch" in n for n in nodes),
                      "seconds": result["seconds"]}), flush=True)


def replay(constraints, certificate):
    """Independent logical replay using ordinary finite Python sets."""
    rows = [(set(word), [set(a) for a in options])
            for word, options in constraints["constraints"]]
    motifs = constraints["motifs"]
    nodes = certificate["nodes"]
    def decode(raw):
        mask = int(raw, 16)
        assert mask >> len(motifs) == 0
        return {i for i in range(len(motifs)) if mask & (1 << i)}
    for node in nodes:
        state = decode(node["initial"])
        for row in node["forced"]:
            premise, options = rows[row]
            assert premise <= state and len(options) == 1
            state.update(options[0])
        if "reject" in node:
            premise, options = rows[node["reject"]]
            assert premise <= state and not options
        elif "branch" in node:
            premise, options = rows[node["branch"]]
            assert premise <= state
            assert len(node["children"]) == len(options)
            for option, child in zip(options, node["children"]):
                assert decode(nodes[child]["initial"]) == state | option
                assert child != nodes.index(node)
        else:
            state = decode(node["satisfying_alphabet"])
            assert all(not premise <= state or any(o <= state for o in options)
                       for premise, options in rows)
    assert len(certificate["roots"]) == len(motifs)*(len(motifs)-1)//2
    assert [(i,j) for i,j,_ in certificate["roots"]] == list(combinations(range(len(motifs)),2))
    for i, j, child in certificate["roots"]:
        assert decode(nodes[child]["initial"]) == {i,j}
    # Every branch strictly adds a motif, so there is no circular certificate.
    for node in nodes:
        if "children" in node:
            initial = decode(node["initial"])
            for child in node["children"]:
                assert initial < decode(nodes[child]["initial"])


if __name__ == "__main__":
    run("clock33_gain12")
    run("clock24_gain12")
