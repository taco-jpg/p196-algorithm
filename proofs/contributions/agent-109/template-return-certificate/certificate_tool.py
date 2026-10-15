#!/usr/bin/env python3
"""Agent #109 complementary-template return-certificate tool (independent of Lean).

Implements the exact symbolic successor (identity (8), blocks (6)/(7)), maximal
trimming, cycle detection, band lower bounds, a Python mirror of the Lean
checker `Agent109.Cert.check`, and export of a certificate as Lean source that
`ReturnCertificate.lean` can check with kernel `decide`.

  python3 certificate_tool.py selftest
  python3 certificate_tool.py iterate C B A Cc STEPS > cycle.json   (lists as JSON, e.g. '[1]')
  python3 certificate_tool.py export cycle.json > Instance.lean
  python3 certificate_tool.py export --unchecked cert.json > Probe.lean

`export` accepts either the `iterate` output ({"cycle": [...], "info": [...]}) or an
explicit certificate ({"states": [...], "links": [...]}). It converts a cycle into
links with minimal feasible band bounds, re-checks the certificate with the Python
mirror of `check`, and exits with status 2 and a reason on stderr when there is no
cycle, a step is palindromic, the gap gains are negative, or the check fails.
`--unchecked` emits Lean for an explicit certificate without the Python check (for
probing rejected certificates; the emitted file then evaluates `check` instead of
claiming a theorem). `test_certificate_tool.py` holds the regression tests.

No certificate instance is known; this tool only formats/checks candidates.
"""
import json, os, sys

def k(x): return 1 if x >= 10 else 0
def t(x): return x - 9 * k(x)
def phase(x): return 1 <= x <= 17 and x != 9
def bounded(w): return all(x <= 18 for x in w)

def norm(w, e):
    out = []
    for x in w:
        out.append((x + e) % 10); e = (x + e) // 10
    return out, e

def zadd(a, b):
    assert len(a) == len(b); return [x + y for x, y in zip(a, b)]

def pair(w): return zadd(w, w[::-1])

def successor(c, B, A, C):
    """(c', B_r, A_r, C_r, gamma) with g,h -> g-2+gamma, h-2+gamma."""
    d = 18 - c
    DB, e0 = norm(B, 0); DA, e1 = norm(A, k(c)); DC, e2 = norm(C, k(d))
    DRA, e3 = norm(A[::-1], k(d)); DRB, gam = norm(B[::-1], k(c))
    u0 = c + e0 - 10 * k(c); u1 = d + e1 - 10 * k(d)
    u2 = d + e2 - 10 * k(d); u3 = c + e3 - 10 * k(c)
    if gam == 0:
        Br = zadd(DB + [u0], DRB[::-1] + [t(c)])
        Ar = zadd([t(c)] + DA + [u1], [u3] + DRA[::-1] + [t(d)])
        Cr = pair([t(d)] + DC + [u2])
        pal = (([t(c)] + DRB)[::-1] == DB + [u0] and
               ([t(d)] + DRA + [u3])[::-1] == [t(c)] + DA + [u1] and
               ([t(d)] + DC + [u2])[::-1] == [t(d)] + DC + [u2])
    else:
        Br = zadd(DB + [u0], [1] + DRB[::-1])
        Ar = zadd(DA + [u1], [u3] + DRA[::-1])
        Cr = pair(DC + [u2])
        pal = ((DRB + [1])[::-1] == DB + [u0] and (DRA + [u3])[::-1] == DA + [u1]
               and (DC + [u2])[::-1] == DC + [u2])
    return 2 * t(c), Br, Ar, Cr, gam, pal

def lead(w, x):
    n = 0
    while n < len(w) and w[n] == x: n += 1
    return n

