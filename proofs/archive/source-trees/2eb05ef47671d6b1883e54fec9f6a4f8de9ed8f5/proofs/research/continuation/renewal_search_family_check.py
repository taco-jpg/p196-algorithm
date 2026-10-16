"""Independent finite controls for the proved all-parameter renewal identities.

The algebraic proof, rather than these tests, establishes all parameter values.
No all-time finite decimal Lychrel witness is asserted.
"""
from pathlib import Path
import json
from renewal_search_scan import m, qstep, balance


def old_wall(k):
    assert k >= 1
    return (10,8)*k+(0,)+(2,7)*k+(9,)+(11,16)*k+(18,)+(10,8)*k


def new_wall(k):
    return (1,)+(9,)*(2*k-1)+(8,2)+(9,)*(2*k-1)+(16,10)+(9,)*(2*k-1)+(17,)


def q_template(k):
    H=(10,8)*k+(0,)+(2,7)*k+(9,)+(1,8)*k
    return H+(18,)+H[::-1]


def d_template(k):
    A=(0,9)*k+(0,)+(2,7)*k+(9,)+(1,8)*k+(8,)
    B=(9,1)+(8,1)*(k-1)+(9,)+(7,2)*k+(0,8,0)+(9,0)*(k-1)+(1,)
    return A+B


def A_wall(k):
    return (5,4)+(9,)*k+(14,13)


def A_trace_expected(k):
    """All-k exact states through the first failed renewed branch."""
    C=k+4
    states=[((10,)+(9,)*(k+1)+(8,), C)]
    states += [((a,a-1)+(9,)*k+(19-a,18-a),C) for a in (1,2,4,8,16)]
    last=(7,13,9,5,11) if k==0 else (7,13,5)+(9,)*(k-1)+(13,5,11)
    states.append((last,C))
    return states


def run():
    alternating_examples=[]
    for k in range(1,65):
        C=4*k+2; D=6*k+3
        W=old_wall(k); V=new_wall(k)
        q=q_template(k)
        assert m.difference_word(W,C)==q and m.word_valid(q)
        Q,d=qstep(q)
        assert d==d_template(k)
        assert Q==V+V[::-1]==m.difference_word(V,D)
        assert balance(q)==(W,C) and balance(Q)==(V,D)
        c=0; carry=[]
        for x in q:
            c=(x+c)//10; carry.append(c)
        holes=[1-sum(carry[j::C]) for j in range(C)]
        assert holes==[j%2 for j in range(C)]
        assert sum(holes)==C//2
        assert not m.digit_monotone(m.wall_step(W)[2],C)
        n=m.realize(q); N=m.integer_step(n)
        assert m.pair_sums(N)==Q
        assert tuple(map(int,str(N)[::-1]))==d
        assert d[0]==0 and d[-1]==1 and d!=d[::-1]
        if k<=3:
            alternating_examples.append(dict(k=k,C=C,new_C=D,n=str(n),next=str(N),wall=W,new_wall=V))
    for k in range(65):
        q=m.difference_word(A_wall(k),k+3)
        for W,C in A_trace_expected(k):
            q,d=qstep(q)
            assert balance(q)==(W,C) and d!=d[::-1]
        q,d=qstep(q);D=k+5
        assert sum(q)==18*D and len(q)==2*D-1
        expected=(15,6,9,11,8,11,9,6,15) if k==0 else (15,6,12)+(9,)*(k-1)+(6,11,8,11,6)+(9,)*(k-1)+(12,6,15)
        assert q==expected
        assert q[D-1]==8 and balance(q) is None
        assert d!=d[::-1]
    result=dict(status='all-parameter identities proved in notes; finite controls only',
                alternating_parameters=list(range(1,65)),
                alternating_literal_integer_checks=64,
                A_family_parameters=list(range(65)),
                A_family_exact_transitions_checked=65*8,
                alternating_examples=alternating_examples)
    Path(__file__).with_name('renewal_search_family_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['alternating_parameters','A_family_parameters','alternating_examples']},indent=2))

if __name__=='__main__':run()
