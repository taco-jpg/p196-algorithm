// Exhaustive 19^2 central packets; ordinary digit-list arithmetic.
// g++ -O3 -std=c++17 universe.cpp -o universe && ./universe
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <string>
#include <vector>
using namespace std;using Word=vector<uint8_t>;
constexpr int pre[39]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
constexpr int cyc[20]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
Word seed(int h,int a,int b){Word d(2*h);for(int i=0;i<h;i++){int p=i<39?pre[i]:cyc[(i-39)%20];if(i==h-2)p=a;if(i==h-1)p=b;d[i]=max(0,p-9);d[2*h-1-i]=p-d[i];}return d;}
Word pairs(Word const&d){Word p(d.size());for(int i=0,n=d.size();i<n;i++)p[i]=d[i]+d[n-1-i];return p;}
int step(Word&d){int n=d.size(),c=0;Word e(n+1);for(int i=0;i<n;i++){int s=d[i]+d[n-1-i]+c;e[i]=s%10;c=s/10;}if(c)e[n]=c;else e.resize(n);d.swap(e);return c;}
struct Head{int f=-1;string patch;};
int main(){
 constexpr int h=500,T=1500;
 Word canonical=seed(h,cyc[(h-2-39)%20],cyc[(h-1-39)%20]);array<Word,8> phases;
 for(int t=0;t<8;t++){phases[t]=pairs(canonical);step(canonical);}
 int minfront=h,lastfailure=-1,late=0,badpal=-1,badodd=-1,badgamma=-1;map<string,int> headtypes;
 for(int a=0;a<19;a++)for(int b=0;b<19;b++){
  Word d=seed(h,a,b);array<Head,44> hist;
  for(int t=0;t<=T;t++){
   Word p=pairs(d);int n=d.size(),f=min(h-50,n/2);
   for(int j=0;j<f;j++)if(p[j]!=phases[t%8][j]){f=j;break;}
   minfront=min(minfront,f);
   bool odd=false,pal=true;for(int j=0;j<min(f,39);j++)odd|=(p[j]&1);
   for(int j=0;j<n/2;j++)if(d[j]!=d[n-1-j]){pal=false;break;}
   if(!odd&&badodd<0)badodd=19*a+b;if(pal&&badpal<0)badpal=19*a+b;
   Head cur;cur.f=f;if(f>=20&&f+40<n/2)for(int j=-20;j<40;j++)cur.patch+=char('A'+p[f+j]);
   if(t==800)headtypes[cur.patch]++;
   if(t>=644){Head const&past=hist[t%44];if(f!=past.f-10||cur.patch.size()!=60||cur.patch!=past.patch)lastfailure=max(lastfailure,t);}
   if(t>=716)late++;hist[t%44]=move(cur);
   if(t<T){int gamma=step(d);if(gamma!=(t%2==0)&&badgamma<0)badgamma=19*a+b;}
  }
 }
 cout<<"digit-list 19^2=361 complete: T="<<T<<" minfront="<<minfront<<" last_44_failure="<<lastfailure<<" late_checks="<<late<<" distinct_heads_at_800="<<headtypes.size()<<" palfail="<<badpal<<" oddfail="<<badodd<<" overflowfail="<<badgamma<<"\n";
 for(auto const &kv:headtypes)cout<<kv.second<<","<<kv.first<<"\n";
 return (lastfailure>=716||minfront<39||badpal>=0||badodd>=0||badgamma>=0||headtypes.size()!=27)?1:0;
}