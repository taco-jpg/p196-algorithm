// N06 decimal p8 buffered exterior; exact ordinary digit-vector replay.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
constexpr int entrance[]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
constexpr int period[]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
constexpr int expected[8][8]={
 {17,8,17,8,17,8,17,8},{5,13,6,14,8,16,13,12},
 {0,5,11,8,17,16,14,9},{1,1,2,4,8,16,14,10},
 {13,5,10,3,6,14,10,6},{4,8,16,8,17,14,10,2},
 {14,9,18,16,13,12,6,7},{12,8,16,16,14,9,0,6}};
vector<uint8_t> seed_digits(int k,int mode){
  vector<int> half(begin(entrance),end(entrance));
  for(int j=0;j<k;++j)half.insert(half.end(),begin(period),end(period));
  int center[]={18,9,8,14,2,11,13,16};if(mode==1)for(int &v:center)v=0;
 if(mode==2){int w[]={17,3,1,13,17,11,14,3};copy(begin(w),end(w),begin(center));}
 half.insert(half.end(),begin(center),end(center));int h=half.size();vector<uint8_t> d(2*h);
  for(int i=0;i<h;++i){int lo=min(9,half[i]);d[i]=lo;d[2*h-1-i]=half[i]-lo;}
  return d;
}
string decimal(const vector<uint8_t>&d){
 string s;for(int i=int(d.size())-1;i>=0;--i)s+=char('0'+d[i]);return s;
}
uint64_t fnv(const vector<uint8_t>& d){uint64_t h=14695981039346656037ULL;
 for(int i=int(d.size())-1;i>=0;--i){h^=uint8_t('0'+d[i]);h*=1099511628211ULL;}
 return h;
}
uint64_t modval(const vector<uint8_t>&d){uint64_t v=0;
 for(int i=int(d.size())-1;i>=0;--i)v=(v*10+d[i])%1000000007ULL;return v;
}
int main(int argc,char**argv){
 if(argc<3){cerr<<"usage: buffered_prefix <seed|scan> L [T]\n";return 2;}
 string mode=argv[1];int L=stoi(argv[2]);
 if(L<0||L>100000){cerr<<"bad L\n";return 2;}
 auto d=seed_digits(L,argc>4?stoi(argv[4]):0);int n0=d.size();
 if(mode=="seed"){cout<<decimal(d)<<'\n';return 0;}
 if(mode!="scan"||argc<4){cerr<<"bad mode\n";return 2;}
 int T=stoi(argv[3]);vector<uint8_t> nxt;int firstfail=-1,firstpal=-1,gammafail=-1;
 for(int t=0;t<=T;++t){
   int n=d.size();bool eq=n>=16;
   for(int i=0;i<8&&eq;++i)if(int(d[i])+int(d[n-1-i])!=expected[i][t%8])eq=false;
   if(!eq&&firstfail==-1)firstfail=t;
   bool pal=true;for(int i=0;i<n/2;++i)if(d[i]!=d[n-1-i]){pal=false;break;}
   if(pal&&firstpal==-1)firstpal=t;
   if(t==T)break;
   nxt.resize(n);int carry=0;
   for(int i=0;i<n;++i){int a=d[i]+d[n-1-i]+carry;nxt[i]=a%10;carry=a/10;}
   if(carry!=(t%2==0)&&gammafail==-1)gammafail=t;
   if(carry)nxt.push_back(carry);
   d.swap(nxt);
 }
 cout<<"L="<<L<<" T="<<T<<" initial_digits="<<n0<<" final_digits="<<d.size()
   <<" first8_failure="<<firstfail<<" palindrome="<<firstpal
   <<" gamma_failure="<<gammafail<<" modulo1000000007="<<modval(d)
   <<" fnv64="<<fnv(d)<<"\n";
}