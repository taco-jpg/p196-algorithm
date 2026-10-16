#!/usr/bin/env python3
"""Agent123 preliminary finite boundary diagnostic. Not an all-width theorem."""
import itertools, sys
from controls import template, realize, reverse_add
cases=0; found={}
for c,B,A,C in itertools.product([i for i in range(1,18) if i!=9],[[]]+[[i] for i in range(1,19)],[[]]+[[i] for i in range(19)],[[]]+[[i] for i in range(0,19,2)]):
    for g,h in [(1,1),(1,2),(2,1),(2,2)]:
        n=realize(template(c,B,A,C,g,h),0);m=reverse_add(n);cases+=1
        if str(m)==str(m)[::-1] and (g,h) not in found:found[g,h]=(c,B,A,C,n,m)
print('boundary cases',cases,'first witnesses',found)
