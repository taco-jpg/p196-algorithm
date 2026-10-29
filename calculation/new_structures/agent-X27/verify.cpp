// Agent X27: independent literal-digit + GMP decimal reverse/add,
// exact parity carry identities, and fixed-boundary parity witness.
// Usage: c++ -std=c++17 -O3 verify.cpp -lgmpxx -lgmp -o verify && ./verify 47 20000
#include <gmpxx.h>
#include <bits/stdc++.h>
using namespace std;
uint64_t hash_digits(const vector<uint8_t>& d){uint64_t h=1469598103934665603ULL;for(uint8_t x:d){h^=x;h*=1099511628211ULL;}return h;}
string dec(const vector<uint8_t>& d){string s; s.reserve(d.size());for(auto i=d.rbegin();i!=d.rend();++i)s.push_back('0'+*i);return s;}
int main(int argc,char**argv){int Q=argc>1?atoi(argv[1]):47, T=argc>2?atoi(argv[2]):20000;int K=argc>3?atoi(argv[3]):16;
 if(Q<0||T<0||T>2000000){cerr<<"invalid argument\n";return 2;}
 vector<uint8_t>d;d.push_back(6);d.insert(d.end(),2*Q,9);d.push_back(1);
 mpz_class g(dec(d)); long long ov=0,oddLen=0,evenLen=0,midOdd=0,noOddGlobal=0;
 int maxFirstOdd=0, minLength=INT_MAX, maxLength=0, maxMid18run=0;
 uint64_t trace=1469598103934665603ULL;
 const int checkpoints[]={0,1,2,7,8,47,100,1000,5000,10000,15000,20000,30000,50000,100000};set<int> marks(begin(checkpoints),end(checkpoints));
 for(int t=0;t<=T;t++){
  int n=(int)d.size();string s=dec(d);
  string gs=g.get_str(10);
  if(s!=gs){cerr<<"ENGINE MISMATCH at t="<<t<<"\n";return 3;}
  int firstOdd=-1;bool allEven=true;bool pal=true;
  for(int i=0;i<n/2;i++){
    int p=d[i]+d[n-1-i];
    if(p&1){if(firstOdd<0)firstOdd=i;allEven=false;}
    if(d[i]!=d[n-1-i])pal=false;
  }
  if(pal){cerr<<"PAL at t="<<t<<"\n";return 4;}
  if(firstOdd<0||firstOdd>=K){cerr<<"NO PARITY BEACON t="<<t<<" n="<<n<<" odd_at="<<firstOdd<<"\n";return 5;}
  if(allEven)noOddGlobal++;
  maxFirstOdd=max(maxFirstOdd,firstOdd);minLength=min(minLength,n);maxLength=max(maxLength,n);
  if(n&1)oddLen++;else evenLen++;
  if((n%2)==0 && ((d[n/2-1]+d[n/2])&1))midOdd++;
  trace^=(uint64_t)(firstOdd+31*t+((uint64_t)n<<12));trace*=1099511628211ULL;
  if(marks.count(t))cout<<"CHECK t="<<t<<" n="<<n<<" firstOdd="<<firstOdd<<" hash="<<hex<<hash_digits(d)<<dec<<" mod1e9+7="<<mpz_class(g % 1000000007).get_ui()<<"\n";
  if(t==T)break;
  vector<int> p(n),c(n+1);vector<uint8_t>e(n);c[0]=0;
  for(int i=0;i<n;i++){p[i]=d[i]+d[n-1-i];int x=p[i]+c[i];e[i]=x%10;c[i+1]=x/10;}
  int gam=c[n];vector<uint8_t>out=e;if(gam){out.push_back(1);ov++;}
  // Exact pairword / two-sided carry parity identities for EVERY mirrored column.
  int nn=out.size();
  for(int i=0;i<nn/2;i++){
   int actual=(out[i]+out[nn-1-i])&1, formula;
   if(gam==0)formula=(c[i]+c[n-1-i])&1;
   else if(i==0)formula=(p[0]+1)&1;
   else formula=(p[i]+p[i-1]+c[i]+c[n-i])&1;
   if(actual!=formula){cerr<<"PARITY IDENTITY FAIL at t="<<t<<" i="<<i<<" gamma="<<gam<<"\n";return 6;}
  }
  // Core-independent k-prefix transducer (physical high-side carry input).
  // This is a stronger check than the parity identity: full P' digits agree.
  int kk=min(K,n/2);vector<int> hi(kk);
  hi[kk-1]=c[n-kk];
  for(int j=kk-1;j>0;j--)hi[j-1]=(p[j]+hi[j])/10;
  int pgam=(p[0]+hi[0])/10;
  if(pgam!=gam){cerr<<"PREFIX OVERFLOW MISMATCH t="<<t<<"\n";return 8;}
  for(int j=0;j<kk;j++){
    int predicted=gam==0 ? (p[j]+c[j])%10 + (p[j]+hi[j])%10
       : (j==0 ? (p[0]+c[0])%10 + 1
                    : (p[j]+c[j])%10 + (p[j-1]+hi[j-1])%10);
    if(predicted!=int(out[j])+out[nn-1-j]){
      cerr<<"PREFIX TRANSITION MISMATCH t="<<t<<" j="<<j<<"\n";return 9;
    }
  }
  string r=gs;reverse(r.begin(),r.end());mpz_class grev(r,10),newg=g+grev;
  if((int)out.size()!=int(newg.get_str(10).size())){cerr<<"OVERFLOW ENGINE MISMATCH at t="<<t<<"\n";return 7;}
  d.swap(out);g.swap(newg);
 }
 cout<<"SUMMARY Q="<<Q<<" T="<<T<<" initialDigits="<<2*Q+2<<" finalDigits="<<d.size()<<" overflow="<<ov<<" oddLenStates="<<oddLen<<" evenLenStates="<<evenLen<<" maxFirstOdd="<<maxFirstOdd<<" noOddGlobal="<<noOddGlobal<<" middleOddEvenN="<<midOdd<<" trace="<<hex<<trace<<dec<<"\n";
 return 0;
}
