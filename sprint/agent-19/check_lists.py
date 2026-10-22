#!/usr/bin/env python3
"""Agent 19 review: parse the explicit prefix lists of the reviewed results from the
Lean sources and check them for vacuous entries (leading zero, digit > 9, empty),
duplicates, the noOverflowPre condition, and bound + 1 <= 100.
Usage: python3 sprint/agent-19/check_lists.py   (run from the repository root)"""
import re, ast, sys, collections
ROOT = "lean/P196/"

def lean_list(src, name):
    m = re.search(r"def %s\s*:\s*List \(List Nat × Nat\)\s*:=\s*(\[.*?\])\n" % re.escape(name), src, re.S)
    if not m:
        return None
    txt = m.group(1).replace("(", "[").replace(")", "]")
    return [(tuple(a), b) for a, b in ast.literal_eval(txt)]

def no_overflow_pre(pre):
    return (pre[0] >= 2) or any(d >= 3 for d in pre)

def validate(entries, label):
    bad = []
    for pre, b in entries:
        if len(pre) == 0 or pre[0] == 0 or any(d > 9 for d in pre):
            bad.append(("invalid-digits", pre))
        if not no_overflow_pre(pre):
            bad.append(("noOverflowPre-false", pre))
        if b + 1 > 100:
            bad.append(("bound>99", pre, b))
    c = collections.Counter(p for p, _ in entries)
    dups = [p for p, n in c.items() if n > 1]
    return bad, dups

def main():
    out = {}
    total = []
    for cert, k in (("F4", 4), ("F5", 5)):
        src = open(ROOT + "Agent124FourDigit/A124%sEntries.lean" % cert).read()
        names = sorted(set(re.findall(r"def (entries\d\d)\s*:", src)))
        allc = []
        for n in names:
            e = lean_list(src, n)
            allc += e
        bad, dups = validate(allc, cert)
        lens = collections.Counter(len(p) for p, _ in allc)
        maxb = max(b for _, b in allc)
        print(f"{cert} (k={k}): chunks={len(names)} entries={len(allc)} lengths={dict(lens)} "
              f"max rank bound={maxb} (=> max ancestry bound {maxb+1}) invalid={len(bad)} duplicates={len(dups)}")
        for x in bad[:10]:
            print("   BAD", x)
        total += [(p, b, cert) for p, b in allc]
        out[cert] = allc
    allp = [p for p, _, _ in total]
    both = set(p for p, _ in out["F4"]) & set(p for p, _ in out["F5"])
    print(f"F4+F5: {len(allp)} entries, {len(set(allp))} distinct prefixes, in both F4 and F5: {len(both)}")
    # prefixes that are refinements of what three-digit word
    parents = collections.Counter(p[:3] for p in set(allp))
    print(f"distinct 3-digit parents of the F4/F5 prefixes: {len(parents)}")
    return out

if __name__ == "__main__":
    main()
