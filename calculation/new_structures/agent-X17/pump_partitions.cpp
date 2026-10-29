#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <set>
#include <string>
#include <utility>
#include <vector>
using namespace std;using D=vector<uint8_t>;
D init(int n,int mask){string m="88283583";D a(n);for(int i=0;i<n;i++)a[i]=m[min(i,n-1-i)%8]-'0';for(int k=1;k<=8;k++)if(mask>>(k-1)&1)a[n/2-k]++;return a;}
D step(const D&a){int n=a.size(),c=0;D b(n);for(int i=0;i<n;i++){int z=a[i]+a[n-1-i]+c;b[i]=z%10;c=z/10;}if(c)b.push_back(c);return b;}
int main(int argc,char**argv){if(argc!=4){cerr<<"usage N T CSV\n";return 2;}int n=atoi(argv[1]),T=atoi(argv[2]); vector<D> a,b;for(int i=0;i<256;i++){a.push_back(init(n,i));b.push_back(init(n+16,i));}ofstream f(argv[3]);f<<"t,valid_masks,first_fail_count,unique_min_cuts,unique_blocks,unique_cut_blocks,min_cut,max_cut\n";vector<int>first(256,-1);for(int t=0;t<=T;t++){set<int> cuts;set<string> blocks;set<pair<int,string>> combine;int valid=0,lo=1000000,hi=-1,failed=0;for(int mask=0;mask<256;mask++){
 const D&A=a[mask],&B=b[mask];int N=A.size(),K=B.size();
 if(K-N!=16 || (N%2)!=(K%2)){if(first[mask]<0)first[mask]=t;failed++;continue;}
 int L=N/2,LL=K/2;
 int p=0;while(p<L && A[p]==B[p] && A[N-1-p]==B[K-1-p])p++;
 int s=0;while(s<L && A[L-1-s]==B[LL-1-s] && A[N-L+s]==B[K-LL+s])s++;
 if(p+s<L){if(first[mask]<0)first[mask]=t;failed++;continue;}
 int j=L-s;string block;block.reserve(16);for(int i=0;i<8;i++){block+=char('0'+B[j+i]);block+=char('0'+B[K-1-j-i]);}
 cuts.insert(j);blocks.insert(block);combine.insert({j,block});lo=min(lo,j);hi=max(hi,j);valid++;
 }
 if(t<=120||t%10==0||failed>0)f<<t<<","<<valid<<","<<failed<<","<<cuts.size()<<","<<blocks.size()<<","<<combine.size()<<","<<lo<<","<<hi<<"\n";
 if(t<T){for(int mask=0;mask<256;mask++){a[mask]=step(a[mask]);b[mask]=step(b[mask]);}}
 }
 cerr<<"first individual fold-splice failures: ";int none=0;for(int k=0;k<256;k++)if(first[k]<0)none++;cerr<<none<<" survive t<= "<<T<<"; first ten:";int count=0;for(int k=0;k<256&&count<10;k++)if(first[k]>=0){cerr<<" mask"<<k<<"@"<<first[k];count++;}cerr<<"\n";
}
