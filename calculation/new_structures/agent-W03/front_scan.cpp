#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
// Independent *literal* base-10 digit arithmetic, LSD first.
using D=vector<unsigned char>;
D seed(int q){D a={4,3};a.insert(a.end(),2*q,9);a.push_back(2);a.push_back(1);return a;}
D step(const D&a){
  int n=a.size(),c=0;D b;b.reserve(n+1);
  for(int i=0;i<n;i++){int v=a[i]+a[n-1-i]+c;b.push_back(v%10);c=v/10;}
  if(c)b.push_back(c);return b;
}
vector<int> group(const D&a){
  vector<int>x;
  for(int i=0;i<(int)a.size();i+=2)x.push_back(a[i]+(i+1<(int)a.size()?10*a[i+1]:0));
  return x;
}
struct Edit {int p,s;vector<int>A,B;bool ins;};
Edit compare(const D&a,const D&b){
  auto x=group(a),y=group(b);int p=0,s=0;
  while(p<(int)min(x.size(),y.size())&&x[p]==y[p])p++;
  while(s<(int)min(x.size(),y.size())-p&&x[x.size()-1-s]==y[y.size()-1-s])s++;
  vector<int>u(x.begin()+p,x.end()-s),v(y.begin()+p,y.end()-s);
  return {p,s,u,v,u.empty()&&v.size()==1&&v[0]==99};
}
string show(const vector<int>&v){
  string s;for(size_t i=0;i<v.size()&&i<6;i++){if(i)s+=":";s+=to_string(v[i]);}return s;
}
int main(int argc,char**argv){
  int lo=argc>1?atoi(argv[1]):15,hi=argc>2?atoi(argv[2]):450,ext=argc>3?atoi(argv[3]):80;
  if(lo<0||hi<lo||ext<0)return 2;
  cout<<"Q,first,first_old,first_new,first_prefix,first_suffix,repair_count,max_repair_run,repair_times\n";
  for(int q=lo;q<=hi;q++){
    auto a=seed(q),b=seed(q+1);int first=-1,rc=0,run=0,maxrun=0;
    Edit initial={};string times;
    for(int t=0;t<4*q+40+ext;t++){
      auto e=compare(a,b);
      if(first<0&&!e.ins){first=t;initial=e;}
      if(first>=0){
        if(t>first&&e.ins){
          rc++;run++;maxrun=max(maxrun,run);
          if(!times.empty())times+=":";times+=to_string(t);
        }else run=0;
        if(t==first+ext)break;
      }
      a=step(a);b=step(b);
    }
    if(first<0)return 3;
    cout<<q<<","<<first<<",\""<<show(initial.A)<<"\",\""<<show(initial.B)
        <<"\","<<initial.p<<","<<initial.s<<","<<rc<<","<<maxrun<<",\""<<times<<"\"\n";
  }
}
