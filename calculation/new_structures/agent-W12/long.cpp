// Resumable W12 100k ordinary decimal RAA centre-pump certificate checker.
// C++17; deterministic state files, checkpointed every 25000 steps.
#include <bits/stdc++.h>
using namespace std;
string add(const string&s){
 int n=s.size(),c=0;string out(n+1,'0');
 for(int i=0;i<n;i++){
  int z=s[i]-'0'+s[n-1-i]-'0'+c;
  out[n-i]='0'+z%10;c=z/10;
 }
 out[0]='0'+c;if(!c)out.erase(out.begin());return out;
}
vector<int> parse(const string&s){
 vector<int>r;
 for(int end=s.size();end>0;end-=4){
  int x=0;for(int j=max(0,end-4);j<end;j++)x=x*10+s[j]-'0';
  r.push_back(x);
 }
 return r;
}
string alt(const string&s){
 string rev(s.rbegin(),s.rend());
 auto a=parse(s),b=parse(rev);
 vector<int>r(max(a.size(),b.size())+1);int c=0;
 for(int i=0;i+1<(int)r.size();i++){
  int z=(i<(int)a.size()?a[i]:0)+(i<(int)b.size()?b[i]:0)+c;
  r[i]=z%10000;c=z/10000;
 }
 r.back()=c;while(r.size()>1&&!r.back())r.pop_back();
 string out=to_string(r.back());char buf[8];
 for(int i=(int)r.size()-2;i>=0;i--){
  sprintf(buf,"%04d",r[i]);out+=buf;
 }
 return out;
}
uint64_t h64(const string&s){
 uint64_t h=1469598103934665603ull;
 for(unsigned char c:s){h^=c;h*=1099511628211ull;}
 return h;
}
int period(const string&s,bool pair){
 int n=s.size(),l=n/2-64,r=n/2+64;
 auto val=[&](int j){
  return pair?s[j]-'0'+s[n-1-j]-'0':s[j]-'0';
 };
 for(int p=1;p<=6;p++){
  bool good=true;
  for(int j=l+p;j<r;j++)if(val(j)!=val(j-p)){good=false;break;}
  if(good)return p;
 }
 return 0;
}
string file(string dir,int t,string s){
 return dir+"/w12_"+to_string(t)+"_"+s;
}
int main(int argc,char**argv){
 if(argc<5){cerr<<"usage: long start stop dir q [word]\n";return 1;}
 int start=atoi(argv[1]),stop=atoi(argv[2]),q=atoi(argv[4]);
 string dir=argv[3],w=argc>5?argv[5]:"428571";
 int m=w.size();string a,b;
 long long g0=0,g1=0,pc[7]={},pp[7]={};
 int maxmatch=0;
 if(start==0){
  a="12";for(int i=0;i<q;i++)a+=w;a+="34";
  b="12";for(int i=0;i<=q;i++)b+=w;b+="34";
 } else {
  ifstream fa(file(dir,start,"a")),fb(file(dir,start,"b")),fs(file(dir,start,"stats"));
  fa>>a;fb>>b;fs>>g0>>g1>>maxmatch;
  for(int i=0;i<=6;i++)fs>>pc[i];
  for(int i=0;i<=6;i++)fs>>pp[i];
  if(!fa||!fb||!fs){cerr<<"BROKEN_CHECKPOINT\n";return 2;}
 }
 for(int t=start;t<=stop;t++){
  int n=a.size(),c=n/2;
  if(b.size()!=a.size()+m
     ||a.compare(0,c,b,0,c)
     ||a.compare(c,n-c,b,c+m,n-c)){
   cerr<<"PUMP_FAIL t="<<t<<"\n";return 3;
  }
  int p=period(a,false),p2=period(a,true);
  if(!p||!p2){cerr<<"PERIOD_FAIL t="<<t<<"\n";return 4;}
  int mm=0;
  while(mm<min(c,n-c)&&a[mm]==a[n-1-mm])mm++;
  if(mm>=min(c,n-c)){cerr<<"NONPAL_FAIL t="<<t<<"\n";return 5;}
  if(t==stop){
   cout<<"checkpoint t="<<t<<" digits="<<n
       <<" gammas="<<g0<<","<<g1
       <<" maxmatch="<<maxmatch<<" p="<<p<<" pp="<<p2
       <<" fnv64="<<hex<<h64(a)<<dec
       <<" inserted="<<b.substr(c,m)<<"\n";
   break;
  }
  pc[p]++;pp[p2]++;maxmatch=max(maxmatch,mm);
  string na=add(a),nb=add(b);
  if(t%1000==0&&(na!=alt(a)||nb!=alt(b))){
   cerr<<"INDEPENDENT_ARITH_FAIL t="<<t<<"\n";return 6;
  }
  if(na.size()>a.size())g1++;else g0++;
  a.swap(na);b.swap(nb);
 }
 ofstream fa(file(dir,stop,"a")),fb(file(dir,stop,"b")),fs(file(dir,stop,"stats"));
 fa<<a;fb<<b;fs<<g0<<' '<<g1<<' '<<maxmatch<<'\n';
 for(int i=0;i<=6;i++)fs<<pc[i]<<' ';
 fs<<'\n';
 for(int i=0;i<=6;i++)fs<<pp[i]<<' ';
 fs<<'\n';
}
