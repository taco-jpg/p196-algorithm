// Independent T=24 quotient transfer; Kahn acyclicity checker.
// Duplicate period-eight boundary and lattice 3 times; quotient by time shift of 8.
// Unlike the DFS implementation, this builds ALL reachable edges and peels indegrees.
#include <cstdint>
#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <unordered_map>
#include <unordered_set>
#include <deque>
#include <functional>
#include <algorithm>
using U=unsigned __int128;
struct H { size_t operator()(U q) const noexcept {uint64_t x=(uint64_t)q,y=q>>64;return (x ^ (y*0x9e3779b97f4a7c15ULL)) * 0xbf58476d1ce4e5b9ULL;}};
constexpr int T=24, P=8,M=48,N=11;
int W[P][M],B[P][N];
int V(int t,int x){t%=P;return x<N?B[t][x]:W[t][((x-N)%M+M)%M];}
int CA(int t,int x){for(int z=1;z<97;z++)if(V(t,x-z)!=9)return V(t,x-z)>=10;std::abort();}
int CD(int t,int x){for(int z=1;z<97;z++)if(V(t,x+z)!=9)return V(t,x+z)>=10;std::abort();}
struct Q{uint8_t a[T]{},d[T]{},h[T]{};};
U pack(const Q&v){U r=0;for(int t=0;t<T;t++){r|=U(v.a[t])<<t;r|=U(v.d[t])<<(24+t);if(t%2==0)r|=U(v.h[t])<<(48+4*(t/2));}return r;}
Q unpack(U v){Q q;for(int t=0;t<T;t++){q.a[t]=(v>>t)&1;q.d[t]=(v>>(24+t))&1;if(t%2==0)q.h[t]=(v>>(48+4*(t/2)))&15;}return q;}
U rotation(U v){const uint64_t m24=(1ULL<<24)-1,m48=(1ULL<<48)-1;uint64_t a=uint64_t(v)&m24,d=uint64_t(v>>24)&m24,h=uint64_t(v>>48)&m48;a=(a>>8)|((a&255)<<16);d=(d>>8)|((d&255)<<16);h=(h>>16)|((h&65535)<<32);return U(a)|(U(d)<<24)|(U(h)<<48);}
U canon(U v){U r=rotation(v),s=rotation(r);return std::min(v,std::min(r,s));}
// Independent local recurrence, enumerate temporal return via recursion in time.
template<class F> void advance(U key,F emit){Q in=unpack(key),out;uint8_t w[T]{};
 for(int seed=0;seed<=18;seed++){
  auto rec=[&](auto&& self,int t,int v)->void{
   if(t==T){if(v==seed)emit(canon(pack(out)),w);return;}
   w[t]=v;
   for(int delta=0;delta<2;delta++){
    if(((v+delta)>=10)!=in.d[t])continue;
    int dn=(v+delta)%10,up=(v+in.a[t])%10;
    int next=up+(t%2==0?in.h[t]:dn);
    if(next>18)continue;
    out.a[t]=(v+in.a[t])>=10;out.d[t]=delta;out.h[t]=(t%2==0?dn:0);
    self(self,t+1,next);
   }
  };rec(rec,0,seed);
 }
}
int main(int argc,char **argv){if(argc!=4){std::cerr<<"usage: rec2_t24_kahn rows j cap\n";return 2;}
 std::ifstream in(argv[1]);if(!in)return 2;
 for(int j=0;j<M;j++)for(int t=0;t<P;t++)if(!(in>>W[t][j]))return 2;
 for(int j=0;j<N;j++)for(int t=0;t<P;t++)if(!(in>>B[t][j]))return 2;
 int j=std::stoi(argv[2]);int x=107+j;size_t cap=std::stoull(argv[3]);if(j<0||j>=M)return 2;
 Q boundary;std::vector<int> free;
 for(int t=0;t<T;t++){boundary.a[t]=CA(t,x);int left=V(t,x-1),down=CD(t,x-1);boundary.d[t]=down;boundary.h[t]=(t%2==0)?(left+down)%10:0;if(t%2==0 && left!=9)free.push_back(t);}
 struct N{U key;uint32_t degree=0;};
 std::vector<N> nodes;nodes.reserve(std::min(cap,(size_t)1200000));
 std::unordered_map<U,uint32_t,H> where;where.reserve(std::min(cap*2,(size_t)2400000));
 std::vector<uint32_t> rowPtr,cols;rowPtr.reserve(std::min(cap,(size_t)1200000));
 auto insert=[&](U key)->std::pair<uint32_t,bool>{auto it=where.find(key);if(it!=where.end())return {it->second,false};if(nodes.size()>=cap)throw std::runtime_error("CAP");uint32_t id=nodes.size();where.emplace(key,id);nodes.push_back({key,0});return {id,true};};
 uint64_t rootCandidates=0;std::vector<uint32_t> roots;
 for(int mask=0;mask<(1<<free.size());mask++){
  Q v=boundary;
  for(size_t k=0;k<free.size();k++){int t=free[k];v.d[t]=(mask>>k)&1;v.h[t]=(V(t,x-1)+v.d[t])%10;}
  advance(pack(v),[&](U nxt,const uint8_t*word){
    for(int t=0;t<T;t++)if(word[t]==V(t,x))return;
    rootCandidates++;
    auto [id,novel]=insert(nxt);if(novel)roots.push_back(id);
  });
 }
 const size_t initial=nodes.size();
 // BFS, all unique edges, and write adjacency to CSR arrays.
 for(size_t i=0;i<nodes.size();i++){
  rowPtr.push_back(cols.size());
  std::vector<U> outgoing;
  advance(nodes[i].key,[&](U tgt,const uint8_t*){outgoing.push_back(tgt);});
  std::sort(outgoing.begin(),outgoing.end());outgoing.erase(std::unique(outgoing.begin(),outgoing.end()),outgoing.end());
  for(auto key:outgoing){auto [id,novel]=insert(key);cols.push_back(id);nodes[id].degree++;}
 }
 rowPtr.push_back(cols.size());
 std::deque<uint32_t> q;for(size_t i=0;i<nodes.size();i++)if(nodes[i].degree==0)q.push_back(i);
 // Reverse Kahn instead of forward Kahn: peel outdegree=0 sinks from reverse links.
 // Construct reverse CSR from forward edges.
 std::vector<uint32_t> revptr(nodes.size()+1,0);for(auto id:cols)revptr[id+1]++;
 for(size_t k=1;k<revptr.size();k++)revptr[k]+=revptr[k-1];
 std::vector<uint32_t> rev(cols.size());auto cursors=revptr;
 for(uint32_t i=0;i<nodes.size();i++)for(size_t z=rowPtr[i];z<rowPtr[i+1];z++)rev[cursors[cols[z]]++]=i;
 std::vector<uint32_t> outdeg(nodes.size());for(size_t i=0;i<nodes.size();i++){outdeg[i]=rowPtr[i+1]-rowPtr[i];}
 q.clear();for(uint32_t i=0;i<nodes.size();i++)if(!outdeg[i])q.push_back(i);
 size_t peeled=0;while(!q.empty()){auto v=q.front();q.pop_front();peeled++;for(size_t k=revptr[v];k<revptr[v+1];k++)if(--outdeg[rev[k]]==0)q.push_back(rev[k]);}
 std::cout<<"j="<<j<<" boundary="<<(1<<free.size())<<" seeds="<<rootCandidates<<" unique_roots="<<initial<<" reachable="<<nodes.size()<<" edges="<<cols.size()<<" cyclic_core="<<(nodes.size()-peeled)<<"\n";
 return nodes.size()==peeled?0:1;
}
