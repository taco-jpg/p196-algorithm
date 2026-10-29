// Independently enumerate 361 seed pairs, using GMP numeric addition and string reversal.
#include <gmp.h>
#include <algorithm>
#include <cstring>
#include <iostream>
#include <string>
using namespace std;
int pre[]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
int cyc[]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
string seed(int h,int a,int b){string high,lo;for(int i=0;i<h;i++){int p=i<39?pre[i]:cyc[(i-39)%20];if(i==h-2)p=a;if(i==h-1)p=b;int low=max(0,p-9);high+=char('0'+p-low);lo+=char('0'+low);}reverse(lo.begin(),lo.end());return high+lo;}
string dec(mpz_t n){string s(mpz_sizeinbase(n,10)+3,0);mpz_get_str(s.data(),10,n);s.resize(strlen(s.c_str()));return s;}
int pairat(string const&s,int i){return (s[i]-'0')+(s[s.size()-1-i]-'0');}
void step(mpz_t a,mpz_t r,string s){reverse(s.begin(),s.end());if(mpz_set_str(r,s.c_str(),10))abort();mpz_add(a,a,r);}
int main(int argc,char**argv){
 int h=argc>1?atoi(argv[1]):500,T=argc>2?atoi(argv[2]):1500,m=argc>3?atoi(argv[3]):20;
 if(h<80||m<=0||m%20||T<0)return 2;
 mpz_t x,y,r;mpz_inits(x,y,r,nullptr);long long checked=0,paths=0;int first=-1,firstgamma=-1,firstpal=-1;
 for(int a=0;a<19;a++)for(int b=0;b<19;b++){
  mpz_set_str(x,seed(h,a,b).c_str(),10);mpz_set_str(y,seed(h+m,a,b).c_str(),10);
  for(int t=0;t<=T;t++){
   string sx=dec(x),sy=dec(y);int nx=sx.size(),ny=sy.size();if(nx+2*m!=ny&&first<0)first=t;
   for(int i=0;i<nx/2;i++){
    int small=pairat(sx,i),large=pairat(sy,i<39?i:i+m);checked++;
    if(small!=large&&first<0){first=t;cerr<<"FIRST GMP discrepancy t="<<t<<" a="<<a<<" b="<<b<<" i="<<i<<"\n";}
   }
   bool pal=true;for(int i=0;i<nx/2;i++)if(sx[i]!=sx[nx-1-i]){pal=false;break;}
   if(pal&&firstpal<0)firstpal=t;paths++;
   if(t<T){step(x,r,sx);step(y,r,sy);if((int)dec(x).size()+2*m!=(int)dec(y).size()&&firstgamma<0)firstgamma=t;}
  }
 }
 cout<<"GMP h="<<h<<" m="<<m<<" T="<<T<<" variants=361 paired_steps="<<paths<<" checked_cells="<<checked<<" firstfail="<<first<<" bad_gamma="<<firstgamma<<" bad_pal="<<firstpal<<"\n";
 mpz_clears(x,y,r,nullptr);return first>=0||firstgamma>=0||firstpal>=0;
}
