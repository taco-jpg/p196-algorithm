"""Finite variable-clock search with two active neutral-nine bands.

State (B,H) stands for B 9^g H 9^g reverse(B).  Both bands must have
opposite incoming carries from their two ends.  The middle and exterior
are allowed to change; clocks are computed from the actual whole word.
The transition is symbolic in g. The finite graph is exhaustive only for
the stated initial interface family, not for arbitrary B or H.
"""
from __future__ import annotations

from collections import Counter
import gzip
import hashlib
import itertools
import json
from pathlib import Path

from seam_transport import normalize, pair_step, nine_runs, maximal_mask

HERE = Path(__file__).resolve().parent
GAP_CONTROLS = (2, 3, 64)


def assemble(state, gap):
    b, h = state
    return b + (9,) * gap + h + (9,) * gap + b[::-1]


def mixed(state):
    b, h = state
    e = normalize(b)[1][-1]
    return normalize(h, e)[1][-1] == 1 - e


def transition(state):
    b, h = state
    assert h and h[0] != 9
    assert not b or (b[0] > 0 and b[-1] != 9)
    assert h == h[::-1] and (len(h) % 2 == 0 or h[len(h) // 2] % 2 == 0)
    assert mixed(state)
    db, ab = normalize(b)
    e = ab[-1]
    dh, ah = normalize(h, e)
    dr, ar = normalize(b[::-1], ah[-1])
    gamma = ar[-1]
    x, y = 9 * (1 - e), 9 * e
    if gamma:
        raw_b = tuple(v + w for v, w in zip(db + (x,), (1,) + dr[::-1]))
        core_digits = dh + (y,)
    else:
        raw_b = tuple(v + w for v, w in zip(db, dr[::-1]))
        core_digits = dh
    raw_h = tuple(v + w for v, w in zip(core_digits, core_digits[::-1]))
    for gap in GAP_CONTROLS:
        q = assemble(state, gap)
        raw_out = raw_b + (9,) * (gap - gamma) + raw_h + (9,) * (gap - gamma) + raw_b[::-1]
        assert pair_step(q) == raw_out
    if all(z == 9 for z in raw_h):
        return {"kind": "bands_merged", "gamma": gamma,
                "raw_outer": raw_b, "raw_middle": raw_h}
    u = 0
    while u < len(raw_b) and raw_b[len(raw_b) - 1 - u] == 9:
        u += 1
    v = 0
    while raw_h[v] == 9:
        v += 1
    assert raw_h[-1 - v] != 9 and 2 * v < len(raw_h)
    target = (raw_b[:len(raw_b) - u], raw_h[v:len(raw_h) - v])
    delta = u + v - gamma
    for gap in GAP_CONTROLS:
        assert pair_step(assemble(state, gap)) == assemble(target, gap + delta)
    assert 2 * len(target[0]) + len(target[1]) + 2 * delta == 2 * len(b) + len(h) + gamma
    if not mixed(target):
        return {"kind": "mixed_carry_lost", "gamma": gamma,
                "target": target, "gap_delta": delta}
    assert any(maximal_mask(assemble(target, 2 + delta)))
    return {"kind": "edge", "gamma": gamma, "target": target, "gap_delta": delta}


def seeds():
    for width in (1, 2):
        for outside in range(1, 19):
            for suffix in itertools.product(range(19), repeat=width - 1):
                b = (outside,) + suffix
                if b[-1] == 9:
                    continue
                for h in range(0, 19, 2):
                    state = (b, (h,))
                    if mixed(state):
                        yield state


def main():
    graph, paths, cycles = {}, [], []
    initials = tuple(seeds())
    for initial in initials:
        state = initial
        positions, path = {}, []
        while True:
            if state in positions:
                loop = path[positions[state]:]
                cycles.append({"initial": initial, "loop": loop,
                               "gap_gain": sum(graph[s]["gap_delta"] for s in loop),
                               "overflow_count": sum(graph[s]["gamma"] for s in loop)})
                break
            positions[state] = len(path)
            path.append(state)
            if state not in graph:
                result = transition(state)
                graph[state] = result
            result = graph[state]
            if result["kind"] != "edge":
                break
            state = result["target"]
        running_delta = 0
        minimum_delta = 0
        for visited in path:
            running_delta += graph[visited].get("gap_delta", 0)
            minimum_delta = min(minimum_delta, running_delta)
        paths.append({"initial": initial, "steps": len(path),
                      "terminal_kind": "cycle" if state in positions and result["kind"] == "edge" else result["kind"],
                      "final_state": state,
                      "initial_gap_for_all_tracked_gaps_at_least_two": 2 - minimum_delta})
    for cycle in cycles:
        assert 2 * cycle["gap_gain"] == cycle["overflow_count"]
    records = [{"state": state, **result} for state, result in sorted(graph.items())]
    payload = json.dumps({"graph": records, "paths": paths, "cycles": cycles},
                         sort_keys=True, separators=(",", ":")).encode()
    (HERE / "neutral_quotient_controls.json.gz").write_bytes(gzip.compress(payload, mtime=0))
    counts = Counter(r["kind"] for r in graph.values())
    summaries = Counter(p["terminal_kind"] for p in paths)
    summary = {"status": "exact symbolic variable-clock graph from the stated initial family; no arbitrary-interface exclusion claimed",
               "initial_outer_widths": [1, 2], "initial_middle": "one even coefficient0..18",
               "maximum_outer_width_reached": max(len(s[0]) for s in graph),
               "maximum_middle_width_reached": max(len(s[1]) for s in graph),
               "gap_controls": GAP_CONTROLS, "initial_states": len(initials),
               "distinct_states": len(graph), "transition_counts": dict(counts),
               "seed_terminal_counts": dict(summaries), "cycles": cycles,
               "longest_path_steps": max(p["steps"] for p in paths),
               "sufficient_initial_gap_for_every_seed": max(p["initial_gap_for_all_tracked_gaps_at_least_two"] for p in paths),
               "longest_path": max(paths, key=lambda p: p["steps"]),
               "archive_payload_sha256": hashlib.sha256(payload).hexdigest()}
    (HERE / "neutral_quotient_results.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
