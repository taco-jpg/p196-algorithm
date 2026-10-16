"""Find a radix-observation two-cycle with a real overflow; not a state cycle.

The deterministic loop stops at the first witness. Its printed source-width
bound is a discovery parameter, not a new exhaustive exterior classification.
"""
from collections import defaultdict
from itertools import product
import json
from pathlib import Path
from explore import step, z


def find():
    for cap in range(1, 5):
        edges = defaultdict(list)
        for c in [6, 12]:
            for width in range(cap + 1):
                for B in product(range(19), repeat=width):
                    if B and (not B[0] or B[-1] == c):
                        continue
                    d, C, gamma = step(c, B)
                    if gamma != 1:
                        continue
                    for t in range(4):
                        e, D, h = step(d, C)
                        u, v = (d, z(d, C)), (e, z(e, D))
                        edge = {"source": [d, C], "target": [e, D],
                                "overflow": h, "overflow_ancestor": [c, B],
                                "steps_after_ancestor_successor": t}
                        edges[u].append((v, edge))
                        opposite = next((w for vv, w in edges[v]
                                         if vv == u and (w["overflow"] or h)), None)
                        if opposite is not None:
                            return {"source_width_bound": cap, "observation": u,
                                    "first_discovered_edge": opposite,
                                    "closing_edge": edge,
                                    "scope": "projected observation cycle only"}
                        d, C = e, D
    return {"status": "NO_WITNESS_WITHIN_THIS_DISCOVERY_DOMAIN"}


if __name__ == "__main__":
    result = find()
    out = Path(__file__).resolve().parents[1] / "evidence/discovery.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))
