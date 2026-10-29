// Agent-13 F1 decimal p8 ternary automatic-centre finite-window obstruction.
// Exhaust every injective decimal coefficient triple and each exact source
// factor; carry choices at all eight steps are unrestricted (necessary filter).
// Capped computations are reported, never silently treated as exclusion.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <set>
#include <string>
#include <unordered_set>
#include <vector>
#include <chrono>
using u128=unsigned __int128;
struct Hash128 { size_t operator()(u128 x) const noexcept {
  uint64_t z=(uint64_t)x ^ (uint64_t)(x>>64) ^ UINT64_C(0x9e3779b97f4a7c15);
  z^=z>>30;z*=UINT64_C(0xbf58476d1ce4e5b9);z^=z>>27;
  z*=UINT64_C(0x94d049bb133111eb);return (size_t)(z^(z>>31));
}};
static std::vector<std::string> factors(int n){
 std::string w="0";
 for(int d=0;d<16;d++){
  std::string v;v.reserve(w.size()*2);
  for(char c:w){v+='0';v+=(c=='0'?'1':c=='1'?'2':'0');}
  w.swap(v);
 }
 std::set<std::string> s;
 for(size_t i=0;i+n<=w.size();i++)s.insert(w.substr(i,n));
 return {s.begin(),s.end()};
}
static u128 pack(const std::array<unsigned char,30>& w,int n){
 u128 k=0;for(int i=n-1;i>=0;--i)k=k*19+w[i];return k;
}
static void unpack(u128 key,int n,unsigned char * w){
 for(int i=0;i<n;i++){w[i]=key%19;key/=19;}
}
static uint64_t pattern(u128 k,int n){
 signed char map[19];std::fill(map,map+19,-1);int count=0;
 uint64_t key=0;
 for(int i=0;i<n;i++){
  int v=k%19;k/=19;
  if(v>18)return UINT64_MAX;
  if(map[v]<0){if(count==3)return UINT64_MAX;map[v]=count++;}
  key |= ((uint64_t)map[v])<<(2*i);
 }return key;
}
static uint64_t pattern_string(const std::string& w){
 signed char map[3]={-1,-1,-1};int count=0;uint64_t key=0;
 for(size_t i=0;i<w.size();i++){
  int v=w[i]-'0';if(map[v]<0)map[v]=count++;
  key |= ((uint64_t)map[v])<<(2*i);
 }return key;
}
static void transition(u128 input,int len,int gam,std::unordered_set<u128,Hash128>& next){
 unsigned char a[30],lo[2][30],up[2][30];unpack(input,len,a);
 for(int lc=0;lc<2;lc++){
  int c=lc;
  for(int i=0;i<len;i++){int z=a[i]+c;lo[lc][i]=z%10;c=z/10;}
 }
 for(int rc=0;rc<2;rc++){
  int c=rc;
  for(int i=len-1;i>=0;i--){int z=a[i]+c;up[rc][i]=z%10;c=z/10;}
 }
 for(int lc=0;lc<2;lc++)for(int rc=0;rc<2;rc++){
  u128 out=0;for(int i=len-1;i>=gam;i--){int v=lo[lc][i]+up[rc][i-gam];out=out*19+v;}
  next.insert(out);
 }
}
struct Out{bool survivors=false,capped=false;size_t max_states=0;int final_states=0;};
static Out run(u128 seed,const std::unordered_set<uint64_t>& target,size_t maxstates,int n){
 constexpr int G[8]={1,0,1,0,1,0,1,0};
 std::unordered_set<u128,Hash128> now,next;now.insert(seed);
 int len=n+4;size_t hi=1;
 for(int gam:G){
  next.clear();next.reserve(now.size()*3+10);
  for(u128 s:now){transition(s,len,gam,next);if(next.size()>maxstates)return {false,true,next.size(),0};}
  len-=gam;hi=std::max(hi,next.size());now.swap(next);
 }
 bool found=false;
 for(u128 k:now)if(target.count(pattern(k,len))){found=true;break;}
 return {found,false,hi,(int)now.size()};
}
int main(int argc,char** argv){
 int start=0,end=5814;size_t maxstates=50000;std::string file="p8_nfa.tsv";int n=16;
 if(argc>1)start=atoi(argv[1]);if(argc>2)end=atoi(argv[2]);
 if(argc>3)maxstates=(size_t)atoll(argv[3]);if(argc>4)file=argv[4];if(argc>5)n=atoi(argv[5]);if(n<4||n>26)return 6;
 auto sources=factors(n+4),targets=factors(n);
 if(sources.empty()||targets.empty()){std::cerr<<"INVALID FACTOR COUNTS\n";return 2;}
 std::unordered_set<uint64_t> target;
 for(const auto& w:targets)target.insert(pattern_string(w));
 std::vector<std::array<int,3>> triples;
 for(int a=0;a<19;a++)for(int b=0;b<19;b++)if(b!=a)
 for(int c=0;c<19;c++)if(c!=a&&c!=b)triples.push_back({a,b,c});
 if(triples.size()!=5814){std::cerr<<"TABLE ERROR\n";return 3;}
 std::ofstream out(file,std::ios::app);if(!out){std::cerr<<"NO OUTPUT FILE\n";return 4;}
 int any=0,capped=0;size_t max_seen=0;
 const auto begin=std::chrono::steady_clock::now();
 for(int t=start;t<std::min(end,5814);t++){
  auto a=triples[t];int hits=0,caps=0;size_t m=0;
  for(const auto& src:sources){
   std::array<unsigned char,30> w{};
   for(int i=0;i<n+4;i++)w[i]=a[src[i]-'0'];
   Out v=run(pack(w,n+4),target,maxstates,n);
   hits+=v.survivors;caps+=v.capped;m=std::max(m,v.max_states);
  }
  out<<t<<'\t'<<a[0]<<','<<a[1]<<','<<a[2]<<'\t'<<sources.size()<<'\t'<<hits<<'\t'<<caps<<'\t'<<m<<'\n';out.flush();
  any+=hits;capped+=caps;max_seen=std::max(max_seen,m);
  if((t+1)%100==0||t+1==end){
   auto sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count();
   std::cout<<"PROGRESS tables="<<(t+1-start)<<" range="<<start<<":"<<t+1<<" tested="<<(t+1-start)*sources.size()<<" hits="<<any<<" cap="<<capped<<" maxstates="<<max_seen<<" seconds="<<sec<<std::endl;
  }
 }
}