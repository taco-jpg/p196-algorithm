// Agent W30: phase-40 odd five-site pairword carrier inside canonical p8 exterior.
// Three independent complete engines: coefficient normalization, ordinary decimal digits,
// and base-1e9 arbitrary-precision integer; optional independent GMP control.
// Usage: ./replay [qExterior=300] [kIsland=4200] [steps=20000] [checkpoint_interval=1000]
#ifdef W30_GMP
#include <gmpxx.h>
#endif
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <vector>
#include <string>
using namespace std;
using Word=vector<uint8_t>;
static const int bb[]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static const int ww[]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
static const int vv[]={17,3,14,3,17};
[[noreturn]] void bad(string s){cerr<<"FAILED: "<<s<<"\n";exit(2);}
Word make_P(int q,int k){Word L;for(int v:bb)L.push_back(v);for(int r=0;r<q;r++)for(int v:ww)L.push_back(v);Word P=L;for(int r=0;r<2*k;r++)for(int v:vv)P.push_back(v);for(auto it=L.rbegin();it!=L.rend();it++)P.push_back(*it);return P;}
Word realize(Word const &P){int n=P.size();if(n%2)bad("even-length required");Word d(n);for(int i=0;i<n/2;i++){int p=P[i];int low=max(0,p-9),high=p-low;d[i]=low;d[n-1-i]=high;}if(!d.back())bad("noncanonical seed");return d;}
Word pairs(Word const &d){Word P(d.size());for(int i=0;i<d.size();i++)P[i]=d[i]+d[d.size()-1-i];return P;}
// independent exact pairword stepping; input P is palindromic by construction
pair<Word,int> pair_step(Word const &P){Word d;d.reserve(P.size()+1);int carry=0;for(int v:P){int s=v+carry;d.push_back(s%10);carry=s/10;}if(carry)d.push_back(carry);return {pairs(d),carry};}
// independent ordinary decimal digit-addition, unlike pair_step no pair coefficients used
pair<Word,int> digit_step(Word const &d){Word o;int c=0;int n=d.size();o.reserve(n+1);for(int i=0;i<n;i++){int v=d[i]+d[n-1-i]+c;o.push_back(v%10);c=v/10;}if(c)o.push_back(c);return {move(o),c};}
string tostr(Word const &d){string s;s.reserve(d.size());for(auto it=d.rbegin();it!=d.rend();it++)s.push_back('0'+*it);return s;}
string summary(Word const&d){uint64_t h=1469598103934665603ULL;for(auto v:d){h^=v;h*=1099511628211ULL;}ostringstream o;o<<hex<<setw(16)<<setfill('0')<<h;return o.str();}
vector<Word> cycle(){Word x(begin(vv),end(vv));vector<Word> a;for(int t=0;t<40;t++){for(auto v:x)if(v==9)bad("9 in odd carrier");int odd=0;for(auto v:x)odd+=(v%2);if(!odd)bad("no odd in carrier");a.push_back(x);Word y(5);int g=(t%2==0);for(int i=0;i<5;i++){int v=x[i],l=x[(i+4)%5],r=x[(i+1)%5];int h=v>=10,hl=l>=10,hr=r>=10;int z=g?(v-9*h+l-9*hl):(2*v+hl+hr-20*h);if(z<0||z>18)bad("range");y[i]=z;}x=y;}if(x!=a[0])bad("no 40-cycle");return a;}
// Independent base-1e9 arbitrary-precision integer; all reversing and addition use its limbs,
// never the paired-coefficient or ordinary decimal digit-addition engines.
struct Big9{
 static constexpr uint32_t BASE=1000000000U;
 vector<uint32_t> limbs;
 explicit Big9(const string &s){for(int e=(int)s.size();e>0;e-=9){int st=max(0,e-9);uint32_t v=0;for(int j=st;j<e;j++)v=10*v+(s[j]-'0');limbs.push_back(v);}trim();}
 void trim(){while(limbs.size()>1&&limbs.back()==0)limbs.pop_back();}
 string digits() const{string out=to_string(limbs.back());char buf[10];for(int i=(int)limbs.size()-2;i>=0;i--){uint32_t v=limbs[i];for(int k=8;k>=0;k--){buf[k]=char('0'+(v%10));v/=10;}out.append(buf,9);}return out;}
 Big9& operator+=(const Big9 &other){size_t n=max(limbs.size(),other.limbs.size());limbs.resize(n,0);uint64_t carry=0;for(size_t i=0;i<n;i++){uint64_t s=carry+limbs[i]+(i<other.limbs.size()?other.limbs[i]:0);limbs[i]=s%BASE;carry=s/BASE;}if(carry)limbs.push_back((uint32_t)carry);return *this;}
};
int main(int argc,char** argv){int q=argc>1?atoi(argv[1]):300,k=argc>2?atoi(argv[2]):4200,T=argc>3?atoi(argv[3]):20000,interval=argc>4?atoi(argv[4]):1000;auto rows=cycle();Word P=make_P(q,k),d=realize(P);int idx=39+20*q;const int end=idx+10*k;bool enough=(idx+T+3<end-T-3);if(!enough)bad("empty guarded island");if(pairs(d)!=P)bad("seed realization");Big9 N(tostr(d));
#ifdef W30_GMP
mpz_class GMP_N(tostr(d),10);
#endif
int odd=0,gammaCount=0;cout<<"start n="<<d.size()<<" q="<<q<<" k="<<k<<" T="<<T<<" initial="<<summary(d)<<"\n";
for(int t=0;t<=T;t++){
  // Compare EVERY coefficient in a two-sided light-cone-protected island, every time.
  int lo=idx+t+2,hi=end-t-2;if(lo>=hi)bad("guard depleted");int mismatches=0,oddProtected=0;for(int j=lo;j<hi;j++){int expect=rows[t%40][(j-idx)%5];if(P[j]!=expect)mismatches++;if(P[j]%2)oddProtected++;}
  if(mismatches)bad("island carrier shape t="+to_string(t)+" bad="+to_string(mismatches));
  if(!oddProtected)bad("no guarded odd witness at t="+to_string(t));
  // Full arithmetic check: GMP big integer -> exact decimal string, compare ALL digits.
  string s=N.digits();if(s!=tostr(d))bad("bigint mismatch at t="+to_string(t));
#ifdef W30_GMP
if(s!=GMP_N.get_str(10))bad("GMP mismatch at t="+to_string(t));
#endif
  if(pairs(d)!=P)bad("full pairword mismatch t="+to_string(t));
  if(equal(d.begin(),d.begin()+d.size()/2,d.rbegin()))bad("palindrome t="+to_string(t));
  odd++;
  if(t%interval==0||t==T){cout<<"CHECK t="<<t<<" len="<<d.size()<<" guard="<<(hi-lo)<<" odd="<<oddProtected<<" gammaSoFar="<<gammaCount<<" digitsFNV64="<<summary(d)<<"\n"<<flush;}
  if(t==T)break;
  // GMP independent arithmetic based on the integer's canonical digits
  reverse(s.begin(),s.end());Big9 R(s);N+=R;
#ifdef W30_GMP
string g_str=GMP_N.get_str(10);reverse(g_str.begin(),g_str.end());mpz_class GR(g_str,10);GMP_N+=GR;
#endif
  auto [nextD,g]=digit_step(d);auto [nextP,g2]=pair_step(P);if(g!=g2)bad("carry disagreement");if(g!=(t%2==0))bad("overflow schedule t="+to_string(t));gammaCount+=g;
  P.swap(nextP);d.swap(nextD);
}
cout<<"PASS "<<T<<" independent base-1e9 bigint and decimal-digit steps, phase-40 five-site carrier, full pairword every step, zero palindromes\n";
}
