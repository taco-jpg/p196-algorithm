// W18: parameter-uniform two-wall decimal carry engine for the seed 5(99)^Q4.
// Reuses the sound local nine-band transfer rule; this seed and threshold are new.
// c++ -O3 -std=c++17 wall.cpp -o /tmp/w18-wall && /tmp/w18-wall 4138 20000
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
using Word=vector<uint8_t>;
static uint64_t hashWord(const Word &u,const Word &v,int L){
 uint64_t h=0;const uint64_t P=1000000007ULL;
 for(auto it=v.rbegin();it!=v.rend();++it)h=(131*h+(*it+'0'))%P;
 for(int j=0;j<L;j++)h=(131*h+'9')%P;
 for(auto it=u.rbegin();it!=u.rend();++it)h=(131*h+(*it+'0'))%P;
 return h;
}
int main(int argc,char**argv){
 int Q=argc>1?atoi(argv[1]):4138;
 int T=argc>2?atoi(argv[2]):20000;
 if(Q<1||T<0||T>1000000){cerr<<"invalid input\n";return 2;}
 Word U{4},V{5};int L=2*Q;int minL=L, minT=0, gammas=0, trims=0;
 auto check=[&](int t){
  if(L<2){cerr<<"BAND EXHAUSTED at t="<<t<<" L="<<L<<"\n";return false;}
  if(U.size()!=V.size() || equal(U.begin(),U.end(),V.rbegin())){
   cerr<<"PALINDROME/BROKEN EXTERIORS at t="<<t<<"\n";return false;
  }
  return true;
 };
 if(!check(0))return 3;
 for(int t=0;t<T;t++){
  const size_t n=U.size();Word low;low.reserve(n+1);
  int c=0;
  for(size_t i=0;i<n;i++){
   int z=U[i]+V[n-1-i]+c;low.push_back(z%10);c=z/10;
  }
  low.push_back(8+c);int hiCarry=1;Word high;high.reserve(n+1);
  for(size_t i=0;i<n;i++){
   int z=V[i]+U[n-1-i]+hiCarry;high.push_back(z%10);hiCarry=z/10;
  }
  Word newV;newV.reserve(n+1);
  if(!hiCarry)newV.push_back(9);
  newV.insert(newV.end(),high.begin(),high.end());
  if(hiCarry)newV.push_back(1);
  L-=hiCarry?1:2;gammas+=hiCarry;
  size_t uLen=low.size(),vStart=0;
  while(uLen && vStart<newV.size() && low[uLen-1]==9 && newV[vStart]==9){
   --uLen;++vStart;L+=2;++trims;
  }
  low.resize(uLen);U.swap(low);
  V.assign(newV.begin()+vStart,newV.end());
  if(L<minL){minL=L;minT=t+1;}
  if(!check(t+1))return 3;
  if(t+1==1 || t+1==100 || t+1==1000 || t+1==5000 || t+1==10000 || t+1==T){
   cout<<"checkpoint t="<<t+1<<" digits="<<2*U.size()+L
       <<" width="<<U.size()<<" band="<<L<<" hash="<<hashWord(U,V,L)<<"\n";
  }
 }
 cout<<"PASS Q="<<Q<<" T="<<T<<" min_band="<<minL<<" min_t="<<minT
     <<" final_digits="<<(2*U.size()+L)<<" final_band="<<L
     <<" trims="<<trims<<" overflow="<<gammas<<" final_hash="<<hashWord(U,V,L)<<"\n";
}
