// AC07 physical (LSD-first) carry-preserving shrinking centre-window census.
// Each t consumes 1 low position and 1-gamma high position. No strict W9 filter.
// Must be paired with verify_ports.py (independent all-centre port proof).
#include <bits/stdc++.h>
using namespace std; using V=vector<unsigned char>;
const V B={10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
const V W={5,18,4,8,1,15,4,0,5};
const V U[3]={{9,12,6},{12,6,9},{6,9,12}};
void cat(V&a,const V&b){a.insert(a.end(),b.begin(),b.end());}
void pw(V&a,const V&b,int n){for(int i=0;i<n;i++)cat(a,b);}
V make(int q,int k,V J,V u,V c){
 V h=B;pw(h,W,q);cat(h,J);pw(h,u,k);V p=h;cat(p,c);reverse(h.begin(),h.end());cat(p,h);return p;
}
V nextpair(const V&p,int&g,int cut=-1,int*cin=nullptr){
 V d;d.reserve(p.size()+1);int c=0;
 for(int i=0;i<(int)p.size();i++){
  if(i==cut&&cin)*cin=c;int z=p[i]+c;d.push_back(z%10);c=z/10;
 }
 g=c;if(g)d.push_back(1);V out(d.size());
 for(int i=0;i<(int)d.size();i++)out[i]=d[i]+d[d.size()-1-i];
 return out;
}
V localnext(const V&p,int c,int g){
 V d(p.size());for(int i=0;i<(int)p.size();i++){int z=p[i]+c;d[i]=z%10;c=z/10;}
 int n=(int)p.size()+g-2;V a(n);
 for(int i=0;i<n;i++)a[i]=d[i+1]+d[n-i];
 return a;
}
V middle(V u,V c,int s){
 V h;pw(h,u,s);V x=h;cat(x,c);reverse(h.begin(),h.end());cat(x,h);return x;
}
struct Ports {int c[120],g[120];};
Ports ports(int ui,int len,int q=14,int k=100,int s=60){
 V C(len,0),p=make(q,k,{5},U[ui],C);Ports b{};
 int cut=34+9*q+1+3*(k-s);
 for(int t=0;t<120;t++){
  int ci=-1,g=0;V d=nextpair(p,g,cut+t,&ci);
  b.c[t]=ci;b.g[t]=g;p.swap(d);
 }
 return b;
}
uint64_t total(int len){uint64_t z=1;for(int i=0;i<len/2;i++)z*=19;if(len%2)z*=10;return z;}
V decode(int len,uint64_t code){
 V c(len);
 for(int i=0;i<len/2;i++){int z=code%19;code/=19;c[i]=c[len-1-i]=z;}
 if(len%2)c[len/2]=2*(code%10);
 return c;
}
int main(int argc,char**argv){
 if(argc<4){cerr<<"usage: ./centre_census UI(0..2) C_length start [end]\n";return 2;}
 int ui=stoi(argv[1]),len=stoi(argv[2]);uint64_t first=stoull(argv[3]);
 uint64_t end=argc>4?stoull(argv[4]):total(len);
 if(ui<0||ui>2||len<1||end>total(len)||first>end)return 2;
 Ports b=ports(ui,len);auto u=U[ui];uint64_t found=0;
 size_t minfirst=999999,maxfirst=0;
 for(uint64_t id=first;id<end;id++){
  V c=decode(len,id),p=middle(u,c,60);
  for(int t=0;t<120;t++)p=localnext(p,b.c[t],b.g[t]);
  V target=middle(u,c,25);
  if(p==target){found++;if(found<=5)cerr<<"CENTRE_FOUND "<<ui<<" "<<len<<" "<<id<<"\n";}
  else{size_t j=0;while(j<p.size()&&p[j]==target[j])j++;
   minfirst=min(minfirst,j);maxfirst=max(maxfirst,j);}
 }
 cout<<"CELL Uindex="<<ui<<" C_len="<<len<<" range=["<<first<<","<<end
     <<") denominator="<<total(len)<<" tested="<<end-first
     <<" found="<<found<<" minfirst="<<minfirst<<" maxfirst="<<maxfirst<<"\n";
}
