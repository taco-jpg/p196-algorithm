// Independent ordinary decimal digit-vector 20,000-step replay for W23.
// g++ -O3 -std=c++17 digit_replay.cpp -o /tmp/w23_digit && /tmp/w23_digit 100 20000
#include <vector>
#include <iostream>
#include <cassert>
#include <cstdint>
#include <iomanip>
#include <algorithm>
using namespace std;using V=vector<int>;
const V B={17,5,0,2,1,9,15,18,14,9,3};
const V W={4,4,14,1,5,11,7,1,15,12,7,9,9,12,14,4,0,6,5,17,13,9,7,3,13,10,4,13,5,1,9,4,11,6,16,3,7,7,12,4,2,13,2,15,10,10,9,3};
const int root[8][8]={{17,8,17,8,17,8,17,8},{5,13,6,14,8,16,13,12},
{0,5,11,8,17,16,14,9},{2,2,4,6,13,12,5,10},
{1,3,7,11,2,6,14,10},{9,11,2,9,9,12,4,9},
{15,5,12,5,11,1,3,7},{18,15,11,5,10,3,6,9}};
V seed(int q,int mask){
 V h=B;for(int i=0;i<q;i++)h.insert(h.end(),W.begin(),W.end());
 h.insert(h.end(),{10,14,1,10});
 for(int j=0;j<5;j++)if(mask>>j&1){
  int pos=11+48*(2+6*j)+20;assert(h[pos]==13 && h[pos+1]==9);h[pos]=8;h[pos+1]=5;
 }
 int n=2*(int)h.size()-1;V d(n);
 for(int i=0;i<(int)h.size()-1;i++){int p=h[i];d[i]=max(0,p-9);d[n-1-i]=min(9,p);}
 d[h.size()-1]=5;assert(d.back());return d;
}
int next(V&d){int c=0,n=d.size();V z;z.reserve(n+1);
 for(int i=0;i<n;i++){int s=d[i]+d[n-1-i]+c;z.push_back(s%10);c=s/10;}
 if(c)z.push_back(c);d.swap(z);return c;}
bool pal(const V&d){for(int i=0,j=(int)d.size()-1;i<j;i++,j--)
 if(d[i]!=d[j])return false;return true;}
uint64_t fnv(const V&d){uint64_t h=1469598103934665603ULL;
 for(int x:d){h^=uint64_t(x);h*=1099511628211ULL;}return h;}
int main(int argc,char**argv){
 int q=argc>1?stoi(argv[1]):100,T=argc>2?stoi(argv[2]):20000;assert(q>=29);
 V a=seed(q,0),b=seed(q,31);int join=-1,rootbad=-1,clockbad=-1,palbad=-1,gammas=0;
 for(int t=0;t<=T;t++){
  if(pal(a)||pal(b)){palbad=t;break;}
  for(int i=0;i<8;i++)if(a[i]+a[a.size()-1-i]!=root[i][t%8] &&rootbad<0)rootbad=t;
  if(t<=4 &&a==b &&join<0)join=t;
  if(t==T)break;
  int g=next(a),h=next(b);gammas+=g;
  if(g!=(1-t%2)&&clockbad<0)clockbad=t;
  if(g!=h ||(t>=4&&a!=b))return 7;
 }
 cout<<"q="<<q<<" steps="<<T<<" join="<<join<<" root_bad="<<rootbad
 <<" clock_bad="<<clockbad<<" first_pal="<<palbad<<" overflows="<<gammas
 <<" digits="<<a.size()<<" fnv="<<hex<<fnv(a)<<dec<<"\n";
 return join==4&&rootbad<0&&clockbad<0&&palbad<0&&
        (T!=20000||(a.size()==19629&&fnv(a)==0x971e60282dc35bc9ULL))?0:8;
}