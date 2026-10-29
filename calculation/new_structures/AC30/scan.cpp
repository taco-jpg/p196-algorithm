// Phase-9 endpoint-only genuine decimal reverse-and-add scanner.
// IMPORTANT: early rejection is allowed ONLY after actual t=120 endpoint mismatch.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>
using V=std::vector<uint8_t>;
struct Rows{std::array<V,12> b,w;std::array<int,12> g;};
Rows read(const std::string &p){
 std::ifstream f(p);if(!f)throw std::runtime_error("missing lattice");int x,pd,nb,m,base;f>>pd>>nb>>m>>base;
 if(pd!=12||nb!=34||m!=9||base!=10)throw std::runtime_error("unexpected header");
 Rows r;for(int&i:r.g)f>>i;
 for(auto &v:r.w){v.resize(9);for(auto &d:v){f>>x;d=x;}}
 for(int t=0;t<12;t++)for(int i=0;i<9;i++)f>>x;
 for(auto &v:r.b){v.resize(34);for(auto &d:v){f>>x;d=x;}}
 if(!f)throw std::runtime_error("bad input");return r;
}
void append(V &a,const V &b){a.insert(a.end(),b.begin(),b.end());}
void power(V &a,const V &b,int exp){for(int i=0;i<exp;i++)append(a,b);}
V templ(const V &b,const V &w,const V&j,const V&u,const V&c,int q,int k){
 V h;h.reserve(34+9*q+j.size()+3*k);append(h,b);power(h,w,q);append(h,j);power(h,u,k);
 V p=h;append(p,c);for(auto it=h.rbegin();it!=h.rend();it++)p.push_back(*it);return p;
}
V realize(const V &p){V d(p.size());size_t n=p.size();for(size_t i=0;i<n/2;i++){
 int x=p[i],hi=std::min(9,x),lo=x-hi;d[i]=lo;d[n-1-i]=hi;
 }if(n%2){int x=p[n/2];if(x%2)throw std::runtime_error("nonrealizable odd centre");d[n/2]=x/2;}
 if(d.back()==0)throw std::runtime_error("leading zero");return d;}
struct Stats{uint64_t total=0,returned=0,badlen=0,badclock=0,pal=0;std::map<int,uint64_t> mismatch;std::map<int,uint64_t> first_bad_g_step;};
int check(const V &b,const V &w,const V&j,const V&u,const V&c,int q,int k, Stats &s, bool requireclock=true){
 V initial=templ(b,w,j,u,c,q,k),expect=templ(b,w,j,u,c,q,k+5);
 V d=realize(initial),next;next.reserve(d.size()+32);
 int gam_seen=0;bool g_ok=true;bool palindrome=false;int phase=9;
 for(int t=0;t<120;t++){
  // Canonical source positive and ordinary digits; no pairword local approximations.
  if(d.size()==1||std::equal(d.begin(),d.begin()+d.size()/2,d.rbegin()))palindrome=true;
  next.resize(d.size());int carry=0;auto n=d.size();
  for(size_t i=0;i<n;i++){int z=d[i]+d[n-1-i]+carry;next[i]=z%10;carry=z/10;}
  if(carry){next.push_back(carry);gam_seen++;}
  int expected_g=((t+phase)%4==0)?1:0; // lattice g=(1000)^3 and phase offset 9
  if(carry!=expected_g){g_ok=false;s.first_bad_g_step[t]++;}
  d.swap(next);
 }
 s.total++;if(!g_ok)s.badclock++;if(palindrome)s.pal++;
 if(d.size()!=expect.size())s.badlen++;
 int first=-1;
 for(size_t i=0;i<std::min(d.size(),expect.size());i++){
  if(int(d[i])+int(d[d.size()-1-i])!=expect[i]){first=int(i);break;}
 }
 if(first==-1&&d.size()!=expect.size())first=int(std::min(d.size(),expect.size()));
 if(first==-1){s.returned++;if(!g_ok||palindrome)std::cerr<<"RETURN_NOT_FULL_CERT_WARNING\n";}
 else s.mismatch[first]++;
 return first;
}
int main(int argc,char**argv){
 if(argc<5){std::cerr<<"usage: scan lattice MODE COUNT SEED [q k] ; MODE=random|slice|single\n";return 2;}
 auto r=read(argv[1]);std::string mode=argv[2];uint64_t count=std::stoull(argv[3]),seed=std::stoull(argv[4]);
 int q=(argc>5)?std::stoi(argv[5]):14,k=(argc>6)?std::stoi(argv[6]):100;
 uint64_t offset=(argc>7)?std::stoull(argv[7]):0;
 V b=r.b[9],w=r.w[9];std::array<V,2> cs{V{4,14,4},V{4,4}};
 std::array<V,30> us;for(int a=0;a<=18;a+=2){V v{9,(uint8_t)a,(uint8_t)(18-a)};
  for(int z=0;z<3;z++)us[(a/2)*3+z]=V{v[z],v[(z+1)%3],v[(z+2)%3]};}
 Stats st;uint64_t state=seed;
 auto ran=[&]()->uint64_t {state^=state>>12;state^=state<<25;state^=state>>27;return state*2685821657736338717ULL;};
 for(uint64_t i=0;i<(mode=="exact"?1:count);i++){
  V J(5);int uix=0,cix=0;
  if(mode=="random"){
   for(auto &d:J)d=ran()%19;uix=ran()%30;cix=ran()%2;
  }else if(mode=="slice"){
   // Exhaust 19^3 combinations for each U and both C for fixed top two J digits seed%361.
   uint64_t z=(i+offset)%6859;for(int j=2;j<5;j++){J[j]=z%19;z/=19;}
   J[0]=seed%19;J[1]=(seed/19)%19;uix=((i+offset)/6859)%30;cix=((i+offset)/(6859*30))%2;
  }else if(mode=="oddgate"){
   uint64_t z=(i+offset)%2476099ULL;for(auto &d:J){d=z%19;z/=19;}
   int a=int(J[0])-int(J[1])+int(J[2])-int(J[3])+int(J[4]);
   if(((a%11)+11)%11!=3)continue;
   uix=((i+offset)/2476099ULL)%2?28:0;cix=0;
  }else if(mode=="exact"){
   uint64_t z=seed;for(auto &d:J){d=z%19;z/=19;}uix=(count-1)%30;cix=(count-1)/30;
  }else if(mode=="single"){
   uint64_t z=i+offset;for(auto &d:J){d=z%19;z/=19;}
   uix=seed%30;cix=(seed/30)%2;
  }else {throw std::runtime_error("bad mode");}
  check(b,w,J,us[uix],cs[cix],q,k,st);
 }
 std::cout<<"mode="<<mode<<" count="<<count<<" seed="<<seed<<" offset="<<offset<<" q="<<q<<" k="<<k<<" return="<<st.returned<<" badlen="<<st.badlen<<" badclock="<<st.badclock<<" palindrome="<<st.pal<<"\n";
 for(auto [ix,n]:st.mismatch)std::cout<<"first_mismatch="<<ix<<" count="<<n<<"\n";
 for(auto [ix,n]:st.first_bad_g_step)std::cout<<"bad_clock_step="<<ix<<" count="<<n<<"\n";
}
