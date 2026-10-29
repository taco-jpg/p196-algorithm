// X07 follow-up: synchronized nine-piston guard in an exact repdigit frontier.
// Compile: g++ -std=c++17 -O3 piston_probe.cpp -lgmpxx -lgmp -o piston_probe
// Run: ./piston_probe 60000 -2907
// Reuses the independently whole-number-validated exact step kernel.
#define main repdigit_main_unused
#include "repdigit_front.cpp"
#undef main
#include <map>
int main(int argc,char**argv){
  const int H=argc>1?atoi(argv[1]):60000;
  const int k=argc>2?atoi(argv[2]):-2907;
  Front f=start(9,k);int maxNeed=0,maxOdd=-1,maxFront=0;
  int overCounts[2]={},carryCounts[2]={};
  int offset=-1,initialOver=-1,initialDelta=-1;
  for(int t=0;t<=H;t++){
    int m=f.left.size(),firstOdd=0;
    while(firstOdd<m && ((f.left[firstOdd]+f.right[m-1-firstOdd])%2==0))++firstOdd;
    if(firstOdd==m){cerr<<"NO ODD PAIR at t="<<t<<"\n";return 3;}
    maxOdd=max(maxOdd,firstOdd);
    maxNeed=max(maxNeed,2*m-f.over);maxFront=max(maxFront,m);
    if(t==1)offset=m-f.over;
    if(t>=1 && m-f.over!=offset){cerr<<"PISTON DRIFT at t="<<t<<"\n";return 4;}
    if(t==0||t%10000==0||t==H)
      cerr<<"checkpoint t="<<t<<" front="<<m<<" G="<<f.over<<" core_lower_bound="<<maxNeed+2<<" odd_bound="<<maxOdd<<"\n";
    if(t==H)break;
    int entering=0;
    for(int i=0;i<m;i++)entering=(f.left[i]+f.right[m-1-i]+entering)/10;
    int g0=f.over,m0=m;
    int gamma=step(f);
    if(t==0){initialOver=gamma;initialDelta=int(f.left.size())-m;}
    else {
      if(entering+gamma!=1){cerr<<"COMPLEMENTARY CARRY FAIL at t="<<t<<"\n";return 5;}
      if(int(f.left.size())-m0!=gamma){cerr<<"PISTON STEP FAIL at t="<<t<<"\n";return 6;}
      carryCounts[entering]++;
    }
    overCounts[gamma]++;
    if(f.over!=g0+gamma)throw runtime_error("overflow counter");
  }
  cout<<"PISTON PASS k="<<k<<" H="<<H<<" offset_after_first="<<offset
      <<" initial_gamma="<<initialOver<<" initial_delta_m="<<initialDelta
      <<" max_needed_n="<<maxNeed+2<<" max_front="<<maxFront
      <<" overflows="<<f.over<<" gamma0="<<overCounts[0]<<" gamma1="<<overCounts[1]
      <<" max_first_odd_index="<<maxOdd<<" final_bulk="<<f.bulk<<"\n";
  return 0;
}
