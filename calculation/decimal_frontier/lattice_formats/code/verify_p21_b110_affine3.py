#!/usr/bin/env python3
"""For-all-n affine proof of three exact periodic exterior head columns.
Not an actual infinite integer orbit or complete exterior certificate.
"""
import json,sys
w=json.load(open(sys.argv[1]));G=w['g'];base=w['base'];B=w['step'];P=len(G)
assert (base,B,G,P)==(110,9809879625,'001001010101001010101',21)
Q,R,S=[w[k] for k in ('first','second','third')]
U,V,W=[w[k] for k in ('firstSlope','secondSlope','thirdSlope')]
c0,c1,c2=[w[k] for k in ('c0','c1','c2')]
a2,a3=w['quotient2'],w['quotient3']
assert all(len(x)==22 for x in [Q,R,S,U,V,W])
assert all(len(x)==21 for x in [c0,c1,c2,a2,a3])
assert (Q[0],R[0],S[0])==(40,99,73)
for x in (Q,R,S,U,V,W):assert x[0]==x[-1]
for t,letter in enumerate(G):
 g=int(letter);d=a2[t];e=a3[t]
 assert all(v in (0,1) for v in (g,c0[t],c1[t],c2[t],d,e))
 assert 1<=Q[t]<=2*base-2 and 0<=R[t]<=2*base-2 and 0<=S[t]<=2*base-2
 assert all(0<=a<=2*B for a in (U[t],V[t],W[t]))
 # Actual carry quotients and affine floor bounds guarantee all n>=0.
 assert (Q[t]+c0[t])//base==g and B*g<=U[t]<=B*(g+1)
 assert (R[t]+g)//base==d and B*d<=V[t]<=B*(d+1)
 assert (R[t]+c1[t])//base==c0[t] and B*c0[t]<=V[t]<=B*(c0[t]+1)
 assert (S[t]+d)//base==e and B*e<=W[t]<=B*(e+1)
 assert (S[t]+c2[t])//base==c1[t] and B*c1[t]<=W[t]<=B*(c1[t]+1)
 if g==0:
  assert Q[t+1]==2*Q[t]+c0[t] and U[t+1]==2*U[t]
  assert R[t+1]==2*R[t]+c1[t]-base*(d+c0[t])
  assert V[t+1]==2*V[t]-B*(d+c0[t])
  assert S[t+1]==2*S[t]+d+c2[t]-base*(e+c1[t])
  assert W[t+1]==2*W[t]-B*(e+c1[t])
 else:
  assert Q[t+1]==Q[t]-base+1 and U[t+1]==U[t]-B
  assert R[t+1]==R[t]+1+Q[t]+c0[t]-base*(d+1)
  assert V[t+1]==V[t]+U[t]-B*(d+1)
  assert S[t+1]==S[t]+d+R[t]+c1[t]-base*(e+c0[t])
  assert W[t+1]==W[t]+V[t]-B*(e+c0[t])
print('PASS exact 3-column affine pump for ALL integers n>=0')
print('base 110+9809879625*n, temporal period21, closed coefficients (40,99,73)')
print('No full exterior, band, centre, real orbit, or base10 Lychrel claim')
