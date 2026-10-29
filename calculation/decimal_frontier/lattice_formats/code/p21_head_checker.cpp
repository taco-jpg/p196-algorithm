// Independently reconstructs carry edges recursively, and runs iterative Tarjan SCC.
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <algorithm>
#include <cstdint>
using namespace std;
const char*g="001001010101001010101";
int K,ns;
void decode(int z,int*x){for(int i=K-1;i>0;i--){x[i]=z%19;z/=19;}x[0]=z+1;}
int encode(const int*x){int v=x[0]-1;for(int i=1;i<K;i++)v=19*v+x[i];return v;}
int main(int argc,char**argv){
 if(argc!=3)return 2;K=atoi(argv[1]);if(K<2||K>4)return 3;
 ns=18;for(int i=1;i<K;i++)ns*=19;
 int N=ns*21;vector<vector<int>>adj(N);uint64_t edges=0;
 for(int t=0;t<21;t++)for(int base=0;base<ns;base++){
  int x[4],y[4];decode(base,x);int gamma=g[t]-'0';auto &out=adj[t*ns+base];
  auto recurse=[&](auto&&self,int j,int low,int demand,int partner)->void{
   if(j==K){out.push_back(((t+1)%21)*ns+encode(y));return;}
   for(int cj=0;cj<2;cj++){
    if((x[j]+cj)/10!=demand)continue;
    y[j]=(x[j]+low)%10+(gamma?partner:(x[j]+cj)%10);
    if(y[j]>18||(j==0&&y[j]==0))continue;
    self(self,j+1,(x[j]+low)/10,cj,(x[j]+cj)%10);
   }
  };
  recurse(recurse,0,0,gamma,1);
  sort(out.begin(),out.end());out.erase(unique(out.begin(),out.end()),out.end());edges+=out.size();
 }
 vector<int>num(N,-1),low(N,-1),comp(N,-1),stack;
 vector<uint8_t>on(N,0);int timer=0,nc=0;vector<int>size;
 for(int v0=0;v0<N;v0++){
  if(num[v0]>=0)continue;
  vector<pair<int,int>>frames{{v0,0}};num[v0]=low[v0]=timer++;stack.push_back(v0);on[v0]=1;
  while(!frames.empty()){
   int v=frames.back().first;int &next=frames.back().second;
   if(next<(int)adj[v].size()){
    int w=adj[v][next++];
    if(num[w]<0){num[w]=low[w]=timer++;stack.push_back(w);on[w]=1;frames.push_back({w,0});}
    else if(on[w])low[v]=min(low[v],num[w]);
   }else{
    if(low[v]==num[v]){
     int cnt=0;
     while(true){int w=stack.back();stack.pop_back();on[w]=0;comp[w]=nc;cnt++;if(w==v)break;}
     size.push_back(cnt);nc++;
    }
    frames.pop_back();if(!frames.empty()){int parent=frames.back().first;low[parent]=min(low[parent],low[v]);}
   }
  }
 }
 vector<uint8_t>cyclic(nc,0);
 for(int v=0;v<N;v++)for(int w:adj[v])if(comp[v]==comp[w]&&(size[comp[v]]>1||w==v))cyclic[comp[v]]=1;
 int ccount=0,core=0,zero=0;for(int c=0;c<nc;c++)if(cyclic[c])ccount++;
 FILE*f=fopen(argv[2],"w");if(!f)return 4;
 for(int v=0;v<N;v++)if(cyclic[comp[v]]){
  core++;if(v<ns){zero++;int x[4];decode(v,x);fprintf(f,"K%d",K);for(int i=0;i<K;i++)fprintf(f," %d",x[i]);fprintf(f,"\n");}
 }
 fclose(f);printf("K=%d vertices=%d edges=%llu cyclic_scc=%d cyclic_nodes=%d phase0=%d\n",K,N,(unsigned long long)edges,ccount,core,zero);
 return 0;
}