def trim(c, B, A, C):
    """Maximal trimming; returns (state, (j, j1, j2, kk))."""
    d = 18 - c
    j = lead(B[::-1], c); B2 = B[:len(B) - j]
    j1 = lead(A, c); A2 = A[j1:]
    j2 = lead(A2[::-1], d); A2 = A2[:len(A2) - j2]
    kk = min(lead(C, d), lead(C[::-1], d), len(C) // 2)
    C2 = C[kk:len(C) - kk]
    assert B2 + [c] * j == B and [c] * j1 + A2 + [d] * j2 == A
    assert [d] * kk + C2 + [d] * kk == C
    return (c, B2, A2, C2), (j, j1, j2, kk)

def step_state(s):
    c2, Br, Ar, Cr, gam, pal = successor(*s)
    s2, tr = trim(c2, Br, Ar, Cr)
    return s2, tr, gam, pal

def key(s): return json.dumps(s)

def find_cycle(s0, steps):
    seen = {key(s0): 0}; path = [s0]; info = []
    s = s0
    for i in range(steps):
        s2, tr, gam, pal = step_state(s)
        info.append((tr, gam, pal)); path.append(s2)
        if key(s2) in seen:
            a = seen[key(s2)]
            return path[a:-1], info[a:]
        seen[key(s2)] = i + 1; s = s2
    return None, None

def bounds(info):
    """Minimal lo, lo' (>=2) with lo[i+1]+2 <= lo[i]+gam+j+j1 (cyclic); None if infeasible."""
    P = len(info)
    out = []
    for which in (0, 1):
        inc = [gam + (tr[0] + tr[1] if which == 0 else tr[2] + tr[3]) - 2
               for tr, gam, _ in info]
        if sum(inc) < 0: return None
        # lo[i+1] <= lo[i] + inc[i]; choose lo[0] = L large, propagate minima.
        pref = [0]
        for x in inc: pref.append(pref[-1] + x)
        L = 2 - min(pref[:P])            # ensures every lo >= 2
        lo = [L + pref[i] for i in range(P)]
        out.append(lo)
    return out

def local_ok(states, links, i):
    """Index-i conjunct of Agent109.Cert.LocalOK; returns (ok, reason)."""
    P = len(states)
    s = states[i]; s2 = states[(i + 1) % P]; L = links[i]; L2 = links[(i + 1) % P]
    c, B, A, C = s
    if not (phase(c) and bounded(B) and bounded(A) and bounded(C)): return False, "phase/bounds"
    c2, Br, Ar, Cr, gam, pal = successor(c, B, A, C)
    j, j1, j2, kk, lo, lo2 = L
    if c2 != s2[0]: return False, "phase link"
    if Br != list(s2[1]) + [s2[0]] * j: return False, "B link"
    if Ar != [s2[0]] * j1 + list(s2[2]) + [18 - s2[0]] * j2: return False, "A link"
    if Cr != [18 - s2[0]] * kk + list(s2[3]) + [18 - s2[0]] * kk: return False, "C link"
    if pal: return False, "palindromic step"
    if not (lo >= 2 and lo2 >= 2): return False, "bound below 2"
    if not (L2[4] + 2 <= lo + gam + j + j1 and L2[5] + 2 <= lo2 + gam + j2 + kk):
        return False, "band bound"
    return True, "ok"

def check(states, links):
    """Python mirror of Agent109.Cert.check."""
    if len(states) == 0 or len(links) != len(states): return False
    return all(local_ok(states, links, i)[0] for i in range(len(states)))

class NoCertificate(Exception):
    pass

def cycle_to_certificate(cycle, info):
    """Turn `find_cycle` output into (states, links); raise NoCertificate otherwise."""
    if not cycle:
        raise NoCertificate("no cycle in the input (iterate found none within its step bound)")
    if len(info) != len(cycle):
        raise NoCertificate("cycle/info length mismatch")
    for i, (tr, gam, pal) in enumerate(info):
        if pal:
            raise NoCertificate(f"step {i} of the cycle reaches a palindrome")
    lo = bounds(info)
    if lo is None:
        raise NoCertificate("a cyclic gap gain is negative: no feasible band bounds")
    states = [(c, list(B), list(A), list(C)) for c, B, A, C in cycle]
    links = [(*tuple(tr), lo[0][i], lo[1][i]) for i, (tr, gam, pal) in enumerate(info)]
    if not check(states, links):
        raise NoCertificate("converted certificate fails the Python check")
    return states, links

def lean_list(w): return "[" + ", ".join(str(x) for x in w) + "]"

def export(states, links, name="cert", checked=True):
    ss = ",\n    ".join(f"⟨{c}, {lean_list(B)}, {lean_list(A)}, {lean_list(C)}⟩"
                       for c, B, A, C in states)
    ls = ",\n    ".join("⟨" + ", ".join(str(x) for x in L) + "⟩" for L in links)
    head = (f"import ReturnCertificate\nopen Agent109.Cert\n\n"
            f"def {name} : Certificate :=\n  {{ states := [\n    {ss}],\n"
            f"    links := [\n    {ls}] }}\n\n")
    if checked:
        return head + f"theorem {name}_valid : check {name} = true := by decide\n"
    return head + f"#eval check {name}\n"

def selftest():
    """Smoke test; the expected-outcome regression suite is test_certificate_tool.py."""
    import subprocess
    here = os.path.dirname(os.path.abspath(__file__))
    r = subprocess.run([sys.executable, "-I", os.path.join(here, "test_certificate_tool.py")],
                       capture_output=True, text=True)
    sys.stdout.write(r.stdout); sys.stderr.write(r.stderr)
    sys.exit(r.returncode)

def main(argv):
    cmd = argv[1]
    if cmd == "selftest":
        selftest()
    elif cmd == "iterate":
        s = (int(argv[2]), json.loads(argv[3]), json.loads(argv[4]), json.loads(argv[5]))
        cyc, info = find_cycle(s, int(argv[6]))
        print(json.dumps({"cycle": cyc, "info": info}))
    elif cmd == "export":
        unchecked = "--unchecked" in argv
        path = [a for a in argv[2:] if a != "--unchecked"][0]
        d = json.load(open(path))
        try:
            if "cycle" in d:
                if unchecked:
                    raise NoCertificate("--unchecked applies only to explicit states/links input")
                states, links = cycle_to_certificate(d["cycle"], d.get("info") or [])
            elif "states" in d and "links" in d:
                states = [tuple(x) for x in d["states"]]; links = [tuple(x) for x in d["links"]]
                if not unchecked and not check(states, links):
                    bad = [(i, local_ok(states, links, i)[1]) for i in range(len(states))
                           if len(links) == len(states) and not local_ok(states, links, i)[0]]
                    raise NoCertificate(f"certificate fails the Python check: {bad}")
            else:
                raise NoCertificate("input has neither cycle/info nor states/links")
        except NoCertificate as e:
            print(f"export: no certificate: {e}", file=sys.stderr)
            sys.exit(2)
        print(export(states, links, checked=not unchecked), end="")
    else:
        print(__doc__, file=sys.stderr); sys.exit(1)

if __name__ == "__main__":
    main(sys.argv)
