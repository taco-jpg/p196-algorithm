#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <map>
#include <string>
#include <vector>
using namespace std;
using V=vector<int>;
static const V B={10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
static const V W={5,18,4,8,1,15,4,0,5};
static const V U={10,8,9};
void append(V&a,const V&b){a.insert(a.end(),b.begin(),b.end());}
V mirror(V a){reverse(a.begin(),a.end());return a;}
V repeat(const V&w,int n){V x;x.reserve(w.size()*n);for(int i=0;i<n;i++)append(x,w);return x;}
V realize(const V&p){
  V d(p.size());
  for(size_t i=0;i<p.size()/2;i++){
    int hi=min(9,p[i]),lo=p[i]-hi; d[i]=lo;d[p.size()-1-i]=hi;
  }
  if(p.size()%2){if(p[p.size()/2]%2)throw runtime_error("odd midpoint");d[p.size()/2]=p[p.size()/2]/2;}
  return d;
}
V step(const V&d,int&gamma){
  V n(d.size());int c=0;
  for(size_t i=0;i<d.size();i++){
    int s=d[i]+d[d.size()-1-i]+c;n[i]=s%10;c=s/10;
  }
  gamma=0;if(c){n.push_back(c);gamma=1;}return n;
}
int alt(const V&x){int a=0;for(size_t i=0;i<x.size();i++)a+=(i%2?-1:1)*x[i];return a;}
V digits_for_j(int z,int len){V a(len);for(int i=0;i<len;i++){a[i]=z%19;z/=19;}return a;}
int main(int argc,char**argv){
  int q=argc>1?atoi(argv[1]):20,k=argc>2?atoi(argv[2]):20;
  V prefix=B;append(prefix,repeat(W,q));size_t cut=prefix.size();
  map<int,long long> hist;long long total=0,passes=0,clockfail=0,near=0;
  for(int len:{3,4}){
    int lim=1;for(int i=0;i<len;i++)lim*=19;
    for(int z=0;z<lim;z++){
      V J=digits_for_j(z,len);if(alt(J)%11!=0)continue;total++;
      V h=B;append(h,repeat(W,q));append(h,J);append(h,repeat(U,k));
      V C={0,0,0};V p=h;append(p,C);append(p,mirror(h));V d=realize(p);
      bool clock=true;
      for(int t=0;t<120;t++){
        int g;V next=step(d,g);if(g!=((t%4)==0))clock=false;d.swap(next);
      }
      if(!clock)clockfail++;
      int first=-1;
      for(size_t i=0;i<cut;i++){
        if(d[i]+d[d.size()-1-i]!=prefix[i]){first=(int)i;break;}
      }
      if(first<0)passes++;
      else {hist[first-(int)cut]++;if(first>=int(cut)-40)near++;}
    }
  }
  cout<<"q="<<q<<" k="<<k<<" U=(10,8,9) C=(0,0,0) odd-centre mod11-gated J count="<<total<<"\n";
  cout<<"strict W9 prefix passes="<<passes<<" clock_fail="<<clockfail
      <<" near_cut_mismatch_count="<<near<<"\n";
  cout<<"first mismatch offset from cut histogram:\n";
  for(auto [d,c]:hist)cout<<d<<":"<<c<<" ";
  cout<<"\n";
}
