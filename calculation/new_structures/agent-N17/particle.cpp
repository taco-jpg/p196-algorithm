// Literal little-endian digit-list decimal reverse-and-add; exact full-pair checks.
// g++ -O3 -std=c++17 particle.cpp -o particle && ./particle 8000 20000
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
using Word=vector<uint8_t>;
constexpr int pre[39]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
constexpr int cyc[20]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
Word seed(int h){Word x(2*h);for(int i=0;i<h;i++){int p=i<39?pre[i]:cyc[(i-39)%20];x[i]=max(0,p-9);x[2*h-1-i]=p-x[i];}return x;}
Word pairs(const Word&x){Word p(x.size());for(int i=0,n=x.size();i<n;i++)p[i]=x[i]+x[n-1-i];return p;}
int advance(Word&x){int n=x.size(),c=0;Word y(n+1);for(int i=0;i<n;i++){int s=x[i]+x[n-1-i]+c;y[i]=s%10;c=s/10;}if(c)y[n]=c;else y.resize(n);x.swap(y);return c;}
struct Head{int f=-1;string w;};
int main(int argc,char**argv){
 int h=argc>1?atoi(argv[1]):8000,T=argc>2?atoi(argv[2]):20000;if(h<150||T<1)return 2;
 Word d=seed(h);array<Word,8> ref;array<Head,44> hist;
 int minfront=h,firstpal=-1,firstodd=-1,firstgamma=-1,firstglider=-1,firstroot=-1,firstperiod=-1,glider_checks=0;
 cout<<"t,n,front,odd,gamma\n";
 for(int t=0;t<=T;t++){
  Word p=pairs(d);int n=d.size();if(t<8)ref[t]=p;
  if(t<8)for(int j=39;j<h-80;j++)if(p[j]!=p[j+20]){firstperiod=t;break;}
  int f=min(n/2,h-50);if(t>=8)for(int j=0;j<f;j++)if(p[j]!=ref[t%8][j]){f=j;break;}
  minfront=min(minfront,f);if(f<39&&firstroot<0)firstroot=t;
  int odd=-1;for(int j=0;j<min(f,39);j++)if(p[j]%2){odd=j;break;}
  if(odd<0&&firstodd<0)firstodd=t;
  bool pal=true;for(int j=0;j<n/2;j++)if(d[j]!=d[n-1-j]){pal=false;break;}
  if(pal&&firstpal<0)firstpal=t;
  Head now;now.f=f;
  if(f>=20&&f+40<n/2)for(int j=-20;j<40;j++)now.w.push_back(char('A'+p[f+j]));
  if(t>=644&&now.w.size()==60){const Head &old=hist[t%44];glider_checks++;
   if(f!=old.f-10||now.w!=old.w)if(firstglider<0)firstglider=t;
  }
  hist[t%44]=now;
  int gamma=0;if(t<T){gamma=advance(d);if(gamma!=(t%2==0)&&firstgamma<0)firstgamma=t;}
  if(t<16||t%1000==0||t==T)cout<<t<<","<<n<<","<<f<<","<<odd<<","<<gamma<<"\n";
 }
 cerr<<"h="<<h<<" T="<<T<<" minfront="<<minfront<<" glider_checks="<<glider_checks
     <<" bad_period="<<firstperiod<<" bad_glider="<<firstglider<<" bad_odd="<<firstodd
     <<" bad_root="<<firstroot<<" bad_overflow="<<firstgamma<<" palindrome="<<firstpal<<"\n";
 return (firstperiod>=0||firstglider>=0||firstodd>=0||firstroot>=0||firstgamma>=0||firstpal>=0)?1:0;
}