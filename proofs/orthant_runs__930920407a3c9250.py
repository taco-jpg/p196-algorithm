"""Exact run arithmetic with independently nonnegative integer parameters.

A length is c + sum(a_i*k_i), for all k_i >= 0. Every ordering decision
used here is certified coefficientwise; undecidable comparisons are errors.
This module makes no assertion about an unbounded number of time steps.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Length:
    coefficients: tuple[int, ...]
    constant: int

    def __add__(self, other):
        assert len(self.coefficients) == len(other.coefficients)
        return Length(tuple(a+b for a,b in zip(self.coefficients,other.coefficients)),
                      self.constant+other.constant)

    def __sub__(self, other):
        assert len(self.coefficients) == len(other.coefficients)
        return Length(tuple(a-b for a,b in zip(self.coefficients,other.coefficients)),
                      self.constant-other.constant)

    def nonnegative(self):
        return self.constant >= 0 and all(a >= 0 for a in self.coefficients)

    def positive(self):
        return self.constant > 0 and all(a >= 0 for a in self.coefficients)

    def zero(self):
        return self.constant == 0 and not any(self.coefficients)

    def at(self, parameters):
        assert len(parameters) == len(self.coefficients)
        assert all(k >= 0 and isinstance(k,int) for k in parameters)
        return self.constant+sum(a*k for a,k in zip(self.coefficients,parameters))


def constant(value, dimension):
    return Length((0,)*dimension,value)


def canon(runs):
    out=[]
    for x,n in runs:
        assert n.nonnegative(), (x,n)
        if n.zero():
            continue
        if out and out[-1][0] == x:
            out[-1]=(x,out[-1][1]+n)
        else:
            out.append((x,n))
    return out


def normal(runs, carry=0):
    out=[]
    for x,n in runs:
        assert n.positive(), (x,n)
        one=constant(1,len(n.coefficients))
        digit=(x+carry)%10
        carry=(x+carry)//10
        assert (x+carry)//10 == carry
        out.extend([(digit,one),((x+carry)%10,n-one)])
    return canon(out),carry


def add_runs(left,right):
    left=list(left);right=list(right);out=[]
    while left and right:
        x,a=left[0];y,b=right[0]
        if (a-b).nonnegative():
            n=b
        elif (b-a).nonnegative():
            n=a
        else:
            raise ValueError(("uncertified orthant comparison",a,b))
        out.append((x+y,n))
        if a==n:left.pop(0)
        else:left[0]=(x,a-n)
        if b==n:right.pop(0)
        else:right[0]=(y,b-n)
    assert not left and not right
    return canon(out)


def step(q):
    d,h=normal(q)
    if h:
        d=canon(d+[(1,constant(1,len(q[0][1].coefficients)))])
    return add_runs(d,d[::-1]),h


def expand(q,parameters):
    return tuple(x for x,n in q for _ in range(n.at(parameters)))


def as_json(q):
    return [[x,list(n.coefficients),n.constant] for x,n in q]
