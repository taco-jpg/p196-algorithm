// Independent real decimal whole-digit replay for two-level inner carry fusion
// six packets -> five at state13 -> three at state94.
#define HIERARCHY_LIBRARY
#include "hierarchical_fusion_probe.cpp"
#include <stdexcept>

static string seed(int q,int R,int D){
 int n=2*q+2*R+D+2;
 string s(n,'0');
 s[0]='8';s[1]='8';
 s[q+R+D]='7';s[q+R+D+1]='8';
 s[q+2*R+D]='3';s[q+2*R+D+1]='7';
 s[n-2]='7';s[n-1]='5';
 return s;
}
static string addrev(const string&s){
 int n=(int)s.size(),carry=0;string r(n,'0');
 for(int j=n-1;j>=0;j--){
  int a=s[j]-'0'+s[n-1-j]-'0'+carry;
  r[j]='0'+a%10;carry=a/10;
 }
 if(carry)r.insert(r.begin(),'0'+carry);
 return r;
}
static bool ispal(const string&s){
 for(size_t i=0;i<s.size()/2;i++)if(s[i]!=s[s.size()-i-1])return false;
 return true;
}
static string expected(const Dyn&x,int q,int R,int D){
 vector<int> bases;
 if(x.n==6)bases={0,q,q+R,q+R+D,q+2*R+D,2*q+2*R+D};
 if(x.n==5)bases={0,q,q+R,q+2*R+D,2*q+2*R+D};
 if(x.n==3)bases={0,q,2*q+2*R+D};
 if((int)bases.size()!=x.n)abort();
 int top=bases.back()+x.p.back().end();
 vector<int> v(top+1);
 for(int i=0;i<x.n;i++)for(int j=0;j<x.p[i].length();j++){
  int e=bases[i]+x.p[i].start+j;
  if(e<0||e>top)throw runtime_error("packet exponent outside numeral");
  v[e]+=x.p[i].d[j];
 }
 string s(top+1,'0');
 for(int e=0;e<=top;e++){
  if(v[e]>=10)throw runtime_error("aggregate digit exceeds base");
  s[top-e]='0'+v[e];
 }
 if(s[0]=='0')throw runtime_error("leading zero");
 return s;
}
int main(int argc,char**argv){
 int T=argc>1?atoi(argv[1]):20000;
 int q=argc>2?atoi(argv[2]):11989;
 int R=argc>3?atoi(argv[3]):60;
 int D=4;
 Dyn x=initial();string real=seed(q,R,D);
 uint64_t h=1469598103934665603ULL;
 int Q=1, matched=0,nonpal=0, second=-1;
 for(int t=0;t<=T;t++){
  if(t==13)x=fuse1(x,D);
  if(x.n==5&&side_contact(x,R,D)){
   if(second>=0)throw runtime_error("duplicate fusion");
   x=fuse2(x,R,D);second=t;
  }
  Q=max(Q,universal_q(x,R,D));
  if(q<Q)throw runtime_error("q outside proven chamber at time "+to_string(t));
  if(!nonpal_outer(x))throw runtime_error("outer nonpal witness failed");
  auto guess=expected(x,q,R,D);
  if(guess!=real)throw runtime_error("full digit mismatch at t="+to_string(t));
  if(ispal(real))throw runtime_error("real decimal palindrome at t="+to_string(t));
  for(char c:real){h^=(unsigned char)c;h*=1099511628211ULL;}
  matched++;nonpal++;
  if(t==0||t==4||t==13||t==14||t==93||t==94||t==95||t==88||t==264||t==1000||t==5000||t==10000||t==T)
   cout<<"t="<<t<<" digits="<<real.length()<<" n="<<x.n<<" qmin="<<Q<<" shape=1 nonpal=1\n";
  if(t<T){real=addrev(real);x=evolve_mode(x,R,D);}
 }
 cout<<"SUMMARY steps="<<T<<" q="<<q<<" R="<<R<<" matched="<<matched<<" nonpal="<<nonpal<<" required_q="<<Q<<" fuse2_t="<<second<<" fnv64="<<h<<"\n";
}
