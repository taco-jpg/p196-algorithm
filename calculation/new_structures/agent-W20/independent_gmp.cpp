// Independent ordinary decimal arbitrary-precision replay for agent-W20.
// g++ -std=c++17 -O3 calculation/new_structures/agent-W20/independent_gmp.cpp -lgmpxx -lgmp -o /tmp/w20_gmp
// /tmp/w20_gmp calculation/new_structures/agent-N18/lattice.txt 240 20000
#include <gmpxx.h>
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
int main(int argc,char**argv){
 try{
  if(argc!=4)throw runtime_error("usage: independent_gmp lattice.txt q steps");
  ifstream f(argv[1]);if(!f)throw runtime_error("missing fixture");
  int ext[39][8], w[20];
  for(auto &r:ext)for(int &x:r)if(!(f>>x))throw runtime_error("bad exterior");
  for(int t=0;t<8;t++)for(int i=0;i<20;i++){
    int x;if(!(f>>x))throw runtime_error("bad band");if(t==0)w[i]=x;
  }
  int q=stoi(argv[2]),steps=stoi(argv[3]);if(q<1||steps<0)throw runtime_error("bad args");
  vector<int> u(43,1);u[13]=7;u[20]=7;u[30]=6;u[40]=u[41]=u[42]=0;
  vector<int> c={8,0,0};c.insert(c.end(),u.begin(),u.end());c.push_back(16);
  c.insert(c.end(),u.rbegin(),u.rend());c.insert(c.end(),{0,0,8});
  vector<int>a;for(auto&r:ext)a.push_back(r[0]);for(int j=0;j<q;j++)for(int v:w)a.push_back(v);
  vector<int>p=a;p.insert(p.end(),c.begin(),c.end());p.insert(p.end(),a.rbegin(),a.rend());
  vector<int>d(p.size());for(size_t i=0;i<p.size()/2;i++){
    d[i]=min(p[i],9);d[p.size()-1-i]=p[i]-d[i];
  }
  d[p.size()/2]=p[p.size()/2]/2;
  string s;for(auto it=d.rbegin();it!=d.rend();++it)s.push_back('0'+*it);
  if(s[0]=='0')throw runtime_error("leading zero seed");
  mpz_class n(s,10);
  int over=0;uint64_t fnv=1469598103934665603ull;
  auto hash=[&](const string&v){uint64_t h=1469598103934665603ull;for(unsigned char x:v){h^=x;h*=1099511628211ull;}return h;};
  for(int t=0;t<=steps;t++){
    s=n.get_str(10);string rev(s.rbegin(),s.rend());
    if(s==rev)throw runtime_error("palindrome at t="+to_string(t));
    int len=s.size();for(int j=0;j<39;j++){
      int pair=(s[len-1-j]-'0')+(s[j]-'0');
      if(pair!=ext[j][t%8])throw runtime_error("exterior mismatch at t="+to_string(t));
    }
    if(t==0||t==88||t==176||t==264||t==352||t==5000||t==10000||t==15000||t==steps)
      cout<<"GMP_CHECK t="<<t<<" digits="<<len<<" fnv64="<<hash(s)<<"\n";
    if(t==steps){fnv=hash(s);break;}
    n+=mpz_class(rev,10);
    if(n.get_str(10).size()>size_t(len))over++;
  }
  cout<<"GMP_PASS q="<<q<<" steps="<<steps<<" final_digits="<<s.size()<<" overflows="<<over<<" final_fnv64="<<fnv<<" palindrome_count=0\n";
 }catch(const exception&e){cerr<<"GMP_FAIL "<<e.what()<<"\n";return 1;}
}
