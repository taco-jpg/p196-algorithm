// Agent-X26 odd-length base-10 reference: exact all-padding 9-pump checker.
#include <bits/stdc++.h>
using namespace std;using W=vector<uint8_t>;
W seed(int L,int k){string s="5"+string(2*L+k,'9')+"4";W d;for(auto i=s.rbegin();i!=s.rend();++i)d.push_back(*i-'0');return d;}
W pairs(const W&d){W p(d.size());for(int i=0,n=d.size();i<n;i++)p[i]=d[i]+d[n-i-1];return p;}
W raa(const W&d){W n;int c=0;for(int i=0,m=d.size();i<m;i++){int x=d[i]+d[m-1-i]+c;n.push_back(x%10);c=x/10;}if(c)n.push_back(c);return n;}
W step(const W&p){W d;int c=0;for(int x:p){int z=x+c;d.push_back(z%10);c=z/10;}if(c)d.push_back(c);return pairs(d);}
W ins(W w,int x){w.insert(w.begin()+w.size()/2,2,(uint8_t)x);return w;}
int main(int argc,char**argv){if(argc!=4)return 2;int L=atoi(argv[1]),T=atoi(argv[2]),k=atoi(argv[3]);if(k%2!=1||L<=T+2)return 3;W a=seed(L,k),b=seed(L+1,k);int minroom=INT_MAX;for(int t=0;t<=T;t++){
 W p=pairs(a),q=pairs(b);if(q!=ins(p,18)){cerr<<"PAIR INSERT FAIL t="<<t<<"\n";return 4;}
 if(b!=ins(a,9)){cerr<<"DIGIT INSERT FAIL t="<<t<<"\n";return 5;}
 int j=p.size()/2,b0=2*L+k;for(int i=j-2;i<=b0;i++)if(p[i]!=18){cerr<<"BAND FAIL t="<<t<<" i="<<i<<"\n";return 6;}
 minroom=min(minroom,b0-j);
 if(t%5000==0||t==T)cout<<"t="<<t<<" digits="<<a.size()<<" padded="<<b.size()<<" minroom="<<minroom<<"\n";
 if(t<T){W p1=step(p),q1=step(q),a1=raa(a),b1=raa(b);if(q1!=ins(p1,18)||pairs(a1)!=p1||pairs(b1)!=q1){cerr<<"COMMUTE FAIL t="<<t<<"\n";return 7;}if(a1.size()+2!=b1.size()){cerr<<"OVERFLOW MISMATCH "<<t<<"\n";return 8;}a.swap(a1);b.swap(b1);}
}cout<<"PASS: all "<<T+1<<" digit/pair insertions, "<<T<<" exact commute edges; arbitrary extra symmetric 9^2 copies by induction\n";}
