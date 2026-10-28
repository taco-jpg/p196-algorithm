// Agent-2: exact period-sixteen stationary first-defect spatial transfer (rec2).
// Input: 48 cycle rows + 11 exterior rows, each with 8 time phases.
// A candidate begins at the first off-lattice column in every time phase.
// Subsequent columns are unrestricted. An infinite right continuation must
// eventually cycle in the finite directed link-state graph.
// This is NOT a centre certificate, nor a test of periods 16,24,... .
#include <bits/stdc++.h>
using namespace std;
using U = uint64_t;
int W[8][48],B[8][11],g[16]={1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0},X=117;
int cell(int t,int x){return x<11?B[t%8][x]:W[t%8][((x-11)%48+48)%48];}
int ac(int t,int x){for(int k=1;k<=96;k++){int v=cell(t,x-k);if(v!=9)return v>=10;}abort();}
int dc(int t,int x){for(int k=1;k<=96;k++){int v=cell(t,x+k);if(v!=9)return v>=10;}abort();}
struct S{int a[16]{},d[16]{},z[16]{};};
U pack(const S&s){U q=0;int k=0;
 for(int t=0;t<16;t++)q|=U(s.a[t])<<k++;
 for(int t=0;t<16;t++)q|=U(s.d[t])<<k++;
 for(int t=0;t<16;t++)if(g[t]){q|=U(s.z[t])<<k;k+=4;}
 return q;}
S unpack(U q){S s;int k=0;
 for(int t=0;t<16;t++)s.a[t]=(q>>k++)&1;
 for(int t=0;t<16;t++)s.d[t]=(q>>k++)&1;
 for(int t=0;t<16;t++)if(g[t]){s.z[t]=(q>>k)&15;k+=4;}
 return s;}
struct Edge{U q;array<uint8_t,16>w;};
template<class F>void next(U q,F emit){
 S s=unpack(q),o;array<uint8_t,16>w{};
 for(int v0=0;v0<=18;v0++){
  auto rec=[&](auto&&self,int t,int v)->void{
   if(t==16){if(v==v0)emit(Edge{pack(o),w});return;}
   w[t]=v;
   for(int din=0;din<2;din++){
    if((v+din>=10)!=s.d[t])continue;
    int up=(v+s.a[t])%10,low=(v+din)%10;
    int v2=up+(g[t]?s.z[t]:low);
    if(v2>18)continue;
    o.a[t]=(v+s.a[t]>=10);o.d[t]=din;o.z[t]=g[t]?low:0;
    self(self,t+1,v2);
   }
  };rec(rec,0,v0);
 }
}
vector<U> starts(){
 S s;vector<int>free;
 for(int t=0;t<16;t++){
  s.a[t]=ac(t,X);int v=cell(t,X-1),d=dc(t,X-1);
  s.d[t]=d;s.z[t]=g[t]?(v+d)%10:0;
  if(g[t]&&v!=9)free.push_back(t);
 }
 vector<U>ans;
 for(int mask=0;mask<(1<<free.size());mask++){
  S a=s;
  for(int i=0;i<(int)free.size();i++){
   int t=free[i];a.d[t]=(mask>>i)&1;
   a.z[t]=(cell(t,X-1)+a.d[t])%10;
  }
  ans.push_back(pack(a));
 }
 return ans;
}
struct Node{U q;int parent;array<uint8_t,16>w;uint8_t color=0;vector<Edge>es;size_t pos=0;};
int main(int argc,char**argv){
 if(argc!=4){cerr<<"usage: rec2_t8_transfer rec2_t8_rows.txt j cap\n";return 2;}
 ifstream f(argv[1]);if(!f)return 2;
 for(int j=0;j<48;j++)for(int t=0;t<8;t++)if(!(f>>W[t][j]))return 2;
 for(int j=0;j<11;j++)for(int t=0;t<8;t++)if(!(f>>B[t][j]))return 2;
 int j=stoi(argv[2]);if(j<0||j>=48)return 2;
 X=11+96+j;size_t cap=stoull(argv[3]);
 vector<Node>nodes;nodes.reserve(min(cap,size_t(2000000)));
 unordered_map<U,int>ids;ids.reserve(min(cap*2,size_t(4000000)));
 auto add=[&](U q,int par,array<uint8_t,16>w)->int{
  auto it=ids.find(q);if(it!=ids.end())return it->second;
  if(nodes.size()>=cap)return -2;
  int i=nodes.size();nodes.push_back({q,par,w,0,{},0});ids.emplace(q,i);return i;
 };
 int nseed=0;
 for(U root:starts())next(root,[&](Edge e){
  bool diff=true;
  for(int t=0;t<16;t++)if(e.w[t]==cell(t,X))diff=false;
  if(diff){++nseed;add(e.q,-1,e.w);}
 });
 cout<<"j="<<j<<" initial_variants="<<starts().size()
     <<" first_defect_seeds="<<nseed<<" unique_states="<<nodes.size()<<"\n";
 vector<int>stack;
 for(int root=0;root<(int)nodes.size();root++){
  if(nodes[root].color)continue;
  nodes[root].color=1;stack.push_back(root);
  while(!stack.empty()){
   int i=stack.back();
   if(nodes[i].es.empty()&&nodes[i].pos==0){
    vector<Edge>e;next(nodes[i].q,[&](Edge x){e.push_back(x);});
    nodes[i].es=move(e);
   }
   if(nodes[i].pos==nodes[i].es.size()){
    nodes[i].color=2;nodes[i].es.clear();stack.pop_back();continue;
   }
   Edge e=nodes[i].es[nodes[i].pos++];
   int to=add(e.q,i,e.w);
   if(to==-2){cout<<"CAP="<<cap<<"\n";return 1;}
   if(nodes[to].color==1){cout<<"FOUND spatial cycle\n";return 1;}
   if(!nodes[to].color){nodes[to].color=1;stack.push_back(to);}
  }
 }
 // Edge counts are deduplicated in the independent tuple-state Python checker.
 cout<<"EXHAUSTED visited="<<nodes.size()<<"\n";
 return 0;
}
