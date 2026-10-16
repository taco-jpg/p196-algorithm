// Exact finite autonomous-outer graph, independent C++ implementation.
// Build: g++ -std=c++17 -O2 -Wall -Wextra -pedantic outer_scan.cpp -o outer_scan
// Run: ./outer_scan 5 ranks-L5.bin > scan-L5.json
// Each output byte is a rank, with 255 denoting an invalid/untrimmed code.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using Word = std::vector<int>;
struct State {int c; Word b;};
struct Result {State s; int gamma; int stripped;};
static Result step(const State& s) {
  int n=static_cast<int>(s.b.size()), k=s.c>=10, t=s.c-9*k;
  Word d(n),r(n); int e=0;
  for(int i=0;i<n;++i){int z=s.b[i]+e;d[i]=z%10;e=z/10;}
  int u=s.c+e-10*k; e=k;
  for(int i=0;i<n;++i){int z=s.b[n-1-i]+e;r[i]=z%10;e=z/10;}
  int gamma=e; Word out(n+1);
  for(int i=0;i<=n;++i){
    int a=i<n?d[i]:u;
    int b=gamma?(i==0?1:r[n-i]):(i<n?r[n-1-i]:t);
    out[i]=a+b;
  }
  int stripped=0;
  while(!out.empty() && out.back()==2*t){out.pop_back();++stripped;}
  return {{2*t,out},gamma,stripped};
}
static void emit(const State& s){
  std::cout<<"["<<s.c<<",[";
  for(size_t i=0;i<s.b.size();++i){if(i)std::cout<<",";std::cout<<s.b[i];}
  std::cout<<"]]";
}
int main(int argc,char**argv){try{
  int L=argc>1?std::stoi(argv[1]):3;
  if(L<0 || L>5)throw std::runtime_error("Supported bounds are 0..5");
  std::array<uint32_t,8> p{},off{};p[0]=1;off[0]=0;
  for(int j=1;j<=L+1;++j){p[j]=p[j-1]*19;off[j]=off[j-1]+p[j-1];}
  uint32_t stride=off[L+1],total=8*stride;
  auto decode=[&](uint32_t id){
    int phase=2*(id/stride+1); uint32_t w=id%stride;int n=0;
    while(n<L && w>=off[n+1])++n;
    w-=off[n];Word B(n);
    for(int j=0;j<n;++j){B[j]=w%19;w/=19;}
    return State{phase,B};
  };
  auto encode=[&](const State&s)->int32_t{
    if(s.b.size()>static_cast<size_t>(L))return -1;
    uint32_t id=(s.c/2-1)*stride+off[s.b.size()];
    for(size_t i=0;i<s.b.size();++i)id+=s.b[i]*p[i];
    return static_cast<int32_t>(id);
  };
  std::vector<int32_t> edge(total,-2);
  std::vector<uint8_t> rank(total,255);
  uint64_t valid=0;
  for(uint32_t i=0;i<total;++i){
    auto s=decode(i);
    if(!s.b.empty() && (s.b.front()==0 || s.b.back()==s.c))continue;
    ++valid;rank[i]=0;edge[i]=encode(step(s).s);
  }
  uint32_t best=0;int maxrank=0;std::vector<uint32_t> path;
  for(uint32_t i=0;i<total;++i){
    if(rank[i]!=0)continue;
    path.clear();int32_t j=i;
    while(j>=0 && rank[j]==0){rank[j]=254;path.push_back(j);j=edge[j];}
    if(j>=0 && rank[j]==254){
      std::cout<<"{\"cycle_detected\":true,\"state\":";emit(decode(j));std::cout<<"}\n";return 2;
    }
    if(j>=0 && rank[j]==255)throw std::runtime_error("Transition entered an invalid state");
    int r=j<0?0:rank[j];
    for(auto it=path.rbegin();it!=path.rend();++it){
      if(++r>=254)throw std::runtime_error("Rank exceeds byte encoding");
      rank[*it]=r;if(r>maxrank){maxrank=r;best=*it;}
    }
  }
  std::vector<uint64_t> hist(maxrank+1,0);
  for(uint32_t i=0;i<total;++i){
    if(rank[i]==255)continue;
    int32_t j=edge[i];
    if(rank[i] != 1+(j<0?0:rank[j]))throw std::runtime_error("Rank identity failed");
    ++hist[rank[i]];
  }
  if(argc>2){std::ofstream f(argv[2],std::ios::binary);f.write(reinterpret_cast<const char*>(rank.data()),rank.size());if(!f)throw std::runtime_error("Rank write failed");}
  std::cout<<"{\"bound\":"<<L<<",\"encoded_slots\":"<<total<<",\"valid_states\":"<<valid<<",\"cycles\":0,\"max_exit_time\":"<<maxrank<<",\"rank_histogram\":{";
  for(int i=1;i<=maxrank;++i){if(i>1)std::cout<<",";std::cout<<"\""<<i<<"\":"<<hist[i];}
  std::cout<<"},\"sharp_outer_path\":[";
  int32_t j=best;bool first=true;
  while(j>=0){if(!first)std::cout<<",";first=false;auto s=decode(j);emit(s);auto out=step(s).s;j=encode(out);if(j<0){std::cout<<",";emit(out);}}
  std::cout<<"]}\n";
}catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 1;}}
