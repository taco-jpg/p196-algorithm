// Constructive decimal zero-shield family. For L neutral 9 pair-coefficients
// sandwiched between 11s, the literal next pairword has a zero strip of
// length >= L-2, and a substrip of >= L-2t zeros after t total steps.
// Full digit-vector replay checks that strip at EVERY requested step.
#include <bits/stdc++.h>
using namespace std;using ull=unsigned long long;
static int advance(vector<uint8_t>&d,vector<uint8_t>&o){int n=d.size(),c=0;o.resize(n+1);for(int i=0;i<n;i++){int sum=d[i]+d[n-i-1]+c;o[i]=sum%10;c=sum/10;}o[n]=c;d.swap(o);d.resize(n+(c!=0));return c;}
static bool pal(const vector<uint8_t>&d){for(size_t i=0;i<d.size()/2;i++)if(d[i]!=d[d.size()-1-i])return false;return true;}
static uint64_t hashd(const vector<uint8_t>&d){uint64_t h=1469598103934665603ull;for(auto x:d){h^=x;h*=1099511628211ull;}return h;}
int main(int argc,char**argv){if(argc<3){cerr<<"usage: bubble_family L STEPS [CHECKPOINT_EVERY=1000]\n";return 2;}int L=atoi(argv[1]),N=atoi(argv[2]),E=argc>3?atoi(argv[3]):1000;if(L<5||N<1||2*N+2>=L){cerr<<"require L>=2*steps+3\n";return 2;}int a0=65,b0=a0+L-1,m=L+130,n=2*m;
 vector<uint8_t>d(n),o;uint32_t state=196u;
 for(int i=0;i<m;i++){
  int p;
  if(i==64||i==L+65) p=11;
  else if(i>=a0&&i<=b0) p=9;
  else {state^=state<<13;state^=state>>17;state^=state<<5;p=state%19;}
  if(i==0)p=12;
  d[i]=max(0,p-9);d[n-1-i]=min(9,p);
 }
 int palhits=0,checkcount=0,gam=0;
 for(int t=0;t<=N;t++){
  if(pal(d)){palhits++;cerr<<"PAL t="<<t<<"\n";return 3;}
  if(t>=1){int a=a0+t,b=b0-t;if(b<a){cerr<<"core exhausted t="<<t<<"\n";return 4;}for(int i=a;i<=b;i++){int p=d[i]+d[d.size()-1-i];if(p!=0){cerr<<"ZERO SHIELD BROKEN step="<<t<<" i="<<i<<" P="<<p<<"\n";return 5;}}checkcount++;}
  if(t%E==0||t==N)cout<<"t="<<t<<" length="<<d.size()<<" gamma="<<gam<<" zero_guaranteed="<<(t?L-2*t:0)<<" hash="<<hex<<hashd(d)<<dec<<"\n";
  if(t==N)break;
  gam=advance(d,o);
 }
 cout<<"PASS L="<<L<<" steps="<<N<<" no_pal="<<N+1<<" shield_checks="<<checkcount<<" final_digits="<<d.size()<<"\n";
}
