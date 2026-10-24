"""Extract (prefix, rank bound) entries from the repo's Agent124 four/five-digit
certificate entry lists. Each entry carries the kernel-checked ancestry bound
t <= bound + 1 (theorems ancestry_NN in A124F4Final / A124F5Final)."""
import re, sys, json, pathlib
root = pathlib.Path(sys.argv[1])
out = {}
for f in ["Agent124FourDigit/A124F4Entries.lean", "Agent124FourDigit/A124F5Entries.lean"]:
    txt = (root / f).read_text()
    for m in re.finditer(r"\(\[([0-9,\s]+)\],\s*(\d+)\)", txt):
        pre = "".join(x.strip() for x in m.group(1).split(","))
        b = int(m.group(2))
        key = pre
        out.setdefault(key, []).append((b, f))
print(len(out), "distinct prefixes", file=sys.stderr)
lens = {}
for k in out: lens[len(k)] = lens.get(len(k), 0) + 1
print("by length", lens, file=sys.stderr)
json.dump({k: min(b for b, _ in v) for k, v in out.items()}, open("repo_bounds.json", "w"), indent=0)
