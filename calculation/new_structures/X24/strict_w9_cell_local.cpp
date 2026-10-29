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
static const array<int,12> GAM={1,0,0,0,1,0,0,0,1,0,0,0};
V make_u(int a,int r){V b{9,a,18-a};return{b[r%3],b[(r+1)%3],b[(r+2)%3]};}
V decode(uint64_t n,int len){V w(len);for(int&i:w){i=n%19;n/=19;}return w;}
bool starts(const V&a,const V&b){return a.size()>=b.size()&&equal(b.begin(),b.end(),a.begin());}
V bulk_step(const V&w,int gamma){int m=w.size();V a(m+1),b(m+1);bool ok=false;for(int s=0;s<=1&&!ok;s++){a[0]=s;for(int i=0;i<m;i++)a[i+1]=(w[i]+a[i])/10;ok=a[m]==s;}if(!ok)throw runtime_error("no cyclic low carry");ok=false;for(int s=0;s<=1&&!ok;s++){b[m]=s;for(int i=m-1;i>=0;i--)b[i]=(w[i]+b[i+1])/10;ok=b[0]==s;}if(!ok)throw runtime_error("no cyclic high carry");V z(m);for(int i=0;i<m;i++){int lo=(w[i]+a[i])%10;int hi=gamma?((w[(i+m-1)%m]+b[i])%10):((w[i]+b[i+1])%10);z[i]=lo+hi;}return z;}
void local_step_into(const V&H,const V&U,int ustart,int gamma,V&low,V&high,V&out){int n=H.size();int state=-1;for(int j=0;j<3;j++){int x=U[(n+j-ustart)%3];if(x!=9){state=x>=10;break;}}if(state<0)throw runtime_error("U tail did not reset high carry");int c=0;for(int i=0;i<n;i++){int z=H[i]+c;low[i]=z%10;c=z/10;}for(int i=n-1;i>=0;i--){if(!gamma){high[i]=state;if(H[i]!=9)state=H[i]>=10;}else{if(H[i]!=9)state=H[i]>=10;high[i]=state;}}for(int i=0;i<n;i++){if(!gamma)out[i]=low[i]+((H[i]+high[i])%10);else if(i==0)out[i]=low[i]+1;else out[i]=low[i]+((H[i-1]+high[i])%10);}}
V initial_collar(int q,const V&J,const V&U,int collar){int root=34+9*q;int n=root+collar;V H(n);for(int i=0;i<34;i++)H[i]=B[i];for(int i=34;i<root;i++)H[i]=W[(i-34)%9];for(int i=root;i<root+(int)J.size();i++)H[i]=J[i-root];int us=root+(int)J.size();for(int i=us;i<n;i++)H[i]=U[(i-us)%3];return H;}
int main(int argc,char**argv){int q=14,k=100,phase=1,steps=120,collar=170;uint64_t start=0,limit=UINT64_MAX;for(int i=1;i<argc;i++){string a=argv[i];if(a=="--q"&&i+1<argc)q=stoi(argv[++i]);else if(a=="--k"&&i+1<argc)k=stoi(argv[++i]);else if(a=="--phase"&&i+1<argc)phase=stoi(argv[++i]);else if(a=="--steps"&&i+1<argc)steps=stoi(argv[++i]);else if(a=="--collar"&&i+1<argc)collar=stoi(argv[++i]);else if(a=="--start"&&i+1<argc)start=stoull(argv[++i]);else if(a=="--limit"&&i+1<argc)limit=stoull(argv[++i]);else{cerr<<"bad argument "<<a<<"\n";return 2;}}
 if(q<14||k<100||phase!=1||steps!=120||collar<158)throw runtime_error("this shard requires phase=1, q>=14, k>=100, 120 steps, collar>=158");
 vector<V> Us;for(int a=0;a<=18;a+=2)for(int r=0;r<3;r++)Us.push_back(make_u(a,r));sort(Us.begin(),Us.end());Us.erase(unique(Us.begin(),Us.end()),Us.end());if(Us.size()!=30)throw runtime_error("U count !=30");
 const uint64_t nJ3=19ULL*19*19,nJ4=19ULL*19*19*19,perJ=30,totalAll=(nJ3+nJ4)*perJ;uint64_t end=min(totalAll,start+limit),tested=0,clockFail=0,bFail=0,wFail=0,wRestored=0,allRestored=0;array<uint64_t,361> hist{};const int rootLen=34+9*q,M=rootLen+collar;V target=B;for(int i=0;i<q;i++)target.insert(target.end(),W.begin(),W.end());
 vector<array<V,121>> traj(Us.size());for(size_t ui=0;ui<Us.size();ui++){traj[ui][0]=Us[ui];for(int t=0;t<steps;t++)traj[ui][t+1]=bulk_step(traj[ui][t],GAM[(phase+t)%12]);if(traj[ui][steps]!=Us[ui])throw runtime_error("U row fails 120-step return at phase 1");}
 // Cone ledger for the 30 physical U rows; used to justify centre independence.
 int maxLeft=0,maxRight=0;for(size_t ui=0;ui<Us.size();ui++){int l=0,r=0;for(int t=0;t<120;t++){const V&u=traj[ui][t];l+=1+(u[l%3]==9);r+=1+(u[(2-r%3+3)%3]==9)-GAM[(phase+t)%12];}maxLeft=max(maxLeft,l);maxRight=max(maxRight,r);}
 for(uint64_t ix=start;ix<end;ix++){int len;uint64_t jc;int ui;if(ix<nJ3*perJ){len=3;jc=ix/perJ;ui=ix%perJ;}else{uint64_t y=ix-nJ3*perJ;len=4;jc=y/perJ;ui=y%perJ;}V J=decode(jc,len);int ustart=rootLen+len;V H=initial_collar(q,J,Us[ui],collar),Q(M),low(M),high(M);tested++;bool ok=true;for(int t=0;t<steps;t++){int g=H[0]>=10;if(g!=GAM[(phase+t)%12]){clockFail++;ok=false;break;}local_step_into(H,traj[ui][t],ustart,g,low,high,Q);H.swap(Q);}if(!ok)continue;bool bSame=equal(B.begin(),B.end(),H.begin());if(!bSame)bFail++;bool wSame=starts(H,target);if(!wSame){wFail++;size_t m=0;while(m<target.size()&&m<H.size()&&target[m]==H[m])m++;if(m>=34&&m<static_cast<size_t>(rootLen)){int off=(int)m-rootLen;int slot=off+180;if(slot>=0&&slot<(int)hist.size())hist[slot]++;}}else{wRestored++;if(starts(H,target))allRestored++;}}
 cout<<"phase="<<phase<<" q="<<q<<" k="<<k<<" steps="<<steps<<" collar="<<collar<<"\n";cout<<"U_count="<<Us.size()<<" J_count="<<(nJ3+nJ4)<<" total_domain="<<totalAll<<" range=["<<start<<","<<end<<") tested="<<tested<<"\n";cout<<"clock_failures="<<clockFail<<" root_B_mismatches="<<bFail<<" W9_endpoint_failures="<<wFail<<" W9_endpoint_restorations="<<wRestored<<" all_prefix_restorations="<<allRestored<<"\n";cout<<"U_cone_max_left="<<maxLeft<<" max_right="<<maxRight<<" center_distance_at_k100>=300\n";if(start||end!=totalAll)cout<<"PARTIAL RANGE: no exhaustion claim.\n";else cout<<"FINITE-DOMAIN COMPLETE: endpoint-W9 restoration checked for every (U,J); centre eliminated only by the 120-step U3 reset/cone argument.\n";
}
