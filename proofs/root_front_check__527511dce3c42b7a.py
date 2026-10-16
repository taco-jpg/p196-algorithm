"""Independent carry scan for the claimed infinite periodic-tail identity.

No discovery module is imported. The exterior overflow clock is prescribed,
not inferred from a finite integer. No finite Lychrel witness is asserted.
"""
from pathlib import Path
import hashlib,json


def at(row,i):
    a=row['start'];b=a+len(row['patch'])
    if i<a:return row['left'][i%len(row['left'])]
    if i>=b:return row['right'][i%len(row['right'])]
    return row['patch'][i-a]


def incoming(row,i,direction):
    # A non-nine resets the carry; periodic tails guarantee it is reached.
    bound=len(row['patch'])+len(row['left'])+len(row['right'])+2
    for distance in range(1,bound+1):
        q=at(row,i+direction*distance)
        if q!=9:return int(q>=10)
    raise AssertionError('carry failed to reset within the proved bound')


def next_at(row,i,h):
    low=(at(row,i)+incoming(row,i,-1))%10
    j=i-h
    high=(at(row,j)+incoming(row,j,1))%10
    return low+high


def compare_step(old,new,h):
    for key in ['left','right']:
        assert len(old[key])==len(new[key])==3
        assert any(q!=9 for q in old[key])
    # Beyond this finite interval, neither carry scan reaches the patch;
    # both the actual output and claimed output are exactly3-periodic.
    lo=min(old['start'],new['start'])-9
    hi=max(old['start']+len(old['patch']),new['start']+len(new['patch']))+9
    for i in range(lo,hi+1):assert next_at(old,i,h)==at(new,i),(i,h,old,new)
    return hi-lo+1


def run():
    folder=Path(__file__).parent;path=folder/'front_525_to_936.json'
    data=json.loads(path.read_text());trace=data['trace'];clock=data['clock']
    assert len(trace)==len(clock)+1==25
    checked=sum(compare_step(a,b,h) for a,b,h in zip(trace,trace[1:],clock))
    initial=trace[0]
    for elapsed,shift in [(4,1),(24,6)]:
        final=trace[elapsed]
        assert final['start']==initial['start']+shift and final['patch']==initial['patch']
        for key in ['left','right']:
            assert final[key]==[initial[key][(i-shift)%3] for i in range(3)]
    result={'verified':True,'exact_periodic_tail_steps':24,
            'finite_interface_and_periodic_cases':checked,
            'four_step_translation':1,'twenty_four_step_translation':6,
            'required_clock':'N,O repeated',
            'finite_exterior_supplied':False,'finite_center_supplied':False,
            'decimal_lychrel_existence_proved':False,
            'certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    (folder/'root_front_check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':run()
