// Experimental packet stack: 8 -> 7 -> 5 -> 3 sheets, two adjustable delays.
#define HIERARCHY_LIBRARY
#include "hierarchical_fusion_probe.cpp"
static Dyn initial8(){Dyn x;x.n=8;x.p.resize(8);x.p[0]={0,{5,7}};x.p[1]={0,{7,3}};x.p[2]={0,{7,3}};x.p[3]={0,{8,7}};x.p[7]={0,{8,8}};return x;}
static Dyn next_nested(const Dyn&x,int R,int S,int D){
 Dyn y;y.n=x.n;y.p.resize(x.n);
 int H=x.p.back().end();
 for(int i=0;i<x.n;i++){
  int mirror=H;
  if(x.n==7&&i==3)mirror+=D;
  if(x.n==5&&i==2)mirror+=2*R+D;
  if(x.n==3&&i==1)mirror+=2*S+2*R+D;
  y.p[i]=newpacket(x.p[i],x.p[x.n-1-i],mirror);
 }
 return y;
}
static Dyn fuse8to7(const Dyn&x,int D){
 if(x.n!=8)abort();Dyn y;y.n=7;
 y.p={x.p[0],x.p[1],x.p[2],merge_groups({{&x.p[3],0},{&x.p[4],D}}),x.p[5],x.p[6],x.p[7]};
 return y;
}
static Dyn fuse7to5(const Dyn&x,int R,int D){
 if(x.n!=7)abort();Dyn y;y.n=5;
 y.p={x.p[0],x.p[1],merge_groups({{&x.p[2],0},{&x.p[3],R},{&x.p[4],2*R+D}}),x.p[5],x.p[6]};
 return y;
}
static Dyn fuse5to3(const Dyn&x,int S,int R,int D){
 if(x.n!=5)abort();Dyn y;y.n=3;
 y.p={x.p[0],merge_groups({{&x.p[1],0},{&x.p[2],S},{&x.p[3],2*S+2*R+D}}),x.p[4]};
 return y;
}
static bool contact7(const Dyn&x,int R,int D){
 if(x.n!=7)abort();auto &a=x.p[2],&c=x.p[3],&b=x.p[4];
 return (!a.empty()&&!c.empty()&&a.end()>=R+c.start) ||
        (!c.empty()&&!b.empty()&&R+c.end()>=2*R+D+b.start);
}
static bool contact5(const Dyn&x,int S,int R,int D){
 if(x.n!=5)abort();auto &a=x.p[1],&c=x.p[2],&b=x.p[3];
 return (!a.empty()&&!c.empty()&&a.end()>=S+c.start) ||
        (!c.empty()&&!b.empty()&&S+c.end()>=2*S+2*R+D+b.start);
}
static int universal_q_nested(const Dyn&x,int R,int S,int D){
 vector<int> a,b;
 if(x.n==8){a={0,1,1,1,1,1,1,2};b={0,0,S,S+R,S+R+D,S+2*R+D,2*S+2*R+D,2*S+2*R+D};}
 if(x.n==7){a={0,1,1,1,1,1,2};b={0,0,S,S+R,S+2*R+D,2*S+2*R+D,2*S+2*R+D};}
 if(x.n==5){a={0,1,1,1,2};b={0,0,S,2*S+2*R+D,2*S+2*R+D};}
 if(x.n==3){a={0,1,2};b={0,0,2*S+2*R+D};}
 if((int)a.size()!=x.n)abort();int Q=1;
 for(int i=0;i<x.n;i++)if(!x.p[i].empty()){
  if(a[i]==0){if(b[i]+x.p[i].start<0)throw runtime_error("negative low exponent");}
  else Q=max(Q,ceil_div(-b[i]-x.p[i].start,a[i]));
  for(int j=i+1;j<x.n;j++)if(!x.p[j].empty()){
   if(x.n==8&&i==3&&j==4)continue;
   int m=a[j]-a[i];int rhs=1+b[i]+x.p[i].end()-b[j]-x.p[j].start;
   if(m==0){if(rhs>0)throw runtime_error("nested finite gap collapse outside assigned fuse");}
   else Q=max(Q,ceil_div(rhs,m));
  }
 }
 if(x.n==8){
  auto &l=x.p[3],&r=x.p[4];int lo=INT_MAX,hi=INT_MIN;
  if(!l.empty()){lo=min(lo,l.start);hi=max(hi,l.end());}
  if(!r.empty()){lo=min(lo,D+r.start);hi=max(hi,D+r.end());}
  if(lo!=INT_MAX){vector<int> v(hi-lo+1);
   for(int j=0;j<l.length();j++)v[l.start+j-lo]+=l.d[j];
   for(int j=0;j<r.length();j++)v[D+r.start+j-lo]+=r.d[j];
   for(int z:v)if(z>=10)throw runtime_error("unfused central capacity >9");
  }
 }
 return Q;
}
#ifndef NESTED3_LIBRARY
int main(int argc,char**argv){
 int R=argc>1?atoi(argv[1]):56,S=argc>2?atoi(argv[2]):110,T=argc>3?atoi(argv[3]):1000,D=4;
 Dyn x=initial8();int first=-1,second=-1,Q=1;
 for(int t=0;t<=T;t++){
  if(t==13)x=fuse8to7(x,D);
  if(x.n==7&&contact7(x,R,D)){x=fuse7to5(x,R,D);first=t;}
  if(x.n==5&&contact5(x,S,R,D)){x=fuse5to3(x,S,R,D);second=t;}
  Q=max(Q,universal_q_nested(x,R,S,D));
  if(!nonpal_outer(x))throw runtime_error("exposed outer mismatch lost");
  if(t<=13||t==first||t==second||t==88||t==176||t==264||t==1000||t==5000||t==10000||t==20000||t==T)
   cout<<"t="<<t<<" n="<<x.n<<" C="<<x.p[x.n/2].length()<<" Q="<<Q<<" second="<<first<<" third="<<second<<"\n";
  if(t<T)x=next_nested(x,R,S,D);
 }
}
#endif // NESTED3_LIBRARY
