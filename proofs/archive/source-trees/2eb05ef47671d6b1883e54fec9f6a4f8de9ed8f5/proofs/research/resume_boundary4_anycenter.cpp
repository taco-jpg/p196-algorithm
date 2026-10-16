// Exact reverse interior graph; eight two-step growth segments.
// Quotient only by rotations of TWO segments, preserving parity of the center.
#include <array>
#include <vector>
#include <unordered_map>
#include <cstdint>
#include <iostream>
#include <chrono>
#include <cstdlib>
#include <algorithm>
using U=uint64_t;
struct Opt{uint8_t a,b,l,r;};
std::array<std::vector<Opt>,1600> tab;
unsigned ix(unsigned l,unsigned r,unsigned a,unsigned b){return ((l*4+r)*10+a)*10+b;}
void half(unsigned pos,unsigned a,unsigned b,unsigned l,unsigned r,unsigned x,unsigned y,unsigned aa,unsigned bb){if(pos==2){tab[ix(l,r,aa,bb)].push_back({uint8_t(a),uint8_t(b),uint8_t(x),uint8_t(y)});return;}unsigned lo=(l>>pos)&1,ri=(r>>pos)&1,s=a+b;for(unsigned u=0;u<2;u++)if((s+u)/10==lo)half(pos+1,(s+u)%10,(s+ri)%10,l,r,x|(u<<pos),y|(((s+ri)/10)<<pos),aa,bb);}
void tables(){for(unsigned l=0;l<4;l++)for(unsigned r=0;r<4;r++)for(unsigned a=0;a<10;a++)for(unsigned b=0;b<10;b++)half(0,a,b,l,r,0,0,a,b);}
U canon(U x){U best=x;for(unsigned i=1;i<4;i++){x=(x>>16)|(x<<48);best=std::min(best,x);}return best;}
unsigned at(U s,unsigned j){return (s>>(8*j))&255;}
bool head(U s){for(unsigned j=0;j<8;j+=2){unsigned ev=at(s,j);if(((ev>>4)&3)!=(ev>>6))return false;unsigned od=at(s,j+1),x=od&15,rc=od>>6,cs=0;for(unsigned t=0;t<2;t++){unsigned z=2*x+((rc>>t)&1);x=z%10;cs|=(z/10)<<t;}if(cs!=((od>>4)&3)||x!=(at(s,(j+2)%8)&15))return false;}return true;}
struct Node{U state;uint32_t parent;};
std::vector<Node> nodes;std::unordered_map<U,uint32_t> seen;size_t current=0,edges=0,cap;bool found=false;U foundstate;
void visit(U state,unsigned k,unsigned al,unsigned first,U old){if(found)return;if(k==4){if(al!=first)return;edges++;U z=canon(old);auto[it,newly]=seen.emplace(z,nodes.size());if(newly){nodes.push_back({z,uint32_t(current)});if(head(z)){found=true;foundstate=z;}}return;}unsigned j=2*k,ev=at(state,j),od=at(state,j+1),desired=at(state,(j+2)%8)&15;for(unsigned ar=0;ar<10;ar++)for(auto a:tab[ix((ev>>4)&3,ev>>6,al,ar)])for(auto b:tab[ix((od>>4)&3,od>>6,od&15,a.b)]){if(b.b!=desired)continue;U pair=ar|(a.l<<4)|(a.r<<6)|(U(a.a|(b.l<<4)|(b.r<<6))<<8);visit(state,k+1,b.a,first,old|(pair<<(8*j)));}}
int main(int argc,char**argv){if(argc<4)return 2;double limit=atof(argv[1]);cap=atoll(argv[2]);tables();seen.reserve(std::min(cap,size_t(1000000)));for(int i=3;i<argc;i++){U s=canon(strtoull(argv[i],nullptr,10));if(seen.emplace(s,nodes.size()).second)nodes.push_back({s,UINT32_MAX});}auto start=std::chrono::steady_clock::now();size_t layerend=nodes.size(),depth=0;std::vector<size_t>layers;bool complete=true;
for(current=0;current<nodes.size();current++){if(current==layerend){layers.push_back(layerend);layerend=nodes.size();depth++;}if(current%256==0){double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();if(nodes.size()>cap||sec>limit){complete=false;break;}}U st=nodes[current].state;if(head(st)){found=true;foundstate=st;complete=false;break;}for(unsigned al=0;al<10;al++)visit(st,0,al,al,0);if(found){complete=false;break;}}
double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();std::cout<<"{\"states\":"<<nodes.size()<<",\"expanded\":"<<current<<",\"edges\":"<<edges<<",\"complete\":"<<(complete?"true":"false")<<",\"found\":"<<(found?"true":"false")<<",\"seconds\":"<<sec<<",\"depth\":"<<depth<<",\"layer_ends\":[";for(size_t i=0;i<layers.size();i++)std::cout<<(i?",":"")<<layers[i];std::cout<<"],\"head_to_bulk_quotient_states\":[";if(found){auto i=seen.at(foundstate);bool first=true;while(true){auto n=nodes[i];std::cout<<(first?"":",")<<n.state;first=false;if(n.parent==UINT32_MAX)break;i=n.parent;}}std::cout<<"]}"<<std::endl;}
