"""Exact minimization of residue-defect L1 charge over every D=6m+c.

The mass inequality L1 >= abs(sum(q)-18D) bounds every possible improving
integer c.  Thus the finite candidate interval is exhaustive, not a cutoff.
All profiles are exact affine words for every m>=256.
"""
from pathlib import Path
import json
from symbolic_defects import Len,budgets,original_coordinates


def run():
    source=json.loads(Path(__file__).with_name("symbolic_defects.json").read_text())
    rows=[];M=256
    for row in source["rows"]:
        q=[(x,Len(a,a*M+b)) for x,a,b in row["q"]]
        center=row["D_offset"]
        old=budgets(q,Len(6,6*M+3))
        upper=sum(abs(x-18)*n.b for x,n in old if x!=18)
        radius=upper//18
        trials=[]
        for c in range(center-radius,center+radius+1):
            B=budgets(q,Len(6,6*M+c))
            assert all(x==18 or n.a==0 for x,n in B)
            charge=sum(abs(x-18)*n.b for x,n in B if x!=18)
            support=sum(n.b for x,n in B if x!=18)
            trials.append({"c":c,"charge":charge,"support":support,
                           "budgets":original_coordinates(B,M)})
        best=min(a["charge"] for a in trials)
        rows.append({"step":row["step"],"mass_offset":center,
                     "initial_upper_bound":upper,"radius":radius,
                     "minimum_charge":best,
                     "minimizing_c":[a["c"] for a in trials if a["charge"]==best],
                     "trials":trials})
    result={"domain":"every m>=256", "parameter":"D=6m+c, c any integer with D>0",
            "global_lower_bound":"L1 >= 18*abs(c - mass_offset)","rows":rows}
    Path(__file__).with_name("optimal_defect_charge.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps([{k:r[k] for k in ["step","minimum_charge","minimizing_c"]}
                     for r in rows if r["step"] in [11,12,13,14,15,16,24,32,48,64,96,128]],indent=2))


if __name__=="__main__":run()
