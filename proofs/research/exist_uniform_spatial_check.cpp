// Independent exact decimal arithmetic for the uniform-run exterior graph.
// No Python transition code or cached search artifacts are imported.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <set>
#include <functional>
#include <iomanip>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;
struct Half {int a,b,l,r;};
struct State {array<uint8_t,64> x{}; bool operator==(State const&o)const{return x==o.x;}};
struct Hash {size_t operator()(State const&s)const{size_t h=1469598103934665603ULL;for(auto a:s.x){h^=a;h*=1099511628211ULL;}return h;}};
struct Search {
 int g=0; vector<int> ps; vector<pair<int,int>> graph_edges; unordered_map<int,vector<Half>> cache;
 unordered_map<State,int,Hash> ids; vector<State> states; vector<int> depths; vector<array<int,3>> parents;
 chrono::steady_clock::time_point start;double seconds;size_t cap;long long edges=0;int maxdepth=0;bool complete=true;int found=-1,founddigit=0;
 vector<Half> const& half(int a,int b,int l,int r,int p){
  int key=a+10*b+100*l+3200*r+102400*p;
  auto it=cache.find(key);if(it!=cache.end())return it->second;
  vector<Half> cur{{a,b,0,0}};
  for(int t=0;t<p;t++){
   vector<Half> out;
   for(auto z:cur)for(int u=0;u<2;u++){
    int left=z.a+z.b+u,right=z.a+z.b+((r>>t)&1);
    if(left/10==((l>>t)&1))out.push_back({left%10,right%10,z.l|(u<<t),z.r|((right/10)<<t)});
   }
   cur=move(out);
  }
  return cache.emplace(key,move(cur)).first->second;
 }
 double elapsed()const{return chrono::duration<double>(chrono::steady_clock::now()-start).count();}
 bool target(State const&s,int d){
  int initial=d;
  for(int j=0;j<g;j++){
   if(s.x[j]!=d)return false;
   int m=0;
   for(int i=0;i<ps[j];i++){int h=d>=5;m|=h<<i;d=2*d-9*h;}
   if(s.x[g+j]!=m||s.x[2*g+j]!=m)return false;
  }
  return d==initial;
 }
 void visit(State const&s,State &ns,int j,int dr,int first,int parent){
  if(!complete)return;
  if(j==g){
   if(dr!=first)return;
   edges++;
   auto [it,inserted]=ids.emplace(ns,int(states.size()));
   graph_edges.emplace_back(parent,it->second);
   if(inserted){states.push_back(ns);depths.push_back(depths[parent]+1);parents.push_back({parent,s.x[0],first});}
   if(states.size()>cap){complete=false;return;}
   if((edges&4095)==0&&elapsed()>seconds)complete=false;
   return;
  }
  // Copy the tiny local vector: later cache insertion cannot invalidate it.
  auto options=half(s.x[j],dr,s.x[g+j],s.x[2*g+j],ps[j]);
  for(auto z:options){
   ns.x[(j+1)%g]=z.a;ns.x[g+j]=z.l;ns.x[2*g+j]=z.r;
   visit(s,ns,j+1,z.b,first,parent);
   if(!complete)return;
  }
 }
 void run(){
  g=ps.size();start=chrono::steady_clock::now();State initial;
  for(int j=0;j<g;j++){initial.x[j]=1;initial.x[g+j]=1<<(ps[j]-1);}
  ids.emplace(initial,0);states.push_back(initial);depths.push_back(0);parents.push_back({-1,0,0});
  for(size_t i=0;i<states.size();i++){
   if(elapsed()>seconds){complete=false;break;}
   State s=states[i];maxdepth=max(maxdepth,depths[i]);
   for(int d:{8,7,5,1,2,4})if(target(s,d)){found=i;founddigit=d;break;}
   if(found>=0)break;
   State ns;for(int first=0;first<10;first++){visit(s,ns,0,first,first,i);if(!complete)break;}
   if(!complete)break;
  }
  vector<int> indeg(states.size(),0);vector<vector<int>> adj(states.size());
  for(auto [u,v]:graph_edges){indeg[v]++;adj[u].push_back(v);}
  vector<int> queue;for(int i=0;i<int(states.size());i++)if(indeg[i]==0)queue.push_back(i);
  for(size_t i=0;i<queue.size();i++)for(int v:adj[queue[i]])if(--indeg[v]==0)queue.push_back(v);
  size_t cyclic_remainder=states.size()-queue.size();
  cout<<"{\"periods\":[";for(int j=0;j<g;j++)cout<<(j?",":"")<<ps[j];
  cout<<"],\"states\":"<<states.size()<<",\"edges\":"<<edges<<",\"maxdepth\":"<<maxdepth<<",\"cyclic_remainder\":"<<cyclic_remainder<<",\"complete\":"<<(complete?"true":"false")<<",\"seconds\":"<<elapsed()<<",\"found\":";
  if(found<0)cout<<"null";
  else{
   cout<<"{\"bulk_digit\":"<<founddigit<<",\"path\":[";
   vector<array<int,3>> path;for(int i=found;parents[i][0]>=0;i=parents[i][0])path.push_back(parents[i]);reverse(path.begin(),path.end());
   for(size_t i=0;i<path.size();i++)cout<<(i?",":"")<<"["<<path[i][1]<<","<<path[i][2]<<"]";
   cout<<"]}";
  }
  cout<<"}\n";
 }
};
int clock_catalog(){
 const int p=24,g=9;const uint32_t mask=(1u<<p)-1;
 vector<set<pair<int,int>>> out(19);
 for(int a=1;a<=18;a++)for(int b=0;b<2;b++){
  int low=a%10,high=(a+b)%10,h=(a+b)/10;
  int next=h?low+1:low+high;out[a].insert({next,h});
 }
 set<uint32_t> clocks;uint64_t calls=0;
 function<void(int,int,int,int,uint32_t)> dfs=[&](int initial,int a,int t,int growth,uint32_t word){
  calls++;if(growth>g||growth+p-t<g)return;
  if(t==p){
   if(a!=initial||growth!=g)return;
   uint32_t best=word;
   for(int shift=1;shift<p;shift++)best=min(best,((word<<shift)|(word>>(p-shift)))&mask);
   clocks.insert(best);return;
  }
  for(auto [next,h]:out[a])dfs(initial,next,t+1,growth+h,(word<<1)|h);
 };
 for(int a=1;a<=18;a++)dfs(a,a,0,0,0);
 cout<<"{\"period\":24,\"growth\":9,\"calls\":"<<calls<<",\"count\":"<<clocks.size()<<",\"clocks\":[";
 bool first=true;for(auto word:clocks){if(!first)cout<<",";first=false;cout<<"\"";for(int i=23;i>=0;i--)cout<<((word>>i)&1);cout<<"\"";}
 cout<<"]}\n";return 0;
}
int main(int argc,char**argv){
 if(argc==2&&string(argv[1])=="--clock-catalog")return clock_catalog();
 if(argc<4||argc>23){cerr<<"usage: executable seconds cap p1 ... pg (g<=20)\n";return 2;}
 Search s;s.seconds=atof(argv[1]);s.cap=strtoull(argv[2],nullptr,10);for(int i=3;i<argc;i++){int p=atoi(argv[i]);if(p<1||p>5)return 3;s.ps.push_back(p);}s.run();
}
