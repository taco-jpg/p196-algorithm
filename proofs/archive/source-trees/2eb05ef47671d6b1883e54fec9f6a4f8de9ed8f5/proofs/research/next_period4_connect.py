"""Try exact finite exterior completion of newly refined period-four cycles."""
import json
import subprocess
from pathlib import Path
from exist_uniform_clock8_catalog import segments
from exist_geom_periodic_qpump import solve


def main():
    data=json.loads(Path('next_period4_results.json').read_text())
    cycles=data['levels'][-1]['cycle_examples']
    results=[]
    for i,c in enumerate(cycles):
        # All phases are fixed independently of the exterior; rotate to the
        # even central origin expected by the exact all-length SMT model.
        shift=c['phases'].index(0)
        clock=c['clock'][shift:]+c['clock'][:shift]
        bulk=c['bulk'][shift:]+c['bulk'][:shift]
        row={'component':i,'period':c['period'],'growth':c['growth'],
             'clock':clock,'bulk':bulk,'exterior_smt':[]}
        if c['growth']<=20:
            canonical=min(tuple(clock[j:]+clock[:j]) for j in range(len(clock)))
            ps=segments(canonical)
            row['spatial_graph']=json.loads(subprocess.check_output(
                ['./exist_uniform_spatial_check','20','2000000']+list(map(str,ps))))
        else:
            row['spatial_graph_status']='Not run: clock exceeds the checker\'s supported segment count.'
        for k in (4,8,16):
            result=solve(c['period'],k,4,c['growth'],seconds=6,
                         forced_clock=clock,forced_bulk=bulk)
            row['exterior_smt'].append(result)
            if result['result']=='sat': break
        results.append(row)
        Path('next_period4_connect_results.json').write_text(json.dumps(results,indent=2)+'\n')
        print(json.dumps(row),flush=True)
        if any(x['result']=='sat' for x in row['exterior_smt']):break


if __name__=='__main__':main()
