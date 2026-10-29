// AC34 exact endpoint-only physical scan. No strict-phase W9 or modular pruning.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
using Vec=std::vector<uint8_t>;
// Exact published phase-1 rows, checked against lat_p12m9.txt by phase1_gate.py.
constexpr int B[]={1,5,10,12,13,10,3,7,14,11,4,2,3,9,15,7,9,15,11,14,13,13,14,5,5,13,11,11,9,5,10,10,4,5};
constexpr int W[]={10,14,13,12,9,7,10,4,5};
void append(Vec& a,const Vec& b){a.insert(a.end(),b.begin(),b.end());}
void power(Vec& a,const Vec& w,int k){for(int i=0;i<k;i++)append(a,w);}
Vec templ(const Vec& J,const Vec& U,const Vec& C,int q,int k){
 Vec h;for(int x:B)h.push_back(x);for(int i=0;i<q;i++)for(int x:W)h.push_back(x);
 append(h,J);power(h,U,k);Vec p=h;append(p,C);std::reverse(h.begin(),h.end());append(p,h);return p;
}
Vec realize(const Vec& p){
 Vec d(p.size());
 for(size_t i=0;i<d.size()/2;i++){d[i]=std::max(0,int(p[i])-9);d[d.size()-1-i]=std::min(9,int(p[i]));}
 if(d.size()%2)d[d.size()/2]=p[d.size()/2]/2;
 return d;
}
int orbit(Vec d,Vec& output){
 Vec next(d.size()+121);int total=0;
 for(int t=0;t<120;t++){
  int carry=0;size_t n=d.size();
  for(size_t i=0;i<n;i++){int s=d[i]+d[n-1-i]+carry;next[i]=s%10;carry=s/10;}
  if(carry)next[n]=carry;
  total+=carry;next.resize(n+carry);d.swap(next);next.resize(d.size()+121);
 }
 output.resize(d.size());for(size_t i=0;i<d.size();i++)output[i]=d[i]+d[d.size()-1-i];
 return total;
}
int first(const Vec& a,const Vec& b){
 size_t i=0;while(i<std::min(a.size(),b.size())&&a[i]==b[i])++i;
 return i==a.size()&&i==b.size()?-1:int(i);
}
int main(int argc,char** argv){
 if(argc<6){std::cerr<<"usage: scan j0 stride upper_index first_index parity(0/1/2) [U_first U_end]\n";return 2;}
 int j0=std::atoi(argv[1]),stride=std::atoi(argv[2]),end=std::atoi(argv[3]),start=std::atoi(argv[4]),parity=std::atoi(argv[5]);
 int lo=(argc>6?std::atoi(argv[6]):0),hi=(argc>7?std::atoi(argv[7]):30);
 if(j0<0||j0>18||stride<1||lo<0||hi>30||lo>hi)return 2;
 std::array<long long,2000> hist{};long long trials=0,found=0,clockSumFail=0;
 const Vec centres[2]={{4,4},{4,14,4}};
 for(int rank=lo;rank<hi;rank++){
  int a=2*(rank/3);Vec base={9,uint8_t(a),uint8_t(18-a)};
  Vec U={base[rank%3],base[(rank+1)%3],base[(rank+2)%3]};
  for(int z=start;z<end;z+=stride){
   int x=z;Vec J(6);J[0]=j0;
   for(int j=1;j<6;j++){J[j]=x%19;x/=19;}
   if(x)break;
   for(int c=0;c<2;c++){
    if(parity!=2 && parity!=c)continue;
    Vec p=templ(J,U,centres[c],14,100),expect=templ(J,U,centres[c],14,105),got;
    int gamma=orbit(realize(p),got),m=first(got,expect);
    trials++;if(gamma!=30)clockSumFail++;
    if(m==-1){found++;std::cout<<"FOUND U_rank="<<rank+1<<" J=";for(auto v:J)std::cout<<int(v)<<",";std::cout<<" centre="<<c<<"\n";}
    else if(m<int(hist.size()))hist[m]++;
   }
  }
 }
 std::cout<<"trials="<<trials<<" returns="<<found<<" gamma_sum_fail="<<clockSumFail<<" mismatch_hist=";
 for(size_t i=0;i<hist.size();i++)if(hist[i])std::cout<<i<<":"<<hist[i]<<",";
 std::cout<<"\n";
}
