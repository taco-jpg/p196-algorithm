// Independent actual-integer GMP replay of the 256^M synchronizing family.
// g++ -O3 -std=c++17 toggle_gmp.cpp -lgmpxx -lgmp -o /tmp/w06tgmp
// /tmp/w06tgmp [M=320] [T=20000]
#include <gmpxx.h>
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
using namespace std;
static const vector<int> B={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static const vector<int> W={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
static const int site[]={1,3,5,7,9,12,14,19};
static const int swapto[]={12,4,2,12,10,16,5,4};
[[noreturn]] void die(const string&s){cerr<<"FAIL "<<s<<"\n";exit(2);}
mpz_class make_seed(int M,bool mutated){
 vector<int> h=B;
 for(int r=0;r<M;r++){
  vector<int> w=W;
  if(mutated)for(int bit=0;bit<8;bit++)if(((r*17+bit*13)%3)==0)w[site[bit]]=swapto[bit];
  h.insert(h.end(),w.begin(),w.end());
 }
 vector<int> p=h;p.push_back(18);p.insert(p.end(),h.rbegin(),h.rend());
 string d(p.size(),'0');int n=p.size();
 for(int i=0;i<n/2;i++){int a=min(9,p[i]);d[n-1-i]='0'+a;d[i]='0'+p[i]-a;}
 d[n/2]='9';
 if(d[0]=='0'||d.back()=='0')die("noncanonical seed");
 return mpz_class(d,10);
}
mpz_class rev_add(const mpz_class&n){string a=n.get_str(10),b=a;reverse(b.begin(),b.end());return n+mpz_class(b,10);}
uint64_t fnv(const string&s){uint64_t h=1469598103934665603ull;for(unsigned char c:s){h^=c;h*=1099511628211ull;}return h;}
int main(int argc,char**argv){int M=argc>1?atoi(argv[1]):320,T=argc>2?atoi(argv[2]):20000;if(M<1||T<2)die("M>=1,T>=2");
 mpz_class base=make_seed(M,false),alt=make_seed(M,true);
 if(base==alt)die("no independent masks");
 mpz_class b1=rev_add(base),a1=rev_add(alt);
 if(b1==a1)die("expected different first-step integers");
 mpz_class b2=rev_add(b1),a2=rev_add(a1);
 if(b2!=a2)die("2-step synchronization mismatch");
 size_t seedlen=base.get_str(10).size();
 int pal=0,clockbad=0;mpz_class n=base;
 for(int t=0;t<=T;t++){
  string s=n.get_str(10);
  if(equal(s.begin(),s.begin()+s.size()/2,s.rbegin()))pal++;
  if(t==0||t==1||t==2||t==T){cout<<"t="<<t<<" digits="<<s.size()<<" fnv="<<hex<<fnv(s)<<dec<<"\n";}
  if(t<T){auto v=rev_add(n);int expected=(t%2==0)?1:0;clockbad+=int(v.get_str(10).size()-s.size())!=expected;n=std::move(v);}
 }
 cout<<"COMPUTED GMP M="<<M<<" T="<<T<<" distinct_seeds_bits="<<8*M<<" initial_digits="<<seedlen
   <<" final_digits="<<n.get_str(10).size()<<" palindrome_count="<<pal<<" clockbad="<<clockbad
   <<" final_full_msd_FNV64="<<hex<<fnv(n.get_str(10))<<dec<<"\n";
 if(pal||clockbad) return 3;
 return 0;
}
