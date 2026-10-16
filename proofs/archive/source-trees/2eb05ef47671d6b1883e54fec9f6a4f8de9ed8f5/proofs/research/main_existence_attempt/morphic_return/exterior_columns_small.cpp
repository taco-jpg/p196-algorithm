#include <array>
#include <vector>
#include <unordered_map>
#include <fstream>
#include <iostream>
#include <chrono>
#include <cstdint>
using namespace std;
struct State{uint64_t f,z;bool operator==(const State&o)const{return f==o.f&&z==o.z;}};
struct Hash{size_t operator()(const State&s)const{uint64_t x=s.z^(s.f*0x9e3779b97f4a7c15ULL);x^=x>>30;x*=0xbf58476d1ce4e5b9ULL;x^=x>>27;return x^(x>>31);}};
struct Node{State s;uint64_t q,r;uint32_t parent,depth;};
struct Edge{State s;uint64_t q,r;};
vector<Edge> succ(const State&s){
  int a[12],b[12],c[12],z[12];
  for(int j=0;j<12;j++){a[j]=(s.f>>j)&1;b[j]=(s.f>>(12+j))&1;c[j]=(s.f>>(24+j))&1;z[j]=int((s.z>>(4*j))&15)-1;}
  vector<Edge> out;
  auto visit=[&](auto&& self,int j,int Q,int Q0,uint64_t nf,uint64_t nz,uint64_t qs,uint64_t rs)->void{
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
  ifstream input(argv[1]);int nt;input>>nt;vector<State> target(nt);unordered_map<State,int,Hash> targetmap;
  for(int i=0;i<nt;i++){input>>target[i].f>>target[i].z;targetmap.emplace(target[i],i);}
  State initial={uint64_t(4095)<<12|uint64_t(4095)<<24,0};uint64_t q0=0,r0=0;
  for(int j=0;j<12;j++){initial.z|=uint64_t(8)<<(4*j);q0|=uint64_t(8)<<(5*j);r0|=uint64_t(17)<<(5*j);}
  vector<Node> nodes;nodes.reserve(min(cap,size_t(3000000)));nodes.push_back({initial,q0,r0,UINT32_MAX,1});
  unordered_map<State,uint32_t,Hash> ids;ids.reserve(min(cap,size_t(3000000)));ids.emplace(initial,0);
  auto start=chrono::steady_clock::now();uint32_t depth=0;size_t cursor=0,edges=0;string status="unknown",reason="time budget";
  uint32_t found=UINT32_MAX;int targetid=-1;
  for(cursor=0;cursor<nodes.size();cursor++){
    Node current=nodes[cursor];
    if(cursor%1024==0&&chrono::duration<double>(chrono::steady_clock::now()-start).count()>seconds)break;
    if(current.depth!=depth){depth=current.depth;cout<<"{\"kind\":\"progress\",\"depth\":"<<depth<<",\"retained_states\":"<<nodes.size()<<",\"expanded\":"<<cursor<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"}"<<endl;}
    if(auto hit=targetmap.find(current.s);hit!=targetmap.end()){found=cursor;targetid=hit->second;goto finish;}
    auto out=succ(current.s);edges+=out.size();
    for(auto&e:out){
      if(ids.find(e.s)!=ids.end())continue;
      if(nodes.size()>=cap){reason="state cap";goto finish;}
      uint32_t id=nodes.size();ids.emplace(e.s,id);nodes.push_back({e.s,e.q,e.r,uint32_t(cursor),current.depth+1});
      if(auto hit=targetmap.find(e.s);hit!=targetmap.end()){found=id;targetid=hit->second;goto finish;}
    }
  }
  if(cursor==nodes.size()){status="closed_reachable_graph_no_exterior";reason="";}
finish:
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
  cout<<"{\"kind\":\"summary\",\"status\":\""<<status<<"\",\"reason\":\""<<reason<<"\",\"retained_states\":"<<nodes.size()<<",\"expanded_states\":"<<cursor<<",\"edges_before_state_deduplication\":"<<edges<<",\"last_depth\":"<<depth<<",\"state_cap\":"<<cap<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<",\"finite_seed_proved\":false}"<<endl;
}
