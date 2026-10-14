"""Positive-only search in the all-length carry-history score cone.

Numerical zero/infeasibility is not a theorem. A candidate must satisfy all
integral rows over exact rationals and have an explicit positive accepted path.
"""
from pathlib import Path
import sys, json, time, math, random
from fractions import Fraction
from collections import deque

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import persist_spacetime_weighted as m
import creative_regular_invariant as r

HERE = Path(__file__).resolve().parent

def word_of_int(n):
    ds = tuple(map(int, str(n)))
    return r.fold(tuple(a+b for a,b in zip(ds, ds[::-1])))

def positive_word(ws):
    """Exact longest-path test, with positive-cycle pumping if necessary."""
    den = math.lcm(*(w.denominator for w in ws))
    w = [int(v*den) for v in ws]
    # Trim away states that cannot terminate, independently of their weights.
    live = {x for x,c in m.TERMS}
    for _ in range(len(m.FS)):
        new = live | {x for x,q,o,y in m.FE if y in live}
        if new == live: break
        live = new
    best = {x:(0,()) for x in (0,1) if x in live}
    for turn in range(len(live)+1):
        for (x,c),(_,_,t) in m.TERMS.items():
            if x in best and best[x][0]+w[t] > 0:
                score,path = best[x]
                word = (tuple(m.FE[e][1] for e in path), c)
                assert m.history_path(word) == list(path)+( [t] )
                return dict(word=word, path=list(path)+[t],
                            exact_score=str(Fraction(score+w[t],den)),
                            pumping=False)
        new = dict(best)
        changed = []
        for ei,(x,q,o,y) in enumerate(m.FE):
            if x in best and y in live:
                val,path = best[x]
                if y not in new or val+w[ei] > new[y][0]:
                    new[y] = (val+w[ei], path+(ei,))
                    changed.append(y)
        if new == best: return None
        best = new
    # A strict improvement past |V| edges contains a positive cycle.
    for _,path in best.values():
        if not path: continue
        vertices = [m.FE[path[0]][0]]+[m.FE[e][3] for e in path]
        prefixes = [0]
        for e in path: prefixes.append(prefixes[-1]+w[e])
        for i in range(len(vertices)):
            for j in range(i+1,len(vertices)):
                gain = prefixes[j]-prefixes[i]
                if vertices[i] != vertices[j] or gain <= 0: continue
                todo = deque([(vertices[i], ())]); seen = {vertices[i]}
                suffix = None
                while todo:
                    x, tail = todo.popleft()
                    for (xx,c),(_,_,t) in m.TERMS.items():
                        if xx == x:
                            suffix = tail,c,t; break
                    if suffix is not None: break
                    for q,o,y,e in m.OUT[x]:
                        if y in live and y not in seen:
                            seen.add(y); todo.append((y,tail+(e,)))
                assert suffix is not None
                tail,c,t = suffix
                base = prefixes[i]+sum(w[e] for e in tail)+w[t]
                repeats = max(1,(-base)//gain+1)
                prefix,cycle = path[:i],path[i:j]
                report = dict(pumping=True, prefix_edges=prefix,
                              cycle_edges=cycle, repeats=repeats,
                              suffix_edges=tail, terminal=t, center=c,
                              exact_score=str(Fraction(base+repeats*gain,den)))
                if len(prefix)+repeats*len(cycle)+len(tail) < 100000:
                    full = prefix+cycle*repeats+tail
                    word = (tuple(m.FE[e][1] for e in full), c)
                    assert m.history_path(word) == list(full)+[t]
                    report.update(word=word,path=list(full)+[t])
                return report
    raise AssertionError('Unexplained strict longest-path improvement')

def exact_check(out):
    if not out.get('candidate'): return None
    vals = [Fraction(x) for x in out['candidate']]
    nv,rows,rhs,meta = m.constraints(out['lambda_'],out['seed'])
    violations = [i for i,row in enumerate(rows[:-1])
                  if sum(vals[j]*v for j,v in row.items()) > 0]
    out['independent_exact_violations'] = violations[:20]
    if violations: return None
    return positive_word(vals[:m.NW])

def main():
    start = time.monotonic()
    seeds = {'196':word_of_int(196),'18887':word_of_int(18887)}
    for label in ('196','18887'):
        q = seeds[label]
        for i in range(1,121):
            q = r.qstep(q)
            if i in (20,80,120): seeds[f'{label}_step{i}'] = q
    rng = random.Random(19618887)
    seeds['random_83_digits'] = (tuple([rng.randrange(1,19)]+[rng.randrange(19) for _ in range(40)]),2*rng.randrange(10))
    seeds['uniform16_103_digits'] = ((8,)+(16,)*50,16)
    # lambda>1 is impossible: bounded tile weights give S_t=O(t),
    # whereas a positive score preserved at that scale grows exponentially.
    jobs = [('1/4','196_step80'),('3/4','196_step80'),
            ('1/4','18887_step80'),('3/4','random_83_digits'),
            ('1/8','uniform16_103_digits'),('1/3','196_step120'),
            ('2/3','random_83_digits'),('7/8','18887_step120'),
            ('1/100','196_step120'),('99/100','random_83_digits'),
            ('1/16','18887_step80'),('1/2','uniform16_103_digits')]
    if len(sys.argv)>2 and sys.argv[2]=='different':
        jobs = [('2/3','random_83_digits'),('1/8','random_83_digits'),
                ('1/100','random_83_digits'),('99/100','random_83_digits'),
                ('1/16','18887_step80')]
    results = json.loads((HERE/'results.json').read_text()) if (HERE/'results.json').exists() else []
    budget = float(sys.argv[1]) if len(sys.argv)>1 else 180
    for lam,label in jobs:
        filename = HERE/f'run_{lam.replace("/","_")}_{label}.json'
        if filename.exists(): continue
        remaining = budget-(time.monotonic()-start)
        if remaining < 2: break
        print(json.dumps(dict(starting=label,lambda_=lam,elapsed=time.monotonic()-start)),flush=True)
        out = m.solve(lam,min(12,remaining-1),'scipy',seeds[label])
        witness = exact_check(out)
        out['finite_word_label'] = label
        out['any_positive_accepted_path'] = witness
        filename.write_text(json.dumps(out,indent=2))
        brief = {k:v for k,v in out.items() if k not in ('candidate','dual_certificate','dual_approx_support','seed')}
        brief['seed_folded_length'] = len(seeds[label][0])
        brief['artifact'] = str(filename)
        results.append(brief)
        (HERE/'results.json').write_text(json.dumps(results,indent=2))
        print(json.dumps(brief),flush=True)
        if witness is not None:
            (HERE/'POSITIVE_CANDIDATE.json').write_text(json.dumps(out,indent=2))
            print('POSITIVE CANDIDATE FOUND; exact all-length rows and positive word checked',flush=True)
            break
    print(json.dumps(dict(total_seconds=time.monotonic()-start,runs=len(results))),flush=True)

if __name__ == '__main__': main()
