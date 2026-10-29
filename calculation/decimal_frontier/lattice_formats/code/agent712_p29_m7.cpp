// agent-712 local research: independent complete cyclic row maps, p29, spatial m7
// Not a claim of a rooted exterior, centre or Lychrel number.
#include <array>
#include <vector>
#include <map>
#include <unordered_map>
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <string>
#include <cassert>
#include <fstream>
using namespace std;
constexpr int B=10,M=7,Q=19*19*19*19,P=29,T=203;
const string g="00001110001000110001000110001";
using Row=array<int,M>;
// (1) pivot/carry-anchor method, independently verified against (2).
bool pivot(const Row &r, int gamma, Row &out) {
  int pivot=-1; for(int i=0;i<M;i++) if(r[i]!=B-1){pivot=i;break;}
  if(pivot<0)return false;
  int a[M]={},d[M]={};
  a[(pivot+1)%M]=(r[pivot]>=B); d[(pivot+M-1)%M]=(r[pivot]>=B);
  for(int s=1;s<M;s++){
    int i=(pivot+s)%M; a[(i+1)%M]=(r[i]+a[i])/B;
    int j=(pivot+M-s)%M;d[(j+M-1)%M]=(r[j]+d[j])/B;
  }
  int e[M],f[M];
  for(int i=0;i<M;i++){e[i]=(r[i]+a[i])%B;f[i]=(r[i]+d[i])%B;}
  for(int i=0;i<M;i++)out[i]=e[i]+f[gamma?(i+M-1)%M:i];
  return true;
}
// (2) direct simultaneous fixed point of cyclic carry equations; no pivot.
bool wrap(const Row &r,int gamma,Row &out) {
  bool neutral=true;for(auto x:r)neutral &= (x==B-1);if(neutral)return false;
  array<int,M> asc={},desc={}; int na=0,nd=0;
  for(int a0=0;a0<=1;a0++){
    array<int,M> tmp={};tmp[0]=a0;
    for(int i=0;i<M-1;i++)tmp[i+1]=(r[i]+tmp[i])/B;
    if((r[M-1]+tmp[M-1])/B==a0){assert(!na);asc=tmp;na++;}
  }
  for(int d0=0;d0<=1;d0++){
    array<int,M> tmp={};tmp[0]=d0;
    tmp[M-1]=(r[0]+tmp[0])/B;
    for(int i=M-1;i>=2;i--)tmp[i-1]=(r[i]+tmp[i])/B;
    if((r[1]+tmp[1])/B==d0){assert(!nd);desc=tmp;nd++;}
  }
  assert(na==1&&nd==1);
  for(int i=0;i<M;i++){
    int im=gamma?(i+M-1)%M:i;
    out[i]=(r[i]+asc[i])%B+(r[im]+desc[im])%B;
  }
  return true;
}
Row decode(int j){Row r{};int a=j%19;int b=j/19%19,c=j/361%19,d=j/6859%19;r={a,b,c,d,d,c,b};return r;}
int encode(const Row &r){if(r[1]!=r[6]||r[2]!=r[5]||r[3]!=r[4])return -2;
  return r[0]+19*r[1]+361*r[2]+6859*r[3];}
int primitive(const Row &r) {for(int d=1;d<=M;d++)if(M%d==0){bool yes=true;for(int i=0;i<M;i++)if(r[i]!=r[(i+d)%M])yes=false;if(yes)return d;}return M;}
int run(Row r, bool usepivot) {
  Row o{};
  for(int i=0;i<T;i++){
    if(!(usepivot ? pivot(r,g[i%P]-'0',o) : wrap(r,g[i%P]-'0',o))) return -1;
    r=o;
  }
  return encode(r);
}
int main(int argc,char**argv) {
  static_assert(T==7*P);
  assert(g.size()==P && count(g.begin(),g.end(),'1')==10);
  vector<int> next(Q,-2);int dead=0,wrong=0,consistent=0;
  for(int id=0;id<Q;id++){
    Row r=decode(id);
    int a=run(r,true),b=run(r,false);
    if(a!=b){cerr<<"DISAGREEMENT id="<<id<<" results "<<a<<" "<<b<<"\n";return 2;}
    if(a==-2){wrong++;cerr<<"WRONG AXIS id="<<id<<"\n"; return 3;}
    if(a==-1)dead++; else consistent++;
    next[id]=a;
  }
  if(argc>1) {
    if(argc!=3 || string(argv[1])!="--dump-map") { cerr<<"usage: agent712_p29_m7 [--dump-map PATH]\n";return 4; }
    ofstream f(argv[2]); if(!f){cerr<<"cannot open map output\n";return 5;}
    for(int v:next)f<<v<<"\n";
  }
  // Functional graph with sink -1 (all-neutral row encountered). Global length bound Q.
  vector<int> indeg(Q,0);for(int id=0;id<Q;id++)if(next[id]>=0)indeg[next[id]]++;
  vector<int> que;que.reserve(Q);
  for(int id=0;id<Q;id++)if(indeg[id]==0)que.push_back(id);
  for(size_t pos=0;pos<que.size();pos++){
    int id=que[pos],n=next[id]; if(n>=0 && --indeg[n]==0)que.push_back(n);
  }
  vector<char> seen(Q,false);map<pair<int,int>,int> hist;int ncyc=0,ncycprim=0,nnodes=0,nodesprim=0;
  for(int id=0;id<Q;id++) if(indeg[id]>0 && !seen[id]){
    vector<int> cycle;int u=id;
    do{seen[u]=true;cycle.push_back(u);u=next[u];}while(u!=id);
    bool prim=false; for(int v:cycle)if(primitive(decode(v))==M)prim=true;
    int period=cycle.size();hist[{prim?M:1,period}]++;
    ncyc++;nnodes+=period;
    if(prim){ncycprim++;nodesprim+=period;}
    cout<<"CYCLE kind="<<(prim?"primitive-m7":"uniform-m1")<<" length="<<period<<" actual_temporal_steps="<<T*period<<" representative=";
    for(auto x:decode(id))cout<<x<<",";
    cout<<"\n";
  }
  cout<<"SUMMARY p="<<P<<" S=10 m="<<M<<" starts="<<Q<<" dead="<<dead<<" valid="<<consistent<<" wrong="<<wrong<<" map_agreement="<<Q<<" complete_cycles="<<ncyc<<" primitive_cycles="<<ncycprim<<" recurrent_nodes="<<nnodes<<" primitive_recurrent_nodes="<<nodesprim<<"\n";
  for(auto [k,v]:hist)cout<<"HIST primitive_m="<<k.first<<" length="<<k.second<<" count="<<v<<"\n";
}
