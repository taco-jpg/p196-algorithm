// Exact backward spatial graph for six growth segments and an 18-step period.
// This decides only the fixed-interface, uniform 3/6-core ansatz, not Lychrel
// existence. A completed queue with absent exterior is an arbitrary-width
// exclusion within that ansatz. No empirical iteration bound is substituted.
// Each state is packed injectively into 24 + 18 + 18 = 60 bits.
#include <array>
#include <vector>
#include <unordered_map>
#include <cstdint>
#include <iostream>
#include <chrono>
#include <cstdlib>
#include <algorithm>
using U=uint64_t;
struct Opt { uint8_t dl,dr,lc,rc; };
struct State { std::array<unsigned,6> d,l,r; };
std::array<unsigned,6> ps={5,2,2,3,2,4};
std::array<std::vector<std::vector<Opt>>,6> tab;
unsigned index(unsigned p,unsigned l,unsigned r,unsigned out,unsigned dr){return (((l*(1u<<p)+r)*10+out)*10+dr);}
void half(unsigned j,unsigned pos,unsigned dl,unsigned dr,unsigned l,unsigned r,unsigned x,unsigned y,unsigned origdl,unsigned origdr){
 if(pos==ps[j]) { tab[j][index(ps[j],l,r,dl,origdr)].push_back({uint8_t(origdl),uint8_t(dr),uint8_t(x),uint8_t(y)}); return; }
 unsigned a=(l>>pos)&1,b=(r>>pos)&1,s=dl+dr;
 for(unsigned u=0;u<2;u++)if((s+u)/10==b)
 half(j,pos+1,(s+a)%10,(s+u)%10,l,r,x|(((s+a)/10)<<pos),y|(u<<pos),origdl,origdr);
}
void tables(){ for(unsigned j=0;j<6;j++){unsigned p=ps[j]; tab[j].resize((1u<<(2*p))*100);for(unsigned l=0;l<(1u<<p);l++)for(unsigned r=0;r<(1u<<p);r++)for(unsigned dl=0;dl<10;dl++)for(unsigned dr=0;dr<10;dr++)half(j,0,dl,dr,l,r,0,0,dl,dr);}}
U pack(State const&s){ U v=0;unsigned k=0;for(unsigned j=0;j<6;j++){v|=U(s.d[j])<<k;k+=4;v|=U(s.l[j])<<k;k+=ps[j];v|=U(s.r[j])<<k;k+=ps[j];}return v;}
State unpack(U v){State s;unsigned k=0;for(unsigned j=0;j<6;j++){s.d[j]=(v>>k)&15;k+=4;s.l[j]=(v>>k)&((1u<<ps[j])-1);k+=ps[j];s.r[j]=(v>>k)&((1u<<ps[j])-1);k+=ps[j];}return s;}
U exterior(){State s;for(unsigned j=0;j<6;j++){s.d[j]=1;s.l[j]=1u<<(ps[j]-1);s.r[j]=0;}return pack(s);}
U target(unsigned d){State s;for(unsigned j=0;j<6;j++){s.d[j]=d;unsigned c=0;for(unsigned i=0;i<ps[j];i++){unsigned h=d>=5;c|=h<<i;d=2*d-9*h;}s.l[j]=s.r[j]=c;}return pack(s);}
struct Node{U state; uint32_t parent;uint8_t dl,dr;};
std::vector<Node> nodes;
std::unordered_map<U,uint32_t> seen;
size_t edges=0,current=0;bool found=false;U goal;size_t cap;
void visit(State const&s,unsigned j,unsigned dr,unsigned rfirst,State&prev){
 if(found)return;
 if(j==6){if(dr!=rfirst)return;edges++;U z=pack(prev);auto [it,newly]=seen.emplace(z,nodes.size());if(newly){nodes.push_back({z,uint32_t(current),uint8_t(prev.d[0]),uint8_t(rfirst)});if(z==goal)found=true;}return;}
 unsigned desired=s.d[(j+1)%6]; auto const&opts=tab[j][index(ps[j],s.l[j],s.r[j],desired,dr)];
 for(auto const&o:opts){prev.d[j]=o.dl;prev.l[j]=o.lc;prev.r[j]=o.rc;visit(s,j+1,o.dr,rfirst,prev);}
}
int main(int argc,char**argv){if(argc>4 && argc!=10){std::cerr<<"Expected digit seconds states [six periods]\n";return 2;}unsigned digit=argc>1?atoi(argv[1]):3;double limit=argc>2?atof(argv[2]):60;cap=argc>3?atoll(argv[3]):5000000;if(argc>4){for(unsigned j=0;j<6;j++)ps[j]=atoi(argv[j+4]);}unsigned total=0;for(auto p:ps){if(p<1||p>5){std::cerr<<"Periods must lie in 1..5\n";return 2;}total+=p;}if(total!=18 || (digit!=3&&digit!=6)){std::cerr<<"Expected total period 18 and bulk digit 3 or 6\n";return 2;}tables();goal=exterior();U root=target(digit);seen.reserve(std::min(cap,size_t(1000000)));seen.emplace(root,0);nodes.push_back({root,UINT32_MAX,0,0});auto start=std::chrono::steady_clock::now();size_t layer_end=1,depth=0;bool complete=true;std::vector<size_t> layers;
 for(current=0;current<nodes.size();current++){if(current==layer_end){layers.push_back(layer_end);layer_end=nodes.size();depth++;}if(current%1024==0){double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();if(nodes.size()>cap||sec>limit){complete=false;break;}}State s=unpack(nodes[current].state), prev;for(unsigned dr=0;dr<10;dr++)visit(s,0,dr,dr,prev);if(found){complete=false;break;}}
 double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();std::cout<<"{\"digit\":"<<digit<<",\"states\":"<<nodes.size()<<",\"expanded\":"<<current<<",\"edges\":"<<edges<<",\"complete\":"<<(complete?"true":"false")<<",\"found\":"<<(found?"true":"false")<<",\"seconds\":"<<elapsed<<",\"depth\":"<<depth<<",\"periods\":[";for(unsigned j=0;j<6;j++)std::cout<<(j?",":"")<<ps[j];std::cout<<"],\"layer_ends\":[";for(size_t j=0;j<layers.size();j++)std::cout<<(j?",":"")<<layers[j];std::cout<<"],\"path\":[";if(found){auto i=seen.at(goal);bool first=true;while(nodes[i].parent!=UINT32_MAX){auto n=nodes[i];std::cout<<(first?"":",")<<"["<<unsigned(n.dl)<<","<<unsigned(n.dr)<<"]";i=n.parent;first=false;}}std::cout<<"]}"<<std::endl;}
