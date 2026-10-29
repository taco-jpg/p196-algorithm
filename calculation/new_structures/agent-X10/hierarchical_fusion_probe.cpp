// Experimental hierarchical two-level centre fusion: 6 -> 5 -> 3 packets.
#define main x10_4sheet_engine_main
#include "four_sheet_fast.cpp"
#undef main
#include <climits>
#include <stdexcept>
struct Dyn{vector<Packet> p;int n;};
static Packet merge_groups(const vector<pair<const Packet*,int>>& groups){
 int lo=INT_MAX,hi=INT_MIN;
 for(auto [p,shift]:groups)if(!p->empty()){
  lo=min(lo,shift+p->start);hi=max(hi,shift+p->end());
 }
 if(lo==INT_MAX)return {};
 vector<int> v(hi-lo+3,0);
 for(auto [p,shift]:groups)for(int j=0;j<p->length();j++)v[shift+p->start+j-lo]+=p->d[j];
 vector<unsigned char> d;d.reserve(v.size());int cy=0;
 for(int a:v){int z=a+cy;d.push_back(z%10);cy=z/10;}
 while(cy){d.push_back(cy%10);cy/=10;}
 while(!d.empty()&&!d.back())d.pop_back();
 int k=0;while(k<(int)d.size()&&!d[k])k++;
 if(k==(int)d.size())return {};
 d.erase(d.begin(),d.begin()+k);
 return {lo+k,move(d)};
}
static Dyn initial(){Dyn x;x.n=6;x.p.resize(6);x.p[0]={0,{5,7}};x.p[1]={0,{7,3}};x.p[2]={0,{8,7}};x.p[5]={0,{8,8}};return x;}
static Dyn evolve_mode(const Dyn&x,int R,int D){
 Dyn y;y.n=x.n;y.p.resize(x.n);
 int H=x.p.back().end();
 for(int i=0;i<x.n;i++){
  int offset=H;
  if(x.n==5&&i==2)offset+=D;
  if(x.n==3&&i==1)offset+=2*R+D;
  y.p[i]=newpacket(x.p[i],x.p[x.n-1-i],offset);
 }
 return y;
}
static Dyn fuse1(const Dyn&x,int D){
 if(x.n!=6)abort();Dyn y;y.n=5;y.p={x.p[0],x.p[1],merge_groups({{&x.p[2],0},{&x.p[3],D}}),x.p[4],x.p[5]};return y;
}
static Dyn fuse2(const Dyn&x,int R,int D){
 if(x.n!=5)abort();Dyn y;y.n=3;y.p={x.p[0],merge_groups({{&x.p[1],0},{&x.p[2],R},{&x.p[3],2*R+D}}),x.p[4]};return y;
}
static bool side_contact(const Dyn&x,int R,int D){
 if(x.n!=5)abort();
 auto&l=x.p[1],&c=x.p[2],&h=x.p[3];
 return (!l.empty()&&!c.empty()&&l.end()>=R+c.start)||(!c.empty()&&!h.empty()&&R+c.end()>=2*R+D+h.start);
}
static bool nonpal_outer(const Dyn&x){
 auto &a=x.p.front(),&b=x.p.back();int H=b.end();
 for(int j=0;j<a.length();j++){int k=H-(a.start+j)-b.start;int z=k>=0&&k<b.length()?b.d[k]:0;if(z!=a.d[j])return true;}
 for(int j=0;j<b.length();j++){int k=H-(b.start+j)-a.start;int z=k>=0&&k<a.length()?a.d[k]:0;if(z!=b.d[j])return true;}
 return false;
}
static int universal_q(const Dyn&x,int R,int D){
 vector<int> a,b;
 if(x.n==6){a={0,1,1,1,1,2};b={0,0,R,R+D,2*R+D,2*R+D};}
 if(x.n==5){a={0,1,1,1,2};b={0,0,R,2*R+D,2*R+D};}
 if(x.n==3){a={0,1,2};b={0,0,2*R+D};}
 if((int)a.size()!=x.n)abort();
 int Q=1;
 for(int i=0;i<x.n;i++)if(!x.p[i].empty()){
  if(a[i]==0){if(b[i]+x.p[i].start<0)throw runtime_error("negative invariant low exponent");}
  else Q=max(Q,ceil_div(-b[i]-x.p[i].start,a[i]));
  for(int j=i+1;j<x.n;j++)if(!x.p[j].empty()){
   if(x.n==6&&i==2&&j==3)continue;
   int slope=a[j]-a[i];
   int rhs=1+b[i]+x.p[i].end()-b[j]-x.p[j].start;
   if(slope==0){if(rhs>0)throw runtime_error("inner zero-slope buffer overlapped at stage "+to_string(x.n));}
   else Q=max(Q,ceil_div(rhs,slope));
  }
 }
 if(x.n==6){
  auto&l=x.p[2],&r=x.p[3];
  int lo=INT_MAX,hi=INT_MIN;
  if(!l.empty()){lo=min(lo,l.start);hi=max(hi,l.end());}
  if(!r.empty()){lo=min(lo,D+r.start);hi=max(hi,D+r.end());}
  if(lo!=INT_MAX){
    vector<int> values(hi-lo+1);
    for(int j=0;j<l.length();j++)values[l.start+j-lo]+=l.d[j];
    for(int j=0;j<r.length();j++)values[D+r.start+j-lo]+=r.d[j];
    for(int v:values)if(v>=10)throw runtime_error("central transparent capacity expired");
  }
 }
 return Q;
}

#ifndef HIERARCHY_LIBRARY
int main(int argc,char**argv){
 int R=argc>1?atoi(argv[1]):60;
 int T=argc>2?atoi(argv[2]):1000;
 int D=4,switch2=-1;Dyn x=initial();int qmin=1;
 for(int t=0;t<=T;t++){
  if(t==13)x=fuse1(x,D);
  if(x.n==5&&side_contact(x,R,D)){x=fuse2(x,R,D);switch2=t;}
  if(!nonpal_outer(x))throw runtime_error("outer witness lost at t="+to_string(t));
  qmin=max(qmin,universal_q(x,R,D));
  if(t<=20||t==88||t==176||t==264||t==352||t==512||t==1000||t==5000||t==10000||t==20000||t==T)
   cout<<"t="<<t<<" n="<<x.n<<" L="<<x.p[0].length()<<" C="<<x.p[x.n/2].length()<<" H="<<x.p.back().length()<<" qmin="<<qmin<<" fuse2_t="<<switch2<<"\n";
  if(t<T)x=evolve_mode(x,R,D);
 }
}

#endif // HIERARCHY_LIBRARY
