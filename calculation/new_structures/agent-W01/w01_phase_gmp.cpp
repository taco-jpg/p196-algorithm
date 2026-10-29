// Independent ordinary-GMP integer verification of W01 time/space scattering covariance.
// No use of the digit-vector arithmetic from w01_scatter_phase.cpp.
#include <gmpxx.h>
#include <algorithm>
#include <array>
#include <deque>
#include <iostream>
#include <string>
using namespace std;
constexpr int ROOT[39]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
constexpr int BULK[20]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
string seed(int flags,int y){
  const int H=12000;string s(2*H,'0');
  for(int j=0;j<H;j++){
    int q=j<39?ROOT[j]:BULK[(j-39)%20];
    if((flags&1)&&j>=6000&&j<6050)q=(7*j+11)%19;
    if((flags&2)&&j>=y&&j<y+50)q=(3*(j-y)+10)%19;
    const int lo=min(9,q),hi=q-lo;
    s[2*H-1-j]=char('0'+lo);s[j]=char('0'+hi);
  }
  return s;
}
struct R {int first=-1;array<int,61> lower{},upper{};};
R measure(const array<string,4>&s){
  for(int k=1;k<4;k++)if(s[k].size()!=s[0].size()){cerr<<"UNALIGNED_LENGTH\n";exit(2);}
  auto part=[&](int side,int j)->int{
    int z[4];for(int k=0;k<4;k++){
      const int a=side?s[k].size()-1-j:j;
      z[k]=s[k][a]-'0';
    }return z[3]-z[2]-z[1]+z[0];
  };
  R r;const int H=int(s[0].size())/2;
  for(int j=0;j<H;j++)if(part(0,j)+part(1,j)!=0){r.first=j;break;}
  if(r.first>=0)for(int u=0;u<61;u++){
    int j=r.first-20+u;
    if(j<0||j>=H){cerr<<"OUT_OF_RANGE";exit(2);}
    r.lower[u]=part(1,j);r.upper[u]=part(0,j);
  }
  return r;
}
int main(int argc,char**argv){
  const int T=argc>1?atoi(argv[1]):4500;
  array<array<mpz_class,4>,2> n;
  for(int z=0;z<2;z++)for(int k=0;k<4;k++)n[z][k]=mpz_class(seed(k,z?8080:8000),10);
  deque<R> history;int first0=-1,first1=-1,lastBad=-1,stable=0,wrong=0;
  for(int t=0;t<=T;t++){
    array<array<string,4>,2>s;
    for(int z=0;z<2;z++)for(int k=0;k<4;k++)s[z][k]=n[z][k].get_str(10);
    R a=measure(s[0]),b=measure(s[1]);
    if(a.first>=0&&first0<0)first0=t;
    if(b.first>=0&&first1<0)first1=t;
    if(t>=2242+88){
      const R& old=history.at(history.size()-88);
      bool good=(b.first==old.first+60 && b.lower==old.lower && b.upper==old.upper);
      if(!good)lastBad=t;
      if(t>=3108){if(!good){cerr<<"COVARIANCE_FAIL t="<<t<<" front="<<b.first<<" old="<<old.first<<"\n";return 3;} stable++;}
      if(b.first!=old.first+59)wrong++;
    }
    history.push_back(a);if(history.size()>89)history.pop_front();
    if(t<T)for(int z=0;z<2;z++)for(int k=0;k<4;k++){
      string reversed=s[z][k];reverse(reversed.begin(),reversed.end());
      n[z][k]+=mpz_class(reversed,10);
    }
  }
  if(first0!=2154||first1!=2242||lastBad!=2835 || stable!=max(0,T-3107)||wrong==0){
    cerr<<"BAD_CONTROLS first="<<first0<<","<<first1<<" lastBad="<<lastBad<<" stable="<<stable<<" wrong="<<wrong<<"\n";return 4;
  }
  cout<<"W01_PHASE_GMP_PASS baselineBirth="<<first0<<" shiftedBirth="<<first1
      <<" lastBadAligned="<<lastBad-88<<" stableWindowComparisons="<<stable
      <<" wrongShift59Failures="<<wrong<<"\n";
}
