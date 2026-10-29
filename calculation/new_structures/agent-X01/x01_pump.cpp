// X01 exact two-sided decimal band transducer; Q is arbitrary while L>=2.
// g++ -O3 -std=c++17 x01_pump.cpp -o x01_pump
// ./x01_pump 49 59 4149 20000
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
using Digits=vector<uint8_t>;
static constexpr uint64_t MOD=1000000007;
uint64_t chash(const Digits& U,const Digits& V,long long L){
 uint64_t h=0;auto add=[&](int d){h=(h*131+(uint64_t)(d+48))%MOD;};
 for(int i=int(V.size())-1;i>=0;--i)add(V[i]);
 for(long long i=0;i<L;i++)add(9);
 for(int i=int(U.size())-1;i>=0;--i)add(U[i]);
 return h;
}
Digits reverse_dec(const string& s){
 Digits d;for(auto i=s.rbegin();i!=s.rend();++i){
  if(*i<'0'||*i>'9')throw runtime_error("bad cap");
  d.push_back(*i-'0');
 }return d;
}
int main(int argc,char**argv){
 if(argc<5){cerr<<"usage: x01_pump high low Q steps [strictlock]\n";return 2;}
 string hs=argv[1],ls=argv[2];int Q=atoi(argv[3]),T=atoi(argv[4]);
 bool strict=(argc<6||atoi(argv[5])!=0);
 if(Q<1||T<0||hs.size()!=ls.size()||hs[0]=='0')return 2;
 Digits U=reverse_dec(ls),V=reverse_dec(hs);
 long long L=2LL*Q,minL=L,extra=0,trimSum=0,g0=0,g1=0;
 int first_lock_failure=-1,first_bad=-1,first_pal=-1,max_trim=0;
 uint64_t pathhash=0;
 for(int t=0;t<=T;t++){
  if(V.empty()||V.back()==0||L<2||U.size()!=V.size()){first_bad=t;break;}
  int a=int(U.size());bool ispal=true;
  for(int i=0;i<a;i++)if(U[i]!=V[a-1-i]){ispal=false;break;}
  if(ispal){first_pal=t;break;}
  minL=min(minL,L);
  pathhash=(pathhash*1000003ULL+(uint64_t)(L%MOD)*17+uint64_t(a)*101+uint64_t(t))%MOD;
  if(t<=8||t==88||t==100||t==300||t==1000||t==5000||t==10000||
     t==20000||t==50000||t==100000||t==T)
   cout<<"STATE t="<<t<<" L="<<L<<" width="<<a<<" n="<<(2LL*a+L)
       <<" checksum="<<chash(U,V,L)<<" g1="<<g1<<" trim="<<trimSum
       <<" badlock="<<extra<<"\n";
  if(t==T)break;
  Digits lo,hi;lo.reserve(a+1);hi.reserve(a+1);int c=0;
  for(int i=0;i<a;i++){int s=U[i]+V[a-1-i]+c;lo.push_back(s%10);c=s/10;}
  int z=8+c;c=1;
  for(int j=0;j<a;j++){int s=V[j]+U[a-1-j]+c;hi.push_back(s%10);c=s/10;}
  int gamma=c;Digits Un=lo,Vn;Un.push_back(z);
  if(gamma){g1++;Vn=hi;Vn.push_back(1);L--;}
  else{g0++;Vn.push_back(9);Vn.insert(Vn.end(),hi.begin(),hi.end());L-=2;}
  int trims=0;
  while(trims<(int)Un.size()&&trims<(int)Vn.size()&&
        Un[Un.size()-1-trims]==9&&Vn[trims]==9)++trims;
  max_trim=max(max_trim,trims);
  if(trims!=1-gamma){if(first_lock_failure<0)first_lock_failure=t;extra++;}
  if(trims){
   Un.resize(Un.size()-trims);Vn.erase(Vn.begin(),Vn.begin()+trims);
   L+=2*trims;trimSum+=trims;
  }
  U.swap(Un);V.swap(Vn);
 }
 cout<<"TOTAL high="<<hs<<" low="<<ls<<" Q="<<Q<<" T="<<T
     <<" first_bad="<<first_bad<<" first_pal="<<first_pal
     <<" first_lock_failure="<<first_lock_failure<<" lock_violations="<<extra
     <<" minL="<<minL<<" finalL="<<L<<" gamma0="<<g0<<" gamma1="<<g1
     <<" trims="<<trimSum<<" max_trim="<<max_trim<<" pathhash="<<pathhash<<"\n";
 return (first_bad<0&&first_pal<0&&(!strict||first_lock_failure<0))?0:1;
}
