// Independent GMP vs decimal-digit-vector replay for an inserted symmetric centre pulse.
#include <gmp.h>
#include <algorithm>
#include <fstream>
#include <iostream>
#include <cstring>
#include <string>
#include <vector>
using namespace std;
int cv(char c){return c<='9'?c-'0':c-'A'+10;}
string numeral(const vector<unsigned char>&d){string s;s.reserve(d.size());for(auto i=d.rbegin();i!=d.rend();i++)s.push_back(char('0'+*i));return s;}
int main(int argc,char**argv){
 if(argc<5)return 1;ifstream f(argv[1]);string header;getline(f,header);
 vector<string>B(8),W(8);for(auto&x:B)getline(f,x);for(auto&x:W)getline(f,x);
 int q=stoi(argv[2]),H=stoi(argv[3]);string core=argv[4];
 vector<int>lo;for(char c:B[0])lo.push_back(cv(c));for(int j=0;j<q;j++)for(char c:W[0])lo.push_back(cv(c));for(char c:core)lo.push_back(cv(c));
 vector<unsigned char>d;for(int p:lo)d.push_back(max(0,p-9));for(auto i=lo.rbegin();i!=lo.rend();i++)d.push_back(min(9,*i));
 mpz_t n,r,z;mpz_inits(n,r,z,NULL);string seed=numeral(d);if(mpz_set_str(n,seed.c_str(),10)!=0)return 2;
 int minpre=999999,mint=-1;for(int t=0;t<=H;t++){
  string s(mpz_sizeinbase(n,10)+3,'\0');mpz_get_str(s.data(),10,n);s.resize(strlen(s.c_str()));
  if(s!=numeral(d)){cerr<<"integer divergence at "<<t<<"\n";return 3;}
  int L=d.size(),m=0;bool palindrome=true;for(int i=0;i<L/2;i++)if(d[i]!=d[L-1-i])palindrome=false;
  if(palindrome){cerr<<"PALINDROME at "<<t<<"\n";return 4;}
  for(int i=0;i<L/2;i++){int x=i<39?cv(B[t%8][i]):cv(W[t%8][(i-39)%20]);if(d[i]+d[L-1-i]!=x)break;++m;}
  if(m<minpre){minpre=m;mint=t;}if(m<39){cerr<<"exterior lost at "<<t<<"\n";return 5;}
  if(t==0||t==22||t==44||t==66||t==88||t==264||t==528||t==792||t==1000||t==5000||t==10000||t==20000)
   cout<<"t="<<t<<" match="<<m<<" D="<<39+20*q-m<<" digits="<<L<<"\n";
  if(t==H)break;
  vector<unsigned char>next;int carry=0;for(int i=0;i<L;i++){int v=d[i]+d[L-1-i]+carry;next.push_back(v%10);carry=v/10;}if(carry)next.push_back(carry);
  string rev=s;reverse(rev.begin(),rev.end());if(mpz_set_str(r,rev.c_str(),10)!=0)return 6;mpz_add(z,n,r);mpz_swap(n,z);
  if((int)next.size()-L!=(t%2==0)){cerr<<"overflow mismatch at "<<t<<"\n";return 7;}
  d.swap(next);
 }
 cout<<"PULSE_PASS q="<<q<<" core="<<core<<" H="<<H<<" minprefix="<<minpre<<" min_at="<<mint<<"\n";
 mpz_clears(n,r,z,NULL);
}
