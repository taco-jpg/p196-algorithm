// Exact forward spatial graph, quotiented by cyclic rotation of eight equal
// two-step segments. The exterior and each supplied bulk SCC are invariant
// under this symmetry. Full uint64 comparisons, not probabilistic hashes.
#include <array>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <cstdint>
#include <iostream>
#include <chrono>
#include <cstdlib>
#include <algorithm>
#include <fstream>
#include <string>
using U=uint64_t;
struct Opt{uint8_t a,b,l,r;};
std::array<std::vector<Opt>,1600> tab;
unsigned ix(unsigned l,unsigned r,unsigned a,unsigned b){return ((l*4+r)*10+a)*10+b;}
void half(unsigned pos,unsigned a,unsigned b,unsigned l,unsigned r,unsigned x,unsigned y,unsigned aa,unsigned bb){
 if(pos==2){tab[ix(l,r,aa,bb)].push_back({uint8_t(a),uint8_t(b),uint8_t(x),uint8_t(y)});return;}
 unsigned lo=(l>>pos)&1,ri=(r>>pos)&1,s=a+b;
 for(unsigned u=0;u<2;u++)if((s+u)/10==lo)
 half(pos+1,(s+u)%10,(s+ri)%10,l,r,x|(u<<pos),y|(((s+ri)/10)<<pos),aa,bb);
}
void tables(){for(unsigned l=0;l<4;l++)for(unsigned r=0;r<4;r++)for(unsigned a=0;a<10;a++)for(unsigned b=0;b<10;b++)half(0,a,b,l,r,0,0,a,b);}
U rotate(U x){return (x>>8)|(x<<56);}
std::pair<U,unsigned> canon(U x){U best=x;unsigned sh=0;for(unsigned i=1;i<8;i++){x=rotate(x);if(x<best){best=x;sh=i;}}return{best,sh};}
struct Node{U state;uint32_t parent;uint8_t a,b,rotation;};
std::vector<Node> nodes;std::unordered_map<U,uint32_t> seen;std::unordered_set<U> targets;
size_t current=0,edges=0,cap;bool found=false;U foundstate;
void visit(U state,unsigned j,unsigned dr,unsigned first,U ds,U cs){
 if(found)return;
 if(j==8){if(dr!=first)return;edges++; // Left segment outputs shift by one.
  U x=0;for(unsigned k=0;k<8;k++)x|=((ds>>(((k+7)%8)*8))&15)<<(k*8);
  x|=cs;auto [z,rot]=canon(x);auto [it,newly]=seen.emplace(z,nodes.size());
  if(newly){nodes.push_back({z,uint32_t(current),uint8_t(state&15),uint8_t(first),uint8_t(rot)});if(targets.count(z)){found=true;foundstate=z;}}
  return;
 }
 unsigned byte=(state>>(j*8))&255,a=byte&15,l=(byte>>4)&3,r=(byte>>6)&3;
 for(auto o:tab[ix(l,r,a,dr)])visit(state,j+1,o.b,first,ds|(U(o.a)<<(j*8)),cs|(U((o.l<<4)|(o.r<<6))<<(j*8)));
}
int main(int argc,char**argv){if(argc<4)return 2;double limit=atof(argv[1]);cap=atoll(argv[2]);for(int k=3;k<argc;k++){std::string a=argv[k];if(a.rfind("file:",0)==0){std::ifstream f(a.substr(5),std::ios::binary);U x;while(f.read(reinterpret_cast<char*>(&x),sizeof(U)))targets.insert(canon(x).first);}else targets.insert(canon(strtoull(argv[k],nullptr,10)).first);}tables();U root=0x2121212121212121ull;seen.reserve(std::min(cap,size_t(1000000)));seen.emplace(root,0);nodes.push_back({root,UINT32_MAX,0,0,0});auto start=std::chrono::steady_clock::now();size_t layerend=1,depth=0;std::vector<size_t>layers;bool complete=true;
 for(current=0;current<nodes.size();current++){
 if(current==layerend){layers.push_back(layerend);layerend=nodes.size();depth++;}
 if(current%256==0){double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();if(nodes.size()>cap||sec>limit){complete=false;break;}}
 U st=nodes[current].state;for(unsigned dr=0;dr<10;dr++)visit(st,0,dr,dr,0,0);
 if(found){complete=false;break;}}
 double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();std::cout<<"{\"states\":"<<nodes.size()<<",\"expanded\":"<<current<<",\"edges\":"<<edges<<",\"complete\":"<<(complete?"true":"false")<<",\"found\":"<<(found?"true":"false")<<",\"seconds\":"<<sec<<",\"found_state\":"<<foundstate<<",\"target_count\":"<<targets.size()<<",\"depth\":"<<depth<<",\"layer_ends\":[";for(size_t i=0;i<layers.size();i++)std::cout<<(i?",":"")<<layers[i];std::cout<<"],\"reverse_quotient_path\":[";
 if(found){auto i=seen.at(foundstate);bool first=true;while(nodes[i].parent!=UINT32_MAX){auto n=nodes[i];std::cout<<(first?"":",")<<"["<<unsigned(n.a)<<","<<unsigned(n.b)<<","<<unsigned(n.rotation)<<"]";first=false;i=n.parent;}}
 std::cout<<"]}"<<std::endl;
}
