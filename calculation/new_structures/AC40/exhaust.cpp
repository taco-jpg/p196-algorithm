// AC40: sound endpoint-only census, base ten pairword normalization.
// Every J (j0=0, j1..j5 in 0..18) and two fixed palindromic centres.
// No strict-phase W9 assumption or mod-11 pruning.
#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <omp.h>
#include <vector>

static constexpr int B[34]={5,2,7,12,0,3,14,15,5,9,0,9,3,4,18,11,9,15,9,10,14,10,5,12,0,17,9,16,1,14,1,14,4,17};
static constexpr int W[9]={11,9,12,2,9,2,4,0,17};
static constexpr int U[3]={9,0,18};
static constexpr int N=2476099; // 19^5, exact full first-symbol slice
struct Output {int site136,site137,gamma,pal;};
static Output calculate(int id, int parity, int q=14, int k=100) {
  uint8_t a[3500], b[3500],d[3500];
  int h=0;
  for(int x:B)a[h++]=x;
  for(int j=0;j<q;j++)for(int x:W)a[h++]=x;
  a[h++]=0;for(int j=5;j>=1;j--){a[34+9*q+j]=id%19;id/=19;}h+=5;
  for(int j=0;j<k;j++)for(int x:U)a[h++]=x;
  int full=h*2+2+parity;
  for(int i=0;i<h;i++)a[full-i-1]=a[i];
  if(parity==0){a[h]=4;a[h+1]=4;}
  else{a[h]=4;a[h+1]=14;a[h+2]=4;}
  int len=full,over=0;
  for(int t=0;t<120;t++) {
    int carry=0;
    for(int i=0;i<len;i++){int z=a[i]+carry;d[i]=z%10;carry=z/10;}
    if(carry){d[len]=carry;len++;over++;}
    for(int i=0;i<len;i++)b[i]=d[i]+d[len-1-i];
    std::copy_n(b,len,a);
  }
  return {a[136],a[137],over,0};
}
int main(int argc,char**argv) {
  int begin=argc>1?std::atoi(argv[1]):0;int end=argc>2?std::atoi(argv[2]):N;
  int nth=argc>3?std::atoi(argv[3]):5;
  assert(0<=begin&&begin<=end&&end<=N);
  omp_set_num_threads(nth);
  uint64_t checked=0, mismatch=0, wrongGamma=0, site136match=0,site137match=0, bothmatch=0;
  uint64_t patterns[19][19]{};
  auto t0=std::chrono::steady_clock::now();
  #pragma omp parallel
  {
    uint64_t loc_checked=0,loc_wrong=0,loc_match=0,loc136=0,loc137=0,loc_both=0;
    uint64_t loc_patterns[19][19]{};
    #pragma omp for schedule(dynamic, 512)
    for(int i=begin;i<end;i++)for(int p=0;p<2;p++){
       Output a=calculate(i,p);loc_checked++;
       loc_wrong+=(a.gamma!=30);loc136+=(a.site136==2);loc137+=(a.site137==9);
       if(a.site136==2&&a.site137==9)loc_both++;
       if(a.site136!=2||a.site137!=9)loc_match++;
       if(a.site136<=18&&a.site137<=18)loc_patterns[a.site136][a.site137]++;
    }
    #pragma omp critical
    {
       checked+=loc_checked;wrongGamma+=loc_wrong;mismatch+=loc_match;
       site136match+=loc136;site137match+=loc137;bothmatch+=loc_both;
       for(int i=0;i<19;i++)for(int j=0;j<19;j++)patterns[i][j]+=loc_patterns[i][j];
    }
  }
  double s=std::chrono::duration<double>(std::chrono::steady_clock::now()-t0).count();
  std::cout<<"{\"start\":"<<begin<<",\"end\":"<<end<<",\"count\":"<<checked<<",\"mismatch136or137\":"<<mismatch<<",\"match_both\":"<<bothmatch<<",\"match136\":"<<site136match<<",\"match137\":"<<site137match<<",\"bad_gamma\":"<<wrongGamma<<",\"seconds\":"<<s<<",\"patterns\":[";
  bool sep=false;for(int i=0;i<19;i++)for(int j=0;j<19;j++)if(patterns[i][j]){if(sep)std::cout<<",";sep=true;std::cout<<"["<<i<<","<<j<<","<<patterns[i][j]<<"]";}std::cout<<"]}\n";
}