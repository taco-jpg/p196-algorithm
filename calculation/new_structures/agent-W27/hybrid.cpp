// W27: central-9 insertion lift of the 196 shell. C++17, no external libraries.
// Reproduce: c++ -O3 -std=c++17 hybrid.cpp -o hybrid && ./hybrid 6005 20000
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
using Digits=vector<uint8_t>;
static Digits make_digits(int q){
 string s="196"+string(2*q,'9')+"196";
 Digits d;for(auto it=s.rbegin();it!=s.rend();++it)d.push_back(uint8_t(*it-'0'));return d;
}
static void digit_step(Digits &d,Digits &tmp){
 size_t n=d.size();tmp.resize(n+1);int carry=0;
 for(size_t i=0;i<n;i++){int s=int(d[i])+int(d[n-i-1])+carry;tmp[i]=uint8_t(s%10);carry=s/10;}
 if(!carry)tmp.pop_back();else tmp[n]=uint8_t(carry);
 d.swap(tmp);
}
// Independent MSB-first literal decimal-string addition, not digit_step.
static void string_step(string &s){
 string rev=s;reverse(rev.begin(),rev.end());string out(s.size()+1,'0');int carry=0;
 for(int i=int(s.size())-1;i>=0;i--){int x=(s[i]-'0')+(rev[i]-'0')+carry;out[i+1]=char('0'+x%10);carry=x/10;}
 if(carry)out[0]=char('0'+carry);else out.erase(out.begin());s.swap(out);
}
static bool palindrome(const Digits &d){
 for(size_t i=0,n=d.size();i<n/2;i++)if(d[i]!=d[n-1-i])return false;return true;
}
static int centre9(const Digits &d){
 int n=int(d.size()),k=n/2,l=k-1,r=k;
 while(l>=0&&d[l]==9)--l;while(r<n&&d[r]==9)++r;return r-l-1;
}
static int central18(const Digits &d){
 int n=int(d.size()),k=n/2,ans=0;
 for(int i=k-1;i>=0;i--){if(d[i]+d[n-1-i]!=18)break;ans+=2;}
 if(n%2&&d[k]==9)ans++;
 return ans;
}
static void assert_same(const Digits &d,const string &s,int t){
 if(d.size()!=s.size()){cerr<<"ENGINE_LENGTH_MISMATCH t="<<t<<"\n";exit(10);}
 for(size_t i=0;i<d.size();i++)if(int(d[i])!=s[s.size()-1-i]-'0'){
  cerr<<"ENGINE_DIGIT_MISMATCH t="<<t<<" i="<<i<<"\n";exit(11);
 }
}
static void assert_insert(const Digits &a,const Digits &b,int t){
 int n=int(a.size()),mid=n/2;
 if(int(b.size())!=n+2 || b[mid]!=9 || b[mid+1]!=9){
  cerr<<"INSERT_LENGTH t="<<t<<"\n";exit(12);
 }
 for(int i=0;i<n;i++)if(a[i]!=b[i+(i>=mid?2:0)]){
  cerr<<"INSERT_DIGIT_MISMATCH t="<<t<<" i="<<i<<"\n";exit(13);
 }
}
static uint64_t fnv(const Digits &d){
 uint64_t h=1469598103934665603ULL;
 for(uint8_t c:d){h^=c;h*=1099511628211ULL;}
 return h;
}
int main(int argc,char**argv){
 int q=argc>1?atoi(argv[1]):6005,T=argc>2?atoi(argv[2]):20000;
 if(q<3||T<1)return 2;
 Digits a=make_digits(q),b=make_digits(q+1),ta,tb;
 string s="196"+string(2*q,'9')+"196";
 int min9=INT32_MAX,min18=INT32_MAX,gamma=0;
 for(int t=0;t<=T;t++){
  assert_same(a,s,t);assert_insert(a,b,t);
  if(palindrome(a)||palindrome(b)){cerr<<"PALINDROME t="<<t<<"\n";return 3;}
  int c=centre9(a),p=central18(a);
  if(c<min9)min9=c;
  if(p<min18)min18=p;
  if(c<4){cerr<<"CENTRE_TOO_SHORT t="<<t<<" c="<<c<<"\n";return 4;}
  if(t%5000==0||t==T)
   cout<<"CHECK t="<<t<<" length="<<a.size()<<" centre9="<<c
       <<" pair18="<<p<<" fnv64="<<fnv(a)<<"\n";
  if(t==T)break;
  int n=int(a.size());digit_step(a,ta);digit_step(b,tb);string_step(s);
  gamma+=int(a.size())-n;
 }
 cout<<"PASS q="<<q<<" steps="<<T<<" min_centre9="<<min9
     <<" min_pair18="<<min18<<" overflow="<<gamma
     <<" final_length="<<a.size()<<" final_hash="<<fnv(a)<<"\n";
}