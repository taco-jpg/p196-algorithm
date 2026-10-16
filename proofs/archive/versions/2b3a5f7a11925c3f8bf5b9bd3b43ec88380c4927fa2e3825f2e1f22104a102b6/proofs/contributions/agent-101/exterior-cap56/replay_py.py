"""Agent #101: independent Python replay of the complete exterior graph for a
cap L, using exterior_ref.step (itself checked against literal integer
reverse-and-add).  Different state indexing and traversal from exterior_cap.c.
Prints counts, cycle count, sharp max exit time and a SHA-256 over the
successor rows in canonical order:  'c|B|c'|B'|gamma\n' or 'c|B|EXIT|gamma\n'."""
import sys, hashlib, itertools
from exterior_ref import step

L = int(sys.argv[1])
PH = [2, 4, 6, 8, 10, 12, 14, 16]

def blocks():
    yield ()
    for b in range(1, L + 1):
        for first in range(1, 19):
            for rest in itertools.product(range(19), repeat=b - 1):
                yield (first,) + rest

off = [0]
for b in range(L + 1):
    off.append(off[-1] + 19 ** b)
PER = off[L + 1]
def idx(c, B):
    x = 0
    for v in reversed(B):
        x = x * 19 + v
    return (c // 2 - 1) * PER + off[len(B)] + x
NS = 8 * PER
succ = [-2] * NS          # -2 invalid slot, -1 exit
states = {}
h = hashlib.sha256()
cnt = 0
for c in PH:
    for B in blocks():
        if B and B[-1] == c:
            continue
        cnt += 1
        cp, Bp, g = step(c, list(B))
        if len(Bp) <= L:
            succ[idx(c, B)] = idx(cp, Bp)
            h.update(f"{c}|{','.join(map(str,B))}|{cp}|{','.join(map(str,Bp))}|{g}\n".encode())
        else:
            succ[idx(c, B)] = -1
            h.update(f"{c}|{','.join(map(str,B))}|EXIT|{g}\n".encode())
n = NS
T = bytearray(n)          # 0 unknown, 255 on-stack
cycles = 0
for s in range(n):
    if T[s] or succ[s] == -2:
        continue
    path = []
    cur = s
    while cur != -1 and T[cur] == 0:
        T[cur] = 255
        path.append(cur)
        cur = succ[cur]
    if cur != -1 and T[cur] == 255:
        cycles += 1
        base = 0
    else:
        base = 0 if cur == -1 else T[cur]
    for p in reversed(path):
        base += 1
        T[p] = base
internal = sum(1 for x in succ if x >= 0)
mx = max(T)
arg = [i for i in range(n) if T[i] == mx]
print(f"cap={L} states={cnt} internal_edges={internal} exit_edges={cnt-internal} "
      f"cycles={cycles} max_exit_time={mx} argmax={arg}")
print("rows_sha256", h.hexdigest())
