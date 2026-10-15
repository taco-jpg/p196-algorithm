#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
struct State { uint32_t w; int x,y; };
struct Local { int s,x,y; };
vector<Local> ng[19][2][2];
void inverse_prefix(uint32_t id, int k, bool nongrowth_only, vector<uint32_t>& out){
 int p[9]; for(int i=k-1;i>=0;i--){p[i]=id%19;id/=19;}
 vector<State> a{{0,0,0}},b; a.reserve(128);b.reserve(128);
 for(int i=0;i<k;i++){
  b.clear();
  for(auto z:a)for(auto v:ng[p[i]][z.x][z.y]) if(i||v.s) b.push_back({z.w*19+v.s,v.x,v.y});
  a.swap(b);if(a.empty())break;
 }
 for(auto z:a)out.push_back(z.w);
 if(nongrowth_only||p[0]>10)return;
 int first=p[0]<=9?p[0]+9:9;
 a.clear();a.push_back({(uint32_t)first,first/10,1});
 for(int i=1;i<k;i++){
  b.clear();
  for(auto z:a)for(int yy=0;yy<2;yy++){
   int last=z.w%19;
   if((last+yy)/10!=z.y)continue;
   int d=p[i]-last-yy+10*z.y;
   if(d<0||d>9)continue;
   for(int xx=0;xx<2;xx++){
    int s=d+10*xx-z.x;
    if(s>=0&&s<=18)b.push_back({z.w*19+s,xx,yy});
   }
  }
  a.swap(b);if(a.empty())break;
 }
 for(auto z:a){int s=z.w%19;if(s/10==z.y||(s+1)/10==z.y)out.push_back(z.w);}
}
void make_initial(int k,int abc,vector<uint32_t>& v){
 uint32_t p=(abc/100)*19*19+(abc/10%10)*19+abc%10;
 v.push_back(p);
 for(int i=3;i<k;i++){
  vector<uint32_t> n;n.reserve(v.size()*10);
  for(auto z:v)for(int d=0;d<10;d++)n.push_back(z*19+d);
  v.swap(n);
 }
}
int main(int argc,char**argv){
 int k=argc>1?stoi(argv[1]):7;size_t cap=argc>2?stoul(argv[2]):100000;
 for(int p=0;p<19;p++)for(int x=0;x<2;x++)for(int y=0;y<2;y++)for(int s=0;s<19;s++)for(int yy=0;yy<2;yy++)
  if((s+yy)/10==y&&2*s+x+yy-10*((s+x)/10+y)==p)ng[p][x][y].push_back({s,(s+x)/10,yy});
 int abc;
 while(cin>>abc){
  vector<uint32_t> cur;make_initial(k,abc,cur);vector<size_t> counts;
  string status="DEPTH";int h;
  for(h=0;h<=100;h++){
   counts.push_back(cur.size());
   if(cur.empty()){status="FINITE";break;}
   if(cur.size()>cap){status="CAP";break;}
   vector<uint32_t> nxt;nxt.reserve(cur.size()*3);
   bool only=h==0&&(abc/10%10<abc/100);
   for(auto s:cur)inverse_prefix(s,k,only,nxt);
   sort(nxt.begin(),nxt.end());nxt.erase(unique(nxt.begin(),nxt.end()),nxt.end());
   if(nxt==cur){status="FIXED";break;}
   cur.swap(nxt);
  }
  cout<<"{\"prefix\":"<<abc<<",\"width\":"<<k<<",\"status\":\""<<status<<"\",\"depth\":"<<h<<",\"counts\":[";
  for(size_t i=0;i<counts.size();i++){if(i)cout<<",";cout<<counts[i];}cout<<"]}"<<endl;
 }
}
