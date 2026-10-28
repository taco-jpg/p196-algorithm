#!/usr/bin/env python3
# differential test: symbolic backward cones (symbwd) vs explicit engine (bwdcensus) on all F1-words of (b, p).
import sys, subprocess, time, re, os
sys.path.insert(0, '/home/claude/research/w3_formats/code')
from symfwd import Sym, uniform_targets

def sym_decide(b, gs, maxlev=10**6):
    S = Sym(b, gs)
    p = S.p; bdd = S.bdd
    T1 = S.build_T(True); T = S.build_T(False)
    Hst = [1 if c else 0 for c in S.g]
    start = S.state_cube([0]*p, Hst, [1]*sum(S.g))
    succ0 = S.image(start, T1)
    if succ0 == bdd.false:
        return None, {}
    inv = {sv: pv for pv, sv in S.ren.items()}
    def pre(B):
        return bdd.exist(S.pvars, bdd.apply('and', T, bdd.let(inv, B)))
    res = {}
    for (l0, ph, tc) in uniform_targets(S):
        Back = tc; Fr = tc; lev = 0
        st = 'HIT' if (succ0 & Back) != bdd.false else None
        while st is None:
            new = pre(Fr) & ~Back
            if new == bdd.false: st = 'CLOSED'; break
            Back = Back | new; Fr = new; lev += 1
            if (succ0 & Back) != bdd.false: st = 'HIT'
        res[(l0, ph)] = (st, S.count(Back) if st == 'CLOSED' else None)
    return True, res

def main():
    b = int(sys.argv[1]); pmin = int(sys.argv[2]); pmax = int(sys.argv[3]); maxw = int(sys.argv[4]) if len(sys.argv) > 4 else 10**9
    bad = 0; ntar = 0; nwords = 0; nhit = 0
    for p in range(pmin, pmax + 1):
        wf = f"/tmp/claude-0/diff_w_{b}_{p}.txt"
        if os.path.exists(wf): os.remove(wf)
        subprocess.run(['./bwdcensus_n', str(b), str(p), str(p), '-dumpw', wf, '-genonly'], capture_output=True, text=True)
        allw = [w.strip() for w in open(wf)] if os.path.exists(wf) else []
        step = max(1, len(allw) // maxw) if maxw < len(allw) else 1
        words = allw[::step]
        out = subprocess.run(['./bwdwords', str(b), '-f1cap', '2', '-bcap', '300000', '-v'], input='\n'.join(words) + '\n', capture_output=True, text=True).stdout
        ehit = set(); eund = set(); eclosed = {}
        for ln in out.splitlines():
            m = re.match(r'(HITFWD|SCC) p=(\d+) g=([01]+) .*?loop0=(\d+) ph=(\d+)', ln)
            if m: ehit.add((m.group(3), int(m.group(4)), int(m.group(5))))
            m = re.match(r'UNDECIDED p=(\d+) g=([01]+) loop0=(\d+) ph=(\d+)', ln)
            if m: eund.add((m.group(2), int(m.group(3)), int(m.group(4))))
            m = re.match(r'TARGET p=(\d+) g=([01]+) loop0=(\d+) ph=(\d+) CLOSED cone=(\d+)', ln)
            if m: eclosed[(m.group(2), int(m.group(3)), int(m.group(4)))] = int(m.group(5))
        for w in words:
            nwords += 1
            ok, res = sym_decide(b, w)
            for (l0, ph), (st, cone) in res.items():
                key = (w, l0, ph)
                if key in eund: continue
                ntar += 1
                e_hit = key in ehit
                s_hit = st == 'HIT'
                if e_hit != s_hit:
                    bad += 1; print("MISMATCH", b, p, w, l0, ph, 'explicit_hit', e_hit, 'sym', st)
                if s_hit: nhit += 1
                if key in eclosed and st == 'CLOSED' and eclosed[key] != int(cone):
                    bad += 1; print("CONE-MISMATCH", b, p, w, l0, ph, eclosed[key], cone)
        print(f"b={b} p={p} words={len(words)} cumulative targets={ntar} hits={nhit} bad={bad}", flush=True)
    print("DONE bad=", bad)

if __name__ == '__main__':
    main()
