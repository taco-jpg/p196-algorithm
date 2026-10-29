// Literal base-10 reverse-and-add for 196; little-endian digit-vector engine.
// Every iterate is tested for palindrome, including unsampled iterations.
// TSV rows are reproducibility checkpoints, never a proof of infinitely many.
#include <bits/stdc++.h>
using namespace std;
static uint64_t hashv(const vector<uint8_t>&v){uint64_t h=1469598103934665603ull;for(auto d:v){h^=d;h*=1099511628211ull;}return h;}
static bool pal(const vector<uint8_t> &d){for(size_t j=0,n=d.size();j<n/2;j++)if(d[j]!=d[n-1-j])return false;return true;}
static int correct_step(vector<uint8_t>&d, vector<uint8_t>&out){const int n=d.size();if((int)out.size()<n+1)out.resize(n+1);int c=0;for(int i=0;i<n;i++){int s=int(d[i])+int(d[n-1-i])+c;out[i]=s%10;c=s/10;}out[n]=c;d.swap(out);d.resize(n+(c!=0));return c;}
static void sample(const vector<uint8_t>&d,int64_t t,int overflow,ofstream& f,ofstream &f2,int K,int raw_step){size_t n=d.size();int m=n/2;int freq[19]={0};for(int i=0;i<m;i++)freq[d[i]+d[n-1-i]]++;double entropy=0;for(int x:freq)if(x){double p=(double)x/m;entropy-=p*log2(p);}f<<t<<'\t'<<n<<'\t'<<overflow<<'\t'<<pal(d)<<'\t'<<fixed<<setprecision(5)<<entropy<<'\t';for(int x:freq)f<<x<<',';f<<'\t'<<hex<<hashv(d)<<dec<<'\n';if(raw_step){f2<<t<<'\t'<<n<<'\t';for(int i=0;i<min(K,m);i++)f2<<char('A'+d[i]+d[n-1-i]);f2<<'\t';for(int i=max(0,m-K);i<m;i++)f2<<char('A'+d[i]+d[n-1-i]);f2<<'\n';}}
int main(int argc,char**argv){if(argc<2){cerr<<"usage: orbit_mine STEPS [SAMPLE_EVERY=100] [K=128] [SNAP_EVERY=1] [PREFIX=orbit]\n";return 2;}int steps=atoi(argv[1]),every=argc>2?atoi(argv[2]):100,K=argc>3?atoi(argv[3]):128,snap=argc>4?atoi(argv[4]):1;string prefix=argc>5?argv[5]:"orbit";vector<uint8_t>d={6,9,1},v;int overflow=0;ofstream f(prefix+"_samples.tsv"),f2(prefix+"_pairs.tsv"),f3(prefix+"_overflow.txt");f<<"step\tlength\toverflow\tpal\tentropy\tpair_hist\tfnv_hash\n";f2<<"step\tlength\touter_pairs_A_to_S\tinner_pairs_A_to_S\n";auto begin=chrono::steady_clock::now();
for(int t=0;t<=steps;t++){
 if(t%every==0||t==steps)sample(d,t,overflow,f,f2,K,t%snap==0);
 else if(t%snap==0){int n=d.size(),m=n/2;f2<<t<<'\t'<<n<<'\t';for(int i=0;i<min(K,m);i++)f2<<char('A'+d[i]+d[n-1-i]);f2<<'\t';for(int i=max(0,m-K);i<m;i++)f2<<char('A'+d[i]+d[n-1-i]);f2<<'\n';}
 if(pal(d)){cerr<<"PALINDROME DETECTED step="<<t<<"\n";return 3;}
 if(t==steps)break;
 overflow=correct_step(d,v);f3<<char('0'+overflow);
 if(t%10000==9999)cerr<<"steps="<<t+1<<" digits="<<d.size()<<" seconds="<<chrono::duration_cast<chrono::seconds>(chrono::steady_clock::now()-begin).count()<<"\n";
}
f3<<"\n";cerr<<"FINAL steps="<<steps<<" digits="<<d.size()<<" seconds="<<chrono::duration_cast<chrono::seconds>(chrono::steady_clock::now()-begin).count()<<"\n";
}
