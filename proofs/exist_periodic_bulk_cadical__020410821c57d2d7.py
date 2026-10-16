"""CNF-backed exact bounded search; UNSAT never extrapolates beyond cap width."""
import argparse
import json
import subprocess
import time
from pathlib import Path

from exist_periodic_bulk import solve

CADICAL = '/workspace/scratch/fe6abe1df721/lean-runtime/lean-4.19.0-linux/bin/cadical'


def run(period, growth, width, residue, seconds=10):
    stem = f'exist_periodic_bulk_cnf_p{period}_g{growth}_k{width}_r{residue}'
    cnf = Path(stem+'.cnf')
    result = solve(period, width, growth, residue, base=10,
                   rotate_after_overflow=True, bulk_start_filter=True,
                   cnf_path=cnf)
    rows = cnf.read_text().splitlines()
    header = next(row for row in rows if row.startswith('p cnf ')).split()
    clauses = [row for row in rows if row and row[0] not in 'cp']
    largest = 0
    for row in clauses:
        values = list(map(int, row.split()))
        assert values[-1] == 0
        largest = max(largest, max(map(abs, values)))
    assert len(clauses) == int(header[3])
    assert largest <= int(header[2])
    start = time.monotonic()
    proc = subprocess.run([CADICAL, '-t', str(seconds), str(cnf)],
                          capture_output=True, text=True, timeout=seconds+30)
    elapsed = time.monotonic()-start
    log = Path(stem+'.log')
    log.write_text(proc.stdout+proc.stderr)
    status = 'sat' if proc.returncode == 10 else 'unsat' if proc.returncode == 20 else 'unknown'
    assert status != 'unsat' or 's UNSATISFIABLE' in proc.stdout
    assert status != 'sat' or 's SATISFIABLE' in proc.stdout
    result.update(result=status, solver='CaDiCaL2.1.3', solver_seconds=elapsed,
                  cnf_variables=int(header[2]), cnf_clauses=len(clauses),
                  cnf_largest_variable=largest, log_path=str(log))
    # CNF is exactly regenerated from the script; keep only a SAT candidate.
    if status != 'sat':
        cnf.unlink()
        result.pop('cnf_path')
    return result


if __name__ == '__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--period',type=int,default=16)
    ap.add_argument('--growth',type=int,default=6)
    ap.add_argument('--widths',default='8,16,32')
    ap.add_argument('--residues',default='0,1,2')
    ap.add_argument('--seconds',type=int,default=10)
    ap.add_argument('--output',default='exist_periodic_bulk_cadical_results.json')
    args=ap.parse_args()
    records=[]
    for width in map(int,args.widths.split(',')):
        for residue in map(int,args.residues.split(',')):
            row=run(args.period,args.growth,width,residue,args.seconds)
            records.append(row)
            Path(args.output).write_text(json.dumps(records,indent=2)+'\n')
            print(json.dumps(row),flush=True)
            if row['result']=='sat':
                raise SystemExit(0)
