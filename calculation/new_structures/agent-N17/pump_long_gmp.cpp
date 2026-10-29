// Independently replay complete long seed pair with actual GMP big integers.
#include <gmp.h>
#include <algorithm>
#include <cstring>
#include <iostream>
#include <string>
using namespace std;
int pre[]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
int cyc[]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
string seed(int h){string hi,lo;hi.reserve(h);lo.reserve(h);for(int i=0;i<h;i++){int p=i<39?pre[i]:cyc[(i-39)%20],d=max(0,p-9);hi+=char('0'+p-d);lo+=char('0'+d);}reverse(lo.begin(),lo.end());return hi+lo;}
string decimal(mpz_t z){string s(mpz_sizeinbase(z,10)+3,'\0');mpz_get_str(s.data(),10,z);s.resize(strlen(s.c_str()));return s;}
int pairat(string const &s,int i){return s[i]-'0'+s[s.size()-i-1]-'0';}
int main(int argc,char**argv){
 int h=argc>1?atoi(argv[1]):8000,T=argc>2?atoi(argv[2]):20000,m=argc>3?atoi(argv[3]):20;
 if(h<80||m<=0||m%20||T<0)return 2;
 mpz_t a,b,r;mpz_inits(a,b,r,nullptr);mpz_set_str(a,seed(h).c_str(),10);mpz_set_str(b,seed(h+m).c_str(),10);
 long long cells=0;int first=-1,badgam=-1,pal=-1,finalLen=0;
 for(int t=0;t<=T;t++){
  string x=decimal(a),y=decimal(b);int n=x.size();if((int)y.size()!=n+2*m&&first<0)first=t;
  for(int i=0;i<n/2;i++){int u=pairat(x,i),v=pairat(y,i<39?i:i+m);cells++;if(u!=v&&first<0){first=t;cerr<<"FAIL at step="<<t<<" index="<<i<<"\n";}}
  bool ispal=true;for(int i=0;i<n/2;i++)if(x[i]!=x[n-1-i]){ispal=false;break;}if(ispal&&pal<0)pal=t;
  finalLen=n;if(t<T){
   string xr=x,yr=y;reverse(xr.begin(),xr.end());reverse(yr.begin(),yr.end());
   mpz_set_str(r,xr.c_str(),10);mpz_add(a,a,r);mpz_set_str(r,yr.c_str(),10);mpz_add(b,b,r);
   if((int)decimal(b).size()!=(int)decimal(a).size()+2*m&&badgam<0)badgam=t;
  }
 }
 cout<<"GMP h="<<h<<" m="<<m<<" T="<<T<<" all_cells="<<cells<<" firstfail="<<first<<" badgamma="<<badgam<<" palindrome="<<pal<<" finalLen="<<finalLen<<"\n";
 mpz_clears(a,b,r,nullptr);return first>=0||badgam>=0||pal>=0;
}
