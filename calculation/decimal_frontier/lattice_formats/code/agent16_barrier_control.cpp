// Exact reachable position automaton for a fixed base and overflow word.
// Derived directly from bauto3's first-coordinate recurrence. No SCC cutoff.
// Compile: c++ -O3 -std=c++17 -o /tmp/a16_graph agent16_root_graph.cpp
#include <bits/stdc++.h>
using namespace std;
struct State {
  vector<int> L,H,Y;
  bool operator<(State const& o) const {return tie(L,H,Y)<tie(o.L,o.H,o.Y);}
};
struct Node {State s; int depth;};
int main(int argc,char**argv){
  if(argc<3){cerr<<"usage: graph BASE G [--dump]\n";return 2;}
  int b=stoi(argv[1]); string gs=argv[2]; int p=gs.size();
  if(b<2 || p<1 || p>30) return 2;
  bool dump=argc>3 && string(argv[3])=="--dump";
  vector<int> g(p),gi;
  for(int t=0;t<p;t++){if(gs[t]!='0' && gs[t]!='1')return 2;
    g[t]=gs[t]-'0';if(g[t])gi.push_back(t);}
  State root; root.L.assign(p,0);root.H=g;root.Y.assign(gi.size(),1);
  map<State,int> ids;vector<Node> nodes;vector<vector<int>> edges;
  auto add=[&](State const&s,int depth)->int{
    auto it=ids.find(s);if(it!=ids.end())return it->second;
    int k=nodes.size();ids.emplace(s,k);nodes.push_back({s,depth});edges.emplace_back();return k;
  };
  add(root,0);long long generated=0;
  for(size_t i=0;i<nodes.size();i++){
    State st=nodes[i].s; vector<int> y(p),xs(p),cs(p);
    for(size_t j=0;j<gi.size();j++)y[gi[j]]=st.Y[j];
    set<int> out;
    for(int x0=(i==0?1:0);x0<=2*b-2;x0++){
      auto rec=[&](auto&&self,int t,int x)->void{
        if(t==p){
          if(x!=x0)return;
          State z;z.L.resize(p);z.H=cs;z.Y.resize(gi.size());
          for(int k=0;k<p;k++)z.L[k]=(xs[k]+st.L[k])/b;
          for(size_t j=0;j<gi.size();j++){
            int k=gi[j];z.Y[j]=(xs[k]+cs[k])%b;
          }
          int v=add(z,nodes[i].depth+1);out.insert(v);generated++;return;
        }
        if(x<0 || x>2*b-2)return;
        for(int c=0;c<2;c++){
          if((x+c)/b!=st.H[t])continue;
          xs[t]=x;cs[t]=c;
          int next=(x+st.L[t])%b+(g[t]?y[t]:(x+c)%b);
          self(self,t+1,next);
        }
      };
      rec(rec,0,x0);
    }
    edges[i].assign(out.begin(),out.end());
    if(i%100000==0 && i)cerr<<"visited="<<i<<" states="<<nodes.size()<<"\n";
  }
  int N=nodes.size();long long E=0;int maxdepth=0;
  vector<vector<int>> rev(N);
  for(int i=0;i<N;i++){
    maxdepth=max(maxdepth,nodes[i].depth);
    for(int j:edges[i]){E++;rev[j].push_back(i);}
  }
  // Nonrecursive Kosaraju for exact SCCs.
  vector<char> seen(N);vector<int> order;order.reserve(N);
  for(int v=0;v<N;v++){
    if(seen[v])continue;
    vector<pair<int,int>> stk{{v,0}};seen[v]=1;
    while(!stk.empty()){
      auto &q=stk.back();int w=q.first;
      if(q.second==(int)edges[w].size()){
        order.push_back(w);stk.pop_back();continue;
      }
      int u=edges[w][q.second++];
      if(!seen[u]){seen[u]=1;stk.emplace_back(u,0);}
    }
  }
  vector<int> comp(N,-1);vector<vector<int>> components;
  for(int oi=N-1;oi>=0;oi--){int v=order[oi];if(comp[v]>=0)continue;
    int id=components.size();components.emplace_back();vector<int> stack{v};comp[v]=id;
    while(!stack.empty()){
      int u=stack.back();stack.pop_back();components.back().push_back(u);
      for(int w:rev[u])if(comp[w]<0){comp[w]=id;stack.push_back(w);}
    }
  }
  vector<pair<int,int>> cycles; // (min depth, SCC size)
  for(auto const&c:components){
    bool loop=c.size()>1;
    if(!loop)for(int w:edges[c[0]])if(w==c[0])loop=true;
    if(loop){int depth=INT_MAX;for(int u:c)depth=min(depth,nodes[u].depth);
      cycles.emplace_back(depth,c.size());}
  }
  sort(cycles.begin(),cycles.end());
  cout<<"G base="<<b<<" g="<<gs<<" states="<<N<<" edges="<<E
      <<" nontrivial_sccs="<<cycles.size()<<" maxdepth="<<maxdepth
      <<" generated="<<generated<<"\n";
  for(auto [depth,size]:cycles)cout<<"SCC depth="<<depth<<" size="<<size<<"\n";
  if(dump)for(int i=0;i<N;i++){
    auto const&s=nodes[i].s;cout<<"V "<<i<<" ";
    for(int x:s.L)cout<<x;cout<<" ";for(int x:s.H)cout<<x;
    cout<<" ";for(size_t j=0;j<s.Y.size();j++){if(j)cout<<",";cout<<s.Y[j];}
    cout<<" ->";for(int j:edges[i])cout<<" "<<j;cout<<"\n";
  }
}
