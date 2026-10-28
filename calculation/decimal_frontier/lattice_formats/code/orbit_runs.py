import sys, collections, time
def pair_word(x):
    s = str(x)
    n = len(s)
    d = [int(c) for c in s[::-1]]
    return [d[i] + d[n-1-i] for i in range(n)]
def runs_of(P):
    """maximal runs of equal coefficient in the lower half"""
    n = len(P); h = n//2
    out = []
    i = 0
    while i < h:
        j = i
        while j < h and P[j] == P[i]: j += 1
        out.append((P[i], i, j-i)); i = j
    return out
if __name__ == '__main__':
    seed = int(sys.argv[1]); steps = int(sys.argv[2])
    x = seed
    best = collections.defaultdict(lambda: (0,0))
    t0 = time.time()
    hist = collections.Counter()
    for t in range(steps):
        P = pair_word(x)
        for (c, pos, ln) in runs_of(P):
            if ln > best[c][0]: best[c] = (ln, t)
            if ln >= 8: hist[c] += 1
        x = x + int(str(x)[::-1])
        if time.time() - t0 > 14: print('time cut at', t); break
    print('digits', len(str(x)))
    print({c: best[c] for c in sorted(best)})
    print('count of runs >=8 by coeff', dict(hist))
