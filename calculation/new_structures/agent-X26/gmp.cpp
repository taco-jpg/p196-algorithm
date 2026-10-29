// Independent GNU MP full-decimal reverse/add and palindrome checker.
#include <bits/stdc++.h>
#include <gmpxx.h>
using namespace std;
string mid(){string m(257,'9');for(int i=0;i<128;i++)if(__builtin_parity((unsigned)i))m[i]='8';return m;}
bool pal(const string&s){for(size_t i=0;i<s.size()/2;i++)if(s[i]!=s[s.size()-1-i])return false;return true;}
uint64_t hash64(const string&s){uint64_t h=1469598103934665603ull;for(unsigned char c:s){h^=c;h*=1099511628211ull;}return h;}
int main(int argc,char**argv){
 if(argc!=4)return 2;
 int L=atoi(argv[1]),T=atoi(argv[2]),stride=atoi(argv[3]);
 string start="5"+string(L,'9')+mid()+string(L,'9')+"4";
 mpz_class a(start),r;
 for(int t=0;t<=T;t++){
  string s=a.get_str();
  if(pal(s)){cerr<<"PAL "<<t<<"\n";return 2;}
  if(t%stride==0||t==T){
   cout<<"t="<<t<<" digits="<<s.size()<<" fnv64="<<hex<<hash64(s)<<dec
       <<" low="<<s.substr(s.size()-min<size_t>(16,s.size()))
       <<" top="<<s.substr(0,min<size_t>(16,s.size()))<<"\n";
  }
  if(t<T){reverse(s.begin(),s.end());mpz_set_str(r.get_mpz_t(),s.c_str(),10);a+=r;}
 }
}
