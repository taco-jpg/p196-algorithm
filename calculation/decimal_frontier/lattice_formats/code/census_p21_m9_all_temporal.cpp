// Exact ALL temporal periods for reflective spatial-m9 bulk, decimal p21.
// Reuse the independently tested carry map and selftest, not a second copy.
#define main previous_census_main
#include "census_p21_m9_superperiod8.cpp"
#undef main
#include <map>
#include <vector>
#include <cstdint>
static constexpr int N=2476099; // 19^5
static void decodeRow(int axis,int id,int *x,const int *rep){
  for(int j=0;j<5;j++){int i=rep[j],k=(axis+M-i)%M;
    x[i]=x[k]=id%TOP;id/=TOP;}
}
static int encodeRow(const int*x,const int*rep){int n=0,pow=1;for(int j=0;j<5;j++){n+=x[rep[j]]*pow;pow*=TOP;}return n;}
static bool blockStep(int *x){int y[M];for(int t=0;t<P;t++){
    if(!phi(x,G[t]-'0',y))return false;memcpy(x,y,sizeof(int)*M);}return true;}
int main(int argc,char**argv){
 if(argc==2 && string(argv[1])=="--selftest")return previous_census_main(argc,argv);
 if(argc<4){fprintf(stderr,"usage: scan CHECKPOINT SUMMARY CYCLE_ROWS\n");return 2;}
 int first=0;FILE*f=fopen(argv[1],"r");if(f){fscanf(f,"%d",&first);fclose(f);}
 if(first<0||first>9)return 3;
 vector<int> next(N,-1),where(N,-1),stack;
 vector<unsigned char>visited(N,0);
 for(int axis=first;axis<9;axis++){
  int rep[5],nr=0;for(int i=0;i<M;i++)if(i<=(axis+M-i)%M)rep[nr++]=i;
  if(nr!=5)return 4;
  long long undefined=0;
  for(int id=0;id<N;id++){
   int x[M];decodeRow(axis,id,x,rep);
   if(!blockStep(x)){undefined++;continue;}
   for(int j=0;j<M;j++)if(x[j]!=x[(axis+M-j)%M])return 5;
   next[id]=encodeRow(x,rep);
  }
  std::fill(visited.begin(),visited.end(),0);
  std::fill(where.begin(),where.end(),-1);
  std::map<int,long long> all,primitive,starts;
  for(int id=0;id<N;id++){
   if(visited[id])continue;
   stack.clear();int v=id;
   while(v>=0 && !visited[v]){visited[v]=1;where[v]=stack.size();stack.push_back(v);v=next[v];}
   if(v>=0 && visited[v]==1){
    int k=int(stack.size())-where[v];all[k]++;
    int x[M];decodeRow(axis,v,x,rep);
    if(spatial9(x)){
     primitive[k]++;starts[k]+=k;
     int original[M];memcpy(original,x,sizeof x);int a=axis;
     for(int t=0;t<k*P;t++){
      for(int j=0;j<M;j++)if(x[j]!=x[(a+M-j)%M])return 6;
      int y[M],z[M],g=G[t%P]-'0';
      if(!phi(x,g,y)||!phi_independent(x,g,z)||memcmp(y,z,sizeof y))return 7;
      memcpy(x,y,sizeof x);a=(a+g)%M;
     }
     if(memcmp(original,x,sizeof x)||a!=axis)return 8;
     FILE*fc=fopen(argv[3],"a");if(!fc)return 9;
     fprintf(fc,"AXIS=%d K=%d ROW=",axis,k);
     for(int j=0;j<M;j++)fprintf(fc,"%d%s",original[j],j+1<M?",":"\n");fclose(fc);
    }
   }
   for(int q:stack){visited[q]=2;where[q]=-1;}
  }
  FILE*out=fopen(argv[2],"a");if(!out)return 10;
  fprintf(out,"AXIS=%d N=%d DEAD=%lld ALL_CYCLES=%lld PRIM_CYCLES=%lld\n",
   axis,N,undefined,[&](){long long z=0;for(auto &it:all)z+=it.second;return z;}(),
   [&](){long long z=0;for(auto &it:primitive)z+=it.second;return z;}());
  for(auto [k,n]:all)fprintf(out,"CYCLE_LENGTH axis=%d k=%d count=%lld primitive_cycles=%lld primitive_labelled_starts=%lld\n",
   axis,k,n,primitive[k],starts[k]);
  fclose(out);
  string tmp=string(argv[1])+".tmp";f=fopen(tmp.c_str(),"w");if(!f)return 11;
  fprintf(f,"%d\n",axis+1);fclose(f);rename(tmp.c_str(),argv[1]);
  fprintf(stderr,"AXIS DONE %d primitive cycles=%lld\n",axis,
   [&](){long long z=0;for(auto &it:primitive)z+=it.second;return z;}());
 }
 puts("ALL AXES COMPLETE");return 0;
}
