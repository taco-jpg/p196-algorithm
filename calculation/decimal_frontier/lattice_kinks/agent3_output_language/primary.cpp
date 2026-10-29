// All-window physical carry output-language theorem, decimal rec2 g0/g1.
// C++17 standard library; no Lean or finite-horizon Lychrel claim.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <queue>
#include <string>
#include <vector>
using namespace std;
constexpr int B=10, NS=76, NE=1444, NH=5776, N=48;
struct S {int p,a,d;};
struct E {int u,v,y;};
struct Graph {
 int g;array<S,NS> s{};vector<E> e;array<vector<int>,NS> gin,grev,outs;
 array<vector<int>,NH> h,hr;array<int,NS> gl{};array<int,NH> hl{};
 explicit Graph(int gamma):g(gamma){
  for(int p=0;p<19;p++)for(int a=0;a<2;a++)for(int d=0;d<2;d++){
   int i=(p*2+a)*2+d;s[i]={p,a,d};gl[i]=(p&1)|(a<<1)|(d<<2);
  }
  for(int i=0;i<NS;i++){
   auto x=s[i];for(int q=0;q<19;q++)for(int D=0;D<2;D++)if(x.d==(q+D)/B){
    int j=(q*2+(x.p+x.a)/B)*2+D;auto z=s[j];
    int y=g?z.p+x.p+z.a+x.d-B*((z.p+z.a)/B+(x.p+x.d)/B):
       2*z.p+z.a+z.d-B*((z.p+z.a)/B+(z.p+z.d)/B);
    assert(y>=0&&y<=18);int id=e.size();e.push_back({i,j,y});outs[i].push_back(id);
    gin[i].push_back(j);grev[j].push_back(i);
   }
  }
  assert(e.size()==NE);
  for(int i=0;i<NE;i++)for(int a=0;a<2;a++)for(int d=0;d<2;d++){
   int u=4*i+2*a+d;hl[u]=(e[i].y&1)|(a<<1)|(d<<2);
  }
  for(int i=0;i<NE;i++)for(int a=0;a<2;a++)for(int d=0;d<2;d++){
   int u=4*i+2*a+d;
   for(int j:outs[e[i].v])for(int D=0;D<2;D++)if(d==(e[j].y+D)/B){
    int A=(e[i].y+a)/B,v=4*j+2*A+D;
    h[u].push_back(v);hr[v].push_back(u);
   }
  }
  int cnt=0;for(const auto&v:h)cnt+=v.size();assert(cnt==109744);
 }
};
vector<int> bfs(int root,const array<vector<int>,NH>& adj){
 vector<int> parent(NH,-1);queue<int>q;q.push(root);parent[root]=root;
 while(!q.empty()){int u=q.front();q.pop();for(int v:adj[u])if(parent[v]<0){parent[v]=u;q.push(v);}}
 return parent;
}
int relation_index(int s,int h){return s*NH+h;}
void carries(const vector<int>&P,vector<int>&a,vector<int>&d){
 int n=P.size(),t=0;a.resize(n);d.resize(n);
 for(int i=0;i<n;i++)t=(P[i]+t)/B;
 for(int i=0;i<n;i++){a[i]=t;t=(P[i]+t)/B;}
 t=0;for(int i=n-1;i>=0;i--)t=(P[i]+t)/B;
 for(int i=n-1;i>=0;i--){d[i]=t;t=(P[i]+t)/B;}
}
vector<int> labels_of(const vector<int>&P){
 vector<int>a,d;carries(P,a,d);vector<int>v(P.size());
 for(int i=0;i<(int)P.size();i++)v[i]=(P[i]&1)|(a[i]<<1)|(d[i]<<2);
 return v;
}
vector<int> cyclic_image(const vector<int>&P,int g){
 vector<int>a,d;carries(P,a,d);int n=P.size();vector<int>Y(n);
 for(int i=0;i<n;i++){
  int im=(i+n-1)%n,imm=(i+n-2)%n,ip=(i+1)%n;
  Y[i]=g?P[i]+P[im]+a[i]+d[im]-B*(a[ip]+d[imm]):
     2*P[i]+a[i]+d[i]-B*(a[ip]+d[im]);
  assert(Y[i]>=0&&Y[i]<=18);
 }
 return Y;
}
vector<int> build_g0_witness(const Graph&G,const vector<uint8_t>&R,const vector<int>&tohub,const vector<int>&fromhub){
 vector<int>target(N);for(int j=0;j<N;j++)target[j]=j%2?11:1;
 auto lab=labels_of(target);for(int j=0;j<N;j++)assert(lab[j]==(j%2?1:7));
 vector<int>a,d;carries(target,a,d);vector<int>src;
 for(int j=0;j<11;j++)src.push_back((target[j]*2+a[j])*2+d[j]);
 int first=-1;for(int h=0;h<NH;h++)if(R[relation_index(src[0],h)]){first=h;break;}
 assert(first>=0);vector<int>ring{first};
 for(int j=1;j<11;j++){
  int found=-1;for(int h:G.h[ring.back()])if(R[relation_index(src[j],h)]){found=h;break;}
  assert(found>=0);ring.push_back(found);
 }
 int u=ring.back();while(u!=1563){u=tohub[u];assert(u>=0);ring.push_back(u);}
 int hubpos=ring.size()-1;
 vector<int>reverse_path;u=first;while(u!=1563){reverse_path.push_back(u);u=fromhub[u];assert(u>=0);}
 reverse(reverse_path.begin(),reverse_path.end());
 if(!reverse_path.empty())reverse_path.pop_back();
 ring.insert(ring.end(),reverse_path.begin(),reverse_path.end());
 int pad=(N-(int(ring.size())%N))%N;
 ring.insert(ring.begin()+hubpos+1,pad,1563);
 assert(ring.size()%N==0);
 for(int j=0;j<(int)ring.size();j++){
  auto&v=G.h[ring[j]];assert(find(v.begin(),v.end(),ring[(j+1)%ring.size()])!=v.end());
 }
 vector<int>P;for(int h:ring)P.push_back(G.s[G.e[h/4].v].p);
 auto Y=cyclic_image(P,0);auto labY=labels_of(Y);
 for(int j=0;j<11;j++)assert(labY[j]==(j%2?1:7));
 for(int j=0;j<(int)P.size();j++){
  assert(Y[j]==G.e[ring[j]/4].y);
  assert(labY[j]==G.hl[ring[j]]);
 }
 cout<<"g0 physical cyclic witness length="<<P.size()<<" alternating 11-mask prefix PASS\n";
 return P;
}

