// Exact K<=4 decimal p21 root-head temporal transition automaton.
// Enumerates carry masks; iterative Kosaraju SCC.
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <algorithm>
#include <cstdint>
using namespace std;
static const char*g="001001010101001010101";
int K,totalState;
int encode(const int*x){int s=x[0]-1;for(int j=1;j<K;j++)s=s*19+x[j];return s;}
void decode(int s,int*x){for(int j=K-1;j>=1;j--){x[j]=s%19;s/=19;}x[0]=s+1;}
int main(int argc,char**argv){
 if(argc!=3){fprintf(stderr,"usage: head_primary K OUTPUT\n");return 2;}
 K=atoi(argv[1]);if(K<2||K>4)return 3;
 totalState=18;for(int i=1;i<K;i++)totalState*=19;
 int N=21*totalState;
 vector<vector<int>>adj(N),rev(N);
 uint64_t edges=0;
 for(int t=0;t<21;t++){
  int gam=g[t]-'0';int x[4],y[4];
  for(int id=0;id<totalState;id++){
   decode(id,x);auto&out=adj[t*totalState+id];
   for(int mask=0;mask<(1<<K);mask++){
    int L=0,H=gam,Y=1,ok=1;
    for(int j=0;j<K;j++){
     int cj=(mask>>j)&1;
     if((x[j]+cj)/10!=H){ok=0;break;}
     y[j]=(x[j]+L)%10+(gam?Y:(x[j]+cj)%10);
     if(y[j]>18||(j==0&&y[j]==0)){ok=0;break;}
     Y=(x[j]+cj)%10;L=(x[j]+L)/10;H=cj;
    }
    if(ok)out.push_back(((t+1)%21)*totalState+encode(y));
   }
   sort(out.begin(),out.end());out.erase(unique(out.begin(),out.end()),out.end());
   for(int v:out){rev[v].push_back(t*totalState+id);edges++;}
  }
 }
 vector<uint8_t>visited(N,0);vector<int>order;order.reserve(N);
 for(int i=0;i<N;i++)if(!visited[i]){
  vector<pair<int,int>>stack{{i,0}};visited[i]=1;
  while(!stack.empty()){
   int v=stack.back().first;int&idx=stack.back().second;
   if(idx<(int)adj[v].size()){
    int w=adj[v][idx++];if(!visited[w]){visited[w]=1;stack.push_back({w,0});}}
   else{order.push_back(v);stack.pop_back();}
  }
 }
 vector<int>comp(N,-1),size;int nc=0;
 for(auto it=order.rbegin();it!=order.rend();it++){
  int root=*it;if(comp[root]!=-1)continue;
  vector<int>stack{root};comp[root]=nc;int cnt=0;
  while(!stack.empty()){
   int v=stack.back();stack.pop_back();cnt++;
   for(int w:rev[v])if(comp[w]<0){comp[w]=nc;stack.push_back(w);}
  }
  size.push_back(cnt);nc++;
 }
 vector<uint8_t>cyclic(nc,0);
 for(int v=0;v<N;v++)for(int w:adj[v])if(comp[v]==comp[w]&&(size[comp[v]]>1||v==w))cyclic[comp[v]]=1;
 int scc=0,core=0,phase0=0;
 for(int c=0;c<nc;c++)if(cyclic[c])scc++;
 FILE*f=fopen(argv[2],"w");if(!f)return 4;
 for(int v=0;v<N;v++)if(cyclic[comp[v]]){
  core++;if(v<totalState){phase0++;int x[4];decode(v,x);fprintf(f,"K%d",K);for(int j=0;j<K;j++)fprintf(f," %d",x[j]);fprintf(f,"\n");}
 }
 fclose(f);
 printf("K=%d vertices=%d edges=%llu cyclic_scc=%d cyclic_nodes=%d phase0=%d\n",K,N,(unsigned long long)edges,scc,core,phase0);
 return (K==2 ? (edges==5586&&scc==1&&core==71&&phase0==4) :
         K==3 ? (edges==106134&&scc==1&&core==115&&phase0==4) :
                (edges==2016546&&scc==1&&core==427&&phase0==18))?0:5;
}
