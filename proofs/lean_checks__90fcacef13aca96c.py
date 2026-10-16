"""Literal Python transcription of the Lean finite checks (TwoDigitProjection,
TwoDigitNumeric.tri3, TwoDigitCertificate: code/bitAt/layerAt/baseCheck/
firstRow/stepRow/shortCheck/Checked), applied to the bitmasks parsed
directly from the committed TwoDigitCert*.lean files.  Also:
  * decodes each mask and compares with the generator's minimal layers,
  * mutation tests: dropping any single triple from any layer, or dropping
    the last layer, must make some check fail (checks are not vacuous).
Usage: python3 -I lean_checks.py <package dir>
"""
import re, sys, json, os

PKG = sys.argv[1]

# ---- TwoDigitProjection (verbatim structure) ----
def hiCarry2(s2, e): return (s2 + e) // 10
def hiCarry1(s1, s2, e): return (s1 + hiCarry2(s2, e)) // 10
def topCarry(s0, s1, s2, e): return (s0 + hiCarry1(s1, s2, e)) // 10
def nextTriple(s0, s1, s2, e):
    if topCarry(s0, s1, s2, e) == 0:
        return (s0 % 10 + (s0 + hiCarry1(s1, s2, e)) % 10,
                (s1 + s0 // 10) % 10 + (s1 + hiCarry2(s2, e)) % 10,
                (s2 + (s1 + s0 // 10) // 10) % 10 + (s2 + e) % 10)
    return (s0 % 10 + 1,
            (s1 + s0 // 10) % 10 + (s0 + hiCarry1(s1, s2, e)) % 10,
            (s2 + (s1 + s0 // 10) // 10) % 10 + (s1 + hiCarry2(s2, e)) % 10)
def nextT(w, e): return nextTriple(w[0], w[1], w[2], e)
def topT(w, e): return topCarry(w[0], w[1], w[2], e)

# ---- TwoDigitNumeric.tri3 and Lychrel196.step ----
def tri3(m): return (m % 10 + m // 100 % 10, m // 10 % 10 + m // 10 % 10, m // 100 % 10 + m % 10)
def rev(n):
    r = 0
    while n:
        r, n = 10 * r + n % 10, n // 10
    return r
def step(n): return n + rev(n)

# ---- TwoDigitCertificate ----
def code(w): return w[0] * 361 + w[1] * 19 + w[2]
def bitAt(m, k): return m // 2 ** k % 2 == 1
def layerAt(ls, r): return ls[r] if r < len(ls) else 0
def rangeAll(n, p): return all(p(i) for i in range(n))
def rowAll(a, p): return rangeAll(19, lambda b: rangeAll(19, lambda c: p((a, b, c))))

class Cert:
    def __init__(self, a, b, layers): self.a, self.b, self.layers = a, b, layers
    @property
    def h(self): return len(self.layers)
    def inLayer(self, r, w): return bitAt(layerAt(self.layers, r), code(w))
    def baseCheck(self): return rangeAll(10, lambda c: self.inLayer(0, (self.a, self.b, c)))
    def firstRow(self, a):
        return rowAll(a, lambda w: rangeAll(2, lambda e:
            (not (topT(w, e) == 0 and self.inLayer(0, nextT(w, e)))) or self.inLayer(1, w)))
    def stepRow(self, r, a):
        return rowAll(a, lambda w: rangeAll(2, lambda e:
            (not self.inLayer(r, nextT(w, e))) or self.inLayer(r + 1, w)))
    def shortCheck(self):
        return rangeAll(100, lambda m: m == 0 or step(m) < 100 or
            (step(m) < 1000 and rangeAll(self.h, lambda r: r == 0 or not self.inLayer(r, tri3(step(m))))))
    def checked(self):
        why = []
        if not self.baseCheck(): why.append("base")
        for a in range(1, 19):
            if not self.firstRow(a): why.append(f"first{a}")
        for r in range(1, self.h):
            for a in range(1, 19):
                if not self.stepRow(r, a): why.append(f"step{r}_{a}")
        if not self.shortCheck(): why.append("short")
        return why

def decode(mask):
    out, k = [], 0
    while mask:
        if mask & 1:
            out.append((k // 361, k // 19 % 19, k % 19))
        mask >>= 1; k += 1
    return out

def parse(path):
    src = open(path).read()
    a = int(re.search(r"\ba := (\d+)", src).group(1))
    b = int(re.search(r"\bb := (\d+)", src).group(1))
    body = re.search(r"layers := \[(.*?)\]", src, re.S).group(1)
    layers = [int(x) for x in re.findall(r"\d+", body)]
    bound = int(re.search(r"Lychrel196\.orbit A t = P → t ≤ (\d+)", src).group(1))
    pre = re.search(r"PalindromeStartsTwo (\d+) (\d+) P", src)
    return a, b, layers, bound, (int(pre.group(1)), int(pre.group(2)))

js = json.load(open(os.path.join(PKG, "generator", "certificates.json")))
CLAIM = {"10": 1, "20": 2, "32": 2, "40": 3, "41": 3, "60": 3, "64": 3, "76": 3,
         "80": 4, "81": 4, "82": 4, "83": 4, "65": 6}
allok = True
for name, claim in CLAIM.items():
    a, b, layers, bound, pre = parse(os.path.join(PKG, f"TwoDigitCert{name}.lean"))
    C = Cert(a, b, layers)
    dec = [decode(m) for m in layers]
    same_as_json = [sorted(map(tuple, l)) for l in js[name]["layers"]] == [sorted(d) for d in dec]
    fails = C.checked()
    # mutation tests
    mut_total = mut_caught = 0
    for r in range(C.h):
        for w in dec[r]:
            mut = list(layers); mut[r] -= 2 ** code(w)
            mut_total += 1
            if Cert(a, b, mut).checked():
                mut_caught += 1
    trunc = Cert(a, b, layers[:-1]).checked() if C.h > 1 else ["n/a(h=1)"]
    ok = (not fails and same_as_json and (a, b) == pre and (str(a) + str(b)) == name
          and bound == claim == C.h and mut_caught == mut_total and bool(trunc))
    allok &= ok
    print(f"{name}: a,b={a},{b} stmt-prefix={pre} h=len(layers)={C.h} stmt-bound={bound} claim={claim} "
          f"layer sizes={[len(d) for d in dec]} matchesJSON={same_as_json} failedChecks={fails} "
          f"singleBitMutationsCaught={mut_caught}/{mut_total} truncatedFails={trunc[:3]} -> {'OK' if ok else 'PROBLEM'}")
    print("    layers:", "; ".join(" ".join(f"({x},{y},{z})" for x, y, z in d) for d in dec))
print("ALL LEAN-CHECK TRANSCRIPTIONS OK" if allok else "PROBLEM FOUND")
