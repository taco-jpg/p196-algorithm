// Exact 192-bit position automaton, compact open-addressed visited set.
// Exhaustion with all scanned edges to new vertices proves the graph acyclic.
// Non-tree edges are reported as UNKNOWN_REPEAT unless SCC checked separately.
// Copyright (c) project contributors; reproducer for agent-15 F2.
#include <bits/stdc++.h>
using namespace std;using u64=uint64_t;
struct Key{u64 w[3]={0,0,0};bool operator==(const Key&o)const{return w[0]==o.w[0]&&w[1]==o.w[1]&&w[2]==o.w[2];}};
struct KH{size_t operator()(const Key& k)const{return (size_t)((k.w[0]*0x9E3779B97F4A7C15ULL)^(k.w[1]*0xC2B2AE3D27D4EB4FULL)^(k.w[2]*0x165667B19E3779F9ULL)^(k.w[0]>>29));}};
inline void put(Key&k,int pos,int nb,u64 v){for(int i=0;i<nb;i++)if((v>>i)&1)k.w[(pos+i)>>6]|=1ULL<<((pos+i)&63);}
inline u64 get(const Key&k,int pos,int nb){u64 v=0;for(int i=0;i<nb;i++)v|=((k.w[(pos+i)>>6]>>((pos+i)&63))&1ULL)<<i;return v;}
int b,p,ydig,ng;vector<int>g,gi,yi;
Key pack(u64 L,u64 H,int*Y){Key k;put(k,0,p,L);put(k,p,p,H);int sh=2*p;for(int i=0;i<ng;i++){put(k,sh,ydig,(u64)Y[i]);sh+=ydig;}return k;}
void unpack(const Key&k,u64&L,u64&H,int*Y){L=get(k,0,p);H=get(k,p,p);int sh=2*p;for(int i=0;i<ng;i++){Y[i]=get(k,sh,ydig);sh+=ydig;}}
template<class F>void transition(u64 L,u64 H,int*Y,bool first,F emit){struct Fr{int t,x,ch;};Fr st[64];int xs[64],hn[64];
 for(int x0=(first?1:0);x0<=2*b-2;x0++){int d=0;st[0]={0,x0,0};while(d>=0){auto &f=st[d];if(f.ch>=2){--d;continue;}int c=f.ch++,t=f.t,x=f.x;
  if((x+c)/b!=(int)((H>>t)&1))continue;int nx=(x+((L>>t)&1))%b+(g[t]?Y[yi[t]]:(x+c)%b);xs[t]=x;hn[t]=c;
  if(t+1<p){st[++d]={t+1,nx,0};}else if(nx==x0){u64 L2=0,H2=0;int Y2[64];for(int tt=0;tt<p;tt++){L2|=(u64)((xs[tt]+((L>>tt)&1))/b)<<tt;H2|=(u64)hn[tt]<<tt;}
    for(int i=0;i<ng;i++)Y2[i]=(xs[gi[i]]+hn[gi[i]])%b;emit(pack(L2,H2,Y2));}
 }}
}
struct Visited{
 vector<Key> keys; vector<uint32_t> parent;vector<uint16_t> lev;vector<int32_t>tab;size_t mask;
 Visited(uint64_t cap){uint64_t sz=1;while(sz<cap*1.6)sz*=2;tab.assign(sz,-1);mask=sz-1;keys.reserve(cap);parent.reserve(cap);lev.reserve(cap);}
 int find(const Key&k)const{size_t h=KH{}(k)&mask;while(tab[h]>=0){int j=tab[h];if(keys[j]==k)return j;h=(h+1)&mask;}return -1;}
 void insert(const Key&k,int par,int l){size_t h=KH{}(k)&mask;while(tab[h]>=0)h=(h+1)&mask;int j=keys.size();keys.push_back(k);parent.push_back(par);lev.push_back(l);tab[h]=j;}
};
int main(int argc,char**argv){if(argc<4){cerr<<"usage: compact <base> <cap> <streamfile> [status-every]\n";return 2;}
 b=atoi(argv[1]);uint64_t cap=strtoull(argv[2],nullptr,10);int every=argc>4?atoi(argv[4]):0;ifstream f(argv[3]);if(!f){cerr<<"bad input file\n";return 3;}
 ydig=1;while((1<<ydig)<b)ydig++;string s;int done=0;cout<<"# F2 compact b="<<b<<" cap="<<cap<<" input="<<argv[3]<<"\n";
 while(getline(f,s)){if(s.empty()||s[0]=='#')continue;p=s.size();ng=0;g.clear();gi.clear();yi.resize(p);u64 Hs=0;for(int t=0;t<p;t++){int x=s[t]-'0';if(x<0||x>1)throw runtime_error("bad stream");g.push_back(x);yi[t]=x?ng++:-1;if(x){gi.push_back(t);Hs|=1ULL<<t;}}if(2*p+ydig*ng>192)throw runtime_error("key length exceeds 192");int Y0[64];for(int i=0;i<ng;i++)Y0[i]=1;
 Key root=pack(0,Hs,Y0);auto t0=chrono::steady_clock::now();Visited v(cap);v.insert(root,UINT32_MAX,0);uint64_t E=0,repeats=0,scan=0;int firstrep=-1;bool capped=false;uint16_t maxlev=0;
 for(uint64_t i=0;i<v.keys.size();i++){u64 L,H;int Y[64];unpack(v.keys[i],L,H,Y);bool first=i==0;
  transition(L,H,Y,first,[&](Key k){int j=v.find(k);if(j>=0){E++;repeats++;if(firstrep<0)firstrep=i;}
    else {if(v.keys.size()>=cap){capped=true;return;}E++;v.insert(k,i,v.lev[i]+1);maxlev=max(maxlev,v.lev.back());}});
  scan=i+1;if(every&&scan%every==0){cerr<<"PROGRESS b="<<b<<" g="<<s<<" scanned="<<scan<<" nodes="<<v.keys.size()<<" edges="<<E<<" repeats="<<repeats<<" secs="<<chrono::duration<double>(chrono::steady_clock::now()-t0).count()<<"\n";}
  if(capped)break;
 }
 auto seconds=chrono::duration<double>(chrono::steady_clock::now()-t0).count();
 cout<<(capped?"CAPPED":(repeats==0?"DECIDED_ACYCLIC":"EXHAUSTED_REPEAT"))<<" b="<<b<<" p="<<p<<" g="<<s<<" states="<<v.keys.size()<<" edges="<<E<<" repeated="<<repeats<<" scanned="<<scan<<" maxlev="<<maxlev<<" seconds="<<seconds<<"\n";cout.flush();done++;
 }
 cout<<"# COMPLETE done="<<done<<"\n";cout.flush();
}
