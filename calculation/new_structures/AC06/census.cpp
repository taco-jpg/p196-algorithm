// AC06: exact decimal pairword 120-step endpoint census, no strict-W9 pruning.
#include <bits/stdc++.h>
using namespace std;
using V=vector<unsigned char>;
constexpr int B[]={10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
constexpr int W[]={5,18,4,8,1,15,4,0,5};
const int UU[3][3]={{9,10,8},{10,8,9},{8,9,10}};
V make(int u,const V&c,int q,int k){
 V h;for(int x:B)h.push_back(x);
 for(int i=0;i<q;i++)for(int x:W)h.push_back(x);
 h.push_back(5);
 for(int i=0;i<k;i++)for(int x:UU[u])h.push_back(x);
 V p=h;p.insert(p.end(),c.begin(),c.end());p.insert(p.end(),h.rbegin(),h.rend());return p;
}
// Normalize pair coefficients with the actual left-to-right decimal carry.
// Reflect digits after gamma overflow, not before it.
void step(const V&in,V&out,int&gamma){
 int n=(int)in.size();if((int)out.size()<n+1)out.resize(n+1);
 int carry=0;
 for(int i=0;i<n;i++){int z=in[i]+carry;out[i]=z%10;carry=(z>=10);}
 gamma=carry;if(carry)out[n]=1;
 int m=n+carry;
 for(int i=0;i<m/2;i++){int z=out[i]+out[m-i-1];out[i]=out[m-i-1]=z;}
 if(m%2)out[m/2]*=2;out.resize(m);
}
int main(int argc,char**argv){
 if(argc<5){cerr<<"Uindex length count(0=all) q [k] [radius]\n";return 2;}
 int u=atoi(argv[1]),L=atoi(argv[2]),q=atoi(argv[4]);
 long long count=atoll(argv[3]);int k=argc>5?atoi(argv[5]):100;
 int radius=argc>6?atoi(argv[6]):122+L+30;
 if(u<0||u>=3||L<1||L>24||q<0||k<0)abort();
 int h=(L+1)/2;long long total=1;
 for(int i=0;i<h;i++)total*=((L%2&&i==h-1)?10:19);
 if(count<=0||count>total)count=total;
 V C(L),source=make(u,C,q,k),target=make(u,C,q,k+5);
 int pos=34+9*q+1+3*k;
 long long clockok=0,smallok=0,largeok=0,fullok=0;
 for(long long id=0;id<count;id++){
  long long z=id;
  for(int j=0;j<h;j++){
   int radix=(L%2&&j==h-1)?10:19;
   int x=z%radix;z/=radix;if(radix==10)x*=2;
   C[j]=C[L-j-1]=x;
  }
  for(int i=0;i<L;i++){
   source[pos+i]=C[i];source[source.size()-pos-i-1]=C[i];
   target[pos+15+i]=C[i];target[target.size()-pos-i-16]=C[i];
  }
  V cur=source,next;bool clk=true;int overflows=0;
  for(int t=0;t<120;t++){
   int g=0;step(cur,next,g);
   if(g!=(t%4==0))clk=false;
   overflows+=g;cur.swap(next);
  }
  bool eq=cur.size()==target.size();
  int mid=(int)target.size()/2,odd=(int)target.size()%2;
  bool small=eq,large=eq;
  if(eq){
   for(int i=max(0,mid-5);i<min((int)cur.size(),mid+5+odd);i++)
    if(cur[i]!=target[i])small=false;
   for(int i=max(0,mid-radius);i<min((int)cur.size(),mid+radius+odd);i++)
    if(cur[i]!=target[i])large=false;
  }
  clockok+=clk&&overflows==30;
  smallok+=small&&clk;
  largeok+=large&&clk;
  fullok+=eq&&cur==target&&clk;
 }
 cout<<"U="<<u<<" L="<<L<<" scanned="<<count<<" total="<<total
 <<" clock_ok="<<clockok<<" radius5_matches="<<smallok
 <<" large_window_matches="<<largeok<<" full_matches="<<fullok<<"\n";
}