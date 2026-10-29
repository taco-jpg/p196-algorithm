// Independent whole-decimal schoolbook replay vs 4-packet transparent initial
// crossing and the 3-packet canonical fused-centre continuation.
#define FUSED20K_LIBRARY
#include "fused_20k.cpp"
#include <stdexcept>
#include <sstream>

static string initial_digits(int q){
 const int n=2*q+D+2;
 string s(n,'0');
 s[0]='8';s[1]='8';
 s[q+D]='7';s[q+D+1]='8';
 s[n-2]='7';s[n-1]='5';
 return s;
}
static string ordinary_add_reverse(const string&s){
 int carry=0,n=(int)s.size();string t(n,'0');
 for(int i=n-1;i>=0;i--){
   int v=s[i]-'0'+s[n-i-1]-'0'+carry;
   t[i]='0'+v%10;carry=v/10;
 }
 if(carry)t.insert(t.begin(),'0'+carry);
 return t;
}
static bool ispal(const string&s){
 for(size_t i=0,n=s.size();i<n/2;i++)if(s[i]!=s[n-1-i])return false;
 return true;
}
static string aggregate4(const S&x,int q){
 int shift[4]={0,q,q+D,2*q+D};
 int top=shift[3]+x[3].end();
 vector<int> out(top+1,0);
 for(int k=0;k<4;k++)for(int j=0;j<x[k].length();j++){
   int pos=shift[k]+x[k].start+j;
   if(pos<0||pos>top)throw runtime_error("4-packet exponent out of range");
   out[pos]+=x[k].d[j];
 }
 string s(top+1,'0');
 for(int j=0;j<=top;j++){
   if(out[j]>=10)throw runtime_error("4-packet overlap overcapacity");
   s[top-j]='0'+out[j];
 }
 if(s[0]=='0')throw runtime_error("4-packet leading zero");
 return s;
}
static string aggregate3(const Three&x,int q){
 int shift[3]={0,q,2*q+D};
 const Packet* p[3]={&x.low,&x.mid,&x.high};
 int top=shift[2]+x.high.end();
 vector<int> out(top+1,0);
 for(int k=0;k<3;k++)for(int j=0;j<p[k]->length();j++){
   int pos=shift[k]+p[k]->start+j;
   if(pos<0||pos>top)throw runtime_error("3-packet exponent out of range");
   out[pos]+=p[k]->d[j];
 }
 string s(top+1,'0');
 for(int j=0;j<=top;j++){
   if(out[j]>=10)throw runtime_error("3-packet overlap overcapacity");
   s[top-j]='0'+out[j];
 }
 if(s[0]=='0')throw runtime_error("3-packet leading zero");
 return s;
}
static uint64_t hash_word(const string&s,uint64_t h){
 for(char c:s){h^=(unsigned char)c;h*=1099511628211ULL;}
 return h;
}
int main(int argc,char**argv){
 int T=argc>1?atoi(argv[1]):20000;
 int q=argc>2?atoi(argv[2]):12002;
 if(T<13||q<11)throw runtime_error("T>=13 and q>=11 required");
 string actual=initial_digits(q);
 S f;f[0]={0,{5,7}};f[1]={0,{8,7}};f[2]={};f[3]={0,{8,8}};
 Three x;
 int matched=0,nonpal=0,Q=11;
 uint64_t digest=1469598103934665603ULL;
 for(int t=0;t<=T;t++){
   if(t==13){x={f[0],fuse(f[1],f[2]),f[3]};}
   string predicted=t<13?aggregate4(f,q):aggregate3(x,q);
   if(predicted!=actual)throw runtime_error("full-digit mismatch at state "+to_string(t));
   if(ispal(actual))throw runtime_error("unexpected actual palindrome at state "+to_string(t));
   matched++;nonpal++;digest=hash_word(actual,digest);
   if(t>=13){Q=max(Q,universal_qmin(x));if(!nonpal_outer(x))throw runtime_error("outer witness fails");}
   if(t==0||t==4||t==13||t==14||t==88||t==264||t==1000||t==5000||t==10000||t==T)
      cout<<"t="<<t<<" digits="<<actual.size()<<" qmin="<<Q<<" full_word_match=1 nonpal=1\n";
   if(t<T){
      actual=ordinary_add_reverse(actual);
      if(t<13)f=evolve(f);
      else x=next(x);
   }
 }
 cout<<"SUMMARY steps="<<T<<" q="<<q<<" matched="<<matched<<" nonpal="<<nonpal<<" bound="<<Q<<" fnv64="<<digest<<"\n";
 if(Q>q)throw runtime_error("universal q bound exceeds chosen q");
}
