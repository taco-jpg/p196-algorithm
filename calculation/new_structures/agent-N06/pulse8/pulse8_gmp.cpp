// N06 pulse8 independent exact GMP replay, never uses digit-list stepping.
#include <gmpxx.h>
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <string>
using namespace std;
int main(int argc,char**argv){
 if(argc<2){cerr<<"usage: independent_gmp T < seed.txt\n";return 2;}
 int T=stoi(argv[1]);string seed;
 if(!(cin>>seed)||seed.empty()||seed[0]=='0'){cerr<<"invalid seed\n";return 2;}
 mpz_class n(seed,10);int len0=seed.size();int firstfail=-1,firstpal=-1,gammafail=-1;
 constexpr int w[8][8]={
   {17,8,17,8,17,8,17,8},{5,13,6,14,8,16,13,12},
   {0,5,11,8,17,16,14,9},{1,1,2,4,8,16,14,10},
   {13,5,10,3,6,14,10,6},{4,8,16,8,17,14,10,2},
   {14,9,18,16,13,12,6,7},{12,8,16,16,14,9,0,6}};
 string s;
 for(int t=0;t<=T;++t){
   s=n.get_str(10);int z=s.size();bool eq=z>=16;
   for(int i=0;i<8&&eq;++i)if((s[i]-'0')+(s[z-1-i]-'0')!=w[i][t%8])eq=false;
   if(!eq&&firstfail<0)firstfail=t;
   bool pal=true;for(int i=0;i<z/2;i++)if(s[i]!=s[z-1-i]){pal=false;break;}
   if(pal&&firstpal<0)firstpal=t;
   if(t==T)break;
   string reversed(s.rbegin(),s.rend());mpz_class r(reversed,10);n+=r;
   if((n.get_str(10).size()==size_t(z+1))!=(t%2==0)&&gammafail<0)gammafail=t;
 }
 uint64_t fnv=14695981039346656037ULL,mod=0;
 for(char c:s){fnv^=uint8_t(c);fnv*=1099511628211ULL;mod=(mod*10+c-'0')%1000000007ULL;}
 cout<<"GMP T="<<T<<" initial_digits="<<len0<<" final_digits="<<s.size()
   <<" first8_failure="<<firstfail<<" palindrome="<<firstpal
   <<" gamma_failure="<<gammafail<<" modulo1000000007="<<mod<<" fnv64="<<fnv<<"\n";
}