#!/usr/bin/env python3
"""Exact sink peeling of the uniformly padded exterior B map using digit MDDs.

Fixed width W, arbitrary temporal period and overflow stream. Source digits
are coefficients 0..2b-2, with positive lowest coefficient. A padded edge
trims exactly g neutral coefficients. EMPTY excludes cycles at this width;
a nonempty FIXED_POINT is an invariant survival set, including cycle basins.
It guarantees a B cycle by finiteness, but supplies no B/C certificate.
"""
from __future__ import annotations

import argparse
import math
import resource
import sys
import time


def cut_step(base, slot, x, high_next):
    """One exact exterior column, or None if its high carry is inconsistent."""
    g, low, high, pending = slot
    if (x+high_next)//base != high:
        return None
    low_next = (x+low)//base
    right = (x+high_next)%base
    output = (x+low)%base + (pending if g else right)
    inner = (g,low_next,high_next,right if g else 0)
    return inner,output


class BudgetExceeded(RuntimeError):
    pass


class MDD:
    """Canonical, level-preserving ordered digit decision diagram."""
    def __init__(self, base, width, node_cap=1_000_000,
                 cache_cap=2_000_000, seconds=300):
        max_width = min(128,(sys.getrecursionlimit()-100)//4)
        if not isinstance(base,int) or not 2 <= base <= 62:
            raise ValueError("base must be an integer in2..62")
        if not isinstance(width,int) or not 0 <= width <= max_width:
            raise ValueError(f"width must be an integer in0..{max_width} for recursion safety")
        if (not isinstance(node_cap,int) or not isinstance(cache_cap,int)
                or min(node_cap,cache_cap) <= 0):
            raise ValueError("node and cache caps must be positive integers")
        if not math.isfinite(seconds) or seconds <= 0:
            raise ValueError("time cap must be positive and finite")
        self.base,self.width,self.arity = base,width,2*base-1
        self.node_cap,self.cache_cap = node_cap,cache_cap
        self.started,self.seconds = time.monotonic(),seconds
        self.nodes = [None,None]  # false and terminal true
        self.unique = {}
        self.union_cache = {}
        self.pre_cache = {}
        self.count_cache = {0:0,1:1}
        self.operations = 0
        self.peak_nodes = 0
        self.peak_cache = 0

    def budget(self):
        self.operations += 1
        if self.operations % 4096 == 0 and time.monotonic()-self.started > self.seconds:
            raise BudgetExceeded(f"time cap {self.seconds}s")
        if len(self.nodes)-2 > self.node_cap:
            raise BudgetExceeded(f"node cap {self.node_cap}")
        if len(self.union_cache)+len(self.pre_cache) > self.cache_cap:
            raise BudgetExceeded(f"cache cap {self.cache_cap}")

    def node(self, level, children):
        self.budget()
        children = tuple(children)
        if not any(children):
            return 0
        key = (level,children)
        old = self.unique.get(key)
        if old is not None:
            return old
        if len(self.nodes)-2 >= self.node_cap:
            raise BudgetExceeded(f"node cap {self.node_cap}")
        result = len(self.nodes)
        self.nodes.append(key)
        self.unique[key] = result
        self.peak_nodes = max(self.peak_nodes,len(self.nodes)-2)
        return result

    def remember(self, cache, key, value):
        if len(self.union_cache)+len(self.pre_cache) >= self.cache_cap:
            raise BudgetExceeded(f"cache cap {self.cache_cap}")
        cache[key] = value
        self.peak_cache = max(self.peak_cache,len(self.union_cache)+len(self.pre_cache))

    def union(self, a, b):
        if a == b or b == 0:
            return a
        if a == 0:
            return b
        if a > b:
            a,b = b,a
        key = (a,b)
        old = self.union_cache.get(key)
        if old is not None:
            return old
        self.budget()
        if a == 1 or b == 1:
            raise AssertionError("terminal/internal union is not level-preserving")
        la,ca = self.nodes[a]
        lb,cb = self.nodes[b]
        if la != lb:
            raise AssertionError("MDD union level mismatch")
        result = self.node(la,[self.union(x,y) for x,y in zip(ca,cb)])
        self.remember(self.union_cache,key,result)
        return result

    def full(self):
        node = 1
        for level in range(self.width-1,-1,-1):
            children = [node]*self.arity
            if level == 0:
                children[0] = 0
            node = self.node(level,children)
        return node

    def count(self, node):
        old = self.count_cache.get(node)
        if old is not None:
            return old
        result = sum(self.count(c) for c in self.nodes[node][1])
        self.count_cache[node] = result
        return result

    def contains(self, node, word):
        if len(word) != self.width:
            return False
        for level,x in enumerate(word):
            if node <= 1 or not 0 <= x < self.arity:
                return False
            ll,children = self.nodes[node]
            if ll != level:
                raise AssertionError("MDD membership level mismatch")
            node = children[x]
        return node == 1

    def pre(self, target, slot):
        if target == 0:
            return 0
        key = (target,slot)
        old = self.pre_cache.get(key)
        if old is not None:
            return old
        self.budget()
        g,low,high,pending = slot
        if target == 1:
            result = int(low+high == 1 and (not g or pending == (self.base-1)*low))
        else:
            level,outputs = self.nodes[target]
            children = [0]*self.arity
            for x in range(1 if level == 0 else 0,self.arity):
                for hn in (0,1):
                    step = cut_step(self.base,slot,x,hn)
                    if step is None:
                        continue
                    inner,y = step
                    if outputs[y] == 0:
                        continue
                    piece = self.pre(outputs[y],inner)
                    children[x] = self.union(children[x],piece)
            result = self.node(level,children)
        self.remember(self.pre_cache,key,result)
        return result

    def preimage(self, target):
        return self.union(self.pre(target,(0,0,0,0)),
                          self.pre(target,(1,0,1,1)))

    def reachable_nodes(self, root):
        seen = set()
        stack = [root]
        while stack:
            u = stack.pop()
            if u < 2 or u in seen:
                continue
            seen.add(u)
            stack.extend(self.nodes[u][1])
        return len(seen)

    def collect(self, root):
        """Copy just the retained root DAG; callers compare roots BEFORE this."""
        seen = set()
        stack = [root]
        while stack:
            u = stack.pop()
            if u < 2 or u in seen:
                continue
            seen.add(u)
            stack.extend(self.nodes[u][1])
        old = self.nodes
        self.nodes = [None,None]
        self.unique = {}
        self.union_cache = {}
        self.pre_cache = {}
        self.count_cache = {0:0,1:1}
        mapped = {0:0,1:1}
        for u in sorted(seen):
            level,children = old[u]
            # Children are interned before their parent, so their old IDs are smaller.
            mapped[u] = self.node(level,[mapped[c] for c in children])
        return mapped[root]


def run(base=10, width=5, rounds=100, node_cap=1_000_000,
        cache_cap=2_000_000, seconds=300, quiet=False, collect=True):
    if not isinstance(rounds,int) or rounds < 0:
        raise ValueError("round bound must be a nonnegative integer")
    mdd = MDD(base,width,node_cap,cache_cap,seconds)
    root = mdd.full()
    records = []
    status = 'UNDECIDED'
    for iteration in range(rounds+1):
        words = mdd.count(root)
        rec = dict(iteration=iteration,words=words,
                   reachable_nodes=mdd.reachable_nodes(root),
                   allocated_nodes=len(mdd.nodes)-2,
                   pre_cache=len(mdd.pre_cache),union_cache=len(mdd.union_cache))
        records.append(rec)
        if not quiet:
            print(' '.join(f'{k}={v}' for k,v in rec.items()),flush=True)
        if root == 0:
            status = 'EMPTY'
            break
        if iteration == rounds:
            break
        nxt = mdd.preimage(root)
        if nxt == root:
            status = 'FIXED_POINT'
            break
        if mdd.count(nxt) >= words:
            raise AssertionError("strictly descending sets must strictly lose words")
        root = nxt
        if collect:
            root = mdd.collect(root)
    summary = dict(status=status,base=base,width=width,iteration=iteration,
                   words=mdd.count(root),seconds=round(time.monotonic()-mdd.started,3),
                   peak_nodes=mdd.peak_nodes,peak_cache=mdd.peak_cache,
                   maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if not quiet:
        print(' '.join(f'{k}={v}' for k,v in summary.items()),flush=True)
    return summary,records


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--base',type=int,default=10)
    p.add_argument('--width',type=int,default=5)
    p.add_argument('--rounds',type=int,default=100)
    p.add_argument('--node-cap',type=int,default=1_000_000)
    p.add_argument('--cache-cap',type=int,default=2_000_000)
    p.add_argument('--seconds',type=float,default=300)
    p.add_argument('--no-collect',action='store_true',help='retain intermediate DAGs and caches')
    a = p.parse_args()
    if min(a.node_cap,a.cache_cap) <= 0 or a.seconds <= 0:
        p.error('node/cache/time caps must be positive')
    result,_ = run(a.base,a.width,a.rounds,a.node_cap,a.cache_cap,a.seconds,collect=not a.no_collect)
    if result['status'] == 'UNDECIDED':
        raise SystemExit(2)


if __name__ == '__main__':
    try:
        main()
    except (BudgetExceeded,MemoryError,RuntimeError) as error:
        print(f'UNDECIDED: {error}',file=sys.stderr,flush=True)
        raise SystemExit(2)
    except ValueError as error:
        print(f'INVALID INPUT: {error}',file=sys.stderr,flush=True)
        raise SystemExit(2)
