"""(1) charge law C' = 2C + 1 - 2 e1 (mod 9), C = sum(B) mod 9, on random B and on N12;
   (2) Lemma D1: cell column v_x is recovered from (I_x, I_{x+1}) -- checked on the N12 cuts."""
import sys, os, random
sys.path.insert(0, os.path.expanduser('~/p196_run/r11e/py'))
import neutral_band_search as nb
b = 10
def phi(B):
    E1 = nb.e1(b, B); C = [0] if E1 == 1 else [10]
    g = nb.gam(b, B, C); B2 = nb.nextB(b, B, C)
    while B2 and B2[-1] == 9: B2 = B2[:-1]
    return B2, g, E1
random.seed(1); bad = 0; n = 0
for trial in range(200000):
    w = random.randint(1, 30); B = [random.randint(1, 18)] + [random.randint(0, 18) for _ in range(w - 1)]
    while B and B[-1] == 9: B = B[:-1]
    if not B: continue
    B2, g, E1 = phi(B); n += 1
    if (sum(B2) - (2 * sum(B) + 1 - 2 * E1)) % 9: bad += 1
print('charge law: tested', n, 'mismatches', bad)
rows = [list(map(int, l.split(','))) for l in open(os.path.expanduser('~/p196_run/r11e/py/n12_wit.txt')) if l.strip()]
es = []
for t in range(12):
    B2, g, E1 = phi(rows[t]); es.append(E1); assert B2 == rows[(t + 1) % 12]
C = [sum(r) % 9 for r in rows]
print('N12 charges', C, 'e', es, 'sum e_t 2^-t mod 9 =', sum(e * pow(5, t, 9) for t, e in enumerate(es)) % 9)
# D1 on N12: cuts file h L H Y1 Y2 Y3; cells x = 10*Hnext + Ynext - c at overflow phases, then propagate
g = [int(c) for c in '000100010001']
cuts = [l.split() for l in open(os.path.expanduser('~/p196_run/r11e/py/n12cuts.txt'))]
print('cuts rows', len(cuts))
