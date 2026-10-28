// Exact position-zero DFA enumeration of primitive canonical overflow streams.
// Necessary filter only; it does not establish any Lychrel certificate.
#include <bits/stdc++.h>
using namespace std; using U=uint64_t;
int b,nn;
struct VHash {size_t operator()(vector<U> const& a)const noexcept {U h=1469598103934665603ULL; for(U x:a)h=(h^x)*1099511628211ULL;return h;}};
struct Dfa {
 vector<vector<U>> st;unordered_map<vector<U>,int,VHash> id;vector<array<int,2>> nx;vector<char>acc;
 Dfa(int bb){b=bb;nn=2*b-2;vector<U> init(nn);for(int i=0;i<nn;i++) init[i]=1ULL<<i;st.push_back(init);id[init]=0;nx.push_back({-1,-1});
 for(size_t i=0;i<st.size();i++) for(int gg=0;gg<2;gg++){
   vector<U> ns(nn);bool any=false;
   for(int j=0;j<nn;j++) {U m=st[i][j];while(m){int xi=__builtin_ctzll(m);m&=m-1;int x=xi+1;
    for(int hn=0;hn<2;hn++){int s=x+hn;if(s/b!=gg)continue;int xn=x%b+(gg?1:s%b);if(xn>=1&&xn<=nn)ns[j]|=1ULL<<(xn-1);}
   } if(ns[j])any=true;}
   if(!any){nx[i][gg]=-1;continue;}
   auto it=id.find(ns);if(it==id.end()){int k=st.size();id.emplace(ns,k);st.push_back(move(ns));nx.push_back({-1,-1});nx[i][gg]=k;}
   else nx[i][gg]=it->second;
 }
 acc.assign(st.size(),0);for(size_t i=0;i<st.size();i++)for(int j=0;j<nn;j++)if(st[i][j]&(1ULL<<j))acc[i]=1;
 }
 void gen(int P, ostream &out){int S=st.size();vector<vector<uint8_t>> feas(P+1,vector<uint8_t>(S));for(int s=0;s<S;s++)feas[0][s]=acc[s];
   for(int r=1;r<=P;r++)for(int s=0;s<S;s++)for(int g=0;g<2;g++){int k=nx[s][g];if(k>=0&&feas[r-1][k])feas[r][s]=1;}
   uint64_t total=0, primitive=0;vector<int> states(P+1),choices(P+1);uint64_t w=0;int d=0;states[0]=0;
   if(!feas[P][0]){cerr<<"b="<<b<<" p="<<P<<" states="<<S<<" f1_legal=0\n";return;}
   while(d>=0){
     if(d==P){bool canonical=true;uint64_t mask=(1ULL<<P)-1;for(int r=1;r<P;r++){uint64_t rot=((w>>r)|(w<<(P-r)))&mask; if(rot<w){canonical=false;break;}}
      if(canonical){total++;bool prim=true;for(int r=1;r<P;r++)if((((w>>r)|(w<<(P-r))) & mask)==w){prim=false;break;}
       if(prim){primitive++;string str;for(int t=0;t<P;t++)str+=('0'+((w>>t)&1));out<<str<<'\n';}}
      --d;continue;}
     if(choices[d]>=2){choices[d]=0;--d;continue;}
     int gg=choices[d]++;int j=nx[states[d]][gg];if(j<0||!feas[P-d-1][j])continue;
     if(gg)w|=1ULL<<d;else w&=~(1ULL<<d);
     states[d+1]=j;choices[d+1]=0;d++;
   }
   cerr<<"b="<<b<<" p="<<P<<" states="<<S<<" canonical_legal="<<total<<" primitive_legal="<<primitive<<"\n";
 }
};
int main(int argc,char**argv){if(argc<4)return 2;int b0=atoi(argv[1]),pmin=atoi(argv[2]),pmax=atoi(argv[3]);Dfa df(b0);for(int p=pmin;p<=pmax;p++){string path="streams_b"+to_string(b0)+"_p"+to_string(p)+".txt";ofstream f(path);df.gen(p,f);} }
