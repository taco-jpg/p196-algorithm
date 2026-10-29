// Agent-8: all-temporal cut-charge classification for the decimal p21/m9 reflective bulk.
// Axis0 represents all nine axes by translation. Independent checker accompanies output.
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <vector>
#include <map>
#include <algorithm>
using namespace std;
constexpr int B=10,M=9,N=2476099;
static const char* G="001001010101001010101";
struct Row { unsigned char v[M]; };
Row decode(int id){ Row r={}; for(int j=0;j<5;j++){int x=id%19;id/=19;r.v[j]=r.v[(M-j)%M]=x;}return r; }
int encode(const Row&r){int n=0,pow=1;for(int j=0;j<5;j++){n+=r.v[j]*pow;pow*=19;}return n;}

bool step(const Row&r,int gamma,Row&out,int *Aout=nullptr,int *Dout=nullptr){
 int z=-1;for(int i=0;i<M;i++)if(r.v[i]!=9){z=i;break;}
 if(z<0)return false;
 int a[M]={},d[M]={},e[M],f[M];a[(z+1)%M]=d[(z+M-1)%M]=(r.v[z]>=B);
 for(int j=1;j<M;j++){int i=(z+j)%M;a[(i+1)%M]=(r.v[i]+a[i])/B;}
 for(int j=1;j<M;j++){int i=(z+M-j)%M;d[(i+M-1)%M]=(r.v[i]+d[i])/B;}
 for(int i=0;i<M;i++){e[i]=(r.v[i]+a[i])%B;f[i]=(r.v[i]+d[i])%B;}
 for(int i=0;i<M;i++)out.v[i]=e[i]+f[(i+M-gamma)%M];
 if(Aout)for(int i=0;i<M;i++){Aout[i]=a[i];Dout[i]=d[i];}
 return true;
}

bool independent(const Row&r,int gamma,Row&out,int *Aout=nullptr,int *Dout=nullptr){
 bool neutral=true;for(int i=0;i<M;i++)if(r.v[i]!=9)neutral=false;
 if(neutral)return false;
 int a[M]={},d[M]={};
 for(int backwards=0;backwards<2;backwards++){
  int good=0,candidate[M]={};
  for(int seed=0;seed<=1;seed++){
   int c=seed,q[M]={};
   for(int j=0;j<M;j++){int i=backwards?(M-j)%M:j;q[i]=c;c=(r.v[i]+c)/B;}
   if(c==seed){good++;memcpy(candidate,q,sizeof(candidate));}
  }
  if(good!=1){fprintf(stderr,"nonunique carry\n");exit(25);}
  memcpy(backwards?d:a,candidate,sizeof(candidate));
 }
 for(int i=0;i<M;i++)out.v[i]=(r.v[i]+a[i])%B+(r.v[(i+M-gamma)%M]+d[(i+M-gamma)%M])%B;
 if(Aout)for(int i=0;i<M;i++){Aout[i]=a[i];Dout[i]=d[i];}
 return true;
}
int afterBlock(Row r){Row next;for(int t=0;t<21;t++){if(!step(r,G[t]-'0',next))return -1;r=next;}return encode(r);}
bool primitive9(Row r){for(int d:{1,3}){bool ok=true;for(int i=0;i<M;i++)if(r.v[i]!=r.v[(i+d)%M])ok=false;if(ok)return false;}return true;}

int check_charge(Row r,int blocks){
 int Q[M]={};int weight=1,axis=0;Row orig=r, next,independentNext;
 for(int t=0;t<21*blocks;t++){
  int g=G[t%21]-'0';
  for(int j=0;j<M;j++)if(r.v[j]!=r.v[(axis+M-j)%M]){fprintf(stderr,"axis error t=%d\n",t);exit(21);}
  int a[M],d[M],aa[M],dd[M];
  if(!step(r,g,next,a,d)||!independent(r,g,independentNext,aa,dd)||memcmp(&next,&independentNext,sizeof(Row))){fprintf(stderr,"differential error\n");exit(22);}
  for(int k=0;k<M;k++){
   if(a[k]!=aa[k]||d[k]!=dd[k])exit(23);
   int L=a[k],H=(r.v[k]+d[k])/B,Y=g?(r.v[(k+M-1)%M]+d[(k+M-1)%M])%B:0;
   int kp=(k+1)%M;
   int Lp=a[kp], Hp=(r.v[kp]+d[kp])/B;
   int Yp=g?(r.v[k]+d[k])%B:0;
   if((r.v[k]+L)%B+(g?Y:(r.v[k]+Hp)%B)!=next.v[k] || Lp!=(r.v[k]+L)/B || H!=(r.v[k]+Hp)/B || (g&&Yp!=(r.v[k]+Hp)%B)){
      fprintf(stderr,"cut transition failure\n");exit(24);
   }
   Q[k]=(Q[k]+weight*(L-H+g*Y))%9;
  }
  weight=(weight*5)%9;axis=(axis+g)%M;r=next;
 }
 if(memcmp(&r,&orig,sizeof(Row))||axis!=0||weight!=1)exit(27);
 for(int k=1;k<M;k++)if((Q[k]+9)%9!=(Q[0]+9)%9){fprintf(stderr,"Q differs by cut\n");exit(28);}
 return (Q[0]+9)%9;
}

int main(int argc,char**argv){
 if(argc!=2){fprintf(stderr,"usage: m9_charge OUTPUT_CYCLE_REP_FILE\n");return 2;}
 vector<int32_t>next(N,-1);vector<uint8_t>status(N,0);vector<int> idx(N,-1),stack;
 for(int i=0;i<N;i++)next[i]=afterBlock(decode(i));
 map<pair<int,int>,int> hist;int total=0,primitive=0;FILE*f=fopen(argv[1],"w");if(!f)return 3;
 fprintf(f,"# axis0 decimal p21 spatial9 primitive row-cycle reps: k Q row[9]\n");
 for(int i=0;i<N;i++){
  if(status[i])continue;
  stack.clear();int v=i;
  while(v>=0&&status[v]==0){status[v]=1;idx[v]=stack.size();stack.push_back(v);v=next[v];}
  if(v>=0&&status[v]==1){
   int k=stack.size()-idx[v];total++;
   Row r=decode(v);
   if(primitive9(r)){
     primitive++;int Q=check_charge(r,k);hist[{k,Q}]++;
     fprintf(f,"%d %d",k,Q);for(int j=0;j<M;j++)fprintf(f," %u",(unsigned)r.v[j]);fprintf(f,"\n");
   }
  }
  for(int j:stack){status[j]=2;idx[j]=-1;}
 }
 fclose(f);
 printf("graph N=%d cycles=%d primitive9=%d\n",N,total,primitive);
 for(auto [p,n]:hist)printf("k=%d Q=%d cycles=%d\n",p.first,p.second,n);
 return (total==35&&primitive==23)?0:1;
}
