// Independent arbitrary-precision decimal integer reverse-and-add replay.
// Reuses only the finite seed definition and checksum from the contract checker.
#define main w16_contract_entry
#include "skew_contract.cpp"
#undef main
#include <gmpxx.h>
int main(int argc,char**argv){
 int kw=argc>1?stoi(argv[1]):440,kv=argc>2?stoi(argv[2]):530,T=argc>3?stoi(argv[3]):20000;
 Word half=B;
 for(int i=0;i<kw;i++)half.insert(half.end(),W.begin(),W.end());
 half.push_back(9);
 for(int i=0;i<kv;i++)half.insert(half.end(),V.begin(),V.end());
 Word p=half;p.push_back(9);p.insert(p.end(),half.rbegin(),half.rend());
 Word seed=normalize(p).first;
 string s;for(auto it=seed.rbegin();it!=seed.rend();++it)s.push_back('0'+*it);
 mpz_class n(s);
 for(int t=0;t<=T;t++){
   string a=n.get_str(),b=a;reverse(b.begin(),b.end());
   if(a==b){cerr<<"PAL t="<<t<<"\n";return 3;}
   if(t<T){mpz_class r(b);n+=r;}
 }
 string final=n.get_str();Word digits;digits.reserve(final.size());
 for(auto it=final.rbegin();it!=final.rend();++it)digits.push_back(*it-'0');
 cout<<"GMP PASS kw="<<kw<<" kv="<<kv<<" steps="<<T
     <<" digits="<<digits.size()<<" fnv64="<<hex<<hashdigits(digits)<<dec<<"\n";
}
