import itertools, random, sys
from cauto2 import solve, lengths, reconstruct

def cstep_forced(b, C, e1, g, v):
    m = len(C); c = e1; DC = []
    for x in C:
        DC.append((x + c) % b); c = (x + c) // b
    if c != 1 - e1: return None
    yd = (b-1)*e1
    if g == 0: cp = [DC[k] + DC[m-1-k] for k in range(m)]
    else:
        W = DC + [yd]; cp = [W[k] + W[m-k] for k in range(m+1)]
    n = len(cp)
    if v:
        if n - 2*v < 1: return None
        if any(x != b-1 for x in cp[:v]) or any(x != b-1 for x in cp[n-v:]): return None
        cp = cp[v:n-v]
    return cp

def brute(b, e, g, m0, v):
    P = len(e); W = 2*b-1; h = (m0+1)//2; sols = 0
    for half in itertools.product(range(W), repeat=h):
        C = list(half) + list(half[:m0//2][::-1])
        cur = C; ok = True
        for t in range(P):
            cur = cstep_forced(b, cur, e[t], g[t], v[t])
            if cur is None: ok = False; break
        if ok and cur == C: sols += 1
    return sols

def check(res, b, e, g, m0, v):
    P = len(e); m = lengths(g, v, m0); J = [(x+1)//2 for x in m]
    C = reconstruct(res, b, P, m)
    cur = C[0]
    for t in range(P):
        if cur != C[t]: return False
        cur = cstep_forced(b, cur, e[t], g[t], v[t])
        if cur is None: return False
    return cur == C[0]

if __name__=="__main__":
    random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    nt = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    stats = {'agree_feas': 0, 'agree_infeas': 0, 'bad': 0}
    tested = 0
    while tested < nt:
        b = random.choice([2, 2, 3, 4])
        P = random.choice([2, 3, 4])
        g = [random.randint(0, 1) for _ in range(P)]
        G = sum(g)
        if G == 0 or G % 2: continue
        e = [random.randint(0, 1) for _ in range(P)]
        # choose v pattern with sum v = G/2 (0/1 entries)
        pos = random.sample(range(P), G//2) if G//2 <= P else None
        v = [1 if t in pos else 0 for t in range(P)]
        m0 = random.randint(1, 7)
        if lengths(g, v, m0) is None: continue
        tested += 1
        bs = brute(b, e, g, m0, v)
        res = solve(b, e, g, m0, v)
        feas = res is not None and not isinstance(res, tuple)
        if (bs > 0) != feas:
            stats['bad'] += 1; print("MISMATCH", b, e, g, m0, v, "brute", bs, "auto", feas)
        elif feas:
            if check(res, b, e, g, m0, v): stats['agree_feas'] += 1
            else: stats['bad'] += 1; print("BADSOL", b, e, g, m0, v)
        else: stats['agree_infeas'] += 1
    print(stats)
