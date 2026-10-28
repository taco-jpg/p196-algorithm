// Independent original-time check: no closed SIX-column history for g=(11000)^k.
// Starts at each necessary cyclic (fourth,fifth) block boundary (three states),
// but imposes NO intermediate 5-step SCC restriction. Direct c4/c5/c6 loops.
// Does not use the six-column block-graph program or its edges.
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
using namespace std;
using U=unsigned __int128;
constexpr int N=19*19*19;
constexpr int L4[5]={1,1,0,0,1};
constexpr int starts[3][2]={{9,9},{15,0},{15,9}};
static inline int key(int a,int b,int c){return 361*a+19*b+c;}
U count_closures(int k){
 U total=0;
 for(const auto&src:starts)for(int z6=0;z6<19;z6++){
  int z4=src[0],z5=src[1];
  array<U,N> cur{},nxt{};cur[key(z4,z5,z6)]=1;
  for(int t=0;t<5*k;t++){
   nxt={};int phase=t%5;bool overflow=phase<2;
   for(int x4=0;x4<19;x4++)for(int x5=0;x5<19;x5++)for(int x6=0;x6<19;x6++){
    U ways=cur[key(x4,x5,x6)];if(!ways)continue;
    for(int c4=0;c4<=1;c4++){
     int h4=(x4+c4)/10;
     if(phase==2&&h4!=0)continue;
     if(phase==3&&h4!=1)continue;
     if(phase==4&&h4!=0)continue;
     int y4=(x4+L4[phase])%10+(overflow?(phase==0?5+h4:h4):(x4+c4)%10);
     int L5=(x4+L4[phase])/10;
     for(int c5=0;c5<=1;c5++){
      if((x5+c5)/10!=c4)continue;
      int y5=(x5+L5)%10+(overflow?(x4+c4)%10:(x5+c5)%10);
      int L6=(x5+L5)/10;
      for(int c6=0;c6<=1;c6++){
       if((x6+c6)/10!=c5)continue;
       int y6=(x6+L6)%10+(overflow?(x5+c5)%10:(x6+c6)%10);
       assert(0<=y4&&y4<19 && 0<=y5&&y5<19 && 0<=y6&&y6<19);
       nxt[key(y4,y5,y6)]+=ways;
      }
     }
    }
   }
   cur=nxt;
  }
  total+=cur[key(z4,z5,z6)];
 }
 return total;
}
int main(int argc,char**argv){
 int kmax=argc>1?atoi(argv[1]):8;
 if(kmax<1||kmax>12)return 2;
 for(int k=1;k<=kmax;k++){
  U n=count_closures(k);
  if(n){cerr<<"FAILED: sixth-column return exists k="<<k<<"\n";abort();}
  cout<<"k="<<k<<" sixth_column_closed=0 PASS\n";
 }
}
