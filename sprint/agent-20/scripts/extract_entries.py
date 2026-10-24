#!/usr/bin/env python3
"""Extract every (prefix, rank bound) entry list used by the Agent124.PrefixL
`entryOK` / `no_196_of_entries` pipeline and audit it statically.

Usage:  python3 extract_entries.py <repo-root> [extra .lean files/dirs ...] > entries.json

For each `def entriesNN : List (List Nat × Nat) := [...]` it records the module,
the width k taken from the matching `entryOK k` line, and the entries.  It then
checks, independently of Lean:
  * every prefix has a nonzero leading digit and digits 0..9 (otherwise
    PalStartsL is vacuously false and the "exclusion" says nothing);
  * noOverflowPre holds (lead >= 2 or some digit >= 3);
  * bound + 1 <= 100;
  * which module theorem `no_196_NN` consumes the list (so the list is really used).
Prints a summary to stderr and a JSON list of entries to stdout.
"""
import json, os, re, sys

ENT_DEF = re.compile(r"def (entries\w*)\s*:\s*List \(List Nat × Nat\)\s*:=\s*\[(.*?)\]\s*\n\s*\n", re.S)
PAIR = re.compile(r"\(\[([0-9,\s]+)\],\s*([0-9]+)\)")
OK = re.compile(r"theorem (\w+)\s*:\s*(entries\w*)\.all \(entryOK (\d+) ")
NO196 = re.compile(r"theorem (no_196_\w+)\s*:.*?no_196_of_entries (\d+) \(R (\w+)\) \w+ \w+ (entries\w*) ", re.S)
SINGLE_OK = re.compile(r"entryOK (\d+) \(R \w+\) \(\[([0-9,\s]+)\],\s*([0-9]+)\) = true")


def lean_files(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
        else:
            for dp, _, fns in os.walk(p):
                for fn in sorted(fns):
                    if fn.endswith(".lean") and "/Drafts/" not in dp + "/":
                        yield os.path.join(dp, fn)


def main():
    root = sys.argv[1]
    lean = os.path.join(root, "lean")
    extra = sys.argv[2:]
    out = []
    NS = re.compile(r"^namespace (\S+)", re.M)
    files = list(lean_files([os.path.join(lean, "P196")] + extra))
    # consumers and width checks may live in another file of the same namespace
    oks, users = {}, {}
    for f in files:
        src = open(f, encoding="utf-8").read()
        ns = (NS.findall(src) or [""])[0]
        for m in OK.finditer(src):
            oks[(ns, m.group(2))] = int(m.group(3))
        for m in NO196.finditer(src):
            users[(ns, m.group(4))] = m.group(1)
    for f in files:
        src = open(f, encoding="utf-8").read()
        mod = os.path.relpath(f, lean)[:-5].replace(os.sep, ".")
        ns = (NS.findall(src) or [""])[0]
        for m in ENT_DEF.finditer(src):
            name, body = m.group(1), m.group(2)
            for pm in PAIR.finditer(body):
                pre = [int(x) for x in pm.group(1).split(",")]
                out.append({"module": mod, "list": name, "k": oks.get((ns, name)),
                            "no196": users.get((ns, name)), "prefix": pre, "bound": int(pm.group(2))})
        for m in SINGLE_OK.finditer(src):
            pre = [int(x) for x in m.group(2).split(",")]
            out.append({"module": mod, "list": None, "k": int(m.group(1)), "no196": "single",
                        "prefix": pre, "bound": int(m.group(3))})
    bad_digits = [e for e in out if e["prefix"][0] == 0 or any(d > 9 for d in e["prefix"])]
    no_ovf = [e for e in out if not (e["prefix"][0] >= 2 or any(d >= 3 for d in e["prefix"]))]
    big = [e for e in out if e["bound"] + 1 > 100]
    unused = [e for e in out if e["no196"] is None]
    nok = [e for e in out if e["k"] is None]
    keys = {}
    for e in out:
        keys.setdefault(tuple(e["prefix"]), []).append(e)
    dups = {k: v for k, v in keys.items() if len(v) > 1}
    by_len = {}
    for k in keys:
        by_len[len(k)] = by_len.get(len(k), 0) + 1
    log = sys.stderr
    print(f"entries extracted: {len(out)}  distinct prefixes: {len(keys)}  by length: {dict(sorted(by_len.items()))}", file=log)
    mods = {}
    for e in out:
        mods.setdefault((e["module"], e["k"]), 0)
        mods[(e["module"], e["k"])] += 1
    for (mo, k), n in sorted(mods.items()):
        print(f"  {mo}  k={k}: {n}", file=log)
    print(f"leading-zero or digit>9 prefixes (vacuous): {len(bad_digits)}", file=log)
    print(f"noOverflowPre fails (entryOK would reject): {len(no_ovf)}", file=log)
    print(f"bound+1 > 100: {len(big)}", file=log)
    print(f"lists without a no_196 consumer in the same namespace: {sorted({(e['module'], e['list']) for e in unused})}", file=log)
    print(f"entries with no entryOK width found: {len(nok)}", file=log)
    print(f"prefixes listed more than once: {len(dups)}", file=log)
    for k, v in list(dups.items())[:10]:
        print(f"   {k}: {[(e['module'], e['k'], e['bound']) for e in v]}", file=log)
    hist = {}
    for e in out:
        hist[e["bound"]] = hist.get(e["bound"], 0) + 1
    print(f"bound histogram: {dict(sorted(hist.items()))}", file=log)
    json.dump(out, sys.stdout)


if __name__ == "__main__":
    main()
