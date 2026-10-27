#!/usr/bin/env python3
"""Audit all B periods with a selected overflow budget using the head bound.

The integer potential is a finite certificate for P <= 4G. The B arithmetic
comes from the existing repository automaton; a result requires EXHAUSTED.
Outputs are summaries, never a claim that a capped search is negative.
"""
import argparse
import itertools
import json
import subprocess
import time


def head_edges():
    edges = {x: set() for x in range(1, 19)}
    for x in edges:
        for carry in (0, 1):
            overflow = int(x + carry >= 10)
            y = x % 10 + 1 if overflow else 2*x + carry
            edges[x].add((overflow, y))
    return edges


def potential_certificate():
    edges = head_edges()
    potential = {x: 0 for x in edges}
    for _ in range(100):
        updated = {x: max([0] + [1-4*g+potential[y] for g,y in es])
                   for x,es in edges.items()}
        if updated == potential:
            break
        potential = updated
    else:
        raise RuntimeError("No finite potential: period bound NOT established")
    if any(1 > 4*g+potential[x]-potential[y]
           for x, es in edges.items() for g,y in es):
        raise RuntimeError("Invalid potential certificate")
    return [potential[x] for x in range(1,19)]


def necklaces(period, weight):
    for indices in itertools.combinations(range(period), weight):
        word = ['0']*period
        for i in indices:
            word[i] = '1'
        word = ''.join(word)
        if word == min(word[i:]+word[:i] for i in range(period)):
            yield word


def head_admissible(word):
    edges = head_edges()
    for initial in edges:
        current = {initial}
        for bit in word:
            current = {y for x in current for g,y in edges[x] if g == int(bit)}
            if not current:
                break
        if initial in current:
            return True
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--solver', required=True)
    parser.add_argument('--weights', nargs='+', type=int, default=[2,4])
    parser.add_argument('--cap', type=int, default=2000000)
    parser.add_argument('--seconds', type=float, default=30)
    parser.add_argument('--budget', type=float, default=1200)
    args = parser.parse_args()
    if any(g not in (2,4,6) for g in args.weights):
        parser.error('supported weights: 2, 4, 6')
    print('POTENTIAL', json.dumps(potential_certificate()), flush=True)
    started=time.monotonic()
    totals={'necklaces':0,'head_survivors':0,'exhausted':0,'undecided':0}
    accepted=[]
    for weight in args.weights:
        for period in range(weight, 4*weight+1):
            row={'period':period,'weight':weight,'necklaces':0,'head_survivors':0,
                 'exhausted':0,'undecided':0,'max_states':0,'max_depth':0,'accepted':[]}
            for word in necklaces(period,weight):
                row['necklaces'] += 1
                if not head_admissible(word):
                    continue
                row['head_survivors'] += 1
                if time.monotonic()-started >= args.budget:
                    row['undecided'] += 1
                    print('UNDECIDED',word,'GLOBAL_BUDGET',flush=True)
                    continue
                try:
                    proc=subprocess.run([args.solver,word,str(args.cap),str(args.seconds)],
                                        text=True,capture_output=True,timeout=args.seconds+15)
                except subprocess.TimeoutExpired:
                    row['undecided'] += 1
                    print('UNDECIDED',word,'EXTERNAL_TIMEOUT',flush=True)
                    continue
                if proc.returncode not in (0,3):
                    raise RuntimeError((word,proc.returncode,proc.stdout,proc.stderr))
                result=json.loads(proc.stdout)
                complete=result['status']=='EXHAUSTED' and proc.returncode==0
                row['exhausted' if complete else 'undecided'] += 1
                row['max_states']=max(row['max_states'],result['states'])
                row['max_depth']=max(row['max_depth'],result['depth'])
                if not complete:
                    print('UNDECIDED',json.dumps(result,sort_keys=True),flush=True)
                if result['accepted']:
                    hit={'g':word,'complete':complete,'streams':result['accepted']}
                    row['accepted'].append(hit); accepted.append(hit)
            for key in totals:
                totals[key] += row[key]
            print('PERIOD',json.dumps(row,sort_keys=True),flush=True)
    print('SUMMARY',json.dumps(totals,sort_keys=True),flush=True)
    print('ACCEPTED',json.dumps(accepted,sort_keys=True),flush=True)
    if totals['undecided']:
        raise SystemExit(3)


if __name__=='__main__':
    main()
