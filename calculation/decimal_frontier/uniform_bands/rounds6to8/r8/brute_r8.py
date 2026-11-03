import os, sys, itertools, subprocess, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify_ext as V
b = int(sys.argv[1]); L = int(sys.argv[2]); pmax = int(sys.argv[3])
def lists():
    for n in range(0, L + 1):
        for B in itertools.product(range(2 * b - 1), repeat=n):
            if n and (B[0] == 0 or B[-1] == b - 1): continue
            yield B
F = {}; info = {}
for B in lists():
    nb, e1, gm, u = V.Bstep(b, list(B)); info[B] = (e1, gm)
    F[B] = tuple(nb) if len(nb) <= L else None
seen = set(); uniq = {}
for B in F:
    path = []; x = B
    while x is not None and x in F and x not in seen and x not in path: path.append(x); x = F[x]
    if x is not None and x in path: uniq[frozenset(path[path.index(x):])] = path[path.index(x):]
    seen.update(path)
print(f"base {b}, trimmed B with width <= {L}: {len(F)} lists, {len(uniq)} periodic orbits of the Agent120 B-map inside the box")
bad = 0
for key, cyc in uniq.items():
    g = "".join(str(info[B][1]) for B in cyc); e = "".join(str(info[B][0]) for B in cyc); p = len(cyc)
    if p > pmax: print(f" orbit p={p} (skipped, p>{pmax})"); continue
    # in reach, the orbit start B_0 sits at time 0 with overflow word g and stream e
    out = subprocess.run(["env", "ALLFITS=1", "./reach_w", str(b), str(p), g, "WIRE"], capture_output=True, text=True).stdout
    streams = re.findall(r"NEW STREAM at height (\d+): ([01]+)", out)
    hit = [h for h, s in streams if s == e]
    ok = bool(hit) and int(hit[0]) <= max(len(B) for B in cyc) + 1
    wmax = max(len(B) for B in cyc)
    print(f" orbit p={p} g={g} e={e} widths={sorted(set(len(B) for B in cyc))}: reach streams={[(int(h),s) for h,s in streams]} -> {chr(65)+chr(71)+chr(82)+chr(69)+chr(69) if ok else chr(68)+chr(73)+chr(83)+chr(65)+chr(71)+chr(82)+chr(69)+chr(69)}")
    bad += not ok
print("disagreements:", bad)
