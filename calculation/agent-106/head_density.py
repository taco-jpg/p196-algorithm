#!/usr/bin/env python3
"""Finite certificate for the neutral decimal B first-coordinate density bound.

Run from the repository root:
    python3 calculation/agent-106/head_density.py

This checks 36 labeled transitions on x=1,...,18. It proves a statement
about their finite projection. The paper argument must separately explain
why a padded A120 B-cycle projects to these edges.

No search over B width or temporal period occurs here.
"""

from collections import Counter


# A feasible integer potential, with R(y)-R(x) >= 2*g-1 on every edge.
POTENTIAL = (0, 3, 2, 2, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0)


def edges():
    """(source coefficient, inner carry, overflow, target coefficient)."""
    for x in range(1, 19):
        for h in (0, 1):
            g = (x + h) // 10
            y = 2 * x + h if g == 0 else x % 10 + 1
            assert 1 <= y <= 18
            yield x, h, g, y


def slack(edge):
    x, _, g, y = edge
    return POTENTIAL[y] - POTENTIAL[x] - (2 * g - 1)


def cyclic_components(relation):
    """Independent transitive-closure classification on only 18 vertices."""
    reach = {x: {x} for x in range(1, 19)}
    for x, _, _, y in relation:
        reach[x].add(y)
    for k in range(1, 19):
        for x in range(1, 19):
            if k in reach[x]:
                reach[x].update(reach[k])
    components = {
        tuple(y for y in range(1, 19) if y in reach[x] and x in reach[y])
        for x in range(1, 19)
    }
    loops = {x for x, _, _, y in relation if x == y}
    return sorted(c for c in components if len(c) > 1 or c[0] in loops)


def main():
    relation = list(edges())
    assert len(relation) == 36
    assert all(slack(edge) >= 0 for edge in relation)
    tight = [edge for edge in relation if slack(edge) == 0]
    components = cyclic_components(tight)
    assert components == [(8, 17), (9, 18)]
    cycle_edges = [edge for edge in tight
                   if any(edge[0] in c and edge[3] in c for c in components)]
    expected = {
        (8, 1, 0, 17), (17, 0, 1, 8), (17, 1, 1, 8),
        (9, 0, 0, 18), (18, 0, 1, 9), (18, 1, 1, 9),
    }
    assert set(cycle_edges) == expected
    print("HEAD_DENSITY_CHECK PASSED")
    print(f"vertices=18 labeled_edges={len(relation)} tight_edges={len(tight)}")
    print("slack_histogram=" + str(dict(sorted(Counter(map(slack, relation)).items()))))
    print("potential=" + str(list(POTENTIAL[1:])))
    print("tight_cyclic_components=" + str(components))
    print("tight_cycle_edges=" + str(cycle_edges))
    print("projection_conclusion: 2*sum(g)<=P")
    print("equality_conclusion: P even; g alternates; x alternates 8,17 or 9,18")


if __name__ == "__main__":
    main()
