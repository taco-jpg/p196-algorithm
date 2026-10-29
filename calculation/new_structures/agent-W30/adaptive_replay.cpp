// Agent W30: full-integer independent replay of an adaptive 5-period central carry fibre.
// Reads the explicit W30 integer-construction helper, without assuming any overflow schedule.
#include <array>
#define main W30_EXPLICIT_SEED_HELPER
#include "replay.cpp"
#undef main
using Row=std::array<int,5>;
static bool fibre(Row const &r,bool reverse,Row &incoming){
 int roots=0;
 for(int c0=0;c0<=1;c0++){
  int c=c0;Row trial{};
  for(int j=0;j<5;j++){
   int i=reverse?(5-j)%5:j;
   trial[i]=c;
   c=(r[i]+c)/10;
  }
  if(c==c0){incoming=trial;roots++;}
 }
 return roots==1; // all-9s has two carry branches; refuse unjustified abstraction.
}
static bool row_step(Row const &r,int gamma,Row &out){
 Row cl{},ch{};
 if(!fibre(r,false,cl)||!fibre(r,true,ch))return false;
 for(int i=0;i<5;i++){
  int j=gamma?(i+4)%5:i;
  out[i]=(r[i]+cl[i])%10 + (r[j]+ch[j])%10;
  if(out[i]<0||out[i]>18)bad("pair coefficient out of range");
 }
 return true;
}
int main(int argc,char **argv){
 int T=argc>1?atoi(argv[1]):50473;
 int radius=argc>2?atoi(argv[2]):1000;
 int interval=argc>3?atoi(argv[3]):5000;
 Word P=make_P(300,4200),d=realize(P);
 Big9 N(tostr(d));
 Row r{17,3,14,3,17};
 int ix=39+20*300;
 int overflowOnes=0,firstClock=-1,firstNine=-1,firstEven=-1;
 bool seenBreak=false;
 for(int t=0;t<=T;t++){
  if(P!=pairs(d))bad("entire pairword mismatches ordinary digits at t="+to_string(t));
  string sn=N.digits();
  if(sn!=tostr(d))bad("independent full base1e9 bigint differs at t="+to_string(t));
  if(equal(d.begin(),d.begin()+d.size()/2,d.rbegin()))bad("palindrome at t="+to_string(t));
  int n=P.size(),centre=n/2;
  int mismatch=0,firstBadOff=0,odd=0,nine=0;
  for(int j=centre-radius;j<=centre+radius;j++){
   int expect=r[(j-ix+5*1000000)%5];
   if(P[j]!=expect){if(!mismatch)firstBadOff=j-centre;mismatch++;}
   odd+=(P[j]%2);nine+=(P[j]==9);
  }
  if(nine && firstNine<0){firstNine=t;cout<<"FIRST_CENTRE_9 t="<<t<<"\n";}
  if(!odd && firstEven<0){firstEven=t;cout<<"FIRST_CENTRE_ALL_EVEN t="<<t<<"\n";}
  int delta=(n-1-2*ix)%5;
  for(int j=0;j<5;j++)if(r[j]!=r[(delta-j+5)%5])bad("mirror axis incompatible t="+to_string(t));
  if(mismatch){
   if(t!=50473||radius!=1000)bad("unexpected centre mismatch t="+to_string(t));
   seenBreak=true;
   cout<<"EXPECTED_WINDOW_BREAK t="<<t<<" count="<<mismatch<<" firstOffset="<<firstBadOff<<"\n";
  }
  if(t%interval==0||t==T){
   cout<<"CHECK t="<<t<<" digits="<<n<<" overflowOnes="<<overflowOnes<<" centreOdd="<<odd<<" centre9="<<nine<<" row=";
   for(auto v:r)cout<<v<<",";
   cout<<" digitsFNV64="<<summary(d)<<"\n"<<flush;
  }
  if(t==T)break;
  auto [nextP,g1]=pair_step(P);
  auto [nextD,g2]=digit_step(d);
  if(g1!=g2)bad("independent carry disagreement t="+to_string(t));
  if(firstClock<0 && g1!=int(t%2==0)){
    firstClock=t;
    cout<<"FIRST_CLOCK_BREAK t="<<t<<" expected="<<int(t%2==0)<<" actual="<<g1<<"\n";
  }
  Row rowNext{};
  if(!row_step(r,g1,rowNext))bad("ambiguous periodic carry row t="+to_string(t));
  // Decimal integer limbs use an independent reversal and addition.
  reverse(sn.begin(),sn.end());Big9 rev(sn);N+=rev;
  overflowOnes+=g1;
  P.swap(nextP);d.swap(nextD);r=rowNext;
  if(seenBreak)bad("did not stop immediately on wave break");
 }
 if(T==50473 && radius==1000 && !seenBreak)bad("expected first local mismatch not detected");
 cout<<"PASS full integer/reverse/digit/pairword replay for "<<T<<" steps, zero palindromes; adaptive centre valid through t="<<(seenBreak?T-1:T)<<"\n";
}
