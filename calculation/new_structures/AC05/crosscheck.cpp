#define main census_cli
#include "census.cpp"
#undef main
#include <random>
int main(){
 std::mt19937_64 rng(0xAC050476);size_t tests=0,fail=0,fallback=0;
 for(int L=7;L<=14;L++)for(int u=0;u<3;u++){
  PortModel pm(u,L,14,100,160);
  for(int i=0;i<240;i++){
   V c(L);for(int j=0;j<(L+1)/2;j++){
    int x=(j==L/2&&(L&1))?2*(rng()%10):(rng()%19);
    c[j]=c[L-1-j]=x;
   }
   int offset,clk,portbad=0;
   bool a=run(u,c,14,100,160,&offset,&clk);
   bool b=pm.fast(u,c,&portbad);
   if(a!=b||!clk){std::cerr<<"FAILED u "<<u<<" L "<<L<<" i "<<i<<"\n";fail++;}
   fallback+=(portbad>0);tests++;
  }
  std::cout<<"CHECK u="<<u<<" L="<<L<<" cumulative="<<tests<<" errors="<<fail<<" fallbacks="<<fallback<<"\n";
 }
 return fail>0;
}
