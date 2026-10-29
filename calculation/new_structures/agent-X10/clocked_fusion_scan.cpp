#define HIERARCHY_LIBRARY
#include "hierarchical_fusion_probe.cpp"
int main(int argc,char**argv){
 int limit=argc>1?atoi(argv[1]):500,D=4;
 Dyn f=initial();for(int t=0;t<13;t++)f=evolve_mode(f,60,D);
 Dyn x=fuse1(f,D);
 vector<int> clock(limit+1,0),demand(limit+1,0);
 for(int t=13;t<=limit;t++){
  const auto&l=x.p[1],&c=x.p[2],&h=x.p[3];
  int A=l.empty()||c.empty()?-100000:l.end()-c.start;
  int B=c.empty()||h.empty()?-100000:c.end()-D-h.start;
  demand[t]=max(A,B);
  if(t<limit)x=evolve_mode(x,60,D);
 }
 cout<<"R,first_fusion,source_clock_demand\n";
 for(int R=10;R<=150;R++){
  int first=-1;
  for(int t=13;t<=limit;t++)if(demand[t]>=R){first=t;break;}
  if(R%5==0||first==88||first==176||first==264)
    cout<<R<<","<<first<<","<<(first>=0?demand[first]:-1)<<"\n";
 }
 cout<<"MILESTONE_DEMAND t=88 "<<demand[88]<<" t=176 "<<demand[176]<<" t=264 "<<demand[264]<<"\n";
}
