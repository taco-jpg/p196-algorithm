// W18: three genuine decimal orbits across the first 9-band collision.
// c++ -O3 -std=c++17 seam_wave.cpp -o /tmp/w18sw && /tmp/w18sw 4138 25000
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;using W=vector<uint8_t>;
static W seed(int q){W a;a.push_back(4);a.insert(a.end(),2*q,9);a.push_back(5);return a;}
static W step(const W&a){W b;int c=0;size_t n=a.size();b.reserve(n+1);for(size_t i=0;i<n;i++){int z=a[i]+a[n-i-1]+c;b.push_back(z%10);c=z/10;}if(c)b.push_back(c);return b;}
static bool pal(const W&a){return equal(a.begin(),a.begin()+a.size()/2,a.rbegin());}
static string clip(const W&a,size_t at,size_t n){string s;for(size_t i=at;i<at+n&&i<a.size()&&s.size()<48;i++)s+=char('0'+a[i]);return s;}
struct Cut{size_t pre,suf,len0,len1;string x,y;};
static Cut diff(const W&a,const W&b){size_t i=0,j=0;while(i<a.size()&&i<b.size()&&a[i]==b[i])i++;while(j<a.size()-i&&j<b.size()-i&&a[a.size()-1-j]==b[b.size()-1-j])j++;return {i,j,a.size()-i-j,b.size()-i-j,clip(a,i,a.size()-i-j),clip(b,i,b.size()-i-j)};}
static uint64_t digest(const W&a){uint64_t h=0;for(auto it=a.rbegin();it!=a.rend();++it)h=(h*131+*it+'0')%1000000007ULL;return h;}
int main(int argc,char**argv){int q=argc>1?atoi(argv[1]):4138,T=argc>2?atoi(argv[2]):25000;if(q<2||T<1)return 2;
 W a=seed(q),b=seed(q+1),c=seed(q+2);int first01=-1,first12=-1;
 for(int t=0;t<=T;t++){
  if(pal(a)||pal(b)||pal(c)){cerr<<"PAL at t="<<t<<"\n";return 3;}
  Cut ab=diff(a,b),bc=diff(b,c);
  bool i01=(ab.len0==0&&ab.len1==2&&ab.y=="99");
  bool i12=(bc.len0==0&&bc.len1==2&&bc.y=="99");
  if(!i01&&first01<0)first01=t;if(!i12&&first12<0)first12=t;
  if(t==0||t==19990||t==20000||t==20004||t==20005||t==20006||t==20009||t==20010||t==20100||t==20500||t==21000||t==22000||t==23000||t==24000||t==25000){
   cout<<"t="<<t<<" lengths="<<a.size()<<","<<b.size()<<","<<c.size()
       <<" ab="<<ab.pre<<"/"<<ab.len0<<"+2/"<<ab.len1<<"/"<<ab.suf
       <<" bc="<<bc.pre<<"/"<<bc.len0<<"+2/"<<bc.len1<<"/"<<bc.suf
       <<" insert99="<<i01<<","<<i12;
   if(t==20006||t==20010)cout<<" ab_subst="<<ab.x<<"->"<<ab.y<<" bc_subst="<<bc.x<<"->"<<bc.y;
   cout<<" hashes="<<digest(a)<<","<<digest(b)<<","<<digest(c)<<"\n";
  }
  if(t!=T){a=step(a);b=step(b);c=step(c);}
 }
 cout<<"PASS Q="<<q<<" T="<<T<<" first_non99="<<first01<<","<<first12<<" all_nonpal=1\n";
}
