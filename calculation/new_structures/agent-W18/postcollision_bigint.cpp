// W18 structurally independent base-1e9 bigint/reversal checker through collision.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;using B=vector<uint32_t>;constexpr uint64_t RAD=1000000000ULL;
static B parse(const string&s){B a;for(int j=(int)s.size();j>0;j-=9){int i=max(0,j-9);a.push_back(stoul(s.substr(i,j-i)));}return a;}
static string render(const B&a){string s=to_string(a.back());for(int j=(int)a.size()-2;j>=0;j--){string t=to_string(a[j]);s+=string(9-t.size(),'0')+t;}return s;}
static B addBig(const B&a,const B&b){B o;uint64_t c=0;for(size_t i=0;i<max(a.size(),b.size());i++){uint64_t z=c+(i<a.size()?a[i]:0)+(i<b.size()?b[i]:0);o.push_back(z%RAD);c=z/RAD;}if(c)o.push_back(c);return o;}
static uint64_t digest(const string&s){uint64_t h=0;for(char ch:s)h=(131*h+ch)%1000000007ULL;return h;}
int main(int argc,char**argv){int Q=argc>1?atoi(argv[1]):4138,T=argc>2?atoi(argv[2]):25000;if(Q<1||T<0)return 2;B n=parse("5"+string(Q*2,'9')+"4");
 for(int t=0;t<=T;t++){
  string s=render(n);if(equal(s.begin(),s.begin()+s.size()/2,s.rbegin())){cerr<<"PAL at "<<t<<"\n";return 3;}
  if(t==20000||t==20006||t==25000)cout<<"checkpoint t="<<t<<" digits="<<s.size()<<" hash="<<digest(s)<<"\n";
  if(t==T){cout<<"PASS Q="<<Q<<" T="<<T<<" final_digits="<<s.size()<<" final_hash="<<digest(s)<<"\n";break;}
  string r(s.rbegin(),s.rend());n=addBig(n,parse(r));
 }
}
