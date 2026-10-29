// Canonical seed insertion at half-width 8000, full coefficient-pair replay through step 20000.
#include <bits/stdc++.h>
using namespace std;using W=vector<uint8_t>;
int pre[]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
int cyc[]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
W seed(int h){W d(2*h);for(int i=0;i<h;i++){int p=i<39?pre[i]:cyc[(i-39)%20];d[i]=max(0,p-9);d[2*h-1-i]=p-d[i];}return d;}
int step(W&d){W out(d.size()+1);int n=d.size(),c=0;for(int i=0;i<n;i++){int v=d[i]+d[n-1-i]+c;out[i]=v%10;c=v/10;}if(c)out[n]=c;else out.resize(n);d.swap(out);return c;}
int main(int argc,char**argv){
 int h=argc>1?atoi(argv[1]):8000,T=argc>2?atoi(argv[2]):20000,m=argc>3?atoi(argv[3]):20;
 if(h<80||m<=0||m%20||T<0)return 2;
 W a=seed(h),b=seed(h+m);long long cells=0;int first=-1,gammaBad=-1,firstPal=-1,lastDigitLen=0;
 for(int t=0;t<=T;t++){
  int n=a.size();if(int(b.size())!=n+2*m&&first<0)first=t;
  for(int i=0;i<n/2;i++){
   int x=a[i]+a[n-1-i],j=i<39?i:i+m,y=b[j]+b[b.size()-1-j];cells++;
   if(x!=y&&first<0){first=t;cerr<<"FAILED t="<<t<<" i="<<i<<"\n";}
  }
  bool pal=true;for(int i=0;i<n/2;i++)if(a[i]!=a[n-1-i]){pal=false;break;}
  if(pal&&firstPal<0)firstPal=t;
  lastDigitLen=n;if(t<T){int g1=step(a),g2=step(b);if(g1!=g2&&gammaBad<0)gammaBad=t;}
 }
 cout<<"h="<<h<<" m="<<m<<" T="<<T<<" all_cells="<<cells<<" firstfail="<<first<<" badgamma="<<gammaBad<<" palindrome="<<firstPal<<" finalLen="<<lastDigitLen<<"\n";
 return first>=0||gammaBad>=0||firstPal>=0;
}
