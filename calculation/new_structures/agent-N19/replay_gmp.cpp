// Independent ordinary arbitrary-precision integer replay with GMP and decimal reversal.
#include <gmpxx.h>
#include <algorithm>
#include <iostream>
#include <string>
#include <cstdlib>
#include <cstdint>
using namespace std;
static uint64_t fnv(const string &s){uint64_t h=14695981039346656037ULL;
 for(unsigned char c:s){h^=c;h*=1099511628211ULL;}return h;}
int main(int argc,char**argv){
 int L=argc>1?atoi(argv[1]):22000,T=argc>2?atoi(argv[2]):20000;
 string initial="9"+string(L,'8')+string(L,'0')+"1";
 mpz_class n(initial), rev;
 const int bulk[6]={8,16,14,10,2,4};
 int first_pal=-1,mincent=1000000;
 for(int t=0;t<=T;t++){
   string s=n.get_str(10);int sz=s.size();
   bool pal=equal(s.begin(),s.begin()+sz/2,s.rbegin());
   if(pal&&first_pal<0)first_pal=t;
   int half=(sz+1)/2,k=0;
   while(k<half){int i=half-1-k,j=sz-1-i;
     if(i==j){if(2*(s[i]-'0')!=bulk[t%6])break;}
     else if((s[i]-'0')+(s[j]-'0')!=bulk[t%6])break;
     ++k;
   }
   mincent=min(mincent,k);
   if(t==0||t==1||t==10||t==100||t==1000||t==10000||t==T)
     cout<<"GMP step="<<t<<" digits="<<sz<<" central="<<k
         <<" palindrome="<<pal<<" fnv64="<<hex<<fnv(s)<<dec<<'\n';
   if(t==T)break;
   reverse(s.begin(),s.end());rev=mpz_class(s,10);n+=rev;
 }
 cout<<"GMP done pal_first="<<first_pal<<" minimum_central_halfwidth="
     <<mincent<<" final_digits="<<n.get_str(10).size()<<'\n';
}
