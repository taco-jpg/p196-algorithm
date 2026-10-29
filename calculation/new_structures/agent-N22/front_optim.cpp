#include <bits/stdc++.h>
using namespace std;using Row=vector<uint8_t>;
static vector<Row> W,B;
vector<Row> csv(const string&p){ifstream f(p);string s;vector<Row>a;while(getline(f,s)){stringstream ss(s);string z;Row r;while(getline(ss,z,','))r.push_back(stoi(z));a.push_back(r);}return a;}
static Row nxt(const Row&p){int c=0;Row d;d.reserve(p.size()+1);for(int v:p){int s=v+c;c=(s>=10);d.push_back(s-10*c);}if(c)d.push_back(c);Row r(d.size());for(int i=0;i<(int)d.size();i++)r[i]=d[i]+d[d.size()-1-i];return r;}
struct C{Row tail;int odd,score,minf,endf;};
static int ntrials=0,T=96;
C assess(Row tail,int odd){
 if(odd&&!tail.empty())tail.back() &= ~1; // centre coefficient even
 Row h=B[0];for(int j=0;j<2;j++)h.insert(h.end(),W[0].begin(),W[0].end());h.insert(h.end(),tail.begin(),tail.end());Row p=h;
 for(int i=(int)h.size()-1-odd;i>=0;i--)p.push_back(h[i]);
 int x0=11+96;int mini=INT_MAX,score=INT_MAX,endf=0;
 for(int t=0;t<=T;t++){
  if(p.size()<15)return {tail,odd,-100000,0,0};
  for(int j=0;j<11;j++)if(p[j]!=B[t%8][j])return {tail,odd,-100000,0,0};
  int hlen=(int)((p.size()+1)/2),j=11;while(j<hlen&&p[j]==W[t%8][(j-11)%48])j++;
  int diff=j-x0;mini=min(mini,diff);
  if(t && t%8==0)score=min(score,diff);
  if(t==T)endf=diff;
  if(t==T)break;
  int n=(int)p.size();p=nxt(p);if((int)p.size()-n != ((t%2)==0?1:0))return {tail,odd,-100000,0,0};
 }
 return {tail,odd,score,mini,endf};
}
string repr(Row v){string o;for(int x:v){if(o.size())o+=',';o+=to_string(x);}return o;}
int main(int argc,char**argv){(void)argc;W=csv(argv[1]);B=csv(argv[2]);int N=atoi(argv[3]);T=atoi(argv[4]);mt19937 gen(372221);vector<C> elite;C best{{},0,-100000,0,0};
 auto measure=[&](Row tail,int odd){C c=assess(tail,odd);if(c.score>best.score ||(c.score==best.score&&c.endf>best.endf)){best=c;cerr<<"BEST n="<<ntrials<<" T="<<T<<" min8="<<best.score<<" end="<<best.endf<<" minall="<<best.minf<<" len="<<best.tail.size()<<" odd="<<best.odd<<" ["<<repr(best.tail)<<"]\n";}if(c.score>=best.score-10){elite.push_back(c);if(elite.size()>200){sort(elite.begin(),elite.end(),[](const C&a,const C&b){return pair(a.score,a.endf)>pair(b.score,b.endf);});elite.resize(64);}}ntrials++;};
 measure({10,14,1,10},1);measure({10,3,0,5,17,16,10,10,18,11,3,10,10,14,15,1,17,2,10},0);
 measure({13,4,0,3,10,16,14,3,5,11,3,11,9,9,1,15,10,6,10,4,2,18,18,1,18,16,13,14,10,12,2,10,4,6,18,16,16,0,11,8,7,11,12,10,1,12,16,0,3,18,18,10},0);
 for(int it=0;it<N;it++){
  Row tail;int odd=gen()%2;
  if(!elite.empty()&&gen()%5!=0){sort(elite.begin(),elite.end(),[](const C&a,const C&b){return pair(a.score,a.endf)>pair(b.score,b.endf);});const C &c=elite[gen()%min<int>(32,elite.size())];tail=c.tail;odd=c.odd;int k=1+gen()%4;
   while(k--){int op=gen()%6;if(op==0&&tail.size()<80)tail.insert(tail.begin()+gen()%(tail.size()+1),gen()%19);
    else if(op==1&&!tail.empty())tail.erase(tail.begin()+gen()%tail.size());else if(op<=4&&!tail.empty())tail[gen()%tail.size()]=gen()%19;else odd^=1;}
  }else {int l=1+gen()%35;for(int j=0;j<l;j++)tail.push_back(gen()%19);}
  measure(move(tail),odd);
 }
 cout<<"RESULT "<<ntrials<<" T="<<T<<" min8="<<best.score<<" end="<<best.endf<<" minall="<<best.minf<<" len="<<best.tail.size()<<" odd="<<best.odd<<" ["<<repr(best.tail)<<"]\n";
}
