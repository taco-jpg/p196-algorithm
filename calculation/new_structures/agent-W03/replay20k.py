#!/usr/bin/env python3
import sys
sys.set_int_max_str_digits(0)
q=int(sys.argv[1]) if len(sys.argv)>1 else 200
head=int(sys.argv[2]) if len(sys.argv)>2 else 88
tail=int(sys.argv[3]) if len(sys.argv)>3 else 26
steps=int(sys.argv[4]) if len(sys.argv)>4 else 20000
n=int(f'{head:02d}'+'99'*q+f'{tail:02d}')
firstpal=None
for t in range(steps+1):
 s=str(n)
 if s==s[::-1]:firstpal=t;break
 if t<steps:n+=int(s[::-1])
print('q',q,'head',head,'tail',tail,'steps',steps,'firstpal',firstpal,'final_digits',len(str(n)),'checksum_mod1000000007',n%1000000007)
assert firstpal is None and len(str(n))==8638 and n%1000000007==232300713
