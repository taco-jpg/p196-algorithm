// Agent-X26: universal finite-horizon arbitrary-centre shield checker.
// Coefficient words are least-significant-first; no infinite-time claim.
#include <bits/stdc++.h>
using namespace std;
using Word=vector<uint8_t>;
Word seed(int L,const string& core) {
 string s="5"+string(L,'9')+core+string(L,'9')+"4";
 Word d; d.reserve(s.size());
 for(auto x=s.rbegin();x!=s.rend();++x)d.push_back(*x-'0');
 return d;
}
Word pairword(const Word& d) {
 Word p(d.size()); for(size_t i=0;i<d.size();i++)p[i]=d[i]+d[d.size()-1-i];return p;
}
Word raa(const Word& d) {
 int c=0;Word out;out.reserve(d.size()+1);
 for(size_t i=0,n=d.size();i<n;i++){int x=d[i]+d[n-i-1]+c;out.push_back(x%10);c=x/10;}
 if(c)out.push_back(c);return out;
}
Word step_pair(const Word& p) {
 int c=0;Word digits;digits.reserve(p.size()+1);
 for(int x:p){int z=x+c;digits.push_back(z%10);c=z/10;}
 if(c)digits.push_back(c);return pairword(digits);
}
int witness(const Word& d) {
 for(int i=0,n=d.size();i<n/2;i++)if(d[i]!=d[n-1-i])return i;return -1;
}
uint64_t fnv(const Word& d) {
 uint64_t h=1469598103934665603ull;
 for(auto it=d.rbegin();it!=d.rend();++it){h^=(uint8_t)('0'+*it);h*=1099511628211ull;}
 return h;
}
string thue_morse(int k) {
 string s(k,'9');for(int i=0;i<k/2;i++)if(__builtin_parity((unsigned)i))s[i]='8';return s;
}
int main(int argc,char**argv){
 if(argc!=4){cerr<<"Usage: ./universal <L> <T> <odd_k>\n";return 2;}
 int L=stoi(argv[1]),T=stoi(argv[2]),k=stoi(argv[3]);
 if(L<=T+2||k%2!=1){cerr<<"Need L>T+2 and odd k for this tested family\n";return 2;}
 Word d=seed(L,string(k,'9')),p=pairword(d);
 Word c=seed(L,thue_morse(k)),pc=pairword(c);
 const int n0=d.size(),b0=n0-2;
 int g=0,maxWitness=0,minMoat=INT_MAX,minEll=INT_MAX;
 cout<<"t\tn\tgamma\tell\t18_moat_lb\twitness\tfnv64_reference\tfnv64_thue\n";
 for(int t=0;t<=T;t++){
   int n=d.size(),ell=L+1-t+g,collar=n-ell;
   if(n!=n0+g||c.size()!=d.size()){cerr<<"ERROR lengths at "<<t<<"\n";return 3;}
   if(ell<2||collar!=L+k+1+t||b0-collar+1!=L-t){
     cerr<<"ERROR indices at "<<t<<"\n";return 3;
   }
   Word q=pairword(d);
   if(q!=p){cerr<<"ERROR own pairword "<<t<<"\n";return 3;}
   for(int i=collar;i<=b0;i++)if(p[i]!=18||p[n-1-i]!=18){
     cerr<<"ERROR reference 18 shell "<<t<<","<<i<<"\n";return 3;
   }
   minMoat=min(minMoat,L-t);minEll=min(minEll,ell);
   int w=witness(d);
   if(w<0||w>=ell-2){cerr<<"ERROR reference witness "<<t<<","<<w<<"\n";return 3;}
   maxWitness=max(maxWitness,w);
   Word qc=pairword(c);
   if(qc!=pc){cerr<<"ERROR core pairword engine "<<t<<"\n";return 3;}
   for(int i=0;i<ell;i++)if(qc[i]!=p[i]||qc[n-1-i]!=p[n-1-i]){
     cerr<<"ERROR core outside influence "<<t<<","<<i<<"\n";return 3;
   }
   if(witness(c)<0){cerr<<"ERROR core palindrome "<<t<<"\n";return 3;}
   if(t<5||t%1000==0||t==T)
     cout<<t<<'\t'<<n<<'\t'<<g<<'\t'<<ell<<'\t'<<L-t<<'\t'<<w<<'\t'
       <<hex<<setw(16)<<setfill('0')<<fnv(d)<<'\t'<<setw(16)<<fnv(c)
       <<dec<<setfill(' ')<<'\n';
   if(t==T)break;
   Word nd=raa(d),nc=raa(c);
   if(nd.size()!=nc.size()){cerr<<"ERROR overflow divergence "<<t<<"\n";return 3;}
   Word pnext=step_pair(p),pcnext=step_pair(pc);
   if(pairword(nd)!=pnext||pairword(nc)!=pcnext){
     cerr<<"ERROR independent digit/pair steps "<<t<<"\n";return 3;
   }
   g+=(nd.size()>(size_t)n);
   d.swap(nd);c.swap(nc);p.swap(pnext);pc.swap(pcnext);
 }
 cerr<<"PASS all "<<T+1<<" time slices; arbitrary centre 10^"<<k
     <<"; max_witness="<<maxWitness<<" min_18_moat="<<minMoat
     <<" min_ell="<<minEll<<" reference_final_digits="<<d.size()<<"\n";
}
