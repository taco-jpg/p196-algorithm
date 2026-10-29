// Independently run ordinary decimal digit-list reverse-add for 20,000 steps.
// This file does not use the graph automaton or its carry equations.
#include <bits/stdc++.h>
using namespace std;
using U=unsigned char;
const string alphabet="0123456789ABCDEFGHI";
vector<array<U,8>> readCols(const string&file, string name){
 ifstream in(file);string s;while(getline(in,s)){istringstream ss(s);string lab,num;if(!(ss>>lab>>num)||lab!=name)continue;
  vector<array<U,8>> result;while(ss>>s){if(s.size()!=8)throw runtime_error("column size");array<U,8> a;for(int i=0;i<8;i++){auto pos=alphabet.find(s[i]);if(pos==string::npos)throw runtime_error("digit");a[i]=(U)pos;}result.push_back(a);}
  if(num!="n="+to_string(result.size()))throw runtime_error("column count");return result;
 }throw runtime_error("missing "+name);
}
int main(int argc,char**argv){
 if(argc<2){cerr<<"usage: replay witness.txt [steps=20000] [fib_letters=400] [guard=2048]\n";return 2;}
 const string file=argv[1];int T=argc>2?atoi(argv[2]):20000, M=argc>3?atoi(argv[3]):400, guard=argc>4?atoi(argv[4]):2048;
 auto prefix=readCols(file,"ROOTPATH"),a=readCols(file,"LOOPA"),b=readCols(file,"LOOPB");
 string style=argc>5?argv[5]:"fib";string w;
 if(style=="fib"||style=="fibmacro"){w="A";while((int)w.size()<M){string next;for(char c:w)next+=(c=='A'?"AB":"A");w=move(next);}w.resize(M);}
 else if(style=="thue"||style=="thuemacro"){for(int i=0;i<M;i++)w+=__builtin_parity((unsigned)i)?'B':'A';}
 else if(style=="allA"||style=="allB")w=string(M,style.back());
 else if(style=="alternating"){for(int i=0;i<M;i++)w+=i%2?'B':'A';}
 else throw runtime_error("style must be fib/thue/fibmacro/thuemacro/allA/allB/alternating");
 if(style=="fibmacro"||style=="thuemacro"){string z;for(char c:w)z+=(c=='A'?"AB":"BA");w=move(z);}
 vector<array<U,8>> cols=prefix;for(char c:w){auto &src=(c=='A'?a:b);cols.insert(cols.end(),src.begin(),src.end());}
 size_t h=cols.size();vector<U>d;d.reserve(2*h+T);
 for(auto c:cols)d.push_back(c[0]/2);
 for(size_t i=h;i-- >0;){U q=cols[i][0];d.push_back(q-q/2);}
 if(d.back()==0)throw runtime_error("leading zero");
 cout<<"SEED columns="<<h<<" decimal_digits="<<d.size()<<" word_style="<<style<<" letters="<<M<<" A="<<count(w.begin(),w.end(),'A')<<" B="<<count(w.begin(),w.end(),'B')<<"\n";
 for(int t=0;t<=T;t++){
  int good=0;size_t n=d.size();
  for(size_t i=0;i<h&&i<n/2;i++){
   if(int(d[i])+int(d[n-1-i])!=cols[i][t%8])break;
   good++;
  }
  if(good<guard){cerr<<"PAIR SHAPE LOST t="<<t<<" matching="<<good<<" guard="<<guard<<"\n";return 1;}
  if(t%1000==0||t==T)cout<<"CHECKPOINT step="<<t<<" n="<<n<<" matching_columns="<<good<<" matched_frac="<<double(good)/h<<"\n";
  bool palindrome=true;for(size_t i=0;i<n/2;i++)if(d[i]!=d[n-1-i]){palindrome=false;break;}
  if(palindrome){cerr<<"PALINDROME at step "<<t<<"\n";return 1;}
  if(t==T)break;
  vector<U>out(n+1);int carry=0;
  for(size_t i=0;i<n;i++){int x=d[i]+d[n-i-1]+carry;out[i]=x%10;carry=x/10;}
  if(carry){out[n]=1;}else out.pop_back();
  if(int(out.size())-int(n)!=(t%2==0?1:0)){cerr<<"WRONG OVERFLOW at "<<t<<"\n";return 1;}
  d.swap(out);
 }
 cout<<"PASS: "<<T<<" steps, no palindromes; all steps match non-periodic eight-phase pair-word prefix of at least "<<guard<<" columns; integer digits independently replayed\n";
}
