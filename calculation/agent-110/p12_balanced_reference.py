#!/usr/bin/env python3
"""Independent bounded all-repetition reference for the documented p12 stream.

The 12-step stream has three overflows, so every center cycle uses an even
number of repetitions.  Two repetitions admit the floor-prefix trim schedule
at phases 4, 12, 20.  The ceiling-prefix profile is its time shift by 12.
For a width bound W >= 2, the exact-W padding theorem therefore reduces every
center cycle to this floor profile, after a possible 12-step rotation.
Start at phase 4: its source width is W and its edge has g=v=1.  Requiring
the raw output head to equal 9 forces the source endpoints to equal 9.

Thus cycles of the partial 24-step return map on C=[9]+D+[9], |C|=W,
D symmetric, capture center cycles of ANY period multiple of 12 with
every center width <= W.  The map uses fixed trims, so it is a function.

This implementation normalizes by first evaluating the entire positional
integer, then recovering digits using divmod.  It imports no repository
mirror, C++ implementation, or other Agent 110 verifier.  Source coefficients
range over 0..18, including odd middle coefficients; actual cycle outputs
automatically enforce the usual even-middle condition.

Output status NONE is a COMPUTED bounded all-repetition negative.  It is not
a Lean result, an unrestricted-width obstruction, or a decimal Lychrel proof.
State and wall-clock caps produce UNDECIDED, never NONE.
"""
import argparse
from collections import deque
import json
import time


E12 = tuple(map(int, '101010010101'))
G12 = tuple(map(int, '100010001000'))


def normalize_integer(base, coefficients, entry):
    value = 0
    for coefficient in reversed(coefficients):
        value = base * value + coefficient
    value += entry
    digits = []
    for _ in coefficients:
        value, digit = divmod(value, base)
        digits.append(digit)
    return tuple(digits), value


def forced_step(base, center, entry, overflow, trim):
    digits, carry = normalize_integer(base, center, entry)
    if carry != 1-entry:
        return None, 'carry'
    if overflow:
        digits += ((base-1)*entry,)
    image = tuple(x+y for x,y in zip(digits,reversed(digits)))
    if len(image)-2*trim < 1:
        return None, 'empty'
    if any(image[i] != base-1 or image[-1-i] != base-1
           for i in range(trim)):
        return None, 'trim'
    return image[trim:len(image)-trim], None


