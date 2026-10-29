#define main original_engine_main
#include "four_sheet_fast.cpp"
#undef main
int main(int argc,char**argv){
 int T=argc>1?atoi(argv[1]):20000;
 S x;x[0]={0,{5,7}};x[1]={0,{7,3}};x[2]={};x[3]={0,{8,8}};
 int Q=1,D=1,U=0,V=0,peakG=0;
 for(int t=0;t<=T;t++){
  auto chk=[&](int k){return !x[k].empty();};
  if(chk(0)){if(x[0].start<0)abort();}
  if(chk(1))Q=max(Q,-x[1].start);
  if(chk(2))U=max(U,-x[2].start);
  if(chk(3))V=max(V,-x[3].start);
  if(chk(0)&&chk(1))Q=max(Q,1+x[0].end()-x[1].start);
  if(chk(1)&&chk(2))D=max(D,1+x[1].end()-x[2].start);
  if(chk(2)&&chk(3))Q=max(Q,1+x[2].end()-x[3].start);
  peakG=max(peakG,needed_G(x));
  if(t==0||t==264||t==1000||t==5000||t==10000||t==20000||t==T){
   cout<<"t="<<t<<" q_min="<<Q<<" (q+r)_min="<<D<<" (q+(q+r))_min="<<U<<" (2q+(q+r))_min="<<V<<" uniformG="<<peakG<<"\n";
  }
  if(t<T)x=evolve(x);
 }
}
