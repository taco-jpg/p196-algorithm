"""Independent exhaustive small-word check of the gap-one identity."""
import json
from pathlib import Path


def normalize(q):
    # This independent oracle forms the integer, then reads its digits.
    value = sum(c * 10**i for i, c in enumerate(q))
    return [int(c) for c in str(value)[::-1]]


def paired(d):
    return [a+b for a, b in zip(d, d[::-1])]


def words():
    return ([[2*a] for a in range(1, 10)]
            + [[a, a] for a in range(1, 19)]
            + [[a, 2*b, a] for a in range(1, 19) for b in range(10)])


def main():
    count = 0
    branches = {str((e,h)): 0 for e in (0,1) for h in (0,1)}
    for b in words():
        for h in words():
            u, d = normalize(b), normalize(h)
            e, f = len(u)-len(b), len(d)-len(h)
            delta = max(e, f)
            bnew = paired(u)
            hnew = [0]*(len(h)+2*delta-e)
            for i, digit in enumerate(d):
                hnew[delta-e+i] += digit
                hnew[len(h)+delta-1-i] += digit
            assert hnew[0] > 0 and hnew[-1] > 0
            assert hnew == hnew[::-1] and max(hnew) <= 18
            expected = bnew+[0]*(1-delta)+hnew+[0]*(1-delta)+bnew[::-1]
            actual = paired(normalize(b+[0]+h+[0]+b[::-1]))
            assert actual == expected, (b,h,e,f)
            branches[str((e,f))] += 1
            count += 1
    result = {'status':'PASS','cases':count,'exterior_core_lengths':[1,2,3],
              'initial_gap':1,'overflow_branches':branches,
              'scope':'Finite independent boundary-case control; unrestricted proof is written.'}
    Path(__file__).with_name('root_separation_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__ == '__main__':
    main()
