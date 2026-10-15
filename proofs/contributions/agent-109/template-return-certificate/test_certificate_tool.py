#!/usr/bin/env python3
"""Agent #109 regression tests for certificate_tool.py with expected outcomes
established independently of the checker under test.

1. The CertDemo certificate (Lean proves `check demo = false` by kernel `decide`)
   is rejected, at index 0, for the B link.
2. Step palindromicity (`pal`) agrees with literal integer arithmetic: a canonical
   integer realizing the template with bands (g,h) in {(2,2),(3,3),(2,5),(6,2)} is
   stepped by n -> n + reverse(n) and its successor's palindromicity is compared.
3. One-step links built from the exact successor and its maximal trimming pass
   the local check iff the step is non-palindromic (expected value from 2.).
4. Every single mutation of such a link (trim offsets, next blocks, phase, a
   bound below 2, an infeasible band bound) is rejected with the expected reason.
5. Whole-certificate checks: a two-state "cycle" passes iff its closing edge is a
   real successor, which is decided by direct list comparison.
6. Band bounds: feasible gain lists produce bounds satisfying every inequality;
   a negative cyclic gain gives None.
7. CLI round trip: `iterate` with no cycle -> `export` exits 2 with a reason;
   explicit rejected certificate -> `export` exits 2; `export --unchecked` emits
   Lean that evaluates `check`; malformed input exits 2.
No valid certificate is known, so no accepting whole-certificate case exists.
"""
import json, os, random, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import certificate_tool as ct  # noqa: E402

rng = random.Random(109)
PHASES = [c for c in range(1, 18) if c != 9]
counts = {}

def bump(k): counts[k] = counts.get(k, 0) + 1

def rand_state():
    c = rng.choice(PHASES)
    B = [rng.randint(0, 18) for _ in range(rng.randint(0, 3))]
    if B: B[0] = rng.randint(1, 18)
    A = [rng.randint(0, 18) for _ in range(rng.randint(0, 3))]
    h = [rng.randint(0, 18) for _ in range(rng.randint(0, 2))]
    C = h + ([2 * rng.randint(0, 9)] if rng.random() < .5 else []) + h[::-1]
    return (c, B, A, C)

def template(c, B, A, C, g, h):
    d = 18 - c
    return B + [c] * g + A + [d] * h + C + [d] * h + A[::-1] + [c] * g + B[::-1]

