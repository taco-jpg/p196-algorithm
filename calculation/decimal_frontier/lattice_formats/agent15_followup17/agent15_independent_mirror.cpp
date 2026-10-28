// Independent checker: compute cyclic carries by guessing a fixed point
// (rather than choosing the first nonneutral coefficient as in the main engine).
// Exact integer arithmetic, validates the all-spatial-period base-7 p21 exclusion.
#include <bits/stdc++.h>
using namespace std;
int b,m;string g;
bool next_row(const vector<int>&r,int gamma,vector<int>&n){
 if(all_of(r.begin(),r.end(),[&](int x){return x==b-1;}))return false;
 vector<int>A(m),D(m);bool af=false,df=false;
 for(int guess=0;guess<=1;guess++){
  vector<int>a(m);a[0]=guess;int c=guess;
  for(int i=0;i<m;i++){c=(r[i]+c)/b;if(i<m-1)a[i+1]=c;}
  if(c==guess){A=a;af=true;break;}
 }
 for(int guess=0;guess<=1;guess++){
  vector<int>d(m);d[m-1]=guess;int c=guess;
  for(int i=m-1;i>=0;i--){c=(r[i]+c)/b;if(i>0)d[i-1]=c;}
  if(c==guess){D=d;df=true;break;}
 }
 if(!af||!df)throw runtime_error("nonneutral carry fixed point absent");
 n.resize(m);for(int i=0;i<m;i++){int j=(i+m-gamma)%m;n[i]=(r[i]+A[i])%b+(r[j]+D[j])%b;}
 return true;
}
struct Counts{long long tested=0,returns=0,genuine=0;};
Counts test(int bb,const string&gs,int mm){b=bb;m=mm;g=gs;int maxv=2*b-1;Counts stats;
 for(int alpha=0;alpha<(m%2?1:2);alpha++){
  vector<int> reps,partner(m);for(int i=0;i<m;i++)partner[i]=(alpha-i+m)%m;
  for(int i=0;i<m;i++)if(i<=partner[i])reps.push_back(i);
  vector<int>val(reps.size());bool run=true;
  while(run){vector<int>r(m);for(int q=0;q<(int)reps.size();q++){r[reps[q]]=val[q];r[partner[reps[q]]]=val[q];}
   stats.tested++;vector<int>z=r,n;bool ok=true;
   for(char gg:g){if(!next_row(z,gg-'0',n)){ok=false;break;}z.swap(n);}
   if(ok&&z==r){stats.returns++;int minper=m;
     for(int d=1;d<m;d++)if(m%d==0){bool per=true;for(int i=0;i<m;i++)if(r[i]!=r[(i+d)%m])per=false;if(per){minper=d;break;}}
     if(minper==m)stats.genuine++;}
   int j=0;for(;j<(int)val.size();j++){if(++val[j]<maxv)break;val[j]=0;}
   if(j==(int)val.size())run=false;
  }
 }
 return stats;
}
int main(){
 auto check=[](int b,string g,int m,long long tested,long long returns,long long genuine){Counts r=test(b,g,m);cout<<"CHECK b="<<b<<" p="<<g.size()<<" m="<<m<<" tested="<<r.tested<<" returns="<<r.returns<<" genuine="<<r.genuine<<"\n";
 if(r.tested!=tested||r.returns!=returns||r.genuine!=genuine)throw runtime_error("independent counts mismatch");};
 check(13,"1010010000",1,25,4,4);
 check(9,"1100011000",4,5202,8,4);
 check(7,"101001010110001011000",1,13,2,2);
 check(7,"101001010110001011000",3,169,2,0);
 check(7,"101001010110001011000",9,371293,2,0);
 cout<<"PASS: exact finite control and base-7 p21 mirror-row census\n";
}
