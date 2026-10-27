#!/usr/bin/env python3
"""Independent arithmetic and language audit of the P24 exterior engine.

The reference image uses a dense, statically indexed product and its own
normalization equations.  Complete subset/product searches compare languages;
finite word counts are separate controls, never a completeness claim.  All
checks raise explicit exceptions, including under python -O.

  python3 calculation/agent-106/p24_exterior_regular_audit.py
  python3 -O calculation/agent-106/p24_exterior_regular_audit.py
"""

from collections import Counter, deque
from itertools import product
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import p24_exterior_regular as subject
import neutral_band_search as mirror

COUNTS = Counter()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def integer_value(base, coefficients):
    value = 0
    for x in reversed(coefficients):
        value = base * value + x
    return value


def integer_digits(base, value, width=0):
    result = []
    while value or len(result) < width:
        value, digit = divmod(value, base)
        result.append(digit)
    return tuple(result)


def encode(driver, phase, low, high, previous=0):
    return 4 * driver.base * phase + 2 * driver.base * low + driver.base * high + previous


def local_reference(driver, symbol, coefficient):
    """Enumerate chronological coefficient/carry solutions, independently."""
    phase, suffix = divmod(symbol, 4 * driver.base)
    low, suffix = divmod(suffix, 2 * driver.base)
    high, previous = divmod(suffix, driver.base)
    b = driver.base
    require(0 <= phase < driver.period and (driver.g[phase] or previous == 0),
            "reference received an untyped letter")
    result = []
    for inward in range(2):
        low_digit = (coefficient + low) % b
        low_out = (coefficient + low - low_digit) // b
        reverse_digit = coefficient + inward - b * high
        if not 0 <= reverse_digit < b:
            continue
        successor = low_digit + (previous if driver.g[phase] else reverse_digit)
        output = encode(driver, phase, low_out, inward,
                        reverse_digit if driver.g[phase] else 0)
        result.append((output, successor))
    return tuple(result)


def cut_symbol(driver, coefficients, inward, cut):
    """A cut of phase zero, using whole integers for both directed carries."""
    b, n = driver.base, len(coefficients)
    low = integer_value(b, coefficients[:cut]) // b ** cut
    high = (integer_value(b, coefficients[cut:][::-1]) + inward) // b ** (n - cut)
    previous = (1 if cut == 0 else (coefficients[cut - 1] + high) % b)
    return encode(driver, 0, low, high, previous if driver.g[0] else 0)


def arithmetic_controls():
    typed = whole_edges = whole_tiles = 0
    drivers = [subject.DEFAULT] + [subject.Driver(b, (0, 1), (0, 1)) for b in range(2, 9)]
    for driver in drivers:
        for t in range(driver.period):
            for low, high in product(range(2), repeat=2):
                for previous in range(driver.base if driver.g[t] else 1):
                    symbol = encode(driver, t, low, high, previous)
                    require(driver.decode(symbol) == (t, low, high, previous), "typed encoding mismatch")
                    for x in range(2 * driver.base - 1):
                        require(subject.tiles(symbol, x, driver) == local_reference(driver, symbol, x),
                                "typed local relation mismatch")
                        typed += 1
    samples = []
    for b in range(2, 6):
        for width in range(1, 4):
            for head in range(1, 2 * b - 1):
                for suffix in product(range(2 * b - 1), repeat=width - 1):
                    for inward in range(2):
                        samples.append((b, (head,) + suffix, inward))
    rng = random.Random(1062401)
    for _ in range(256):
        b, n = rng.choice((2, 4, 10, 11, 17, 26)), rng.randrange(1, 33)
        word = (rng.randrange(1, 2 * b - 1),) + tuple(rng.randrange(2 * b - 1) for _ in range(n - 1))
        samples.append((b, word, rng.randrange(2)))
    for b, word, inward in samples:
        n = len(word)
        whole = word + (2 * (b - 1) * inward,) + word[::-1]
        digits = integer_digits(b, integer_value(b, whole))
        g = len(digits) - (2 * n + 1)
        require(g in (0, 1), "ordinary integer overflow is not a bit")
        target = tuple(digits[j] + digits[-j - 1] for j in range(n))
        driver = subject.Driver(b, (g,), (0,))
        symbols = [cut_symbol(driver, word, inward, j) for j in range(n + 1)]
        require(symbols[0] == encode(driver, 0, 0, g, 1 if g else 0), "physical root mismatch")
        for j in range(n):
            require((symbols[j + 1], target[j]) in local_reference(driver, symbols[j], word[j]),
                    "ordinary integer contradicts a local tile")
            whole_tiles += 1
        whole_edges += 1
    return {"typed_cases": typed, "whole_integer_edges": whole_edges, "whole_integer_tiles": whole_tiles}


