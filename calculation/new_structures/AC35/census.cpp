#include <array>
#include <cstdlib>
#include <iostream>
#include <vector>
#include <chrono>
#include <omp.h>
using namespace std;
static const int B[34]={2,11,1,6,8,1,7,15,9,3,9,4,7,9,10,16,9,11,4,10,8,8,9,11,11,7,4,3,9,12,1,1,9,11};
static const int W[9]={1,10,8,5,9,16,0,9,11};
using Arr=array<unsigned char,2000>;
struct Ret{int first=999999,gamma=0,prefix=0,exact=0;};
Ret run(const int J[6],const int U[3],const vector<int>&C,int q,int k){
 Arr a={},b={},d={};int nh=0;
 for(int x:B)a[nh++]=x;
 for(int t=0;t<q;t++)for(int x:W)a[nh++]=x;
 for(int j=0;j<6;j++)a[nh++]=J[j];
 for(int t=0;t<k;t++)for(int j=0;j<3;j++)a[nh++]=U[j];
 int h=nh;for(int x:C)a[nh++]=x;
 for(int i=0;i<h;i++)a[nh++]=a[h-1-i];
 int n=nh,gam=0;
 for(int t=0;t<120;t++){
  int c=0;
  for(int i=0;i<n;i++){int v=a[i]+c;c=(v>=10);d[i]=v-(c?10:0);}
  if(c)d[n]=1;
  int n2=n+c;gam+=c;
  for(int i=0;i<n2;i++)b[i]=d[i]+d[n2-1-i];
  a.swap(b);n=n2;
 }
 Ret r;r.gamma=gam;int i=0;
 for(int x:B){if(i>=n||a[i]!=x){r.first=i;return r;}++i;}
 for(int t=0;t<q;t++)for(int x:W){if(i>=n||a[i]!=x){r.first=i;return r;}++i;}
 r.prefix=1;
 for(int j=0;j<6;j++){if(i>=n||a[i]!=J[j]){r.first=i;return r;}++i;}
 for(int t=0;t<k+5;t++)for(int j=0;j<3;j++){if(i>=n||a[i]!=U[j]){r.first=i;return r;}++i;}
 for(int x:C){if(i>=n||a[i]!=x){r.first=i;return r;}++i;}
 r.first=i;r.exact=(n==2*(34+9*q+6+3*(k+5))+(int)C.size());return r;
}
int main(int argc,char**argv){
 if(argc<5){cerr<<"usage: census U_rank0 J0 Ctype limit [q=14] [k=100] [odd_mod11_gate=0|1]\n";return 2;}
 int ur=atoi(argv[1]),j0=atoi(argv[2]),ct=atoi(argv[3]);
 long long lim=atoll(argv[4]);int q=argc>5?atoi(argv[5]):14,k=argc>6?atoi(argv[6]):100;
 bool gate=argc>7&&atoi(argv[7])==1;
 if(ur<0||ur>=30||j0<0||j0>18||ct<0||ct>1||q<0||k<0||2*(34+9*q+6+3*(k+5))+3>2000){cerr<<"bad args or buffer too short\n";return 2;}
 if(lim<0||lim>2476099)lim=2476099;
 int aa=2*(ur/3),rot=ur%3,base[3]={9,aa,18-aa},U[3]={base[rot],base[(rot+1)%3],base[(rot+2)%3]};
 vector<int>C=ct?vector<int>{4,14,4}:vector<int>{4,4};
 long long hist[2002]={},skipped=0,badclock=0,prefix=0,returns=0;int best=0;long long bestcode=0;
 auto t0=chrono::steady_clock::now();
 #pragma omp parallel num_threads(5)
 {
  long long local[2002]={},s=0,bc=0,pr=0,re=0;int b=0;long long bc2=0;int J[6]={j0,0,0,0,0,0};
  #pragma omp for schedule(static)
  for(long long code=0;code<lim;code++){
   long long v=code;for(int j=5;j>=1;j--){J[j]=v%19;v/=19;}
   if(ct&&gate){int alt=0;for(int z=0;z<6;z++)alt+=(z%2==0?J[z]:-J[z]);if((alt%11+11)%11!=3){s++;continue;}}
   auto x=run(J,U,C,q,k);
   if(x.first>=0&&x.first<2002)local[x.first]++;
   bc+=(x.gamma!=30);pr+=x.prefix;re+=x.exact;
   if(x.first>b){b=x.first;bc2=code;}
  }
  #pragma omp critical
  {for(int z=0;z<2002;z++)hist[z]+=local[z];skipped+=s;badclock+=bc;prefix+=pr;returns+=re;if(b>best){best=b;bestcode=bc2;}}
 }
 double seconds=chrono::duration<double>(chrono::steady_clock::now()-t0).count();
 cout<<"{ \"phase\":2,\"U_rank_zero\":"<<ur<<",\"J0\":"<<j0<<",\"Ctype\":"<<ct<<",\"tested\":"<<lim
 <<",\"pruned_odd_mod11\":"<<skipped<<",\"clock_bad\":"<<badclock<<",\"W9_prefix_retained\":"<<prefix
 <<",\"full_returns\":"<<returns<<",\"best_prefix\":"<<best<<",\"best_Jcode\":"<<bestcode<<",\"seconds\":"<<seconds<<",\"hist\":{";
 bool first=true;for(int i=0;i<2002;i++)if(hist[i]){if(!first)cout<<",";first=false;cout<<"\""<<i<<"\":"<<hist[i];}
 cout<<"}}\n";
}