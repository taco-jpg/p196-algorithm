// AC01 rooted p12/m9 centre-only search. Direct ordinary-decimal digit arrays;
// NO strict-phase W9 pruning. Full 120 steps, then central window equality.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <iomanip>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
static constexpr int B[]={10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
static constexpr int W[]={5,18,4,8,1,15,4,0,5};
static constexpr int U[3][3]={{9,0,18},{0,18,9},{18,9,0}};
static uint64_t ipow(uint64_t a,int b) {uint64_t r=1;while(b--)r*=a;return r;}
struct Runner {
 int q,k,u,n,rad;vector<uint8_t> a,b,wanted,coeff;uint64_t all=0, hits=0, clocks=0;
 uint64_t hash=1469598103934665603ULL;
 Runner(int uq,int nn,int qq=14,int kk=100):q(qq),k(kk),u(uq),n(nn),rad(122+nn+30){
   vector<int> half;
   for(int x:B)half.push_back(x);
   for(int j=0;j<q;j++)for(int x:W)half.push_back(x);
   half.push_back(5);
   for(int j=0;j<k;j++)for(int x:U[u])half.push_back(x);
   int N=2*int(half.size())+n;
   a.assign(N+121,0);b.assign(N+121,0);coeff.assign(N,0);wanted.assign(N+30,0);
   for(int i=0;i<int(half.size());i++){coeff[i]=half[i];coeff[N-1-i]=half[i];}
   for(int i=0;i<int(half.size());i++){wanted[i]=half[i];wanted[N+29-i]=half[i];}
 }
 bool check(const vector<int>& c){
   const int N=int(coeff.size());const int h=(N-n)/2;for(int i=0;i<n;i++)coeff[h+i]=c[i];
   for(int i=0;i<N/2;i++){int v=coeff[i],hi=min(9,v);a[i]=uint8_t(v-hi);a[N-1-i]=uint8_t(hi);}
   if(N&1){if(coeff[N/2]&1)throw runtime_error("odd centre midpoint");a[N/2]=uint8_t(coeff[N/2]/2);}
   int len=N,over=0;vector<uint8_t>*d=&a,*e=&b;
   for(int t=0;t<120;t++){
      int carry=0;for(int i=0;i<len;i++){
         int s=int((*d)[i])+int((*d)[len-1-i])+carry;
         (*e)[i]=uint8_t(s%10);carry=s/10;
      }
      if(carry){(*e)[len]=uint8_t(carry);len++;over++;}
      swap(d,e);
   }
   bool ok=(len==N+30 && over==30);
   const int centre=len/2;const int outHalf=(N+30-n)/2;
   if(ok)for(int i=max(0,centre-rad);i<min(len,centre+rad+1);i++){
      int want=0;
      if(i<outHalf){
        if(i<h)want=coeff[i];else want=U[u][(i-h)%3];
      }else if(i<outHalf+n)want=c[i-outHalf];
      else{
        int j=(N+29)-i;
        if(j<h)want=coeff[j];else want=U[u][(j-h)%3];
      }
      if(int((*d)[i])+int((*d)[len-1-i])!=want){ok=false;break;}
   }
   all++; if(ok){hits++; cerr<<"FOUND U="<<u<<" n="<<n<<" C=";for(int v:c)cerr<<v<<',';cerr<<'\n';}
   if(over!=30)clocks++;
   hash^=uint64_t((*d)[0])+31ULL*(*d)[len/2]+397ULL*(*d)[len-1]+8191ULL*len;
   hash*=1099511628211ULL;
   return ok;
 }
};
#ifndef AC01_NO_MAIN
int main(int argc,char**argv){
 if(argc<5){cerr<<"usage: census Uidx C_length OFFSET LIMIT [q k]\n";return 2;}
 int u=atoi(argv[1]),n=atoi(argv[2]);uint64_t off=stoull(argv[3]),limit=stoull(argv[4]);
 int q=argc>5?atoi(argv[5]):14,k=argc>6?atoi(argv[6]):100;
 if(u<0||u>2||n<1||n>24)throw runtime_error("bad U or C length");
 const uint64_t mid=n%2?10:1,total=ipow(19,n/2)*mid;
 if(off>total)throw runtime_error("offset too large");
 limit=min(limit,total-off);Runner r(u,n,q,k);vector<int> C(n);
 for(uint64_t j=off;j<off+limit;j++){
    uint64_t x=j;int h=n/2;
    if(n&1){C[h]=2*int(x%10);x/=10;}
    for(int i=0;i<h;i++){C[i]=C[n-1-i]=int(x%19);x/=19;}
    r.check(C);
 }
 cout<<"CELL U="<<u<<" C="<<n<<" offset="<<off<<" checked="<<r.all<<" total="<<total<<" matches="<<r.hits<<" clock_deviations="<<r.clocks<<" hash64="<<hex<<r.hash<<dec<<" q="<<q<<" k="<<k<<'\n';
}
#endif // AC01_NO_MAIN
