#!/usr/bin/env python3
"""Replay discovered center drivers and apply an external, pinned B engine.

This orchestrator does not claim an exhaustive driver census. Its engine is
Agent 108 PR405 (head b30d1d5a71d9be24fa28c5e05c76302919a322e6), not authored
here. A full candidate is returned only after positional-integer and mirror
cycleOK checks, then the batch stops for the separate Lean/publication gate.
Exit10 means candidate success, not an undecided or failed search.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import resource
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import neutral_band_search as mirror


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digits_of(word, incoming, base):
    n = incoming + sum(a * base**j for j, a in enumerate(word))
    digits = []
    for _ in word:
        n, digit = divmod(n, base)
        digits.append(digit)
    return digits, n


def couple(base, center_edges, words):
    """Independent integer reconstruction, then the unchanged exact mirror."""
    require(type(base) is int and base >= 2, "invalid base")
    period = len(center_edges)
    require(period > 0 and isinstance(words, list) and len(words) == period,
            "exterior witness phase count mismatch")
    for w in words:
        require(isinstance(w, list) and all(type(a) is int and 0 <= a <= 2*base-2 for a in w),
                "invalid exterior coefficients")
        require(not w or w[0] > 0, "zero exterior head")
    full = []
    for phase, edge in enumerate(center_edges):
        B, B2 = words[phase], words[(phase+1) % period]
        C, C2 = list(edge['C']), list(edge['next_C'])
        require(C2 == list(center_edges[(phase+1) % period]['C']), "broken center seam")
        for w in (C, C2):
            require(all(type(a) is int and 0 <= a <= 2*base-2 for a in w),
                    "invalid center coefficients")
        v, expected_e, expected_g = edge['v'], edge['e'], edge['g']
        require(type(v) is int and v >= 0 and type(expected_e) is int and type(expected_g) is int
                and expected_e in (0, 1) and expected_g in (0, 1),
                "invalid center labels")
        low, e = digits_of(B, 0, base)
        cd, e2 = digits_of(C, e, base)
        high, g = digits_of(B[::-1], e2, base)
        require((e, e2, g) == (expected_e, 1-expected_e, expected_g),
                "supplied exterior does not realize the center driver")
        left = low + [(base-1)*(1-e)]*g
        right = ([1] if g else []) + high[::-1]
        raw_B = [a+b for a, b in zip(left, right)]
        require(len(left) == len(right), "exterior alignment mismatch")
        u = len(raw_B) - len(B2)
        require(u >= 0 and raw_B == B2 + [base-1]*u, "invalid exterior suffix trim")
        ds = cd + [(base-1)*e]*g
        raw_C = [a+b for a, b in zip(ds, ds[::-1])]
        require(raw_C == [base-1]*v + C2 + [base-1]*v, "invalid center pair trim")
        E = (B, C, B2, C2, u, v)
        require(mirror.edgeOK(base, E), "mirror edge rejected")
        full.append(E)
    require(mirror.cycleOK(base, full, words[0], list(center_edges[0]['C'])),
            "mirror cycleOK rejected")
    return full


def control(binary=None):
    cycles = edges = rejected = 0
    for base, es in mirror._lean_certs():
        center = [{'C':E[1], 'next_C':E[3], 'v':E[5],
                   'e':mirror.e1(base,E[0]), 'g':mirror.gam(base,E[0],E[1])} for E in es]
        result = couple(base, center, [E[0] for E in es])
        require(result == es, "known full certificate reconstruction differs")
        cycles += 1
        edges += len(result)
        bad = [dict(row) for row in center]
        bad[0]['g'] ^= 1
        try:
            couple(base, bad, [E[0] for E in es])
        except ValueError:
            rejected += 1
        else:
            raise ValueError("corrupted driver incorrectly accepted")
    result = {'status':'PASS', 'known_cycles':cycles, 'integer_and_mirror_edges':edges,
              'corrupted_drivers_rejected':rejected}
    with tempfile.TemporaryDirectory(prefix='a101-bad-record-') as temporary:
        malformed = Path(temporary)/'nonobject_engine.py'
        malformed.write_text('#!/usr/bin/env python3\nprint("null")\n')
        malformed.chmod(0o700)
        decision, witness = run_engine(malformed, '0', '1', 2, 256, 100, 100, 1)
        require(decision.get('status') == 'UNDECIDED'
                and decision.get('reason') == 'nonobject_engine_record' and witness is None,
                'nonobject engine record did not fail closed')
        result['malformed_engine_records_rejected'] = 1
        from unittest.mock import patch
        marker = {'type':'WITNESS','e':'0','g':'1','B_t':[[9]]}
        partial = (json.dumps(marker)+'\n'+ '{"type":"RES').encode()
        error = subprocess.TimeoutExpired(['fixture'],1,output=partial)
        with patch.object(subprocess,'run',side_effect=error):
            decision, retained = run_engine(malformed,'0','1',1,256,100,100,1)
        require(decision.get('status') == 'UNDECIDED' and retained == marker,
                'timeout discarded an already emitted complete witness')
        result['timeout_witness_records_retained'] = 1
    if binary is not None:
        from check_prefix_sink import exterior
        E, G = '10100110011', '11100010000'
        decision, witness = run_engine(binary, E, G, 30, 1024, 1500000, 300000000, 1000)
        require(decision['status'] == 'FEASIBLE' and witness is not None,
                'known decimal exterior was not reconstructed')
        require((witness.get('e'), witness.get('g')) == (E, G), 'wrong exterior witness driver')
        words = witness['B_t']
        require(len(words) == len(E), 'wrong exterior fixture period')
        for phase, B in enumerate(words):
            raw, e, g = exterior(tuple(B))
            following = tuple(words[(phase+1) % len(words)])
            u = len(raw)-len(following)
            require((e,g) == (int(E[phase]),int(G[phase])) and u >= 0
                    and raw == following+(9,)*u, 'exterior fixture integer replay failed')
        result['external_engine_positive_edges'] = len(words)
        E, G = '010100110100101011001011', '110001001000110001001000'
        decision, witness = run_engine(binary, E, G, 30, 1024, 1500000, 300000000, 1000)
        require(decision['status'] == 'EXHAUSTED_NO_B_FOR_E' and decision['depth'] == 39
                and witness is None, 'published one-lap negative control differs')
        result['external_engine_negative_depth'] = decision['depth']
    return result


def run_engine(binary, e, g, seconds, mib, nodes, operations, depth):
    command = [str(binary), g, str(nodes), str(operations), str(depth), str(seconds),
               '--e', e, '--witness']
    def guard():
        _, hard = resource.getrlimit(resource.RLIMIT_AS)
        requested = mib * 1024**2
        if hard != resource.RLIM_INFINITY:
            requested = min(requested, hard)
        resource.setrlimit(resource.RLIMIT_AS, (requested, hard))
        old_soft, old_hard = resource.getrlimit(resource.RLIMIT_CPU)
        cpu = seconds + 3
        if old_hard != resource.RLIM_INFINITY:
            cpu = min(cpu, old_hard)
        if old_soft != resource.RLIM_INFINITY:
            cpu = min(cpu, old_soft)
        resource.setrlimit(resource.RLIMIT_CPU, (cpu, old_hard))
    started = time.monotonic()
    interrupted = None
    try:
        p = subprocess.run(command, text=True, capture_output=True, timeout=seconds+5,
                           preexec_fn=guard)
        output, returncode = p.stdout, p.returncode
    except subprocess.TimeoutExpired as error:
        # subprocess.run has killed and reaped the worker. Complete witness
        # records emitted before the timeout must remain available for replay.
        output = error.stdout or b''
        if isinstance(output, bytes):
            output = output.decode('utf-8',errors='replace')
        returncode, interrupted = None, 'outer_wall_cap'
    records = []
    lines = output.splitlines()
    for index, line in enumerate(lines):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except ValueError:
            interrupted = interrupted or 'malformed_engine_output'
            break
        if not isinstance(row, dict):
            interrupted = interrupted or 'nonobject_engine_record'
            break
        records.append(row)
    witness = [r for r in records if r.get('type') == 'WITNESS']
    require(len(witness) <= 1, 'multiple exterior witness records')
    witness = witness[0] if witness else None
    results = [r for r in records if r.get('type') == 'RESULT']
    if interrupted or len(results) != 1 or returncode not in (0, 3):
        return {'status':'UNDECIDED','reason':interrupted or 'missing_or_failed_result',
                'returncode':returncode,'wall_seconds':time.monotonic()-started}, witness
    result = dict(results[0])
    require(result.get('g') == g and result.get('requested_e') == e,
            'engine reported a different driver')
    status = result.get('status')
    if status == 'EXHAUSTED_NO_B_FOR_E':
        require(returncode == 0 and result.get('reason') in ('empty_layer','exact_layer_repeat'),
                'engine incomplete negative')
    elif status == 'FEASIBLE':
        require(returncode == 0, 'engine inconsistent feasibility status')
    else:
        result['status'] = 'UNDECIDED'
    result['wall_seconds'] = time.monotonic()-started
    return result, witness


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('catalog', type=Path, nargs='?')
    ap.add_argument('--engine', type=Path)
    ap.add_argument('--candidate', type=Path)
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--max-drivers', type=int, default=20)
    ap.add_argument('--indices', help='comma-separated zero-based catalog indices, in trial order')
    ap.add_argument('--seconds', type=int, default=60)
    ap.add_argument('--total-seconds', type=int, default=1500)
    ap.add_argument('--memory-mb', type=int, default=2048)
    ap.add_argument('--nodes', type=int, default=1500000)
    ap.add_argument('--operations', type=int, default=300000000)
    ap.add_argument('--depth', type=int, default=1000)
    args = ap.parse_args()
    if args.selftest:
        print(json.dumps(control(args.engine),sort_keys=True));return 0
    if args.catalog is None or args.engine is None or args.candidate is None:
        ap.error('catalog, --engine and --candidate are required for triage')
    if not (1 <= args.max_drivers <= 10000 and 1 <= args.seconds <= 1200
            and 1 <= args.total_seconds <= 1500 and 64 <= args.memory_mb <= 4096
            and 2 <= args.nodes <= 10000000 and 1 <= args.operations <= 2000000000
            and 1 <= args.depth <= 1000000):
        ap.error('unsupported resource limits')
    require(args.engine.is_file(), 'external engine binary missing')
    require(not args.candidate.exists(), 'candidate destination already exists')
    require(args.candidate.parent.is_dir(), 'candidate parent directory is missing')
    require(args.catalog.stat().st_size <= 64*1024**2, 'catalog exceeds 64 MiB input guard')
    from check_d7_drivers import validate_driver, validate_catalog
    rows = [json.loads(line) for line in args.catalog.read_text().splitlines() if line.strip()]
    require(all(isinstance(row, dict) for row in rows), 'catalog records must be objects')
    started = time.monotonic()
    source_catalog = validate_catalog(rows)
    drivers = [row for row in rows if row.get('type') == 'DRIVER']
    if args.indices is None:
        selected = list(range(len(drivers)))
    else:
        require(args.indices and all(part.isdecimal() for part in args.indices.split(',')),
                'indices must be comma-separated nonnegative integers')
        selected = [int(part) for part in args.indices.split(',')]
        require(len(set(selected)) == len(selected) and all(i < len(drivers) for i in selected),
                'duplicate or out-of-range catalog index')
    outcomes = {}
    completed = 0
    for index in selected:
        row = drivers[index]
        if completed >= args.max_drivers:
            break
        remaining = args.total_seconds-(time.monotonic()-started)
        if remaining < 6:
            break
        checked = validate_driver(row)
        checked.pop('edges', None)
        edges = row['edges']
        e = ''.join(str(edge['e']) for edge in edges)
        g = ''.join(str(edge['g']) for edge in edges)
        P, G = len(edges), g.count('1')
        reason = None
        if P > 96 or 2*P+4*G > 240:
            reason = 'unsupported_engine_count_budget'
        if not G:
            reason = 'unsupported_zero_overflow'
        if G:
            starts = [j for j, value in enumerate(g) if value == '1']
            if max(b-a for a,b in zip(starts,starts[1:]+[starts[0]+P])) > 5:
                reason = 'unsupported_engine_overflow_gap'
        if reason:
            decision, witness = {'status':'UNDECIDED','reason':reason}, None
        else:
            seconds = min(args.seconds, max(1,int(remaining)-5))
            decision, witness = run_engine(args.engine, e, g, seconds, args.memory_mb,
                                           args.nodes, args.operations, args.depth)
        status = decision['status']
        if witness is not None:
            require((witness.get('e'),witness.get('g')) == (e,g), 'witness labels differ')
            full = couple(10, edges, witness.get('B_t'))
            candidate = {'status':'PYTHON_MIRROR_CANDIDATE','lean_verified':False,
                         'base':10,'catalog_index':index,'period':P,'e':e,'g':g,
                         'B':full[0][0],'C':full[0][1],'edges':full}
            try:
                with args.candidate.open('x') as output:
                    json.dump(candidate,output,sort_keys=True);output.write('\n')
            except OSError as error:
                print(json.dumps(dict(candidate,type='CANDIDATE',path=None,
                                      save_error=str(error)),sort_keys=True),flush=True)
                return 10
            print(json.dumps({'type':'CANDIDATE','path':str(args.candidate.resolve()),
                              'period':P,'e':e,'g':g}),flush=True)
            return 10
        if status == 'FEASIBLE':
            status = 'UNDECIDED'
            decision = dict(decision,status=status,reason='feasible_without_reconstructed_witness')
        outcomes[status] = outcomes.get(status,0)+1
        completed += 1
        print(json.dumps({'type':'TRIAGE','index':index,'period':P,'G':G,'e':e,'g':g,
                          'center_replay':checked,'result':decision},sort_keys=True),flush=True)
    print(json.dumps({'type':'TRIAGE_SUMMARY','status':'SCOPED_TRIAGE_COMPLETE'
                      if completed == len(selected) else 'UNDECIDED_BATCH_CAP',
                      'catalog_drivers':len(drivers),'selected_indices':selected,
                      'processed':completed,'outcomes':outcomes,
                      'source_catalog_status':source_catalog['producer_status'],
                      'seconds':time.monotonic()-started,
                      'complete_driver_census':False},sort_keys=True),flush=True)
    return 0 if completed == len(selected) else 3


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, RuntimeError, KeyError, TypeError) as exc:
        print(json.dumps({'status':'UNDECIDED','reason':str(exc)}))
        raise SystemExit(2)
