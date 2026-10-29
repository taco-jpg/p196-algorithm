#!/usr/bin/env python3
"""Reproduce the symbolic and wholly independent GMP integer replays."""
import json, subprocess, sys, tempfile
from pathlib import Path

root=Path(__file__).resolve().parent
with tempfile.TemporaryDirectory() as td:
    scratch=Path(td)
    subprocess.run([sys.executable,str(root/'packet_symbolic.py'),'--q','14000',
                    '--steps','20000','--output',str(scratch/'snapshots.json')],check=True)
    result=json.loads((scratch/'snapshots.json').read_text())
    assert result['required_q_for_nonoverlap']==11985
    assert result['uniform_no_palindrome_q_bound']==22107
    assert result['minimum_central_zero_gap']==2015
    subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra',str(root/'replay_gmp.cpp'),
                    '-lgmpxx','-lgmp','-lcrypto','-o',str(scratch/'replay_gmp')],check=True)
    replay=subprocess.run([str(scratch/'replay_gmp'),'88','75','14000','20000'],
                          check=True,text=True,capture_output=True)
    got=replay.stdout.strip().splitlines()
    reference=(root/'checkpoints.txt').read_text().strip().splitlines()
    assert got[:-1]==reference, 'GMP digest/shape checkpoints differ from committed reference'
    assert got[-1]=='PASS 20000 steps min_gap=2015 required_q=11985'
    assert len(reference)==len(result['checkpoints'])==22
    for entry,line in zip(result['checkpoints'],reference):
        vals=line.split()
        assert [entry['step'],entry['A_digits'],entry['B_digits'],entry['shift'],
                entry['gap'],entry['number_digits'],entry['sha256']]==[
                 *map(int,vals[:6]),vals[6]]
    bad=subprocess.run([sys.executable,str(root/'packet_symbolic.py'),'--prefix','1',
                        '--suffix','1','--q','20','--steps','1',
                        '--output',str(scratch/'bad.json')],capture_output=True)
    assert bad.returncode!=0 and b'palindrome' in bad.stderr.lower()
    print('PASS: 20000 exact integer additions, 20001 full packet word equalities,')
    print('       20001 nonpalindrome checks, 22 SHA256 checkpoints,')
    print('       uniform-in-q bound, and a forced-palindrome rejection control.')
