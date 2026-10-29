// W30 fourth probe: follow first boundary intrusion through nested centre windows.
#include <array>
#define main W30_EXPLICIT_SEED_HELPER
#include "replay.cpp"
#undef main
using Row=std::array<int,5>;
static bool solve(Row const &r,bool reverse,Row &c){
 int roots=0;for(int initial=0;initial<=1;initial++){
  int carry=initial;Row a{};for(int k=0;k<5;k++){
   int i=reverse?(5-k)%5:k;
   a[i]=carry;carry=(r[i]+carry)/10;
  }
  if(carry==initial){c=a;roots++;}
 }return roots==1;
}
static bool update(Row const &r,int gamma,Row &next){
 Row cl{},ch{};if(!solve(r,false,cl)||!solve(r,true,ch))return false;
 for(int i=0;i<5;i++){
  int j=(i-gamma+5)%5;
  next[i]=(r[i]+cl[i])%10+(r[j]+ch[j])%10;
 }return true;
}
int main(int argc,char **argv){
 int limit=argc>1?atoi(argv[1]):85000;
 Word P=make_P(300,4200);Row r{17,3,14,3,17};
 const int idx=6039;const std::array<int,8> radii{5000,2000,1000,500,200,100,20,0};
 std::array<int,8> firstBad{},recover{},lastBad{},totalBad{};
 firstBad.fill(-1);recover.fill(-1);lastBad.fill(-1);totalBad.fill(0);
 int gammaOnes=0,firstAllEven=-1;
 for(int t=0;t<=limit;t++){
  const int n=P.size(),m=n/2;
  std::array<int,8> mismatch{};
  for(int j=m-radii[0];j<=m+radii[0];j++){
   int v=r[(j-idx+5*1000000)%5];
   if(P[j]!=v){int off=abs(j-m);
    for(int k=0;k<8;k++)if(off<=radii[k])mismatch[k]++;
   }
  }
  for(int k=0;k<8;k++){
   if(mismatch[k] && firstBad[k]<0){firstBad[k]=t;std::cout<<"FIRST_INTRUSION radius="<<radii[k]<<" t="<<t<<" badCount="<<mismatch[k]<<"\n"<<std::flush;}
   if(mismatch[k]){lastBad[k]=t;totalBad[k]++;}
   if(!mismatch[k] && firstBad[k]>=0 && recover[k]<0){recover[k]=t;std::cout<<"FIRST_RECOVERY radius="<<radii[k]<<" t="<<t<<"\n"<<std::flush;}
  }
  if(!std::any_of(P.begin(),P.end(),[](int x){return x%2;})&&firstAllEven<0){firstAllEven=t;std::cout<<"NO_GLOBAL_ODD_WITNESS t="<<t<<"\n";}
  if(t%5000==0||t==limit){
   std::cout<<"CHECK t="<<t<<" n="<<n<<" gammas="<<gammaOnes<<" badR5000="<<mismatch[0]<<" badR1000="<<mismatch[2]<<" badR0="<<mismatch[7]<<" row=";
   for(int x:r)std::cout<<x<<",";
   std::cout<<"\n"<<std::flush;
  }
  if(t==limit)break;
  auto [nxt,g]=pair_step(P);Row out{};
  if(!update(r,g,out))bad("ambiguous centre row at t="+std::to_string(t));
  gammaOnes+=g;P.swap(nxt);r=out;
 }
 if(firstAllEven>=0)bad("some state lost the all-word odd pairword witness at "+std::to_string(firstAllEven));
 std::cout<<"PASS nonpalindromicity through t="<<limit<<" by a checked odd coefficient of the exact full pairword at every step\n";
 std::cout<<"SUMMARY t="<<limit<<" globalOddLost="<<firstAllEven<<"\n";
 for(int k=0;k<8;k++)std::cout<<"WINDOW radius="<<radii[k]<<" first="<<firstBad[k]<<" recovered="<<recover[k]<<" last="<<lastBad[k]<<" mismatchedSteps="<<totalBad[k]<<"\n";
 return 0;
}
