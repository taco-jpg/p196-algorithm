// Independent decimal digit-vector reverse-and-add; no big integers or pairword transition machinery.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>
using namespace std;
using Row = vector<int>;
vector<Row> read_csv(const string& s){ifstream f(s);if(!f)throw runtime_error("missing "+s);vector<Row>a;string line;while(getline(f,line)){istringstream is(line);string z;Row r;while(getline(is,z,','))r.push_back(stoi(z));a.push_back(r);}return a;}
vector<uint8_t> seed(const Row& B,const Row& W,int q,const Row& tail,bool odd){
 Row h=B;for(int k=0;k<q;k++)h.insert(h.end(),W.begin(),W.end());h.insert(h.end(),tail.begin(),tail.end());
 if(odd && h.back()%2)throw runtime_error("odd length requires even centre coefficient");
 Row P=h;for(int i=(int)h.size()-1-(odd?1:0);i>=0;i--)P.push_back(h[i]);
 vector<uint8_t>d(P.size(),0);int n=P.size();
 for(int i=0;i<n/2;i++){
   int high=min(9,P[i]),low=P[i]-high;
   if(high<0||low<0||low>9)throw runtime_error("illegal pair coefficient");
   d[i]=low;d[n-1-i]=high;
 }
 if(n%2)d[n/2]=P[n/2]/2;
 assert(d.back()!=0);
 return d;
}
void step(vector<uint8_t>& d){
 int n=d.size(),c=0;vector<uint8_t>y; y.reserve(n+1);
 for(int i=0;i<n;i++){
   int sum=int(d[i])+int(d[n-1-i])+c;
   y.push_back(sum%10);c=sum/10;
 }
 if(c)y.push_back(c);
 d.swap(y);
}
string decimal(const vector<uint8_t>&d){string s;s.reserve(d.size());for(int i=(int)d.size()-1;i>=0;i--)s+=char('0'+d[i]);return s;}
int main(int argc,char**argv){
  if(argc<6){cerr<<"usage: outward_digits rows.csv B.csv tail.csv steps output_prefix [q=100]\n";return 2;}
  auto W=read_csv(argv[1]),B=read_csv(argv[2]),Tail=read_csv(argv[3]);int T=stoi(argv[4]),q=argc>=7?stoi(argv[6]):100;
  if(Tail.size()!=1 || Tail[0].size()!=80)throw runtime_error("expected 80-coefficient tail");
  bool diagnose=argc>=8 && string(argv[7])=="--until-break";
  if(W.size()!=8||B.size()!=8)throw runtime_error("8 phases required");
  vector<uint8_t>d=seed(B[0],W[0],q,Tail[0],false);
  ofstream log(string(argv[5])+"_stats.csv"),cp(string(argv[5])+"_checkpoints.txt");
  log<<"t,length,matched_band,front_index\n";int minmatch=1000000000,maxloss=0;int init_band=q*48;
  vector<int> checkpoints={0,1,2,3,7,8,16,64,128,136,176,184,256,1000,5000,10000,15000,19999,20000};
  for(int t=0;t<=T;t++){
    int n=d.size(),half=(n+1)/2;
    if(n<2||d.back()==0){cerr<<"BAD length/leading at "<<t<<"\n";return 1;}
    bool pal=true;for(int i=0;i<n/2;i++)if(d[i]!=d[n-1-i]){pal=false;break;}
    if(pal){cerr<<"PALINDROME "<<t<<"\n";return diagnose?0:1;}
    auto&b=B[t%8];auto&w=W[t%8];
    for(int i=0;i<11;i++)if(d[i]+d[n-1-i]!=b[i]){cerr<<(diagnose?"B_BREAK":"BAD B")<<" phase="<<t%8<<" t="<<t<<" index="<<i<<"\n";return diagnose?0:1;}
    int match=0;while(11+match<half&&d[11+match]+d[n-12-match]==w[match%48])match++;
    minmatch=min(minmatch,match);maxloss=max(maxloss,init_band-match);
    if(t>=8 && t<=128 && t%8==0 && match<q*48+2){cerr<<"NO POSITIVE FRONT at t="<<t<<" matched="<<match<<"\n";return 1;}
    if(t==128 && match!=q*48+7){cerr<<"NO FRONT +7 at 128, got="<<match-q*48<<"\n";return 1;}
    if(t==184 && match!=q*48-1){cerr<<"NO FRONT -1 at 184, got="<<match-q*48<<"\n";return 1;}
    if(!diagnose && match<128){cerr<<"BAND below 128 at t="<<t<<" matched="<<match<<"\n";return 1;}
    if(t<=24 || (t%8==0 && t<=256) || t%80==0 || t==T)log<<t<<','<<n<<','<<match<<','<<11+match<<'\n';
    if(find(checkpoints.begin(),checkpoints.end(),t)!=checkpoints.end()) cp<<t<<' '<<decimal(d)<<'\n';
    if(t==T)break;
    int len=n;step(d);
    if(int(d.size())-len!=(t%2==0?1:0)){cerr<<(diagnose?"OVERFLOW_BREAK":"BAD overflow")<<" t="<<t<<"\n";return diagnose?0:1;}
  }
  cerr<<"PASS: steps="<<T<<" q="<<q<<" final_digits="<<d.size()<<" min_band="<<minmatch<<" max_loss="<<maxloss<<" nonpal, 8-phase B/W, overflow all checked\n";
}
