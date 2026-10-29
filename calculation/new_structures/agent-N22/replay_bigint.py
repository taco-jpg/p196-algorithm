#!/usr/bin/env python3
"""Independent ordinary Python-bigint replay of the N22 decimal candidate.

Unlike replay_digits.cpp, this script does not use vector digit arithmetic for steps;
N is an actual Python integer, and N <- N + int(str(N)[::-1]).
"""
import argparse,hashlib,sys,csv
sys.set_int_max_str_digits(0)

def load_csv(path):
    with open(path) as f: return [[int(s) for s in row] for row in csv.reader(f)]

def seed(W,B,q):
    h=B[0]+W[0]*q+[10,14,1,10]
    p=h+h[-2::-1]
    d=[0]*len(p)
    for i in range(len(p)//2):
        high=min(9,p[i]);d[i]=p[i]-high;d[-1-i]=high
    d[len(p)//2]=p[len(p)//2]//2
    return int(''.join(map(str,d[::-1])))

def check(N,t,W,B):
    s=str(N);n=len(s)
    if s==s[::-1]:raise AssertionError(f'palindrome t={t}')
    if n<2 or s[0]=='0':raise AssertionError('leading zero')
    for i in range(11):
        if int(s[i])+int(s[-1-i])!=B[t%8][i]:
            raise AssertionError(f'B mismatch t={t} index={i}')
    for j in range(128):
        i=11+j
        if int(s[i])+int(s[-1-i])!=W[t%8][j%48]:
            raise AssertionError(f'W mismatch t={t} i={i}')
    return s

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--w',default='rows.csv');ap.add_argument('--b',default='B.csv');ap.add_argument('--checkpoints',default='rec2_checkpoints.txt');ap.add_argument('--steps',type=int,default=20000);ap.add_argument('--q',type=int,default=100)
    args=ap.parse_args()
    W=load_csv(args.w);B=load_csv(args.b);N=seed(W,B,args.q)
    checkpoints={}
    for l in open(args.checkpoints):
        k,v=l.strip().split(' ');checkpoints[int(k)]=v
    used=0
    for t in range(args.steps+1):
        s=check(N,t,W,B)
        if t in checkpoints:
            assert checkpoints[t]==s,(t,'independent bigint disagrees with digit-list replay')
            used+=1
            print(f'{t}: digits={len(s)} sha256={hashlib.sha256(s.encode()).hexdigest()}')
        if t==args.steps:break
        N+=int(s[::-1])
        assert len(str(N))-len(s)==(t%2==0),f'overflow t={t}'
    print(f'PASS Python bigint: {args.steps} reverse-add steps; {used} full-number checkpoints identical; all nonpal; B11/W128 phase and overflow exact')
if __name__=='__main__':main()
