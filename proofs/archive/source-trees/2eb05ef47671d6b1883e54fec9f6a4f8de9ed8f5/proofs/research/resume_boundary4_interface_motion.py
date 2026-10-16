"""Explore interface motion; exact finite return equality is separately checked."""
from resume_defect_interface import strip_step,travels
from resume_defect_center import BASE
import json

def run(rot,right_value,steps=512):
 left=BASE[rot:]+BASE[:rot];right=(right_value,)
 margin=2*steps+128
 L=((margin+3)//4)*4
 q=left*(L//4)+right*margin
 origin=0;initial_left=left;history=[];seen={};hit=None
 for t in range(steps+1):
  if t%16==0:
   a=0;b=len(q)
   while a<b and q[a]==left[(origin+a)%4]:a+=1
   while b>a and q[b-1]==right[0]:b-=1
   assert a>=16 and len(q)-b>=16, "Interface reached artificial boundary"
   core=q[a:b]
   item={'time':t,'left_front':origin+a-L,'right_front':origin+b-L,'width':len(core),'left_phase':(origin+a)%4}
   key=((origin+a)%4,core)
   if key in seen:
    tt,pos=seen[key];period=t-tt;velocity=origin+a-pos
    phase=(origin+a)%4
    paddedleft=initial_left[phase:]+initial_left[:phase]
    # travels uses left periodic buffer terminating at phase zero.
    exact=travels(core,paddedleft,(right_value,),steps=period,shift=velocity)
    hit={'period':period,'shift':velocity,'start_time':tt,'core':core,'left':paddedleft,'right':right_value,'exact_travels_check':exact}
    if exact:break
   seen[key]=(t,origin+a)
   history.append(item)
  if t==steps:break
  q,left,right,origin=strip_step(q,left,right,origin,t%2)
 return {'rotation':rot,'right':right_value,'steps':steps,'history':history,'travelling_interface':hit}
if __name__=='__main__':
 out=[]
 for rot in range(4):
  for r in (6,12):
   x=run(rot,r);out.append(x)
   print(json.dumps({'rotation':rot,'right':r,'last':x['history'][-1],'travelling_interface':x['travelling_interface']}),flush=True)
   json.dump(out,open('resume_boundary4_interface_motion_results.json','w'),indent=2)
