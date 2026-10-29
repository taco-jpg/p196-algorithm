// W03: exact decimal RAA cap-steering scan, original digits least significant first.
#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
using D=vector<unsigned char>;
D seed(int head,int q,int tail){D a={(unsigned char)(tail%10),(unsigned char)(tail/10)};a.insert(a.end(),2*q,9);a.push_back(head%10);a.push_back(head/10);return a;}
D step(const D&a){int n=a.size(),c=0;D b;b.reserve(n+1);for(int i=0;i<n;i++){int v=a[i]+a[n-1-i]+c;b.push_back(v%10);c=v/10;}if(c)b.push_back(c);return b;}
vector<int> group(const D&a){vector<int>out;for(int i=0;i<(int)a.size();i+=2)out.push_back(a[i]+(i+1<(int)a.size()?10*a[i+1]:0));return out;}
bool insertion(const D&a,const D&b){auto x=group(a),y=group(b);int p=0,s=0,n=min(x.size(),y.size());while(p<n&&x[p]==y[p])p++;while(s<n-p&&x[x.size()-1-s]==y[y.size()-1-s])s++;return x.size()==(size_t)(p+s)&&y.size()==(size_t)(p+s+1)&&y[p]==99;}
bool pal(const D&a){for(int i=0,j=(int)a.size()-1;i<j;i++,j--)if(a[i]!=a[j])return false;return true;}
void trial(const string&mode,int head,int tail,int q){
 D a=seed(head,q,tail),b=seed(head,q+1,tail);int first=-1,count=0,run=0,maxrun=0,firstheal=-1;bool palfree=true;
 for(int t=0;t<10*q+200;t++){
  if(pal(a)||pal(b))palfree=false;
  bool ins=insertion(a,b);
  if(first<0&&!ins)first=t;
  if(first>=0){
   if(t>first&&ins){count++;run++;maxrun=max(maxrun,run);if(firstheal<0)firstheal=t;}else run=0;
   if(t==first+80)break;
  }
  a=step(a);b=step(b);
 }
 if(first<0){cerr<<"unreached collision"<<head<<","<<tail<<","<<q<<"\n";exit(3);}
 cout<<mode<<","<<head<<","<<tail<<","<<q<<","<<first<<","<<count<<","<<maxrun<<","<<firstheal<<","<<(palfree?1:0)<<"\n";
}
int main(int argc,char**argv){string mode=argc>1?argv[1]:"all";
 cout<<"mode,head,tail,Q,first,heals,maxrun,firstheal,palfree\n";
 if(mode=="all"||mode=="suffix")for(int tail=1;tail<=99;tail++)if(tail%10)for(int q=20;q<=260;q+=10)trial("suffix",12,tail,q);
 if(mode=="all"||mode=="prefix")for(int head=10;head<=99;head++)trial("prefix",head,26,200);
 if(mode=="all"||mode=="focused")for(int q=140;q<=500;q++)trial("focused",88,26,q);
}
