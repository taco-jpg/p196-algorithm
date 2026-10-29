#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
using V=vector<int>;
static const V B={1,5,10,12,13,10,3,7,14,11,4,2,3,9,15,7,9,15,11,14,13,13,14,5,5,13,11,11,9,5,10,10,4,5};
static const V W={10,14,13,12,9,7,10,4,5};
static const V U6={17,14,17,1,4,1};
static const array<int,12> GAM={1,0,0,0,1,0,0,0,1,0,0,0};
V decode(uint64_t n,int len){V w(len);for(int&i:w){i=n%19;n/=19;}return w;}
bool starts(const V&a,const V&b){return a.size()>=b.size()&&equal(b.begin(),b.end(),a.begin());}
V bulk_step(const V&w,int gamma){int m=w.size();V a(m+1),b(m+1);bool ok=false;for(int s=0;s<=1&&!ok;s++){a[0]=s;for(int i=0;i<m;i++)a[i+1]=(w[i]+a[i])/10;ok=a[m]==s;}if(!ok)throw runtime_error("no cyclic low carry");ok=false;for(int s=0;s<=1&&!ok;s++){b[m]=s;for(int i=m-1;i>=0;i--)b[i]=(w[i]+b[i+1])/10;ok=b[0]==s;}if(!ok)throw runtime_error("no cyclic high carry");V z(m);for(int i=0;i<m;i++){int lo=(w[i]+a[i])%10;int hi=gamma?((w[(i+m-1)%m]+b[i])%10):((w[i]+b[i+1])%10);z[i]=lo+hi;}return z;}
void local_step_into(const V&H,const V&U,int ustart,int gamma,V&low,V&high,V&out){int n=H.size();int state=-1;for(int j=0;j<6;j++){int x=U[(n+j-ustart)%6];if(x!=9){state=x>=10;break;}}if(state<0)throw runtime_error("U6 tail did not reset high carry");int c=0;for(int i=0;i<n;i++){int z=H[i]+c;low[i]=z%10;c=z/10;}for(int i=n-1;i>=0;i--){if(!gamma){high[i]=state;if(H[i]!=9)state=H[i]>=10;}else{if(H[i]!=9)state=H[i]>=10;high[i]=state;}}for(int i=0;i<n;i++){if(!gamma)out[i]=low[i]+((H[i]+high[i])%10);else if(i==0)out[i]=low[i]+1;else out[i]=low[i]+((H[i-1]+high[i])%10);}}
V initial_collar(int q,const V&J,int collar){int root=34+9*q;int n=root+collar;V H(n);for(int i=0;i<34;i++)H[i]=B[i];for(int i=34;i<root;i++)H[i]=W[(i-34)%9];for(int i=root;i<root+(int)J.size();i++)H[i]=J[i-root];int us=root+(int)J.size();for(int i=us;i<n;i++)H[i]=U6[(i-us)%6];return H;}
int main(int argc,char**argv){int q=24,k=100,phase=1,steps=240,collar=320;uint64_t start=0,limit=UINT64_MAX;for(int i=1;i<argc;i++){string a=argv[i];if(a=="--q"&&i+1<argc)q=stoi(argv[++i]);else if(a=="--k"&&i+1<argc)k=stoi(argv[++i]);else if(a=="--phase"&&i+1<argc)phase=stoi(argv[++i]);else if(a=="--steps"&&i+1<argc)steps=stoi(argv[++i]);else if(a=="--collar"&&i+1<argc)collar=stoi(argv[++i]);else if(a=="--start"&&i+1<argc)start=stoull(argv[++i]);else if(a=="--limit"&&i+1<argc)limit=stoull(argv[++i]);else{cerr<<"bad argument "<<a<<"\n";return 2;}}
 if(q<24||k<100||phase!=1||steps!=240||collar<320)throw runtime_error("this shard requires phase=1, q>=24, k>=100, 240 steps, collar>=320");
 const uint64_t nJ3=19ULL*19*19,nJ4=19ULL*19*19*19,totalAll=nJ3+nJ4;uint64_t end=min(totalAll,start+limit),tested=0,clockFail=0,bFail=0,prefixFail=0,prefixRestored=0;const int rootLen=34+9*q,M=rootLen+collar;V target=B;for(int i=0;i<q;i++)target.insert(target.end(),W.begin(),W.end());
 array<V,241> traj;traj[0]=U6;for(int t=0;t<steps;t++)traj[t+1]=bulk_step(traj[t],GAM[(phase+t)%12]);if(traj[steps]!=U6)throw runtime_error("U6 row fails 240-step return at phase 1");
 int maxLeft=0,maxRight=0;for(int t=0;t<steps;t++){const V&u=traj[t];maxLeft=max(maxLeft,t+1+(int)count_if(u.begin(),u.end(),[](int x){return x==9;}));}
 int l=0,r=0;for(int t=0;t<steps;t++){const V&u=traj[t];l+=1+(u[l%6]==9);r+=1+(u[(5-r%6+6)%6]==9)-GAM[(phase+t)%12];}maxLeft=l;maxRight=r;
 V w=W;int m0=rootLen,m=m0,maxWLoss=0;for(int t=0;t<steps;t++){int r9=0;while(w[(m-35-r9+900000)%9]==9)r9++;m-=1+r9-GAM[(phase+t)%12];maxWLoss=max(maxWLoss,m0-m);w=bulk_step(w,GAM[(phase+t)%12]);}
 for(uint64_t ix=start;ix<end;ix++){int len;uint64_t jc;if(ix<nJ3){len=3;jc=ix;}else{uint64_t y=ix-nJ3;len=4;jc=y;}V J=decode(jc,len);int ustart=rootLen+len;V H=initial_collar(q,J,collar),Q(M),low(M),high(M);tested++;bool ok=true;for(int t=0;t<steps;t++){int g=H[0]>=10;if(g!=GAM[(phase+t)%12]){clockFail++;ok=false;break;}local_step_into(H,traj[t],ustart,g,low,high,Q);H.swap(Q);}if(!ok)continue;bool bSame=equal(B.begin(),B.end(),H.begin());if(!bSame)bFail++;if(starts(H,target))prefixRestored++;else prefixFail++;}
 cout<<"phase="<<phase<<" q="<<q<<" k="<<k<<" steps="<<steps<<" collar="<<collar<<" U6=";for(int x:U6)cout<<x<<',';cout<<"\n";cout<<"J_count="<<totalAll<<" range=["<<start<<","<<end<<") tested="<<tested<<"\n";cout<<"clock_failures="<<clockFail<<" root_B_mismatches="<<bFail<<" W9_endpoint_failures="<<prefixFail<<" W9_endpoint_restorations="<<prefixRestored<<"\n";cout<<"U6_cone_left="<<maxLeft<<" right="<<maxRight<<" W9_max_loss="<<maxWLoss<<" W_insert_cut_guard="<<(rootLen-52-maxWLoss)<<" U_insert_cut_guard="<<(330-maxLeft)<<" center_distance_at_k100=600\n";if(start||end!=totalAll)cout<<"PARTIAL RANGE: no exhaustion claim.\n";else cout<<"FINITE-DOMAIN COMPLETE: endpoint-W9 restoration checked for every J; centre eliminated only by the 240-step U6 reset/cone argument.\n";
}