vector<int> build_g1_sharp_witness(const Graph&G){
 const int hub=0;auto fromhub=bfs(hub,G.h),tohub=bfs(hub,G.hr);
 vector<uint8_t>good(NH);for(int h=0;h<NH;h++)good[h]=fromhub[h]>=0&&tohub[h]>=0;
 vector<vector<int>>cur(NH);
 for(int h=0;h<NH;h++)if(good[h]&&G.hl[h]==7)cur[h]={h};
 for(int k=1;k<10;k++){
  int symbol=k%2?1:7;vector<vector<int>>nxt(NH);
  for(int u=0;u<NH;u++)if(!cur[u].empty())for(int v:G.h[u])
   if(good[v]&&G.hl[v]==symbol&&nxt[v].empty()){
    nxt[v]=cur[u];nxt[v].push_back(v);
   }
  cur.swap(nxt);
 }
 auto distance=[&](int x,const vector<int>&par){int n=0;while(x!=hub){assert(par[x]>=0);x=par[x];n++;}return n;};
 int end=-1,best=INT32_MAX;
 for(int h=0;h<NH;h++)if(!cur[h].empty()){
  int cost=distance(h,tohub)+distance(cur[h][0],fromhub);
  if(cost<best){best=cost;end=h;}
 }
 assert(end>=0);vector<int>ring=cur[end];
 int u=end;while(u!=hub){u=tohub[u];ring.push_back(u);}
 int hubpos=ring.size()-1;
 vector<int>reverse_path;u=cur[end][0];while(u!=hub){reverse_path.push_back(u);u=fromhub[u];}
 reverse(reverse_path.begin(),reverse_path.end());
 if(!reverse_path.empty())reverse_path.pop_back();
 ring.insert(ring.end(),reverse_path.begin(),reverse_path.end());
 int pad=(N-(int(ring.size())%N))%N;
 ring.insert(ring.begin()+hubpos+1,pad,hub);
 assert(ring.size()%N==0);
 for(int i=0;i<(int)ring.size();i++){
  auto&v=G.h[ring[i]];assert(find(v.begin(),v.end(),ring[(i+1)%ring.size()])!=v.end());
 }
 vector<int>P;for(int h:ring)P.push_back(G.s[G.e[h/4].v].p);
 auto Y=cyclic_image(P,1);auto labels=labels_of(Y);
 for(int i=0;i<10;i++)assert(labels[i]==(i%2?1:7));
 for(int i=0;i<(int)ring.size();i++){
  assert(Y[i]==G.e[ring[i]/4].y&&labels[i]==G.hl[ring[i]]);
 }
 cout<<"g1 physical cyclic sharpness witness length="<<P.size()<<" alternating 10-mask prefix PASS\n";
 return P;
}

