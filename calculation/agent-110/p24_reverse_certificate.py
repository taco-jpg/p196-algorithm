#!/usr/bin/env python3
"""Independently check terminal membership, predecessor closure, FIRST separation.

Search flags, hashes, claimed cardinalities, and canonicalization are untrusted.
Local tiles are generated FORWARD, independently of the primary inverse code.
"""
import argparse
from bisect import bisect_left
import json
from pathlib import Path
import resource
import sys
import time


class Incomplete(Exception):
    pass


class Budget:
    def __init__(self, seconds=1500, operations=500_000_000, memory_mib=2048):
        self.start = time.monotonic()
        self.seconds, self.limit, self.memory = seconds, operations, memory_mib
        self.operations = 0

    def check_now(self):
        if time.monotonic()-self.start >= self.seconds:
            raise Incomplete('wall cap')
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform == 'darwin':
            rss //= 1024
        if rss > self.memory*1024:
            raise Incomplete('resident memory cap')

    def tick(self, amount=1):
        self.operations += amount
        if self.operations > self.limit:
            raise Incomplete('operation cap')
        if self.operations % 4096 < amount:
            self.check_now()


def integer(x):
    return type(x) is int


class Checker:
    def __init__(self, data, budget):
        self.budget = budget
        self.base = data['base']
        self.e, self.g = data['e'], data['g']
        if not integer(self.base) or not 2 <= self.base <= 62:
            raise ValueError('invalid base')
        if (not isinstance(self.e, str) or not isinstance(self.g, str)
                or not self.g or len(self.e) != len(self.g)
                or len(self.g) > 64 or set(self.e+self.g)-{'0','1'} or '1' not in self.g):
            raise ValueError('invalid fixed driver')
        self.p = len(self.g)
        starts = [t for t, bit in enumerate(self.g) if bit == '1']
        expected = [{'start':s, 'length':(starts[(i+1)%len(starts)]-s-1)%self.p+1}
                    for i,s in enumerate(starts)]
        blocks = data['blocks']
        if (not isinstance(blocks, list)
                or any(not isinstance(block, dict) or set(block) != {'start','length'}
                       or not integer(block['start']) or not integer(block['length'])
                       for block in blocks)
                or blocks != expected or any(block['length'] > 6 for block in expected)):
            raise ValueError('invalid or unsupported block partition')
        self.blocks, self.n = expected, len(expected)
        self.root, self.nodes = data['root'], data['nodes']
        if (not isinstance(self.nodes, list) or len(self.nodes) < 2
                or not integer(self.root) or not 0 <= self.root < len(self.nodes)):
            raise ValueError('invalid node list/root')
        for ident, level in ((0,0),(1,self.n)):
            node = self.nodes[ident]
            if (not isinstance(node,dict) or not integer(node['level'])
                    or node['level'] != level or not isinstance(node['arcs'],list)
                    or node['arcs']):
                raise ValueError('invalid reject/accept sentinels')
        self.labels, self.children = [(), ()], [(), ()]
        for ident, node in enumerate(self.nodes[2:], 2):
            self.budget.tick()
            if not isinstance(node,dict):
                raise ValueError('invalid node record')
            level, arcs = node['level'], node['arcs']
            if not integer(level) or not 0 <= level < self.n or not isinstance(arcs, list):
                raise ValueError('invalid explicit node level')
            bound = self.base << (2*self.blocks[level]['length'])
            previous = -1
            for arc in arcs:
                self.budget.tick()
                if not isinstance(arc, list) or len(arc) != 2:
                    raise ValueError('invalid arc record')
                label, child = arc
                if (not integer(label) or not previous < label < bound
                        or not integer(child) or not 0 <= child < len(self.nodes)):
                    raise ValueError('invalid or duplicate arc')
                if child and self.nodes[child]['level'] != level+1:
                    raise ValueError('skipped level or cyclic diagram')
                if child == 1 and level+1 != self.n:
                    raise ValueError('premature accept')
                previous = label
            self.labels.append(tuple(a[0] for a in arcs))
            self.children.append(tuple(a[1] for a in arcs))
        if self.root not in (0,1) and self.nodes[self.root]['level'] != 0:
            raise ValueError('root does not begin at level zero')
        if self.root == 1:
            raise ValueError('empty-word acceptance is unsupported')
        self.tiles, self.dead = {}, set()
        self.tiles_by_start = {}
        self.node_count, self.ports = len(self.nodes), 2*self.base-1

    def branch(self, node, label):
        if node < 2:
            return 0
        k = bisect_left(self.labels[node], label)
        return self.children[node][k] if k < len(self.labels[node]) and self.labels[node][k] == label else 0

    def contains(self, word):
        node = self.root
        for label in word:
            node = self.branch(node, label)
        return node == 1

    def symbols(self, low, high, lag):
        result = []
        for block in self.blocks:
            start, length = block['start'], block['length']
            L = sum(low[(start+j)%self.p] << j for j in range(length))
            H = sum(high[(start+j)%self.p] << j for j in range(length))
            result.append(L | (H << length) | (lag[start] << (2*length)))
        return tuple(result)

    def terminal(self):
        e = tuple(map(int, self.e))
        return self.symbols(e, tuple(1-x for x in e), tuple((self.base-1)*x for x in e))

    def first(self):
        """Literal positive FIRST-column enumeration in original time order."""
        b, p = self.base, self.p
        low, high, lag, column = [0]*p, [0]*p, [0]*p, [0]*p
        answers = {}
        def visit(t, x, initial):
            self.budget.tick()
            if t == p:
                if x == initial:
                    answers.setdefault(self.symbols(low,high,lag), tuple(column))
                return
            if not 1 <= x <= 2*b-2:
                return
            g = int(self.g[t])
            for incoming in (0,1):
                self.budget.tick()
                digit, outgoing = (x+incoming)%b, (x+incoming)//b
                if outgoing != g:
                    continue
                low[t], high[t], lag[t], column[t] = x//b, incoming, digit, x
                visit(t+1, x%b+(1 if g else digit), initial)
        for initial in range(1,2*b-1):
            visit(0,initial,initial)
        return answers

    def local_tiles(self, length, target):
        """Every (start-x,end-x,source-symbol,column), via FORWARD choices."""
        key = length,target
        if key in self.tiles:
            return self.tiles[key]
        b, mask = self.base,(1<<length)-1
        L,H,Y = target&mask,(target>>length)&mask,target>>(2*length)
        answer = set()
        def continuation(j,x,oldL,oldH,oldY,values):
            self.budget.tick()
            if j == length:
                source = oldL | (oldH<<length) | (oldY<<(2*length))
                answer.add((values[0],x,source,values))
                return
            carry_high = (H>>j)&1
            digit,previous_high = (x+carry_high)%b,(x+carry_high)//b
            for old_low in (0,1):
                self.budget.tick()
                if (x+old_low)//b != ((L>>j)&1):
                    continue
                continuation(j+1,(x+old_low)%b+digit,oldL|(old_low<<j),
                             oldH|(previous_high<<j),oldY,values+(x,))
        for x in range(2*b-1):
            if (x+(H&1))%b != Y:
                continue
            previous_high = (x+(H&1))//b
            for old_low in (0,1):
                self.budget.tick()
                if (x+old_low)//b != (L&1):
                    continue
                digit = (x+old_low)%b
                for oldY in range(b):
                    continuation(1,digit+oldY,old_low,previous_high,oldY,(x,))
        self.tiles[key] = tuple(sorted(answer))
        by_start = {}
        for row in self.tiles[key]:
            by_start.setdefault(row[0], []).append(row)
        self.tiles_by_start[key] = {start:tuple(rows) for start,rows in by_start.items()}
        return self.tiles[key]

    def counterexample(self,target,source,port,initial,level=0):
        self.budget.tick()
        if target == 0:
            return None
        if level == self.n:
            return () if target==1 and port==initial and source!=1 else None
        # Every node ID is in [0,node_count), and every coefficient port is
        # in [0,ports). Mixed-radix encoding is injective; Python integers
        # retain every bit. Node levels remain fixed, so target determines
        # the recursion level. This stores exactly the same memo relation.
        key = ((target*self.node_count+source)*self.ports+port)*self.ports+initial
        if key in self.dead:
            return None
        for label,child in zip(self.labels[target],self.children[target]):
            self.budget.tick()
            length = self.blocks[level]['length']
            self.local_tiles(length,label)
            for start,end,old,values in self.tiles_by_start[length,label].get(port,()):
                self.budget.tick()
                suffix = self.counterexample(child,self.branch(source,old),end,initial,level+1)
                if suffix is not None:
                    return ((label,old,values),)+suffix
        self.dead.add(key)
        return None

    def cardinality(self,node,memo):
        self.budget.tick()
        if node in memo:
            return memo[node]
        memo[node] = sum(self.cardinality(child,memo) for child in self.children[node])
        return memo[node]

    def check(self):
        if not self.contains(self.terminal()):
            return {'status':'TERMINAL_NOT_INCLUDED'}
        first = self.first()
        overlap = [word for word in first if self.contains(word)]
        if overlap:
            return {'status':'BOUNDARY_OVERLAP','first_states':len(first),'word':overlap[0],
                    'first_column':first[overlap[0]],'note':'set membership alone is not a B witness'}
        for initial in range(2*self.base-1):
            witness = self.counterexample(self.root,self.root,initial,initial)
            if witness is not None:
                return {'status':'NOT_PREDECESSOR_CLOSED','first_states':len(first),
                        'local_witness':witness,'initial_port':initial}
        return {'status':'PREDECESSOR_CLOSED_NO_EXTERIOR','first_states':len(first),
                'set_cardinality':self.cardinality(self.root,{0:0,1:1}),
                'product_states':len(self.dead),'tile_queries':len(self.tiles)}


