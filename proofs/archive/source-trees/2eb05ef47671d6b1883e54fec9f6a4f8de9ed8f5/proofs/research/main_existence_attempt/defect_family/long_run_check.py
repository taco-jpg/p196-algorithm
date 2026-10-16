"""Independent finite controls for the algebraic maximal-18-run rule."""
from itertools import product
from pathlib import Path
import json


def digits(q,incoming):
    result=[];c=incoming
    for x in q:
        result.append((x+c)%10);c=(x+c)//10
    return result


def run():
    count=0
    for length in range(1,13):
        for left,right,a,b in product(range(18),range(18),range(2),range(2)):
            q=(left,)+(18,)*length+(right,)
            lo=digits(q,a);hi=digits(q[::-1],b)[::-1]
            no=[x+y for x,y in zip(lo,hi)]
            # The preserved interior is all 18; any retained endpoint has
            # a non-18 neighbor, so the surviving run cannot join another.
            assert all(x==18 for x in no[2:length])
            if no[1]==18:assert no[0]!=18
            if no[length]==18:assert no[length+1]!=18
            ov=[lo[i]+hi[i-1] for i in range(1,len(q))]
            assert ov[0]!=18 and ov[-1]!=18
            assert ov[1:-1]==[18]*(length-1)
            count+=2
    out={"checked_local_transitions":count,
         "scope":"finite controls; arbitrary-length proof is in defect_family_report.md"}
    Path(__file__).with_name("long_run_check.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out))


if __name__=="__main__":run()
