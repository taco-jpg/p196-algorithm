// Agent-X23: distributed 3-site decimal kink crystal; finite-horizon replay only.
// g++ -O3 -std=c++17 crystal18.cpp -lgmpxx -lgmp -o crystal18
// ./crystal18 400 5000 20000
#include <array>
#include <vector>
#include <string>
#include <algorithm>
#include <cassert>
#include <iostream>
#include <gmpxx.h>
using namespace std;
using V=vector<unsigned char>;using R=array<int,3>;
const int B[39]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
const int W[20]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
V step(const V& p){V d,n;d.reserve(p.size()+1);int c=0;for(int a:p){int z=a+c;d.push_back(z%10);c=z/10;}if(c)d.push_back(c);n.resize(d.size());for(size_t i=0;i<d.size();i++)n[i]=d[i]+d[d.size()-1-i];return n;}
R digits(R v,bool forward){for(int init=0;init<2;init++){int c=init;R d{};for(int k=0;k<3;k++){int i=forward?k:2-k,z=v[i]+c;d[i]=z%10;c=z/10;}if(c==init)return d;}abort();}
R advance(R v,int g){R lo=digits(v,true),hi=digits(v,false),n{};for(int i=0;i<3;i++)n[i]=lo[i]+hi[(i+3-g)%3];return n;}
string decimal(const mpz_class &v){size_t z=mpz_sizeinbase(v.get_mpz_t(),10)+3;string s(z,'\0');mpz_get_str(s.data(),10,v.get_mpz_t());s.resize(s.find('\0'));return s;}
int main(int argc,char**argv){
 int q=argc>1?atoi(argv[1]):400,r=argc>2?atoi(argv[2]):5000,T=argc>3?atoi(argv[3]):20000;
 if(q<1||r<1||T<18){cerr<<"invalid arguments\n";return 1;}
 V half,p;for(int x:B)half.push_back(x);for(int k=0;k<q;k++)for(int x:W)half.push_back(x);for(int k=0;k<r;k++)for(int x:{8,6,8})half.push_back(x);
 p=half;for(auto it=half.rbegin();it!=half.rend();++it)p.push_back(*it);
 string s(p.size(),'0');for(size_t i=0;i<p.size()/2;i++){int x=p[i],hi=min(x,9),lo=x-hi;s[i]=char('0'+hi);s[s.size()-1-i]=char('0'+lo);}mpz_class N;if(mpz_set_str(N.get_mpz_t(),s.c_str(),10))abort();
 R ring{8,6,8};vector<R> rclock;array<array<int,39>,8> bp{};array<array<int,20>,8> wp{};
 int minW=INT_MAX,minR=INT_MAX;const int start=39+20*q;
 for(int t=0;t<=T;t++){
  int len=(int)p.size(),h=(len+1)/2;if((int)s.size()!=len){cerr<<"length mismatch at "<<t<<"\n";return 2;}
  for(int i=0;i<len;i++)if(p[i]!=(s[i]-'0')+(s[len-1-i]-'0')){cerr<<"GMP mismatch at "<<t<<" "<<i<<"\n";return 3;}
  if(equal(s.begin(),s.end(),s.rbegin())){cerr<<"palindrome at "<<t<<"\n";return 4;}
  if(t<8){for(int i=0;i<39;i++)bp[t][i]=p[i];for(int i=0;i<20;i++)wp[t][i]=p[39+i];}
  for(int i=0;i<39;i++)if(p[i]!=bp[t%8][i]){cerr<<"B clock failure "<<t<<"\n";return 5;}
  int nm=0;for(int i=39;i<h&&p[i]==wp[t%8][(i-39)%20];i++)nm++;
  int nr=0;for(int i=h-1;i>=start&&p[i]==ring[(i-start)%3];i--)nr++;
  if(nm<200||nr<100){cerr<<"bulk guard exhausted at "<<t<<" W="<<nm<<" R="<<nr<<"\n";return 6;}
  minW=min(minW,nm);minR=min(minR,nr);
  if(t%1000==0||t==T)cout<<t<<","<<len<<","<<nm<<","<<nr<<","<<ring[0]<<","<<ring[1]<<","<<ring[2]<<"\n";
  if(t==T)break;
  rclock.push_back(ring);V next=step(p);int g=(int)next.size()-len;
  if(g!=(1-t%2)){cerr<<"overflow failure at "<<t<<"\n";return 7;}
  string reversed(s.rbegin(),s.rend());mpz_class Vrev;if(mpz_set_str(Vrev.get_mpz_t(),reversed.c_str(),10))abort();N+=Vrev;s=decimal(N);
  ring=advance(ring,g);p.swap(next);
 }
 bool p18=true,smaller=false;for(int i=11;i+18<(int)rclock.size();i++)if(rclock[i]!=rclock[i+18])p18=false;
 for(int period:{2,6}){bool all=true;for(int i=11;i+period<(int)rclock.size();i++)if(rclock[i]!=rclock[i+period])all=false;if(all)smaller=true;}
 if(!p18||smaller){cerr<<"18-cycle mismatch\n";return 8;}
 cout<<"SUCCESS,minimum_W="<<minW<<",minimum_crystal="<<minR<<",period=18,not_infinite_certificate\n";
}
