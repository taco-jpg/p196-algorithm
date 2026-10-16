"""Independent, exact check of the finite center/periodic tail certificates.

The prescribed N,O clock still needs a finite exterior to produce an integer.
No finite decimal Lychrel witness is asserted by these local certificates.
"""
from pathlib import Path
import json,sys,hashlib
HERE=Path(__file__).parent
sys.path.insert(0,str(HERE.parent/'morphic_return'))
from root_front_check import at,compare_step

def run():
    source=HERE/'centers_period4_width8.json'
    data=json.loads(source.read_text());results=[]
    for record in data:
        assert record['status']=='exact_center_cycle_verified'
        trace=record['trace'];assert len(trace)==5
        checked=sum(compare_step(a,b,h) for a,b,h in zip(trace,trace[1:],[0,1,0,1]))
        first,last=trace[0],trace[-1]
        assert last['start']==first['start']+1 and last['patch']==first['patch']
        for key in ['left','right']:
            assert last[key]==[first[key][(i-1)%3] for i in range(3)]
        safety=[]
        for row in trace[:-1]:
            lo=row['start'];hi=lo+len(row['patch'])-1;axis2=lo+hi
            # The minimal symmetric patch determines the reflected tail phase.
            for i in range(lo-6,hi+7):assert at(row,i)==at(row,axis2-i)
            if axis2%2==0:assert at(row,axis2//2)%2==0
            witness=next((i,at(row,i)) for i in range(lo-3,hi+4)
                         if at(row,i)>9 and at(row,i)!=11)
            safety.append(dict(position=witness[0],coefficient=witness[1],
                               in_finite_patch=lo<=witness[0]<=hi))
        results.append(dict(bulk_phase=record['bulk_phase'],odd_center=record['odd_center'],
                            exact_cases=checked,palindrome_excluding_coefficients=safety))
    result=dict(status='all_exact_center_cycles_verified',
                checker='nearest_non_nine_carry_reset_and_finite_periodic_residues',
                certificates=results,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                finite_exterior_supplied=False,decimal_lychrel_existence_proved=False)
    (HERE/'root_center_check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':run()
