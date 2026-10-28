// Agent-2 exact finite-state transfer for a stationary first-defect column.
// COMPUTED necessary-condition test, NOT a decimal Lychrel certificate.
// Reproduce:
//  python3 calculation/decimal_frontier/lattice_kinks/code/agent2_boundary_data.py > /tmp/agent2_rec0_rows.txt
//  c++ -O3 -std=c++17 calculation/decimal_frontier/lattice_kinks/code/agent2_boundary_transfer.cpp -o /tmp/agent2_transfer
//  /tmp/agent2_transfer /tmp/agent2_rec0_rows.txt 4 9
// Data order: rec0 W[spatial][time] 20 rows, then transient B[spatial][time] 39 rows.

// For each k, compute indegree core of time-automaton on k consecutive columns.
// A (k+1)-cycle projects to a k-cycle, so lift only the surviving k indegree-core
// (which contains all cycles) by the next free digit. All other states can be excluded
// without a 19^(k+1) enumeration. x is fixed in spatial coordinates.
#include <bits/stdc++.h>
using namespace std;using u64=uint64_t;
int W[8][20], B[8][39];
int gam[8]={1,0,1,0,1,0,1,0};
int K=3, X=120;
vector<u64> pow19;
int cell(int t,int x){return W[t%8][(x-39+2000)%20];}
int acarry(int t,int x){for(int r=1;r<=60;r++){int v=cell(t,x-r);if(v!=9)return v>=10;}abort();}
int dcarry(int t,int x){for(int r=1;r<=60;r++){int v=cell(t,x+r);if(v!=9)return v>=10;}abort();}
u64 encode(int t,const int*z){u64 n=t;for(int i=K-1;i>=0;i--)n=19*n+z[i];return n;}
void decode(u64 n,int &t,int*z){for(int i=0;i<K;i++){z[i]=n%19;n/=19;}t=n;}
template<class F>void successors(u64 n, F emit){
 int t,v[16],dn[16],up[16],asc[17],ds[17],vv[16];decode(n,t,v);
 assert(t>=0&&t<8); if(v[0]==cell(t,X))return;
 asc[0]=acarry(t,X);
 for(int i=0;i<K;i++){up[i]=(v[i]+asc[i])%10;asc[i+1]=(v[i]+asc[i]>=10);}
 const int left=cell(t,X-1), ld=dcarry(t,X-1);
 for(int top=0;top<2;top++){
  ds[K]=top;
  for(int i=K-1;i>=0;i--){dn[i]=(v[i]+ds[i+1])%10;ds[i]=(v[i]+ds[i+1]>=10);}
  if((!gam[t] || left==9)&&ds[0]!=ld)continue;
  for(int i=0;i<K;i++){
   int second=gam[t]?(i==0?(left+ds[0])%10:dn[i-1]):dn[i];
   vv[i]=up[i]+second;
  }
  if(vv[0]!=cell(t+1,X))emit(encode((t+1)%8,vv));
 }
}
vector<u64> core(const vector<u64>& ids, u64 &edges){
// Sorted 64-bit key array; bounded memory even at 56M nodes.
 // This is slower per lookup than a hash table but needs only 12 bytes/node.
 const auto &lookup=ids;
 auto findid=[&](u64 key)->uint32_t {
  auto it=lower_bound(lookup.begin(),lookup.end(),key);
  if(it==lookup.end()||*it!=key)return UINT32_MAX;
  return (uint32_t)(it-lookup.begin());
 };
 vector<uint32_t> indeg(ids.size(),0);edges=0;
 for(u64 id:ids)successors(id,[&](u64 id2){
  uint32_t j=findid(id2);if(j==UINT32_MAX)return;
  ++indeg[j];++edges;
 });
 deque<uint32_t> q; for(uint32_t i=0;i<indeg.size();i++)if(!indeg[i])q.push_back(i);
 while(!q.empty()){
  uint32_t i=q.front();q.pop_front();
  successors(ids[i],[&](u64 id2){uint32_t j=findid(id2);if(j==UINT32_MAX)return;
   if(--indeg[j]==0)q.push_back(j);
  });
 }
 vector<u64> left;left.reserve(ids.size()/10);
 for(uint32_t i=0;i<ids.size();i++)if(indeg[i])left.push_back(ids[i]);
 return left;
}
int main(int argc,char**argv){if(argc<4){cerr<<"usage: data j maxk\n";return 2;}
 ifstream f(argv[1]);if(!f)return 2;for(int j=0;j<20;j++)for(int t=0;t<8;t++)f>>W[t][j];for(int j=0;j<39;j++)for(int t=0;t<8;t++)f>>B[t][j];
 X=119+stoi(argv[2]);int maxK=stoi(argv[3]);if(maxK>12)return 2;
 pow19={1};for(int i=1;i<=maxK;i++)pow19.push_back(19*pow19.back());
 vector<u64> prev;
 for(K=2;K<=maxK;K++){
  vector<u64> nodes;
  if(K==2){nodes.reserve(8*18*19);
   for(int t=0;t<8;t++)for(int d1=0;d1<19;d1++)for(int d0=0;d0<19;d0++)if(d0!=cell(t,X)){nodes.push_back(u64(t)*361+u64(d1)*19+d0);}
  }else{
   nodes.reserve(prev.size()*19);
   for(u64 id:prev){u64 t=id/pow19[K-1], word=id%pow19[K-1];
    for(int high=0;high<19;high++)nodes.push_back((t*19+high)*pow19[K-1]+word);
   }
  }
  sort(nodes.begin(),nodes.end());
  auto start=chrono::steady_clock::now();u64 edges=0;
  vector<u64> surv=core(nodes,edges);
  double seconds=chrono::duration<double>(chrono::steady_clock::now()-start).count();
  cout<<"j="<<argv[2]<<" k="<<K<<" candidates="<<nodes.size()<<" retained_edges="<<edges<<" survivor_core="<<surv.size()<<" seconds="<<fixed<<setprecision(3)<<seconds<<"\n"<<flush;
  prev.swap(surv);
  if(prev.empty())break;
 }
}