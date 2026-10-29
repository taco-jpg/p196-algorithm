#include <numeric>
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <vector>
using namespace std;
// Exhaustive 240-phase low-prefix census for rooted p12/m9 U6=(3,3,9,15,15,9).
// The cut is 330 coefficients into U6^k; the proven 300/240 cone bounds make the
// prefix independent of every admissible centre for q>=24,k>=100. No centre or
// modular pruning is used in this exhaustive J scan.
using V = vector<int>;
static const V B={10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
static const V W={5,18,4,8,1,15,4,0,5};
static const V U={3,3,9,15,15,9};
static int gam(int t){return t%4==0;}
static int tr(int x,int c){return x+c>=10;}
static V F(const V&w,int g){
  int m=(int)w.size(); V lo(m),hi(m); int z=0;
  for(int rep=0;rep<2;rep++) for(int x:w) z=tr(x,z);
  lo[0]=z; for(int i=1;i<m;i++) lo[i]=tr(w[i-1],lo[i-1]);
  z=0; for(int i=m-1;i>=0;i--) z=tr(w[i],z); for(int i=m-1;i>=0;i--) z=tr(w[i],z);
  hi[0]=z; for(int i=m-1;i>0;i--) hi[i]=tr(w[i],hi[(i+1)%m]);
  for(int i=0;i<m;i++){
    assert(tr(w[i],lo[i])==lo[(i+1)%m]);
    assert(tr(w[i],hi[(i+1)%m])==hi[i]);
  }
  V out(m);
  for(int i=0;i<m;i++){
    int low=(w[i]+lo[i])%10;
    int high= g ? (w[(i-1+m)%m]+hi[i])%10 : (w[i]+hi[(i+1)%m])%10;
    out[i]=low+high;
  }
  return out;
}
static vector<V> make_rows(const V&w,int n){vector<V> r; r.push_back(w); for(int t=0;t<n;t++) r.push_back(F(r.back(),gam(t))); return r;}
static V repeated(const V&w,int n){V out;out.reserve(w.size()*n);for(int i=0;i<n;i++)out.insert(out.end(),w.begin(),w.end());return out;}
static V get_target(int q,const V&J){V p=B;V ww=repeated(W,q);p.insert(p.end(),ww.begin(),ww.end());p.insert(p.end(),J.begin(),J.end());V uu=repeated(U,55);p.insert(p.end(),uu.begin(),uu.end());return p;}
struct Stats{long long total=0,wrestored=0,fullprefix=0,allJ=0;int first_min=99999,first_max=-1;long long first_hist[64]={0};long long by_band[4]={0};vector<V> hits;};
static void check_candidate(const V&J,int q,const vector<V>&ur,Stats&st){
  V P=get_target(q,J); const int M=(int)P.size();
  vector<int> all(M+6), b(M+6), lo(M), hi(M); V Q(M);
  for(int t=0;t<240;t++){
    // The six coefficients just before the cut must remain in the exact U6 bulk.
    for(int j=0;j<6;j++) assert(P[M-6+j]==ur[t][j]); // M-base=330, and 324 mod 6 = 0
    for(int j=0;j<6;j++) all[M+j]=ur[t][j];
    int r=M; while(r<M+6 && all[r]==9) ++r;
    assert(r<M+6); // every U6 row has non-9 reset in every 6-cell window
    b[r]=all[r]/10;
    for(int i=r-1;i>=0;i--){int x=(i<M?P[i]:ur[t][i-M]);b[i]=(x+b[i+1])/10;}
    int carry=0;
    for(int i=0;i<M;i++){int z=P[i]+carry;lo[i]=z%10;carry=z/10;}
    int g=P[0]/10;
    assert(g==gam(t));
    for(int i=0;i<M;i++) hi[i]=(P[i]+b[i+1])%10;
    if(!g){for(int i=0;i<M;i++)Q[i]=lo[i]+hi[i];}
    else {Q[0]=lo[0]+1;for(int i=1;i<M;i++)Q[i]=lo[i]+hi[i-1];}
    for(int i=0;i<M;i++) assert(Q[i]>=0 && Q[i]<=18);
    // Exact two-sided cone shield: this tail remains the next U6 phase.
    for(int j=0;j<6;j++) assert(Q[M-6+j]==ur[t+1][j]);
    bool odd=false;for(int i=0;i<(int)B.size();i++) odd |= (Q[i]&1);
    assert(odd); // phasewise rooted non-palindrome guard
    P.swap(Q);
  }
  V target=get_target(q,J);
  int first=-1;for(int i=0;i<M;i++)if(P[i]!=target[i]){first=i;break;}
  ++st.total;
  if(equal(P.begin(),P.begin()+250,target.begin())) ++st.wrestored;
  if(first<0){++st.fullprefix;st.hits.push_back(J);}
  else {
    st.first_min=min(st.first_min,first);st.first_max=max(st.first_max,first);
    if(first<(int)B.size()) st.by_band[0]++;
    else if(first<250) st.by_band[1]++;
    else if(first<250+(int)J.size()) st.by_band[2]++;
    else st.by_band[3]++;
    int dist=250-first;
    if(dist>=0 && dist<64) st.first_hist[dist]++;
  }
}
int main(int argc,char**argv){
  int q=24; if(argc>1) q=stoi(argv[1]); assert(q>=24);
  auto ur=make_rows(U,240);auto wr=make_rows(W,240);
  assert(ur[48]==U && ur[120]==V({15,15,9,3,3,9}) && ur[240]==U);
  assert(wr[12]==W && wr[240]==W);
  for(int t=0;t<240;t++){assert(gam(t)==(t%4==0));assert(accumulate(ur[t].begin(),ur[t].end(),0)==54);for(int i=0;i<6;i++)assert(!(ur[t][i]==9&&ur[t][(i+1)%6]==9));}
  Stats st;
  for(int len: {3,4}){
    long long n=1;for(int i=0;i<len;i++)n*=19;
    for(long long id=0;id<n;id++){
      long long x=id;V J(len);for(int i=0;i<len;i++){J[i]=x%19;x/=19;}
      ++st.allJ;
      check_candidate(J,q,ur,st);
    }
    cerr<<"DONE |J|="<<len<<" total="<<st.total<<" W-restored="<<st.wrestored<<" full-prefix="<<st.fullprefix<<"\n";
  }
  cout<<"label=COMPUTED_SCOPED_U6_240_ALL_J_CELL\n";
  cout<<"U=(3,3,9,15,15,9), q="<<q<<", k=100, C=[0,0,0] representative, all 19^3+19^4 J words\n";
  cout<<"all_J="<<st.allJ<<" checked="<<st.total<<" W9_prefix_restored="<<st.wrestored<<" full_prefix_return="<<st.fullprefix<<"\n";
  cout<<"first_mismatch_min="<<st.first_min<<" first_mismatch_max="<<st.first_max<<" bands(B,W,J,Uguard)="<<st.by_band[0]<<","<<st.by_band[1]<<","<<st.by_band[2]<<","<<st.by_band[3]<<"\n";
  cout<<"distance_from_W_cut_histogram (dist=250-first, 0..63):";for(int i=0;i<64;i++)if(st.first_hist[i])cout<<" "<<i<<":"<<st.first_hist[i];cout<<"\n";
  for(auto&J:st.hits){cout<<"FULL_PREFIX_HIT J=";for(int x:J)cout<<x<<",";cout<<"\n";}
  return 0;
}
