// Exhaustive two-cell packet pumping: every source pair-word position is compared.
// g++ -O3 -std=c++17 pump_universe.cpp -o /tmp/n17u && /tmp/n17u 500 1500 20
#include <bits/stdc++.h>
using namespace std;using W=vector<uint8_t>;
int pre[]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
int cyc[]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
W seed(int h,int a,int b){W z(2*h);for(int i=0;i<h;i++){int p=i<39?pre[i]:cyc[(i-39)%20];if(i==h-2)p=a;if(i==h-1)p=b;z[i]=max(0,p-9);z[2*h-1-i]=p-z[i];}return z;}
int step(W &z){W y(z.size()+1);int n=z.size(),c=0;for(int i=0;i<n;i++){int s=z[i]+z[n-i-1]+c;y[i]=s%10;c=s/10;}if(c)y[n]=c;else y.resize(n);z.swap(y);return c;}
int main(int argc,char**argv){
 int h=argc>1?atoi(argv[1]):500,T=argc>2?atoi(argv[2]):1500,m=argc>3?atoi(argv[3]):20;
 if(h<80||m<=0||m%20||T<0)return 2;
 long long cells=0,steps=0;int first=-1,firstgamma=-1,firstpal=-1,minodd=9999;
 for(int a=0;a<19;a++)for(int b=0;b<19;b++){
  W x=seed(h,a,b),y=seed(h+m,a,b);
  for(int t=0;t<=T;t++){
   int len=x.size();
   if(int(y.size())!=len+2*m&&first<0)first=t;
   for(int i=0;i<len/2;i++){
    int p=x[i]+x[len-i-1],j=i<39?i:i+m,q=y[j]+y[y.size()-j-1];
    cells++;if(p!=q&&first<0){first=t;cerr<<"FIRST discrepancy t="<<t<<" a="<<a<<" b="<<b<<" site="<<i<<"\n";}
    if(p%2&&minodd>i)minodd=i;
   }
   bool pal=true;for(int i=0;i<len/2;i++)if(x[i]!=x[len-i-1]){pal=false;break;}
   if(pal&&firstpal<0)firstpal=t;steps++;
   if(t<T){int gx=step(x),gy=step(y);if(gx!=gy&&firstgamma<0)firstgamma=t;}
  }
 }
 cout<<"h="<<h<<" m="<<m<<" T="<<T<<" variants=361 paired_steps="<<steps<<" checked_cells="<<cells<<" firstfail="<<first<<" bad_gamma="<<firstgamma<<" bad_pal="<<firstpal<<" min_odd_site="<<minodd<<"\n";
 return first>=0||firstgamma>=0||firstpal>=0;
}
