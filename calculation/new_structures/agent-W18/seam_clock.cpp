// W18: explore delayed birth of the postcollision seam packet across 40 padding levels.
// Uses the *exact* two-wall prefix to t=19990 (N23 lemma), then ordinary decimal digits.
// c++ -O3 -std=c++17 seam_clock.cpp -o /tmp/w18sc && /tmp/w18sc
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
using namespace std;using W=vector<uint8_t>;
static W step(const W&a){W b;int c=0;size_t n=a.size();for(size_t i=0;i<n;i++){int z=a[i]+a[n-1-i]+c;b.push_back(z%10);c=z/10;}if(c)b.push_back(c);return b;}
static bool pal(const W&a){return equal(a.begin(),a.begin()+a.size()/2,a.rbegin());}
int main(int argc,char**argv){int Q=4138,T=argc>1?atoi(argv[1]):19990,extra=argc>2?atoi(argv[2]):300;
 W U{4},V{5};int L=2*Q;
 for(int t=0;t<T;t++){
  size_t n=U.size();W lo;int c=0;for(size_t i=0;i<n;i++){int z=U[i]+V[n-1-i]+c;lo.push_back(z%10);c=z/10;}lo.push_back(8+c);
  W hi;int h=1;for(size_t i=0;i<n;i++){int z=V[i]+U[n-1-i]+h;hi.push_back(z%10);h=z/10;}
  W nv;if(!h)nv.push_back(9);nv.insert(nv.end(),hi.begin(),hi.end());if(h)nv.push_back(1);L-=h?1:2;
  size_t r=lo.size(),s=0;while(r&&s<nv.size()&&lo[r-1]==9&&nv[s]==9){--r;++s;L+=2;}lo.resize(r);U=lo;V.assign(nv.begin()+s,nv.end());
  if(L<2){cerr<<"band guard lost before snapshot\n";return 2;}
 }
 auto build=[&](int j){W a=U;a.insert(a.end(),L+2*j,9);a.insert(a.end(),V.begin(),V.end());return a;};
 vector<W> x;const int K=41;for(int i=0;i<K;i++)x.push_back(build(i));
 vector<int> first(K-1,-1);
 for(int t=0;t<=extra;t++){
  for(int i=0;i<K-1;i++)if(first[i]<0){
   const W&a=x[i],&b=x[i+1];size_t l=0,h=0;
   while(l<a.size()&&l<b.size()&&a[l]==b[l])l++;
   while(h<a.size()-l&&h<b.size()-l&&a[a.size()-1-h]==b[b.size()-1-h])h++;
   if(!(a.size()==l+h&&b.size()==l+h+2&&b[l]==9&&b[l+1]==9))first[i]=T+t;
  }
  if(t==extra)break;
  for(auto&y:x){if(pal(y)){cerr<<"palindrome in scan\n";return 3;}y=step(y);}
 }
 for(int i=0;i<K-1;i++)cout<<"Q="<<Q+i<<" first_non99="<<first[i]<<" delay="<<(i?first[i]-first[i-1]:0)<<"\n";
}