def nfa_dfa_equivalent(nfa, dfa, cap=200000):
    """Complete reachable subset/product search; absent arcs reject."""
    initial = (frozenset(nfa.initials), dfa.start)
    seen, stack = {initial}, [initial]
    while stack:
        states, q = stack.pop()
        if bool(states & nfa.finals) != (q in dfa.finals):
            return False, len(seen)
        choices = {}
        for old in states:
            for label, target in nfa.transitions[old]:
                choices.setdefault(label, set()).add(target)
        row = dfa.transitions[q] if q >= 0 else {}
        for label in choices.keys() | row.keys():
            target = (frozenset(choices.get(label, ())), row.get(label, -1))
            if target not in seen:
                seen.add(target)
                require(len(seen) <= cap, "independent language audit exceeded its explicit state cap")
                stack.append(target)
    return True, len(seen)


def as_nfa(dfa):
    return subject.NFA(frozenset((dfa.start,)), dfa.finals,
                       tuple(tuple(row.items()) for row in dfa.transitions))


def same_language(left, right):
    return nfa_dfa_equivalent(as_nfa(left), right)


def terminal_reference(dfa, driver):
    """Character-level product with the positive periodic target language."""
    unit = tuple(encode(driver, t, e, 1 - e, (driver.base - 1) * e if driver.g[t] else 0)
                 for t, e in enumerate(driver.e))
    initial = (dfa.start, 0, False)
    seen, queue = {initial}, deque(((initial, 0),))
    while queue:
        (q, phase, started), length = queue.popleft()
        if started and phase == 0 and q in dfa.finals:
            return length // len(unit)
        successor = dfa.transitions[q].get(unit[phase])
        if successor is not None:
            target = (successor, (phase + 1) % len(unit), True)
            if target not in seen:
                seen.add(target)
                queue.append((target, length + 1))
    return None


def dense_image_reference(dfa, driver, first=False):
    """All (input node, initial coefficient, current coefficient), not BFS."""
    ports = 2 * driver.base - 1
    index = lambda q, initial, current: (q * ports + initial) * ports + current
    rows = []
    finals = set()
    for q, row in enumerate(dfa.transitions):
        for initial in range(ports):
            for current in range(ports):
                state = index(q, initial, current)
                if q in dfa.finals and initial == current:
                    finals.add(state)
                outgoing = []
                if not first or current > 0:
                    for label, q2 in row.items():
                        for output, successor in local_reference(driver, label, current):
                            outgoing.append((output, index(q2, initial, successor)))
                rows.append(tuple(outgoing))
    initials = frozenset(index(dfa.start, a, a) for a in range(1 if first else 0, ports))
    return subject.NFA(initials, frozenset(finals), tuple(rows))


def mask_reference(dfa, driver, first=False):
    """Forward reachability from every small (q,x), independently of masks."""
    ports = 2 * driver.base - 1
    result = []
    for q in range(dfa.nodes):
        for x in range(ports):
            seen, stack, bits = {(q, x)}, [(q, x)], 0
            while stack:
                current_q, current = stack.pop()
                if current_q in dfa.finals and (not first or current > 0):
                    bits |= 1 << current
                if first and current == 0:
                    continue
                for symbol, target_q in dfa.transitions[current_q].items():
                    for _, successor in local_reference(driver, symbol, current):
                        target = (target_q, successor)
                        if target not in seen:
                            seen.add(target)
                            stack.append(target)
            result.append(bits)
    return result


