// Exact all-spatial-period g1->g0 physical intermediate-row rigidity for decimal rec2.
// C++17 standard library, no external solver or Lean; PAPER PROOF via finite graph SCC.
#include <algorithm>
#include <array>
#include <cassert>
#include <iostream>
#include <numeric>
#include <stack>
#include <utility>
#include <vector>
using namespace std;
constexpr int BASE=10, N=48, NS=76;
struct S {int p,a,d;};
using Word=array<int,N>;
array<S,NS> states{};
array<vector<int>,NS> next_state{};
int state_id(int p,int a,int d){return (p*2+a)*2+d;}
int local_id(int j,int s,int t){return (j*NS+s)*NS+t;}
void setup(){
 for(int p=0;p<=18;p++)for(int a=0;a<2;a++)for(int d=0;d<2;d++)states[state_id(p,a,d)]={p,a,d};
 int edges=0;
 for(int i=0;i<NS;i++)for(int j=0;j<NS;j++){
  auto x=states[i],y=states[j];
  if(y.a==(x.p+x.a)/BASE && x.d==(y.p+y.d)/BASE){next_state[i].push_back(j);edges++;}
 }
 assert(edges==1444);
}
void carries(const Word& W,Word& a,Word& d){
 int c=0;
 for(int r=0;r<2;r++)for(int x:W)c=(x+c)/BASE;
 for(int i=0;i<N;i++){a[i]=c;c=(W[i]+c)/BASE;}
 c=0;
 for(int r=0;r<2;r++)for(int i=N-1;i>=0;i--)c=(W[i]+c)/BASE;
 for(int i=N-1;i>=0;i--){d[i]=c;c=(W[i]+c)/BASE;}
}
Word step(const Word&W,int g){
 Word a{},d{},Y{};carries(W,a,d);
 for(int j=0;j<N;j++){
  int prev=(j+N-1)%N,prev2=(j+N-2)%N,after=(j+1)%N;
  Y[j]=g?W[j]+W[prev]+a[j]+d[prev]-BASE*(a[after]+d[prev2]):
    2*W[j]+a[j]+d[j]-BASE*(a[after]+d[prev]);
  assert(Y[j]>=0&&Y[j]<=18);
 }
 return Y;
}
int g0_value(const S& t){return (t.p+t.a)%BASE+(t.p+t.d)%BASE;}
int g1_value(const S& s,const S& q){return (q.p+q.a)%BASE+(s.p+s.d)%BASE;}
struct Graph{
 vector<array<int,3>> node;vector<vector<int>> edge,reverse_edge;
 explicit Graph(const Word& target){
  vector<int> index(N*NS*NS,-1);
  array<vector<int>,19> by_z{};
  for(int t=0;t<NS;t++)by_z[g0_value(states[t])].push_back(t);
  for(int j=0;j<N;j++)for(int s=0;s<NS;s++)for(int t:by_z[target[j]]){
   index[local_id(j,s,t)]=node.size();node.push_back({j,s,t});
  }
  edge.resize(node.size());reverse_edge.resize(node.size());
  for(int u=0;u<(int)node.size();u++){
   auto [j,s,t]=node[u];int j2=(j+1)%N;
   for(int ss:next_state[s]){
    int y=g1_value(states[s],states[ss]);
    for(int tt:next_state[t])if(states[tt].p==y && g0_value(states[tt])==target[j2]){
     int v=index[local_id(j2,ss,tt)];assert(v>=0);
     edge[u].push_back(v);reverse_edge[v].push_back(u);
    }
   }
  }
 }
};
vector<vector<int>> cyclic_sccs(const Graph&G){
 int n=G.node.size();vector<char>seen(n);vector<int>order;
 order.reserve(n);
 for(int root=0;root<n;root++)if(!seen[root]){
  vector<pair<int,size_t>>stack{{root,0}};seen[root]=1;
  while(!stack.empty()){
   auto &[u,k]=stack.back();
   if(k<G.edge[u].size()){
    int v=G.edge[u][k++];if(!seen[v]){seen[v]=1;stack.emplace_back(v,0);}
   }else{order.push_back(u);stack.pop_back();}
  }
 }
 fill(seen.begin(),seen.end(),0);vector<vector<int>>cyclic;
 for(auto it=order.rbegin();it!=order.rend();it++)if(!seen[*it]){
  vector<int>part,stack{*it};seen[*it]=1;
  while(!stack.empty()){
   int u=stack.back();stack.pop_back();part.push_back(u);
   for(int v:G.reverse_edge[u])if(!seen[v]){seen[v]=1;stack.push_back(v);}
  }
  if(part.size()>1 || find(G.edge[part[0]].begin(),G.edge[part[0]].end(),part[0])!=G.edge[part[0]].end())cyclic.push_back(move(part));
 }
 return cyclic;
}
int main(){
 setup();
 Word X={4,4,14,1,5,11,7,1,15,12,7,9,9,12,14,4,0,6,5,17,13,9,7,3,13,10,4,13,5,1,9,4,11,6,16,3,7,7,12,4,2,13,2,15,10,10,9,3};
 const Word original=X;
 for(int phase=0;phase<8;phase++){
  int g=phase%2?0:1;
  Word Y=step(X,g);
  if(g==1){
   Word Z=step(Y,0);
   Graph H(Z);auto cyc=cyclic_sccs(H);
   assert(cyc.size()==1);
   int expected=(phase%4==0?282:310);
   assert((int)cyc[0].size()==expected);
   int expected_nodes=(phase%4==0?14592:15276);
   int expected_edges=(phase%4==0?14360:16190);
   assert((int)H.node.size()==expected_nodes);
   int total=0;for(const auto&x:H.edge)total+=x.size();assert(total==expected_edges);
   Word A{},D{};carries(Y,A,D);
   array<int,N> unique_t{};unique_t.fill(-1);
   for(int u:cyc[0]){
    auto [j,s,t]=H.node[u];
    if(unique_t[j]<0)unique_t[j]=t;
    else assert(unique_t[j]==t);
   }
   for(int j=0;j<N;j++)assert(unique_t[j]==state_id(Y[j],A[j],D[j]));
   cout<<"phase="<<phase<<" g1->g0 nodes="<<H.node.size()<<" edges="<<total
       <<" cyclic_sccs="<<cyc.size()<<" cyclic_vertices="<<cyc[0].size()
       <<" intermediate_states_per_position=1/48 PASS\n";
  }
  X=Y;
 }
 assert(X==original);
 cout<<"PAPER PROOF finite graph certificate PASS: any cyclic source of spatial period 48*k, k>=1, returning the pinned two-phase rec2 target has exactly the pinned intermediate physical row\n";
}
