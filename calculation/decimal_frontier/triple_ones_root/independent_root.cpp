// Independent literal temporal-digit DP: no block graph or symbolic proof reused.
// g=(111 0^r)^k; compare exact closed root histories against 4^k if r=4, else 0.
// g++ -std=c++17 -O2 independent_root.cpp -o /tmp/independent_root && /tmp/independent_root 100 12
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
using namespace std;
using u64=uint64_t;
int main(int argc,char**argv){
  int rm=argc>1?atoi(argv[1]):100,km=argc>2?atoi(argv[2]):12;
  if(rm<6||km<1||km>12)return 2;
  int total=0;
  for(int r=1;r<=rm;r++)for(int k=1;k<=km;k++){
    u64 count=0;
    for(int x0=1;x0<=18;x0++){
      array<u64,19> dp{};dp[x0]=1;
      for(int block=0;block<k;block++)for(int i=0;i<r+3;i++){
        int g=i<3;
        array<u64,19> ndp{};
        for(int x=0;x<=18;x++)if(dp[x])for(int c=0;c<=1;c++){
          if((x+c)/10!=g)continue;
          int y=x%10+(g?1:((x+c)%10));
          if(y<0||y>18)return 3;
          ndp[y]+=dp[x];
        }
        dp=ndp;
      }
      count+=dp[x0];
    }
    u64 expected=r==4?(1ULL<<(2*k)):0;
    if(count!=expected){printf("FAIL r=%d k=%d got=%llu expected=%llu\n",r,k,(unsigned long long)count,(unsigned long long)expected);return 1;}
    total++;
  }
  printf("PASS independent full-time recurrence r1..%d k1..%d cases=%d\n",rm,km,total);
}
