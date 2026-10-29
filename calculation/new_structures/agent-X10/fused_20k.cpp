// Independent 3-packet exact arithmetic symbolic continuation from the first central crossing.
// Physical bases are 0, q, and 2q+D (D=4): a *single* central packet absorbs
// cross-sheet carries, retaining ordinary decimal digits even after t=14.
#define main four_sheet_engine_main
#include "four_sheet_fast.cpp"
#undef main
#include <stdexcept>
#include <climits>

static constexpr int D=4;
struct Three {Packet low, mid, high;};
static Packet fuse(const Packet&a,const Packet&b){
 int lo=INT_MAX,hi=INT_MIN;
 if(!a.empty()){lo=min(lo,a.start);hi=max(hi,a.end());}
 if(!b.empty()){lo=min(lo,D+b.start);hi=max(hi,D+b.end());}
 if(lo==INT_MAX)return {};
 vector<int> raw(hi-lo+2,0);
 for(int j=0;j<a.length();j++)raw[a.start+j-lo]+=a.d[j];
 for(int j=0;j<b.length();j++)raw[D+b.start+j-lo]+=b.d[j];
 int cy=0;vector<unsigned char> res(raw.size());
 for(size_t i=0;i<raw.size();i++){int v=raw[i]+cy;res[i]=(unsigned char)(v%10);cy=v/10;}
 if(cy)res.push_back(cy);
 while(!res.empty()&&!res.back())res.pop_back();
 int skip=0;while(skip<(int)res.size()&&!res[skip])skip++;
 if(skip==(int)res.size())return {};
 res.erase(res.begin(),res.begin()+skip);
 return {lo+skip,move(res)};
}
static Three next(const Three&x){
 if(x.high.empty())throw runtime_error("missing top");
 Three y;
 y.low=newpacket(x.low,x.high,x.high.end());
 y.high=newpacket(x.high,x.low,x.high.end());
 y.mid=newpacket(x.mid,x.mid,D+x.high.end());
 return y;
}
static int universal_qmin(const Three&x){
 if(x.high.empty())throw runtime_error("missing top");
 if(!x.low.empty()&&x.low.start<0)throw runtime_error("negative low");
 int Q=1;
 if(!x.mid.empty()){
   Q=max(Q,ceil_div(-x.mid.start,1));
   if(!x.low.empty())Q=max(Q,1+x.low.end()-x.mid.start);
   Q=max(Q,1+x.mid.end()-D-x.high.start);
 }
 Q=max(Q,ceil_div(-D-x.high.start,2));
 if(!x.low.empty())Q=max(Q,ceil_div(1+x.low.end()-D-x.high.start,2));
 return Q;
}
static bool nonpal_outer(const Three&x){
 if(x.high.empty())throw runtime_error("missing top");
 int H=x.high.end();
 for(int j=0;j<x.low.length();j++){
   int target=H-(x.low.start+j)-x.high.start;
   int d=(target>=0&&target<x.high.length())?x.high.d[target]:0;
   if(x.low.d[j]!=d)return true;
 }
 for(int j=0;j<x.high.length();j++){
   int target=H-(x.high.start+j)-x.low.start;
   int d=(target>=0&&target<x.low.length())?x.low.d[target]:0;
   if(x.high.d[j]!=d)return true;
 }
 return false;
}
static uint64_t hash3(const Three&x){
 uint64_t z=1469598103934665603ULL;
 for(const Packet&p:{x.low,x.mid,x.high}){
  z^=(uint32_t)p.start;z*=1099511628211ULL;
  for(auto d:p.d){z^=d;z*=1099511628211ULL;}
 }
 return z;
}

#ifndef FUSED20K_LIBRARY
int main(int argc,char**argv){
 int T=argc>1?atoi(argv[1]):20000;
 if(T<13)throw runtime_error("T must be >=13");
 S f;f[0]={0,{5,7}};f[1]={0,{8,7}};f[2]={};f[3]={0,{8,8}};
 for(int t=0;t<13;t++)f=evolve(f);
 Three x={f[0],fuse(f[1],f[2]),f[3]};
 int Q=11,nonpal=0;
 cout<<"t,qmin,lowlen,midlen,highlen,midlo,midhi,highend,nonpal_witness,fnv64\n";
 for(int t=13;t<=T;t++){
  Q=max(Q,universal_qmin(x));
  bool nonpalnow=nonpal_outer(x);
  if(nonpalnow)nonpal++;
  else throw runtime_error("outer nonpal witness failed at t="+to_string(t));
  if(t==13||t==14||t==15||t==88||t==264||t==1000||t==5000||t==10000||t==T)
   cout<<t<<","<<Q<<","<<x.low.length()<<","<<x.mid.length()<<","<<x.high.length()<<","<<x.mid.start<<","<<x.mid.end()<<","<<x.high.end()<<","<<nonpalnow<<","<<hash3(x)<<"\n";
  if(t<T)x=next(x);
 }
 cout<<"SUMMARY steps="<<T<<" q_min="<<Q<<" safe_states="<<(T+1)<<" all_outer_nonpal="<<(nonpal==T-12)<<" mid_at_final="<<x.mid.length()<<"\n";
}

#endif // FUSED20K_LIBRARY
