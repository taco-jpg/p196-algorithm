"""Exact wall renewal obstructions and symbolic continuation.

No Lychrel witness is asserted.  Affine run lengths denote every integer
parameter k >= 0; symbolic identities are not inferred from samples.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
for candidate in (ROOT / "research", ROOT):
    if (candidate / "astra_moving_boundary_check.py").exists():
        sys.path.insert(0, str(candidate))
        break
from astra_moving_boundary_check import (
    wall_step, difference_word, digit_monotone, realize, integer_step, pair_sums,
)


@dataclass(frozen=True)
class Len:
    """a*k+b, for every k >= 0."""
    a: int = 0
    b: int = 1

    def __add__(self, other):
        return Len(self.a + other.a, self.b + other.b)

    def __sub__(self, other):
        return Len(self.a - other.a, self.b - other.b)

    def at(self, k):
        return self.a*k + self.b

    def nonnegative(self):
        return self.a >= 0 and self.b >= 0

    def positive(self):
        return self.a >= 0 and self.b > 0


ONE = Len()
ZERO = Len(0, 0)


def canon(runs):
    out = []
    for digit, length in runs:
        assert length.nonnegative(), (digit, length)
        if length == ZERO:
            continue
        if out and out[-1][0] == digit:
            out[-1] = (digit, out[-1][1] + length)
        else:
            out.append((digit, length))
    return out


def expand(runs, k):
    return tuple(x for digit, length in runs for x in (digit,)*length.at(k))


def normal(runs, carry):
    """Carry normalization of a constant run uses one reset column.

    Every input run must have a positive minimum length.  The first
    column sets the stable carry; the remainder may have minimum zero.
    """
    out = []
    for x, length in runs:
        assert length.positive(), (x, length)
        first = (x + carry) % 10
        carry = (x + carry) // 10
        tail = (x + carry) % 10
        assert (x + carry) // 10 == carry
        out.extend(((first, ONE), (tail, length - ONE)))
    return canon(out), carry


def add_runs(left, right):
    """Exact pointwise addition when affine boundaries have fixed order."""
    left, right = list(left), list(right)
    out = []
    while left and right:
        x, nx = left[0]
        y, ny = right[0]
        if (nx - ny).nonnegative():
            n = ny
        elif (ny - nx).nonnegative():
            n = nx
        else:
            raise ValueError(f"parameter-dependent crossing: {nx}, {ny}")
        out.append((x + y, n))
        if nx == n:
            left.pop(0)
        else:
            left[0] = (x, nx - n)
        if ny == n:
            right.pop(0)
        else:
            right[0] = (y, ny - n)
    assert not left and not right
    return canon(out)


def symbolic_wall_step(runs):
    low, a = normal(runs, 0)
    high_reverse, h = normal(list(reversed(runs)), 1)
    high = list(reversed(high_reverse))
    assert a == 1-h
    if h:
        low = canon(low + [(8, ONE)])
        high = canon([(1, ONE)] + high)
    return add_runs(low, high), h


def V(m):
    return ((1,) + (9,)*(2*m-1) + (8, 2) + (9,)*(2*m-1)
            + (16, 10) + (9,)*(2*m-1) + (17,))


def W8(m):
    assert m >= 3
    return ((1,6,6,5,13) + (18,)*(2*m-5) + (13,8,6,5,2)
            + (9,)*(2*m-4) + (16,13,12,10,5)
            + (0,)*(2*m-5) + (5,13,12,12,17))


def symbol_list(runs):
    return [[d, n.a, n.b] for d, n in runs]


def fixed_prefix(runs, count):
    """A parameter-independent prefix, proved from minimum run lengths."""
    result = []
    for digit, length in runs:
        need = count-len(result)
        if need == 0:
            break
        if length.b >= need:
            result.extend([digit]*need)
            break
        assert length.a == 0, (runs, count)
        result.extend([digit]*length.b)
    assert len(result) == count
    return result


def order_fringe(runs, gain):
    low, a = normal(runs, 0)
    low = canon(low + [(8+a,ONE)])
    first = fixed_prefix(low, gain+1)
    last = list(reversed(fixed_prefix(list(reversed(low)), gain+1)))
    return dict(gain=gain,first=first,last=last,
                ordered=all(x >= y for x,y in zip(last,first)))


def verify_symbolic_continuation():
    # m=k+4. The variable minimum lengths remain positive during all
    # eight normalizations, so no disappearing-run case is suppressed.
    q = [(1,ONE),(9,Len(2,7)),(8,ONE),(2,ONE),(9,Len(2,7)),
         (16,ONE),(10,ONE),(9,Len(2,7)),(17,ONE)]
    phases = [symbol_list(q)]
    hs = []
    ordering = []
    gain = 0
    for _ in range(8):
        ordering.append(order_fringe(q,gain))
        assert ordering[-1]['ordered']
        q, h = symbolic_wall_step(q)
        hs.append(h)
        gain += h
        phases.append(symbol_list(q))
    expected = canon([(x,ONE) for x in (1,6,6,5,13)]
          + [(18,Len(2,3))] + [(x,ONE) for x in (13,8,6,5,2)]
          + [(9,Len(2,4))] + [(x,ONE) for x in (16,13,12,10,5)]
          + [(0,Len(2,3))] + [(x,ONE) for x in (5,13,12,12,17)])
    assert q == expected, (q, expected)
    assert hs == [0,0,0,1,0,0,1,1]
    failure = order_fringe(q,gain)
    assert failure == dict(gain=3,first=[1,6,6,5],last=[3,3,8,9],ordered=False)
    for k in (0,1,4,19):
        assert expand(q,k) == W8(k+4)
    return dict(parameter="m=k+4, every integer k>=0", overflow_flags=hs,
                exact_affine_phases=phases,exact_ordering_checks=ordering,
                exact_failure_check=failure)


def first_collision_controls():
    checked = 0
    for half in range(1,4):
        for interior in product(range(19), repeat=half-1):
            U = (9,) + interior
            for middle in ((), (9,)):
                W = U + middle + tuple(18-x for x in U[::-1])
                C = len(W)
                _, h, r = wall_step(W)
                if h != 1:
                    continue
                N = integer_step(realize(difference_word(W,C)))
                Q = pair_sums(N)
                Cnew = sum(map(int,str(N)))//9
                if set(W) == {9}:
                    assert Cnew == 2*C
                    assert str(N) == str(N)[::-1]
                else:
                    k = next(i for i,x in enumerate(W) if x != 9)
                    assert W[k] >= 10
                    assert Cnew == C+k
                    assert len(Q) == 2*C+1
                    assert Q[0] == 10
                    assert Q[C-k] == 17-r[k]
                    assert 9 <= Q[C-k] <= 17
                    assert any(sum(Q[j::Cnew]) != 18 for j in range(Cnew))
                    assert str(N) != str(N)[::-1]
                checked += 1
    return checked


def continuation_controls():
    records = []
    for m in list(range(1,25)) + [50,100]:
        C = 6*m+3
        W = V(m)
        n = realize(difference_word(W,C))
        for t in range(8):
            Wnext, h, r = wall_step(W)
            assert digit_monotone(r,C), (m,t)
            n = integer_step(n)
            assert pair_sums(n) == difference_word(Wnext,C)
            W = Wnext
        if m >= 3:
            assert W == W8(m)
        _, h, r = wall_step(W)
        assert not digit_monotone(r,C)
        N = integer_step(n)
        Q = pair_sums(N)
        D = sum(map(int,str(N)))//9
        assert str(N) != str(N)[::-1]
        if m == 1:
            assert D == C+2 and len(Q) == 2*D-1 and Q[D-1] == 16
            bad_residue = [D-1, 16]
        else:
            assert D == C+1 and len(Q) == 2*D+1
            assert Q[1] == 12 and Q[D+1] == 3
            assert sum(Q[1::D]) == 15
            bad_residue = [1,15]
        records.append(dict(m=m,C=C,D=D,width=len(Q),bad_residue=bad_residue))
    return records


def modulus_is_not_balance_counterexample():
    # An explicit certificate; the discovery solver is not required.
    c = [2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,1,11,
         2,1,1,11,2,1,2,1,2,1,2,1,2,1,2,1,2,1]
    C = len(c)
    budget = [10*c[(j+1)%C]-c[j] for j in range(C)]
    assert sum(c) == 2*C
    assert all(budget[j] == budget[-j % C] for j in range(C))
    L = 14*C+1
    q = [0]*L
    q[0] = q[-1] = budget[0]//2
    q[C//2] = q[L-1-C//2] = budget[C//2]//2
    for j in range(1,C//2):
        remaining, t = budget[j], 0
        while remaining:
            x = min(18,remaining)
            i = j+t*C
            q[i] = q[L-1-i] = x
            remaining -= x
            t += 1
    assert all(sum(q[j::C]) == budget[j] for j in range(C))
    n = realize(tuple(q))
    assert sum(map(int,str(n))) == 9*C
    assert integer_step(n) % (10**C-1) == 0
    assert budget != [18]*C
    return dict(C=C,width=L,input_digit_sum=9*C,cyclic_carries=c,
                cyclic_q_budget=budget,balanced=False)


def run():
    out = dict(status="exact renewal obstructions; no all-time closure",
               symbolic_continuation=verify_symbolic_continuation(),
               first_collision_checks=first_collision_controls(),
               finite_integer_controls=continuation_controls(),
               modulus_counterexample=modulus_is_not_balance_counterexample())
    path = Path(__file__).with_name("wall_renewal_results.json")
    path.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:v for k,v in out.items() if k != "symbolic_continuation"},indent=2))


if __name__ == "__main__":
    run()
