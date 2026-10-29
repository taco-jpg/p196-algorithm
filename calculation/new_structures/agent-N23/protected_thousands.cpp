// Independent base-1000 limb big integers, explicit ordinary decimal string reversal.
// No use of digit-vector oracle or symbolic transducer.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
using Big=vector<uint16_t>;
static Big parse(const string& s){
 Big a;a.reserve((s.size()+2)/3);
 for(int j=(int)s.size();j>0;j-=3){int k=max(0,j-3),v=0;for(int i=k;i<j;i++)v=10*v+s[i]-'0';a.push_back(v);}
 while(a.size()>1&&a.back()==0)a.pop_back();return a;
}
static string render(const Big& x){
 string s=to_string(x.back());s.reserve(3*x.size());
 for(int i=(int)x.size()-2;i>=0;i--){int v=x[i];s.push_back(char('0'+v/100));s.push_back(char('0'+v/10%10));s.push_back(char('0'+v%10));}
 return s;
}
static Big add(const Big&a,const Big&b){
 int n=max(a.size(),b.size()),carry=0;Big c;c.reserve(n+1);
 for(int i=0;i<n;i++){int z=carry+(i<(int)a.size()?a[i]:0)+(i<(int)b.size()?b[i]:0);c.push_back(z%1000);carry=z/1000;}
 if(carry)c.push_back(carry);return c;
}
int main(int argc,char**argv){
 int Q=(argc>1)?atoi(argv[1]):30037,T=(argc>2)?atoi(argv[2]):100000;
 Big n=parse("12"+string(2*Q,'9')+"34");
 int minimum=INT32_MAX,last=0; uint64_t check=0;
 for(int t=0;t<=T;t++){
  string s=render(n),r=s;reverse(r.begin(),r.end());
  if(s==r){cerr<<"palindrome t="<<t<<"\n";return 2;}
  int l=((int)s.size()-1)/2,h=((int)s.size())/2,c=0;
  while(l>=0 && h<(int)s.size() && s[l]=='9'&&s[h]=='9'){c+=l==h?1:2;l--;h++;}
  if(c<2){cerr<<"band exhausted t="<<t<<" core="<<c<<"\n";return 3;}
  minimum=min(minimum,c);
  if(t==T){last=c;for(unsigned char ch:s)check=(check*131+ch)%1000000007ULL;
   cout<<"PASS independent base1000 limbs steps="<<T<<" Q="<<Q<<" lastdigits="<<s.size()<<" central_min="<<minimum<<" central_last="<<last<<" hash="<<check<<"\n";break;}
  n=add(n,parse(r));
 }
}
