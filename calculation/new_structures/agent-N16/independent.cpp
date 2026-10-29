// Independent decimal digit-vector replay; no GMP, and no symbolic pairword step.
#include <array>
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
using namespace std;
static int cv(char c){if(c>='0'&&c<='9')return c-'0';if(c>='A'&&c<='I')return 10+c-'A';abort();}
static uint64_t fnv=1469598103934665603ULL;
static void add(uint64_t x){fnv^=x;fnv*=1099511628211ULL;}
static bool palindrome(const vector<unsigned char>&d){for(size_t i=0;i<d.size()/2;i++)if(d[i]!=d[d.size()-1-i])return false;return true;}
static vector<unsigned char> add_reverse(const vector<unsigned char>&d){
 vector<unsigned char> result;result.reserve(d.size()+1);unsigned carry=0;
 for(size_t i=0;i<d.size();i++){unsigned z=d[i]+d[d.size()-1-i]+carry;result.push_back(z%10);carry=z/10;}
 if(carry)result.push_back(carry);return result;
}
static array<uint32_t,5> residues(const vector<unsigned char>&d){
 const int ms[5]={9,11,99,101,1001};array<uint32_t,5> r{};
 for(auto it=d.rbegin();it!=d.rend();it++)for(int k=0;k<5;k++)r[k]=(10*r[k]+*it)%ms[k];
 return r;
}
int main(int argc,char**argv){
 int q=argc>2?atoi(argv[2]):300,H=argc>3?atoi(argv[3]):20000;
 if(q<=0||H<1)return 2;
 ifstream in(argc>1?argv[1]:"rows.txt");if(!in){cerr<<"rows missing\n";return 2;}
 string header;getline(in,header);vector<string>B(8),W(8);
 for(int i=0;i<8;i++)getline(in,B[i]);for(int i=0;i<8;i++)getline(in,W[i]);
 for(int i=0;i<8;i++)if(B[i].size()!=39||W[i].size()!=20)return 3;
 vector<int>P;for(char c:B[0])P.push_back(cv(c));for(int j=0;j<q;j++)for(char c:W[0])P.push_back(cv(c));
 vector<unsigned char>d;d.reserve(2*P.size()+H);
 for(int p:P)d.push_back(max(0,p-9));
 for(auto i=P.rbegin();i!=P.rend();i++)d.push_back(min(9,*i));
 int minpre=999999,at=-1,initial=d.size();
 for(int t=0;t<=H;t++){
  if(palindrome(d)){cerr<<"PAL t="<<t<<"\n";return 4;}
  int L=(int)d.size(),z=0;
  for(int i=0;i<L/2;i++){
   int pair=d[i]+d[L-1-i],ex=(i<39?cv(B[t%8][i]):cv(W[t%8][(i-39)%20]));
   if(pair!=ex)break;
   z++;
  }
  if(z<minpre){minpre=z;at=t;}
  if(z<39){cerr<<"prefix fails t="<<t<<" z="<<z<<"\n";return 5;}
  add((uint64_t)(z+37*t+L));const int ms[5]={9,11,99,101,1001};
  auto rs=residues(d);for(int k=0;k<5;k++)add(rs[k]+1231u*ms[k]);
  if(t==H)break;
  auto nx=add_reverse(d);
  if((int)nx.size()-L!=(t%2==0)){cerr<<"overflow t="<<t<<"\n";return 6;}
  d.swap(nx);
 }
 cout<<"PASS digit-vector seed_digits="<<initial<<" q="<<q<<" steps="<<H<<" min_prefix="<<minpre<<" min_at="<<at<<" final_digits="<<d.size()<<" checksum="<<hex<<fnv<<dec<<"\n";
}
