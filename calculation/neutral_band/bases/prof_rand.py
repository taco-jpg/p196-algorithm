import os
import sys, time, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb_mirror import run
for b in (2, 3, 4, 8, 10, 11, 26):
    rng = random.Random(1); hi = 2 * b - 2; cnt = {}; t0 = time.time(); N = 2000
    for _ in range(N):
        lb = rng.randint(1, 12); B = [rng.randint(1, hi)] + [rng.randint(0, hi) for _ in range(lb - 1)]
        lc = rng.randint(0, 12); half = [rng.randint(0, hi) for _ in range((lc + 1) // 2)]; C = half + half[:lc // 2][::-1]
        r = run(b, B, C, maxsteps=400, maxlen=120); cnt[r[0]] = cnt.get(r[0], 0) + 1
    print(b, cnt, '%.1f us/start' % ((time.time() - t0) / N * 1e6), flush=True)
