#include <array>
#include <vector>
#include <unordered_map>
#include <fstream>
#include <iostream>
#include <cstdint>
#include <algorithm>
#include <chrono>
using namespace std;
using State=array<uint16_t,16>;
struct Hash {size_t operator()(State const&s)const {size_t h=1469598103934665603ULL;for(auto x:s){h^=x;h*=1099511628211ULL;}return h;}};
int tau[240][16];uint16_t minimal[65536];
vector<State> states;vector<int> rankv;vector<uint8_t> status;unordered_map<State,uint32_t,Hash> ids;
vector<pair<uint32_t,int>> trace;uint64_t cap=5000000;bool cycle=false,capped=false;chrono::steady_clock::time_point started;
int step(State const&s,int y,State&out){out.fill(0);for(int g=0;g<16;g++){unsigned aset=s[g];while(aset){int mask=__builtin_ctz(aset);aset&=aset-1;for(int bit=0;bit<2;bit++){int dst=tau[g*15+mask-1][y+8*bit];if(dst<0)return 0;out[dst/15]|=1u<<(dst%15+1);}}}for(auto &x:out)x=minimal[x];return 1;}
uint32_t index(State const&s){auto it=ids.find(s);if(it!=ids.end())return it->second;uint32_t k=states.size();ids.emplace(s,k);states.push_back(s);rankv.push_back(-1);status.push_back(0);return k;}
int dfs(uint32_t u){
 if(status[u]==2)return rankv[u];
 if(status[u]==1){cycle=true;cout<<"CYCLE at "<<u<<" trace length "<<trace.size()<<"\n";for(auto [v,y]:trace)cout<<v<<":"<<y+1<<" ";cout<<"\n";return -1;}
 if(states.size()>cap){capped=true;return -1;}
 status[u]=1;int r=0;State s=states[u];
 for(int y=0;y<8;y++){State out;if(!step(s,y,out))continue;uint32_t v=index(out);trace.emplace_back(u,y);int rr=dfs(v);trace.pop_back();if(cycle||capped)return -1;r=max(r,rr+1);}
 status[u]=2;rankv[u]=r;
 if(u%100000==0){double secs=chrono::duration<double>(chrono::steady_clock::now()-started).count();cout<<"progress "<<states.size()<<" finished "<<u<<" rank "<<r<<" seconds "<<secs<<endl;}
 return r;
}
int main(int argc,char**argv){
 if(argc<2)return 1;if(argc>2)cap=stoull(argv[2]);ifstream f(argv[1]);for(auto&row:tau)for(int &x:row)f>>x;
 for(unsigned aset=0;aset<65536;aset++){unsigned out=aset&~1u;for(int m=1;m<16;m++)if(out&(1u<<m)){for(int z=1;z<16;z++)if(z!=m&&(aset&(1u<<z))&&((z&m)==z)){out&=~(1u<<m);break;}}minimal[aset]=out;}
 started=chrono::steady_clock::now();int maxr=0;
 for(int g=0;g<16;g++){State s{};s[g]=1u<<15;int r=dfs(index(s));cout<<"root "<<g<<" rank "<<r<<" states "<<states.size()<<endl;if(cycle||capped)break;maxr=max(maxr,r);}
 cout<<"RESULT states "<<states.size()<<" maxrank "<<maxr<<" cycle "<<cycle<<" capped "<<capped<<endl;
 if(!cycle&&!capped){ofstream o(string(argv[1])+".certificate",ios::binary);uint32_t n=states.size();o.write((char*)&n,4);for(size_t i=0;i<states.size();i++){o.write((char*)states[i].data(),32);o.write((char*)&rankv[i],4);}}
}