def audit_image(dfa, driver, first=False, masks=True):
    reference = dense_image_reference(dfa, driver, first)
    pruned = subject.image(dfa, driver=driver, first=first, pretrim=True)
    unpruned = subject.image(dfa, driver=driver, first=first, pretrim=False)
    require(nfa_dfa_equivalent(reference, pruned)[0], "dense reference/pruned image mismatch")
    require(nfa_dfa_equivalent(reference, unpruned)[0], "dense reference/unpruned image mismatch")
    require(same_language(pruned, unpruned)[0], "pretrim changes the complete language")
    require(subject.terminal_intersection(pruned, driver) == terminal_reference(pruned, driver),
            "periodic-terminal intersection mismatch")
    COUNTS["dense_image_cases"] += 1
    COUNTS["terminal_cases"] += 1
    if masks:
        labels = {a for row in dfa.transitions for a in row}
        local = {a: tuple(subject.tiles(a, x, driver) for x in range(driver.ports)) for a in labels}
        measured = subject.coaccessibility_masks(dfa, local, driver=driver, first=first)
        require(measured == mask_reference(dfa, driver, first), "coaccessibility masks mismatch")
        COUNTS["mask_product_states"] += len(measured)
    return pruned


def head_step(x, inward):
    digits = integer_digits(10, integer_value(10, (x, 18 * inward, x)))
    return len(digits) - 3, digits[0] + digits[-1]


