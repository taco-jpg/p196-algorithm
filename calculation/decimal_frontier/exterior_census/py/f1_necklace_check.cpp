// Independent FKM enumeration of base-10 F1 necklace words, no semigroup/Burnside.
// Compile: c++ -O3 -std=c++17 f1_necklace_check.cpp -o /tmp/f1_check
// Run: /tmp/f1_check 44  (higher periods may take a long time).
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <vector>
#include <map>
#include <cstdlib>
using namespace std;
using u64=uint64_t;
int b=10,ns=18,p;u64 edges[2][64];
vector<int> word;map<int,u64> countG;u64 total,primitive;
struct Row{u64 r[64];};
void extend(const Row&a,int g,Row&o){
 for(int i=0;i<ns;i++){u64 q=a.r[i],m=0;
  while(q){int j=__builtin_ctzll(q);q&=q-1;m|=edges[g][j];}o.r[i]=m;}
}
bool live(const Row&a){for(int i=0;i<ns;i++)if(a.r[i])return true;return false;}
bool closed(const Row&a){for(int i=0;i<ns;i++)if(a.r[i]&(1ULL<<i))return true;return false;}
void gen(int t,int pp,int G,const Row&R){
 if(t>p){if(p%pp==0&&closed(R)){total++;countG[G]++;if(pp==p)primitive++;}return;}
 for(int a=word[t-pp];a<=1;a++){Row r;extend(R,a,r);if(!live(r))continue;
  word[t]=a;gen(t+1,a==word[t-pp]?pp:t,G+a,r);}
}
int main(int argc,char**argv){
 int pmax=atoi(argv[1]);
 for(int x=1;x<=18;x++)for(int c=0;c<=1;c++){
  int g=(x+c)/b;if(g>1)continue;
  int nx=x%b+(g?1:(x+c)%b);
  if(nx>=1&&nx<=18)edges[g][x-1]|=1ULL<<(nx-1);
 }
 for(p=1;p<=pmax;p++){
  total=primitive=0;countG.clear();word.assign(p+2,0);Row r;
  for(int i=0;i<ns;i++)r.r[i]=1ULL<<i;
  gen(1,1,0,r);
  printf("p=%d n=%llu primitive=%llu byG=",p,
         (unsigned long long)total,(unsigned long long)primitive);
  for(auto [G,n]:countG)printf(" %d:%llu",G,(unsigned long long)n);
  printf("\n");fflush(stdout);
 }
}
