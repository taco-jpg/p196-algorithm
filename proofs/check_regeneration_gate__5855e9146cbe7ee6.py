"""Independent sparse-polynomial audit of the nine-step safe gate trace."""
import hashlib
import json
from pathlib import Path
from check_affine_catalogue import numerator, plus, add, reflect

HERE=Path(__file__).resolve().parent


def literal(template,r):
    b,h,bulk,offset=template
    return tuple(b)+tuple([bulk]*(r+offset))+tuple(h)+tuple([bulk]*(r+offset))+tuple(b[::-1])


def main():
    path=HERE/'regeneration_gate.json'
    data=json.loads(path.read_text())
    states=data['states']
    assert len(states)==10
    for t,(q,out) in enumerate(zip(states,states[1:])):
        Q,L,_=numerator(q)
        assert Q==reflect(Q,L)
        C,CL,h=numerator(q,carry=True)
        assert CL==L and h==data['overflow_clock'][t]
        D=add(Q,{plus(e,(0,1)):v for e,v in C.items()},
              {e:-10*v for e,v in C.items()})
        W=plus(L,(0,h))
        O,OW,_=numerator(out)
        assert W==OW and O==add(D,reflect(D,W))
        symbols={s for s,_,_ in q}
        assert max(symbols)>=10 and not(q[0][0]==11 and symbols<={0,11})
        assert q[0][0]>0 and out[0][0]>0
        assert all(0<=s<=18 for s,_,_ in q+out)
    controls=0
    for row in data['ordinary_integer_controls']:
        r=row['R']
        values=list(map(int,row['integers']))
        assert len(values)==10
        for t,n in enumerate(values):
            s=str(n)
            q=tuple(int(a)+int(b) for a,b in zip(s,s[::-1]))
            assert q==literal(data['templates'][t],r)
            if t:
                assert n==values[t-1]+int(str(values[t-1])[::-1])
                assert s!=s[::-1]
                controls+=1
    assert data['templates'][9][0][1]==7
    assert data['templates'][0][0][1]==18
    assert data['templates'][9][2]==0 and data['templates'][0][2]==9
    result={'status':'PASS','symbolic_transitions':9,
            'ordinary_integer_transitions':controls,
            'includes_R3_minimum_boundary':any(x['R']==3 for x in data['ordinary_integer_controls']),
            'all_parameter_scope':'R>=4 by sparse polynomial identities; R=3 by exact integer boundary',
            'gate_scope':'g>=0, including g=0 via R=3',
            'imports_run_generator_or_normalizer':False,
            'certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'formalized_in_Lean':False,'decimal_lychrel_existence_proved':False}
    (HERE/'regeneration_gate_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
