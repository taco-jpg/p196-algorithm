// Agent X30: phase slip against an ordinary decimal reference.
// Run: g++ -O3 -std=c++17 phase_shadow.cpp -o shadow; ./shadow 12000 4000 1 1 20000
#include <bits/stdc++.h>
using namespace std;
vector<uint8_t> make_seed(int q,int at,int span,int kind){
 string s; s.reserve(4*q);
 for(int k=0;k<q;k++){
  string w="5346";
  if(kind && k>=at && k<at+span)
   w=kind==1?"3465":kind==2?"4653":kind==3?"6534":"5345";
  s+=w;
 }
 vector<uint8_t>d;
 for(auto it=s.rbegin();it!=s.rend();++it)d.push_back(*it-'0');
 return d;
}
void advance(vector<uint8_t>&d,vector<uint8_t>&work){
 int n=d.size(),c=0;
 work.resize(n+1);
 for(int i=0;i<n;i++){int z=d[i]+d[n-1-i]+c;work[i]=z%10;c=z/10;}
 if(c)work[n]=c;
 work.resize(n+c);d.swap(work);
}
int period4(const vector<uint8_t>&d){
 int n=d.size(),run=0,best=0;
 for(int i=0;i<n/2;i++){
  int z=d[i]+d[n-1-i];
  run=(i>=4&&z==d[i-4]+d[n-1-i+4])?run+1:1;
  best=max(best,run);
 }return best;
}
int main(int argc,char**argv){
 int q=argc>1?atoi(argv[1]):12000,at=argc>2?atoi(argv[2]):4000,
     span=argc>3?atoi(argv[3]):1,kind=argc>4?atoi(argv[4]):1,
     T=argc>5?atoi(argv[5]):20000;
 if(q<=0||at<0||span<=0||at+span>q||kind<1||kind>4||T<0)return 1;
 auto x=make_seed(q,at,span,0),y=make_seed(q,at,span,kind);
 vector<uint8_t>u,v;
 int over=0,minrun=INT_MAX,minrun_at=0,min_left=INT_MAX,min_right=INT_MAX,
  max_witness=0,max_diff=0,min_diff=INT_MAX,unshielded=0;
 cout<<"t,n,overflow,diff_count,guard_LSB,guard_MSB,witness_index,p4_maxrun\n";
 for(int t=0;t<=T;t++){
  int n=x.size();
  if(n!=(int)y.size()){cerr<<"clock divergence t="<<t<<"\n";return 2;}
  int lo=n,hi=-1,ndiff=0;
  for(int i=0;i<n;i++)if(x[i]!=y[i]){lo=min(lo,i);hi=i;ndiff++;}
  if(ndiff==0){cerr<<"unexpected coalescence t="<<t<<"\n";return 3;}
  int guardL=lo,guardR=n-hi-1,witness=-1;
  for(int i=0;i<n/2;i++)if(y[i]!=y[n-1-i]){witness=i;break;}
  if(witness<0){cerr<<"PALINDROME t="<<t<<"\n";return 4;}
  if(witness>=min(guardL,guardR))unshielded++;
  int run=period4(y);
  if(run<minrun){minrun=run;minrun_at=t;}
  min_left=min(min_left,guardL);min_right=min(min_right,guardR);
  max_witness=max(max_witness,witness);
  max_diff=max(max_diff,ndiff);min_diff=min(min_diff,ndiff);
  if(t%1000==0||t==T)
   cout<<t<<","<<n<<","<<over<<","<<ndiff<<","<<guardL<<","
       <<guardR<<","<<witness<<","<<run<<"\n";
  if(t==T)break;
  advance(x,u);advance(y,v);
  if(x.size()!=y.size())return 5;
  if(x.size()>n)over++;
 }
 cerr<<"PASS q="<<q<<" at="<<at<<" span="<<span<<" kind="<<kind
     <<" T="<<T<<" overflows="<<over<<" min_pair_p4_run="<<minrun
     <<" min_run_step="<<minrun_at<<" min_guard_LSB="<<min_left
     <<" min_guard_MSB="<<min_right<<" max_witness="<<max_witness
     <<" min_hamming="<<min_diff<<" max_hamming="<<max_diff
     <<" unshielded_witness_steps="<<unshielded<<"\n";
 return unshielded?6:0;
}
