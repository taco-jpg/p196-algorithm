#include <boost/multiprecision/cpp_int.hpp>
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <fstream>
#include <filesystem>
#include <sstream>
#include <string>
#include <vector>
using boost::multiprecision::cpp_int;
using V = std::vector<int>;
const V B={10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
const V W={5,18,4,8,1,15,4,0,5};
cpp_int value(const V& d){cpp_int n=0;for(auto it=d.rbegin();it!=d.rend();++it){n*=10;n+=*it;}return n;}
V digits(cpp_int n){if(n==0)return V{0};V d;while(n>0){d.push_back((int)(n%10));n/=10;}return d;}
cpp_int reverse10(const cpp_int& n){std::string s=n.convert_to<std::string>();cpp_int r=0;for(auto it=s.rbegin();it!=s.rend();++it){r*=10;r+=(*it-'0');}return r;}
V reverse_word(V x){std::reverse(x.begin(),x.end());return x;}
V repeat(const V& w,int n){V r;r.reserve(w.size()*n);for(int i=0;i<n;i++)r.insert(r.end(),w.begin(),w.end());return r;}
V tpl(int q,int k,const V& J,const V& U,const V& C){V h=B;V wq=repeat(W,q),uk=repeat(U,k);h.insert(h.end(),wq.begin(),wq.end());h.insert(h.end(),J.begin(),J.end());h.insert(h.end(),uk.begin(),uk.end());V out=h;out.insert(out.end(),C.begin(),C.end());V rh=reverse_word(h);out.insert(out.end(),rh.begin(),rh.end());return out;}
V realize(const V& p){V d(p.size());for(size_t i=0;i<p.size()/2;i++){assert(p[i]>=0&&p[i]<=18);int hi=std::min(9,p[i]),lo=p[i]-hi;assert(lo>=0&&lo<=9);d[i]=lo;d[p.size()-1-i]=hi;}if(p.size()%2){int m=p[p.size()/2];assert(m%2==0&&m>=0&&m<=18);d[p.size()/2]=m/2;}assert(d.back()>0);return d;}
V pairword(const V& d){V p(d.size());for(size_t i=0;i<d.size();i++)p[i]=d[i]+d[d.size()-1-i];return p;}
long long sumv(const V& v){return std::accumulate(v.begin(),v.end(),0LL);}
long long valmod(const V& p,long long mod){long long z=0,pow=1;for(int x:p){z=(z+(long long)x*pow)%mod;pow=(pow*10)%mod;}return z;}
long long projection(const V& p){long long S=sumv(p),N=p.size();assert(((N-1)*S)%2==0);return (S+9*(((N-1)*S/2)%9))%81;}
struct Result {int q,k;bool ret;int mismatch;int overflows;long long S0,S120;long long Kmod81,Kneed81;cpp_int K,Kneed;long long gap;};
Result run(const std::string& name,int q,int k,const V& J,const V& U,const V& C){
  V P0=tpl(q,k,J,U,C);V target=tpl(q,k+5,J,U,C);V d=realize(P0);cpp_int n=value(d);assert(pairword(d)==P0);
  long long S0=sumv(P0);assert(S0==2*sumv(d));cpp_int K=0;int overflows=0;std::vector<int> gam;
  for(int t=0;t<120;t++){
    long long St=2*sumv(d);V out;out.reserve(d.size()+1);int carry=0,cc=0;
    for(size_t i=0;i<d.size();i++){int z=d[i]+d[d.size()-1-i]+carry;carry=z/10;cc+=carry;out.push_back(z%10);}
    if(carry){out.push_back(carry);overflows++;}
    cpp_int nn=n+reverse10(n);assert(nn==value(out));
    K += cpp_int(cc) << (119-t);
    long long Sn=2*sumv(out);assert(Sn==2*St-18LL*cc);
    assert(digits(nn)==out);
    gam.push_back((int)out.size()-(int)d.size());d.swap(out);n=nn;
  }
  V P120=pairword(d);long long S120=sumv(P120);assert(S120==2*sumv(d));
  int mismatch=-1;for(size_t i=0;i<std::min(P120.size(),target.size());i++)if(P120[i]!=target[i]){mismatch=(int)i;break;}if(mismatch<0&&P120.size()!=target.size())mismatch=(int)std::min(P120.size(),target.size());
  cpp_int pow120=cpp_int(1)<<120;cpp_int numer=(pow120-1)*S0-270;assert(numer%18==0);cpp_int Kneed=numer/18;
  assert(cpp_int(S120)==pow120*S0-18*K);
  long long kmod=(K%81).convert_to<long long>();long long needmod=((7*(S0%81)-15)%81+81)%81;
  assert((Kneed%81).convert_to<long long>()==needmod);
  long long gap=S120-S0-270;assert(cpp_int(gap)==18*(Kneed-K));
  assert((valmod(P0,81)==projection(P0)));assert(valmod(P120,81)==projection(P120));
  assert(overflows==30);for(int t=0;t<120;t++)assert(gam[t]==((t%4==0)?1:0));
  std::cout<<name<<" q="<<q<<" k="<<k<<" digits="<<P0.size()<<" overflows="<<overflows
           <<" return="<<(P120==target)<<" first_mismatch="<<mismatch
           <<" Kmod81="<<kmod<<" required="<<needmod<<" gate="<<(kmod==needmod)
           <<" mass_gap="<<gap<<" Kdiff="<<(Kneed-K)<<"\n";
  return {q,k,P120==target,mismatch,overflows,S0,S120,kmod,needmod,K,Kneed,gap};
}
int main(){
  assert(B.size()==34&&sumv(B)==307&&W.size()==9&&sumv(W)==60);
  // Cross-check the literal rooted exterior and phase-0 W word against the repository data.
  std::filesystem::path data=std::filesystem::path(__FILE__).parent_path()/"../../decimal_frontier/lattice_kinks/data/lat_p12m9.txt";
  std::ifstream in(data);
  if(!in.good()){data=std::filesystem::path("/mnt/data/S20/lat_p12m9.txt");in.clear();in.open(data);}
  assert(in.good()); std::vector<int> raw; int token; while(in>>token)raw.push_back(token);
  assert(raw.size()>=232+34); assert(raw[0]==12&&raw[1]==34&&raw[2]==9&&raw[3]==10);
  V Wfile(raw.begin()+16,raw.begin()+25); V Bfile(raw.begin()+232,raw.begin()+266);
  assert(Wfile==W&&Bfile==B);
  V J19={12,14,9,16,2,4,3,11,10,11,4,11,8,8,10,9,7,9,16};
  V U19={8,9,10};V C19={5,12,5};
  V Jeven={5};V Ueven={9,2,16};V Ceven={1,1};
  V Jodd={6};V Uodd={9,2,16};V Codd={12};
  for(int q:{20,40,80,160}){run("R02-J19",q,2*q,J19,U19,C19);run("even-C",q,2*q,Jeven,Ueven,Ceven);run("odd-C",q,2*q,Jodd,Uodd,Codd);}
  std::cout<<"PASS: rooted B/W cross-checked against lat_p12m9.txt; 12 genuine 120-step cpp_int reverse-add runs; independent LSD carry engine agrees every step; exact carry-mass identity and mod-729-derived K mod81 gate checked.\n";
}