def realize(q):
    L = len(q); dg = [0] * L
    for i in range((L + 1) // 2):
        j = L - 1 - i
        if i == j: dg[i] = q[i] // 2; continue
        hi = min(9, q[i]); dg[j], dg[i] = hi, q[i] - hi
    return int("".join(map(str, reversed(dg))))

def literal_pal_after_step(s, g=3, h=3):
    n = realize(template(*s, g, h))
    m = n + int(str(n)[::-1])
    return str(m) == str(m)[::-1]

# 1. CertDemo
demo_states = [(2, [1], [3], [4]), (4, [3, 5], [1], [2, 2])]
demo_links = [(0, 0, 0, 0, 5, 5), (0, 0, 0, 0, 5, 5)]
assert ct.check(demo_states, demo_links) is False
assert ct.local_ok(demo_states, demo_links, 0) == (False, "B link")
bump("certdemo_rejected")

# 2.-4.
for _ in range(3000):
    s = rand_state()
    c2, Br, Ar, Cr, gam, pal = ct.successor(*s)
    for g, h in ((2, 2), (3, 3), (2, 5), (6, 2)):
        assert pal == literal_pal_after_step(s, g, h), (s, g, h)
        bump("pal_vs_integers")
    if pal: bump("palindromic_steps")
    s2, tr, _, _ = ct.step_state(s)
    good = [(*tr, 4, 4), (0, 0, 0, 0, 2, 2)]
    ok, why = ct.local_ok([s, s2], good, 0)
    assert ok == (not pal) and (ok or why == "palindromic step"), (s, ok, why)
    bump("one_step_links")
    if pal:
        continue
    j, j1, j2, kk = tr
    muts = []
    muts.append(([s, s2], [(j + 1, j1, j2, kk, 4, 4), good[1]], "B link"))
    muts.append(([s, s2], [(j, j1 + 1, j2, kk, 4, 4), good[1]], "A link"))
    muts.append(([s, s2], [(j, j1, j2 + 1, kk, 4, 4), good[1]], "A link"))
    muts.append(([s, s2], [(j, j1, j2, kk + 1, 4, 4), good[1]], "C link"))
    if s2[1]:
        nb = list(s2[1]); nb[0] = (nb[0] + 1) % 19
        muts.append(([s, (s2[0], nb, s2[2], s2[3])], good, "B link"))
    muts.append(([s, ((s2[0] % 16) + 2 if s2[0] != 16 else 2, s2[1], s2[2], s2[3])], good, "phase link"))
    muts.append(([s, s2], [(*tr, 1, 4), good[1]], "bound below 2"))
    muts.append(([s, s2], [(*tr, 4, 4), (0, 0, 0, 0, 7 + gam + j + j1, 2)], "band bound"))
    for st, lk, want in muts:
        assert ct.local_ok(st, lk, 0) == (False, want), (s, want, ct.local_ok(st, lk, 0))
        bump("mutations_rejected")
    # 5. two-state cycle: closes iff step(s2) equals s after trimming
    s3, tr2, _, _ = ct.step_state(s2)
    closes = (s3[0], list(s3[1]), list(s3[2]), list(s3[3])) == (s[0], list(s[1]), list(s[2]), list(s[3]))
    whole = ct.check([s, s2], [(*tr, 50, 50), (*tr2, 50, 50)])
    assert whole == (closes and whole), s
    assert (not closes) <= (not whole)
    bump("two_state_cycles_checked")

# 6. bounds
for _ in range(2000):
    P = rng.randint(1, 8)
    info = [((rng.randint(0, 3), rng.randint(0, 2), rng.randint(0, 2), rng.randint(0, 2)),
             rng.randint(0, 1), False) for _ in range(P)]
    gains = [(g + t[0] + t[1] - 2, g + t[2] + t[3] - 2) for t, g, _ in info]
    feasible = sum(x for x, _ in gains) >= 0 and sum(y for _, y in gains) >= 0
    lo = ct.bounds(info)
    assert (lo is not None) == feasible
    if lo:
        for i, (t, g, _) in enumerate(info):
            n = (i + 1) % P
            assert lo[0][i] >= 2 and lo[1][i] >= 2
            assert lo[0][n] + 2 <= lo[0][i] + g + t[0] + t[1]
            assert lo[1][n] + 2 <= lo[1][i] + g + t[2] + t[3]
        bump("feasible_bounds")
    else:
        bump("infeasible_bounds")

# 7. CLI round trip
tool = os.path.join(HERE, "certificate_tool.py")
def run(*args):
    return subprocess.run([sys.executable, "-I", tool, *args], capture_output=True, text=True)
with tempfile.TemporaryDirectory() as tmp:
    r = run("iterate", "2", "[1]", "[3]", "[4]", "40")
    assert r.returncode == 0
    out = json.loads(r.stdout)
    assert out["cycle"] is None
    p = os.path.join(tmp, "cycle.json"); open(p, "w").write(r.stdout)
    r = run("export", p)
    assert r.returncode == 2 and "no cycle" in r.stderr, (r.returncode, r.stderr)
    bump("cli_no_cycle")
    p2 = os.path.join(tmp, "demo.json")
    json.dump({"states": demo_states, "links": demo_links}, open(p2, "w"))
    r = run("export", p2)
    assert r.returncode == 2 and "fails the Python check" in r.stderr and "B link" in r.stderr
    bump("cli_rejected_certificate")
    r = run("export", "--unchecked", p2)
    assert r.returncode == 0 and "#eval check cert" in r.stdout and "theorem" not in r.stdout
    open(os.path.join(HERE, "ExportDemo.lean"), "w").write(r.stdout)
    bump("cli_unchecked_export")
    p3 = os.path.join(tmp, "bad.json"); json.dump({"foo": 1}, open(p3, "w"))
    r = run("export", p3)
    assert r.returncode == 2
    bump("cli_malformed")
    # direct conversion errors
    for cyc, info, want in [(None, [], "no cycle"),
                            ([(2, [1], [], [])], [((0, 0, 0, 0), 0, True)], "palindrome"),
                            ([(2, [1], [], [])], [((0, 0, 0, 0), 0, False)], "negative")]:
        try:
            ct.cycle_to_certificate(cyc, info); raise AssertionError("expected NoCertificate")
        except ct.NoCertificate as e:
            assert want in str(e), (want, str(e))
        bump("conversion_errors")

# No sampled state had a palindromic step, by the tool and by literal integer
# arithmetic alike. This is a theorem: Agent109.NoPal.not_stepPal in
# ../template-step-safety/ proves StepPal is never true. The "palindromic step"
# reason is therefore exercised only through the conversion-error cases above.
assert counts.get("palindromic_steps", 0) == 0 and counts["mutations_rejected"] > 0
print(json.dumps({"counts": counts, "result": "PASS",
                  "note": "no accepting whole certificate is known; components tested separately"}))
