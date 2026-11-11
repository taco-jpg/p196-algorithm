// topproj: top_k.bin keys (u128 phase<<100 | cells 5 bit each, cell 0 = bottom cell of the k-window). Count distinct projections to the top d cells and to the bottom d cells.
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <vector>
#include <algorithm>
using namespace std;
typedef unsigned __int128 u128;
int main(int argc,char**argv){
  int k=atoi(argv[2]);
  FILE*f=fopen(argv[1],"rb");
  vector<u128> K; fseek(f,0,SEEK_END); long sz=ftell(f); fseek(f,0,SEEK_SET); K.resize(sz/16); fread(K.data(),16,K.size(),f); fclose(f);
  printf("k=%d keys=%zu; top-d projection counts:",k,K.size());
  for(int d=1;d<=k;d++){
    vector<u128> P; P.reserve(K.size());
    for(auto s:K){ u128 ph=s>>100; u128 cells=(s&(((u128)1<<100)-1)); // take top d cells: cells index k-d..k-1
      u128 t=(cells>>(5*(k-d))); P.push_back((ph<<100)|t);} 
    sort(P.begin(),P.end()); P.erase(unique(P.begin(),P.end()),P.end());
    printf(" %zu",P.size());
  }
  printf("\n");
}
