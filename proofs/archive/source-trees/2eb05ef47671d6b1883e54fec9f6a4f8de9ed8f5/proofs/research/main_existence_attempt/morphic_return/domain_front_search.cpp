#include <array>
#include <vector>
#include <iostream>
#include <fstream>
#include <map>
#include <chrono>
using namespace std;
using V=array<int,3>;
int mod(int i){return (i%3+3)%3;}
struct Bulk{V q,a,b,lo,hi;};
Bulk bulk(V q){
  Bulk z;z.q=q;int c=0;
  for(int t=0;t<2;t++)for(int i=0;i<3;i++){z.a[i]=c;c=(q[i]+c)/10;}
  c=0;for(int t=0;t<2;t++)for(int i=2;i>=0;i--){c=(q[i]+c)/10;z.b[i]=c;}
  for(int i=0;i<3;i++){z.lo[i]=(q[i]+z.a[i])%10;z.hi[i]=(q[i]+z.b[(i+1)%3])%10;}
  return z;
}
using Trace=array<Bulk,25>;
Trace trace(V q){
  Trace t;
  for(int k=0;k<=24;k++){
    t[k]=bulk(q);if(k==24)break;V n;
    for(int i=0;i<3;i++)n[i]=t[k].lo[i]+t[k].hi[mod(i-k%2)];q=n;
  }
  return t;
}
struct Dom{int l;vector<int> v;};
int at(const Dom& d,int i,const V& b,const V& c){
  return i<d.l?b[mod(i)]:i>=d.l+(int)d.v.size()?c[mod(i)]:d.v[i-d.l];
}
Dom step(const Dom& d,const Trace& b,const Trace& c,int t){
  int x=d.l-4,y=d.l+(int)d.v.size()+4,h=t%2,n=y-x;
  vector<int> lo(n),hi(n);int car=b[t].a[mod(x)];
  for(int i=x;i<y;i++){int z=at(d,i,b[t].q,c[t].q)+car;lo[i-x]=z%10;car=z/10;}
  car=c[t].b[mod(y)];
  for(int i=y-1;i>=x;i--){int z=at(d,i,b[t].q,c[t].q)+car;hi[i-x]=z%10;car=z/10;}
  vector<int> v(n-h);for(int i=x+h;i<y;i++)v[i-x-h]=lo[i-x]+hi[i-x-h];
  int l=x+h,a=0,e=v.size();
  while(a<e&&v[a]==b[t+1].q[mod(l+a)])a++;
  while(e>a&&v[e-1]==c[t+1].q[mod(l+e-1)])e--;
  return {l+a,vector<int>(v.begin()+a,v.begin()+e)};
}
bool equalshift(const Dom& end,const Dom& start,const V& b,const V& c,int shift){
  Dom s={start.l+shift,start.v};
  for(int i=min(end.l,s.l);i<max(end.l+(int)end.v.size(),s.l+(int)s.v.size());i++)
    if(at(end,i,b,c)!=at(s,i,b,c))return false;
  return true;
}
void word(const V& v){cout<<'['<<v[0]<<','<<v[1]<<','<<v[2]<<']';}
int main(int argc,char**argv){
  if(argc<2)return 2;ifstream input(argv[1]);int n;input>>n;vector<V> motifs(n);vector<Trace> tr;
  for(auto&v:motifs){for(auto&x:v)input>>x;tr.push_back(trace(v));if(tr.back()[24].q!=v)return 3;}
  int maxwidth=argc>2?stoi(argv[2]):1;double seconds=argc>3?stod(argv[3]):120;
  auto begin=chrono::steady_clock::now();long long tested=0,capped=0;map<int,int> emitted;map<int,long long> counts;bool timedout=false;
  for(int w=0;w<=maxwidth;w++)for(int bi=0;bi<n;bi++)for(int ci=0;ci<n;ci++)if(bi!=ci){
    int limit=1;for(int j=0;j<w;j++)limit*=19;
    for(int code=0;code<limit;code++){
      if(tested%1024==0&&chrono::duration<double>(chrono::steady_clock::now()-begin).count()>seconds){timedout=true;goto done;}
      Dom d={0,vector<int>(w)};int z=code;for(auto&v:d.v){v=z%19;z/=19;}Dom initial=d;bool cap=false;
      for(int t=0;t<24;t++){d=step(d,tr[bi],tr[ci],t);if(d.v.size()>256){cap=true;break;}}
      tested++;if(cap){capped++;continue;}
      for(int shift=-48;shift<=48;shift+=3)if(equalshift(d,initial,motifs[bi],motifs[ci],shift)){
        counts[shift]++;
        if(emitted[shift]<100){
          cout<<"{\"kind\":\"candidate_local_front\",\"left\":";word(motifs[bi]);cout<<",\"right\":";word(motifs[ci]);
          cout<<",\"patch\":[";for(int i=0;i<w;i++){if(i)cout<<',';cout<<initial.v[i];}
          cout<<"],\"shift\":"<<shift<<",\"period\":24}"<<endl;emitted[shift]++;
        }
      }
    }
  }
done:
  cout<<"{\"kind\":\"summary\",\"tested\":"<<tested<<",\"capped\":"<<capped<<",\"max_patch_width\":"<<maxwidth
      <<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-begin).count()<<",\"front_counts\":{";
  bool first=true;for(auto [s,c]:counts){if(!first)cout<<',';first=false;cout<<'\"'<<s<<"\":"<<c;}
  cout<<"},\"enumeration_complete\":"<<(timedout?"false":"true")<<",\"finite_seed_proved\":false}"<<endl;
}
