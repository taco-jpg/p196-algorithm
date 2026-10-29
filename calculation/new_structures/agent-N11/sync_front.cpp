// Constructive delayed phase-lock shadow between N_L and N_big.
// Exact literal decimal digit-vector replay, multi-scale prefix front + overflow.
#include <bits/stdc++.h>
using namespace std;
static vector<uint8_t> make(int L){uint32_t x=196;int m=L+130;vector<uint8_t>d(2*m);for(int i=0;i<m;i++){int p;if(i==64||i==L+65)p=11;else if(i>=65&&i<65+L)p=9;else{x^=x<<13;x^=x>>17;x^=x<<5;p=x%19;}if(i==0)p=12;d[i]=max(0,p-9);d[2*m-1-i]=min(9,p);}return d;}
static int advance(vector<uint8_t>&d,vector<uint8_t>&out){int n=d.size(),c=0;out.resize(n+1);for(int i=0;i<n;i++){int v=d[i]+d[n-1-i]+c;out[i]=v%10;c=v/10;}out[n]=c;d.swap(out);d.resize(n+(c!=0));return c;}
int main(int argc,char**argv){int L1=argc>1?atoi(argv[1]):2000,L2=argc>2?atoi(argv[2]):45000,T=argc>3?atoi(argv[3]):15000;vector<uint8_t>a=make(L1),b=make(L2),o1,o2;vector<int>ks={1,2,4,8,16,32,64,128,256,512,1024};vector<int>first(ks.size(),-1);int firstG=-1,g1=0,g2=0;
for(int t=0;t<=T;t++){
 if(g1!=g2&&firstG<0)firstG=t;
 int minidx=ks.back()+1;
 int m=int(min(a.size(),b.size())/2);
 for(int i=0;i<min(m,ks.back());i++)if(a[i]+a[a.size()-1-i]!=b[i]+b[b.size()-1-i]){minidx=i;break;}
 for(size_t j=0;j<ks.size();j++)if(first[j]<0&&minidx<ks[j])first[j]=t;
 if(t==T)break;
 g1=advance(a,o1);g2=advance(b,o2);
}
cout<<"L="<<L1<<" comparator="<<L2<<" checked="<<T<<" first_gamma="<<firstG<<"\n";
for(size_t j=0;j<ks.size();j++)cout<<"K="<<ks[j]<<" first_diff="<<first[j]<<"\n";
}
