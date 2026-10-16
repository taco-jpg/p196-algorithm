#!/usr/bin/env python3
"""Independent literal-integer verification of every graph control and rank.

This verifier does not import build_graph. It recomputes fixed-width
normalization by integer evaluation and decimal digit extraction rather
than the generator's column-carry recurrence. Exact rank recurrence and
edge inclusion are checked without trusting the topological algorithm.
"""
from pathlib import Path
import gzip
import hashlib
import json

HERE = Path(__file__).resolve().parent
PHASES = [[4,4,0],[8,8,0],[16,16,0],[7,14,7],[15,8,15],[6,14,14],[13,9,9]]
N = 19**3
COUNT = 7*N


def decimal_columns(value):
    # Fixed represented width six is retained even if high digits are zero.
    return [(value // 10**i) % 10 for i in range(6)], value // 10**6


def main():
    compressed = (HERE/'six_prefix_graph.json.gz').read_bytes()
    decoded = gzip.decompress(compressed)
    cert = json.loads(decoded)
    summary = json.loads((HERE/'graph_summary.json').read_text())
    assert hashlib.sha256(compressed).hexdigest() == summary['compressed_sha256']
    assert hashlib.sha256(decoded).hexdigest() == summary['decoded_sha256']
    assert cert['phases'] == PHASES
    assert len(cert['targets']) == len(cert['rank']) == COUNT
    assert all(type(r) is int and r >= 0 for r in cert['rank'])
    accepted = 0
    for vertex in range(COUNT):
        phase = vertex // N
        suffix = vertex % N
        p = PHASES[phase] + [suffix // 361, suffix // 19 % 19, suffix % 19]
        low_value = sum(d * 10**i for i,d in enumerate(p))
        high_value = sum(d * 10**i for i,d in enumerate(reversed(p)))
        low, _ = decimal_columns(low_value)
        next_phase = (phase+1) % 7
        expected = []
        for incoming in range(2):
            high, overflow = decimal_columns(high_value + incoming)
            assert overflow in (0,1)
            if overflow:
                q = [low[0]+1] + [low[i]+high[6-i] for i in range(1,6)]
            else:
                q = [low[i]+high[5-i] for i in range(6)]
            target = -1
            if q[:3] == PHASES[next_phase]:
                target = next_phase*N + q[3]*361 + q[4]*19 + q[5]
                assert 0 <= target < COUNT
                accepted += 1
            expected.append(target)
        assert cert['targets'][vertex] == expected, vertex
        children = [cert['rank'][w]+1 for w in expected if w >= 0]
        assert cert['rank'][vertex] == max(children, default=0), vertex
    maxima = [max(cert['rank'][i*N:(i+1)*N]) for i in range(7)]
    assert maxima[0] == 26 and maxima == summary['rank_max_by_phase']
    assert accepted == summary['accepted_labeled_edges'] == 61731
    prefix_records = cert['seven_step_prefix_controls']
    assert len(prefix_records) == 128
    returned_count = 0
    for mask, rec in enumerate(prefix_records):
        bits = [(mask >> t) % 2 for t in range(7)]
        assert rec['controls'] == bits
        p = [4,4,0]
        trace, overflows = [p], []
        for c in bits:
            low_value = sum(d * 10**i for i,d in enumerate(p))
            high_value = sum(d * 10**i for i,d in enumerate(reversed(p))) + c
            lo = [(low_value // 10**i) % 10 for i in range(3)]
            hi = [(high_value // 10**i) % 10 for i in range(3)]
            e = high_value // 1000
            assert e in (0,1)
            p = ([lo[0]+1,lo[1]+hi[2],lo[2]+hi[1]] if e else
                 [lo[i]+hi[2-i] for i in range(3)])
            trace.append(p)
            overflows.append(e)
        returns = p == [4,4,0]
        guard = (bits[0],bits[1],bits[3],bits[5],bits[6]) == (0,0,0,0,1)
        assert rec['trace'] == trace and rec['overflows'] == overflows
        assert rec['returned'] == returns == guard
        if returns:
            returned_count += 1
            assert trace == PHASES + [PHASES[0]] and overflows == [0,0,1,0,1,0,1]
    assert returned_count == 4
    result = {"status": "INDEPENDENT_LITERAL_INTEGER_AND_RANK_VERIFICATION_PASS",
              "vertices": COUNT, "labeled_controls_recomputed": 2*COUNT,
              "accepted_labeled_edges": accepted, "rank_inequalities_checked": accepted,
              "exact_rank_recurrences_checked": COUNT, "rank_max_by_phase": maxima,
              "prefix_controls_independently_checked": 128,
              "returning_control_words": returned_count,
              "compressed_sha256": hashlib.sha256(compressed).hexdigest(),
              "decoded_sha256": hashlib.sha256(decoded).hexdigest(),
              "whole_word_bridge": "written, independently reviewed",
              "kernel_checked_rank_proof": False, "main_existence_proved": False}
    (HERE/'graph_verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
