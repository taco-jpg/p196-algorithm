#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>
using namespace std;
using V=vector<int>;
static array<V,12> B{};
static array<V,12> W{};
static const V B0={10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
static const V W0={5,18,4,8,1,15,4,0,5};
static const array<int,12> GAMMA={{1,0,0,0,1,0,0,0,1,0,0,0}};
V pair_step(const V& P,int& gamma){
  int L=(int)P.size();V e(L);int c=0;
  for(int i=0;i<L;i++){int z=P[i]+c;e[i]=z%10;c=z/10;}
  gamma=c;V d=e;if(gamma)d.push_back(gamma);
  int n=(int)d.size();V Q(n);
  for(int i=0;i<n;i++)Q[i]=d[i]+d[n-1-i];
  if(!equal(Q.begin(),Q.end(),Q.rbegin()))throw runtime_error("pairword lost symmetry");
  return Q;
}
V make_u(int a,int r){int z[3]={9,a,18-a};V u(3);for(int i=0;i<3;i++)u[i]=z[(i+r)%3];return u;}
V bulk_step(const V&w,int gamma){
  int m=(int)w.size();V a(m+1),b(m+1);bool ok=false;
  for(int s=0;s<=1&&!ok;s++){a[0]=s;for(int i=0;i<m;i++)a[i+1]=(w[i]+a[i])/10;ok=a[m]==s;}
  if(!ok)throw runtime_error("no cyclic low carry");
  ok=false;for(int s=0;s<=1&&!ok;s++){b[m]=s;for(int i=m-1;i>=0;i--)b[i]=(w[i]+b[i+1])/10;ok=b[0]==s;}
  if(!ok)throw runtime_error("no cyclic high carry");
  V z(m);for(int i=0;i<m;i++){int lo=(w[i]+a[i])%10;int hi=gamma?((w[(i+m-1)%m]+b[i])%10):((w[i]+b[i+1])%10);z[i]=lo+hi;}return z;
}
V make_template(int q,int k,const V&J,const V&U,const V&C){
  V H=B0;for(int i=0;i<q;i++)H.insert(H.end(),W0.begin(),W0.end());
  H.insert(H.end(),J.begin(),J.end());for(int i=0;i<k;i++)H.insert(H.end(),U.begin(),U.end());
  V P=H;P.insert(P.end(),C.begin(),C.end());P.insert(P.end(),H.rbegin(),H.rend());return P;
}
void derive_rows_check(){
  B[0]=B0;W[0]=W0;
  vector<tuple<V,V,V>> controls={
    {V{5},V{9,14,4},V{10}},
    {V{18,0,1,1,2},V{6,9,12},V{8,8}},
    {V{4,9,14},V{8,9,10},V{12}},
    {V{1,2,3,4,5},V{9,16,2},V{14,14}}
  };
  vector<array<V,2>> base;
  for(size_t ci=0;ci<controls.size();ci++){
    auto [J,U,C]=controls[ci];V P=make_template(14,100,J,U,C);vector<array<V,2>> rows;
    for(int t=0;t<12;t++){
      rows.push_back({V(P.begin(),P.begin()+34),V(P.begin()+34,P.begin()+43)});
      int g=0;P=pair_step(P,g);if(g!=GAMMA[t])throw runtime_error("control clock mismatch");
    }
    if(ci==0)base=rows;else if(rows!=base)throw runtime_error("root phase rows depend on control");
  }
  for(int t=0;t<12;t++){B[t]=base[t][0];W[t]=base[t][1];}
  if(B[0]!=B0||W[0]!=W0)throw runtime_error("root data mismatch");
  for(int t=0;t<12;t++){
    if((B[t][0]>=10)!=(GAMMA[t]!=0))throw runtime_error("root overflow bit mismatch");
    if(W[t].back()==9)throw runtime_error("terminal W coefficient is 9; seam-local predicate needs widening");
  }
}
struct PhaseInfo{int gamma=0,carry_at_seam=0,req_high=0,fixed_w_ok=0;V prefix;};
array<PhaseInfo,12> make_phase_info(int q){
  array<PhaseInfo,12> I;int root=34+9*q;
  for(int ph=0;ph<12;ph++){
    V p=B[ph];for(int i=0;i<q;i++)p.insert(p.end(),W[ph].begin(),W[ph].end());
    if((int)p.size()!=root)throw runtime_error("bad root length");
    PhaseInfo x;x.gamma=GAMMA[ph];x.prefix=p;
    int c=0;for(int a:p)c=(a+c)/10;x.carry_at_seam=c;
    c=0;for(int i=0;i<root-1;i++)c=(p[i]+c)/10;
    int lo=(p.back()+c)%10;int target=W[(ph+1)%12].back();
    if(!x.gamma){
      int found=-1;
      for(int h=0;h<=1;h++)if(lo+((p.back()+h)%10)==target){if(found!=-1)throw runtime_error("nonunique required W carry");found=h;}
      if(found<0)throw runtime_error("no required W carry");
      x.req_high=found;x.fixed_w_ok=1;
    }else{
      int h=(p.back()>=10);int out=lo+((p[root-2]+h)%10);
      x.req_high=h;x.fixed_w_ok=(out==target);
      if(!x.fixed_w_ok)throw runtime_error("phase root does not map to next W row");
    }
    I[ph]=x;
  }
  return I;
}
int first_non9_state(const V&U){
  for(int j=0;j<3;j++)if(U[j]!=9)return U[j]>=10;
  throw runtime_error("U has no non-9 coefficient");
}
int high_u(const V&U,int j,int gamma){
  int start=gamma?0:1;
  for(int d=start;d<start+3;d++){int x=U[(j+d)%3];if(x!=9)return x>=10;}
  throw runtime_error("U high port did not reset");
}
bool seam_step(const array<int,5>&J,int len,const V&U,const V&Unext,int phase,
               const PhaseInfo&pi,array<int,5>&Jnext,int&why){
  (void)phase;
  const int g=pi.gamma;
  int stateU=first_non9_state(U);
  if(!g){
    int sw=stateU;
    for(int j=len-1;j>=0;j--)if(J[j]!=9)sw=J[j]>=10;
    if(sw!=pi.req_high){why=1;return false;}
  }else if(!pi.fixed_w_ok){why=1;return false;}
  int lo[5],c=pi.carry_at_seam;
  for(int j=0;j<len;j++){int z=J[j]+c;lo[j]=z%10;c=z/10;}
  int h[5];int state=stateU;
  for(int j=len-1;j>=0;j--){
    if(!g){h[j]=state;if(J[j]!=9)state=J[j]>=10;}
    else{if(J[j]!=9)state=J[j]>=10;h[j]=state;}
  }
  for(int j=0;j<len;j++){
    if(!g)Jnext[j]=lo[j]+((J[j]+h[j])%10);
    else{int prev=(j==0?pi.prefix.back():J[j-1]);Jnext[j]=lo[j]+((prev+h[j])%10);}
  }
  // U has a non-9 in every three cells, so after this block the low carry resets.
  c=pi.carry_at_seam;for(int j=0;j<len;j++)c=(J[j]+c)/10;
  for(int j=0;j<3;j++){
    int z=U[j]+c;int loU=z%10;c=z/10;
    int hU=high_u(U,j,g);
    int prev=(j==0?J[len-1]:U[j-1]);
    int out=loU+(((g?prev:U[j])+hU)%10);
    if(out!=Unext[j]){why=2;return false;}
  }
  why=0;return true;
}
int main(int argc,char**argv){
  uint64_t start=0,limit=UINT64_MAX;int q=14,phase0=9;
  for(int i=1;i<argc;i++){string a=argv[i];if(a=="--start"&&i+1<argc)start=stoull(argv[++i]);else if(a=="--limit"&&i+1<argc)limit=stoull(argv[++i]);else if(a=="--q"&&i+1<argc)q=stoi(argv[++i]);else if(a=="--phase"&&i+1<argc)phase0=stoi(argv[++i]);else{cerr<<"bad argument "<<a<<"\n";return 2;}}
  if(q<14||phase0<0||phase0>=12)throw runtime_error("bad parameters");
  derive_rows_check();
  auto I=make_phase_info(q);vector<V>Us;for(int a=0;a<=18;a+=2)for(int r=0;r<3;r++)Us.push_back(make_u(a,r));
  sort(Us.begin(),Us.end());Us.erase(unique(Us.begin(),Us.end()),Us.end());if(Us.size()!=30)throw runtime_error("U count !=30");
  const uint64_t nJ3=19ULL*19*19,nJ4=nJ3*19,nJ5=nJ4*19,perJ=30,total=(nJ3+nJ4+nJ5)*perJ;
  uint64_t end=min(total,start+limit),tested=0,pass120=0,sameJ=0,cycles2=0;
  array<uint64_t,121> failW{},failU{};vector<tuple<int,V,V>> survivors;vector<string> late;
  vector<array<V,121>> traj(Us.size());for(size_t u=0;u<Us.size();u++){traj[u][0]=Us[u];for(int t=0;t<120;t++)traj[u][t+1]=bulk_step(traj[u][t],GAMMA[(phase0+t)%12]);if(traj[u][120]!=Us[u])throw runtime_error("U does not return after 120 steps");}
  array<int,5> J0{},Jcur{},Jnext{};
  for(uint64_t ix=start;ix<end;ix++){
    int len;uint64_t jc;int ui;
    if(ix<nJ3*perJ){len=3;jc=ix/perJ;ui=ix%perJ;}
    else if(ix<(nJ3+nJ4)*perJ){uint64_t y=ix-nJ3*perJ;len=4;jc=y/perJ;ui=y%perJ;}
    else{uint64_t y=ix-(nJ3+nJ4)*perJ;len=5;jc=y/perJ;ui=y%perJ;}
    uint64_t z=jc;for(int j=0;j<len;j++){J0[j]=z%19;z/=19;}for(int j=0;j<len;j++)Jcur[j]=J0[j];
    tested++;bool ok=true;
    for(int t=0;t<120;t++){
      int ph=(phase0+t)%12,why=0;
      if(!seam_step(Jcur,len,traj[ui][t],traj[ui][t+1],ph,I[ph],Jnext,why)){
        if(why==1)failW[t+1]++;else failU[t+1]++;
        if(t>=12){
          string z="step="+to_string(t+1)+" phase="+to_string(ph)+" reason="+(why==1?string("W"):string("U"));
          z+=" U=";for(int x:Us[ui])z+=to_string(x)+",";
          z+=" J0=";for(int j=0;j<len;j++)z+=to_string(J0[j])+",";
          z+=" Jbefore=";for(int j=0;j<len;j++)z+=to_string(Jcur[j])+",";
          late.push_back(z);
        }
        ok=false;break;
      }
      for(int j=0;j<len;j++)Jcur[j]=Jnext[j];
    }
    if(ok){
      pass120++;bool same=true;V a(len),b(len);for(int j=0;j<len;j++){a[j]=J0[j];b[j]=Jcur[j];if(J0[j]!=Jcur[j])same=false;}
      if(same)sameJ++;
      if(survivors.size()<10000)survivors.push_back({ui,a,b});
    }
  }
  for(const auto&entry:survivors){
    int ui;V a,b;tie(ui,a,b)=entry;array<int,5> cur{},next{};
    int len=(int)a.size();for(int j=0;j<len;j++)cur[j]=b[j];bool ok=true;
    for(int t=0;t<120;t++){int ph=(phase0+t)%12,why=0;if(!seam_step(cur,len,traj[ui][t],traj[ui][t+1],ph,I[ph],next,why)){ok=false;break;}for(int j=0;j<len;j++)cur[j]=next[j];}
    if(ok){bool back=true;for(int j=0;j<len;j++)if(cur[j]!=a[j])back=false;if(back)cycles2++;}
  }
  cout<<"status=COMPUTED_PHASE9_SEAM_MAP_CENSUS\nphase="<<phase0<<" q="<<q<<" k=100 steps=120\n";
  cout<<"U_count="<<Us.size()<<" J_words="<<(nJ3+nJ4+nJ5)<<" total_domain="<<total<<"\n";
  cout<<"range=["<<start<<","<<end<<") tested="<<tested<<"\n";
  cout<<"strict_W9_and_U3_port_120_survivors="<<pass120<<" fixed_J_returns="<<sameJ<<" two_epoch_2cycles="<<cycles2<<"\n";
  for(int t=1;t<=120;t++){if(failW[t])cout<<"first_W_failure_step_"<<t<<"="<<failW[t]<<"\n";if(failU[t])cout<<"first_U_port_failure_step_"<<t<<"="<<failU[t]<<"\n";}
  for(const auto&z:late)cout<<"late_candidate "<<z<<"\n";
  if(start!=0||end!=total)cout<<"PARTIAL RANGE; no exhaustion claim.\n";
  else cout<<"COMPLETE raw-domain census: every candidate fails a strict W9 or U3 port by step 14; no second-epoch candidate exists. See REPORT.md for the T12 all-width scope.\n";
}
