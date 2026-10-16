"""Bounded counterexample-guided refinement with complete configurations.

At depth 4 use the saved minimized observer. Higher depths are exact lazy
carry-observer extensions; no unexplored transition is treated as absent.
A collision is an all-length class obstruction. Failure to find one is
UNKNOWN and is never a closure certificate.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / 'main_existence_attempt/return_pass/language'
sys.path.insert(0, str(SOURCE))
from residual_kernel import base_machine, START_FST, fst_edge


class Stored:
    def __init__(self, data):
        self.d = data['delta']
    def step(self, state, q):
        return self.d[state][q]


class Extension:
    def __init__(self, previous):
        self.previous = previous
        self.base = base_machine()[0]
        key = (0, tuple((st, 0) for st in START_FST))
        self.keys = [key]
        self.ids = {key: 0}
        self.edges = {}

    def step(self, state, q):
        cache_key = (state, q)
        cached = self.edges.get(cache_key)
        if cached is not None:
            return cached
        b, paths = self.keys[state]
        targets = set()
        for st, previous_state in paths:
            for ns, emitted in fst_edge(st, q):
                targets.add((ns, self.previous.step(previous_state, emitted)))
        key = (self.base[b][q], tuple(sorted(targets)))
        found = self.ids.get(key)
        if found is None:
            found = len(self.keys)
            self.ids[key] = found
            self.keys.append(key)
        self.edges[cache_key] = found
        return found


def folded(n):
    digits = str(n)
    return (tuple(int(digits[i])+int(digits[-i-1])
                  for i in range(len(digits)//2)),
            None if len(digits)%2 == 0 else 2*int(digits[len(digits)//2]))


def realize(pairs, center):
    return int(''.join(str(min(9, q)) for q in pairs) +
               ('' if center is None else str(center//2)) +
               ''.join(str(max(0, q-9)) for q in reversed(pairs)))


def run(max_depth, max_pairs, trace_steps, hit_cap, seconds):
    begin = time.monotonic()
    nfa_file = SOURCE / 'safe_image2_nfa.json'
    observer_file = SOURCE / 'observation_depth4.json'
    nfa = json.loads(nfa_file.read_text())
    d4 = json.loads(observer_file.read_text())
    trans = [dict(row) for row in nfa['transitions']]
    machines = [Stored(d4)]
    for _ in range(4, max_depth):
        machines.append(Extension(machines[-1]))

    def configuration(p):
        current = set(nfa['initial'])
        for q in p:
            current = {v for u in current for v in trans[u].get(q, ())}
        return tuple(sorted(current))

    def observations(p):
        states = [0] * len(machines)
        for q in p:
            states = [machine.step(s, q) for machine, s in zip(machines, states)]
        return tuple(states)

    trace = []
    targets = {}
    n = 196
    for t in range(trace_steps+1):
        p, c = folded(n)
        subset = configuration(p)
        obs = observations(p)
        row = dict(step=t, integer=str(n), pairs=p, center=c,
                   subset=subset, observer_states=obs)
        trace.append(row)
        targets.setdefault((obs[0], subset), {}).setdefault(c, []).append(t)
        n += int(str(n)[::-1])
    target_d4 = {key[0] for key in targets}
    hits = {}
    tested_words = set()
    candidates = 0
    target_matches = 0
    arithmetic_trials = 0
    progress = []
    next_log = begin + 5
    completed_lengths = []
    status = 'BOUNDED_REFINEMENT_COMPLETE_NO_INVARIANT'

    def examine(p, known_d4=None, source='enumeration'):
        nonlocal candidates, target_matches, arithmetic_trials
        p = tuple(p)
        candidates += 1
        if known_d4 is None:
            known_d4 = 0
            for q in p:
                known_d4 = d4['delta'][known_d4][q]
        if known_d4 not in target_d4:
            return
        subset = configuration(p)
        ending_map = targets.get((known_d4, subset))
        if ending_map is None:
            return
        obs = observations(p)
        for c, positions in ending_map.items():
            if not p and c in (None, 0):
                continue
            w = p, c
            if w in tested_words:
                continue
            tested_words.add(w)
            target_matches += 1
            useful = [(t, k) for t in positions for k in range(len(machines))
                      if obs[k] == trace[t]['observer_states'][k]
                      and (t, k) not in hits]
            if not useful:
                continue
            arithmetic_trials += 1
            n = realize(p, c)
            hit = None
            for h in range(1, hit_cap+1):
                n += int(str(n)[::-1])
                if str(n) == str(n)[::-1]:
                    hit = h
                    break
            if hit is None:
                continue
            for t, k in useful:
                hits[t, k] = dict(trace_step=t, depth=k+4, pairs=p, center=c,
                                  first_palindrome=hit, source=source,
                                  subset=subset, observer_state=obs[k])

    corpus_file = ROOT / 'main_existence_attempt/ancestry_direct_pass/language/terminal_acceptance_result.json'
    corpus = json.loads(corpus_file.read_text())
    for row in corpus['proofs']:
        examine(row['pairs'], source='prior_finite_witness_corpus')
    for length in range(max_pairs+1):
        if time.monotonic()-begin >= seconds:
            status = 'UNKNOWN_TIME_CAP'
            break
        if length == 0:
            examine(())
            completed_lengths.append(0)
            continue
        # Prefix state updates avoid re-running D4 on every full word.
        stack = [((), 0)]
        halted = False
        while stack:
            prefix, state = stack.pop()
            if len(prefix) == length:
                examine(prefix, state)
            else:
                alphabet = range(18, 0 if not prefix else -1, -1)
                stack.extend((prefix+(q,), d4['delta'][state][q]) for q in alphabet)
            now = time.monotonic()
            if now-begin >= seconds:
                status = 'UNKNOWN_TIME_CAP'
                halted = True
                break
            if now >= next_log:
                row = dict(seconds=now-begin, length=length, candidates=candidates,
                           target_matches=target_matches, arithmetic_trials=arithmetic_trials,
                           excluded_trace_classes=len(hits))
                progress.append(row)
                print(json.dumps(row), flush=True)
                # Retain actual obstruction words during long enumeration;
                # a process interruption must not turn progress counts into
                # the only surviving evidence.
                checkpoint = dict(status='UNKNOWN_CHECKPOINT', trace=trace,
                    max_depth=max_depth, completed_enumeration_lengths=completed_lengths,
                    excluded_trace_classes=len(hits),
                    collisions=[hits[key] for key in sorted(hits)],
                    progress=progress)
                (HERE/'correlated_cegar_checkpoint.json').write_text(
                    json.dumps(checkpoint, separators=(',', ':'))+'\n')
                next_log = now+5
        if halted:
            break
        completed_lengths.append(length)

    summary = dict(status=status, positive_invariant_found=False,
                   closure_status='NOT_PROVED', max_depth=max_depth,
                   max_pairs=max_pairs, completed_enumeration_lengths=completed_lengths,
                   trace_steps=trace_steps, orbit_limit=hit_cap, seconds_cap=seconds,
                   seconds=time.monotonic()-begin, candidates=candidates,
                   target_matches=target_matches, arithmetic_trials=arithmetic_trials,
                   excluded_trace_classes=len(hits),
                   furthest_excluded_trace_step_by_depth={str(k+4): max(
                       (t for t, j in hits if j == k), default=None)
                       for k in range(len(machines))},
                   lazy_observer_states={str(k+4): len(machine.keys)
                       for k, machine in enumerate(machines) if k},
                   nfa_sha256=hashlib.sha256(nfa_file.read_bytes()).hexdigest(),
                   observer4_sha256=hashlib.sha256(observer_file.read_bytes()).hexdigest(),
                   progress=progress)
    result = dict(summary, trace=trace, collisions=[hits[key] for key in sorted(hits)])
    (HERE/'correlated_cegar_result.json').write_text(json.dumps(result, separators=(',', ':'))+'\n')
    (HERE/'correlated_cegar_summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    checkpoint_path = HERE/'correlated_cegar_checkpoint.json'
    if checkpoint_path.exists():
        checkpoint_path.unlink()
    print(json.dumps(summary), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-depth', type=int, default=7)
    parser.add_argument('--max-pairs', type=int, default=5)
    parser.add_argument('--trace-steps', type=int, default=80)
    parser.add_argument('--orbit-limit', type=int, default=300)
    parser.add_argument('--seconds', type=float, default=180)
    a = parser.parse_args()
    run(a.max_depth, a.max_pairs, a.trace_steps, a.orbit_limit, a.seconds)
