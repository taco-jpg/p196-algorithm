// Independent full-time joint fourth/fifth decimal coefficient DP.
// It never constructs a five-time-step block or SCC; instead it iterates
// literal position-automaton equations over all (x4,x5) in [0,18]^2.
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
using namespace std;
using U=uint64_t;
static constexpr int N=19*19;
U trace_at(int repetitions){
 U total=0;
 constexpr int L4[5]={1,1,0,0,1};
 for(int initial4=0;initial4<19;initial4++)for(int initial5=0;initial5<19;initial5++){
  array<U,N>dp{},nxt{};dp[19*initial4+initial5]=1;
  for(int t=0;t<5*repetitions;t++){
   int phase=t%5;bool overflow=phase<2;
   nxt={};
   for(int x4=0;x4<19;x4++)for(int x5=0;x5<19;x5++){
    U ways=dp[19*x4+x5];if(!ways)continue;
    for(int c4=0;c4<=1;c4++){
     int h4=(x4+c4)/10;
     // Third outgoing carry permits arbitrary a at phase0, b at phase1.
     // At phases2,3,4 it is exactly 0,1,0.
     if(phase==2&&h4!=0)continue;
     if(phase==3&&h4!=1)continue;
     if(phase==4&&h4!=0)continue;
     int Y4=(phase==0?5+h4:h4);
     int next4=(x4+L4[phase])%10+(overflow?Y4:(x4+c4)%10);
     int L5=(x4+L4[phase])/10;
     for(int c5=0;c5<=1;c5++){
      if((x5+c5)/10!=c4)continue;
      int next5=(x5+L5)%10+(overflow?(x4+c4)%10:(x5+c5)%10);
      if(next4<0||next4>=19||next5<0||next5>=19)abort();
      nxt[19*next4+next5]+=ways;
     }
    }
   }
   dp=nxt;
  }
  total+=dp[19*initial4+initial5];
 }
 return total;
}
int main(int argc,char**argv){
 int maxk=argc>1?atoi(argv[1]):12;
 if(maxk<1||maxk>20)return 2;
 U power6=1;
 for(int k=1;k<=maxk;k++){
  if((k&1)==0)power6*=6;
  U expected=(k&1)?0:2*power6;
  U got=trace_at(k);
  if(got!=expected){cerr<<"FAIL k="<<k<<" got="<<got<<" expected="<<expected<<"\n";abort();}
  cout<<"k="<<k<<" fifth_closed="<<got<<" PASS\n";
 }
}
