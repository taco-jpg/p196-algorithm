// AC46. Two-carry, actual-gamma inner window for arbitrary unknown outer pairword.
// A physical complete return requires the resulting protected central word
// to equal the central source word after U^k -> U^(k+5).
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <vector>
using V=std::vector<uint8_t>;
static constexpr int K=100;
static inline void norm(const V &x, int initial, V &d){
  d.resize(x.size());int c=initial;
  for(size_t i=0;i<x.size();i++){
    int z=x[i]+c;d[i]=z%10;c=z/10;
  }
}
static bool symmetric(const V &x){for(size_t i=0,n=x.size();i<n/2;i++)if(x[i]!=x[n-1-i])return false;return true;}
static inline std::pair<V,int> centre_step(const V &s,int gamma){
  V d0,d1;norm(s,0,d0);norm(s,1,d1);
  int m=(int)s.size(), n=m-gamma;
  V r0(n),r1(n);int trim=0;
  for(int j=0;j<n;j++){
    r0[j]=d0[gamma+j]+d0[m-1-j];
    r1[j]=d1[gamma+j]+d1[m-1-j];
    if(r0[j]!=r1[j])trim=std::max(trim,1+std::min(j,n-1-j));
  }
  assert(n>2*trim);
  V out(r0.begin()+trim,r0.end()-trim);
  assert(symmetric(out));
  return {std::move(out), gamma+trim};
}
static V repeat(const V&u,int k){V z;z.reserve(u.size()*k);for(int i=0;i<k;i++)z.insert(z.end(),u.begin(),u.end());return z;}
static V initial(const V&u,const V&c){V z=repeat(u,K);z.insert(z.end(),c.begin(),c.end());auto r=repeat(u,K);z.insert(z.end(),r.rbegin(),r.rend());return z;}
static std::pair<int,int> run(const V&u,const V&c){
  V s=initial(u,c);int shift=0;const int original=(int)s.size();
  for(int i=0;i<120;i++){
    auto [next,inc]=centre_step(s,(i%4==0));s=std::move(next);shift+=inc;
    assert(!s.empty());
  }
  assert((int)s.size()+2*shift==original+30);
  V target=repeat(u,K+5);
  target.insert(target.end(),c.begin(),c.end());
  auto rev=repeat(u,K+5);
  target.insert(target.end(),rev.rbegin(),rev.rend());
  int m=(int)c.size(),rmax=std::min({100,(int(s.size())-m)/2,(int(target.size())-m)/2});
  for(int r=0;r<=rmax;r++){
    int a=((int)s.size()-m)/2-r,b=((int)target.size()-m)/2-r;
    for(int j=0;j<m+2*r;j++)if(s[a+j]!=target[b+j])return {r,(int)s.size()};
  }
  return {-1,(int)s.size()};
}
int main(int argc,char**argv){
  int maxL=argc>1?std::atoi(argv[1]):4;
  assert(maxL>=1 && maxL<=8);
  long long total=0,hits=0;int minCore=10000;
  for(int length=1;length<=maxL;length++){
    long long ct=0;std::map<int,long long> histogram;
    int half=(length+1)/2;long long nc=1;
    for(int j=0;j<half;j++)nc*=19;
    for(int a=0;a<=18;a+=2){
      V q={9,(uint8_t)a,(uint8_t)(18-a)};
      for(int rot=0;rot<3;rot++){
        V u={q[rot],q[(rot+1)%3],q[(rot+2)%3]};
        for(long long code=0;code<nc;code++){
          long long v=code;V c(length);
          for(int j=0;j<half;j++){int x=v%19;v/=19;c[j]=c[length-1-j]=x;}
          if(length%2 && (c[half-1]&1))continue;
          auto [r,core]=run(u,c);
          if(r==-1){
            if(hits<8){std::cerr<<"SURVIVING core U=";for(int x:u)std::cerr<<x<<",";std::cerr<<" C=";for(int x:c)std::cerr<<x<<",";std::cerr<<"\n";}
            hits++;
          }
          histogram[r]++;ct++;minCore=std::min(minCore,core);
        }
      }
    }
    total+=ct;
    std::cout<<"length="<<length<<" cases="<<ct<<" hist=";
    for(auto [r,n]:histogram)std::cout<<r<<":"<<n<<",";
    std::cout<<" survivors="<<histogram[-1]<<" min_core="<<minCore<<"\n";
  }
  std::cout<<"TOTAL="<<total<<" SURVIVORS="<<hits<<"\n";
  return 0;
}