int main(int argc,char**argv){
 assert(argc==2);Graph A(0),B1(1);int hub=1563;
 auto f=bfs(hub,A.h),r=bfs(hub,A.hr);
 vector<uint8_t> good(NH);int goodcnt=0;
 for(int i=0;i<NH;i++){good[i]=f[i]>=0&&r[i]>=0;goodcnt+=good[i];}
 assert(goodcnt==3116&&find(A.h[hub].begin(),A.h[hub].end(),hub)!=A.h[hub].end());
 vector<uint8_t> R0(NS*NH),R1(NS*NH);int n0=0,n1=0;
 for(int i=0;i<NS;i++)for(int h=0;h<NH;h++)if(good[h]&&A.gl[i]==A.hl[h]){R0[relation_index(i,h)]=1;n0++;}
 for(int i=0;i<NS;i++)for(int h=0;h<NH;h++)if(R0[relation_index(i,h)]){
  bool ok=true;
  for(int j:A.gin[i]){
   bool found=false;for(int v:A.h[h])if(R0[relation_index(j,v)]){found=true;break;}
   if(!found){ok=false;break;}
  }
  if(ok){R1[relation_index(i,h)]=1;n1++;}
 }
 assert(n0==29600&&n1==14924);
 int covered=0;
 for(int i=0;i<NS;i++){
  bool any=false;
  for(int h=0;h<NH;h++)if(R1[relation_index(i,h)]){
   any=true;
   for(int j:A.gin[i]){
    bool lift=false;for(int v:A.h[h])if(R1[relation_index(j,v)]){lift=true;break;}
    assert(lift);
   }
  }
  covered+=any;
 }
 assert(covered==76);
 cout<<"PAPER PROOF certificate: g0 recurrent SCC=3116; R0=29600 R1=14924; all 76 target states covered and every target edge lifts\n";
 const int pattern[11]={7,1,7,1,7,1,7,1,7,1,7};
 const int expected[11]={722,191,133,99,81,79,71,57,36,10,0};
 vector<uint8_t> cur(NH),nxt(NH);
 for(int k=0;k<11;k++){
  fill(nxt.begin(),nxt.end(),0);
  if(k==0){for(int h=0;h<NH;h++)if(B1.hl[h]==pattern[0])nxt[h]=1;}
  else for(int h=0;h<NH;h++)if(cur[h])for(int v:B1.h[h])if(B1.hl[v]==pattern[k])nxt[v]=1;
  int cnt=accumulate(nxt.begin(),nxt.end(),0);assert(cnt==expected[k]);
  cur.swap(nxt);
 }
 cout<<"PAPER PROOF certificate: g1 alternating (7,1)^5,7 is impossible (length10 has 10 states; length11 has 0)\n";
 auto P=build_g0_witness(A,R1,r,f);auto Y=cyclic_image(P,0);
 auto P1=build_g1_sharp_witness(B1),Y1=cyclic_image(P1,1);
 ofstream o(argv[1]);assert(o.good());o<<P.size()<<"\n";
 for(int i=0;i<(int)P.size();i++)o<<P[i]<<(i+1==(int)P.size()?'\n':' ');
 for(int i=0;i<(int)Y.size();i++)o<<Y[i]<<(i+1==(int)Y.size()?'\n':' ');
 o<<P1.size()<<"\n";
 for(int i=0;i<(int)P1.size();i++)o<<P1[i]<<(i+1==(int)P1.size()?'\n':' ');
 for(int i=0;i<(int)Y1.size();i++)o<<Y1[i]<<(i+1==(int)Y1.size()?'\n':' ');
 o.close();cout<<"PASS all-window g0 lifting, g1 forbidden block and both physical witnesses\n";
}
