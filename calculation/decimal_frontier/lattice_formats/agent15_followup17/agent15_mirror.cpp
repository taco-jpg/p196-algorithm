// Exhaustive exact test of spatially self-mirror absorbing bulk fixed points.
// Reduction: for odd m all reflection axes are rotations of axis 0;
// for even m axes split into parity classes 0,1.  Phi commutes with
// spatial translations, so testing one representative per class is complete.
// NOT a reachability test: positive rows require full automaton & integer replay.
#include <bits/stdc++.h>
using namespace std;
static int b,m,p;static string word;
static inline bool phi(const int* r,int gam,int*o){
 int i0=0;while(i0<m&&r[i0]==b-1)i0++;if(i0==m)return false;
 int A[24],D[24];int c=r[i0]>=b;
 A[(i0+1)%m]=c;for(int s=1;s<m;s++){int i=(i0+s)%m,j=(i+1)%m;A[j]=(r[i]+A[i])/b;}
 D[(i0+m-1)%m]=c;for(int s=1;s<m;s++){int i=(i0+m-s)%m,j=(i+m-1)%m;D[j]=(r[i]+D[i])/b;}
 for(int i=0;i<m;i++){int e=(r[i]+A[i])%b;int j=gam?(i+m-1)%m:i;int f=(r[j]+D[j])%b;o[i]=e+f;}
 return true;
}
static bool check(const int* r){int a[24],z[24];copy(r,r+m,a);
 for(int t=0;t<p;t++){if(!phi(a,word[t]-'0',z))return false;copy(z,z+m,a);}
 return equal(a,a+m,r);
}
int main(int argc,char**argv){if(argc<5){cerr<<"usage: bulk <base> <binaryword> <m> <max_initial_rows>\n";return 2;}
 b=atoi(argv[1]);word=argv[2];m=atoi(argv[3]);p=word.size();uint64_t cap=strtoull(argv[4],nullptr,10),count=0,hits=0,genuine=0;int S=count_if(word.begin(),word.end(),[](char x){return x=='1';});
 if(S%m){cerr<<"m does not divide S\n";return 3;}
 for(int alpha=0;alpha<(m%2?1:2);alpha++){vector<int> reps,part(m);for(int i=0;i<m;i++){part[i]=(alpha-i+m)%m;if(i<=part[i])reps.push_back(i);}
 vector<int>digits(reps.size());uint64_t inClass=0;int r[24];bool keepGoing=true;
 while(keepGoing){for(size_t j=0;j<reps.size();j++){r[reps[j]]=digits[j];r[part[reps[j]]]=digits[j];}
  count++;inClass++;
  if(check(r)){hits++;int d=1;for(;d<m;d++)if(m%d==0){bool period=true;for(int i=0;i<m;i++)if(r[i]!=r[(i+d)%m]){period=false;break;}if(period)break;}
   if(d==m){genuine++;if(genuine<=30){cout<<"HIT base="<<b<<" p="<<p<<" m="<<m<<" axis="<<alpha<<" word="<<word<<" row=";for(int i=0;i<m;i++)cout<<r[i]<<",";cout<<"\n";}}}
  if(count>=cap){cout<<"CAPPED b="<<b<<" p="<<p<<" m="<<m<<" axis="<<alpha<<" tested="<<count<<" hits="<<hits<<" genuine="<<genuine<<"\n";return 0;}
  size_t j=0;while(j<digits.size()&&++digits[j]>=2*b-1){digits[j]=0;j++;}if(j==digits.size())keepGoing=false;
 }
 cout<<"AXIS_DONE base="<<b<<" p="<<p<<" m="<<m<<" alpha="<<alpha<<" tested="<<inClass<<"\n";
 }
 cout<<"EXHAUSTED b="<<b<<" p="<<p<<" m="<<m<<" tested="<<count<<" return_rows="<<hits<<" genuine_rows="<<genuine<<"\n";
}
