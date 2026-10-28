// Agent-2 K1: exact period-T=24 stationary first-defect rec2 spatial transfer.
// Full unquotiented 96-bit cut-state graph, DFS cycle detection.
// Excludes only fixed first-defect columns and exact temporal period 24.
#include <bits/stdc++.h>
using namespace std;
using u32=unsigned __int128;
struct HashU128 {size_t operator()(u32 x) const {
 uint64_t a=(uint64_t)x,b=(uint64_t)(x>>64);
 uint64_t h=a^(b*0x9e3779b97f4a7c15ULL);h^=h>>30;
 h*=0xbf58476d1ce4e5b9ULL;h^=h>>27;return (size_t)h;
}};
int W[8][48],B[8][11];int gam[24]={1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0};
int x0=117;
int cell(int t,int x){return x<11? B[t%8][x]:W[t%8][((x-11)%48+48)%48];}
int asc(int t,int x){for(int d=1;d<96;d++){int v=cell(t,x-d);if(v!=9)return v>=10;} abort();}
int desc(int t,int x){for(int d=1;d<96;d++){int v=cell(t,x+d);if(v!=9)return v>=10;}abort();}
int carry(int v,int c){return v+c>=10;}
struct State{int a[24]{},g[24]{},dd[24]{};};
u32 enc(const State&s){u32 r=0;int k=0;for(int t=0;t<24;t++)r |=u32(s.a[t])<<k++;
 for(int t=0;t<24;t++)r|=u32(s.g[t])<<k++;
 for(int t=0;t<24;t++)if(gam[t]){r|=u32(s.dd[t])<<k;k+=4;}
 return r;}
State dec(u32 r){State s;int k=0;for(int t=0;t<24;t++)s.a[t]=(r>>k++)&1;
 for(int t=0;t<24;t++)s.g[t]=(r>>k++)&1;
 for(int t=0;t<24;t++)if(gam[t]){s.dd[t]=(r>>k)&15;k+=4;}
 return s;}
struct Edge{u32 z;array<uint8_t,24> word;};
template<class F> void succ(u32 key,F emit){State s=dec(key),o;array<uint8_t,24> w{};
 for(int v0=0;v0<=18;v0++){
 auto rec=[&](auto&& self,int t,int v)->void{
  if(t==24){if(v==v0)emit(Edge{enc(o),w});return;}
  w[t]=v;
  for(int di=0;di<2;di++){
   if(carry(v,di)!=s.g[t])continue;
   int dv=(v+di)%10,up=(v+s.a[t])%10;
   int next=up+(gam[t]?s.dd[t]:dv);
   if(next>18)continue;
   o.a[t]=carry(v,s.a[t]);o.g[t]=di;o.dd[t]=gam[t]?dv:0;
   self(self,t+1,next);
  }
 };rec(rec,0,v0);
 }
}
vector<u32> initial(){State s;vector<int> free;for(int t=0;t<24;t++){
 s.a[t]=asc(t,x0);int lv=cell(t,x0-1),ld=desc(t,x0-1);
 s.g[t]=ld;s.dd[t]=gam[t]?(lv+ld)%10:0;
 if(gam[t]&&lv!=9)free.push_back(t);
 }
 vector<u32> z;for(int mask=0;mask<(1<<free.size());mask++){
 State p=s;for(int i=0;i<(int)free.size();i++){
 int t=free[i];p.g[t]=mask>>i&1;p.dd[t]=(cell(t,x0-1)+p.g[t])%10;
 }z.push_back(enc(p));
 }return z;
}
struct Node{u32 state;int parent;array<uint8_t,24> word;uint8_t color=0;vector<Edge> edges;size_t next=0;};
int main(int argc,char**argv){if(argc<4){cerr<<"usage data j cap\n";return 2;}
 ifstream f(argv[1]);for(int j=0;j<48;j++)for(int t=0;t<8;t++)f>>W[t%8][j];
 for(int j=0;j<11;j++)for(int t=0;t<8;t++)f>>B[t%8][j];
 x0=11+2*48+atoi(argv[2]);int cap=atoi(argv[3]);
 vector<Node> nodes;nodes.reserve(cap);unordered_map<u32,int,HashU128> ids;ids.reserve(cap*2);
 auto add=[&](u32 z,int parent,array<uint8_t,24> w)->int{
  auto it=ids.find(z);if(it!=ids.end())return it->second;
  if(nodes.size()>=size_t(cap))return -2;
  int id=nodes.size();nodes.push_back({z,parent,w,0,{},0});ids.emplace(z,id);return id;
 };
 array<uint8_t,24> initw{};
 int seedCount=0;
 for(u32 root:initial())succ(root,[&](Edge e){
  bool diff=true;for(int t=0;t<24;t++)if(e.word[t]==cell(t,x0))diff=false;
  if(diff){seedCount++;add(e.z,-1,e.word);}
 });
 cout<<"j="<<argv[2]<<" initial_variants="<<initial().size()<<" first_defect_seeds="<<seedCount<<" unique_states="<<nodes.size()<<"\n"<<flush;
 if(nodes.empty())return 0;
 vector<int> stack;stack.reserve(50000);int calls=0;
 for(int root=0;root<(int)nodes.size();root++){
  if(nodes[root].color)continue;
  nodes[root].color=1;stack.push_back(root);
  while(!stack.empty()){
   int i=stack.back();
   if(nodes[i].edges.empty()&&nodes[i].next==0){
    vector<Edge> es;succ(nodes[i].state,[&](Edge e){es.push_back(e);});
    nodes[i].edges=move(es);
   }
   if(nodes[i].next==nodes[i].edges.size()){
    nodes[i].color=2;nodes[i].edges.clear();stack.pop_back();continue;
   }
   Edge e=nodes[i].edges[nodes[i].next++];calls++;
   int j=add(e.z,i,e.word);
   if(j==-2){cout<<"CAP="<<cap<<" edges="<<calls<<"\n";return 0;}
   if(nodes[j].color==1){
    vector<int> prefix;int p=i;
    while(p!=j && p!=-1){prefix.push_back(p);p=nodes[p].parent;}
    reverse(prefix.begin(),prefix.end());
    cout<<"FOUND reachable spatial cycle: visited="<<nodes.size()<<" edges="<<calls<<" cycle_end="<<j<<" loop_length="<<prefix.size()+1<<"\n";
    for(int q:prefix){cout<<"col"<<q<<" ";for(int v:nodes[q].word)cout<<v<<",";cout<<"\n";}
    cout<<"closing ";for(int v:e.word)cout<<v<<",";cout<<"\n";
    return 0;
   }
   if(nodes[j].color==0){nodes[j].color=1;stack.push_back(j);}
  }
 }
 cout<<"EXHAUSTED visited="<<nodes.size()<<" edges="<<calls<<"\n";
}
