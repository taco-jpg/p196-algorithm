// Exact two-sided decimal digit transducer for U ++ 9^L ++ V.
// L is symbolic: all exterior steps and carry schedules are independent of its initial size.
// Requires L>=2, and verifies each resulting state is nonpalindromic.
#include <cstdint>
#include <cstdlib>
#include <vector>
#include <algorithm>
#include <iostream>
using namespace std;
int main(int argc,char**argv){
 int Qmin=(argc>1)?atoi(argv[1]):6016,steps=(argc>2)?atoi(argv[2]):20000;
 vector<int> U={4,3},V={2,1};
 long long L=2LL*Qmin,minL=L;
 int trimCount=0,off0=0,off1=0;
 for(int t=0;t<=steps;t++){
  int a=(int)U.size();
  if(U.size()!=V.size()||V.empty()||L<2||V.back()==0){cerr<<"invalid band t="<<t<<" L="<<L<<"\n";return 2;}
  bool pal=true;for(int i=0;i<a;i++)if(U[i]!=V[a-1-i]){pal=false;break;}
  if(pal){cerr<<"PALINDROME t="<<t<<"\n";return 3;}
  minL=min(minL,L);if(t==steps)break;
  vector<int>lo,hi;lo.reserve(a+1);hi.reserve(a+1);
  int c=0;
  for(int i=0;i<a;i++){int s=U[i]+V[a-1-i]+c;lo.push_back(s%10);c=s/10;}
  int z=8+c;c=1;
  for(int j=0;j<a;j++){int s=V[j]+U[a-1-j]+c;hi.push_back(s%10);c=s/10;}
  int gamma=c;vector<int>Un=lo,Vn;Un.push_back(z);
  if(gamma==0){Vn.push_back(9);Vn.insert(Vn.end(),hi.begin(),hi.end());L-=2;off0++;}
  else{Vn=hi;Vn.push_back(1);L-=1;off1++;}
  while(!Un.empty()&&!Vn.empty()&&Un.back()==9&&Vn.front()==9){
   Un.pop_back();Vn.erase(Vn.begin());L+=2;trimCount++;
  }
  U.swap(Un);V.swap(Vn);
 }
 const int a=U.size();uint64_t hash=0;
 auto addchar=[&](int d){hash=(hash*131+(uint64_t)(48+d))%1000000007ULL;};
 for(int i=a-1;i>=0;i--)addchar(V[i]);
 for(long long i=0;i<L;i++)addchar(9);
 for(int i=a-1;i>=0;i--)addchar(U[i]);
 cout<<"PASS parametric neutral-9 transducer for ALL Q >= "<<Qmin<<" over "<<steps
 <<" steps; minL="<<minL<<" finalL="<<L<<" finalDigits="<<2*a+L
 <<" exteriorWidth="<<a<<" gamma0="<<off0<<" gamma1="<<off1
 <<" trim="<<trimCount<<" checksum="<<hash<<"\n";
}
