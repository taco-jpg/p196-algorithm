// Independent base-10 digit vector for an odd-centre delayed-repair seed.
// Does not use automaton carry states or any engine transitions.
#include <bits/stdc++.h>
using namespace std;using B=unsigned char;using C=array<B,8>;
vector<C> get(const string &fn,const string &lab){ifstream f(fn);string l;while(getline(f,l)){istringstream ss(l);string k,s;ss>>k;if(k!=lab)continue;ss>>s;vector<C> out;while(ss>>s){if(s.size()!=8)throw runtime_error("bad col");C c;for(int t=0;t<8;t++){auto n=string("0123456789ABCDEFGHI").find(s[t]);if(n==string::npos)throw runtime_error("invalid col");c[t]=(B)n;}out.push_back(c);}return out;}throw runtime_error("missing "+lab);}
int main(int argc,char **argv){string file=argc>1?argv[1]:"bridge_witness_generated.txt";int steps=argc>2?atoi(argv[2]):20000;int blocks=argc>3?atoi(argv[3]):200;int guard=argc>4?atoi(argv[4]):1024;
 auto p=get(file,"ROOTPATH"),a=get(file,"LOOPA"),b=get(file,"LOOPB");if(p.size()!=45||a.size()!=92||b.size()!=97)throw runtime_error("wrong control witness");vector<C> path=p;for(int i=0;i<blocks;i++){auto &z=i%2?b:a;path.insert(path.end(),z.begin(),z.end());}path.push_back(a[0]);path.push_back(a[1]);int h=path.size();
 vector<B> d;d.reserve(2*h+steps);for(int i=0;i<h-1;i++)d.push_back(path[i][0]/2);if(path.back()[0]%2)throw runtime_error("odd central coefficient");d.push_back(path.back()[0]/2);for(int i=h-2;i>=0;i--)d.push_back(path[i][0]-path[i][0]/2);if(d.back()==0)throw runtime_error("leading zero");
 // Further columns are only a reference phase oracle, never used to produce the integer evolution.
 path.insert(path.end(),a.begin()+2,a.end());path.insert(path.end(),a.begin(),a.end());
 ofstream f("long_replay_checkpoints.csv");f<<"step,decimal_digits,matching_exterior_columns,full_phase_pairword,central_deficit,top_two_differ\n";
 int minmatch=INT_MAX;int full9=0,full10=0;int firstfailure=-1;for(int t=0;t<=steps;t++){
   int n=d.size(),m=(n+1)/2,k=0;
   for(;k<m&&k<(int)path.size();k++)if(int(d[k])+int(d[n-1-k])!=(int)path[k][t%8])break;
   bool full=k==m;bool nonpal=false;for(int i=0;i<n/2;i++)if(d[i]!=d[n-1-i]){nonpal=true;break;}
   if(!nonpal){cerr<<"palindrome step "<<t<<"\n";return 2;}
   if(t<=10&&t>=9){if(t==9)full9=full;if(t==10)full10=full;}
   if(!full&&firstfailure<0)firstfailure=t;
   minmatch=min(minmatch,k);
   if(k<guard){cerr<<"exterior guard fails step "<<t<<" match "<<k<<"\n";return 3;}
   if(t==0||t<=16||t%1000==0||t==steps)f<<t<<','<<n<<','<<k<<','<<full<<','<<(m-k)<<','<<nonpal<<'\n';
   if(t==steps)break;
   vector<B> next(n+1);int carry=0;for(int i=0;i<n;i++){int sum=int(d[i])+int(d[n-1-i])+carry;next[i]=sum%10;carry=sum/10;}if(carry)next[n]=carry;else next.pop_back();
   if((int)next.size()-n!=(t%2==0?1:0)){cerr<<"overflow schedule fails step "<<t<<"\n";return 4;}
   d.swap(next);
 }
 cout<<"PASS delayed-repair odd-centre seed: blocks="<<blocks<<" seed_digits="<<2*h-1<<" steps="<<steps<<" final_digits="<<d.size()<<" min_matching_exterior="<<minmatch<<" first_full_failure="<<firstfailure<<" restored_at9="<<full9<<" restored_at10="<<full10<<" no_palindromes=1\n";
 if(!full9||!full10||firstfailure!=3)return 5;
}
