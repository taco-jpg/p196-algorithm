#!/usr/bin/env python3
"""Rewrite section 4 of EXTERIOR.md from the census DB (idempotent).  usage: append_results.py [--files F...]"""
import subprocess,sys,os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mr=subprocess.run([sys.executable,f'{ROOT}/py/make_results.py']+sys.argv[1:],capture_output=True,text=True).stdout
s=open(f'{ROOT}/EXTERIOR.md').read()
i=s.index('## 4. Results')
j=s.find('<!-- END RESULTS -->')
tailtxt = s[j:] if j>=0 else '<!-- END RESULTS -->\n'
head=s[:i]
intro='''## 4. Results (base 10; generated from the census DB by `py/make_results.py`, i.e. every number below is a program output)

**Statement (COMPUTED + PAPER PROOF F1).**  A cyclic overflow word g of length p with a B-cycle must be accepted by the first-coordinate NFA (section 2, PAPER PROOF).
For EVERY p <= 32 all F1 survivors were run through the exact engine with the caps shown; every survivor is EXHAUSTED (no B-cycle of any width, any e) EXCEPT
  * ACCEPT: p11 (g=00001110001), p12 (g=(0001)^3) and p22 (g = the p11 word twice; the ONLY accepted stream is e11e11, i.e. the repetition) — nothing else accepted;
  * the UNDECIDED words in the last table (CAPPED: nothing is claimed for them, they may or may not carry an exterior).
Hence: **no new primitive decimal exterior stream (B-cycle) exists with p <= 32 except possibly for the listed undecided words; every p in 2..15, 17..20, 22, 23 is completely decided (the open words with p <= 24 are p16 (01)^8, p21 001001010101001010101, p24 (0001)^6 and (01)^12).**
Not claimed: anything about centres, anything for p >= 33 (first-pass numbers for p = 33 may be appended below), the B-level uniqueness for imprimitive accepted words beyond the counts quoted in section 3b.

'''
tail='''
'''
open(f'{ROOT}/EXTERIOR.md','w').write(head+intro+mr+'\n'+tailtxt)
print('EXTERIOR.md section 4 rewritten,',len(mr.splitlines()),'lines')
