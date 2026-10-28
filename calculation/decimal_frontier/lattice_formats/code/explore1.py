import sys, random, collections
sys.path.insert(0,'/home/claude/research/w3_formats/code')
from gt import *

def run_template(T, maxsteps=300, maxsize=60):
    """forward; return (status, steps, final)"""
    seen = {}
    cur = T
    offs = []
    for t in range(maxsteps):
        if cur in seen:
            return ('cycle', t, cur, seen[cur])
        seen[cur] = t
        try:
            T2, gm, info = step(cur)
        except (Ambiguous, Unsupported) as e:
            return ('unsupported', t, str(e)[:50])
        if not info['differs']:
            return ('dead', t, cur)
        if T2.lit_size() > maxsize: return ('grow', t, T2)
        cur = T2
    return ('long', maxsteps, cur)

if __name__ == '__main__':
    b = 10
    rng = random.Random(1)
    for k in [0, 18, 2, 6, 9]:
        res = collections.Counter(); best = (0,None)
        for trial in range(3000):
            lb = rng.randint(1,6)
            B = tuple(rng.randint(0,18) for _ in range(lb))
            if B[0]==0: continue
            T = Template(b, [('L',B),('B',(k,),0)], ())
            r = run_template(T, 200, 40)
            res[r[0]] += 1
            if r[0] in ('dead','grow','long','cycle') and r[1] > best[0]: best = (r[1], B, r[0])
        print('band', k, dict(res), 'longest', best)
