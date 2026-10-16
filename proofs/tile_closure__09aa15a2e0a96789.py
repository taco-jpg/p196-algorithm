"""Least closure in the archived exact carry-tile language template.

This is a finite graph calculation covering every word length, not an orbit
cutoff. A safe fixed point would still require independent numeric/graph audit.
"""
from collections import deque
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'research'))
from persist_spacetime_tile_grammar import composed_tiles
from persist_spacetime_weighted import history_path, safety_graph

ST, CE, CT = composed_tiles()
CO = [[] for _ in ST]
CI = [[] for _ in ST]
for u, v, a, b in CE:
    CO[u].append((v, a, b))
    CI[v].append((u, a, b))
TO = [[] for _ in ST]
for u, a, x, b in CT:
    TO[u].append((a, x, b))
SS, SI, SE, STT = safety_graph()
SO = [[] for _ in SS]
for u, v, d in SE:
    a, = d
    SO[u].append((v, a))
TT = [[] for _ in SS]
for u, d in STT:
    a, = d
    TT[u].append(a)


def unsafe(allowed):
    seen = set(SI)
    todo = deque(SI)
    while todo:
        u = todo.popleft()
        if any(a in allowed for a in TT[u]):
            return True
        for v, a in SO[u]:
            if a in allowed and v not in seen:
                seen.add(v)
                todo.append(v)
    return False


def image_tiles(allowed):
    # Reachability uses accepted-input edges only; the second history is
    # intentionally unrestricted, because closure must admit all its tiles.
    reachable = set(range(4))
    todo = deque(reachable)
    while todo:
        u = todo.popleft()
        for v, a, b in CO[u]:
            if a in allowed and v not in reachable:
                reachable.add(v)
                todo.append(v)
    live = {u for u in reachable if any(a in allowed for a, x, b in TO[u])}
    todo = deque(live)
    while todo:
        v = todo.popleft()
        for u, a, b in CI[v]:
            if u in reachable and a in allowed and u not in live:
                live.add(u)
                todo.append(u)
    result = set()
    for u in reachable & live:
        for v, a, b in CO[u]:
            if a in allowed and v in live:
                result.add(b)
        for a, x, b in TO[u]:
            if a in allowed:
                result.add(b)
                if x is not None:
                    result.add(x)
    return result


def closure(word):
    return closure_tiles(history_path(word))


def closure_tiles(tiles):
    allowed = set(tiles)
    sizes = []
    while True:
        sizes.append(len(allowed))
        if unsafe(allowed):
            return False, allowed, sizes
        new = allowed | image_tiles(allowed)
        if new == allowed:
            return True, allowed, sizes
        allowed = new


if __name__ == '__main__':
    import json, random, time
    start = time.monotonic()
    for word in [((7,), 18), ((8, 16), 16), ((8,), 16), ((1,), 0)]:
        yes, a, sizes = closure(word)
        print(json.dumps(dict(word=word, safe_fixed_point=yes, sizes=sizes)), flush=True)
    rng = random.Random(196)
    for trial in range(3000):
        k = rng.randrange(0, 12)
        p = (rng.randrange(1,19),) + tuple(rng.randrange(19) for _ in range(k))
        c = rng.choice([None] + list(range(0,19,2)))
        yes, a, sizes = closure((p,c))
        if yes:
            print(json.dumps(dict(candidate_word=(p,c), allowed_tiles=sorted(a), sizes=sizes)),flush=True)
            break
        if trial % 250 == 0:
            print(json.dumps(dict(trial=trial,seconds=time.monotonic()-start)),flush=True)
    else:
        print(json.dumps(dict(no_candidate_in_sample=3000,seconds=time.monotonic()-start)),flush=True)
