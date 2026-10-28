import random, sys, time
from htrans import decide
from hsat import solve
from runbase import loops
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
ntest = int(sys.argv[2]) if len(sys.argv) > 2 else 60
agree = 0; nsucc = 0; nex = 0; bad = 0
t0 = time.time()
for it in range(ntest):
    b = random.choice([2, 3, 4, 5, 6, 7, 10])
    T = random.randint(1, 6)
    gam = [random.randint(0, 1) for _ in range(T)]
    e1 = [random.randint(0, 1) for _ in range(T)]
    lps = loops(b)
    lp = random.choice(lps)
    if T % len(lp) != 0: continue
    s = random.randrange(len(lp))
    cs = [lp[(s + t) % len(lp)] for t in range(T)]
    A = random.randint(0, max(0, sum(gam) // 2 + 1))
    A = min(A, T)
    res = decide(b, gam, e1, cs, A, cap=300000)
    if res[0] == 'CAP': print('cap', b, gam, e1, cs, A); continue
    Wmax = 9
    sat_feas = None
    for W in (Wmax,):
        st, Q0 = solve(b, gam, e1, cs, W, A, tl=30)
        sat_feas = st in ('OPTIMAL', 'FEASIBLE')
        if st not in ('OPTIMAL', 'FEASIBLE', 'INFEASIBLE'): sat_feas = None
    if res[0] == 'SUCCESS':
        nsucc += 1
        width = res[1]
        # the transfer path length bounds the register width needed: SAT at W>=width must be feasible
        st, Q0 = solve(b, gam, e1, cs, max(Wmax, width), A, tl=60)
        ok = st in ('OPTIMAL', 'FEASIBLE')
    else:
        nex += 1
        ok = (sat_feas is False)
    if ok: agree += 1
    else:
        bad += 1; print('DISAGREE', b, gam, e1, cs, A, res[:2], sat_feas)
print('tests', agree + bad, 'agree', agree, 'success', nsucc, 'exhausted', nex, 'bad', bad, round(time.time() - t0, 1), 's')
