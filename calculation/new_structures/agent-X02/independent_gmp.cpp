// X02: independent GNU GMP arbitrary-precision integer replay; no digitwise addition.
#include <gmpxx.h>
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
using namespace std;
int main(int argc,char**argv){
 int h=argc>1?atoi(argv[1]):20200,H=argc>2?atoi(argv[2]):20000;
 if(h<=H+30)throw runtime_error("h must exceed H+30");
 string digits="9"+string(2*h-2,'7')+"68";
 mpz_class n(digits,10);
 int qcycle[6]={14,10,2,4,8,16};uint64_t hsh=1469598103934665603ULL;
 unsigned long long checked=0;int mincorr=INT32_MAX;
 for(int t=0;t<=H;t++){
  string s=n.get_str(10);
  string backwards=s;reverse(backwards.begin(),backwards.end());
  if(s==backwards)throw runtime_error("palindrome at "+to_string(t));
  int N=(int)s.size();int margin=t+20;
  if(margin>=N-margin-1)throw runtime_error("corridor exhausted");
  mincorr=min(mincorr,N-2*margin);
  int need=qcycle[t%6];
  for(int i=margin;i<N-margin;i++){
   int q=(s[i]-'0')+(s[N-1-i]-'0');
   if(q!=need)throw runtime_error("band mismatch t="+to_string(t)+" i="+to_string(i));
   checked++;
  }
  if(t==H){
   for(auto it=s.rbegin();it!=s.rend();++it){hsh^=(unsigned char)(*it-'0')+1;hsh*=1099511628211ULL;}
   cout<<"GMP_INDEPENDENT_PASS H="<<H<<" n="<<N<<" checked="<<checked<<" mincorr="<<mincorr<<" digit_fnv64="<<hex<<hsh<<dec<<"\n";
   break;
  }
  mpz_class rev(backwards,10);
  n+=rev;
 }
}
