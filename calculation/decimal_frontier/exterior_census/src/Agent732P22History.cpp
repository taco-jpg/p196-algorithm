// Agent 732: exact weighted cut-state census for neutral-band B-histories.
// Single-threaded, no floating-point arithmetic, no state cap.
// Usage: g++ -O3 -std=c++17 Agent732P22History.cpp -o /tmp/agent732-history
//        /tmp/agent732-history 0000111000100001110001 95
#include <algorithm>
#include <array>
#include <fstream>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>
using namespace std;
using u64=uint64_t; using u128=__uint128_t;
struct Key { u64 lo,hi; bool operator==(Key const& o) const noexcept {return lo==o.lo&&hi==o.hi;} };
struct Hash {size_t operator()(Key const& k) const noexcept {u64 x=k.lo^((k.hi+0x9e3779b97f4a7c15ULL)*0xbf58476d1ce4e5b9ULL); x^=x>>30; x*=0xbf58476d1ce4e5b9ULL; x^=x>>27; x*=0x94d049bb133111ebULL; return (size_t)(x^(x>>31));}};
using Vec=unordered_map<Key,u64,Hash>;
struct Cut { u64 L,H,Y; };
struct Counter {
 int p,ng; vector<int> g,yi; vector<int> gidx; u64 mask;
 Counter(const string& s):p((int)s.size()),ng(0),g(p),yi(p,-1),mask((p>0&&p<=30)?((1ULL<<p)-1):0){
  if(p<1||p>30){cerr<<"requires 1<=p<=30\n";exit(2);}
  for(int t=0;t<p;t++){if(s[t]!='0'&&s[t]!='1'){cerr<<"binary g expected\n";exit(2);}g[t]=s[t]-'0';if(g[t]){yi[t]=ng++;gidx.push_back(t);}}
  if(2*p+4*ng>128||ng>16){cerr<<"state exceeds 128-bit storage or Y exceeds 64 bits\n";exit(2);}
 }
 Key key(const Cut& c)const{u128 v=(u128)c.L|((u128)c.H<<p)|((u128)c.Y<<(2*p));return {(u64)v,(u64)(v>>64)};}
 Cut decode(const Key& k)const{u128 v=((u128)k.hi<<64)|k.lo;Cut c; c.L=(u64)v&mask;c.H=(u64)(v>>p)&mask;c.Y=(u64)(v>>(2*p));return c;}
 void accumulate(Vec& dst,Key k,u64 weight) const {auto it=dst.find(k);if(it==dst.end()){dst.emplace(k,weight);return;}if(numeric_limits<u64>::max()-it->second<weight){cerr<<"MULTIPLICITY OVERFLOW\n";exit(3);}it->second+=weight;}
 template<class Fn> void succ(const Cut &c,bool first,Fn emit) const {
  for(int x0=first?1:0;x0<=18;x0++){
   auto dfs=[&](auto&& self,int t,int x,u64 Ln,u64 Hn,u64 Yn)->void{
    if(t==p){if(x==x0)emit(key({Ln,Hn,Yn}));return;}
    if(first&&x==0)return;
    int l=(int)((c.L>>t)&1),h=(int)((c.H>>t)&1);
    for(int carry=0;carry<=1;carry++){
     if((x+carry)/10!=h)continue;
     int digit=(x+carry)%10;
     int nx=(x+l)%10+(g[t]? (int)((c.Y>>(4*yi[t]))&15ULL) :digit);
     u64 Lnext=Ln|((u64)((x+l)/10)<<t),Hnext=Hn|((u64)carry<<t);
     u64 Ynext=Yn;
     if(g[t])Ynext|=((u64)digit)<<(4*yi[t]);
     self(self,t+1,nx,Lnext,Hnext,Ynext);
    }
   };
   dfs(dfs,0,x0,0,0,0);
  }
 }
 bool accepting(const Cut& c) const {
  if(((c.L^c.H)&mask)!=mask)return false;
  for(int i=0;i<ng;i++){int t=gidx[i],want=((c.L>>t)&1)?9:0;if(((c.Y>>(4*i))&15ULL)!=(u64)want)return false;}
  return true;
 }
 u64 accepted(const Vec& vec,vector<pair<u64,u64>>* all=nullptr)const{
  u64 count=0;for(auto& entry:vec){auto c=decode(entry.first);if(!accepting(c))continue;
   if(numeric_limits<u64>::max()-count<entry.second){cerr<<"ACCEPT OVERFLOW\n";exit(3);}count+=entry.second;
   if(all)all->push_back({c.L,entry.second});
  }return count;
 }
};
int main(int argc,char**argv){
 if(argc<3){cerr<<"usage: "<<argv[0]<<" <overflow-string> <max-width>\n";return 2;}
 string g=argv[1];int D=stoi(argv[2]);Counter m(g);
 int dumpDepth=-1;string dumpPath;
 if(argc==5){dumpDepth=stoi(argv[3]);dumpPath=argv[4]; if(dumpDepth<0||dumpDepth>D){cerr<<"invalid dump depth\n";return 2;}}
 u64 h=0;for(int t=0;t<m.p;t++)if(m.g[t])h|=1ULL<<t;
 u64 y=0;for(int i=0;i<m.ng;i++)y|=1ULL<<(4*i);
 Vec cur,next; cur.reserve(1024);cur.emplace(m.key({0,h,y}),1);
 int fixed=-1;u64 maxfront=0,nonzero=0;for(int d=0;d<=D;d++){
  auto accepted=m.accepted(cur);if(accepted)nonzero++;
  if(cur.size()>maxfront)maxfront=cur.size();
  if(d==dumpDepth){
   vector<array<u64,4>> rows; rows.reserve(cur.size());
   for(auto &e:cur){auto c=m.decode(e.first); rows.push_back({c.L,c.H,c.Y,e.second});}
   sort(rows.begin(),rows.end());
   ofstream csv(dumpPath); if(!csv){cerr<<"cannot write CSV\n";return 2;}
   for(auto &row:rows)csv<<row[0]<<","<<row[1]<<","<<row[2]<<","<<row[3]<<"\n";
   if(!csv){cerr<<"CSV write failed\n";return 2;}
  }
  if(d<=3||accepted||d%10==0||d==D)printf("depth=%d states=%zu accepted=%llu\n",d,cur.size(),(unsigned long long)accepted);
  if(accepted>0){vector<pair<u64,u64>> e;m.accepted(cur,&e);for(auto [L,n]:e){string es;for(int t=0;t<m.p;t++)es.push_back((L>>t)&1?'1':'0');printf("  ACCEPT_E=%s MULT=%llu\n",es.c_str(),(unsigned long long)n);}}
  if(d==D)break;
  next.clear();next.reserve(cur.size());
  size_t index=0;for(auto &ent:cur){Cut c=m.decode(ent.first);bool first=(d==0);m.succ(c,first,[&](Key k){m.accumulate(next,k,ent.second);});++index;}
  if(next==cur){fixed=d;printf("WEIGHTED_FIXED_POINT at transition depth %d -> %d states=%zu\n",d,d+1,cur.size());break;}
  cur.swap(next);
 }
 printf("SUMMARY p=%d G=%d maxfront=%llu fixed=%d\n",m.p,m.ng,(unsigned long long)maxfront,fixed);
 return fixed>=0||dumpDepth>=0?0:1;
}
