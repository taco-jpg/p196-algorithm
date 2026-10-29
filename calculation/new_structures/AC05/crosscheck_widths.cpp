#define main census_main
#include "census.cpp"
#undef main
#include <random>
int main(){
 std::mt19937_64 rng(0xAC050476);int count=0,fail=0,fall=0;
 for(auto [q,k]:vector<pair<int,int>>{{14,100},{20,80},{40,160},{80,320},{160,640}}){
  for(int L=7;L<=14;L++)for(int u=0;u<3;u++){
   PortModel pm(u,L,q,k,152+L);
   for(int i=0;i<20;i++){
    V c(L);for(int j=0;j<(L+1)/2;j++){
     int x=(j==L/2&&(L&1))?2*(rng()%10):(rng()%19);
     c[j]=c[L-j-1]=x;
    }
    int offset=0,clock=0,pb=0;
    bool a=run(u,c,q,k,152+L,&offset,&clock),b=pm.fast(u,c,&pb);
    if(a!=b||!clock)fail++;
    if(pb)fall++;
    count++;
   }
  }
  cout<<"WIDTH q="<<q<<" k="<<k<<" count="<<count<<" mismatch="<<fail<<" fallback="<<fall<<"\n";
 }
 return fail>0;
}
