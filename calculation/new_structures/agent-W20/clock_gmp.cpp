// W20 independent ordinary GMP replay to the first rooted exterior break.
// g++ -std=c++17 -O3 -Wall -Wextra -Werror clock_gmp.cpp -lgmpxx -lgmp -o clock_gmp
// clock_gmp lattice_n18.txt 240 0 0 0 21396
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
  if(argc!=7)throw runtime_error("usage: clock_gmp fixture q x y z expected_first_mismatch");
  int q=stoi(argv[2]),x=stoi(argv[3]),y=stoi(argv[4]),z=stoi(argv[5]),expect=stoi(argv[6]);
  ifstream f(argv[1]);int ext[39][8],W[20];
  for(auto&r:ext)for(auto &t:r)if(!(f>>t))throw runtime_error("missing ext");
  for(int t=0;t<8;t++)for(int j=0;j<20;j++){int a;if(!(f>>a))throw runtime_error("missing band");if(t==0)W[j]=a;}
  vector<int>U(43,1);U[13]=7;U[20]=7;U[30]=6;U[40]=x;U[41]=y;U[42]=z;
  vector<int>C={8,0,0};C.insert(C.end(),U.begin(),U.end());C.push_back(16);
  C.insert(C.end(),U.rbegin(),U.rend());C.insert(C.end(),{0,0,8});
  vector<int>A;for(auto&r:ext)A.push_back(r[0]);for(int k=0;k<q;k++)for(int a:W)A.push_back(a);
  vector<int>P=A;P.insert(P.end(),C.begin(),C.end());P.insert(P.end(),A.rbegin(),A.rend());
  vector<int>D(P.size());for(size_t j=0;j<P.size()/2;j++){D[j]=min(P[j],9);D[P.size()-1-j]=P[j]-D[j];}D[P.size()/2]=P[P.size()/2]/2;
  string S;for(auto j=D.rbegin();j!=D.rend();j++)S.push_back(*j+'0');mpz_class N(S,10);
  int first=-1,col=-1;string last;
  for(int t=0;t<=expect;t++){
    S=N.get_str(10);last=S;string R(S.rbegin(),S.rend());
    if(S==R)throw runtime_error("palindrome step="+to_string(t));
    for(int j=0;j<39;j++)if(S[S.size()-1-j]-'0'+S[j]-'0'!=ext[j][t%8]){first=t;col=j;break;}
    if(first>=0)break;
    N+=mpz_class(R,10);
  }
  if(first!=expect)throw runtime_error("first mismatch observed="+to_string(first)+" expected="+to_string(expect));
  uint64_t h=1469598103934665603ULL;for(unsigned char a:last){h^=a;h*=1099511628211ULL;}
  cout<<"CLOCK_GMP_PASS q="<<q<<" payload="<<x<<","<<y<<","<<z<<" first_mismatch="<<first<<" col="<<col<<" digits="<<last.size()<<" fnv64="<<h<<" no_palindromes_through_first_failure=1\n";
 }catch(const exception&e){cerr<<"CLOCK_GMP_FAIL: "<<e.what()<<"\n";return 1;}
}
