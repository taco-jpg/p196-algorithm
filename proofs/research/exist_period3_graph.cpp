#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>
// All-period functional graph for a reflection-compatible period-three q core.
// A state consists of k outer pair sums P, core residue r modulo3,
// and a cyclic core Q with Q_i=Q_(r-1-i). The fixed reflection coefficient
// is even, as required by the odd-length members of the same family.
// The full finite word is P ++ periodic(Q,3m+r) ++ reverse(P), m>=4.
static constexpr uint32_t dead=std::numeric_limits<uint32_t>::max();
using Prefix=std::array<int,8>;
using Triple=std::array<int,3>;
int mod3(int x){return (x%3+3)%3;}
Triple bulk_decode(int state){
 int r=state/190,a=2*((state%190)/19),b=state%19;
 Triple q{};for(int i=0;i<3;i++)q[i]=(mod3(2*i)==mod3(r-1)?a:b);
 return q;
}
int bulk_encode(Triple q,int r){
 int a=-1,b=-1;
 for(int i=0;i<3;i++){
  if(q[i]<0||q[i]>18||q[i]!=q[mod3(r-1-i)])throw std::runtime_error("bulk symmetry");
  if(mod3(2*i)==mod3(r-1))a=q[i];else b=q[i];
 }
 if(a%2)throw std::runtime_error("odd central coefficient");
 return r*190+(a/2)*19+b;
}
Prefix decode(uint32_t code,int k){Prefix p{};p[0]=1+code%18;code/=18;for(int i=1;i<k;i++){p[i]=code%19;code/=19;}return p;}
uint32_t encode(Prefix p,int k){uint32_t s=0;for(int i=k-1;i>=1;i--)s=s*19+p[i];return s*18+p[0]-1;}
struct Step{bool valid=false;int overflow=0;Prefix p{};Triple q{};int r=0;};
Step step(Prefix p,int k,int core,int periods){
 int r=core/190,M=3*periods+r,n=2*k+M;
 Triple Q=bulk_decode(core);std::array<int,80>q{},d{},w{};
 for(int i=0;i<k;i++)q[i]=q[n-1-i]=p[i];
 for(int i=0;i<M;i++)q[k+i]=Q[i%3];
 int c=0;for(int i=0;i<n;i++){int s=q[i]+c;d[i]=s%10;c=s/10;}
 int L=n+c;if(c)d[n]=c;
 for(int i=0;i<L;i++)w[i]=d[i]+d[L-1-i];
 Step z;z.overflow=c;z.r=(r+c)%3;
 for(int i=0;i<3;i++)z.q[i]=w[k+6+i];
 for(int i=k;i<L-k;i++)if(w[i]!=z.q[(i-k)%3])return z;
 for(int i=0;i<k;i++)z.p[i]=w[i];
 bulk_encode(z.q,z.r);z.valid=true;return z;
}
bool safe(Prefix p,int k,Triple q){
 bool low=true,exc=p[0]==11;
 for(int i=0;i<k;i++){low&=p[i]<=9;exc&=p[i]==0||p[i]==11;}
 for(int x:q){low&=x<=9;exc&=x==0||x==11;}
 return !low&&!exc;
}
void array(std::ostream&o,Prefix p,int k){o<<'[';for(int i=0;i<k;i++){if(i)o<<',';o<<p[i];}o<<']';}
int main(int argc,char**argv){
 int lo=argc>1?std::stoi(argv[1]):1,hi=argc>2?std::stoi(argv[2]):4;
 std::string filename=argc>3?argv[3]:"exist_period3_graph_results.json";
 if(lo<1||hi>5)throw std::runtime_error("unsupported width");
 std::ofstream f(filename);f<<"{\"model\":\"symmetric period3 q core, arbitrary clock and period\",\"middle_period_controls\":[4,5],\"widths\":[\n";
 for(int k=lo;k<=hi;k++){
  auto t=std::chrono::steady_clock::now();uint32_t per=18;for(int i=1;i<k;i++)per*=19;
  uint32_t total=570*per;std::vector<uint32_t>next(total,dead);uint64_t valid=0,unsafe=0,fail=0,over=0;
  for(uint32_t id=0;id<total;id++){
   int core=id/per;Prefix p=decode(id%per,k);
   if(!safe(p,k,bulk_decode(core))){unsafe++;continue;}
   Step a=step(p,k,core,4),b=step(p,k,core,5);
   if(a.valid!=b.valid||a.overflow!=b.overflow)throw std::runtime_error("length control mismatch");
   if(!a.valid){fail++;continue;}
   if(a.q!=b.q||a.p!=b.p||a.r!=b.r)throw std::runtime_error("result mismatch");
   valid++;over+=a.overflow;next[id]=bulk_encode(a.q,a.r)*per+encode(a.p,k);
  }
  std::vector<uint8_t>color(total,0);uint64_t cycles=0,cycle_states=0,maxsegment=0;
  std::vector<std::vector<uint32_t>>witnesses;
  for(uint32_t id=0;id<total;id++){
   if(color[id])continue;uint32_t v=id;uint64_t depth=0;
   while(v!=dead&&!color[v]){color[v]=1;v=next[v];depth++;}
   if(depth>maxsegment)maxsegment=depth;
   if(v!=dead&&color[v]==1){std::vector<uint32_t>c;uint32_t u=v;do{c.push_back(u);u=next[u];}while(u!=v);cycles++;cycle_states+=c.size();if(witnesses.size()<20)witnesses.push_back(c);}
   v=id;while(v!=dead&&color[v]==1){color[v]=2;v=next[v];}
  }
  double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-t).count();
  if(k!=lo)f<<",\n";
  f<<"{\"boundary_width\":"<<k<<",\"states\":"<<total<<",\"unsafe_states\":"<<unsafe<<",\"core_mismatches\":"<<fail<<",\"valid_edges\":"<<valid<<",\"overflow_edges\":"<<over<<",\"cycles\":"<<cycles<<",\"cycle_states\":"<<cycle_states<<",\"max_dfs_segment\":"<<maxsegment<<",\"seconds\":"<<sec<<",\"witnesses\":[";
  for(size_t i=0;i<witnesses.size();i++){
   if(i)f<<',';f<<'[';
   for(size_t j=0;j<witnesses[i].size();j++){
    if(j)f<<',';uint32_t id=witnesses[i][j];int core=id/per;Prefix p=decode(id%per,k);Triple q=bulk_decode(core);Step a=step(p,k,core,4);
    f<<"{\"prefix\":";array(f,p,k);f<<",\"bulk\":["<<q[0]<<','<<q[1]<<','<<q[2]<<"],\"residue\":"<<core/190<<",\"overflow\":"<<a.overflow<<'}';
   }f<<']';
  }f<<"]}";f.flush();
  std::cout<<"k="<<k<<" states="<<total<<" edges="<<valid<<" cycles="<<cycles<<" seconds="<<sec<<std::endl;
 }
 f<<"\n]}\n";
}
