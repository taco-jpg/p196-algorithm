"""Independent ordinary-integer checks of spatial column semantics."""
from pathlib import Path
from itertools import product
import json
HERE=Path(__file__).resolve().parent


def representative(q):
    n=len(q);ds=[0]*n
    for i in range(n//2):
        ds[n-1-i]=min(q[i],9);ds[i]=q[i]-ds[n-1-i]
    if n%2:ds[n//2]=q[n//2]//2
    return int(''.join(map(str,ds[::-1])))


def run():
    checked=columns=overflow=0
    for length in range(2,7):
        for half in product(range(19),repeat=length//2):
            if half[0]==0:continue
            centers=(None,)if length%2==0 else tuple(range(0,19,2))
            for center in centers:
                q=half+(()if center is None else(center,))+half[::-1]
                n=representative(q);m=n+int(str(n)[::-1])
                digits=tuple(map(int,str(m)[::-1]));nq=tuple(a+b for a,b in zip(digits,digits[::-1]))
                carries=[0]
                for v in q:carries.append((v+carries[-1])//10)
                h=len(str(m))-length;assert h==carries[-1]
                overflow+=h
                previous_z=None
                for i in range(length//2):
                    a=carries[i];b=carries[length-i]
                    incoming_high=carries[length-1-i]
                    low=(q[i]+a)%10
                    assert b==(q[i]+incoming_high)//10
                    if h:
                        high=1 if i==0 else previous_z+b
                        assert 0<=high<=9
                        expected=low+high
                    else:expected=low+(q[i]+incoming_high)%10
                    assert expected==nq[i],(q,i,m)
                    previous_z=q[i]-10*b;assert -1<=previous_z<=9
                    columns+=1
                checked+=1
    result=dict(canonical_q_words=checked,checked_prefix_columns=columns,
                overflow_words=overflow,lengths=[2,3,4,5,6],
                method='Construct ordinary decimal representative, reverse/add as integers, and compare exact prefix column equations.',
                all_checks_passed=True,decimal_existence_proved=False)
    (HERE/'numeric_control.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result));return result


if __name__=='__main__':run()
