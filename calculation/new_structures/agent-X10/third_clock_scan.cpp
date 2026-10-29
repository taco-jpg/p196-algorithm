#define NESTED3_LIBRARY
#include "nested_three_fusion_probe.cpp"
int main(int argc,char**argv){
 int R=argc>1?atoi(argv[1]):56,T=argc>2?atoi(argv[2]):500,D=4;
 Dyn x=initial8();int t2=-1;
 vector<int> demand(T+1,-1);
 for(int t=0;t<=T;t++){
  if(t==13)x=fuse8to7(x,D);
  if(x.n==7&&contact7(x,R,D)){x=fuse7to5(x,R,D);t2=t;}
  if(x.n==5){
   const auto&a=x.p[1],&c=x.p[2],&b=x.p[3];
   int lhs=a.empty()||c.empty()?-100000:a.end()-c.start;
   int rhs=c.empty()||b.empty()?-100000:c.end()-(2*R+D)-b.start;
   demand[t]=max(lhs,rhs);
  }
  if(t<T)x=next_nested(x,R,1000,D); // S has no influence before fusion3.
 }
 cout<<"S,third_fusion_t,demand_at_fusion\n";
 for(int S=70;S<=180;S++){
  int first=-1;
  for(int t=t2;t<=T;t++)if(demand[t]>=S){first=t;break;}
  if(S%10==0||first==176||first==264||S==108||S==109||S==110)
    cout<<S<<","<<first<<","<<(first>=0?demand[first]:-1)<<"\n";
 }
 cout<<"CHECK R="<<R<<" fuse2_t="<<t2<<" demand_t176="<<demand[176]<<" demand_t264="<<demand[264]<<"\n";
}
