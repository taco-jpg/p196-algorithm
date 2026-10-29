// AC33: exhaustive unpruned endpoint-only fixed-centre census.
// Source coefficients and W row from lat_p12m9.txt, phase zero, LSD-first.
// Ordinary decimal digits are never updated in place.
#include <array>
#include <chrono>
#include <iostream>
#include <algorithm>
#include <cstdlib>
using namespace std;
const int B[34]={10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
const int W[9]={5,18,4,8,1,15,4,0,5};
const int Us[3][3]={{9,0,18},{9,8,10},{9,16,2}};
const int Cs[2][3]={{4,4,0},{4,14,4}};
const int CL[2]={2,3};
int main(int argc,char**argv){
  if(argc<3){cerr<<"usage: census Uindex(0..2) Cindex(0..1) [J0 J1 lo hi]\n";return 2;}
  int ui=atoi(argv[1]),ci=atoi(argv[2]),j0=argc>3?atoi(argv[3]):0,j1=argc>4?atoi(argv[4]):0;
  int maxX=(j1==-1?2476099:130321);
  int lo=argc>5?atoi(argv[5]):0,hi=argc>6?atoi(argv[6]):maxX;
  if(ui<0||ui>2||ci<0||ci>1||j0<0||j0>18||j1<-1||j1>18||lo<0||hi>maxX||lo>=hi)return 3;
  if(j1==-1 && (ui!=0 || ci!=1 || j0!=0))return 4;
  const int q=14,k=100;
  const int H=34+9*q+6+3*k,N=2*H+CL[ci],targetN=N+30,cut=34+9*q;
  int Hword[600],P[1200];int J[6]={j0,j1,0,0,0,0};
  for(int i=0;i<34;i++)Hword[i]=B[i];
  for(int i=0;i<9*q;i++)Hword[34+i]=W[i%9];
  for(int i=0;i<3*k;i++)Hword[cut+6+i]=Us[ui][i%3];
  for(int i=0;i<CL[ci];i++)P[H+i]=Cs[ci][i];
  long long checked=0,goodW=0,goodFull=0,goodClock=0,pruned=0;
  array<long long,161> mismatch{};
  int d[2][1200];
  auto start=chrono::steady_clock::now();
  for(int x=lo;x<hi;x++){
    int tmp=x;
    if(j1==-1){J[1]=tmp%19;tmp/=19;}
    for(int h=2;h<6;h++){J[h]=tmp%19;tmp/=19;Hword[cut+h]=J[h];}
    Hword[cut]=J[0];Hword[cut+1]=J[1];
    // Existing T12 all-width theorem makes the odd-centre mod-11 gate
    // necessary for reference-width return. Never use this for even C.
    if(j1==-1 && (2*(J[0]-J[1]+J[2]-J[3]+J[4]-J[5])-6)%11!=0){
      pruned++;continue;
    }
    for(int i=0;i<H;i++){P[i]=Hword[i];P[N-i-1]=Hword[i];}
    for(int i=0;i<N/2;i++){
      int z=P[i],a=min(9,z);d[0][i]=z-a;d[0][N-1-i]=a;
    }
    if(N%2)d[0][N/2]=P[N/2]/2;
    int nd=N,cur=0,overflows=0;
    for(int t=0;t<120;t++){
      int carry=0,*in=d[cur],*out=d[1-cur];
      for(int i=0;i<nd;i++){
        int z=in[i]+in[nd-1-i]+carry;
        out[i]=z%10;carry=z/10;
      }
      if(carry){out[nd++]=carry;overflows++;}
      cur=1-cur;
    }
    checked++;
    if(overflows==30)goodClock++;
    if(nd!=targetN){mismatch[160]++;continue;}
    int first=160;
    for(int i=0;i<cut;i++){
      int expected=i<34?B[i]:W[(i-34)%9];
      if(d[cur][i]+d[cur][nd-1-i]!=expected){first=i;break;}
    }
    if(first<160){mismatch[first]++;continue;}
    goodW++;
    bool full=true;
    for(int i=0;i<targetN/2;i++){
      int target=i<cut?(i<34?B[i]:W[(i-34)%9]):
        (i<cut+6?J[i-cut]:(i<H+15?Us[ui][(i-cut-6)%3]:Cs[ci][i-H-15]));
      if(d[cur][i]+d[cur][nd-1-i]!=target){full=false;break;}
    }
    if(full && targetN%2 && d[cur][targetN/2]*2 != Cs[ci][CL[ci]/2]) full=false;
    if(full)goodFull++;
  }
  double seconds=chrono::duration<double>(chrono::steady_clock::now()-start).count();
  cout<<"{\"U\":"<<ui<<",\"C\":"<<ci<<",\"J0\":"<<j0<<",\"J1\":"<<j1
      <<",\"lo\":"<<lo<<",\"hi\":"<<hi<<",\"tested\":"<<checked<<",\"pruned_mod11\":"<<pruned
      <<",\"length30\":"<<goodClock<<",\"outer_W9_pass\":"<<goodW
      <<",\"full_return\":"<<goodFull<<",\"elapsed_s\":"<<seconds<<",\"mismatch_hist\":[";
  bool first=true;
  for(int i=0;i<=160;i++)if(mismatch[i]){
    if(!first)cout<<",";
    cout<<"["<<i<<","<<mismatch[i]<<"]";first=false;
  }
  cout<<"]}\n";
}
