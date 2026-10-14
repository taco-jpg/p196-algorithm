#include <array>
#include <vector>
#include <unordered_map>
#include <fstream>
#include <iostream>
#include <chrono>
#include <cstdint>
#include <csignal>
#include <sys/resource.h>
#include <sys/time.h>
using namespace std;
volatile sig_atomic_t stop_signal=0;
void stop_handler(int sig){stop_signal=sig;}
struct State{uint64_t f,z;bool operator==(const State&o)const{return f==o.f&&z==o.z;}};
// Only visited keys are quotiented. Node states and their recorded columns
// stay in the actual temporal orientation reached from a genuine root.
State canonical(State s){
  State best=s;
  constexpr uint64_t low11=2047ULL|(2047ULL<<12)|(2047ULL<<24);
  constexpr uint64_t first=1ULL|(1ULL<<12)|(1ULL<<24);
  for(int k=1;k<12;k++){
    s.f=((s.f>>1)&low11)|((s.f&first)<<11);
    s.z=(s.z>>4)|((s.z&15ULL)<<44);
    if(s.f<best.f||(s.f==best.f&&s.z<best.z))best=s;
  }
  return best;
}
struct Hash{size_t operator()(const State&s)const{uint64_t x=s.z^(s.f*0x9e3779b97f4a7c15ULL);x^=x>>30;x*=0xbf58476d1ce4e5b9ULL;x^=x>>27;return x^(x>>31);}};
struct Node{State s;uint64_t q,r;uint32_t parent,depth;};
struct Edge{State s;uint64_t q,r;};
vector<Edge> succ(const State&s){
  int a[12],b[12],c[12],z[12];
  for(int j=0;j<12;j++){a[j]=(s.f>>j)&1;b[j]=(s.f>>(12+j))&1;c[j]=(s.f>>(24+j))&1;z[j]=int((s.z>>(4*j))&15)-1;}
  vector<Edge> out;
  auto visit=[&](auto&& self,int j,int Q,int Q0,uint64_t nf,uint64_t nz,uint64_t qs,uint64_t rs)->void{
    if(stop_signal)return;
    if(j==12){if(Q==Q0)out.push_back({{nf,nz},qs,rs});return;}
    for(int nc=0;nc<2;nc++){
      if((Q+nc)/10!=c[j])continue;
      int R=(Q+a[j])%10+Q+nc-10*c[j];if(R<0||R>18)continue;
      for(int oc=0;oc<2;oc++){
        if((R<9&&oc!=0)||(R>9&&oc!=1)||(z[j]==-1&&oc!=1)||(z[j]==9&&oc!=0))continue;
        int nxt=(R+b[j])%10+z[j]+oc;if(nxt<0||nxt>18)continue;
        uint64_t f=nf|uint64_t((Q+a[j])/10)<<j|uint64_t((R+b[j])/10)<<(12+j)|uint64_t(nc)<<(24+j);
        self(self,j+1,nxt,Q0,f,nz|uint64_t(R-10*oc+1)<<(4*j),qs|uint64_t(Q)<<(5*j),rs|uint64_t(R)<<(5*j));
      }
    }
  };
  for(int q=0;q<19;q++)visit(visit,0,q,q,0,0,0,0);
  return out;
}
int main(int argc,char**argv){
  if(argc<2)return 2;double seconds=argc>2?stod(argv[2]):120;size_t cap=argc>3?stoull(argv[3]):3000000;
  uint64_t memory_mib=argc>4?stoull(argv[4]):3072;
  rlimit memory_limit={memory_mib*1024*1024,memory_mib*1024*1024};
  if(setrlimit(RLIMIT_AS,&memory_limit)!=0){cerr<<"Could not install memory limit"<<endl;return 4;}
  uint64_t rss_stop_kib=(memory_mib-32)*1024;
  signal(SIGALRM,stop_handler);signal(SIGINT,stop_handler);signal(SIGTERM,stop_handler);
  itimerval timer{};timer.it_value.tv_sec=int(seconds);timer.it_value.tv_usec=int((seconds-int(seconds))*1000000);
  setitimer(ITIMER_REAL,&timer,nullptr);
  ifstream input(argv[1]);int nt;input>>nt;vector<State> target(nt);unordered_map<State,int,Hash> targetmap;
  for(int i=0;i<nt;i++){input>>target[i].f>>target[i].z;targetmap.emplace(target[i],i);}
  vector<Node> nodes;unordered_map<State,uint32_t,Hash> ids;
  auto start=chrono::steady_clock::now();uint32_t depth=0;size_t cursor=0,edges=0;string status="unknown",reason="time budget";
  uint32_t found=UINT32_MAX;int targetid=-1;
  try{
  nodes.reserve(cap);ids.reserve(cap);
  for(int outer=8;outer<=9;outer++){
    State initial={uint64_t(4095)<<12|(outer==8?uint64_t(4095)<<24:0),0};
    uint64_t q0=0,r0=0;
    for(int j=0;j<12;j++){
      initial.z|=uint64_t(outer)<<(4*j);
      q0|=uint64_t(outer)<<(5*j);r0|=uint64_t(outer+9)<<(5*j);
    }
    ids.emplace(canonical(initial),uint32_t(nodes.size()));
    nodes.push_back({initial,q0,r0,UINT32_MAX,1});
  }
  for(cursor=0;cursor<nodes.size();cursor++){
    Node current=nodes[cursor];
    if(stop_signal){reason=stop_signal==SIGALRM?"wall-clock budget":"clean interrupt";break;}
    if(cursor%1024==0){
      if(chrono::duration<double>(chrono::steady_clock::now()-start).count()>seconds)break;
      rusage memory{};getrusage(RUSAGE_SELF,&memory);
      if(uint64_t(memory.ru_maxrss)>=rss_stop_kib){reason="RSS budget";break;}
    }
    if(current.depth!=depth){depth=current.depth;cout<<"{\"kind\":\"progress\",\"depth\":"<<depth<<",\"retained_states\":"<<nodes.size()<<",\"expanded\":"<<cursor<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"}"<<endl;}
    if(auto hit=targetmap.find(current.s);hit!=targetmap.end()){found=cursor;targetid=hit->second;goto finish;}
    auto out=succ(current.s);if(stop_signal){reason=stop_signal==SIGALRM?"wall-clock budget":"clean interrupt";break;}edges+=out.size();
    for(auto&e:out){
      State key=canonical(e.s);
      if(ids.find(key)!=ids.end())continue;
      if(nodes.size()>=cap){reason="state cap";goto finish;}
      uint32_t id=nodes.size();ids.emplace(key,id);nodes.push_back({e.s,e.q,e.r,uint32_t(cursor),current.depth+1});
      if(auto hit=targetmap.find(e.s);hit!=targetmap.end()){found=id;targetid=hit->second;goto finish;}
    }
  }
  if(cursor==nodes.size()){status="closed_reachable_graph_no_exterior";reason="";}
  }catch(const bad_alloc&){status="unknown";reason="allocation or virtual memory budget";}
finish:
  timer={};setitimer(ITIMER_REAL,&timer,nullptr);
  if(found!=UINT32_MAX){
    status="target_intersection_requires_suffix_replay";reason="";vector<uint32_t> path;
    for(uint32_t i=found;i!=UINT32_MAX;i=nodes[i].parent)path.push_back(i);
    cout<<"{\"kind\":\"candidate\",\"target_index\":"<<targetid<<",\"width\":"<<path.size()<<",\"rows\":[";
    for(int t=0;t<24;t++){
      if(t)cout<<',';cout<<'[';bool first=true;
      for(auto it=path.rbegin();it!=path.rend();++it){auto&n=nodes[*it];if(!first)cout<<',';first=false;cout<<(((t%2?n.r:n.q)>>(5*(t/2)))&31);}
      cout<<']';
    }
    cout<<"]}"<<endl;
  }
  rusage memory{};getrusage(RUSAGE_SELF,&memory);
  cout<<"{\"kind\":\"summary\",\"status\":\""<<status<<"\",\"reason\":\""<<reason<<"\",\"retained_states\":"<<nodes.size()<<",\"expanded_states\":"<<cursor<<",\"edges_before_state_deduplication\":"<<edges<<",\"last_depth\":"<<depth<<",\"state_cap\":"<<cap<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<",\"time_budget_seconds\":"<<seconds<<",\"virtual_memory_limit_bytes\":"<<memory_limit.rlim_cur<<",\"rss_stop_kib\":"<<rss_stop_kib<<",\"peak_rss_kib\":"<<memory.ru_maxrss<<",\"node_bytes\":"<<sizeof(Node)<<",\"quotient\":\"C12 temporal slot rotations\",\"roots\":[[8,17],[9,18]],\"finite_seed_proved\":false}"<<endl;
}