def schedule():
    g = G12 * 2
    e = E12 * 2
    s = 0
    v = []
    lengths = []
    for gg in g:
        lengths.append(s % 2)
        v.append((s+gg)//2-s//2)
        s += gg
    assert s == 6
    assert [i for i,x in enumerate(v) if x] == [4,12,20]
    assert lengths[4] == 1
    rotate = lambda values: tuple(values[4:] + values[:4])
    # Width profile is W-1+(prefix overflow parity), rotated to phase 4.
    offsets = tuple(x-1 for x in rotate(lengths))
    assert offsets[0] == 0 and set(offsets) == {0,-1}
    return rotate(e), rotate(g), rotate(v), offsets


ENTRIES, OVERFLOWS, TRIMS, WIDTH_OFFSETS = schedule()


def center_from_code(code, width):
    inner_length = width-2
    half = []
    for _ in range((inner_length+1)//2):
        code, digit = divmod(code,19)
        half.append(digit)
    assert code == 0
    inner = tuple(half + half[:inner_length//2][::-1])
    return (9,) + inner + (9,)


def code_from_center(center):
    width = len(center)
    assert width >= 2 and center[0] == 9 and center[-1] == 9
    assert center == center[::-1]
    code = 0
    for coefficient in reversed(center[1:1+(width-1)//2]):
        assert 0 <= coefficient <= 18
        code = 19*code + coefficient
    return code


def return_map(center, width):
    for phase,(entry,overflow,trim) in enumerate(zip(ENTRIES,OVERFLOWS,TRIMS)):
        assert len(center) == width+WIDTH_OFFSETS[phase]
        center, reason = forced_step(10,center,entry,overflow,trim)
        if center is None:
            return None, phase, reason
    assert len(center) == width
    return center, None, None


def controls():
    assert ENTRIES[0] == OVERFLOWS[0] == TRIMS[0] == 1
    # Positive control from the published base-26 certificate, rotated to
    # its g=v=1 edge.  All four center images must match exactly.
    centers = [
        (25,6,14,6,25), (32,20,20,32),
        (12,41,41,12), (38,28,32,28,38),
    ]
    for i,(entry,overflow,trim) in enumerate([(1,1,1),(0,0,0),(1,1,0),(0,0,0)]):
        out,reason = forced_step(26,centers[i],entry,overflow,trim)
        assert reason is None and out == centers[(i+1)%4]
    for width in range(2,9):
        for code in range(19**((width-1)//2)):
            assert code_from_center(center_from_code(code,width)) == code
    # Both profiles are related by the original stream's 12-step symmetry.
    s = 0
    floor = []
    ceiling = []
    r = []
    for gg in G12*2:
        r.append(s%2)
        floor.append((s+gg)//2-s//2)
        ceiling.append((s+gg+1)//2-(s+1)//2)
        s += gg
    assert all(floor[(i+12)%24] == ceiling[i] for i in range(24))
    assert all(r[(i+12)%24] == 1-r[i] for i in range(24))
    return {'base26_positive_edges':4,'encoding_roundtrips':14479,
            'profile_shift_checks':48,'status':'PASS'}


def solve(width, max_states, seconds):
    started = time.monotonic()
    n = 19**((width-1)//2)
    result = {'width':width,'domain_states':n,'period':24,'start_phase':4}
    if n > max_states:
        return dict(result,status='UNDECIDED',reason='state cap',max_states=max_states)
    # Failed returns have no outgoing edge and cannot belong to a cycle.
    # Store only successful edges; vertices outside their endpoint set are
    # isolated and can be counted as peeled without allocating N entries.
    successor = {}
    initial_valid = completed = edges = 0
    for code in range(n):
        if code % 512 == 0 and time.monotonic()-started > seconds:
            return dict(result,status='UNDECIDED',reason='time cap',processed=code)
        center = center_from_code(code,width)
        target,failed_phase,reason = return_map(center,width)
        if failed_phase != 0 or reason != 'carry':
            initial_valid += 1
        if target is None:
            continue
        completed += 1
        # A next trim/overflow edge cannot begin without neutral endpoints.
        if target[0] != 9 or target[-1] != 9:
            continue
        dest = code_from_center(target)
        assert 0 <= dest < n
        successor[code] = dest
        edges += 1
    active = set(successor) | set(successor.values())
    indegree = dict.fromkeys(active,0)
    for dest in successor.values():
        indegree[dest] += 1
    ready = deque(i for i,d in indegree.items() if d == 0)
    removed = n-len(active)
    while ready:
        if removed % 16384 == 0 and time.monotonic()-started > seconds:
            return dict(result,status='UNDECIDED',reason='peel time cap',removed=removed)
        node = ready.popleft()
        removed += 1
        dest = successor.get(node,-1)
        if dest >= 0:
            indegree[dest] -= 1
            if indegree[dest] == 0:
                ready.append(dest)
    result.update(initial_flip_valid=initial_valid,completed_returns=completed,
                  edges=edges,removed=removed,cycle_nodes=n-removed,
                  seconds=round(time.monotonic()-started,6))
    if removed == n:
        result['status'] = 'NONE'
    else:
        seed = next(i for i,d in indegree.items() if d)
        orbit = [seed]
        seen = {seed}
        cur = successor[seed]
        while cur != seed:
            assert cur >= 0 and cur not in seen
            orbit.append(cur)
            seen.add(cur)
            cur = successor[cur]
        result.update(status='CENTER_CYCLE',cycle_length=len(orbit),
                      seed_center=center_from_code(seed,width),
                      cycle_codes=orbit[:128])
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('widths',type=int,nargs='*',default=list(range(2,9)))
    parser.add_argument('--max-states',type=int,default=200000)
    parser.add_argument('--seconds',type=float,default=300)
    args = parser.parse_args()
    if any(w < 2 for w in args.widths):
        parser.error('widths must be at least 2')
    if args.max_states < 1 or not 0 < args.seconds <= 1740:
        parser.error('positive max-states and a per-width budget in (0,1740] are required')
    print(json.dumps({'controls':controls()},sort_keys=True),flush=True)
    capped = False
    for width in args.widths:
        result = solve(width,args.max_states,args.seconds)
        print(json.dumps(result,sort_keys=True),flush=True)
        capped |= result['status'] == 'UNDECIDED'
        if result['status'] == 'CENTER_CYCLE':
            return 3
    return 2 if capped else 0


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without Python -O: assertions must remain enabled.')
    raise SystemExit(main())
