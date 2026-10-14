"""An all-length two-step delayed overlap repair, without recurrent closure."""
from __future__ import annotations

import json
from pathlib import Path

from seam_overlap import literal_step, realize
from variable_overlap import shifted_double


DOMAIN = tuple((u, v) for u in range(1, 4) for v in range(5, 8)
               if u+v <= 8)


def component(r, u, v, outside=1):
    return ((outside,) + (0,)*r + (u, v, v, u) + (0,)*r + (outside,))


def control(r, u, v):
    assert r >= 1 and (u, v) in DOMAIN
    a = component(r, u, v)
    q = shifted_double(a, 1)
    ga, gq = literal_step(a), literal_step(q)
    assert ga == tuple(2*x for x in a)
    raw = shifted_double(ga, 1)
    difference = [x-y for x, y in zip(gq, raw)]
    center = len(gq) // 2
    expected = [0] * len(gq)
    expected[center-1:center+2] = [1, -20, 1]
    assert difference == expected
    gga, ggq = literal_step(ga), literal_step(gq)
    target_component = component(r, 4*u+1, 4*v-19, outside=4)
    assert gga == target_component
    assert ggq == shifted_double(target_component, 1)
    assert (4*u+1, 4*v-19) not in DOMAIN

    seed_a, seed_q = realize(a), realize(q)
    comp_value = seed_a + int(str(seed_a)[::-1])
    assert str(comp_value) == str(comp_value)[::-1]
    whole_value = seed_q
    palindrome_times = []
    for t in range(1, 4):
        whole_value += int(str(whole_value)[::-1])
        if str(whole_value) == str(whole_value)[::-1]:
            palindrome_times.append(t)
    assert palindrome_times == ([3] if (u, v) == (1, 5) else [])
    return {"r": r, "u": u, "v": v, "ordinary_seed": str(seed_q),
            "component_successor_is_palindrome": True,
            "whole_first_hit_through_3": 3 if (u, v) == (1, 5) else None,
            "return_component_outer": 4,
            "return_core": [4*u+1, 4*v-19, 4*v-19, 4*u+1],
            "spacer_parameter_after_return": r,
            "immediate_same_gate_reuse": False}


def main():
    cases = [control(r, u, v) for r in tuple(range(1, 65)) + (127, 256)
             for u, v in DOMAIN]
    result = {
        "status": "all-r exact safe two-step delayed repair; no recurrent reset",
        "parameter_domain": {"r": "every integer >=1", "u_v": DOMAIN},
        "independent_literal_controls": len(cases),
        "selected_cases": [c for c in cases if c["r"] in (1, 64)],
        "whole_safe_through_return": True,
        "return_time": 2,
        "intermediate_independent_overlap_fails": True,
        "spacer_growth": 0,
        "all_time_safety": False,
        "finite_Lychrel_witness": False,
        "new_Lean_theorem": False,
    }
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != "selected_cases"}, indent=2))


if __name__ == '__main__':
    main()