def head_histories(length):
    """Chronological walks; close only after the requested whole length."""
    result = []
    for start in range(1, 19):
        viable = [set() for _ in range(length + 1)]
        viable[length].add(start)
        for t in range(length - 1, -1, -1):
            for x in range(1, 19):
                for inward in range(2):
                    g, successor = head_step(x, inward)
                    if g == subject.G[t % 24] and successor in viable[t + 1]:
                        viable[t].add(x)
        def visit(t, x, heads, highs, letters):
            if t == length:
                require(x == start, "chronological endpoint failed")
                result.append((tuple(heads), tuple(highs), tuple(letters)))
                return
            for inward in range(2):
                g, successor = head_step(x, inward)
                if g == subject.G[t % 24] and successor in viable[t + 1]:
                    letter = encode(subject.DEFAULT, t % 24, x // 10, inward, (x + inward) % 10 if g else 0)
                    visit(t + 1, successor, heads + [x], highs + [inward], letters + [letter])
        if start in viable[0]:
            visit(0, start, [], [], [])
    return result


def first_language_controls():
    relation = {}
    for start in range(1, 19):
        states = {start}
        for g in subject.G[:12]:
            states = {successor for x in states for inward in range(2)
                      for overflow, successor in (head_step(x, inward),) if overflow == g}
        if states:
            relation[start] = states
    require(relation == {9: set(range(8, 19))}, "12-phase endpoint relation changed")
    unit = head_histories(12)
    head = (9, 10, 1, 2, 5, 11, 2, 5, 10, 1, 2, 4)
    require(len(unit) == 8 and all(xs == head for xs, _, _ in unit), "closed head profile mismatch")
    choices = tuple(tuple(sorted({hs[t] for _, hs, _ in unit})) for t in range(12))
    require(choices == ((1,), (0, 1), (0,), (1,), (1,), (0, 1),
                        (1,), (0,), (0, 1), (0,), (0,), (1,)), "free carry positions changed")
    require({hs for _, hs, _ in unit} == set(product(*choices)), "head carry choices are coupled")
    # A different DFA construction: final state zero on a cycle, plus a fresh
    # nonfinal initial state.  The 12-phase endpoint relation proves that its
    # independent choices characterize all 24*k closed head walks, for any k.
    rows = []
    for t in range(24):
        x = head[t % 12]
        rows.append({encode(subject.DEFAULT, t, x // 10, h,
                            (x + h) % 10 if subject.G[t] else 0): (t + 1) % 24
                     for h in choices[t % 12]})
    rows.append(dict(rows[0]))
    expected = subject.DFA(24, frozenset((0,)), tuple(rows))
    require(same_language(expected, subject.first_language())[0], "closed-form all-k language mismatch")
    actual = audit_image(subject.physical_root_language(), subject.DEFAULT, first=True)
    require(same_language(expected, actual)[0], "root image all-k language mismatch")
    counts = {}
    for length, count in ((24, 64), (48, 4096)):
        histories = head_histories(length)
        words = {word for _, _, word in histories}
        require(len(words) == len(histories) == count, "finite-lap head census mismatch")
        require(all(subject.accepts(actual, word) for word in words), "first image drops a head history")
        counts[length] = count
    return {"unit_words": 8, "one_lap": counts[24], "two_laps": counts[48],
            "complete_language_nodes": actual.nodes, "complete_language_edges": actual.edges}


def check_quotient(source, target, mapping):
    require(len(mapping) == source.nodes and mapping[source.start] == target.start,
            "independent quotient start mismatch")
    require(set(mapping) == set(range(target.nodes)), "independent quotient is not onto")
    for state in range(source.nodes):
        mapped = mapping[state]
        require((state in source.finals) == (mapped in target.finals), "independent quotient final mismatch")
        require(set(source.transitions[state]) == set(target.transitions[mapped]),
                "independent quotient missing/extra labels")
        for a, successor in source.transitions[state].items():
            require(mapping[successor] == target.transitions[mapped][a], "independent quotient target mismatch")


def automata_controls():
    rng = random.Random(1062402)
    cases = [subject.NFA(frozenset((0,)), frozenset((0,)), (((0, 0), (1, 1)), ((1, 1),), ())),
             subject.NFA(frozenset((0,)), frozenset((1,)), (((0, 0), (0, 1)), ((1, 1),), ((2, 1),))),
             subject.NFA(frozenset(), frozenset(), ())]
    for _ in range(24):
        n = rng.randrange(2, 8)
        rows = tuple(tuple((a, v) for a in range(3) for v in range(n) if rng.randrange(7) == 0)
                     for _ in range(n))
        cases.append(subject.NFA(frozenset(q for q in range(n) if rng.randrange(3) == 0),
                                 frozenset(q for q in range(n) if rng.randrange(3) == 0), rows))
    product_states = 0
    for nfa in cases:
        trimmed = subject.trim_nfa(nfa, subject.Budget())
        determined = subject.determinize(trimmed)
        source, reduced, mapping = subject.minimize(determined, return_map=True)
        check_quotient(source, reduced, mapping)
        for dfa in (determined, reduced):
            equal, states = nfa_dfa_equivalent(nfa, dfa)
            require(equal, "automata transformation changes complete language")
            product_states += states
    left = subject.DFA(0, frozenset((1,)), ({0: 1}, {0: 1}))
    right = subject.DFA(0, frozenset((1,)), ({1: 1}, {1: 1}))
    require((left.nodes, left.edges) == (right.nodes, right.edges), "same-size negative control malformed")
    require(not same_language(left, right)[0] and not subject.equivalent(left, right),
            "same-size different languages falsely identified")
    caught = 0
    for check in (lambda: check_quotient(left, right, (0, 1)),
                  lambda: subject.validate_quotient(left, right, (0, 1))):
        try:
            check()
        except ValueError:
            caught += 1
    require(caught == 2, "missing-label quotient guards failed")
    try:
        subject.run(budget=subject.Budget(), max_layers=1)
    except subject.Limited as exc:
        require(str(exc) == "layer_cap", "wrong capped-run reason")
        caught += 1
    require(caught == 3, "capped nonexhausted run did not remain undecided")
    driver = subject.Driver(2, (1,), (0,))
    label = encode(driver, 0, 0, 1, 0)
    terminal_cases = ((subject.DFA(0, frozenset((0,)), ({label: 1}, {label: 0})), 2),
                      (subject.DFA(0, frozenset((2,)), ({label: 1}, {label: 0}, {})), None),
                      (subject.DFA(0, frozenset((0,)), ({},)), None))
    for dfa, expected in terminal_cases:
        require(terminal_reference(dfa, driver) == expected and
                subject.terminal_intersection(dfa, driver) == expected,
                "positive-lap terminal control failed")
        COUNTS["terminal_cases"] += 1
    return {"nfa_cases": len(cases), "complete_product_states": product_states, "negative_guards": caught + 1}


def whole_word_closure_control():
    driver = subject.Driver(2, (1,), (0,))
    # Source 4^+.  Coefficients 0 -> 1 -> 0 close over two laps, and output
    # letters are 0,5.  Requiring closure after each lap destroys this walk.
    source = subject.DFA(0, frozenset((1,)), ({4: 1}, {4: 1}))
    target = audit_image(source, driver)
    require((0, 1) in local_reference(driver, 4, 0) and
            (5, 0) in local_reference(driver, 4, 1), "whole-word fixture tiles changed")
    require(subject.accepts(target, (0, 5)) and subject.accepts(target, (0, 5, 0, 5)),
            "an intermediate final incorrectly blocks continuation")
    require(not subject.accepts(target, (0,)) and not subject.accepts(target, (5,)),
            "whole-word fixture unexpectedly closes in one lap")
    return {"base": 2, "source_unit": 4, "accepted_two_lap_word": (0, 5)}


def known_base_controls():
    findings = []
    fixtures = {b: es for b, es in mirror._lean_certs() if b in (2, 4)}
    require(set(fixtures) == {2, 4}, "known-base fixture extraction failed")
    for b, edges in sorted(fixtures.items()):
        require(mirror.cycleOK(b, edges, edges[0][0], edges[0][1]), "existing positive fixture rejected")
        e = tuple(mirror.e1(b, edge[0]) for edge in edges)
        g = tuple(mirror.gam(b, edge[0], edge[1]) for edge in edges)
        driver = subject.Driver(b, g, e)
        width = max(len(edge[0]) for edge in edges)
        require(width == 2, "known-base small fixture width changed")
        padded = [tuple(edge[0]) + (b - 1,) * (width - len(edge[0])) for edge in edges]
        for t, word in enumerate(padded):
            center = edges[t][1]
            require(mirror.hyp(b, list(word), center), "padded known source violates Hyp")
            expected = padded[(t + 1) % len(edges)] + (b - 1,) * g[t]
            require(tuple(mirror.nextB(b, list(word), center)) == expected,
                    "known padded exterior edge does not close")
        cut_words = []
        for j in range(width + 1):
            letters = []
            for t, word in enumerate(padded):
                single = subject.Driver(b, (g[t],), (e[t],))
                letters.append(cut_symbol(single, word, 1 - e[t], j) + 4 * b * t)
            cut_words.append(tuple(letters))
        layer = subject.physical_root_language(driver)
        require(subject.accepts(layer, cut_words[0]), "known root word rejected")
        for j in range(1, width + 1):
            layer = audit_image(layer, driver, first=j == 1)
            require(subject.accepts(layer, cut_words[j]), "known positive cut word rejected")
        require(cut_words[-1] == driver.terminal_word(), "known cut does not reach the exact terminal")
        require(subject.terminal_intersection(layer, driver) == 1, "known positive terminal omitted")
        findings.append({"base": b, "period": len(edges), "width": width, "terminal_laps": 1})
    return findings


def center_control():
    e = tuple(map(int, "010100110100101011001011"))
    g = tuple(map(int, "110001001000110001001000"))
    v = tuple(map(int, "100001000000100001000000"))
    initial = (9, 14, 13, 18, 13, 14, 9)
    dummy = {(0, 0): (1,), (0, 1): (9,), (1, 0): (1, 10), (1, 1): (10,)}
    center = initial
    max_width = len(center)
    for t in range(24):
        exterior = list(dummy[e[t], g[t]])
        require(mirror.hyp(10, exterior, list(center)), "center fixture violates Hyp")
        require(mirror.e1(10, exterior) == e[t] and mirror.e2(10, exterior, list(center)) == 1 - e[t]
                and mirror.gam(10, exterior, list(center)) == g[t], "center driver mismatch")
        value = integer_value(10, center) + e[t]
        require(value // 10 ** len(center) == 1 - e[t], "ordinary center carry mismatch")
        digits = integer_digits(10, value % 10 ** len(center), len(center))
        if g[t]:
            digits += (9 * e[t],)
        reference = tuple(digits[j] + digits[-j - 1] for j in range(len(digits)))
        raw = tuple(mirror.nextC(10, exterior, list(center)))
        require(raw == reference, "ordinary center update disagrees with mirror")
        if v[t]:
            require(raw[0] == raw[-1] == 9 and len(raw) >= 2, "center trim is not neutral")
            center = raw[1:-1]
        else:
            center = raw
        max_width = max(max_width, len(center))
    require(center == initial and sum(g) == 8 and sum(v) == 4, "24-phase center does not close")
    return {"period": 24, "sum_g": sum(g), "sum_v": sum(v), "max_width": max_width,
            "scope": "center only; the dummy exteriors do not form a B cycle"}


def main():
    results = (("arithmetic", arithmetic_controls()),
               ("first_language", first_language_controls()),
               ("automata", automata_controls()),
               ("whole_word_closure", whole_word_closure_control()),
               ("known_bases", known_base_controls()),
               ("center24", center_control()))
    for name, result in results:
        print(name, result)
    print("image_and_terminal_controls", dict(COUNTS))
    print("AUDIT PASSED: arithmetic, complete-language controls, masks, known positives, center24")
    print("Scope: this audit does not prove a decimal exterior cycle or all-width exhaustion.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
