// Agent X17: two independent-from-formula ordinary decimal digit orbits, paired-shadow diagnostics.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
using Dig=vector<uint8_t>;
Dig step(const Dig& a) {
  const size_t n=a.size(); Dig b(n); int c=0;
  for(size_t i=0;i<n;i++) {int z=a[i]+a[n-1-i]+c; b[i]=z%10;c=z/10;}
  if(c) b.push_back(uint8_t(c));
  return b;
}
Dig make_pal(int n, const string& motif) {
  Dig a(n);
  for(int i=0;i<n;i++) a[i]=uint8_t(motif[min(i,n-1-i)%motif.size()]-'0');
  if(a[n-1]==0) throw runtime_error("leading zero");
  return a;
}
bool pal(const Dig& a) {for(size_t i=0;i<a.size()/2;i++) if(a[i]!=a[a.size()-1-i])return false;return true;}
uint64_t fnv(const Dig& a) {uint64_t h=14695981039346656037ULL;for(auto x:a){h^=x;h*=1099511628211ULL;}return h;}
int main(int argc,char**argv){
  if(argc<5){cerr<<"usage: shadow LENGTH STEPS MOTIF OUTPUT.csv [PERTURB_POS_FROM_CENTRE]\n";return 2;}
  int n=atoi(argv[1]), T=atoi(argv[2]);string motif=argv[3];int off=argc>5?atoi(argv[5]):1;
  if(n%2!=1||n<3||off<=0||off>n/2)return 2;
  Dig a=make_pal(n,motif),b=a;int j=n/2-off;
  if(b[j]==9) return 2;
  b[j]++;
  ofstream f(argv[4]);f<<"t,length,shadow_left,shadow_right,same_length,base_pal,pert_pal,base_hash,pert_hash,outer_witness\n";
  int minimum=1000000000, splitt=-1, pal_t=-1, witnesses=0,
      first_lost_witness=-1, first_zero_shadow=-1;
  for(int t=0;t<=T;t++) {
    int l=0,r=0, witness=-1;bool same=a.size()==b.size();
    if(same){int L=int(a.size());while(l<L&&a[l]==b[l])l++;while(r<L&&a[L-1-r]==b[L-1-r])r++;
      int outer=min(l,r);minimum=min(minimum,outer);
      for(int k=0;k<outer;k++)if(a[k]!=a[L-1-k]){witness=k;break;}
      if(witness>=0)witnesses++;
      if(t>0 && witness<0 && first_lost_witness<0)first_lost_witness=t;
      if(outer==0 && first_zero_shadow<0)first_zero_shadow=t;
    }else if(splitt<0)splitt=t;
    bool pb=pal(b); if(pb&&pal_t<0)pal_t=t;
    if(t<=10||t%100==0||t==T||t>=32590||!same||pb)f<<t<<","<<a.size()<<","<<l<<","<<r<<","<<same<<","<<pal(a)<<","<<pb<<","<<fnv(a)<<","<<fnv(b)<<","<<witness<<"\n";
    if(!same||pb){cerr<<"early stop t="<<t<<" length_split="<<!same<<" pert_pal="<<pb<<"\n";break;}
    if(t<T){a=step(a);b=step(b);}
  }
  cerr<<"initial="<<n<<" steps_requested="<<T<<" first_length_split="<<splitt<<" first_pert_pal="<<pal_t<<" baseline_outer_witness_snapshots="<<witnesses<<" min_shadow="<<minimum<<" first_lost_external_witness="<<first_lost_witness
      <<" first_zero_shadow="<<first_zero_shadow<<"\n";
}