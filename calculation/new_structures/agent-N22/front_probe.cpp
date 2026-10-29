#include <bits/stdc++.h>
using namespace std;using R=vector<int>;
vector<R> load(string p){ifstream f(p);string s;vector<R>x;while(getline(f,s)){stringstream is(s);string a;R r;while(getline(is,a,','))r.push_back(stoi(a));x.push_back(r);}return x;}
R step(const R&x){R d;int c=0;for(int v:x){int y=v+c;c=(y>=10);d.push_back(y-10*c);}if(c)d.push_back(c);R p(d.size());for(size_t j=0;j<d.size();j++)p[j]=d[j]+d[d.size()-1-j];return p;}
int main(int argc,char**argv){if(argc<7){cerr<<"usage: front_probe rows.csv B.csv tailComma odd q maxSteps\n";return 1;}
auto W=load(argv[1]),B=load(argv[2]);R tail;string a;stringstream ss(argv[3]);while(getline(ss,a,','))tail.push_back(stoi(a));int odd=stoi(argv[4]),q=stoi(argv[5]),T=stoi(argv[6]);R h=B[0];for(int j=0;j<q;j++)h.insert(h.end(),W[0].begin(),W[0].end());h.insert(h.end(),tail.begin(),tail.end());R p=h;for(int j=(int)h.size()-1-odd;j>=0;j--)p.push_back(h[j]);int x0=11+q*48,firstB=-1,firstClock=-1,minF=INT_MAX,maxF=INT_MIN;int n0=p.size();for(int t=0;t<=T;t++){
int n=p.size(),k=(n+1)/2;bool b=true;for(int j=0;j<11;j++)if(p[j]!=B[t%8][j])b=false;if(!b&&firstB<0)firstB=t;
int j=11;while(j<k&&p[j]==W[t%8][(j-11)%48])j++;int f=j-x0;minF=min(minF,f);maxF=max(maxF,f);if(t%8==0)cout<<"t="<<t<<" front="<<f<<" B="<<b<<" len="<<n<<" centreHalf="<<k-j<<"\n";
if(t==T)break;
 auto y=step(p);if(firstClock<0&&((int)y.size()-n)!=((t%2)==0?1:0))firstClock=t;p=move(y);
}
cerr<<"SUMMARY initialLen="<<n0<<" finalLen="<<p.size()<<" firstB="<<firstB<<" firstClock="<<firstClock<<" minF="<<minF<<" maxF="<<maxF<<"\n";
}
