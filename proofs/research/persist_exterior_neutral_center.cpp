// Exact center-side graph for repetitions of the new 11-step exterior clock.
// Full 128-bit keys; quotient by cyclic rotation of whole four-segment blocks.
#include <array>
#include <vector>
#include <unordered_map>
#include <cstdint>
#include <iostream>
#include <chrono>
#include <cstdlib>
#include <algorithm>
using U=__uint128_t;
struct Hash{size_t operator()(U v)const{uint64_t a=v,b=v>>64; a^=b+0x9e3779b97f4a7c15ull+(a<<6)+(a>>2);a^=a>>30;a*=0xbf58476d1ce4e5b9ull;a^=a>>27;a*=0x94d049bb133111ebull;return a^(a>>31);}};
struct Opt{uint8_t a,b,l,r;};
std::array<std::vector<std::vector<Opt>>,6> tab;
std::array<unsigned,12> ps,off;
unsigned Q,reps,total;
unsigned ix(unsigned p,unsigned l,unsigned r,unsigned a,unsigned b){return ((l*(1u<<p)+r)*10+a)*10+b;}
void half(unsigned p,unsigned pos,unsigned a,unsigned b,unsigned l,unsigned r,unsigned x,unsigned y,unsigned aa,unsigned bb){if(pos==p){tab[p][ix(p,l,r,aa,bb)].push_back({uint8_t(a),uint8_t(b),uint8_t(x),uint8_t(y)});return;}unsigned lo=(l>>pos)&1,ri=(r>>pos)&1,s=a+b;for(unsigned u=0;u<2;u++)if((s+u)/10==lo)half(p,pos+1,(s+u)%10,(s+ri)%10,l,r,x|(u<<pos),y|(((s+ri)/10)<<pos),aa,bb);}
void tables(){for(unsigned p=1;p<=5;p++){tab[p].resize((1u<<(2*p))*100);for(unsigned l=0;l<(1u<<p);l++)for(unsigned r=0;r<(1u<<p);r++)for(unsigned a=0;a<10;a++)for(unsigned b=0;b<10;b++)half(p,0,a,b,l,r,0,0,a,b);}}
U canon(U x){U best=x;U m=(U(1)<<38)-1;for(unsigned i=1;i<reps;i++){x=(x>>38)|((x&m)<<(total-38));best=std::min(best,x);}return best;}
unsigned digit(U s,unsigned j){return (s>>off[j])&15;}
unsigned lc(U s,unsigned j){return (s>>(off[j]+4))&((1u<<ps[j])-1);}
unsigned rc(U s,unsigned j){return (s>>(off[j]+4+ps[j]))&((1u<<ps[j])-1);}
U col(unsigned d,unsigned l,unsigned r,unsigned j){return U(d|(l<<4)|(r<<(4+ps[j])))<<off[j];}
bool head(U s){for(unsigned j=0;j<Q;j+=2){if(lc(s,j)!=rc(s,j))return false;unsigned x=digit(s,j+1),r=rc(s,j+1),out=0;for(unsigned t=0;t<ps[j+1];t++){unsigned z=2*x+((r>>t)&1);x=z%10;out|=(z/10)<<t;}if(out!=lc(s,j+1)||x!=digit(s,(j+2)%Q))return false;}return true;}
struct Node{U state;uint32_t parent;};
std::vector<Node> nodes;std::unordered_map<U,uint32_t,Hash> seen;size_t current=0,edges=0,cap;bool found=false;U foundstate;
void visit(U state,unsigned k,unsigned al,unsigned first,U old){if(found)return;if(k==Q/2){if(al!=first)return;edges++;U z=canon(old);auto[it,newly]=seen.emplace(z,nodes.size());if(newly){nodes.push_back({z,uint32_t(current)});if(head(z)){found=true;foundstate=z;}}return;}unsigned j=2*k,desired=digit(state,(j+2)%Q);for(unsigned ar=0;ar<10;ar++)for(auto a:tab[ps[j]][ix(ps[j],lc(state,j),rc(state,j),al,ar)])for(auto b:tab[ps[j+1]][ix(ps[j+1],lc(state,j+1),rc(state,j+1),digit(state,j+1),a.b)]){if(b.b!=desired)continue;visit(state,k+1,b.a,first,old|col(ar,a.l,a.r,j)|col(a.a,b.l,b.r,j+1));}}
std::string dec(U n){if(!n)return"0";std::string s;while(n){s+=char('0'+n%10);n/=10;}std::reverse(s.begin(),s.end());return s;}
int main(int argc,char**argv){if(argc<5)return 2;reps=atoi(argv[1]);unsigned rot=atoi(argv[2]);double limit=atof(argv[3]);cap=atoll(argv[4]);if(reps<1||reps>3||rot>3)return 2;Q=4*reps;unsigned p0[4]={1,1,4,5},d0[4]={9,0,9,9},l0[4]={1,0,3,3},r0[4]={0,1,12,28};total=0;U root=0;for(unsigned j=0;j<Q;j++){unsigned v=(j+rot)%4;ps[j]=p0[v];off[j]=total;total+=4+2*ps[j];root|=col(j%2?d0[v]:9-d0[v],l0[v],r0[v],j);}tables();seen.reserve(std::min(cap,size_t(1000000)));seen.emplace(root,0);nodes.push_back({root,UINT32_MAX});auto start=std::chrono::steady_clock::now();size_t layerend=1,depth=0;std::vector<size_t>layers;bool complete=true;
for(current=0;current<nodes.size();current++){if(current==layerend){layers.push_back(layerend);layerend=nodes.size();depth++;}if(current%256==0){double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();if(nodes.size()>cap||sec>limit){complete=false;break;}}U st=nodes[current].state;if(head(st)){found=true;foundstate=st;complete=false;break;}for(unsigned al=0;al<10;al++)visit(st,0,al,al,0);if(found){complete=false;break;}}
double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();std::cout<<"{\"repeats\":"<<reps<<",\"rotation\":"<<rot<<",\"states\":"<<nodes.size()<<",\"expanded\":"<<current<<",\"edges\":"<<edges<<",\"complete\":"<<(complete?"true":"false")<<",\"found\":"<<(found?"true":"false")<<",\"seconds\":"<<sec<<",\"depth\":"<<depth<<",\"layer_ends\":[";for(size_t i=0;i<layers.size();i++)std::cout<<(i?",":"")<<layers[i];std::cout<<"],\"head_to_bulk_quotient_states\":[";if(found){auto i=seen.at(foundstate);bool first=true;while(true){auto n=nodes[i];std::cout<<(first?"":",")<<char(34)<<dec(n.state)<<char(34);first=false;if(n.parent==UINT32_MAX)break;i=n.parent;}}std::cout<<"]}"<<std::endl;}
