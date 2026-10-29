// Deterministic rooted temporal strip discovery, not SCC enumeration.
// g++ -O3 -std=c++17 .../carryset_discover.cpp -o /tmp/n14discover
// cd calculation/new_structures/agent-N14 && /tmp/n14discover 7 7000 300
#include <bits/stdc++.h>
using namespace std;
using ll=long long;
struct Row{array<uint8_t,12>x;uint8_t g,u;};
mt19937_64 rng(14);
int K;
uint64_t encode(const array<uint8_t,12>&x){uint64_t k=0;for(int i=0;i<K;i++)k=k*19+x[i];return k;}
bool primitive(const string&g){int n=g.size();for(int p=1;p<n;p++)if(n%p==0){bool eq=1;for(int i=p;i<n;i++)if(g[i]!=g[i%p]){eq=0;break;}if(eq)return false;}return true;}
int horizonFlex(vector<Row>&v,int off,int p){
 vector<int> allow(p),L(p);vector<uint8_t>gam(p);
 for(int t=0;t<p;t++){
  const auto &x=v[off+t].x; const auto &next=v[off+(t+1)%p].x;
  int lo[12]={};for(int j=1;j<K;j++)lo[j]=(x[j-1]+lo[j-1])/10;
  L[t]=(x[K-1]+lo[K-1])/10;gam[t]=v[off+t].g;
  for(int u=0;u<2;u++){
   int c[12]={};c[K-1]=u;for(int j=K-1;j>=1;j--)c[j-1]=(x[j]+c[j])/10;
   int gg=(x[0]+c[0])/10;if(gg!=gam[t])continue;
   bool ok=true;
   for(int j=0;j<K;j++){
    int partner=gg?(j==0?1:(x[j-1]+c[j-1])%10):(x[j]+c[j])%10;
    if((x[j]+lo[j])%10+partner !=next[j]){ok=false;break;}
   }
   if(ok)allow[t] |= 1<<u;
  }
  if(!allow[t])return 0;
 }
 uint32_t S=(1u<<19)-1;unordered_set<uint64_t>seen;
 for(int t=0;t<19*p+2;t++){
  uint64_t key=(uint64_t(t%p)<<19)|S;if(seen.count(key))return -1;seen.insert(key);
  int j=t%p;uint32_t T=0;
  for(int z=0;z<19;z++)if((S>>z)&1){
   for(int upper=0;upper<2;upper++){
    int u=(z+upper)/10;if(!(allow[j]&(1<<u)))continue;
    int partner=gam[j]?(v[off+j].x[K-1]+u)%10:(z+upper)%10;
    int zn=(z+L[j])%10+partner;T|=1u<<zn;
   }
  }
  if(!T)return t+1;S=T;
 }
 return -2;
}
int main(int argc,char**argv){
 K=argc>1?atoi(argv[1]):7;ll runs=argc>2?atoll(argv[2]):7000;int maxsteps=argc>3?atoi(argv[3]):300;
 assert(K>=1 && K<=12);
 vector<Row>v;v.reserve(maxsteps);
 for(ll run=0;run<runs;run++){
  array<uint8_t,12>x{};x[0]=1+rng()%18;for(int j=1;j<K;j++)x[j]=rng()%19;
  unordered_map<uint64_t,int>seen;v.clear();
  for(int t=0;t<maxsteps;t++){
   auto [it,inserted]=seen.emplace(encode(x),t);
   if(!inserted){
    int off=it->second,p=t-off;
    if(p>=28 && p<=80){
     string g;for(int j=off;j<t;j++)g+=char('0'+v[j].g);
     if(primitive(g)){
      int depth=horizonFlex(v,off,p);
      if(depth<0){
       cout<<"INFINITE_NEXT_COLUMN run="<<run<<" p="<<p<<" K="<<K<<" gamma="<<g<<"\n";
       ofstream w("n14_k7_found.txt");
       w<<"gamma="<<g<<"\nrows=";
       for(int j=off;j<t;j++){
        if(j>off)w<<";";
        for(int k=0;k<K;k++){if(k)w<<",";w<<int(v[j].x[k]);}
       }
       w<<"\n";
       return 0;
      }
     }
    }
    break;
   }
   array<uint8_t,12>c{},l{},nx{};c[K-1]=rng()%2;
   for(int j=K-1;j>=1;j--)c[j-1]=(x[j]+c[j])/10;
   int g=(x[0]+c[0])/10;
   for(int j=1;j<K;j++)l[j]=(x[j-1]+l[j-1])/10;
   for(int j=0;j<K;j++){
    int partner=g?(j==0?1:(x[j-1]+c[j-1])%10):(x[j]+c[j])%10;
    nx[j]=(x[j]+l[j])%10+partner;
   }
   v.push_back({x,(uint8_t)g,c[K-1]});x=nx;
   if(x[0]==0)break;
  }
 }
 cerr<<"no lift candidate under run cap\n";
 return 1;
}
