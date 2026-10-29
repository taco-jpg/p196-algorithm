// Exact check of two synchronized bulk insertions for k and k+q, through T steps.
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <cstdlib>
#include <climits>
using namespace std;
constexpr int X[6]={8,16,14,10,2,4},Y[6]={16,14,10,2,4,8};
struct Band{int start=-1,len=-1;};
vector<unsigned char> seed(int k){string s="9"+string(k,'8')+"59"+string(k,'9')+"80"+string(k,'7')+"20"+string(k,'0')+"1";vector<unsigned char>d;for(auto it=s.rbegin();it!=s.rend();++it)d.push_back(*it-'0');return d;}
vector<int> folded(const vector<unsigned char>&d){int n=d.size();vector<int>p((n+1)/2);for(int i=0;i<(n+1)/2;i++)p[i]=d[i]+d[n-1-i];return p;}
vector<unsigned char> step(const vector<unsigned char>&d){int n=d.size(),c=0;vector<unsigned char>q(n+1);for(int i=0;i<n;i++){int s=d[i]+d[n-1-i]+c;q[i]=s%10;c=s/10;}if(c)q[n]=c;else q.pop_back();return q;}
Band longest(const vector<int>&p,int val){Band ans;for(int i=0;i<(int)p.size();){int j=i+1;while(j<(int)p.size()&&p[j]==p[i])j++;if(p[i]==val&&j-i>ans.len)ans={i,j-i};i=j;}return ans;}
int main(int argc,char**argv){int k=argc>1?atoi(argv[1]):15000,T=argc>2?atoi(argv[2]):20000,q=argc>3?atoi(argv[3]):1;auto d=seed(k),e=seed(k+q);int minodd=INT_MAX,maxgap=-1;for(int t=0;t<=T;t++){
 auto a=folded(d),b=folded(e);Band ax=longest(a,X[t%6]),ay=longest(a,Y[t%6]),bx=longest(b,X[t%6]),by=longest(b,Y[t%6]);
 if((int)b.size()!=(int)a.size()+2*q||bx.start!=ax.start||bx.len!=ax.len+q||by.start!=ay.start+q||by.len!=ay.len+q){cerr<<"BLOCK_DELTA_FAIL t="<<t<<" ax="<<ax.start<<","<<ax.len<<" bx="<<bx.start<<","<<bx.len<<" ay="<<ay.start<<","<<ay.len<<" by="<<by.start<<","<<by.len<<"\n";return 2;}
 b.erase(b.begin()+by.start+by.len-q,b.begin()+by.start+by.len);b.erase(b.begin()+bx.start+bx.len-q,b.begin()+bx.start+bx.len);
 if(a!=b){int where=0;while(where<(int)a.size()&&a[where]==b[where])where++;cerr<<"PAIRWORD_DIFF t="<<t<<" first="<<where<<"\n";return 3;}
 int odd=0;for(int v:a)odd+=(v%2);minodd=min(minodd,odd);maxgap=max(maxgap,ay.start-ax.start-ax.len);
 if(t==0||t==1||t==10||t==100||t==1000||t==5000||t==10000||t==15000||t==T)cout<<"PUMP step="<<t<<" h="<<a.size()<<" left="<<ax.len<<" right="<<ay.len<<" odd="<<odd<<" junction="<<(ay.start-ax.start-ax.len)<<"\n";
 if(t<T){d=step(d);e=step(e);}
 }
 cout<<"PUMP_ALL_STEPS_PASS k="<<k<<" T="<<T<<" q="<<q<<" min_odd="<<minodd<<" max_gap="<<maxgap<<"\n";
}