def check(data,seconds=1500,operations=500_000_000,memory_mib=2048,budget=None):
    if budget is None:
        budget = Budget(seconds,operations,memory_mib)
    checker = None
    try:
        budget.check_now()
        checker = Checker(data,budget)
        result = checker.check()
        budget.check_now()
    except Incomplete as error:
        result = {'status':'UNDECIDED','reason':str(error)}
    except (KeyError,IndexError,TypeError,ValueError,OverflowError,RecursionError,MemoryError) as error:
        result = {'status':'UNDECIDED','reason':'invalid certificate or resource error: '+str(error)}
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == 'darwin':
        rss //= 1024
    result.update(operations=budget.operations,seconds=time.monotonic()-budget.start,
                  finished_product_states=len(checker.dead) if checker is not None else 0,
                  cached_tile_queries=len(checker.tiles) if checker is not None else 0,
                  peak_rss_kib=rss)
    return result


def selftest():
    c={'base':2,'e':'0','g':'1','blocks':[{'start':0,'length':1}],'root':2,
       'nodes':[{'level':0,'arcs':[]},{'level':1,'arcs':[]},{'level':0,'arcs':[[2,1]]}]}
    if check(c)['status'] != 'PREDECESSOR_CLOSED_NO_EXTERIOR':
        raise RuntimeError('hand-checked base2 negative fixture failed')
    c['root']=0
    if check(c)['status'] != 'TERMINAL_NOT_INCLUDED':
        raise RuntimeError('missing terminal was accepted')
    c['root']=2; c['nodes'][2]['arcs']=[[2,2]]
    if check(c)['status'] != 'UNDECIDED':
        raise RuntimeError('cyclic diagram was accepted')
    print(json.dumps({'status':'PASS','initial_fixtures':3}))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate',type=Path,nargs='?')
    parser.add_argument('--selftest',action='store_true')
    parser.add_argument('--seconds',type=float,default=1500)
    parser.add_argument('--operations',type=int,default=500_000_000)
    parser.add_argument('--memory-mib',type=int,default=2048)
    args=parser.parse_args()
    if args.selftest:
        selftest(); return 0
    if (args.certificate is None or not 0 < args.seconds <= 1500
            or args.operations < 1 or not 64 <= args.memory_mib <= 4096):
        parser.error('provide a certificate and valid resource limits')
    budget = Budget(args.seconds,args.operations,args.memory_mib)
    try:
        budget.check_now()
        # A CLI-wide address-space ceiling also covers uninterruptible JSON
        # allocation before periodic resident-memory checks can run.
        soft,hard = resource.getrlimit(resource.RLIMIT_AS)
        ceilings = [args.memory_mib*1024*1024]
        ceilings += [limit for limit in (soft,hard) if limit != resource.RLIM_INFINITY]
        resource.setrlimit(resource.RLIMIT_AS,(min(ceilings),hard))
        if args.certificate.stat().st_size > 128*1024*1024:
            raise Incomplete('input size cap')
        raw = args.certificate.read_text()
        budget.check_now()
        data = json.loads(raw)
        del raw
        budget.check_now()
        result = check(data,budget=budget)
    except (Incomplete,OSError,ValueError,OverflowError,RecursionError,MemoryError) as error:
        result = {'status':'UNDECIDED','reason':'input or resource error: '+str(error),
                  'operations':budget.operations,'seconds':time.monotonic()-budget.start}
    print(json.dumps(result,sort_keys=True))
    return 0 if result['status']=='PREDECESSOR_CLOSED_NO_EXTERIOR' else 2


if __name__=='__main__':
    raise SystemExit(main())
