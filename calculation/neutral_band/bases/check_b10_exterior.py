import os
"""Independent check of the base-10 period-11 exterior against the Lean-mirror `step` (not G_ext):
for random symmetric centers C, follow the mirror's canonical map from (B0, C); whenever it survives t steps its exterior must equal
G_ext^t(B0).  Also report how far random centers survive (the carry word E must be reproduced by the center)."""
import sys, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb_mirror import step, hyp
from decouple import G_ext
b = 10
B0 = [1, 3, 7, 7, 5, 5, 7, 9, 12, 11, 3, 2, 6, 3, 15, 7, 2, 7, 11, 12, 11, 5, 4, 6, 14, 9, 9, 4, 4]
orb = [B0]
for t in range(12): orb.append(G_ext(b, orb[-1])[0])
rng = random.Random(7); best = 0; agree = True; total_steps = 0
for _ in range(300000):
    c = rng.randint(0, 14); half = [rng.randint(0, 18) for _ in range((c + 1) // 2)]; C = half + half[:c // 2][::-1]
    B, Cc = list(B0), C; t = 0
    while t < 12:
        e = step(b, B, Cc)
        if e is None: break
        t += 1; total_steps += 1
        if e[2] != orb[t]: agree = False
        B, Cc = e[2], e[3]
    best = max(best, t)
print("mirror exterior == G_ext orbit at every survived step:", agree, "| total mirror steps compared:", total_steps,
      "| longest random-center survival:", best, "of 11 steps")
