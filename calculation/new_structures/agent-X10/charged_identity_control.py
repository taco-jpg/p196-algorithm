#!/usr/bin/env python3
"""Independent Python big-integer truth controls for all 90 charged channels.
Proof shape: u a^R (9-a)^R v -> H 0^(2R) L, s=A+D, t=B+C+1.
The code below is independent of the C++ packet recurrence and digit replayer.
"""
import json

def vals(s, t):
    A = max(1, s - 9)
    D = s - A
    C = max(1, t - 10)
    B = t - 1 - C
    assert A in range(1, 10) and D in range(10)
    assert B in range(10) and C in range(1, 10)
    return 10 * A + B, 10 * C + D

def run():
    checks = 0
    channels = []
    for s in range(10, 19):
        for t in range(10, 20):
            u, v = vals(s, t)
            H = 100 + 10 * (s - 9) + (t - 10)
            L = 10 * (t - 10) + (s - 10)
            for a in (0, 1, 4, 5, 8, 9):
                for R in (1, 2, 3, 11, 37):
                    original = f"{u:02d}" + str(a) * R + str(9-a) * R + f"{v:02d}"
                    actual = int(original) + int(original[::-1])
                    predicted = f"{H:d}" + '0' * (2*R) + f"{L:02d}"
                    assert str(actual) == predicted, (s,t,a,R,u,v, actual,predicted)
                    checks += 1
            channels.append((s,t,H,L,u,v))
    assert len(channels) == 90 and checks == 2700
    for R in (1, 2, 3, 4, 10, 101):
        n = '88' + '4' * R + '5' * R + '49'
        assert str(int(n) + int(n[::-1])) == '183' + '0' * (2*R) + '37'
        checks += 1
    print(json.dumps({"channels":len(channels), "independent_python_bigint_identities":checks,
                      "best_channel":{"s":17,"t":13,"u":88,"v":49,"H":183,"L":37},
                      "second_control":{"s":13,"t":16,"u":88,"v":75,"H":146,"L":63}},
                     sort_keys=True))

if __name__ == '__main__':
    run()
