// acc_prefix: for a level file (K.bin) and lattice file, per layer: number of accepting states and distinct prefix counts per depth.
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <cstdint>
#include <cstring>
using namespace std;
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"r"); int BASE,tp,nB,m; fscanf(f,"%d %d %d %d",&BASE,&tp,&nB,&m);
  vector<int> clk(tp); for(auto&x:clk) fscanf(f,"%d",&x);
  vector<vector<int>> Bt(tp,vector<int>(nB)),W(tp,vector<int>(m));
  for(int t=0;t<tp;t++)for(int x=0;x<nB;x++)fscanf(f,"%d",&Bt[t][x]);
  for(int t=0;t<tp;t++)for(int x=0;x<m;x++)fscanf(f,"%d",&W[t][x]);
  fclose(f);
  FILE*g=fopen(argv[2],"rb"); int hdr[2]; fread(hdr,sizeof(int),2,g); int T=hdr[0],K=hdr[1];
  int D=argc>3?atoi(argv[3]):12; if(D>K)D=K;
  long total=0;
  for(int l=0;l<T;l++){
    int rec[4]; fread(rec,sizeof(int),4,g); int t=rec[0],j=rec[1],par=rec[2],n=rec[3];
    long acc=0; vector<long> cnt(D+1,0); static vector<uint8_t> prev; prev.assign(K,255);
    vector<uint8_t> buf(n*(size_t)K);
    fread(buf.data(),1,buf.size(),g);
    int lv=W[t][j];
    bool any=false;
    for(int i=0;i<n;i++){
      uint8_t*w=&buf[i*(size_t)K];
      if(w[0]==lv) continue;
      acc++;
      for(int d=1;d<=D;d++){ if(!any || memcmp(w,prev.data(),d)!=0) cnt[d]++; }
      memcpy(prev.data(),w,K); any=true;
    }
    total+=acc;
    if(acc){ printf("  (%d,%d,%d) g%d acc=%ld prefixes:",t,j,par,clk[t],acc); for(int d=1;d<=D;d++) printf(" %ld",cnt[d]); printf("\n"); }
  }
  printf("K=%d total accepting=%ld\n",K,total);
}
