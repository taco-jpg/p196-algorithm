// AC18 phase-9 exact two-ended carry-collar endpoint-only exclusion census.
// Each successful collar step is exact for EVERY palindromic centre (see REPORT).
#include <array>
#include <vector>
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <chrono>
#include <string>
#include <cassert>
using namespace std;
static const int B[]={1,5,10,10,5,8,17,1,4,11,9,9,15,16,7,12,4,3,3,2,3,2,4,7,6,8,6,4,8,12,12,12,9,7};
static const int W[]={10,4,5,10,14,13,12,9,7};
// U ranks use parameter a=0,2,...,18 with rotations ordered as below, three per group.
static array<array<int,3>,30> getU(){array<array<int,3>,30> a{};int z=0;for(int v=0;v<=18;v+=2){a[z++]={9,v,18-v};a[z++]={v,18-v,9};a[z++]={18-v,9,v};}return a;}

// Unknown incoming carry before the high-end segment is exhaustively either 0 or 1.
// If both choices agree on the last R out-digits and gamma, resulting new prefix is exact.
// Output loses those positions whose high-end digit differs between cases.
struct Trial {int first=-1;int observed=-1,expected=-1;int certified=-1;int overflow=-1;int err=0;};
Trial run(const int* jj,int nj,const int* uu,int R0){
   int A[700],T[700],lo[700],hi[700];
   int n=0;for(int x:B)A[n++]=x;for(int r=0;r<14;r++)for(int x:W)A[n++]=x;
   for(int j=0;j<nj;j++) A[n++]=jj[j];
   for(int r=0;r<100;r++)for(int j=0;j<3;j++)A[n++]=uu[j];
   int H=n;
   if(R0>0 && R0<n)n=R0;
   int overflow_count=0;
   for(int t=0;t<120;t++){
      int c=0;
      for(int i=0;i<n;i++){int z=A[i]+c;lo[i]=z%10;c=z/10;}
      int c0=0,c1=1,first_diff=n;
      for(int i=n-1;i>=0;i--){
         int v=A[i];int z0=v+c0,z1=v+c1;
         hi[i]=z0%10;
         if(z0%10!=z1%10) first_diff=i;
         c0=z0/10;c1=z1/10;
      }
      if(c0!=c1)return Trial{.certified=n,.overflow=overflow_count,.err=1};
      int gamma=c0;overflow_count+=gamma;
      int m=min(n,first_diff+gamma);
      if(m<=0)return Trial{.certified=n,.overflow=overflow_count,.err=2};
      for(int i=0;i<m;i++)T[i]=lo[i]+(gamma?(i==0?gamma:hi[i-1]):hi[i]);
      std::copy(T,T+m,A);n=m;
   }
   const int cut=34+14*9; // W9 band ends at 160.
   int first=-1,observed=-1,expected=-1;
   for(int i=0;i<n;i++){
      int expected_i;
      if(i<34)expected_i=B[i];
      else if(i<cut)expected_i=W[(i-34)%9];
      else if(i<cut+nj)expected_i=jj[i-cut];
      else expected_i=uu[(i-cut-nj)%3];
      if(A[i]!=expected_i){first=i;observed=A[i];expected=expected_i;break;}
   }
   return Trial{.first=first,.observed=observed,.expected=expected,.certified=n,.overflow=overflow_count,.err=first<0?3:0};
}
int main(int argc,char**argv){
 int rank0=0,rank1=30,nj0=3,nj1=4;int r0=300;long maxcases=0;
 for(int i=1;i<argc;i++){
   string s=argv[i];if(s=="--rank-start")rank0=atoi(argv[++i]);
   else if(s=="--rank-end")rank1=atoi(argv[++i]);
   else if(s=="--j-min")nj0=atoi(argv[++i]);
   else if(s=="--j-max")nj1=atoi(argv[++i]);
   else if(s=="--prefix")r0=atoi(argv[++i]);
   else if(s=="--maxcases")maxcases=atol(argv[++i]);
   else {cerr<<"unknown flag "<<s<<"\n";return 1;}
 }
 auto us=getU();long long count=0;long long fails=0;long long err=0;map<int,long long> hist;map<int,long long> overflow;map<int,long long> cert;int min_cert=999;
 auto start=chrono::steady_clock::now();
 for(int rank=rank0;rank<rank1;rank++)for(int nj=nj0;nj<=nj1;nj++){
    long sz=1;for(int j=0;j<nj;j++)sz*=19;
    for(long idx=0;idx<sz;idx++){
      int jj[10],tmp=idx;for(int j=0;j<nj;j++){jj[j]=tmp%19;tmp/=19;}
      auto t=run(jj,nj,us[rank].data(),r0);
      count++; hist[t.first]++;overflow[t.overflow]++;min_cert=min(min_cert,t.certified);
      if(t.err) {err++; if(err<=5)cerr<<"FAIL rank="<<rank<<" jlen="<<nj<<" jidx="<<idx<<" error="<<t.err<<" known="<<t.certified<<" first="<<t.first<<"\n";}
      if(t.first>=0)fails++;
      if(maxcases && count>=maxcases)goto done;
    }
    cerr<<"PROGRESS rank="<<rank<<" |J|="<<nj<<" count="<<count<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"\n";
 }
 done:cout<<"CENSUS count="<<count<<" mismatches="<<fails<<" unresolved="<<err<<" min_cert="<<min_cert<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"\n";
 cout<<"MISMATCH_POS";for(auto [key,v]:hist)cout<<" "<<key<<":"<<v;cout<<"\n";
 cout<<"OVERFLOWS";for(auto [key,v]:overflow)cout<<" "<<key<<":"<<v;cout<<"\n";
 return err?2:0;
}