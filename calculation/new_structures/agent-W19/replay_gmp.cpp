// Independent ordinary GNU GMP decimal reversal and addition.
#include <gmpxx.h>
#include <bits/stdc++.h>
using namespace std;
static vector<array<int,8>> parse(const string&s){
 vector<array<int,8>> rows;size_t i=0;
 while((i=s.find('[',i))!=string::npos){
  size_t j=s.find(']',i);if(j==string::npos)throw runtime_error("bad phase");
  string x=s.substr(i+1,j-i-1);stringstream ss(x);array<int,8> row{};string value;
  for(int k=0;k<8;k++){if(!getline(ss,value,','))throw runtime_error("bad row");row[k]=stoi(value);}
  rows.push_back(row);i=j+1;
 }
 return rows;
}
static uint64_t fnv_lsd(const string&s){
 uint64_t h=14695981039346656037ULL;
 for(auto it=s.rbegin();it!=s.rend();++it){h^=(uint8_t)(*it-'0');h*=1099511628211ULL;}
 return h;
}
static mpz_class read_number(const string&name){
 ifstream f(name);if(!f)throw runtime_error("cannot read seed");
 string s;getline(f,s);
 if(s.empty()||s[0]=='0')throw runtime_error("invalid decimal seed");
 for(char ch:s)if(ch<'0'||ch>'9')throw runtime_error("seed is not decimal");
 return mpz_class(s,10);
}
static mpz_class reverse_add(const mpz_class&n){
 string s=n.get_str(10);reverse(s.begin(),s.end());return n+mpz_class(s,10);
}
int main(int argc,char**argv){try{
 if(argc!=5)throw runtime_error("usage: replay_gmp phase.txt seed0.txt seed1.txt steps");
 ifstream in(argv[1]);string line0,line1;getline(in,line0);getline(in,line1);
 auto root=parse(line0),bulk=parse(line1);
 if(root.size()!=39||bulk.size()!=20)throw runtime_error("bad phase dimensions");
 int steps=stoi(argv[4]);if(steps<3)throw runtime_error("steps>=3");
 mpz_class n=read_number(argv[2]);mpz_class other=read_number(argv[3]);
 auto original_len=n.get_str(10).size();
 if(other.get_str(10).size()!=original_len)throw runtime_error("seed length mismatch");
 for(int t=0;t<=steps;t++){
  string s=n.get_str(10);size_t len=s.size();
  if(len!=original_len+(t+1)/2)throw runtime_error("length mismatch");
  if(equal(s.begin(),s.begin()+len/2,s.rbegin()))throw runtime_error("palindrome");
  size_t half=len/2,j=0;
  for(;j<half;j++){
   int want=j<39?root[j][t%8]:bulk[(j-39)%20][t%8];
   if(s[j]-'0'+s[len-1-j]-'0'!=want)break;
  }
  if(j<200)throw runtime_error("phase guard lost");
  if(t==0||t==1000||t==10000||t==steps)
   cout<<"GMP_CHECKPOINT t="<<t<<" digits="<<len<<" first_bad="<<j
       <<" fnv64="<<hex<<fnv_lsd(s)<<dec<<"\n";
  if(t==3){if(n!=other)throw runtime_error("third integer did not coalesce");
   cout<<"GMP_THREE_STEP_COALESCENCE true\n";}
  if(t<steps){n=reverse_add(n);if(t<3)other=reverse_add(other);}
 }
 cout<<"GMP_LONG_PASS steps="<<steps<<" palindromes=0\n";
 return 0;
}catch(const exception&e){cerr<<"FAIL "<<e.what()<<"\n";return 1;}}
