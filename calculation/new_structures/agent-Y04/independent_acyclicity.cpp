// Independent Y04 check: iterative temporal-column DP and iterative DFS for cycles.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <tuple>
#include <unordered_map>
#include <utility>
#include <vector>
using namespace std;
using U=uint64_t;
struct Edge{U dest;int label;};
U pack(int l,int h,int y){return (U(l)<<24)|(U(h)<<16)|U(y);}
vector<Edge> transitions(U state,bool root){
  int l=state>>24,h=(state>>16)&255,y=state&65535;
  vector<Edge> out;
  for(int start=root?1:0;start<=18;++start){
    vector<array<int,4>> states{{start,0,0,0}};
    for(int t=0;t<8;++t){
      vector<array<int,4>> next;
      for(auto w:states)for(int upper=0;upper<=1;++upper){
        int a=w[0],low=(l>>t)&1,high=(h>>t)&1;
        if(a+upper<10*high || a+upper>=10*(high+1))continue;
        int highOutput=(t&1)?(a+upper)%10:((y>>(4*(t/2)))&15);
        next.push_back({(a+low)%10+highOutput,
          w[1]|(((a+low)/10)<<t),w[2]|(upper<<t),
          w[3]|((t&1)?0:(((a+upper)%10)<<(4*(t/2))))});
      }
      states.swap(next);
    }
    for(auto w:states)if(w[0]==start)out.push_back({pack(w[1],w[2],w[3]),start});
  }
  sort(out.begin(),out.end(),[](Edge a,Edge b){return tie(a.dest,a.label)<tie(b.dest,b.label);});
  out.erase(unique(out.begin(),out.end(),[](Edge a,Edge b){return a.dest==b.dest&&a.label==b.label;}),out.end());
  return out;
}
bool hasCycle(const vector<vector<int>>& adj){
  vector<unsigned char> colour(adj.size());
  for(size_t src=0;src<adj.size();++src){
    if(colour[src])continue;
    vector<pair<int,size_t>> stack{{int(src),0}};colour[src]=1;
    while(!stack.empty()){
      auto &top=stack.back();int u=top.first;
      if(top.second==adj[u].size()){
        colour[u]=2;stack.pop_back();continue;
      }
      int v=adj[u][top.second++];
      if(colour[v]==1)return true;
      if(!colour[v]){colour[v]=1;stack.emplace_back(v,0);}
    }
  }
  return false;
}
int main(){
  U root=pack(0,85,0x1111);vector<U> states{root};
  unordered_map<U,int> ids{{root,0}};
  vector<vector<pair<int,int>>> edges;
  for(size_t i=0;i<states.size();++i){
    vector<pair<int,int>> out;
    for(auto e:transitions(states[i],i==0)){
      auto it=ids.find(e.dest);int to;
      if(it==ids.end()){
        to=int(states.size());ids.emplace(e.dest,to);states.push_back(e.dest);
      } else to=it->second;
      out.emplace_back(to,e.label);
    }
    edges.push_back(move(out));
  }
  size_t count=0;for(auto &out:edges)count+=out.size();
  cout<<"INDEPENDENT states="<<states.size()<<" edges="<<count<<'\n';
  if(states.size()!=244785||count!=263584)throw runtime_error("bad independent graph");
  for(int charge:{0,3,6}){
    vector<vector<int>> adj(edges.size());long long count=0;
    for(size_t q=0;q<edges.size();++q)
      for(auto [mid,a]:edges[q])for(auto [end,b]:edges[mid])
        if((a+b)%9==charge){adj[q].push_back(end);++count;}
    bool cycle=hasCycle(adj);
    cout<<"INDEPENDENT EVEN residue="<<charge<<" macro_edges="<<count<<" cycle="<<cycle<<'\n';
    if(cycle)throw runtime_error("cycle in even subgraph");
  }
  unordered_map<U,int> augIndex;vector<pair<int,int>> augmented;
  for(auto &row:edges)for(auto [to,a]:row)if(a%2==0){
    U k=U(to)*19+a;
    if(!augIndex.count(k)){
      augIndex.emplace(k,int(augmented.size()));augmented.push_back({to,a});
    }
  }
  cout<<"INDEPENDENT odd_states="<<augmented.size()<<'\n';
  for(int charge:{0,3,6}){
    vector<vector<int>> adj(augmented.size());long long count=0;
    for(size_t i=0;i<augmented.size();++i){
      auto [q,previous]=augmented[i];
      for(auto [mid,a]:edges[q])for(auto [end,b]:edges[mid])
        if(b%2==0 && (previous+2*a+b)%18==2*charge){
          adj[i].push_back(augIndex.at(U(end)*19+b));++count;
        }
    }
    bool cycle=hasCycle(adj);
    cout<<"INDEPENDENT ODD residue="<<charge<<" macro_edges="<<count<<" cycle="<<cycle<<'\n';
    if(cycle)throw runtime_error("cycle in odd subgraph");
  }
  cout<<"INDEPENDENT COMPLETE GRAPH AND ALL-RESIDUE ACYCLICITY PASS\n";
}
