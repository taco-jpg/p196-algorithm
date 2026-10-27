#!/usr/bin/env python3
"""Arithmetic fixtures for the independent P24 exterior-language review.

This file does not implement a tile relation or a language-image algorithm.
It reads explicit known certificate DATA from the baseline Lean sources,
replays them with whole positional integers, and supplies padded exterior
witnesses, including every spatial cut, for independent engine controls.

P24 center data: Agent101, PR381 at f29759a359d923c7d8c1a22d7e7aecde462d565a.
P24 one-lap cardinalities: Agent117, issue289 comment6433395207.  Comparing
these numbers is attributed corroboration, never a proof about all laps.
Optional base20 data: Agent116 PR356 at b7a718b78d67cf54d362232ba1b8f90fbec23af8.
The whole-integer checks are independent of the new block/automata engines.
"""
import argparse
from copy import deepcopy
from itertools import product
import json
from pathlib import Path
import re
import subprocess
import time


ROOT = Path(__file__).resolve().parents[2]
MAIN_PIN = "eafbbbfd6b5b857597f95f68268c56dbd96b6bcb"
P24_PIN = "f29759a359d923c7d8c1a22d7e7aecde462d565a"
P24_E = "010100110100101011001011"
P24_G = "110001001000110001001000"
P24_V = "100001000000100001000000"
P24_C0 = [9, 14, 13, 18, 13, 14, 9]
P24_LAYERS_SOURCE = "https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433395207"
P24_LAYERS = [
    1, 64, 256, 1088, 16752, 44368, 249216, 202564, 276380, 286144,
    220196, 187392, 151668, 256644, 245568, 244208, 369040, 444672,
    535936, 433352, 422000, 573536, 599296, 339168, 177672, 295192,
    339000, 235128, 136016, 261224, 306616, 208224, 214768, 166208,
    40592, 48288, 31232, 13248, 2560, 0,
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def positional_value(base, coefficients):
    value = 0
    for coefficient in reversed(coefficients):
        value = value * base + coefficient
    return value


def integer_normalization(base, coefficients, incoming=0):
    """One integer division; no per-column carry recurrence is used."""
    width = len(coefficients)
    quotient, remainder = divmod(positional_value(base, coefficients) + incoming,
                                 base ** width)
    digits = [(remainder // base ** j) % base for j in range(width)]
    require(quotient in (0, 1), "nonbinary normalization carry")
    return digits, quotient


def exterior(base, word):
    require(base >= 2 and all(isinstance(x, int) and 0 <= x <= 2 * base - 2
                             for x in word), "invalid exterior coefficients")
    require(not word or word[0] > 0, "zero exterior head")
    low, e = integer_normalization(base, word)
    high, g = integer_normalization(base, word[::-1], 1 - e)
    if g:
        low.append((base - 1) * (1 - e))
        high = [1] + high[::-1]
    else:
        high.reverse()
    require(len(low) == len(high), "exterior digit alignment mismatch")
    return [a + b for a, b in zip(low, high)], e, g


def center(base, word, e, g):
    require(e in (0, 1) and g in (0, 1), "nonbinary center driver")
    require(all(isinstance(x, int) and 0 <= x <= 2 * base - 2 for x in word),
            "invalid center coefficients")
    digits, outgoing = integer_normalization(base, word, e)
    require(outgoing == 1 - e, "center does not flip the carry")
    if g:
        a, b = digits + [(base - 1) * e], [(base - 1) * e] + digits[::-1]
    else:
        a, b = digits, digits[::-1]
    return [x + y for x, y in zip(a, b)]


def template_value(base, B, C, gap):
    require(gap >= 0, "negative template gap")
    neutral = [base - 1] * gap
    return positional_value(base, B + neutral + C + neutral + B[::-1])


def reverse_integer(base, number):
    answer = 0
    while number:
        number, digit = divmod(number, base)
        answer = answer * base + digit
    return answer


def split_top_level(text):
    fields, start, depth = [], 0, 0
    for i, char in enumerate(text):
        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
        elif char == "," and depth == 0:
            fields.append(text[start:i].strip())
            start = i + 1
    require(depth == 0, "unbalanced Lean data brackets")
    fields.append(text[start:].strip())
    return fields


def literal_list(text):
    require(re.fullmatch(r"\[\s*(?:\d+\s*(?:,\s*\d+\s*)*)?\]", text) is not None,
            "expected a literal natural-coefficient list")
    return list(map(int, re.findall(r"\d+", text)))


def load_baseline_certificates():
    paths = [
        ROOT / "lean/P196/Drafts/Agent120NeutralBandCalibration/A120PowerTwo.lean",
        ROOT / "lean/P196/Agent213KnownBaseMechanisms/KnownBases.lean",
    ]
    certificates = []
    for path in paths:
        source = path.read_text()
        lists = {m[1]: literal_list(m[2]) for m in re.finditer(
            r"def\s+(\w+)\s*:\s*List Nat\s*:=\s*(\[[^\]]*\])", source)}
        for match in re.finditer(r"def cert(\d+)\s*:\s*List Edge\s*:=\s*(.*?)\n\n",
                                 source, re.S):
            edges = []
            for body in re.findall(r"⟨([^⟩]*)⟩", match[2]):
                fields = split_top_level(body)
                require(len(fields) == 6, "Lean edge does not have six fields")
                words = [literal_list(field) if field.startswith("[") else lists[field][:]
                         for field in fields[:4]]
                require(all(field.isdigit() for field in fields[4:]), "invalid edge trims")
                edges.append(words + list(map(int, fields[4:])))
            require(edges, "empty parsed Lean certificate")
            certificates.append({"base": int(match[1]), "edges": edges,
                                 "source": str(path.relative_to(ROOT)), "pin": MAIN_PIN})
    require(sorted(row["base"] for row in certificates) == [2, 4, 8, 11, 16, 17, 26, 32],
            "baseline parser did not recover exactly the eight known bases")
    return sorted(certificates, key=lambda row: row["base"])


def replay_certificate(certificate):
    base, edges = certificate["base"], certificate["edges"]
    require(edges, "empty certificate data")
    gap, overflows, exterior_trims, center_trims = 6, 0, 0, 0
    previous = edges[0][:2]
    for index, edge in enumerate(edges):
        require(len(edge) == 6, "edge data must contain six fields")
        B, C, B2, C2, u, v = edge
        require([B, C] == previous, f"certificate discontinuity at edge {index}")
        require(isinstance(u, int) and u >= 0 and isinstance(v, int) and v >= 0,
                "invalid natural trim")
        raw_B, e, g = exterior(base, B)
        require(raw_B == B2 + [base - 1] * u, f"exterior replay failed at {index}")
        require(center(base, C, e, g) == [base - 1] * v + C2 + [base - 1] * v,
                f"center replay failed at {index}")
        before = template_value(base, B, C, gap)
        next_gap = gap + u + v - g
        require(before + reverse_integer(base, before) ==
                template_value(base, B2, C2, next_gap),
                f"whole reverse-add equality failed at {index}")
        previous, gap = [B2, C2], next_gap
        overflows += g
        exterior_trims += u
        center_trims += v
    require(previous == edges[0][:2], "certificate does not close")
    require(exterior_trims == overflows and 2 * center_trims == overflows,
            "closed length accounting failed")
    return {"base": base, "edges": len(edges), "G": overflows,
            "U": exterior_trims, "V": center_trims,
            "source": certificate["source"], "pin": certificate["pin"]}


def primitive_exterior(certificate):
    base, edges = certificate["base"], certificate["edges"]
    labels = [(edge[0], edge[2], edge[4]) for edge in edges]
    length = len(labels)
    period = next(p for p in range(1, length + 1) if length % p == 0 and
                  all(labels[t] == labels[t % p] for t in range(length)))
    words = [edge[0][:] for edge in edges[:period]]
    e, g = [], []
    for word in words:
        _, carry, overflow = exterior(base, word)
        e.append(carry)
        g.append(overflow)
    require(1 in g, "positive exterior control has no overflow")
    rotation = g.index(1)
    words = words[rotation:] + words[:rotation]
    e, g = e[rotation:] + e[:rotation], g[rotation:] + g[:rotation]
    return words, "".join(map(str, e)), "".join(map(str, g))


def replay_fixed_width(base, e, g, words):
    require(len(words) == len(e) == len(g) and words, "driver length mismatch")
    width = len(words[0])
    require(width > 0 and all(len(word) == width for word in words),
            "fixed-width witness has inconsistent or zero width")
    for t, word in enumerate(words):
        raw, carry, overflow = exterior(base, word)
        require((str(carry), str(overflow)) == (e[t], g[t]),
                f"fixed-width driver mismatch at phase {t}")
        require(raw == words[(t + 1) % len(words)] + [base - 1] * overflow,
                f"fixed-width boundary replay failed at phase {t}")
    return width


def integer_spatial_states(base, e, g, words):
    """Cut carries/digits directly from prefix/suffix positional integers."""
    width = replay_fixed_width(base, e, g, words)
    states = []
    for j in range(width + 1):
        L, H, Y = [], [], []
        for t, word in enumerate(words):
            incoming = 1 - int(e[t])
            L.append(positional_value(base, word[:j]) // base ** j)
            H.append((positional_value(base, word[j:][::-1]) + incoming) //
                     base ** (width - j))
            reverse_value = positional_value(base, word[::-1]) + incoming
            Y.append((1 if j == 0 else
                      (reverse_value // base ** (width - j)) % base) if g[t] == "1" else 0)
        states.append({"L": L, "H": H, "Y": Y})
    require(states[0] == {"L": [0] * len(e), "H": list(map(int, g)),
                          "Y": list(map(int, g))}, "physical FIRST tuple mismatch")
    require(states[-1] == {"L": list(map(int, e)),
                           "H": [1 - int(x) for x in e],
                           "Y": [(base - 1) * int(e[t]) if g[t] == "1" else 0
                                 for t in range(len(e))]}, "neutral terminal tuple mismatch")
    return states


def make_exterior_controls(certificate):
    base = certificate["base"]
    natural_words, e, g = primitive_exterior(certificate)
    width = max(1, max(map(len, natural_words)))
    rows, checked_edges = [], 0
    for extra in range(3):
        padded = [word + [base - 1] * (width + extra - len(word)) for word in natural_words]
        for k in (1, 2):
            words = deepcopy(padded * k)
            states = integer_spatial_states(base, e * k, g * k, words)
            checked_edges += len(words)
            if extra == 0:
                rows.append({"label": f"base{base}_k{k}", "base": base,
                             "primitive_e": e, "primitive_g": g,
                             "e": e * k, "g": g * k, "k": k,
                             "width": width, "B_words": words, "spatial_states": states,
                             "source": certificate["source"], "pin": certificate["pin"]})
    return rows, checked_edges


def base6_two_lap_control():
    """Agent105's physical B-only counterexample; no center is supplied."""
    source = "https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433504667"
    words = [[4, 7, 7, 8, 3], [9, 3, 4, 5, 8],
             [4, 7, 7, 10, 2, 2], [9, 3, 4, 9]]
    trims = [0, 0, 2, 0]
    for phase, word in enumerate(words):
        raw, e, g = exterior(6, word)
        require((e, g) == (phase % 2, phase % 2) and
                raw == words[(phase + 1) % 4] + [5] * trims[phase],
                "Agent105 base6 natural-trim control failed integer replay")
    words = words[1:] + words[:1]
    padded = [word + [5] * (6 - len(word)) for word in words]
    states = integer_spatial_states(6, "1010", "1010", padded)
    return {"label": "agent105_base6_k2", "base": 6, "primitive_e": "10", "primitive_g": "10",
            "e": "1010", "g": "1010", "k": 2, "width": 6, "B_words": padded,
            "spatial_states": states, "source": source,
            "scope": "attributed B-only two-lap positive; no center or new period-descent claim"}


def padding_controls():
    words_checked = padding_equalities = trim_equalities = 0
    for base in (2, 4, 10):
        h = base - 1
        for width in range(3):
            for word in product(range(2 * base - 1), repeat=width):
                if word and word[0] == 0:
                    continue
                word = list(word)
                raw, e, g = exterior(base, word)
                words_checked += 1
                for extra in (1, 2):
                    require(exterior(base, word + [h] * extra) == (raw + [h] * extra, e, g),
                            "neutral exterior padding covariance failed")
                    padding_equalities += 1
                target = raw[:]
                while True:
                    common = max(1, width, len(target))
                    padded_source = word + [h] * (common - width)
                    padded_target = target + [h] * (common - len(target))
                    require(exterior(base, padded_source) == (padded_target + [h] * g, e, g),
                            "arbitrary trim to fixed-width padding failed")
                    trim_equalities += 1
                    if not target or target[-1] != h:
                        break
                    target.pop()
    return {"words": words_checked, "padding_equalities": padding_equalities,
            "all_natural_trim_equalities": trim_equalities,
            "bases": [2, 4, 10], "maximum_original_width": 2}


def replay_p24_center():
    current = P24_C0[:]
    rows, padding_equalities = [], 0
    for t in range(48):
        phase = t % 24
        e, g, v = int(P24_E[phase]), int(P24_G[phase]), int(P24_V[phase])
        raw = center(10, current, e, g)
        require(len(raw) >= 2 * v and raw[:v] == [9] * v and
                (v == 0 or raw[-v:] == [9] * v), "P24 neutral center trim failed")
        following = raw[v:len(raw) - v] if v else raw[:]
        for extra in (1, 2):
            padded = [9] * extra + current + [9] * extra
            require(center(10, padded, e, g) == [9] * extra + raw + [9] * extra,
                    "P24 common center-padding covariance failed")
            padding_equalities += 1
        if t < 24:
            rows.append({"phase": t, "e": e, "g": g, "v": v,
                         "C": current[:], "C2": following[:]})
        current = following
        if (t + 1) % 24 == 0:
            require(current == P24_C0, "P24 center failed to close after a whole lap")
    return {"base": 10, "e": P24_E, "g": P24_G, "v": P24_V, "C0": P24_C0,
            "edges": rows, "replayed_edges": 48, "common_padding_equalities": padding_equalities,
            "widths": sorted({len(row["C"]) for row in rows}), "G": 8, "V": 4,
            "source": "https://github.com/taco-jpg/p196-algorithm/pull/381", "pin": P24_PIN}


def malformed_witness_controls(fixtures):
    original = next(row for row in fixtures if row["label"] == "base16_k1")
    rejected = 0
    for kind in ("e", "g", "coefficient", "width"):
        row = deepcopy(original)
        if kind in ("e", "g"):
            row[kind] = str(1 - int(row[kind][0])) + row[kind][1:]
        elif kind == "coefficient":
            row["B_words"][0][0] += 1
        else:
            row["B_words"][0].pop()
        try:
            replay_fixed_width(row["base"], row["e"], row["g"], row["B_words"])
        except ValueError:
            rejected += 1
        else:
            raise ValueError(f"malformed {kind} witness was accepted")
    return rejected


def check_p24_layers(events):
    """Only checks supplied finite-k=1 counts against the attributed source."""
    layers = [row for row in events if row.get("event") == "layer"]
    require(layers, "no layer records to compare")
    for expected_depth, row in enumerate(layers):
        depth = row["depth"]
        require(depth == expected_depth and depth < len(P24_LAYERS),
                "P24 layer indices are not a supported complete prefix")
        require(row.get("k_counts") and int(row["k_counts"][0]) == P24_LAYERS[depth],
                f"P24 one-lap cardinality disagrees at depth {depth}")
        require(row.get("target_hit_k") != 1, "engine claims a forbidden P24 one-lap terminal")
    return {"status": "PASS", "compared_layers": len(layers),
            "maximum_depth": layers[-1]["depth"], "k": 1,
            "scope": "attributed finite-k cardinality control, not all-k evidence",
            "source": P24_LAYERS_SOURCE}


def fixture_cut_letters(fixture, depth):
    """Encode an integer-replayed cut using the public block-label format."""
    primitive = fixture["primitive_g"]
    period = len(primitive)
    starts = [t for t, bit in enumerate(primitive) if bit == "1"]
    state = fixture["spatial_states"][depth]
    letters = []
    for repetition in range(fixture["k"]):
        for index, start in enumerate(starts):
            end = starts[index + 1] if index + 1 < len(starts) else period
            length = end - start
            offset = repetition * period + start
            low = sum(state["L"][offset + j] << j for j in range(length))
            high = sum(state["H"][offset + j] << j for j in range(length))
            lag = state["Y"][offset]
            require(low < 2 ** length and high < 2 ** length and 0 <= lag < fixture["base"],
                    "integer fixture cut lies outside a typed alphabet")
            cfg = low | (high << length) | (lag << (2 * length))
            letters.append((start << 32) | cfg)
    return letters


def dfa_contains(dfa, letters):
    states = dfa["states"]
    current = dfa["start"]
    require(0 <= current < len(states), "invalid DFA start in engine dump")
    for letter in letters:
        edges = states[current]["edges"]
        require(len({pair[0] for pair in edges}) == len(edges),
                "engine dump is not deterministic")
        targets = [target for symbol, target in edges if symbol == letter]
        if not targets:
            return False
        current = targets[0]
        require(0 <= current < len(states), "invalid DFA edge target in engine dump")
    return states[current]["final"] is True


def check_fixture_membership(events, fixtures):
    comparisons = 0
    for event in events:
        if event.get("event") != "layer":
            continue
        depth = event["depth"]
        require("dfa" in event, "positive coverage control requires --dump-dfa")
        require(not dfa_contains(event["dfa"], []),
                "positive-lap language incorrectly contains the empty word")
        for fixture in fixtures:
            if depth <= fixture["width"]:
                letters = fixture_cut_letters(fixture, depth)
                require(dfa_contains(event["dfa"], letters),
                        f"engine lost arithmetic witness {fixture['label']} at spatial depth {depth}")
                wrong_type = letters[:]
                wrong_type[0] = (1 << 32) | (wrong_type[0] & ((1 << 32) - 1))
                require(not dfa_contains(event["dfa"], wrong_type),
                        "engine accepted a word with the wrong initial block phase type")
                comparisons += 1
    require(comparisons > 0, "engine emitted no positive-fixture membership checks")
    return comparisons


def maximum_gap(g):
    positions = [j for j, value in enumerate(g) if value == "1"]
    require(positions and positions[0] == 0, "driver must start with overflow")
    return max((positions[(j + 1) % len(positions)] - positions[j] - 1) % len(g) + 1
               for j in range(len(positions)))


def engine_controls(executable, fixtures, bases):
    rows = []
    processed = set()
    for fixture in fixtures:
        if fixture["base"] in processed or fixture["base"] not in bases:
            continue
        processed.add(fixture["base"])
        e, g = fixture["primitive_e"], fixture["primitive_g"]
        if maximum_gap(g) > 5:
            rows.append({"base": fixture["base"], "status": "UNSUPPORTED_GAP_REPLAY_ONLY"})
            continue
        command = [str(executable.resolve()), str(fixture["base"]), e, g,
                   "--layers", str(fixture["width"] + 1), "--seconds", "5", "--dump-dfa",
                   "--memory-mib", "1024", "--nfa-cap", "500000", "--dfa-cap", "500000",
                   "--edge-cap", "5000000", "--ops-cap", "20000000"]
        try:
            process = subprocess.run(command, text=True, capture_output=True, timeout=8)
        except subprocess.TimeoutExpired:
            rows.append({"base": fixture["base"], "status": "OUTER_TIMEOUT_UNDECIDED"})
            continue
        events = [json.loads(line) for line in process.stdout.splitlines() if line.strip()]
        compared = check_fixture_membership(events, [row for row in fixtures
                                                    if row["base"] == fixture["base"]])
        results = [row for row in events if row.get("event") == "result"]
        require(results, f"engine did not return a structured result: {process.stderr[:300]}")
        result = results[-1]
        status = result["status"]
        require(status == "TARGET_HIT" or "UNDECIDED" in status,
                f"positive fixture lost by regular engine: base={fixture['base']}, {result}")
        if status == "TARGET_HIT":
            require(process.returncode == 0, "TARGET_HIT had an error exit")
            require(any(isinstance(row.get("target_hit_k"), int) and row["target_hit_k"] >= 1
                        for row in events if row.get("event") == "layer"),
                    "TARGET_HIT omitted its positive repetition count")
        rows.append({"base": fixture["base"], "e": e, "g": g,
                     "known_width": fixture["width"], "status": status,
                     "known_witness_repetitions": fixture["k"],
                     "exit_code": process.returncode, "arithmetic_witness_memberships": compared,
                     "mistyped_boundary_rejections": compared,
                     "empty_word_rejections": sum(row.get("event") == "layer" for row in events)})
    require(rows, "no requested bases matched positive controls")
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cert20", type=Path, help="optional PR356 cert20.json fixture")
    parser.add_argument("--output", type=Path, help="write complete arithmetic-control JSON")
    parser.add_argument("--p24-layers", type=Path, help="compare P24 engine JSONL k=1 layer counts")
    parser.add_argument("--engine", type=Path, help="optional compiled regular-language engine")
    parser.add_argument("--engine-bases", default="2,4,16")
    args = parser.parse_args()
    started = time.monotonic()
    certificates = load_baseline_certificates()
    if args.cert20 is not None:
        item = json.loads(args.cert20.read_text())
        require(item["base"] == 20, "optional fixture is not base20")
        certificates.append({"base": 20, "edges": item["edges"],
                             "source": "calculation/agent-116/cert20.json (PR356)",
                             "pin": "b7a718b78d67cf54d362232ba1b8f90fbec23af8"})
    certificates.sort(key=lambda row: row["base"])
    replay = [replay_certificate(row) for row in certificates]
    fixtures, padded_edges = [], 0
    for certificate in certificates:
        rows, count = make_exterior_controls(certificate)
        fixtures.extend(rows)
        padded_edges += count
    two_lap = base6_two_lap_control()
    fixtures.append(two_lap)
    center_control = replay_p24_center()
    payload = {"exterior_controls": fixtures, "p24_center": center_control,
               "p24_one_lap_cardinalities": P24_LAYERS,
               "p24_one_lap_source": P24_LAYERS_SOURCE}
    result = {"status": "PASS", "certificate_replays": replay,
              "certificate_edges": sum(row["edges"] for row in replay),
              "padded_exterior_edges": padded_edges, "fixture_count": len(fixtures),
              "full_certificate_fixture_count": len(fixtures) - 1,
              "attributed_B_only_controls": [{"base": 6, "primitive_e": "10", "primitive_g": "10",
                                              "repetitions": 2, "natural_edges": 4, "padded_edges": 4,
                                              "width": 6, "source": two_lap["source"]}],
              "p24_center_edges": center_control["replayed_edges"],
              "p24_center_padding_equalities": center_control["common_padding_equalities"],
              "p24_center_widths": center_control["widths"],
              "small_padding_controls": padding_controls(),
              "malformed_witnesses_rejected": malformed_witness_controls(fixtures),
              "primitive_drivers": [{"base": row["base"], "e": row["e"], "g": row["g"],
                                      "width": row["width"], "max_overflow_gap": maximum_gap(row["g"])}
                                     for row in fixtures if row["k"] == 1]}
    if args.p24_layers is not None:
        events = [json.loads(line) for line in args.p24_layers.read_text().splitlines() if line.strip()]
        result["p24_layer_comparison"] = check_p24_layers(events)
    if args.engine is not None:
        bases = set(map(int, args.engine_bases.split(",")))
        result["engine_controls"] = engine_controls(args.engine, fixtures, bases)
        if any("UNDECIDED" in row["status"] for row in result["engine_controls"]):
            result["status"] = "PASS_ARITHMETIC_WITH_UNDECIDED_ENGINE_CONTROLS"
    if args.output is not None:
        args.output.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")
    result["elapsed_seconds"] = round(time.monotonic() - started, 6)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
