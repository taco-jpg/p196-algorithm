# symmetries of the bulk tables: (tau, sigma) with X[(t+tau)%P][(j+sigma)%M] == X[t][j] for X in L, UP, DN and G[t+tau]==G[t];
# and the cross-isomorphism rec1 <-> rec0.  Also the orbit structure of the phase map.
import sys
def load(fn):
    tok = open(fn).read().split(); it = iter(tok)
    P = int(next(it)); M = int(next(it))
    G = [int(next(it)) for _ in range(P)]
    L = []; U = []; D = []
    for t in range(P):
        L.append([int(next(it)) for _ in range(M)]); U.append([int(next(it)) for _ in range(M)]); D.append([int(next(it)) for _ in range(M)])
    return P, M, G, L, U, D
def syms(A, B):
    P, M, G, L, U, D = A; P2, M2, G2, L2, U2, D2 = B
    out = []
    for tau in range(P):
        for sg in range(M):
            if all(G2[(t + tau) % P] == G[t] for t in range(P)) and all(L2[(t+tau)%P][(j+sg)%M] == L[t][j] and U2[(t+tau)%P][(j+sg)%M] == U[t][j] and D2[(t+tau)%P][(j+sg)%M] == D[t][j] for t in range(P) for j in range(M)):
                out.append((tau, sg))
    return out
r0 = load("lat_rec0.tbl"); r1 = load("lat_rec1.tbl"); r2 = load("lat_rec2.tbl")
print("rec0 self-symmetries (tau,sigma):", syms(r0, r0))
print("rec2 self-symmetries:", syms(r2, r2))
print("rec0 -> rec1 isomorphisms X1[t+tau][j+sigma] = X0[t][j]:", syms(r0, r1))
def orbits(A):
    P, M, G, L, U, D = A; seen = {}; orbs = []
    for t in range(P):
        for j in range(M):
            for par in range(2):
                if (t, j, par) in seen: continue
                x = (t, j, par); orb = []
                while x not in seen:
                    seen[x] = len(orbs); orb.append(x); tt, jj, pp = x; g = G[tt]; dh = 1 if (g == 1 and pp == 0) else 0
                    x = ((tt + 1) % P, (jj + dh) % M, (pp + g) % 2)
                orbs.append(orb)
    return orbs
for nm, A in (("rec0", r0), ("rec2", r2)):
    ob = orbits(A); print(nm, "orbits:", len(ob), [len(o) for o in ob], "t=0 phases per orbit:", [sorted((j, p) for (t, j, p) in o if t == 0)[:12] for o in ob])
