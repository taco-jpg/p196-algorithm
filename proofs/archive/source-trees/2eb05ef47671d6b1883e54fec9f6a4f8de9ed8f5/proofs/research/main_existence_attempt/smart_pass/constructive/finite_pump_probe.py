"""Positive synthesis probes for free-clock spatial periods five and seven.

This imports the established exact all-length center/carry encoding. Every
SAT candidate would undergo its numeric controls and a separate symbolic
checker before any existence claim. UNKNOWN is not an exclusion.
"""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from exist_geom_periodic_qpump import solve
HERE=Path(__file__).resolve().parent

if __name__=='__main__':
    rows=[]
    for period,width,spatial,growth in [(28,20,5,10),(30,20,5,10),(40,20,7,14)]:
        row=solve(period,width,spatial,growth,seconds=5,nonuniform=True)
        rows.append(row)
        (HERE/'finite_pump_results.json').write_text(json.dumps(dict(
            status='positive_free_clock_synthesis',queries=rows,
            scope='Fixed finite exterior and a reflection-compatible periodic interior; spatial periods five and seven; clocks and bulk coefficients unpinned.',
            decimal_lychrel_existence_proved=False),indent=2)+'\n')
        print(json.dumps(row),flush=True)
        if row['result']=='sat':break
