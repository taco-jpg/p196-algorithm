// COMPUTED: exhaustive 88-step decimal core covariance and one-time band renewal.
#include <bits/stdc++.h>
using namespace std;
int cols[39][8],rows[8][20];vector<int>B,W;
vector<int>seed(const vector<int>&C,int q){
 vector<int>a=B;for(int k=0;k<q;k++)a.insert(a.end(),W.begin(),W.end());
 vector<int>p=a;p.insert(p.end(),C.begin(),C.end());
 for(int j=(int)a.size()-1;j>=0;j--)p.push_back(a[j]);return p;
}
void one(vector<int>&p,int&g){
 int n=p.size(),c=0;vector<int>d(n+1),next;
 for(int i=0;i<n;i++){int z=p[i]+c;d[i]=z%10;c=z/10;}
 g=c;if(g)d[n]=1;else d.resize(n);
 int m=d.size();next.resize(m);
 for(int i=0;i<m;i++)next[i]=d[i]+d[m-1-i];p.swap(next);
}
int run(vector<int>&p,int steps){
 for(int t=0;t<=steps;t++){
  if(p.size()<78)return 1;
  for(int j=0;j<39;j++)if(p[j]!=cols[j][t%8])return 2;
  if(t==steps)break;
  int g;one(p,g);if(g!=((t%2)==0))return 3;
 }
 return 0;
}
long long total=0,renewals=0;
int best=0,maxConsecutive=0;vector<int>bestC,winC;
void check(const vector<int>&C){
 auto x=seed(C,1),y=seed(C,2);
 int a=run(x,88),b=run(y,88);
 if(a||b){cerr<<"bad exterior/overflow core length="<<C.size()<<" idx="<<total<<" status="<<a<<","<<b<<"\n";exit(2);}
 if(x.size()!=2*39+C.size()+84){cerr<<"bad length\n";exit(3);}
 if(!equal(B.begin(),B.end(),x.begin())||!equal(B.begin(),B.end(),x.rbegin())||
    !equal(B.begin(),B.end(),y.begin())||!equal(B.begin(),B.end(),y.rbegin())||
    !equal(W.begin(),W.end(),y.begin()+39)||!equal(W.begin(),W.end(),y.rbegin()+39)){
  cerr<<"bad padding\n";exit(4);
 }
 vector<int>core(x.begin()+39,x.end()-39),core2(y.begin()+59,y.end()-59);
 if(core!=core2){cerr<<"bad 88-step core equality at "<<total<<"\n";exit(5);}
 int k=0;while(k<20&&k<(int)core.size()&&core[k]==W[k])k++;
 if(k>best){best=k;bestC=C;}
 if(k==20){
  renewals++;int n=1;vector<int>D(core.begin()+20,core.end()-20);
  for(int j=1;j<30;j++){
   auto z=seed(D,1);
   if(run(z,88))break;
   vector<int>out(z.begin()+39,z.end()-39);
   if(out.size()<40||!equal(W.begin(),W.end(),out.begin()))break;
   D.assign(out.begin()+20,out.end()-20);n++;
  }
  if(n>maxConsecutive){maxConsecutive=n;winC=C;}
 }
 total++;
}
void enumerate(int L){
 int h=L/2;vector<int>C(L);long long count=1;
 for(int i=0;i<h;i++)count*=19;
 for(long long i=0;i<count;i++){
  long long k=i;
  for(int j=0;j<h;j++){C[j]=C[L-1-j]=k%19;k/=19;}
  if(L%2)for(int z=0;z<=18;z+=2){C[h]=z;check(C);}
  else check(C);
 }
 cerr<<"complete L="<<L<<" cases="<<count*(L%2?10:1)<<" cumulative="<<total<<"\n";
}
int main(int argc,char**argv){
 int maxL=argc>1?atoi(argv[1]):7;
 ifstream f("lattice.txt");if(!f){cerr<<"run from agent-N18 directory\n";return 1;}
 for(auto&a:cols)for(int&v:a)f>>v;
 for(auto&a:rows)for(int&v:a)f>>v;
 for(auto&a:cols)B.push_back(a[0]);
 for(int v:rows[0])W.push_back(v);
 for(int L=0;L<=maxL;L++)enumerate(L);
 cout<<"PASS count="<<total<<" first_renewal="<<renewals
 <<" max_consecutive_renewals="<<maxConsecutive<<" witness=";
 for(int x:winC)cout<<x<<",";
 cout<<" best_W_prefix="<<best<<"\n";
}
