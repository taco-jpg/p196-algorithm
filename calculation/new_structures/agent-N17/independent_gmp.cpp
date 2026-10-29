// Independent large-integer checker: GMP mpz_set_str, mpz_add, mpz_get_str.
// g++ -O3 -std=c++17 independent_gmp.cpp -lgmp -o independent_gmp
// ./independent_gmp 8000 20000 samples.csv
#include <gmp.h>
#include <algorithm>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
const int pre[39]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
const int bulk[20]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
int coeff(const string &s,size_t i){return (s[i]-'0')+(s[s.size()-1-i]-'0');}
string build(int half){
 string low,high;low.reserve(half);high.reserve(half);
 for(int i=0;i<half;i++){int x=i<39?pre[i]:bulk[(i-39)%20];int down=x>9?x-9:0;
  low.push_back(char('0'+down));high.push_back(char('0'+x-down));}
 reverse(low.begin(),low.end());return high+low;
}
string repr(mpz_t x){size_t n=mpz_sizeinbase(x,10)+3;string s(n,'\0');
 mpz_get_str(s.data(),10,x);s.resize(strlen(s.c_str()));return s;}
int main(int argc,char**argv){
 int h=argc>1?atoi(argv[1]):8000,T=argc>2?atoi(argv[2]):20000;
 string csvpath=argc>3?argv[3]:"/dev/null";string seed=build(h);
 mpz_t x,r;mpz_inits(x,r,NULL);
 if(mpz_set_str(x,seed.c_str(),10)){cerr<<"bad seed";return 1;}
 vector<string> phases(8);long long checksum=0;int minfront=h,firstfail=-1,firstpal=-1,firstgamma=-1,firstperiod=-1;
 ofstream f(csvpath);f<<"t,len,front,odd_witness,gamma\n";
 for(int t=0;t<=T;t++){
  string s=repr(x);if(t<8)phases[t]=s;int n=s.size();
  bool ispal=true;for(int i=0;i<n/2;i++)if(s[i]!=s[n-1-i]){ispal=false;break;}
  if(ispal&&firstpal<0)firstpal=t;
  int front=min(n/2,h-50);
  if(t>=8){const string &ref=phases[t%8];for(int i=0;i<front;i++)
   if(coeff(s,i)!=coeff(ref,i)){front=i;break;}}
  minfront=min(minfront,front);
  int odd=-1;for(int i=0;i<min(front,39);i++)if(coeff(s,i)&1){odd=i;break;}
  if((odd<0||front<39)&&firstfail<0)firstfail=t;
  if(t<8)for(int i=39;i<h-80;i++)if(coeff(s,i)!=coeff(s,i+20)){firstperiod=t;break;}
  int gamma=0;if(t<T){string sr=s;reverse(sr.begin(),sr.end());
   mpz_set_str(r,sr.c_str(),10);mpz_add(x,x,r);
   gamma=((int)repr(x).size()>n);if(gamma!=(t%2==0)&&firstgamma<0)firstgamma=t;}
  if(t<16||t%1000==0||t==T)f<<t<<","<<n<<","<<front<<","<<odd<<","<<gamma<<"\n";
  checksum=(checksum*1000003LL+(odd+31)*13+front+gamma+1+t)%1000000007LL;
 }
 cerr<<"GMP: T="<<T<<" h="<<h<<" minfront="<<minfront<<" badroot="<<firstfail
     <<" palindrome="<<firstpal<<" badgamma="<<firstgamma<<" badperiod="<<firstperiod
     <<" checksum="<<checksum<<"\n";
 mpz_clears(x,r,NULL);
 return (firstfail<0&&firstpal<0&&firstgamma<0&&firstperiod<0)?0:1;
}