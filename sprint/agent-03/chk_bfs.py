"""Cross-check fwdbfs.c bitsets F<k>.bin (k = 3,4,5) against a pure-Python BFS of the
reference forward_prefix. Run in the work dir."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from fwdref import forward_prefix
def code(w): 
    c = 0
    for x in reversed(w): c = c*19 + x
    return c
def bfs(w0):
    seen = {tuple(w0)}; st = [list(w0)]
    while st:
        w = st.pop()
        for e in (0,1):
            v = tuple(forward_prefix(w, e))
            if v not in seen: seen.add(v); st.append(list(v))
    return seen
w100 = [8,8,13,9,14,14,14]
for k in (3,4,5):
    F = bfs(w100[:k])
    data = open(f"F{k}.bin","rb").read()
    bits = {i for i in range(19**k) if (data[i>>3] >> (i&7)) & 1}
    assert bits == {code(list(w)) for w in F}, k
    print(k, len(F), "matches C bitset")
