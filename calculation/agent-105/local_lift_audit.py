#!/usr/bin/env python3
"""Independent exact finite-width completions of abstract center-prefix edges.

The solver keeps both normalization carries while choosing paired coefficients
from the outside inward.  A SAT result supplies one full symmetric center and
its exact canonical successor; it does not connect independently chosen edges
into a full center cycle.  Completion counts are exact for the specified width.

Example: python3 calculation/agent-105/local_lift_audit.py --selftest --details
"""
from functools import lru_cache
from itertools import product
import argparse
import importlib.util
import json
from pathlib import Path
import random
import sys


def center_step(c, e, g, base=10):
    carry = e
    digits = []
    for a in c:
        digits.append((a + carry) % base)
        carry = (a + carry) // base
    if carry != 1-e:
        return None
    if g:
        digits.append((base-1)*e)
    raw = tuple(a+b for a,b in zip(digits, reversed(digits)))
    v = 0
    while len(raw) >= 2 and raw[0] == raw[-1] == base-1:
        raw = raw[1:-1]
        v += 1
    if not raw or raw[0] == base-1:
        return None
    return raw, v


def lift_edge(source, target, e, g, v, width, base=10, require_even_middle=False):
    """Solve one exact local edge; all returned counts concern this width only."""
    if type(base) is not int or base < 2 or type(width) is not int or width < 1:
        raise ValueError("invalid base or source width")
    if e not in (0,1) or g not in (0,1) or type(v) is not int or v < 0:
        raise ValueError("invalid driver or trim")
    source, target = tuple(source), tuple(target)
    h = base-1
    if not source or not target or any(type(a) is not int or not 0 <= a <= 2*h for a in source+target):
        raise ValueError("invalid coefficient prefixes")
    out_width = width+g-2*v
    result = {"status":"UNSAT", "source_width":width, "target_width":out_width,
              "completion_count":0, "dp_states":0, "even_middle":require_even_middle}
    if out_width < len(target) or width < len(source) or source[0] == h or target[0] == h:
        return result
    fixed = {}
    for i,a in enumerate(source):
        j = min(i,width-1-i)
        if j in fixed and fixed[j] != a:
            return result
        fixed[j] = a
    raw_length = width+g
    required = {}
    for i,a in enumerate((h,)*v+target):
        if i >= raw_length:
            return result
        j = min(i,raw_length-1-i)
        if j in required and required[j] != a:
            return result
        required[j] = a
    half = (width+1)//2

    @lru_cache(None)
    def solve(i, left, right, previous_high):
        if i == half:
            return 1, ()
        choices = (fixed[i],) if i in fixed else range(2*base-1)
        count, example = 0, None
        for a in choices:
            if width%2 and i == half-1 and require_even_middle and a%2:
                continue
            low, next_left = (a+left)%base, (a+left)//base
            if width%2 and i == half-1:
                incoming = (left,) if next_left == right else ()
            else:
                incoming = range(2)
            for next_right in incoming:
                if (a+next_right)//base != right:
                    continue
                if width%2 == 0 and i == half-1 and next_right != next_left:
                    continue
                high = (a+next_right)%base
                raw = low + (high if not g else h*e if i == 0 else previous_high)
                if i in required and required[i] != raw:
                    continue
                if width%2 == 0 and i == half-1 and g:
                    if half in required and required[half] != 2*high:
                        continue
                n, tail = solve(i+1,next_left,next_right,high if g else -1)
                count += n
                if example is None and n:
                    example = (a,)+tail
        return count, example

    count, example = solve(0,e,1-e,-1)
    result.update(completion_count=count,dp_states=solve.cache_info().currsize)
    if count:
        full = example+example[:width//2][::-1]
        actual = center_step(full,e,g,base)
        if actual is None or len(actual[0]) != out_width or actual[1] != v or actual[0][:len(target)] != target:
            raise ArithmeticError("paired carry solver produced an invalid full edge")
        result.update(status="SAT",source=list(full),target=list(actual[0]),trim=v)
    return result


def symmetric_words(base,width):
    for a in product(range(2*base-1),repeat=(width+1)//2):
        yield a+a[:width//2][::-1]


def brute_count(source,target,e,g,v,width,base,even_middle):
    n = 0
    for c in symmetric_words(base,width):
        if c[:len(source)] != tuple(source) or c[0] == base-1:
            continue
        if even_middle and width%2 and c[width//2]%2:
            continue
        out = center_step(c,e,g,base)
        if out is not None and out[1] == v and out[0][:len(target)] == tuple(target):
            n += 1
    return n


def selftest():
    rng = random.Random(105_2026_27)
    checks = 0
    for base,maxwidth in ((2,7),(3,6),(10,4)):
        for width in range(1,maxwidth+1):
            for _ in range(20):
                a = tuple(rng.randrange(2*base-1) for _ in range((width+1)//2))
                c = a+a[:width//2][::-1]
                if c[0] == base-1:
                    continue
                e,g = int(c[0]<base-1),rng.randrange(2)
                out = center_step(c,e,g,base)
                if out is None:
                    continue
                dst,v = out
                src = c[:min(width,2)]
                target = dst[:min(len(dst),2)]
                for mutated in (False,True):
                    y = target
                    if mutated:
                        y = target[:-1]+((target[-1]+1)%(2*base-1),)
                        if y[0] == base-1:
                            continue
                    for even in (False,True):
                        answer = lift_edge(src,y,e,g,v,width,base,even)
                        expected = brute_count(src,y,e,g,v,width,base,even)
                        if answer["completion_count"] != expected:
                            raise AssertionError((base,width,src,y,e,g,v,even,answer,expected))
                        checks += 1
    print(json.dumps({"paired_carry_vs_bruteforce":checks,"status":"PASS"}))


def load_module(name,path):
    spec = importlib.util.spec_from_file_location(name,path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def integer_mirror_check(lift,e,g,base,mirror):
    c = lift["source"]
    if len(c)%2 and c[len(c)//2]%2:
        raise ValueError("odd middle coefficient is not an ordinary pair word")
    bword = [base if g else 1,0,base*e]
    if not mirror.hyp(base,bword,c) or (mirror.e1(base,bword),mirror.gam(base,bword,c)) != (e,g):
        raise ArithmeticError("control exterior has incorrect drivers")
    c2,v = center_step(c,e,g,base)
    if tuple(mirror.nextC(base,bword,c)) != (base-1,)*v+c2+(base-1,)*v:
        raise ArithmeticError("local center edge disagrees with repository mirror")
    gap = 3
    word = bword+[base-1]*gap+c+[base-1]*gap+bword[::-1]
    digits = [0]*len(word)
    for i in range(len(word)//2):
        digits[i] = max(0,word[i]-(base-1))
        digits[-1-i] = word[i]-digits[i]
    if len(word)%2:
        digits[len(word)//2] = word[len(word)//2]//2
    n = sum(a*base**i for i,a in enumerate(digits))
    reverse = sum(a*base**i for i,a in enumerate(digits[::-1]))
    total = n+reverse
    summed = []
    while total:
        total,a = divmod(total,base)
        summed.append(a)
    pair = [a+b for a,b in zip(summed,summed[::-1])]
    b2 = mirror.nextB(base,bword,c)
    expected = b2+[base-1]*(gap-g+v)+list(c2)+[base-1]*(gap-g+v)+b2[::-1]
    if pair != expected:
        raise ArithmeticError("ordinary integer reverse-add disagrees with local lift")


def audit(driver,width0,details=False):
    here = Path(__file__).resolve().parent
    prefix = load_module("a105_old_prefix",here/"prefix_budget.py")
    mirror = load_module("a105_local_mirror",here.parent/"neutral_band_search.py")
    e,g,k = ("10100110011","11100010000",1) if driver == "p11" else ("101010010101","100010001000",2)
    witness = prefix.find_closed(prefix.PrefixModel(4,10),e,g,k,30)
    if witness["status"] != "ABSTRACT_BUDGET_WITNESS":
        raise RuntimeError("old prefix witness unavailable")
    width, lifts = width0, []
    for edge in witness["path"]:
        got = lift_edge(edge["source"],edge["target"],edge["e"],edge["g"],edge["v"],width,10,True)
        got["phase"] = edge["t"]
        if got["status"] == "SAT":
            integer_mirror_check(got,edge["e"],edge["g"],10,mirror)
        lifts.append(got)
        width += edge["g"]-2*edge["v"]
    if width != width0:
        raise ArithmeticError("trim budget does not close the length schedule")
    seams = []
    for t,lift in enumerate(lifts):
        nxt = lifts[(t+1)%len(lifts)]
        if lift["status"] == nxt["status"] == "SAT":
            if lift["target"] != nxt["source"]:
                at = next(i for i,(a,b) in enumerate(zip(lift["target"],nxt["source"])) if a != b)
                seams.append({"phase":t,"first_disagreement":at})
    summary = {"driver":driver,"initial_width":width0,"edge_count":len(lifts),
               "locally_SAT":sum(x["status"] == "SAT" for x in lifts),
               "UNSAT_phases":[x["phase"] for x in lifts if x["status"] != "SAT"],
               "completion_counts":[x["completion_count"] for x in lifts],
               "dp_states":sum(x["dp_states"] for x in lifts),
               "selected_completion_seam_mismatches":seams,
               "scope":"independent local edges only; no center cycle"}
    if details:
        summary["lifts"] = lifts
    print(json.dumps(summary))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--driver",choices=("p11","p12","both"),default="both")
    p.add_argument("--width",type=int,default=12)
    p.add_argument("--details",action="store_true")
    p.add_argument("--selftest",action="store_true")
    a = p.parse_args()
    if a.selftest:
        selftest()
    for driver in ("p11","p12") if a.driver == "both" else (a.driver,):
        audit(driver,a.width,a.details)


if __name__ == "__main__":
    main()
