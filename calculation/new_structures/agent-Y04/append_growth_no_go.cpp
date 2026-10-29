// Y04: exhaustive all-width obstruction to append-only p8 centre renewal.
// Rooted periodic carry graph; all 2-column charge-compatible subgraphs are DAGs.
#include <algorithm>
#include <cstdint>
#include <deque>
#include <functional>
#include <iostream>
#include <stdexcept>
#include <unordered_map>
#include <vector>
using namespace std;
struct State {int l,h,y;};
struct Edge {int to,a;};
struct Vertex {State state; vector<Edge> out;};
uint64_t key(State s) {return (uint64_t(s.l)<<24)|(uint64_t(s.h)<<16)|s.y;}
int main() {
  vector<Vertex> graph{{{0,85,0x1111},{}}};
  unordered_map<uint64_t,int> index{{key(graph[0].state),0}};
  index.reserve(500000);
  for (size_t i=0;i<graph.size();++i) {
    State q=graph[i].state;
    auto build=[&](auto&& self,int t,int a,int a0,int nl,int nh,int ny)->void {
      if(t==8) {
        if(a!=a0) return;
        State nxt{nl,nh,ny};
        auto found=index.find(key(nxt));int j;
        if(found==index.end()) {
          j=int(graph.size());index.emplace(key(nxt),j);
          graph.push_back({nxt,{}});
        } else j=found->second;
        for(auto edge:graph[i].out)if(edge.to==j && edge.a==a0)return;
        graph[i].out.push_back({j,a0});return;
      }
      for(int upper=0;upper<=1;++upper) {
        if((a+upper)/10 != ((q.h>>t)&1)) continue;
        int low=(q.l>>t)&1;
        int right=(t%2)?(a+upper)%10:(q.y>>(4*(t/2)))&15;
        int next=(a+low)%10+right;
        self(self,t+1,next,a0,
             nl|(((a+low)/10)<<t),nh|(upper<<t),
             ny|(t%2?0:(((a+upper)%10)<<(4*(t/2)))));
      }
    };
    for(int a0=(i==0?1:0);a0<=18;++a0)build(build,0,a0,a0,0,0,0);
  }
  size_t raw=0;for(auto &v:graph)raw+=v.out.size();
  cout<<"ROOTED states="<<graph.size()<<" edges="<<raw<<'\n';
  if(graph.size()!=244785||raw!=263584)throw runtime_error("root graph count differs");
  auto dag=[&](const vector<vector<int>>& arcs)->bool {
    vector<int> indegree(arcs.size());
    for(auto &out:arcs)for(int v:out)++indegree[v];
    deque<int> ready;for(int i=0;i<int(arcs.size());++i)if(!indegree[i])ready.push_back(i);
    int removed=0;
    while(!ready.empty()) {
      int u=ready.front();ready.pop_front();++removed;
      for(int v:arcs[u])if(!--indegree[v])ready.push_back(v);
    }
    return removed==int(arcs.size());
  };
  for(int charge:{0,3,6}) {
    vector<vector<int>> macro(graph.size());long long total=0;
    for(size_t i=0;i<graph.size();++i)
      for(auto first:graph[i].out)for(auto second:graph[first.to].out)
        if((first.a+second.a)%9==charge) {
          macro[i].push_back(second.to);++total;
        }
    bool acyclic=dag(macro);
    cout<<"EVEN residue="<<charge<<" macro_edges="<<total<<" acyclic="<<acyclic<<'\n';
    if(!acyclic)throw runtime_error("even-centre potential charge cycle");
  }
  // The odd centre is a single digit: its pair coefficient is even and
  // contributes half its value to the ordinary digit sum.
  unordered_map<uint64_t,int> prevIndex;
  vector<pair<int,int>> prevNodes;
  for(auto &vertex:graph)for(auto e:vertex.out)if(e.a%2==0) {
    uint64_t k=uint64_t(e.to)*19+e.a;
    if(!prevIndex.count(k)) {
      int j=int(prevNodes.size());prevIndex.emplace(k,j);
      prevNodes.push_back({e.to,e.a});
    }
  }
  cout<<"ODD augmented_states="<<prevNodes.size()<<'\n';
  for(int charge:{0,3,6}) {
    vector<vector<int>> macro(prevNodes.size());long long total=0;
    for(size_t i=0;i<prevNodes.size();++i) {
      auto [q,previous]=prevNodes[i];
      for(auto first:graph[q].out)for(auto second:graph[first.to].out) {
        if(second.a%2 || (previous+2*first.a+second.a)%18!=2*charge)continue;
        macro[i].push_back(prevIndex.at(uint64_t(second.to)*19+second.a));++total;
      }
    }
    bool acyclic=dag(macro);
    cout<<"ODD residue="<<charge<<" macro_edges="<<total<<" acyclic="<<acyclic<<'\n';
    if(!acyclic)throw runtime_error("odd-centre potential charge cycle");
  }
  cout<<"ALL ROOTED p8 APPEND-ONLY EIGHT-STEP RENEWALS EXCLUDED (BOTH PARITIES)\n";
}
