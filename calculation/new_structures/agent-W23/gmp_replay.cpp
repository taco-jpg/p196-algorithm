// Independent GMP decimal strings+arbitrary-precision arithmetic 20,000-step replay.
// g++ -O3 -std=c++17 gmp_replay.cpp -lgmpxx -lgmp -o /tmp/w23_gmp && /tmp/w23_gmp 100 20000
#include <gmpxx.h>
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <cstdint>
using namespace std;
const int W[]={4,4,14,1,5,11,7,1,15,12,7,9,9,12,14,4,0,6,5,17,13,9,7,3,13,10,4,13,5,1,9,4,11,6,16,3,7,7,12,4,2,13,2,15,10,10,9,3};
const int ROOT[8][8]={{17,8,17,8,17,8,17,8},{5,13,6,14,8,16,13,12},
{0,5,11,8,17,16,14,9},{2,2,4,6,13,12,5,10},
{1,3,7,11,2,6,14,10},{9,11,2,9,9,12,4,9},
{15,5,12,5,11,1,3,7},{18,15,11,5,10,3,6,9}};
string original_seed(int q){
 vector<int> h={17,5,0,2,1,9,15,18,14,9,3};
 for(int i=0;i<q;i++)for(int p:W)h.push_back(p);
 for(int p:{10,14,1,10})h.push_back(p);
 string s;for(int i=0;i<(int)h.size()-1;i++)s.push_back('0'+min(9,h[i]));
 s.push_back('5');for(int i=(int)h.size()-2;i>=0;i--)s.push_back('0'+max(0,h[i]-9));
 return s;
}
int main(int argc,char**argv){
 int q=argc>1?stoi(argv[1]):100,T=argc>2?stoi(argv[2]):20000;
 mpz_class z(original_seed(q),10);string s;int gam=0;
 for(int t=0;t<=T;t++){
  s=z.get_str(10);
  if(equal(s.begin(),s.end(),s.rbegin()))return 2;
  for(int i=0;i<8;i++)if(s[i]-'0'+s[s.size()-1-i]-'0'!=ROOT[i][t%8])return 3;
  if(t==T)break;
  string rev(s.rbegin(),s.rend());z+=mpz_class(rev,10);
  int g=(int)z.get_str(10).size()-(int)s.size();
  if(g!=1-t%2)return 4;gam+=g;
 }
 uint64_t hash=1469598103934665603ULL;
 for(auto it=s.rbegin();it!=s.rend();it++){hash^=uint64_t(*it-'0');hash*=1099511628211ULL;}
 cout<<hex<<hash<<dec<<" digits="<<s.size()<<" overflow="<<gam<<"\n";
 return T!=20000||(hash==0x971e60282dc35bc9ULL&&s.size()==19629)?0:5;
}