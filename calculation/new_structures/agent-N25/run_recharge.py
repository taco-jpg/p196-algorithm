#!/usr/bin/env python3
"""Reproduce paired-cell recharge law and independent ordinary-integer local witness."""
import argparse, csv, io, json, pathlib, subprocess, sys, tempfile
ap=argparse.ArgumentParser();ap.add_argument("--skip-full-replay",action="store_true");opts=ap.parse_args()
P=pathlib.Path(__file__).resolve().parent
expected=json.loads((P/'recharge.json').read_text())
assert expected['steps']==20000 and expected['gap']==40001
with tempfile.TemporaryDirectory() as temp:
    exe=pathlib.Path(temp)/'safe_scan'
    subprocess.run(['g++','-std=c++17','-O3',str(P/'safe_scan.cpp'),'-o',str(exe)],check=True)
    run=subprocess.run([str(exe),'20000','40001'],capture_output=True,text=True,check=True)
    rows=[{k:int(v) for k,v in r.items()} for r in csv.DictReader(io.StringIO(run.stdout))]
    assert rows==expected['checkpoints'], 'checkpoint mismatch'
    assert 'deposits_outer=19753 deposits_central=19804' in run.stderr
    assert 'width_growth_events_outer=0 central=0' in run.stderr
    assert rows[-1]['outer_paired']==27981 and rows[-1]['central_symmetric']==28032
    assert rows[-1]['outer_eta']==19753 and rows[-1]['central_eta']==19804
    print('RECHARGE PASS:',len(rows),'checkpoints; 20,000 consecutive integer steps; gamma=8227; paired credits=19753,19804')
subprocess.run([sys.executable,str(P/'regen_check.py')],check=True)
if not opts.skip_full_replay:
    subprocess.run([sys.executable,str(P/'run.py'),'--steps','20000','--gap','40001'],check=True,stdout=subprocess.DEVNULL)
    print('INDEPENDENT 20,000-step digit-vs-base1e9 check: PASS')
