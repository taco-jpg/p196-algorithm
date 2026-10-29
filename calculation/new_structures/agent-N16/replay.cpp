// GMP arbitrary-precision decimal integer replay. Independent of the digit-vector engine.
#include <gmp.h>
#include <algorithm>
#include <cassert>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <string>
using namespace std;
static const string Bs="H501D4EC98FGHDH9144B8G09EB9B6DI947HF97D;8D5158982IEDFCC7B586AF7A47228AD8EBFE5HB;H6B2AGIG5HA8C65G2BGD1BG09E44H17I94C9CF4;8E8438GGCD99B9BC949B5397A498C98G8E7339A;H8H86HDE680040459A92B6IF09IH49ICI8F6791;8GGGEEC9BE804449F00C48FF6A8HCE8CCHECDGA;HDEEAA6049H08899A1149HBBE0IF69I56GA68E1;8C9A62764E788GI90225E7A4759FCG8EBD87ED6";
static const string Ws="H31DHBE3I12073ECF97D;CB45CA78CA327A8895HB;639B51FH5174F0HGIBF4;A9D1767ED68BA68FGB8A;2073ECF97DH31DHBE3I1;327A8895HBCB45CA78CA;74F0HGIBF4639B51FH51;8BA68FGB8AA9D1767ED6";
static int val(char c){if(c>='0'&&c<='9')return c-'0';if(c>='A'&&c<='I')return 10+c-'A';abort();}
static string row(string s,int phase){size_t pos=0;for(int i=0;i<phase;i++)pos=s.find(';',pos)+1;size_t end=s.find(';',pos);return s.substr(pos,end==string::npos?string::npos:end-pos);}
static string seed_decimal(int q){
 string lo=row(Bs,0),w=row(Ws,0);for(int i=0;i<q;i++)lo+=w;
 string s; s.reserve(2*lo.size());
 for(char c:lo)s+=char('0'+min(9,val(c)));
 for(auto it=lo.rbegin();it!=lo.rend();it++)s+=char('0'+max(0,val(*it)-9));
 return s;
}
int main(int argc,char**argv){
 int q=argc>1?atoi(argv[1]):300,T=argc>2?atoi(argv[2]):20000;
 if(q<1||T<1)return 2;
 string b[8],w[8];for(int t=0;t<8;t++){b[t]=row(Bs,t);w[t]=row(Ws,t);assert(b[t].size()==39&&w[t].size()==20);}
 string init=seed_decimal(q);mpz_t n,r,v;mpz_inits(n,r,v,nullptr);
 assert(mpz_set_str(n,init.c_str(),10)==0);
 int minPrefix=1000000,minT=-1,maxLen=0;unsigned long long checksum=1469598103934665603ULL;
 for(int t=0;t<=T;t++){
  string buf(mpz_sizeinbase(n,10)+3,'\0');mpz_get_str(buf.data(),10,n);buf.resize(strlen(buf.c_str()));
  int L=(int)buf.size();maxLen=max(maxLen,L);if(buf[0]=='0')return 5;
  int matching=0;for(int i=0;i<L/2;i++){
   int x=(buf[L-1-i]-'0')+(buf[i]-'0');
   int expected=(i<39?val(b[t%8][i]):val(w[t%8][(i-39)%20]));
   if(x!=expected)break;matching++;
  }
  if(matching<minPrefix){minPrefix=matching;minT=t;}
  if(matching<39){cerr<<"B mismatch at "<<t<<" match="<<matching<<"\n";return 6;}
  bool pal=true;for(int i=0;i<L/2;i++)if(buf[i]!=buf[L-1-i]){pal=false;break;}
  if(pal){cerr<<"palindrome t="<<t<<"\n";return 7;}
  checksum^=(unsigned long long)(matching+37*t+L);checksum*=1099511628211ULL;
  for(int m:{9,11,99,101,1001}){unsigned long rem=mpz_fdiv_ui(n,m);checksum^=rem+1231u*m;checksum*=1099511628211ULL;}
  if(t==T)break;
  string rev=buf;reverse(rev.begin(),rev.end());assert(mpz_set_str(r,rev.c_str(),10)==0);
  mpz_add(v,n,r);string vbuf(mpz_sizeinbase(v,10)+3,'\0');mpz_get_str(vbuf.data(),10,v);
  int L2=strlen(vbuf.c_str());
  if((L2!=L && L2!=L+1)||((L2==L+1)!=(t%2==0))){cerr<<"gamma mismatch at "<<t<<"\n";return 8;}
  mpz_swap(n,v);
 }
 cout<<"PASS seed_digits="<<init.size()<<" q="<<q<<" steps="<<T<<" min_prefix="<<minPrefix<<" min_at="<<minT<<" final_digits="<<maxLen<<" checksum="<<hex<<checksum<<dec<<"\n";
 mpz_clears(n,r,v,nullptr);return 0;
}
