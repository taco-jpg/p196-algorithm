// Exhaustive finite-center return-map cycles, not a decimal existence proof.
#include <array>
#include <vector>
#include <iostream>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <algorithm>
using W=std::vector<int>;
W bulk_step(W q,bool h){int n=q.size();W a(n),b(n),lo(n),hi(n),out(n);int j=0;while(q[j]==9)j++;a[j]=b[j]=q[j]>=10;for(int k=1;k<n;k++){int i=(j+k)%n;a[i]=(q[i]+a[(i+n-1)%n])/10;}for(int k=1;k<n;k++){int i=(j-k+n)%n;b[i]=(q[i]+b[(i+1)%n])/10;}for(int i=0;i<n;i++){lo[i]=(q[i]+a[(i+n-1)%n])%10;hi[i]=(q[i]+b[(i+1)%n])%10;}for(int i=0;i<n;i++)out[i]=lo[i]+hi[(i+n-int(h))%n];return out;}
std::array<W,16> bulks;std::array<int,16> incoming;
void phases(int rot){W b={3,10,15,8};std::rotate(b.begin(),b.begin()+rot,b.end());int origin=0;for(int t=0;t<16;t++){bulks[t]=b;incoming[t]=b[(origin+3)%4]>=10;b=bulk_step(b,t%2);origin+=t%2;}}
W coreof(uint32_t x,int pairs,bool odd){W a(pairs),out;int middle=0;if(odd){middle=2*(x%10);x/=10;}for(int i=0;i<pairs;i++){a[i]=x%19;x/=19;}out=a;if(odd)out.push_back(middle);for(int i=pairs-1;i>=0;i--)out.push_back(a[i]);return out;}
int64_t step(uint32_t code,int pairs,bool odd){W core=coreof(code,pairs,odd);constexpr int nbuf=24;int len=2*nbuf+core.size();std::array<int,128> q,d,out;for(int i=0;i<nbuf;i++)q[i]=bulks[0][i%4];for(int i=0;i<int(core.size());i++)q[nbuf+i]=core[i];for(int i=0;i<nbuf;i++)q[nbuf+core.size()+i]=bulks[0][3-i%4];for(int t=0;t<16;t++){int c=incoming[t];for(int i=0;i<len;i++){int s=q[i]+c;d[i]=s%10;c=s/10;}int h=t%2;if(h){for(int i=1;i<len;i++)out[i-1]=d[i]+d[len-i];len--;}else{for(int i=0;i<len;i++)out[i]=d[i]+d[len-1-i];}q=out;}
 constexpr int remain=20;for(int i=0;i<remain;i++)if(q[i]!=bulks[0][i%4]||q[len-1-i]!=bulks[0][i%4])return -1;
 uint32_t result=0;for(int i=pairs-1;i>=0;i--)result=result*19+q[remain+i];if(odd){int center=q[remain+pairs];if(center%2)return-1;result=result*10+center/2;}return result;}
int main(int argc,char**argv){int pairs=argc>1?atoi(argv[1]):3;int rot=argc>2?atoi(argv[2]):0;bool odd=argc>3?atoi(argv[3]):false;if(pairs<0||pairs>5||rot<0||rot>3)return 2;phases(rot);if(argc>4){std::cout<<step(strtoul(argv[4],nullptr,10),pairs,odd)<<std::endl;return 0;}uint32_t count=odd?10:1;for(int i=0;i<pairs;i++)count*=19;std::vector<int32_t> next(count,-1);uint32_t edges=0;auto start=std::chrono::steady_clock::now();for(uint32_t x=0;x<count;x++){next[x]=step(x,pairs,odd);if(next[x]>=0)edges++;}
 std::vector<uint8_t> color(count,0);std::vector<std::vector<uint32_t>> cycles;for(uint32_t x=0;x<count;x++){if(color[x])continue;int64_t y=x;std::vector<uint32_t> path;while(y>=0&&!color[y]){color[y]=1;path.push_back(y);y=next[y];}if(y>=0&&color[y]==1){std::vector<uint32_t> cyc;auto it=std::find(path.begin(),path.end(),uint32_t(y));for(;it!=path.end();it++)cyc.push_back(*it);cycles.push_back(cyc);}for(auto z:path)color[z]=2;}
 double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();std::cout<<"{\"pairs\":"<<pairs<<",\"rotation\":"<<rot<<",\"odd\":"<<(odd?"true":"false")<<",\"states\":"<<count<<",\"internal_edges\":"<<edges<<",\"seconds\":"<<sec<<",\"edge_list\":[";bool firstedge=true;for(uint32_t x=0;x<count;x++)if(next[x]>=0){std::cout<<(firstedge?"":",")<<"["<<x<<","<<next[x]<<"]";firstedge=false;}std::cout<<"],\"cycles\":[";for(size_t k=0;k<cycles.size();k++){std::cout<<(k?",":"")<<"[";for(size_t j=0;j<cycles[k].size();j++)std::cout<<(j?",":"")<<cycles[k][j];std::cout<<"]";}std::cout<<"]}"<<std::endl;}
