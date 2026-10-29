#!/usr/bin/env python3
"""Exact two-ended affine-packet decimal RAA family; independent GMP replay in replay_gmp.cpp.

For q >= max_t(len(B_t)-s_t), the identity N_t(q)=A_t*10**(q+s_t)+B_t
holds through every simulated step. No claim is made beyond steps.
"""
import argparse, hashlib, json, sys
from pathlib import Path
sys.set_int_max_str_digits(1000000)

def reverse_decimal(s):
    return int(s[::-1])

def run(prefix, suffix, q, steps, snapshot=1000):
    assert prefix[0]!='0' and suffix[0]!='0' and suffix[-1]!='0'
    A=int(prefix)*10**len(suffix)
    B=int(suffix)
    s=0
    min_gap=10**9
    required_q=0
    uniform_q=0
    checkpoints=[]
    for t in range(steps):
        sa,sb=str(A),str(B)
        e=q+s
        gap=e-len(sb)
        min_gap=min(min_gap,gap)
        required_q=max(required_q,len(sb)-s)
        uniform_q=max(uniform_q,len(sb)+max(len(sa),len(sb))-s)
        canonical=sa+'0'*max(len(sa),len(sb))+sb
        if canonical==canonical[::-1]:
            raise ValueError(f'uniform-gap palindrome at step {t}')
        if gap<0:
            raise ValueError(f'packet overlap at step {t}: q={q}, s={s}, lenB={len(sb)}')
        word=sa+'0'*gap+sb
        if word==word[::-1]:
            raise ValueError(f'palindrome at step {t}')
        if t%snapshot==0 or t==steps-1:
            checkpoints.append({'step':t,'A_digits':len(sa),'B_digits':len(sb),'shift':s,
                                'gap':gap,'number_digits':len(word),
                                'sha256':hashlib.sha256(word.encode('ascii')).hexdigest()})
        d=len(sa)-len(sb)
        ra,rb=reverse_decimal(sa),reverse_decimal(sb)
        if d>=0:
            A+=rb*10**d
        else:
            A=A*10**(-d)+rb
            s+=d
        B+=ra
    return {'label':'COMPUTED','base':10,'prefix':prefix,'suffix':suffix,'q':q,
            'steps':steps,'palindromes':0,'required_q_for_nonoverlap':required_q,
            'uniform_no_palindrome_q_bound':uniform_q,
            'minimum_central_zero_gap':min_gap,'checkpoints':checkpoints,
            'scope':'Finite T-step family for all integer q >= uniform_no_palindrome_q_bound; not infinite.'}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--prefix',default='88')
    p.add_argument('--suffix',default='75')
    p.add_argument('--q',type=int,default=14000)
    p.add_argument('--steps',type=int,default=20000)
    p.add_argument('--output',default='packet_checkpoints.json')
    args=p.parse_args()
    result=run(args.prefix,args.suffix,args.q,args.steps)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print('PASS',result['steps'],'steps min_gap',result['minimum_central_zero_gap'],
          'required_q',result['required_q_for_nonoverlap'],
          'uniform_q',result['uniform_no_palindrome_q_bound'])

if __name__=='__main__':
    main()
