// N28: independent ordinary-digit orbit vs. exact paired-coefficient pumping checker.
// Coefficient representation P is least-significant-first, symmetric, entries 0..18.
// The independent orbit uses only source digits and direct addition of their reverse.
#include <vector>
#include <cstdint>
#include <iostream>
#include <algorithm>
#include <cstdlib>
#include <string>
#include <cassert>
using D = std::vector<unsigned char>;
static D pairstep(const D& p, D& carries, int& gam) {
  D digits;digits.reserve(p.size()+1);carries.clear();carries.reserve(p.size()+1);
  int c=0;carries.push_back(0);
  for(auto x:p){int s=x+c;digits.push_back(s%10);c=s/10;carries.push_back(c);}
  if(c)digits.push_back(c);
  gam=int(digits.size())-int(p.size());
  return digits;
}
static D ordinary_step(const D& a) {
  const size_t n=a.size();D v;v.reserve(n+1);int c=0;
  for(size_t i=0;i<n;++i){int s=a[i]+a[n-1-i]+c;v.push_back(s%10);c=s/10;}
  if(c)v.push_back(c);
  return v;
}
static bool palindrome(const D& a){for(size_t i=0;i<a.size()/2;++i)if(a[i]!=a[a.size()-1-i])return false;return true;}
static D pairsof(const D& a) {const size_t n=a.size();D p(n);for(size_t i=0;i<n;++i)p[i]=a[i]+a[n-1-i];return p;}
static D initial_p(int k) {
  D half={18,7,18,12};half.reserve(4+4*k);
  for(int i=0;i<k;++i)half.push_back(2);
  for(int i=0;i<k;++i){half.push_back(6);half.push_back(12);}
  for(int i=0;i<k;++i)half.push_back(18);
  D p=half;p.push_back(8);
  for(auto it=half.rbegin();it!=half.rend();++it)p.push_back(*it);
  return p;
}
static D initial_seed(const D& p){
  D d(p.size(),0);const size_t n=p.size();
  for(size_t i=0;i<n/2;++i){d[i]=p[i]/2;d[n-i-1]=p[i]-d[i];}
  d[n/2]=p[n/2]/2;return d;
}
static std::pair<D,int> emitted(const D& p, size_t index, size_t len, int carry){
  D e;e.reserve(len);
  for(size_t i=0;i<len;++i){int q=p[index+i]+carry;e.push_back(q%10);carry=q/10;}
  return {e,carry};
}
static uint64_t fnv(const D& x){uint64_t h=14695981039346656037ULL;for(auto z:x){h^=z;h*=1099511628211ULL;}return h;}
int main(int argc,char**argv){
  const int k=argc>1?std::atoi(argv[1]):25000;
  const int steps=argc>2?std::atoi(argv[2]):20000;
  if(k<10||steps<1)return 2;
  D p=initial_p(k),n=initial_seed(p);
  if(pairsof(n)!=p || palindrome(n)){std::cerr<<"invalid initial seed\n";return 2;}
  const size_t slots[]={size_t(4+k/2),size_t(4+2*k),size_t(4+3*k+k/2)};
  D words[3]={{2},{6,12},{18}};
  int gamcount=0;
  for(int t=0;t<steps;++t){
    if(pairsof(n)!=p){std::cerr<<"PAIR_MISMATCH t="<<t<<"\n";return 3;}
    D carries;int gam=0;D model=pairstep(p,carries,gam);
    const size_t N=p.size(),M=model.size();
    D nxt=ordinary_step(n);
    if(model!=nxt){std::cerr<<"ORDINARY_ARITHMETIC_MISMATCH t="<<t<<"\n";return 4;}
    if(palindrome(nxt)){std::cerr<<"PALINDROME t="<<t+1<<"\n";return 5;}
    bool anchor=false;for(size_t i=0;i<slots[0];++i)if(model[i]!=model[M-1-i]){anchor=true;break;}
    if(!anchor){std::cerr<<"NO_NONPAL_ANCHOR t="<<t<<"\n";return 6;}
    for(int j=0;j<3;++j){
      const size_t i=slots[j],m=words[j].size(),h=M-i,r=N-i;
      if(i+m>N/2||h+m>N||h<N/2){std::cerr<<"CUT_BOUNDS t="<<t<<" j="<<j<<"\n";return 7;}
      for(size_t z=0;z<m;++z)if(p[i+z]!=words[j][z]||p[r+z]!=words[j][m-1-z]){
        std::cerr<<"PERIOD_BREAK t="<<t<<" j="<<j<<"\n";return 8;
      }
      // gamma=1: high-side insertion cut is one digit right of the mirrored cut.
      // Sliding across one site is valid iff p[r]=p[r+m] within the m-periodic word.
      if(gam==1 && p[r]!=p[r+m]){std::cerr<<"SHIFT_BAD t="<<t<<" j="<<j<<"\n";return 9;}
      auto lo=emitted(p,i,m,carries[i]),hi=emitted(p,h,m,carries[h]);
      if(lo.second!=carries[i]||hi.second!=carries[h]){
        std::cerr<<"CARRY_LOOP_FAIL t="<<t<<" j="<<j<<"\n";return 10;
      }
      D v(m);
      for(size_t z=0;z<m;++z)v[z]=lo.first[z]+hi.first[m-1-z];
      words[j].swap(v);
    }
    if(gam)++gamcount;
    n.swap(nxt);p=pairsof(n);
    if(t==0||t==231||t==999||t==9999||t+1==steps)
      std::cout<<"STEP "<<t+1<<" digits="<<n.size()<<" gamma="<<gam<<" fnv64="<<fnv(n)<<" slots="<<slots[0]<<","<<slots[1]<<","<<slots[2]<<"\n";
  }
  std::cout<<"PASS base=10 steps="<<steps<<" k="<<k<<" digits="<<n.size()<<" overflows="<<gamcount<<" model_eq_every_step=1 triple_pump_every_step=1 nonpal_every_step=1\n";
}
