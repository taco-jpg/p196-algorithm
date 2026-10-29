// Independent ordinary-big-integer checker: no pairword arithmetic advances N.
// g++ -std=c++17 -O3 -Wall -Wextra -Werror verify_gmp.cpp -lgmpxx -lgmp -o verify_gmp
#include <gmpxx.h>
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
static vector<array<int,8>> parse(const string& s) {
  vector<array<int,8>> out; size_t pos=0;
  while ((pos=s.find('[',pos))!=string::npos) {
    size_t end=s.find(']',pos); if(end==string::npos) throw runtime_error("missing ]");
    string b=s.substr(pos+1,end-pos-1); array<int,8> row{}; size_t off=0;
    for(int i=0;i<8;i++) {
      size_t nxt=b.find(',',off);
      if(i<7 && nxt==string::npos)throw runtime_error("short row");
      row[i]=stoi(b.substr(off,nxt==string::npos?string::npos:nxt-off));
      if(row[i]<0||row[i]>18)throw runtime_error("bad coefficient");
      off=nxt+1;
    }
    out.push_back(row); pos=end+1;
  }
  return out;
}
static uint64_t fnv(const string&s) {
  uint64_t h=14695981039346656037ULL;
  for(unsigned char c:s){h^=c;h*=1099511628211ULL;}return h;
}
int main(int argc,char**argv) {
 try {
  if(argc!=5)throw runtime_error("usage: verify_gmp p8_rec0_rows.txt copies steps watch");
  ifstream in(argv[1]);if(!in)throw runtime_error("missing data file");
  string a,b;getline(in,a);getline(in,b);
  auto path=parse(a),cyc=parse(b);
  if(path.size()!=39||cyc.size()!=20)throw runtime_error("bad row counts");
  int copies=stoi(argv[2]),steps=stoi(argv[3]),watch=stoi(argv[4]);
  if(copies<0||steps<0||watch<1||watch>39)throw runtime_error("bad arguments");
  vector<int> half;for(auto &r:path)half.push_back(r[0]);
  for(int z=0;z<copies;z++)for(auto &r:cyc)half.push_back(r[0]);
  int n=2*int(half.size());string s(n,'0');
  for(int i=0;i<int(half.size());i++) {
    int lo=min(9,half[i]),hi=half[i]-lo;
    s[n-1-i]=char('0'+lo);s[i]=char('0'+hi);
  }
  if(s[0]=='0')throw runtime_error("leading zero");
  mpz_class value(s,10);int expected_length=n;
  for(int t=0;t<=steps;t++){
    s=value.get_str(10);
    if(int(s.size())!=expected_length)throw runtime_error("length mismatch step "+to_string(t));
    if(equal(s.begin(),s.begin()+s.size()/2,s.rbegin()))throw runtime_error("PALINDROME step "+to_string(t));
    for(int i=0;i<watch;i++) {
      int q=(s[i]-'0')+(s[s.size()-1-i]-'0');
      if(q!=path[i][t%8])throw runtime_error("BULK mismatch step "+to_string(t)+" col "+to_string(i)+" got "+to_string(q)+" expected "+to_string(path[i][t%8]));
    }
    // Even steps: outer pair 17; odd steps: leading/trailing digits 1 and 7.
    if((t%2==0 && ((s[0]-'0')+(s.back()-'0')!=17))||
       (t%2==1 && (s[0]!='1'||s.back()!='7')))
      throw runtime_error("outer witness failed at "+to_string(t));
    if(t==0||t==1000||t==5000||t==10000||t==steps)
      cout<<"step="<<t<<" digits="<<s.size()<<" fnv64="<<hex<<fnv(s)<<dec
          <<" first="<<s.substr(0,12)<<" last="<<s.substr(s.size()-12)<<"\n";
    if(t==steps)break;
    string rev=s;reverse(rev.begin(),rev.end());
    mpz_class reversed(rev,10);value+=reversed;
    expected_length+=(t%2==0)?1:0;
  }
  cout<<"PASS base=10 steps="<<steps<<" copies="<<copies<<" watch="<<watch
      <<" initial_digits="<<n<<" final_digits="<<expected_length<<"\n";
  return 0;
 }catch(const exception&e){cerr<<"FAIL "<<e.what()<<"\n";return 1;}
}
