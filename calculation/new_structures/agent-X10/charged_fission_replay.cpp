// Independent whole-decimal replay of charged complementary-band fission.
// g++ -std=c++17 -O3 charged_fission_replay.cpp -o charged_fission_replay
// ./charged_fission_replay 20000 5976 88 49 4
// This file intentionally uses ordinary decimal schoolbook arithmetic for the
// actual orbit, not the packet recurrence. The latter serves as a full-word oracle.
#define COMPLEMENT_FRONT_LIBRARY
#include "complement_front_probe.cpp"
#include <stdexcept>
#include <cstdint>

static string add_reverse(const string &s){
 int c=0,n=(int)s.size();string out(n,'0');
 for(int j=n-1;j>=0;--j){
  int v=(s[j]-'0')+(s[n-1-j]-'0')+c;
  out[j]='0'+v%10;c=v/10;
 }
 if(c)out.insert(out.begin(),'0'+c);
 return out;
}
static bool palword(const string&s){for(size_t i=0;i<s.size()/2;++i)if(s[i]!=s[s.size()-1-i])return false;return true;}
static string charged_seed(int R,int u,int v,int a){
 return to_string(u)+string(R,char('0'+a))+string(R,char('0'+9-a))+to_string(v);
}
static string oracle_word(const Two&x,int M){
 int top=M+x.hi.end();if(top<0)throw runtime_error("negative top");
 vector<int> d(top+1,0);
 for(int j=0;j<x.lo.length();j++){
  int e=x.lo.start+j;if(e<0||e>top)throw runtime_error("low packet out of range");
  d[e]+=x.lo.d[j];
 }
 for(int j=0;j<x.hi.length();j++){
  int e=M+x.hi.start+j;if(e<0||e>top)throw runtime_error("high packet out of range");
  d[e]+=x.hi.d[j];
 }
 string s(top+1,'0');
 for(int e=0;e<=top;e++){
  if(d[e]<0||d[e]>=10)throw runtime_error("packet overlap carry");
  s[top-e]='0'+d[e];
 }
 if(s[0]=='0')throw runtime_error("leading zero in oracle");
 return s;
}
static Packet packet(int n){
 Packet p;while(n>0){p.d.push_back(n%10);n/=10;}return p;
}
int main(int argc,char**argv){
 const int T=argc>1?atoi(argv[1]):20000;
 const int R=argc>2?atoi(argv[2]):5976;
 const int u=argc>3?atoi(argv[3]):88;
 const int v=argc>4?atoi(argv[4]):49;
 const int a=argc>5?atoi(argv[5]):4;
 if(T<0||R<=0||u<10||u>99||v<10||v>99||a<0||a>9)throw runtime_error("invalid input");
 const int A=u/10,B=u%10,C=v/10,D=v%10,s=A+D,t=B+C+1;
 if(s<10||t<10)throw runtime_error("fission precondition not satisfied");
 const int H=100+10*(s-9)+(t-10),L=10*(t-10)+(s-10),M=2*R+2;
 if(H>=1000||L>=100)throw runtime_error("out-of-format boundary digit");
 string charged=charged_seed(R,u,v,a);
 if(palword(charged))throw runtime_error("charged starting seed palindrome");
 string real=add_reverse(charged);
 string fission=to_string(H)+string(2*R,'0')+string(1,'0'+L/10)+string(1,'0'+L%10);
 if(real!=fission)throw runtime_error("one-step complementary-band fission identity false");
 Two x={packet(L),packet(H)};
 int Q=1,matched=0,nonpal=1;uint64_t hash=1469598103934665603ULL;
 cout<<"charged t=0 len="<<charged.size()<<" nonpal=1 H="<<H<<" L="<<L<<" R="<<R<<" u="<<u<<" v="<<v<<" a="<<a<<"\n";
 for(int k=0;k<=T;k++){
  if(x.lo.start<0)throw runtime_error("low packet runs off edge");
  Q=max(Q,1+x.lo.end()-x.hi.start);
  Q=max(Q,-x.hi.start);
  if(M<Q)throw runtime_error("gap guard fails at k="+to_string(k)+" required="+to_string(Q));
  string prediction=oracle_word(x,M);
  if(real!=prediction)throw runtime_error("independent whole-decimal mismatch at k="+to_string(k));
  if(palword(real))throw runtime_error("actual decimal palindrome at k="+to_string(k));
  matched++;nonpal++;
  for(char c:real){hash^=(uint8_t)c;hash*=1099511628211ULL;}
  if(k==0||k==4||k==13||k==88||k==176||k==264||k==1000||k==5000||k==10000||k==T)
    cout<<"t="<<(k+1)<<" digits="<<real.size()<<" required_M="<<Q<<" whole_word_match=1 nonpal=1\n";
  if(k<T){real=add_reverse(real);x=next2(x);}
 }
 cout<<"SUMMARY steps_after_fission="<<T<<" charged_steps="<<(T+1)<<" all_nonpal_states="<<nonpal<<" actual_word_matches="<<matched<<" H="<<H<<" L="<<L<<" R="<<R<<" M="<<M<<" universal_Q="<<Q<<" initial_len="<<charged.size()<<" final_len="<<real.size()<<" fnv64="<<hash<<"\n";
}
