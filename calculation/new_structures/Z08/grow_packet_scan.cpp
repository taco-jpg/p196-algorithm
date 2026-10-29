// Exact local-collar census for the phase-0 two-band growing seam J0 R^m U^k.
// Scope: odd palindromic centres, U ranks 8 and 20; necessary endpoint restoration only.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <mutex>
#include <stdexcept>
#include <string>
#include <vector>
#ifdef _OPENMP
#include <omp.h>
#endif
using namespace std;
using V3=array<int,3>; using J5=array<int,5>;
static constexpr int GAM[12]={1,0,0,0,1,0,0,0,1,0,0,0};
static constexpr int W[12][9]={
 {5,18,4,8,1,15,4,0,5},{10,14,13,12,9,7,10,4,5},
 {1,10,8,5,9,16,0,9,11},{4,0,17,11,9,12,2,9,2},
 {8,1,15,4,0,5,5,18,4},{12,9,7,10,4,5,10,14,13},
 {5,9,16,0,9,11,1,10,8},{11,9,12,2,9,2,4,0,17},
 {4,0,5,5,18,4,8,1,15},{10,4,5,10,14,13,12,9,7},
 {0,9,11,1,10,8,5,9,16},{2,9,2,4,0,17,11,9,12}};
static constexpr int LW=108, RR=171, NJ=5, N=LW+NJ+RR;
using Win=array<uint8_t,N>;
static int mod(int x,int m){x%=m;return x<0?x+m:x;}
static int alt3(const V3&w){return w[0]-w[1]+w[2];}
static int alt5(const J5&w){return w[0]-w[1]+w[2]-w[3]+w[4];}
static int low_cyclic3(const V3&w){for(int s=0;s<=1;s++){int c=s;for(int x:w)c=(x+c)/10;if(c==s)return s;}throw runtime_error("no cyclic low carry");}
static V3 bulk_step3(const V3&w,int gamma){
 int a[4]={},b[4]={};bool ok=false;
 for(int s=0;s<=1&&!ok;s++){a[0]=s;for(int i=0;i<3;i++)a[i+1]=(w[i]+a[i])/10;ok=(a[3]==s);}if(!ok)throw runtime_error("no cyclic low carry");ok=false;
 for(int s=0;s<=1&&!ok;s++){b[3]=s;for(int i=2;i>=0;i--)b[i]=(w[i]+b[i+1])/10;ok=(b[0]==s);}if(!ok)throw runtime_error("no cyclic high carry");
 V3 z{};for(int i=0;i<3;i++)z[i]=(w[i]+a[i])%10+(gamma?((w[(i+2)%3]+b[i])%10):((w[i]+b[i+1])%10));return z;
}
static array<int,9> bulk_step9(const array<int,9>&w,int gamma){
 int a[10]={},b[10]={};bool ok=false;
 for(int s=0;s<=1&&!ok;s++){a[0]=s;for(int i=0;i<9;i++)a[i+1]=(w[i]+a[i])/10;ok=(a[9]==s);}if(!ok)throw runtime_error("no cyclic W low carry");ok=false;
 for(int s=0;s<=1&&!ok;s++){b[9]=s;for(int i=8;i>=0;i--)b[i]=(w[i]+b[i+1])/10;ok=(b[0]==s);}if(!ok)throw runtime_error("no cyclic W high carry");
 array<int,9> z{};for(int i=0;i<9;i++)z[i]=(w[i]+a[i])%10+(gamma?((w[(i+8)%9]+b[i])%10):((w[i]+b[i+1])%10));return z;
}
static bool all9(const V3&w){return w[0]==9&&w[1]==9&&w[2]==9;}
struct RPath{V3 r[121];int high[120];};
static vector<V3> r_candidates(const V3&U){
 vector<V3> out;const int target=mod(alt3(U),11);
 for(int a=0;a<=18;a++)for(int b=0;b<=18;b++)for(int c=0;c<=18;c++){
  V3 R{a,b,c};if((a+b+c)%9)continue;if(mod(alt3(R),11)!=target)continue;if(R==U||R==V3{9,9,9})continue;
  V3 x=R;bool hit999=all9(x),bad_reset=((x[0]==9&&x[1]==9)||(x[1]==9&&x[2]==9)||(x[2]==9&&x[0]==9));for(int t=0;t<120;t++){x=bulk_step3(x,GAM[t%12]);if(all9(x))hit999=true;if((x[0]==9&&x[1]==9)||(x[1]==9&&x[2]==9)||(x[2]==9&&x[0]==9))bad_reset=true;}
  if(x==R&&!hit999&&bad_reset)throw runtime_error("120-cycle R has adjacent 9s; collar bound must be revised");
  if(x==R&&!hit999)out.push_back(R);
 }
 return out;
}
static vector<J5> j_candidates(int residue){
 vector<J5> out;out.reserve(226000);
 for(int code=0;code<2476099;code++){int z=code;J5 j{};for(int i=0;i<5;i++){j[i]=z%19;z/=19;}if(mod(2*alt5(j),11)==residue)out.push_back(j);}
 return out;
}
static void fill_window(Win&h,const J5&j,const V3&r){
 for(int i=0;i<LW;i++)h[i]=W[0][i%9];for(int i=0;i<NJ;i++)h[LW+i]=j[i];for(int i=0;i<RR;i++)h[LW+NJ+i]=r[i%3];
}
static void local_step(const Win&h,Win&o,int gamma,int lowcarry,int highstate,int leftprev){
 uint8_t low[N],high[N];int c=lowcarry;
 for(int i=0;i<N;i++){int z=(int)h[i]+c;low[i]=(uint8_t)(z%10);c=z/10;}
 int st=highstate;
 if(!gamma){for(int i=N-1;i>=0;i--){high[i]=(uint8_t)st;if(h[i]!=9)st=(h[i]>=10);}}
 else {for(int i=N-1;i>=0;i--){if(h[i]!=9)st=(h[i]>=10);high[i]=(uint8_t)st;}}
 if(!gamma){for(int i=0;i<N;i++)o[i]=(uint8_t)(low[i]+(((int)h[i]+high[i])%10));}
 else {o[0]=(uint8_t)(low[0]+((leftprev+high[0])%10));for(int i=1;i<N;i++)o[i]=(uint8_t)(low[i]+(((int)h[i-1]+high[i])%10));}
}
static bool endpoint(const J5&j,const V3&r,const RPath&rp,const int wlow[120]){
 Win h{},o{};fill_window(h,j,r);
 for(int t=0;t<120;t++){local_step(h,o,GAM[t%12],wlow[t],rp.high[t],W[t%12][8]);h.swap(o);}
 Win want{};fill_window(want,j,r);return h==want;
}
static void printv(const V3&x){cout<<"("<<x[0]<<","<<x[1]<<","<<x[2]<<")";}
int main(int argc,char**argv){
 long long limit=-1;int ufilter=0; // 0=both, 8=U8 only, 20=U20 only
 for(int i=1;i<argc;i++){string a=argv[i];if(a=="--limit"&&i+1<argc)limit=stoll(argv[++i]);else if(a=="--u"&&i+1<argc)ufilter=stoi(argv[++i]);else throw runtime_error("usage: grow_packet_scan [--u 8|20] [--limit n]");}
 array<int,9> w0{};for(int i=0;i<9;i++)w0[i]=W[0][i];
 for(int ph=0;ph<12;ph++)for(int i=0;i<9;i++)if(W[ph][i]==9&&W[ph][(i+1)%9]==9)throw runtime_error("W phase has adjacent 9s");
 array<array<int,9>,121> wt{};wt[0]=w0;
 int wlow[120]{};
 for(int t=0;t<120;t++){int cyc=-1;for(int s=0;s<=1;s++){int c=s;for(int i=0;i<9;i++)c=(wt[t][i]+c)/10;if(c==s){cyc=s;break;}}if(cyc<0)throw runtime_error("no W cyclic carry");wlow[t]=cyc;
  wt[t+1]=bulk_step9(wt[t],GAM[t%12]);if(wt[t+1]!=array<int,9>{W[(t+1)%12][0],W[(t+1)%12][1],W[(t+1)%12][2],W[(t+1)%12][3],W[(t+1)%12][4],W[(t+1)%12][5],W[(t+1)%12][6],W[(t+1)%12][7],W[(t+1)%12][8]})throw runtime_error("W bulk path does not match published lattice at phase "+to_string(t+1));
 }
 if(wt[120]!=w0)throw runtime_error("W does not return after 120 steps");
 vector<V3> Us={{6,12,9},{9,18,0}};long long total=0,restored=0;vector<string> samples;mutex sample_mutex;
 cout<<"GROWING_SEAM_LOCAL_CENSUS status=COMPUTED necessary-window endpoint screen; window="<<N<<" LW="<<LW<<" RR="<<RR<<" steps=120\n";
 for(const V3&U:Us){if(ufilter&&((ufilter==8&&U!=V3{6,12,9})||(ufilter==20&&U!=V3{9,18,0})))continue;
  int au=mod(alt3(U),11);auto Rs=r_candidates(U);auto Js=j_candidates(au);
  cout<<"U=";printv(U);cout<<" A(U)="<<au<<" R_cycles="<<Rs.size()<<" J_gate="<<Js.size()<<"\nR_list=";for(auto r:Rs){printv(r);cout<<" ";}cout<<"\n";
  long long tested=(long long)Rs.size()*Js.size();if(limit>=0)tested=min(tested,limit);long long surv=0;
  vector<RPath> paths(Rs.size());for(size_t ri=0;ri<Rs.size();ri++){paths[ri].r[0]=Rs[ri];for(int t=0;t<120;t++){paths[ri].r[t+1]=bulk_step3(paths[ri].r[t],GAM[t%12]);int hs=-1;for(int x:paths[ri].r[t])if(x!=9){hs=x>=10;break;}if(hs<0)throw runtime_error("R motif became all 9 despite filter");paths[ri].high[t]=hs;}if(paths[ri].r[120]!=Rs[ri])throw runtime_error("R candidate does not return at t=120");}
  #pragma omp parallel for schedule(static) reduction(+:surv)
  for(long long idx=0;idx<tested;idx++){size_t ri=idx/Js.size(),ji=idx%Js.size();if(endpoint(Js[ji],Rs[ri],paths[ri],wlow)){
    surv++;
    #pragma omp critical
    {if(samples.size()<100){string s="U="+to_string(U[0])+","+to_string(U[1])+","+to_string(U[2])+" J=";for(int x:Js[ji])s+=to_string(x)+",";s+=" R=";for(int x:Rs[ri])s+=to_string(x)+",";samples.push_back(s);}}
   }}
  total+=tested;restored+=surv;cout<<"U_RESULT tested="<<tested<<" endpoint_restorers="<<surv<<"\n"<<flush;
 }
 if(limit<0)cout<<"CENSUS_RESULT tested="<<total<<" endpoint_restorers="<<restored<<"\n";
 else cout<<"PARTIAL_RESULT tested="<<total<<" endpoint_restorers="<<restored<<"\n";
 for(const auto&s:samples)cout<<"SURVIVOR "<<s<<"\n";
 ofstream sf("survivors.txt");for(const auto&s:samples)sf<<s<<"\n";
}
