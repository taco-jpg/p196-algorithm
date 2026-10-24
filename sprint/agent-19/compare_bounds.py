#!/usr/bin/env python3
"""Agent 19 review: compare forward-scan maxima (output of scan.c) with every ancestry
bound stated by the reviewed results. A scan time above a proved bound would mean the
Lean statement does not say what the Python model of reverse-and-add says.
Usage: python3 sprint/agent-19/compare_bounds.py scan_out1.txt [scan_out2.txt ...]"""
import sys, re, os
sys.path.insert(0, os.path.dirname(__file__))
from check_lists import lean_list

def load_scan(paths):
    p3, p4 = {}, {}
    for path in paths:
        for line in open(path):
            f = line.split()
            if f[0] in ("P3", "P4"):
                d = p3 if f[0] == "P3" else p4
                key, t, seed = f[1], int(f[2]), int(f[3])
                if key not in d or t > d[key][0]:
                    d[key] = (t, seed)
    return p3, p4

def claims():
    """(prefix string, proved bound on t, source)"""
    out = [("217", 23, "Agent118 ancestry_bound23"), ("218", 34, "Agent118 ancestry_bound34"),
           ("777", 25, "Agent118 ancestry_bound25"), ("620", 12, "Agent124Prefix620 ancestry_620"),
           ("739", 39, "Agent104Prefix739 ancestry_bound39"), ("2641", 6, "Agent117P2641 ancestry_2641")]
    src = open("lean/P196/Agent124PrefixFiveSix/Agent124PrefixSummary.lean").read()
    for a, b, c, B in re.findall(r"\((\d), (\d), (\d), (\d+)\)", src):
        out.append((a + b + c, int(B), "Agent124PrefixFiveSix ancestry_all"))
    for cert in ("F4", "F5"):
        s = open("lean/P196/Agent124FourDigit/A124%sEntries.lean" % cert).read()
        for n in sorted(set(re.findall(r"def (entries\d\d)\s*:", s))):
            for pre, b in lean_list(s, n):
                out.append(("".join(map(str, pre)), b + 1, "Agent124FourDigit %s.ancestry_%s" % (cert, n[-2:])))
    return out

def main():
    p3, p4 = load_scan(sys.argv[1:])
    viol, seen, tight = [], 0, []
    for pre, bound, srcname in claims():
        d = p3 if len(pre) == 3 else p4
        if pre in d:
            seen += 1
            t, seed = d[pre]
            if t > bound:
                viol.append((pre, t, seed, bound, srcname))
            if t == bound:
                tight.append((pre, t, seed, srcname))
    print(f"claims checked: {len(claims())}; prefixes reached by the scan: {seen}; violations: {len(viol)}")
    for v in viol:
        print("VIOLATION", v)
    print(f"bounds attained exactly by the scan: {len(tight)}")
    for x in tight[:40]:
        print("  tight", x)
    for pre in ("217", "218", "777", "620", "739"):
        print(f"  {pre}: scan max t = {p3.get(pre)}")
    big = sorted(((v[0], k, v[1]) for k, v in p3.items()), reverse=True)[:5]
    print("  largest delays to any 3-digit palindrome prefix in the scan:", big)

if __name__ == "__main__":
    main()
