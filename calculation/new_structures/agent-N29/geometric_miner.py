#!/usr/bin/env python3
"""Constructively mine base-10 long 9-band trajectories; verify EVERY edge as Q[10^q] identity."""
import sys,json,argparse
from pathlib import Path
sys.set_int_max_str_digits(1000000)
from geometric_checker import pvalue,reverse_template,root_check,scalar,add

def tmpl_from_string(s,q):
    runs=[];i=0
    while i<len(s):
        if s[i]=='9':
            j=i
            while j<len(s) and s[j]=='9':j+=1
            runs.append((j-i,i,j));i=j
        else:i+=1
    if not runs:return None
    width,start,end=max(runs)
    return [{'lit':s[:start]},{'rep':'9','a':1,'c':width-q},{'lit':s[end:]}],width

def run(q,steps,out):
    n=int('12'+'9'*q+'34')
    q_ind=q+37
    n_ind=int('12'+'9'*q_ind+'34')
    prev_poly=None;min_width=q;max_abs_c=0;meta=[]
    for t in range(steps+1):
        s=str(n)
        candidate=tmpl_from_string(s,q)
        if not candidate:raise ValueError(f'no 9-band at step {t}')
        T,width=candidate
        if width<2:raise ValueError(f'9-band exhausted step {t}')
        # Genuine ordinary-integer control at DIFFERENT q, at EVERY step.
        word_ind=T[0]['lit']+'9'*(q_ind+T[1]['c'])+T[2]['lit']
        if str(n_ind)!=word_ind:raise ValueError(f'independent integer mismatch step {t}')
        if word_ind==word_ind[::-1]:raise ValueError(f'independent palindrome step {t}')
        P=pvalue(T)
        if prev_poly is not None and P!=prev_poly:
            raise ValueError(f'bad polynomial identity step {t}')
        valid,reason=root_check(add(P,scalar(pvalue(reverse_template(T)),-1)),10,q)
        if not valid:raise ValueError(f'palindromic q at step {t}: {reason}')
        if t%25==0 or t==steps:
            meta.append({'t':t,'width_at_q':width,'c':width-q,
                'left':len(T[0]['lit']),'right':len(T[2]['lit']),
                'number_digits':len(s),'left_prefix':T[0]['lit'][:16],
                'right_suffix':T[2]['lit'][-16:]})
        min_width=min(min_width,width);max_abs_c=max(max_abs_c,q-width)
        if t==steps:break
        prev_poly=add(P,pvalue(reverse_template(T)))
        n+=int(s[::-1])
        n_ind+=int(str(n_ind)[::-1])
    result={'status':'COMPUTED','base':10,'seed':'12 9^q 34','qmin':q,'steps':steps,
        'universal_nonpal':True,'all_edges_polynomially_proved':True,
        'independent_integer_q':q_ind,'independent_integer_steps':steps,
        'min_9_run':min_width,'worst_repetition_offset':-max_abs_c,
        'checkpoints':meta,'not_infinite':True}
    Path(out).write_text(json.dumps(result,indent=2)+'\n')
    print('PASS',steps,'exact geometric polynomial edges',
        'minimum_9_width',min_width,'checkpoints',len(meta))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--q',type=int,default=600)
    p.add_argument('--steps',type=int,default=400)
    p.add_argument('--out',default='geometric_miner_out.json')
    a=p.parse_args();run(a.q,a.steps,a.out)
