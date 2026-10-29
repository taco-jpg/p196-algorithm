// Independent real-integer check of the W01 three-body screened corridor.
// No digit-vector step, no CSV, no precomputed trajectory.
#include <gmpxx.h>
#include <algorithm>
#include <array>
#include <iostream>
#include <string>
using namespace std;
constexpr int ROOT[39]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
constexpr int BULK[20]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
string create(int mask,int Z){const int H=12000;string digits(2*H,'0');for(int j=0;j<H;j++){
 int q=j<39?ROOT[j]:BULK[(j-39)%20];
 if((mask&1)&&j>=6000&&j<6050)q=(7*j+11)%19;
 if((mask&2)&&j>=8000&&j<8050)q=(3*(j-8000)+10)%19;
 if((mask&4)&&j>=Z&&j<Z+50)q=(5*(j-Z)+3)%19;
 int l=min(9,q),h=q-l;digits[2*H-1-j]='0'+l;digits[j]='0'+h;
 }return digits;}
int main(int argc,char**argv){int T=argc>1?atoi(argv[1]):5600;int Z=argc>2?atoi(argv[2]):10080;int k=(Z-10000)/80;int birth=4354+88*k;int pos=9014+60*k;
 array<mpz_class,8>numbers;for(int k=0;k<8;k++)numbers[k]=mpz_class(create(k,Z),10);
 int first=-1,firstPos=-1,lastFailed=-1,windowOK=0,lastGap=-1,wrongFront=0;
 for(int t=0;t<=T;t++){
   array<string,8>strings;for(int k=0;k<8;k++)strings[k]=numbers[k].get_str(10);
   int n=strings[0].size(),h=n/2;
   for(int k=0;k<8;k++){
     if(int(strings[k].size())!=n){cerr<<"LENGTH_MISMATCH t="<<t<<" k="<<k<<"\n";return 2;}
     bool odd=0;for(int j=0;j<39;j++)odd|=((strings[k][j]+strings[k][n-1-j])%2)!=0;
     if(!odd){cerr<<"NO_NONPAL_WITNESS t="<<t<<" k="<<k<<"\n";return 2;}
   }
   auto dig=[&](int flag,int j,int side){int i=side?n-1-j:j;return int(strings[flag][i]-'0');};
   auto yz=[&](int j,int side){return dig(6,j,side)-dig(4,j,side)-dig(2,j,side)+dig(0,j,side);};
   auto yzWithX=[&](int j,int side){return dig(7,j,side)-dig(5,j,side)-dig(3,j,side)+dig(1,j,side);};
   auto triple=[&](int j,int side){return yzWithX(j,side)-yz(j,side);};
   auto xy=[&](int j,int side){return dig(3,j,side)-dig(2,j,side)-dig(1,j,side)+dig(0,j,side);};
   int f=-1,shield=-1,fxy=-1;
   // Two separate scans: pair-front uses digit *sums*, shield-front uses actual digit tracks.
   for(int j=0;j<h;j++){
      if(f<0 && triple(j,0)+triple(j,1))f=j;
      if(fxy<0 && xy(j,0)+xy(j,1))fxy=j;
      if(shield<0 && (yzWithX(j,0)||yzWithX(j,1)))shield=j;
      if(f>=0&&shield>=0&&fxy>=0)break;
   }
   if(f>=0&&first<0){first=t;firstPos=f;}
   if(t>=birth){
      if(f<0||shield<0){cerr<<"MISSING_FRONT "<<t<<"\n";return 3;}
      bool equal=true;
      for(int r=-20;r<=40;r++)for(int side=0;side<2;side++){
        int j=f+r;
        if(yzWithX(j,side)!=0)equal=false;
        if(t>=5300 && triple(j,side)!=-yz(j,side)){cerr<<"SHIELD_IDENTITY_FAIL";return 3;}
      }
      if(!equal)lastFailed=t;
      if(t>=5300){
         if(f!=fxy+2000+80*k){cerr<<"BAD_XY_TRANSLATION t="<<t<<" f="<<f<<" fxy="<<fxy<<"\n";return 4;}
         for(int r=-20;r<=35;r++)for(int side=0;side<2;side++)if(triple(f+r,side)!=-xy(fxy+r,side)){
           cerr<<"BAD_ANTIPODAL_XY t="<<t<<" r="<<r<<"\n";return 4;}
         if(!equal||shield-f<41){cerr<<"SHIELD_FAIL t="<<t<<" gap="<<shield-f<<"\n";return 4;}windowOK++;}
      if(shield!=f+40)wrongFront++;
      if(t==T)lastGap=shield-f;
   }
   if(t<T)for(int k=0;k<8;k++){
     string flipped=strings[k];reverse(flipped.begin(),flipped.end());
     numbers[k]+=mpz_class(flipped,10);
   }
 }
 if(first!=birth||firstPos!=pos||windowOK!=max(0,T-5299)||wrongFront==0){
   cerr<<"BAD_EXPECTED first="<<first<<"@"<<firstPos<<" lastFailed="<<lastFailed<<" windowOK="<<windowOK<<" wrongFront="<<wrongFront<<"\n";return 5;
 }
 cout<<"W01_TRIPLE_PARAM_GMP_PASS Z="<<Z<<" first="<<first<<"@"<<firstPos
  <<" lastNonzeroTile="<<lastFailed<<" canceledTiles="<<windowOK
  <<" signedCancels="<<windowOK*122<<" antipodalXYChecks="<<windowOK*112<<" finalGap="<<lastGap<<"\n";
}
