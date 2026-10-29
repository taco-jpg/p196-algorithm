// N06 independent GMP spatial-pumping verification of two distinct seeds.
#include <gmpxx.h>
#include <algorithm>
#include <iostream>
#include <string>
using namespace std;
const string entrance[]={
"H501D4EC98FGHDH9144B8G09EB9B6DI947HF97D",
"8D5158982IEDFCC7B586AF7A47228AD8EBFE5HB",
"H6B2AGIG5HA8C65G2BGD1BG09E44H17I94C9CF4",
"8E8438GGCD99B9BC949B5397A498C98G8E7339A",
"H8H86HDE680040459A92B6IF09IH49ICI8F6791",
"8GGGEEC9BE804449F00C48FF6A8HCE8CCHECDGA",
"HDEEAA6049H08899A1149HBBE0IF69I56GA68E1",
"8C9A62764E788GI90225E7A4759FCG8EBD87ED6"};
const string lattice[]={
"H31DHBE3I12073ECF97D","CB45CA78CA327A8895HB",
"639B51FH5174F0HGIBF4","A9D1767ED68BA68FGB8A",
"2073ECF97DH31DHBE3I1","327A8895HBCB45CA78CA",
"74F0HGIBF4639B51FH51","8BA68FGB8AA9D1767ED6"};
const string alphabet="0123456789ABCDEFGHI";
int main(int argc,char**argv){
 if(argc<3){cerr<<"usage: gmp_pump L T [mutate] < (seed_L seed_Lplus1)\n";return 2;}
 int L=stoi(argv[1]),T=stoi(argv[2]);string a,b;
 if(!(cin>>a>>b))return 2;
 if(argc>3){int i=b.size()/2;b[i]=(b[i]=='9'?'0':char(b[i]+1));}
 mpz_class na(a,10),nb(b,10);
 int firstFront=-1,firstCore=-1,passes=0;
 for(int t=0;t<=T;t++){
  string sa=na.get_str(10),sb=nb.get_str(10);int n=sa.size(),m=sb.size();
  auto F=[&](const string&s){
   int z=s.size(),f=0;
   while(f<z/2){
    int want=alphabet.find(f<39?entrance[t%8][f]:lattice[t%8][(f-39)%20]);
    int actual=(s[f]-'0')+(s[z-1-f]-'0');
    if(want!=actual)break;f++;
   }return f;
  };
  int f=F(sa),g=F(sb);bool valid=(m==n+40&&g==f+20),core=valid;
  if(core)for(int i=f;i<n/2;i++){
   int x=(sa[i]-'0')+(sa[n-1-i]-'0'),j=i+20;
   int y=(sb[j]-'0')+(sb[m-1-j]-'0');
   if(x!=y){core=false;break;}
  }
  if(!valid&&firstFront<0)firstFront=t;
  if(!core&&firstCore<0)firstCore=t;
  if(core)passes++;
  if(t==0||t==100||t==1000||t==T||t==firstCore||t==firstFront)
   cout<<"checkpoint L="<<L<<" t="<<t<<" frontA="<<f<<" frontB="<<g<<" fullCore="<<core<<"\n";
  if(t==T)break;
  string ra(sa.rbegin(),sa.rend()),rb(sb.rbegin(),sb.rend());
  na+=mpz_class(ra,10);nb+=mpz_class(rb,10);
 }
 cout<<"PUMP L="<<L<<" T="<<T<<" firstCore="<<firstCore
     <<" firstFront="<<firstFront<<" goodStates="<<passes<<"\n";
 if(argc>3)return firstCore==0?0:1;
 return (firstCore==11+88*L&&firstFront==12+88*L)?0:1;
}