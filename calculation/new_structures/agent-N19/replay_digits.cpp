// Independent decimal reverse-and-add using least-significant-first digit vectors.
#include <vector>
#include <string>
#include <iostream>
#include <algorithm>
#include <cstdint>
#include <cstdlib>
using namespace std;
static uint64_t fnv(const vector<unsigned char>&v){
 uint64_t h=14695981039346656037ULL;
 for(auto i=v.rbegin();i!=v.rend();++i){h^=uint64_t(*i+'0');h*=1099511628211ULL;}
 return h;
}
int main(int argc,char**argv){
 int L=argc>1?atoi(argv[1]):22000,T=argc>2?atoi(argv[2]):20000;
 vector<unsigned char>d(2*L+2,0);d[0]=1;
 for(int i=L+1;i<2*L+1;i++)d[i]=8;
 d.back()=9;
 int cycle[]={8,16,14,10,2,4},mincore=1000000,firstpal=-1;
 for(int t=0;t<=T;t++){
   int n=d.size(),h=(n+1)/2,k=0;
   bool pal=true;
   for(int i=0;i<n/2;i++)if(d[i]!=d[n-1-i]){pal=false;break;}
   if(pal&&firstpal<0)firstpal=t;
   while(k<h){int i=h-1-k,j=n-1-i;
     if((i==j?2*d[i]:d[i]+d[j])!=cycle[t%6])break;
     ++k;
   }
   mincore=min(mincore,k);
   if(t==0||t==1||t==10||t==100||t==1000||t==10000||t==T)
     cout<<"DIGITS step="<<t<<" digits="<<n<<" central="<<k
         <<" palindrome="<<pal<<" fnv64="<<hex<<fnv(d)<<dec<<'\n';
   if(t==T)break;
   vector<unsigned char>next(n+1);int c=0;
   for(int i=0;i<n;i++){int s=d[i]+d[n-1-i]+c;next[i]=s%10;c=s/10;}
   if(c)next[n]=c;else next.pop_back();d.swap(next);
 }
 cout<<"DIGITS done pal_first="<<firstpal<<" minimum_central_halfwidth="<<mincore
     <<" final_digits="<<d.size()<<'\n';
}
