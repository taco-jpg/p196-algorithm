#!/usr/bin/env python3
"""Independent Python big-integer reverse/add and every-state SHA-256, X08."""
import sys, hashlib
sys.set_int_max_str_digits(0)
seed = int(sys.argv[1]) if len(sys.argv)>1 else 1497
steps = int(sys.argv[2]) if len(sys.argv)>2 else 20000
n = seed
h = hashlib.sha256()
maxodd=-1
miss=0
for t in range(steps+1):
    s = str(n)
    if s == s[::-1]:
        raise RuntimeError("palindrome at t=%d"%t)
    k = next((i for i in range(len(s)//2) if (int(s[i])+int(s[-i-1]))%2),-1)
    if k<0: miss+=1
    else: maxodd=max(maxodd,k)
    h.update(s.encode("ascii"))
    h.update(b"\n")
    if t in (0,1,8,88,2048,20000):
        print("step=%d length=%d first_odd=%d head=%s tail=%s"%(t,len(s),k,s[:24],s[-24:]),flush=True)
    if t<steps:
        n+=int(s[::-1])
print("SHA256(whole-orbit-newline)=%s oddless=%d max_first_odd=%d"%(h.hexdigest(),miss,maxodd))
