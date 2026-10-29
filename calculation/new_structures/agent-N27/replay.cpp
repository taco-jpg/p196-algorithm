// N27: exact neutral-template evolution versus independent decimal schoolbook addition.
// Reproduce: g++ -O3 -std=c++17 replay.cpp -o replay; ./replay 3000 12000 20000 0
// Alternative exterior: ./replay 40 1000 333 1
#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <vector>
using std::vector;
using V=vector<int>;
static void require(bool yes,const char*msg,int t){if(!yes){fprintf(stderr,"FAIL step=%d %s\n",t,msg);exit(2);}}
static int norm(const V&src,int c,V&dst){dst.resize(src.size());for(size_t i=0;i<src.size();++i){const int s=src[i]+c;dst[i]=s%10;c=s/10;}return c;}
static V pairword(const V&d){V p(d.size());for(size_t i=0;i<d.size();++i)p[i]=d[i]+d[d.size()-i-1];return p;}
static V integer_step(const V&d){V out;out.reserve(d.size()+1);int c=0;for(size_t i=0;i<d.size();++i){int s=d[i]+d[d.size()-i-1]+c;out.push_back(s%10);c=s/10;}if(c)out.push_back(c);return out;}
static bool palindrome(const V&d){for(size_t i=0;i<d.size()/2;++i)if(d[i]!=d[d.size()-1-i])return false;return true;}
static V build(const V&B,const V&C,int g){V P;P.reserve(2*B.size()+2*(size_t)g+C.size());P.insert(P.end(),B.begin(),B.end());P.insert(P.end(),g,9);P.insert(P.end(),C.begin(),C.end());P.insert(P.end(),g,9);P.insert(P.end(),B.rbegin(),B.rend());return P;}
static V seed_from_pairs(const V&P){V d(P.size());for(size_t i=0;i<P.size()/2;++i){int j=P.size()-1-i;d[i]=std::min(9,P[i]);d[j]=P[i]-d[i];if(i==0&&d[j]==0){d[i]--;d[j]++;}}if(P.size()%2)d[P.size()/2]=P[P.size()/2]/2;return d;}
struct S{V B,C;int g;int e1,e2,gam,u,v;};
static bool template_step(S& s){V a,c,revnorm,BB,CC;int e1=norm(s.B,0,a),e2=norm(s.C,e1,c);s.e1=e1;s.e2=e2;if(e1==e2)return false;V RB(s.B.rbegin(),s.B.rend());int gam=norm(RB,e2,revnorm);s.gam=gam;
 if(gam){BB.resize(s.B.size()+1);for(size_t i=0;i<BB.size();++i)BB[i]=(i<s.B.size()?a[i]:9*(1-e1))+(i?revnorm[s.B.size()-i]:1);CC.resize(s.C.size()+1);for(size_t i=0;i<CC.size();++i)CC[i]=(i<s.C.size()?c[i]:9*(1-e2))+(i?c[s.C.size()-i]:9*(1-e2));}
 else{BB.resize(s.B.size());for(size_t i=0;i<BB.size();++i)BB[i]=a[i]+revnorm[s.B.size()-1-i];CC.resize(s.C.size());for(size_t i=0;i<CC.size();++i)CC[i]=c[i]+c[s.C.size()-1-i];}
 int u=0;while(!BB.empty()&&BB.back()==9){BB.pop_back();++u;}int v=0;while(CC.size()>=2&&CC.front()==9&&CC.back()==9){CC.erase(CC.begin());CC.pop_back();++v;}
 s.u=u;s.v=v;s.g+=u+v-gam;s.B.swap(BB);s.C.swap(CC);return true;
}
static uint64_t hash(const V&a){uint64_t z=1469598103934665603ULL;for(int x:a){z^=(uint64_t)x+1;z*=1099511628211ULL;}return z;}
int main(int argc,char**argv){int m=argc>1?atoi(argv[1]):3000;int g=argc>2?atoi(argv[2]):12000;int N=argc>3?atoi(argv[3]):20000;
 require(m>0&&g>0&&N>0,"inputs must be positive",0);
 S s{{12,9},{6},g,0,0,0,0,0};if(argc>4&&atoi(argv[4])==1)s.B={2,14,14};
 s.C.insert(s.C.end(),m,9);s.C.push_back(6);
 V d=seed_from_pairs(build(s.B,s.C,s.g));require(d.back()!=0,"seed leading zero",0);
 int gain=0,trims=0,minGap=s.g;uint64_t trace=1469598103934665603ULL;
 for(int t=0;t<=N;++t){
  require(!palindrome(d),"palindrome encountered",t);
  require(s.g>0,"outer neutral band exhausted",t);
  require(s.B.size()>0&&s.B[0]!=0,"leading pair coefficient invalid",t);
  V expected=build(s.B,s.C,s.g);V actual=pairword(d);
  require(expected==actual,"predicted full pairword disagrees with schoolbook",t);
  trace=(trace ^ hash(actual))*1099511628211ULL;
  if(t==0||t==1||t==100||t==1000||t==5000||t==10000||t==15000||t==20000){
   printf("STEP %d n=%zu gap=%d B=%zu C=%zu digitHash=%016llx pairHash=%016llx e1=%d e2=%d\n",t,d.size(),s.g,s.B.size(),s.C.size(),(unsigned long long)hash(d),(unsigned long long)hash(actual),s.e1,s.e2);fflush(stdout);
  }
  if(t==N)break;
  V dnext=integer_step(d);
  int change=(int)dnext.size()-(int)d.size();
  bool ok=template_step(s);
  require(ok,"carry-flip hypothesis failed",t);
  require(s.g>0,"gap exhausted after step",t);
  require(s.gam==change,"predicted length change differs",t);
  gain+=s.gam;trims+=s.u+s.v;minGap=std::min(minGap,s.g);
  d.swap(dnext);
 }
 printf("PASS steps=%d minGap=%d finalGap=%d finalN=%zu totalOverflow=%d totalTrims=%d traceHash=%016llx\n",N,minGap,s.g,d.size(),gain,trims,(unsigned long long)trace);
}