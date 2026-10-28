import sys
from hyb import *
from hsurv import survive
from runsat import stream
def show(name, lp, s, t0, W, T, b=10):
    loops = {'0': [0], '18': [18], '6': [6, 12], '2': [2, 4, 8, 16, 14, 10]}[lp]
    cyc = stream(name); p = len(cyc)
    gam = [cyc[(t0 + t) % p][1] for t in range(T)]; e1 = [cyc[(t0 + t) % p][2] for t in range(T)]
    cs = [loops[(s + t) % len(loops)] for t in range(T)]
    st, Q0 = survive(b, gam, e1, cs, W, 120, True)
    print(st, Q0, 'gam', gam, 'e1', e1, 'c', cs)
    if Q0 is None: return
    C = list(Q0); c = cs[0]
    for t in range(T):
        B, g2, e12, u = cyc[(t0 + t) % p]
        r = hstep_raw(b, B, C, c)
        print(f"t={t:2d} gam={gam[t]} e1={e1[t]} c={c:2d} k={r['k'] if r else '-'} C={C}")
        if r is None: print('  DEAD'); break
        B2, C2, u2, v, p_ = trim(b, r['B'], r['C'], r['c'])
        print(f"      raw C'={r['C']}  e2={r['e2']} e3={r['e3']}  -> trimmed v={v} p={p_} C2={C2}")
        C, c = C2, r['c']
if __name__ == '__main__':
    a = sys.argv
    show(a[1], a[2], int(a[3]), int(a[4]), int(a[5]), int(a[6]))
