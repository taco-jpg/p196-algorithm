// Independent GMP whole-integer reverse-and-add and pairword shape check.
#include <gmpxx.h>
#include <algorithm>
#include <fstream>
#include <iostream>
#include <string>
#include <cstdint>
using namespace std;
static const int W[8][20]={
{17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13},
{12,11,4,5,12,10,7,8,12,10,3,2,7,10,8,8,9,5,17,11},
{6,3,9,11,5,1,15,17,5,1,7,4,15,0,17,16,18,11,15,4},
{10,9,13,1,7,6,7,14,13,6,8,11,10,6,8,15,16,11,8,10},
{2,0,7,3,14,12,15,9,7,13,17,3,1,13,17,11,14,3,18,1},
{3,2,7,10,8,8,9,5,17,11,12,11,4,5,12,10,7,8,12,10},
{7,4,15,0,17,16,18,11,15,4,6,3,9,11,5,1,15,17,5,1},
{8,11,10,6,8,15,16,11,8,10,10,9,13,1,7,6,7,14,13,6}};
int maxmatch(const string&s,int t){
 int n=s.size(),best=0,run=0;
 for(int i=39;i<n/2;i++){
  int p=(s[n-1-i]-'0')+(s[i]-'0');
  if(p==W[t%8][(i-39)%20]){run++;best=max(best,run);}else run=0;
 }
 return best;
}
int main(int argc,char**argv){
 if(argc<3)return 2;
 ifstream f(argv[1]);string seed;f>>seed;
 mpz_class n(seed,10);
 int steps=stoi(argv[2]),minimum=100000000;
 uint64_t digest=1469598103934665603ULL;
 for(int t=0;t<=steps;t++){
  string s=n.get_str(10),reversed=s;
  reverse(reversed.begin(),reversed.end());
  for(char x:s)digest=(digest^(uint64_t)(unsigned char)x)*1099511628211ULL;
  digest=(digest^255ULL)*1099511628211ULL;
  if(s==reversed){cerr<<"PAL "<<t<<"\n";return 3;}
  int matched=t?maxmatch(s,t):-1;
  if(t && matched<40){cerr<<"BAND FAIL "<<t<<" "<<matched<<"\n";return 4;}
  if(t)minimum=min(minimum,matched);
  if(t%2000==0||t==steps)cout<<"CHECK "<<t<<" digits="<<s.size()<<" longest_bulk="<<matched<<"\n";
  if(t==steps)break;
  n+=mpz_class(reversed,10);
 }
 cout<<"PASSED gmp "<<steps<<" min_longest_bulk="<<minimum<<" digest="<<hex<<digest<<dec<<"\n";
}
