// Independent GMP-only multi-gap replay, no symbolic packets.
#include <gmpxx.h>
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
using namespace std;
uint64_t fnv(const string&s){uint64_t h=14695981039346656037ULL;for(unsigned char c:s){h^=c;h*=1099511628211ULL;}return h;}
string pairword(const string&w){string p(w.size(),'A');for(size_t j=0;j<w.size();j++)p[j]='A'+w[j]+w[w.size()-1-j]-2*'0';return p;}
bool pal(const string&w){for(size_t j=0;j<w.size()/2;j++)if(w[j]!=w[w.size()-1-j])return false;return true;}
int main(int argc,char**argv){try{if(argc!=8&&argc!=9)throw runtime_error("usage: gmp Q2 DELTA END TSV STATE TOP MID [RESUME]");
 long long q2=stoll(argv[1]),delta=stoll(argv[2]);int end=stoi(argv[3]),start=0;
 string seed=string(argv[6])+string(q2+delta,'0')+string(argv[7])+string(q2,'0')+"75";
 if(argc==9){ifstream in(argv[8]);in>>start>>seed;}
 mpz_class n(seed,10);ofstream out(argv[4]);out<<"t\tdigits\tfull_fnv64\tpair_fnv64\n";
 for(int t=start;t<=end;t++){string w=n.get_str();if(pal(w))throw runtime_error("palindrome "+to_string(t));
  if(t%1000==0||t==end){out<<t<<'\t'<<w.size()<<'\t'<<hex<<fnv(w)<<'\t'<<fnv(pairword(w))<<std::dec<<'\n';out.flush();}
  if(t==end)break;string r=w;reverse(r.begin(),r.end());n+=mpz_class(r,10);
 }
 ofstream state(argv[5]);state<<end<<'\n'<<n.get_str()<<'\n';cerr<<"GMP PASS "<<end<<" length "<<n.get_str().size()<<'\n';
 }catch(const exception&e){cerr<<"FAIL "<<e.what()<<'\n';return 1;}}
