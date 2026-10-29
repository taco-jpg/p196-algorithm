#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <omp.h>
using D = unsigned char;
static constexpr int Q=14, K=100, STEPS=120, CAP=1100;
static const int B[34]={10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
static const int W[9]={5,18,4,8,1,15,4,0,5};
static const int U[3]={4,9,14};

struct Stats {
  long long count=0, clock_ok=0, b_ok=0, w_ok=0, bw_ok=0;
  int first_min=9999, first_max=-1;
  long long first_hist[126]{};
};

static inline void check_word(const int* J,int jlen,Stats& s) {
  std::array<int,500> H{};
  int h=0;
  for(int x:B) H[h++]=x;
  for(int q=0;q<Q;q++) for(int x:W) H[h++]=x;
  for(int j=0;j<jlen;j++) H[h++]=J[j];
  for(int k=0;k<K;k++) for(int x:U) H[h++]=x;
  int n=2*h+2;
  std::array<D,CAP> a{},b{};
  for(int i=0;i<h;i++) {
    a[i]=H[i]>9?H[i]-9:0;
    a[n-1-i]=H[i]<9?H[i]:9;
  }
  // C=(0,0); the two centre coefficients are zero.
  D* cur=a.data();
  D* nxt=b.data();
  bool clock=true;
  for(int t=0;t<STEPS;t++) {
    int carry=0;
    for(int i=0;i<n;i++) {
      int z=int(cur[i])+int(cur[n-1-i])+carry;
      nxt[i]=D(z%10);
      carry=z/10;
    }
    if(carry != (t%4==0?1:0)) clock=false;
    if(carry) nxt[n++]=1;
    std::swap(cur,nxt);
  }
  s.count++;
  if(clock) s.clock_ok++;
  bool bm=true,wm=true;
  int first=-1;
  for(int i=0;i<34;i++) {
    if(int(cur[i])+int(cur[n-1-i])!=B[i]) {
      bm=false;
      if(first<0) first=i;
    }
  }
  for(int i=0;i<9*Q;i++) {
    int pos=34+i;
    int want=W[i%9];
    if(int(cur[pos])+int(cur[n-1-pos])!=want) {
      wm=false;
      if(first<0) first=pos;
    }
  }
  if(bm) s.b_ok++;
  if(wm) s.w_ok++;
  if(bm&&wm) s.bw_ok++;
  if(first>=34 && first<34+9*Q) {
    int off=first-34;
    s.first_min=std::min(s.first_min,off);
    s.first_max=std::max(s.first_max,off);
    s.first_hist[off]++;
  }
}

static Stats combine(const Stats& a,const Stats& b) {
  Stats r;
  r.count=a.count+b.count;
  r.clock_ok=a.clock_ok+b.clock_ok;
  r.b_ok=a.b_ok+b.b_ok;
  r.w_ok=a.w_ok+b.w_ok;
  r.bw_ok=a.bw_ok+b.bw_ok;
  r.first_min=std::min(a.first_min,b.first_min);
  r.first_max=std::max(a.first_max,b.first_max);
  for(int i=0;i<126;i++) r.first_hist[i]=a.first_hist[i]+b.first_hist[i];
  return r;
}

static void show(const char* name,const Stats& s) {
  std::cout<<name<<" count="<<s.count<<" clock_ok="<<s.clock_ok
           <<" B_ok="<<s.b_ok<<" W9_ok="<<s.w_ok<<" BW_ok="<<s.bw_ok
           <<" first_W_offset_range="<<s.first_min<<".."<<s.first_max<<"\n";
  std::cout<<name<<" first_offset_hist=";
  for(int i=0;i<126;i++) if(s.first_hist[i]) std::cout<<i<<":"<<s.first_hist[i]<<",";
  std::cout<<"\n";
}

static Stats run(int jlen) {
  Stats byfirst[19];
  #pragma omp parallel for schedule(dynamic) num_threads(5)
  for(int a=0;a<19;a++) {
    Stats s;
    if(jlen==3) {
      for(int b=0;b<19;b++) for(int c=0;c<19;c++) {
        int J[4]={a,b,c,0};
        check_word(J,3,s);
      }
    } else {
      for(int b=0;b<19;b++) for(int c=0;c<19;c++) for(int d=0;d<19;d++) {
        int J[4]={a,b,c,d};
        check_word(J,4,s);
      }
    }
    byfirst[a]=s;
  }
  Stats total;
  for(int a=0;a<19;a++) total=combine(total,byfirst[a]);
  show(jlen==3?"J3":"J4",total);
  return total;
}

int main() {
  std::cout<<"CONFIG q="<<Q<<" k="<<K<<" steps="<<STEPS
           <<" U=4,9,14 C=0,0 gamma=1000^30\n";
  Stats s3=run(3),s4=run(4);
  Stats all=combine(s3,s4);
  show("TOTAL",all);
  return (s3.w_ok==0 && s4.w_ok==0 &&
          s3.clock_ok==s3.count && s4.clock_ok==s4.count) ? 0 : 1;
}
