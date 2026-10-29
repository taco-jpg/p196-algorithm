// X04: commuting zero and p8/m20 lattice insertions in genuine decimal RAA.
// Reproduce: g++ -O3 -std=c++17 hybrid.cpp -o hybrid
//            ./hybrid calculation/new_structures/agent-N16/rows.txt 300 14000 20000
#include <bits/stdc++.h>
using namespace std;
using D = vector<uint8_t>;
vector<string>B(8),W(8);
int cv(char c){return c<='9'?c-'0':c-'A'+10;}
D seed(int q,int z){
 D half,p;for(char c:B[0])half.push_back(cv(c));
 for(int k=0;k<q;k++)for(char c:W[0])half.push_back(cv(c));
 p=half;p.insert(p.end(),z,0);for(auto i=half.rbegin();i!=half.rend();i++)p.push_back(*i);
 int n=p.size();D d(n);
 for(int i=0;i<n/2;i++){d[i]=max(0,(int)p[i]-9);d[n-1-i]=min(9,(int)p[i]);}
 if(n%2){assert(p[n/2]%2==0);d[n/2]=p[n/2]/2;}return d;
}
D step(const D&d){int n=d.size(),carry=0;D v(n+1);for(int i=0;i<n;i++){
 int s=d[i]+d[n-1-i]+carry;v[i]=s%10;carry=s/10;
}if(carry)v[n]=carry;else v.pop_back();return v;}
D pairs(const D&d){D p(d.size());for(int i=0;i<(int)d.size();i++)p[i]=d[i]+d[d.size()-1-i];return p;}
D insW(const D&p,int t){D out;out.reserve(p.size()+40);
 out.insert(out.end(),p.begin(),p.begin()+39);
 for(char c:W[t%8])out.push_back(cv(c));
 out.insert(out.end(),p.begin()+39,p.end()-39);
 for(auto i=W[t%8].rbegin();i!=W[t%8].rend();i++)out.push_back(cv(*i));
 out.insert(out.end(),p.end()-39,p.end());return out;
}
D insZero(D p){p.insert(p.begin()+p.size()/2,0);return p;}
int zeroWidth(const D&p){int n=p.size(),i=n/2-1;if(n%2&&p[n/2]!=0)return 0;
 int cnt=0;while(i>=0&&p[i]==0)cnt++,i--;return 2*cnt+(n%2);}
bool isPal(const D&d){for(int i=0;i<(int)d.size()/2;i++)if(d[i]!=d[d.size()-1-i])return false;return true;}
uint64_t hashv=1469598103934665603ULL;
void hashadd(uint64_t x){hashv^=x;hashv*=1099511628211ULL;}
int main(int argc,char**argv){string file=argc>1?argv[1]:"calculation/new_structures/agent-N16/rows.txt";
 int q=argc>2?atoi(argv[2]):300,z=argc>3?atoi(argv[3]):14000,T=argc>4?atoi(argv[4]):20000;
 if(q<1||z<4||T<0)return 2;ifstream f(file);if(!f)return 2;
 string hdr;getline(f,hdr);for(int j=0;j<8;j++)getline(f,B[j]);for(int j=0;j<8;j++)getline(f,W[j]);
 for(int j=0;j<8;j++)if(B[j].size()!=39||W[j].size()!=20)return 3;
 D d[4]={seed(q,z),seed(q+1,z),seed(q,z+1),seed(q+1,z+1)};
 int minpre=INT_MAX,minzero=INT_MAX,growth=0,prior=z;
 cout<<"t,n,prefix,zero,fp\n";
 for(int t=0;t<=T;t++){
  D p[4];for(int j=0;j<4;j++)p[j]=pairs(d[j]);
  if(insW(p[0],t)!=p[1]||insZero(p[0])!=p[2]||insW(p[2],t)!=p[3]||
     insZero(p[1])!=p[3]||insW(insZero(p[0]),t)!=insZero(insW(p[0],t))){cerr<<"PUMP_FAIL "<<t<<"\n";return 4;}
  int L=d[0].size(),pre=0;
  for(int i=0;i<L/2;i++){int expected=i<39?cv(B[t%8][i]):cv(W[t%8][(i-39)%20]);
    if(p[0][i]!=expected)break;pre++;}
  if(pre<39){cerr<<"ROOT_FAIL "<<t<<"\n";return 5;}
  for(int j=0;j<4;j++)if(isPal(d[j])){cerr<<"PAL "<<t<<" seed="<<j<<"\n";return 6;}
  int zero=zeroWidth(p[0]);minpre=min(minpre,pre);minzero=min(minzero,zero);
  if(zero>prior)growth++;prior=zero;
  hashadd(t);hashadd(L);hashadd(pre);hashadd(zero);for(int j=0;j<16;j++)hashadd(p[0][j]);
  if(t%880==0||t==T)cout<<t<<','<<L<<','<<pre<<','<<zero<<','<<hex<<hashv<<dec<<'\n';
  if(t==T)break;
  for(int j=0;j<4;j++){D nx=step(d[j]);if((int)nx.size()-(int)d[j].size()!=(t%2==0)){
    cerr<<"GAMMA_FAIL "<<t<<" seed="<<j<<"\n";return 7;}
    d[j].swap(nx);}
 }
 cerr<<"HYBRID_PASS steps="<<T<<" q="<<q<<" z="<<z<<" min_prefix="<<minpre
     <<" min_zero="<<minzero<<" growth_steps="<<growth<<" fnv="<<hex<<hashv<<dec<<"\n";
}
