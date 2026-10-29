#include <array>
// agent W30 third probe: adaptive 5-site periodic carry fibre, paired with a true decimal pairword orbit.
#define main W30_REPLAY_MAIN
#include "replay.cpp"
#undef main
using Array = array<int,5>;
static int cyclic_carry(Array const &R, bool reverse, Array &carries){
 for(int c0=0;c0<=1;c0++){
  int c=c0;Array tmp{};
  for(int j=0;j<5;j++){int i=reverse?(5-j)%5:j;tmp[i]=c;c=(R[i]+c)/10;}
  if(c==c0){carries=tmp;return 1;}
 }
 return 0;
}
static bool fullrow(Array const &R, int gamma, Array &Y){
 Array cl{},ch{}; if(!cyclic_carry(R,false,cl)||!cyclic_carry(R,true,ch))return false;
 for(int i=0;i<5;i++){
  int d=(R[i]+cl[i])%10;int j=gamma?(i+4)%5:i;
  Y[i]=d+(R[j]+ch[j])%10;
 }
 return true;
}
int main(int argc,char **argv){int limit=argc>1?atoi(argv[1]):40000;
 Word P=make_P(300,4200);Array R{17,3,14,3,17};int idx=6039;int first9=-1,first_even=-1, first_notperiod=-1, first_mismatch=-1,first_clock=-1,first_nonmirror=-1,firstamb=-1;
 for(int t=0;t<=limit;t++){
  int n=P.size(),ctr=n/2;int width=argc>2?atoi(argv[2]):100;bool equalAll=true, periodAll=true;int odd=0,nine=0;
  for(int j=ctr-width;j<=ctr+width;j++){
   if(P[j]!=R[(j-idx+5*100000)%5])equalAll=false;
   if(j+5<=ctr+width && P[j]!=P[j+5])periodAll=false;
   odd+=P[j]%2;nine+=(P[j]==9);
  }
  if(!equalAll&&first_mismatch==-1){first_mismatch=t;cout<<"FIRST predicted row mismatch t="<<t<<"\n";}
  if(!periodAll&&first_notperiod==-1){first_notperiod=t;cout<<"FIRST observed period5 mismatch t="<<t<<"\n";}
  if(nine&&first9==-1){first9=t;cout<<"FIRST nine in centre t="<<t<<"\n";}
  if(!odd&&first_even==-1){first_even=t;cout<<"FIRST no odd in centre200 t="<<t<<"\n";}
  int delta=(n-1-2*idx)%5;for(int i=0;i<5;i++)if(R[i]!=R[(delta-i+5)%5]){if(first_nonmirror<0){first_nonmirror=t;cout<<"FIRST row not mirror-compatible t="<<t<<"\n";}break;}
  if(t>=26705 && (t<26740||t%1000==0)){cout<<"time="<<t<<" row=";for(int v:R)cout<<v<<",";cout<<" odd="<<odd<<" nine="<<nine<<" rowOK="<<equalAll<<" per5="<<periodAll<<"\n";}
  if(t==limit)break;
  auto [Q,g]=pair_step(P);
  if(g!=int(t%2==0)&&first_clock<0){first_clock=t;cout<<"FIRST GAMMA OFF t="<<t<<" observed="<<g<<"\n";}
  Array y{};if(!fullrow(R,g,y)){if(firstamb<0){firstamb=t;cout<<"FIRST cyclic carry ambiguous t="<<t<<"\n";}break;}
  P.swap(Q);R=y;
  if(first_notperiod>=0||first_mismatch>=0)break;
 }
 cout<<"SUMMARY clock="<<first_clock<<" nine="<<first9<<" all_even="<<first_even<<" wrongrow="<<first_mismatch<<" nonperiod="<<first_notperiod<<" mirror="<<first_nonmirror<<" ambiguous="<<firstamb<<"\n";
}
