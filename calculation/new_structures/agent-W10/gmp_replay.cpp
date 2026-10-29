// Independent arbitrary-precision replay: GNU MP, decimal export/reversal,
// exact integer addition. No period assumptions or digit-carry implementation.
#include <gmpxx.h>
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <string>
using namespace std;
static uint64_t fnv_lsd(const string &s){
  uint64_t h=14695981039346656037ull;
  for(auto it=s.rbegin();it!=s.rend();++it){h^=(uint8_t)(*it-'0');h*=1099511628211ull;}
  return h;
}
int main(int argc,char**argv){
  if(argc!=3){cerr<<"usage: gmp_replay BLOCKS STEPS\n";return 2;}
  int q=atoi(argv[1]),T=atoi(argv[2]);if(q<1||T<0)return 2;
  string seed;seed.reserve(4*q);for(int i=0;i<q;i++)seed+="5346";
  mpz_class x(seed,10);int gamma=0,prev=0;
  cout<<"step\tlength\tlength_increases\tfnv64_lsd\n";
  for(int t=0;t<=T;t++){
    string s=x.get_str(10);
    if(t>0)gamma+=(int)s.size()-prev;
    prev=(int)s.size();
    string reversed=s;reverse(reversed.begin(),reversed.end());
    if(s==reversed){cerr<<"ERROR palindrome at step "<<t<<"\n";return 3;}
    if(t%1000==0||t==T)
      cout<<t<<'\t'<<s.size()<<'\t'<<gamma<<'\t'<<hex<<setw(16)<<setfill('0')<<fnv_lsd(s)<<dec<<setfill(' ')<<'\n';
    if(t==T)break;
    mpz_class y(reversed,10);
    x+=y;
  }
  cerr<<"GMP PASS block=5346 q="<<q<<" steps="<<T<<" gamma="<<gamma<<"\n";
}
