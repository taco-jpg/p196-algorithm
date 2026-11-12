from walls import *
import sys
kmax=int(sys.argv[1]); Qmax=int(sys.argv[2])
wall_scan('p11',(0,0,0,0,1,1,1,0,0,0,1),kmax,Qmax,maxnodes=3000000)
wall_scan('p12',(0,0,0,1,0,0,0,1,0,0,0,1),kmax,Qmax,maxnodes=3000000)
