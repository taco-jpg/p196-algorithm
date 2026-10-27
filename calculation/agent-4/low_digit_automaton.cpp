// Independent necessary first-coordinate overflow filter, base 10, Agent 4 T2.
// Passing this test does not imply a full B or C cycle.
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <string>
using namespace std;
using Mask = uint32_t;
static array<Mask,18> edges[2];
void initialize(){
  for(int x=1;x<=18;x++) for(int c=0;c<=1;c++){
    int g=(x+c)/10;
    int y=g ? x%10+1 : 2*x+c;
    if(y>=1 && y<=18) edges[g][x-1] |= Mask(1)<<(y-1);
  }
}
bool feasible(uint64_t w,int p){
  array<Mask,18> states{},next{};
  for(int x=0;x<18;x++)states[x]=Mask(1)<<x;
  for(int t=0;t<p;t++){
    next.fill(0);
    int bit=(w>>t)&1;
    for(int x=0;x<18;x++){
      Mask m=edges[bit][x];
      while(m){int y=__builtin_ctz(m);m&=m-1;next[y]|=states[x];}
    }
    states=next;
  }
  for(int x=0;x<18;x++)if(states[x]&(Mask(1)<<x))return true;
  return false;
}
uint64_t canon(uint64_t w,int p){
  uint64_t result=w,mask=(uint64_t(1)<<p)-1;
  for(int r=1;r<p;r++){
    uint64_t rot=(w>>r)|(w<<(p-r)&mask);
    if(rot<result)result=rot;
  }
  return result;
}
int main(int argc,char**argv){
  initialize();
  if(argc==3 && string(argv[1])=="--check"){
    string s=argv[2];int p=s.size();
    if(p<1||p>24)return 2;
    uint64_t word=0;
    for(int t=0;t<p;t++){
      if(s[t]!='0'&&s[t]!='1')return 2;
      if(s[t]=='1')word|=uint64_t(1)<<t;
    }
    printf("%s %s\n",s.c_str(),feasible(word,p)?"PASSES NECESSARY TEST":"IMPOSSIBLE FOR B-CYCLE");
    return 0;
  }
  if(argc==3 && string(argv[1])=="--emit"){
    int p=atoi(argv[2]);
    if(p<1||p>24)return 2;
    for(uint64_t w=0;w<(uint64_t(1)<<p);w++){
      if(canon(w,p)!=w||!feasible(w,p))continue;
      for(int t=0;t<p;t++)putchar('0'+((w>>t)&1));
      putchar('\n');
    }
    return 0;
  }
  int maxp=argc>=2?atoi(argv[1]):20;
  if(maxp<1||maxp>24)return 2;
  for(int p=1;p<=maxp;p++){
    uint64_t total=0,ok=0;
    array<uint64_t,25> byG{},yesG{};
    for(uint64_t w=0;w<(uint64_t(1)<<p);w++){
      if(canon(w,p)!=w)continue;
      total++;
      int k=__builtin_popcountll(w);
      byG[k]++;
      if(feasible(w,p)){ok++;yesG[k]++;}
    }
    printf("p=%d necklaces=%llu feasible=%llu impossible=%llu by-overflows=",
      p,(unsigned long long)total,(unsigned long long)ok,(unsigned long long)(total-ok));
    for(int k=0;k<=p;k++)if(byG[k])printf("%d:%llu/%llu,",k,(unsigned long long)yesG[k],(unsigned long long)byG[k]);
    puts("");
  }
}