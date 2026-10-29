// Empirical neutral-9 stripe transformations in the real decimal 196 orbit.
// On sampled steps, each run of >=5 coefficient-9 sites has an interior
// successor run of constant coefficient 0, 9, or 18 (depending on two carries).
#include <bits/stdc++.h>
using namespace std;using ull=unsigned long long;
static int go(vector<uint8_t>&d,vector<uint8_t>&o){int n=d.size(),c=0;o.resize(n+1);for(int i=0;i<n;i++){int z=d[i]+d[n-1-i]+c;o[i]=z%10;c=z/10;}o[n]=c;d.swap(o);d.resize(n+(c!=0));return c;}
int main(int argc,char**argv){int N=argc>1?atoi(argv[1]):100000,stride=argc>2?atoi(argv[2]):100;
 vector<uint8_t>d={6,9,1},o,p,q;array<ull,3>trans[2]{};ull events=0,bad=0;ofstream f("neutral_switch_events.tsv");f<<"t\tstart\tlen9\tgam\tnew_symbol\tinterior_len\n";
 for(int t=0;t<N;t++){bool sample=t%stride==0;int n=d.size(),m=n/2;if(sample){p.resize(m);for(int i=0;i<m;i++)p[i]=d[i]+d[n-1-i];}
 int gamma=go(d,o);
 if(sample){int nextm=d.size()/2;q.resize(nextm);for(int i=0;i<nextm;i++)q[i]=d[i]+d[d.size()-1-i];
  for(int j=0;j<m;){if(p[j]!=9){j++;continue;}int k=j;while(k<m&&p[k]==9)k++;int L=k-j;
   if(L>=5&&j>3&&k<m-3){int st=j+1,en=gamma?k:(k-1);int x=q[st];bool match=x==0||x==9||x==18;for(int i=st;i<en;i++)if(q[i]!=x)match=false;
    if(!match){bad++;cerr<<"UNEXPECTED t="<<t<<" start="<<j<<" gamma="<<gamma<<" symbol="<<x<<"\n";}
    if(x==0)trans[gamma][0]++;else if(x==9)trans[gamma][1]++;else if(x==18)trans[gamma][2]++;
    events++;if(L>=7||events<=20)f<<t<<'\t'<<j<<'\t'<<L<<'\t'<<gamma<<'\t'<<x<<'\t'<<(en-st)<<'\n';
   }j=k;}
 }}
 cout<<"steps="<<N<<" stride="<<stride<<" sampled 9-runs>=5 total="<<events<<" errors="<<bad<<"\n";
 for(int g=0;g<2;g++)cout<<"gamma="<<g<<" -> symbol0 "<<trans[g][0]<<" neutral9 "<<trans[g][1]<<" symbol18 "<<trans[g][2]<<"\n";
 if(bad)return 2;
}
