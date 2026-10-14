"""Finite obstruction search for freely mixed period-three bulk codes.

This is a discovery/certificate search, not a finite decimal orbit witness.
The exact cyclic bulk transducer is implemented independently here.  Every
rejected two-letter code comes with a short cyclic input whose macro output
cannot be tiled by the code.  A finite surrounding decimal construction
would still need separate boundary and central equations.
"""
from itertools import product, combinations
from pathlib import Path
import json, time


def bulk_step(q, h):
    q = tuple(q)
    n = len(q)
    if all(x == 9 for x in q):
        # The three possible sums of complementary-direction output digits.
        return {tuple([x]*n) for x in (0, 9, 18)}
    cut = next(i for i, x in enumerate(q) if x != 9)
    c = int(q[cut] >= 10)
    low = [0]*n
    for k in range(1, n+1):
        i = (cut+k) % n
        low[i] = (q[i]+c) % 10
        c = (q[i]+c)//10
    c = int(q[cut] >= 10)
    high = [0]*n
    for k in range(1, n+1):
        i = (cut-k) % n
        high[i] = (q[i]+c) % 10
        c = (q[i]+c)//10
    return {tuple(low[i]+high[(i-h) % n] for i in range(n))}


def macro(q, clock):
    states = {tuple(q)}
    for h in clock:
        states = {y for x in states for y in bulk_step(x, h)}
    return states


def motifs(clock):
    return [q for q in product(range(19), repeat=3) if q in macro(q, clock)]


def tiled(q, code):
    return all(q[i:i+3] in code for i in range(0, len(q), 3))


def code_probe(code, clock, words):
    for word in words:
        q = sum((code[i] for i in word), ())
        out = macro(q, clock)
        if not any(tiled(x, code) for x in out):
            return {"block_word": word, "input": q, "outputs": sorted(out)}
    return None


def cyclic_binary_words(n):
    for w in product(range(2), repeat=n):
        if not (0 in w and 1 in w):
            continue
        if w == min(w[j:]+w[:j] for j in range(n)):
            yield w


def run(name, clock):
    started = time.monotonic()
    candidates = motifs(clock)
    words = tuple(w for n in range(2, 7) for w in cyclic_binary_words(n))
    rejects = []
    survivors = []
    for code in combinations(candidates, 2):
        fail = code_probe(code, clock, words)
        if fail is None:
            survivors.append(code)
        else:
            rejects.append({"code": code, **fail})
    result = {"name": name, "clock": clock, "candidate_motifs": candidates,
              "candidate_two_block_codes": len(candidates)*(len(candidates)-1)//2,
              "cyclic_test_words": words, "rejected_codes": rejects,
              "surviving_codes": survivors, "seconds": time.monotonic()-started}
    Path(__file__).with_name(name+"_mixture.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ("candidate_motifs", "cyclic_test_words", "rejected_codes")}), flush=True)
    return result


if __name__ == "__main__":
    run("clock33_gain12", (1,1,0,0,0,1,0,0,0,0,1)*3)
    run("clock24_gain12", (0,1)*12)
