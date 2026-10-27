#!/usr/bin/env python3
"""Independent exact-language audit of the uniform cyclic image construction.

No center arithmetic or production automata code is imported. Two independently
organized finite transducers (delayed output and required coefficient) are
compared by exact DFA product reachability, so those comparisons have no word
length cutoff. Bounded explicit relational enumeration and backward witnesses
are additional controls. A table-filling minimizer tests canonical equality of
partial DFAs, including explicit dead arcs and unreachable accepting states.

Run: python3 calculation/agent-111/regular_audit.py
This audits algorithms on synthetic languages, not a decimal certificate.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from functools import lru_cache
from itertools import product
import json
import random


@dataclass(frozen=True)
class DFA:
    edges: tuple[tuple[tuple[int, int], ...], ...]
    accepting: frozenset[int]

    def accepts(self, word):
        q = 0
        for letter in word:
            q = dict(self.edges[q]).get(letter, -1)
            if q < 0:
                return False
        return q in self.accepting


EMPTY = DFA(((),), frozenset())


def typed(kind, local):
    if not 0 <= kind < 2**32 or not 0 <= local < 2**32:
        raise ValueError("typed symbol outside its two 32-bit fields")
    return (kind << 32) | local


def encode(kind, y, coefficient):
    if coefficient not in (-1, 0, 1):
        raise ValueError("coefficient outside synthetic audit alphabet")
    return typed(kind, 3 * y + coefficient + 1)


def decode(letter):
    y, c = divmod(letter & (2**32 - 1), 3)
    return letter >> 32, y, c - 1


def from_words(words):
    edges, accepting = [{}], set()
    for word in words:
        q = 0
        for letter in word:
            if letter not in edges[q]:
                edges[q][letter] = len(edges)
                edges.append({})
            q = edges[q][letter]
        accepting.add(q)
    return DFA(tuple(tuple(sorted(x.items())) for x in edges), frozenset(accepting))


def distinguish(left, right):
    """Return a separating word, or None for exact equality at every length."""
    queue = deque([(0, 0, ())])
    seen = {(0, 0)}
    while queue:
        lq, rq, word = queue.popleft()
        if (lq in left.accepting) != (rq in right.accepting):
            return word
        le = dict(left.edges[lq]) if lq >= 0 else {}
        re = dict(right.edges[rq]) if rq >= 0 else {}
        for letter in sorted(le.keys() | re.keys()):
            pair = (le.get(letter, -1), re.get(letter, -1))
            if pair not in seen:
                seen.add(pair)
                queue.append((*pair, word + (letter,)))
    return None


def productive_trim(dfa):
    reverse = [[] for _ in dfa.edges]
    for q, edges in enumerate(dfa.edges):
        for _, target in edges:
            reverse[target].append(q)
    good, queue = set(dfa.accepting), deque(dfa.accepting)
    while queue:
        for q in reverse[queue.popleft()]:
            if q not in good:
                good.add(q)
                queue.append(q)
    if 0 not in good:
        return EMPTY
    ids, states, edges = {0: 0}, [0], []
    for q in states:
        row = []
        for letter, target in sorted(dfa.edges[q]):
            if target in good:
                if target not in ids:
                    ids[target] = len(states)
                    states.append(target)
                row.append((letter, ids[target]))
        edges.append(tuple(row))
    return DFA(tuple(edges), frozenset(ids[q] for q in states if q in dfa.accepting))


def canonical(dfa):
    """Independent pair-distinguishability minimizer, with an implicit sink."""
    dfa = productive_trim(dfa)
    n = len(dfa.edges)
    if n > 500:
        raise RuntimeError("synthetic audit minimization budget exceeded")
    alphabet = sorted({letter for row in dfa.edges for letter, _ in row})
    rows = [dict(row) for row in dfa.edges] + [{}]
    delta = [[row.get(letter, n) for letter in alphabet] for row in rows]
    different = [[(a in dfa.accepting) != (b in dfa.accepting)
                  for b in range(n + 1)] for a in range(n + 1)]
    changed = True
    while changed:
        changed = False
        for a in range(n + 1):
            for b in range(a):
                if not different[a][b] and any(different[x][y]
                        for x, y in zip(delta[a], delta[b])):
                    different[a][b] = different[b][a] = True
                    changed = True
    representative = [next(b for b in range(a + 1) if not different[a][b])
                      for a in range(n)]
    start = representative[0]
    ids, states, output = {start: 0}, [start], []
    for q in states:
        row = []
        for letter, target in dfa.edges[q]:
            target = representative[target]
            if target not in ids:
                ids[target] = len(states)
                states.append(target)
            row.append((letter, ids[target]))
        output.append(tuple(row))
    return DFA(tuple(output), frozenset(ids[q] for q in states if q in dfa.accepting))


class NFA:
    def __init__(self):
        self.edges = []
        self.accepting = set()
        self.starts = set()

    def state(self, accepting=False):
        q = len(self.edges)
        self.edges.append({})
        if accepting:
            self.accepting.add(q)
        return q

    def arc(self, source, letter, target):
        self.edges[source].setdefault(letter, set()).add(target)

    def determinize(self):
        if not self.starts:
            return EMPTY
        initial = frozenset(self.starts)
        ids, states, output, accepting = {initial: 0}, [initial], [], set()
        for subset in states:
            if subset & self.accepting:
                accepting.add(ids[subset])
            moves = {}
            for q in subset:
                for letter, targets in self.edges[q].items():
                    moves.setdefault(letter, set()).update(targets)
            row = []
            for letter, targets in sorted(moves.items()):
                target = frozenset(targets)
                if target not in ids:
                    if len(states) >= 5000:
                        raise RuntimeError("synthetic audit determinization budget exceeded")
                    ids[target] = len(states)
                    states.append(target)
                row.append((letter, ids[target]))
            output.append(tuple(row))
        return DFA(tuple(output), frozenset(accepting))


def delayed_image(dfa, relation):
    # The cyclic relation is defined on nonempty words: image(L - {epsilon}).
    nfa = NFA()
    terminal = nfa.state(accepting=True)
    ids, pending = {}, []

    def state(key):
        if key not in ids:
            ids[key] = nfa.state()
            pending.append(key)
        return ids[key]

    for letter, q in dfa.edges[0]:
        for y, first in relation.get(letter, ()):
            nfa.starts.add(state((q, letter >> 32, y, first)))
    for key in pending:
        q, kind, previous_y, first = key
        source = ids[key]
        if q in dfa.accepting:
            nfa.arc(source, encode(kind, previous_y, first), terminal)
        for letter, target in dfa.edges[q]:
            for y, c in relation.get(letter, ()):
                child = state((target, letter >> 32, y, first))
                nfa.arc(source, encode(kind, previous_y, c), child)
    return nfa.determinize()


def required_image(dfa, relation):
    """Independent direct-output transducer, guessing the next coefficient."""
    coefficients = sorted({c for rows in relation.values() for _, c in rows})
    nfa, ids, pending = NFA(), {}, []

    def state(key):
        if key not in ids:
            q, required, first, consumed = key
            ids[key] = nfa.state(consumed and q in dfa.accepting and required == first)
            pending.append(key)
        return ids[key]

    for first in coefficients:
        nfa.starts.add(state((0, first, first, False)))
    for key in pending:
        q, required, first, _ = key
        for letter, target in dfa.edges[q]:
            for y, c in relation.get(letter, ()):
                if c == required:
                    for next_c in coefficients:
                        nfa.arc(ids[key], encode(letter >> 32, y, next_c),
                                state((target, next_c, first, True)))
    return nfa.determinize()


def words_up_to(dfa, maximum):
    result, pending = set(), [(0, ())]
    for q, word in pending:
        if q in dfa.accepting:
            result.add(word)
        if len(word) < maximum:
            pending.extend((target, word + (letter,)) for letter, target in dfa.edges[q])
        if len(pending) > 1000000:
            raise RuntimeError("synthetic audit word budget exceeded")
    return result


def explicit_image(words, relation):
    result = set()
    for word in words:
        if not word:
            continue
        for choices in product(*(relation.get(letter, ()) for letter in word)):
            result.add(tuple(encode(letter >> 32, choices[i][0],
                                    choices[(i + 1) % len(word)][1])
                             for i, letter in enumerate(word)))
    return result


def predecessor(dfa, relation, target):
    if not target:
        return None
    decoded = [decode(letter) for letter in target]

    @lru_cache(None)
    def visit(i, q):
        if i == len(target):
            return () if q in dfa.accepting else None
        kind, y, _ = decoded[i]
        row = (y, decoded[(i - 1) % len(target)][2])
        for letter, child in dfa.edges[q]:
            if letter >> 32 == kind and row in relation.get(letter, ()):
                suffix = visit(i + 1, child)
                if suffix is not None:
                    return (letter,) + suffix
        return None

    return visit(0, 0)


def perturb(dfa):
    """Split equivalent states; add explicit dead arcs and unreachable accepts."""
    n, noise = len(dfa.edges), typed(7, 999)
    rows, accepting = [], set()
    for q, edges in enumerate(dfa.edges):
        for copy in range(2):
            rows.append(tuple(sorted([(letter, 2 * target + ((copy + letter) & 1))
                                      for letter, target in edges] + [(noise, 2 * n)])))
            if q in dfa.accepting:
                accepting.add(2 * q + copy)
    rows.extend((((noise, 2 * n),), ((noise, 2 * n + 1),)))
    accepting.add(2 * n + 1)
    return DFA(tuple(rows), frozenset(accepting))


def audit_temporal_mapping():
    """Check wrapped unit segments against direct chronological phase order."""
    cases = 0
    for period in range(1, 10):
        for trims in product((0, 1), repeat=period):
            if not any(trims):
                continue
            segments = []
            for trim in range(period):
                if trims[trim]:
                    segment = [(trim + 1) % period]
                    while not trims[segment[-1]]:
                        segment.append((segment[-1] + 1) % period)
                    segments.append(segment)
            anchor = segments[0][0]
            for repeats in (1, 2, 3, 5):
                total = period * repeats
                actual = [((i // len(segments)) * period + phase +
                           (period if phase < anchor else 0)) % total
                          for i in range(len(segments) * repeats)
                          for phase in segments[i % len(segments)]]
                expected = [(anchor + j) % total for j in range(total)]
                if actual != expected:
                    raise AssertionError("wrapped segment columns lost temporal alignment")
                cases += 1
    return cases


def audit():
    rng = random.Random(11110)
    alphabet = [typed(kind, local) for kind in range(2) for local in range(2)]
    universe = list(product(range(2), (-1, 0, 1)))
    models = []
    for _ in range(60):
        n = rng.randrange(2, 6)
        edges = tuple(tuple((letter, rng.randrange(n)) for letter in alphabet
                            if rng.random() < .4) for _ in range(n))
        dfa = DFA(edges, frozenset(q for q in range(1, n) if rng.random() < .5))
        relation = {letter: tuple(rng.sample(universe, rng.randrange(3)))
                    for letter in alphabet}
        models.append((dfa, relation, 4))
    a, b = typed(0, 1), typed(1, 1)
    alternating = DFA((((a, 1),), ((b, 2),), ((a, 1),)), frozenset({2}))
    identity = {a: ((0, 0),), b: ((0, 0),)}
    models += [(alternating, identity, 8),
               (alternating, {a: ((0, -1), (1, 0)), b: ((0, 0), (1, 1))}, 8),
               (from_words({(a,), (a, a), (a, a, a)}), {a: ((0, -1), (1, 0), (1, 0))}, 3),
               (EMPTY, identity, 4),
               (from_words({()}), identity, 4),
               (DFA((((a, 0), (b, 0)),), frozenset({0})), identity, 5)]
    # Two correlated words; coordinate projection would incorrectly admit four.
    correlated = from_words({(typed(0, 0), typed(1, 0)), (typed(0, 1), typed(1, 1))})
    models.append((correlated, {letter: ((letter & 1, 0),) for letter in alphabet}, 2))
    exact_checks = finite_words = backward_checks = canonical_checks = 0
    max_states = 0
    for dfa, relation, bound in models:
        delayed, required = delayed_image(dfa, relation), required_image(dfa, relation)
        max_states = max(max_states, len(delayed.edges), len(required.edges))
        if distinguish(delayed, required) is not None:
            raise AssertionError("infinite regular image languages differ")
        exact_checks += 1
        if canonical(delayed) != canonical(required):
            raise AssertionError("canonical equality differs from product equivalence")
        expected = explicit_image(words_up_to(dfa, bound), relation)
        actual = words_up_to(delayed, bound)
        if actual != expected or () in actual:
            raise AssertionError("regular image differs from explicit finite relation")
        if {len(word) for word in actual} - {len(word) for word in words_up_to(dfa, bound)}:
            raise AssertionError("cyclic image introduced a new word length")
        finite_words += len(actual)
        for target in rng.sample(sorted(actual), min(20, len(actual))):
            old = predecessor(dfa, relation, target)
            if old is None or not dfa.accepts(old) or target not in explicit_image({old}, relation):
                raise AssertionError("backward extraction lost a full accepted input path")
            backward_checks += 1
        noisy = perturb(dfa)
        if distinguish(dfa, noisy) is not None or canonical(dfa) != canonical(noisy):
            raise AssertionError("explicit rejecting sink changed a partial-DFA language")
        canonical_checks += 1
    if canonical(delayed_image(alternating, identity)) != canonical(alternating):
        raise AssertionError("identity failed on the infinite (A B)+ language")
    if words_up_to(delayed_image(alternating, {}), 8):
        raise AssertionError("changed local relation reused a previous image")
    rotated = DFA((((b, 1),), ((a, 2),), ((b, 1),)), frozenset({2}))
    if distinguish(alternating, rotated) is None:
        raise AssertionError("typed phase rotation was silently identified")
    if len(explicit_image(words_up_to(correlated, 2), models[-1][1])) != 2:
        raise AssertionError("correlated control lost its two-word scope")
    positive_words = DFA((((a, 1), (b, 1)), ((a, 1), (b, 1))), frozenset({1}))
    for fn in (delayed_image, required_image):
        if distinguish(fn(from_words({()}), identity), EMPTY) is not None:
            raise AssertionError("image of the empty-word-only language is nonempty")
        star = DFA((((a, 0), (b, 0)),), frozenset({0}))
        if distinguish(fn(star, identity), positive_words) is not None:
            raise AssertionError("removing epsilon also removed valid nonempty loops")
    return {"exact_regular_language_comparisons": exact_checks,
            "bounded_explicit_output_words": finite_words,
            "backward_predecessor_checks": backward_checks,
            "partial_dfa_canonical_checks": canonical_checks,
            "largest_unminimized_dfa": max_states,
            "empty_word_controls": 4,
            "anchor_temporal_mapping_cases": audit_temporal_mapping()}


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True))
