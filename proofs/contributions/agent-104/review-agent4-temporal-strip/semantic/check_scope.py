#!/usr/bin/env python3
"""Small independent finite controls. These are diagnostics, not Lean proofs."""
import hashlib
import itertools
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
COMMIT = "5bd98567b259659fd3195f5aa61617422aa80914"
SOURCE = "proofs/agent4/temporal_strip/NoAlternatingReturn.lean"
SOURCE_SHA = "49b1065166c02c2efd1bf58c3391c5166b44106f12e82af371304e9fe3ae7ba0"


def pinned(path):
    return subprocess.check_output(["git", "show", COMMIT + ":" + path], cwd=REPO)


def valid(c):
    return all(0 <= a <= 1 for a in c[:4]) and 0 <= c[4] <= 9


def left(c):
    le, lo, he, ho, d = c
    return le == he == 0 and ho == 1 and d + lo == 4


def right(c):
    le, lo, he, ho, d = c
    return le == he == 1 and ho == 0 and d + lo == 6


def column(s, t, x, y, xnext):
    a, b, u, v, d = s
    aa, bb, uu, vv, dd = t
    return {
        "coefficient_bounds": 0 <= x <= 18 and 0 <= y <= 18,
        "low_even": aa == (x + a) // 10,
        "low_odd": bb == (y + b) // 10,
        "high_even": u == (x + uu) // 10,
        "high_odd": v == (y + vv) // 10,
        "delayed": dd == (y + vv) % 10,
        "even_to_odd": y == (x + a) % 10 + (x + uu) % 10,
        "odd_to_next_even": xnext == (y + b) % 10 + d,
    }


def scalar_controls():
    found = {"left": [], "right": []}
    tested = 0
    for x, y in itertools.product(range(19), repeat=2):
        for a, b, r, u, v in itertools.product(range(2), repeat=5):
            tested += 1
            if ((x+a)//10 == 0 and (y+b)//10 == r and x//10 == u
                    and (y+1)//10 == v and (y+1)%10+r == 4
                    and y == (x+a)%10+x%10):
                assert (r,x,y,a,u,v) in [(0,1,3,1,0,0),(1,6,12,0,0,1)]
                found["left"].append([x,y,a,b,r,u,v])
            if ((x+a)//10 == 1 and (y+b)//10 == r and (x+1)//10 == u
                    and y//10 == v and y%10+r == 6
                    and y == (x+a)%10+(x+1)%10):
                assert (r,x,y,a,u,v) in [(0,12,6,1,1,0),(1,17,15,0,1,1)]
                found["right"].append([x,y,a,b,r,u,v])
    assert tested == 11552
    assert len(found["left"]) == len(found["right"]) == 4
    return {"tuples_tested_per_classifier": tested,
            "tuple_order": ["x","y","a","b","r","u","v"],
            "satisfying_tuples": found}


def scope_controls():
    stationary = []
    for c, x, y, aligned in [((0,1,0,1,3),6,12,left),
                              ((1,0,1,0,6),12,6,right)]:
        checks = column(c,c,x,y,x)
        assert valid(c) and aligned(c) and all(checks.values())
        stationary.append({"cut": c, "x": x, "y": y, "checks": checks})
    open_time = []
    for j in range(3):
        s = (1,0,0,0,3) if j == 0 else (0,0,0,1,4)
        t = (0,0,0,1,4) if j == 0 else (0,1,0,1,3)
        x, y = (1,3) if j == 0 else (6,12)
        checks = column(s,t,x,y,6)
        assert valid(s) and valid(t) and left(t) and all(checks.values())
        assert left(s) == (j != 0)
        open_time.append({"alignment":"left", "j":j, "source":s,
                          "target":t, "checks":checks})
        s = (0,0,1,1,7) if j == 0 else (1,0,1,0,6)
        t = (1,1,1,0,5) if j == 0 else (1,0,1,0,6)
        x, y = (17,15) if j == 0 else (12,6)
        checks = column(s,t,x,y,12)
        assert valid(s) and valid(t) and right(t) and all(checks.values())
        assert right(s) == (j != 0)
        open_time.append({"alignment":"right", "j":j, "source":s,
                          "target":t, "checks":checks})
    return {"stationary_interior": stationary, "open_time_finite_controls": open_time,
            "open_time_scope": "Finite branch controls only. Universal Nat fixtures are separately supplied as uncompiled Lean examples."}


def pair(n):
    digits = [int(d) for d in reversed(str(n))]
    return [a+b for a,b in zip(digits,reversed(digits))]


def carry_digits(q):
    c, out = [0], []
    for a in q:
        z = a + c[-1]
        out.append(z % 10)
        c.append(z // 10)
    return c, out


def actual_control():
    step = lambda n: n + int(str(n)[::-1])
    nums = [15]
    nums.extend([step(nums[0])])
    nums.extend([step(nums[1])])
    assert nums == [15,66,132]
    words = list(map(pair,nums))
    assert words == [[6,6],[12,12],[3,6,3]]
    ce, de = carry_digits(words[0])
    co, do = carry_digits(words[1])
    assert ce[-1] == 0 and co[-1] == 1
    cuts = [(ce[i],co[i],ce[2-i],co[2-i],co[-1] if i == 0 else do[2-i])
            for i in [0,1]]
    assert cuts == [(0,0,0,1,1),(0,1,0,1,3)]
    assert left(cuts[1])
    cyclic = column(cuts[0],cuts[1],6,12,6)
    actual = column(cuts[0],cuts[1],6,12,3)
    assert not cyclic["odd_to_next_even"]
    assert all(v for k,v in cyclic.items() if k != "odd_to_next_even")
    assert all(actual.values())
    return {"numbers":nums,"pair_words":words,"overflow":[ce[-1],co[-1]],
            "cuts_at_0_and_1":cuts,"cyclic_column_checks":cyclic,
            "actual_open_column_checks":actual,
            "conclusion":"Actual alternation and aligned 6/12 columns do not imply cyclic temporal closure."}


def main():
    source = pinned(SOURCE)
    assert hashlib.sha256(source).hexdigest() == SOURCE_SHA
    report = {"status":"PASS_FINITE_DIAGNOSTICS_ONLY", "source_commit":COMMIT,
              "source_path":SOURCE,"source_sha256":SOURCE_SHA,
              "scalar_classifications":scalar_controls(),
              "scope_controls":scope_controls(),
              "ordinary_finite_scope_control":actual_control(),
              "lean_executed_by_this_script":False,
              "actual_map_bridge_established":False}
    (HERE / "diagnostics.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"], "scalar_tuples":11552,
                      "ordinary_control":report["ordinary_finite_scope_control"]["numbers"]}))


if __name__ == "__main__":
    main()
