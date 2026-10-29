#include <gmpxx.h>
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
using namespace std;
static uint64_t digest(const string& s){uint64_t h=1469598103934665603ULL;for(char c:s){h^=uint8_t(c);h*=1099511628211ULL;}return h;}
int main(int argc,char**argv){
 if(argc<3){cerr<<"usage x29_gmp seedfile steps [expected-trajectory]"<<endl;return 2;}
 ifstream file(argv[1]);string s;file>>s;mpz_class n(s,10);int steps=stoi(argv[2]);uint64_t trajectory=1469598103934665603ULL;
 for(int t=0;t<=steps;++t){s=n.get_str(10);string r=s;reverse(r.begin(),r.end());if(s==r){cerr<<"pal at "<<t<<endl;return 3;}trajectory=(trajectory^digest(s))*1099511628211ULL;
  if(t%5000==0||t==steps)cerr<<"gmp t="<<t<<" digits="<<s.size()<<" hash="<<hex<<digest(s)<<dec<<endl;
  if(t<steps)n+=mpz_class(r,10);
 }
 cout<<"GMP PASS t="<<steps<<" digits="<<s.size()<<" hash="<<hex<<digest(s)<<" trajectory="<<trajectory<<dec<<endl;
 if(argc>=4){uint64_t expected=stoull(argv[3],nullptr,16);if(trajectory!=expected){cerr<<"trajectory mismatch!"<<endl;return 4;}}
}
