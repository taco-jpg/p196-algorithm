// Independent mpz big-integer enumeration of all 361 packets; no shared digit-list step.
#include <gmp.h>
#include <algorithm>
#include <array>
#include <cstring>
#include <iostream>
#include <set>
#include <string>
#include <vector>
using namespace std;
const int pre[39]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
const int bulk[20]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
string initial(int h,int a,int b){string high,low;for(int i=0;i<h;i++){int p=i<39?pre[i]:bulk[(i-39)%20];if(i==h-2)p=a;if(i==h-1)p=b;int lo=max(0,p-9);high+=char('0'+p-lo);low+=char('0'+lo);}reverse(low.begin(),low.end());return high+low;}
string dec(mpz_t x){string z(mpz_sizeinbase(x,10)+3,'\0');mpz_get_str(z.data(),10,x);z.resize(strlen(z.c_str()));return z;}
int coef(const string &s,int i){return s[i]-'0'+s[s.size()-i-1]-'0';}
struct H {int f=-1;string w;};
int main(){
 const int h=500,T=1500;int a0=bulk[(h-2-39)%20],b0=bulk[(h-1-39)%20];mpz_t n,rev;mpz_inits(n,rev,NULL);
 mpz_set_str(n,initial(h,a0,b0).c_str(),10);array<vector<int>,8> ref;
 for(int t=0;t<8;t++){string s=dec(n);for(int j=0;j<h-50;j++)ref[t].push_back(coef(s,j));
  string rv=s;reverse(rv.begin(),rv.end());mpz_set_str(rev,rv.c_str(),10);mpz_add(n,n,rev);}
 int minfront=h,lastbad=-1,badpal=-1,badodd=-1,badgamma=-1,comp=0;set<string> heads800;
 for(int a=0;a<19;a++)for(int b=0;b<19;b++){
  mpz_set_str(n,initial(h,a,b).c_str(),10);array<H,44> hist;
  for(int t=0;t<=T;t++){
   string s=dec(n);int L=s.size(),front=min(h-50,L/2);
   for(int i=0;i<front;i++)if(coef(s,i)!=ref[t%8][i]){front=i;break;}
   minfront=min(minfront,front);
   bool odd=false,pal=true;for(int i=0;i<min(front,39);i++)odd|=(coef(s,i)&1);
   for(int i=0;i<L/2;i++)if(s[i]!=s[L-1-i]){pal=false;break;}
   if(!odd&&badodd<0)badodd=19*a+b;if(pal&&badpal<0)badpal=19*a+b;
   H now;now.f=front;if(front>=20&&front+40<L/2)for(int j=-20;j<40;j++)now.w+=char('A'+coef(s,front+j));
   if(t==800)heads800.insert(now.w);
   if(t>=644){H const&prev=hist[t%44];if(front!=prev.f-10||now.w.size()!=60||now.w!=prev.w)lastbad=max(lastbad,t);}
   if(t>=716)comp++;hist[t%44]=move(now);
   if(t<T){string sr=s;reverse(sr.begin(),sr.end());mpz_set_str(rev,sr.c_str(),10);mpz_add(n,n,rev);
    int g=(int)dec(n).size()-L;if(g!=(t%2==0)&&badgamma<0)badgamma=19*a+b;}
  }
 }
 cout<<"GMP exhaustive 361 cases: T="<<T<<" minfront="<<minfront<<" last_44_failure="<<lastbad<<" complete_late_checks="<<comp<<" distinct_head800="<<heads800.size()<<" badpal="<<badpal<<" badodd="<<badodd<<" badgamma="<<badgamma<<"\n";
 mpz_clears(n,rev,NULL);return (lastbad>=716||minfront<39||badpal>=0||badodd>=0||badgamma>=0||heads800.size()!=27)?1:0;
}