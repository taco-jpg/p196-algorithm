// Exact ordinary decimal replay of a triple hierarchy 8->7->5->3.
#define NESTED3_LIBRARY
#include "nested_three_fusion_probe.cpp"
#include <stdexcept>
static string init_num(int q,int R,int S,int D){
 int B=2*q+2*S+2*R+D,n=B+2;
 string s(n,'0');s[0]='8';s[1]='8';
 // 78*10^(q+S+R), 37*10^(q+S), 37*10^q, 75.
 int top=B+1;
 int ix=top-(q+S+R+1);s[ix]='7';s[ix+1]='8';
 ix=top-(q+S+1);s[ix]='3';s[ix+1]='7';
 ix=top-(q+1);s[ix]='3';s[ix+1]='7';
 s[n-2]='7';s[n-1]='5';return s;
}
static string add_reverse(const string&s){
 int n=(int)s.size(),cy=0;string t(n,'0');
 for(int j=n-1;j>=0;j--){int v=s[j]-'0'+s[n-1-j]-'0'+cy;t[j]='0'+v%10;cy=v/10;}
 if(cy)t.insert(t.begin(),'0'+cy);
 return t;
}
static bool is_palindrome(const string&s){for(size_t i=0;i<s.size()/2;i++)if(s[i]!=s[s.size()-i-1])return false;return true;}
static string exact_packet_word(const Dyn&x,int q,int R,int S,int D){
 vector<int> base;
 if(x.n==8)base={0,q,q+S,q+S+R,q+S+R+D,q+S+2*R+D,q+2*S+2*R+D,2*q+2*S+2*R+D};
 if(x.n==7)base={0,q,q+S,q+S+R,q+S+2*R+D,q+2*S+2*R+D,2*q+2*S+2*R+D};
 if(x.n==5)base={0,q,q+S,q+2*S+2*R+D,2*q+2*S+2*R+D};
 if(x.n==3)base={0,q,2*q+2*S+2*R+D};
 if((int)base.size()!=x.n)abort();
 int top=base.back()+x.p.back().end();
 vector<int> aggregate(top+1);
 for(int k=0;k<x.n;k++)for(int j=0;j<x.p[k].length();j++){
  int pos=base[k]+x.p[k].start+j;
  if(pos<0||pos>top)throw runtime_error("out of range exponent");
  aggregate[pos]+=x.p[k].d[j];
 }
 string s(top+1,'0');
 for(int j=0;j<=top;j++){
  if(aggregate[j]>=10)throw runtime_error("cross packet carry unnormalized");
  s[top-j]='0'+aggregate[j];
 }
 if(s[0]=='0')throw runtime_error("missing high digit");
 return s;
}
int main(int argc,char**argv){
 int T=argc>1?atoi(argv[1]):20000;
 int q=argc>2?atoi(argv[2]):12014;
 int R=argc>3?atoi(argv[3]):56;
 int S=argc>4?atoi(argv[4]):109;
 int D=4;Dyn x=initial8();
 string actual=init_num(q,R,S,D);
 uint64_t hash=1469598103934665603ULL;
 int Q=1,matched=0,nonpal=0,second=-1,third=-1;
 for(int t=0;t<=T;t++){
  if(t==13)x=fuse8to7(x,D);
  if(x.n==7&&contact7(x,R,D)){x=fuse7to5(x,R,D);second=t;}
  if(x.n==5&&contact5(x,S,R,D)){x=fuse5to3(x,S,R,D);third=t;}
  Q=max(Q,universal_q_nested(x,R,S,D));
  if(Q>q)throw runtime_error("parameter q exits protected region at t="+to_string(t));
  if(!nonpal_outer(x))throw runtime_error("outer nonpal witness disappears");
  string predicted=exact_packet_word(x,q,R,S,D);
  if(predicted!=actual)throw runtime_error("complete-digit mismatch at t="+to_string(t));
  if(is_palindrome(actual))throw runtime_error("real decimal palindrome");
  matched++;nonpal++;
  for(char v:actual){hash^=(unsigned char)v;hash*=1099511628211ULL;}
  if(t==0||t==4||t==13||t==14||t==87||t==88||t==89||t==175||t==176||t==177||t==264||t==1000||t==5000||t==10000||t==T)
     cout<<"t="<<t<<" digits="<<actual.length()<<" phase="<<x.n<<" qmin="<<Q<<" matched=1 nonpal=1\n";
  if(t<T){actual=add_reverse(actual);x=next_nested(x,R,S,D);}
 }
 cout<<"SUMMARY steps="<<T<<" q="<<q<<" R="<<R<<" S="<<S<<" matched="<<matched<<" nonpal="<<nonpal<<" qmin="<<Q<<" fuses="<<13<<","<<second<<","<<third<<" fnv64="<<hash<<"\n";
}
