// Independent full-GMP integer RAA vs two-ended packet prediction, every step.
// g++ -std=c++17 -O2 -Wall -Wextra replay_gmp.cpp -lgmpxx -lgmp -lcrypto -o replay_gmp
#include <gmpxx.h>
#include <openssl/sha.h>
#include <algorithm>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
using namespace std;

string reverse_copy(string a) { reverse(a.begin(),a.end()); return a; }
mpz_class from_decimal(const string &a) { return mpz_class(a.c_str(),10); }
string sha256(const string &s) {
    unsigned char buf[SHA256_DIGEST_LENGTH]; SHA256((const unsigned char*)s.data(),s.size(),buf);
    ostringstream os; for(unsigned char c:buf)os<<hex<<setfill('0')<<setw(2)<<(int)c;
    return os.str();
}
int main(int argc,char**argv) {
    if(argc!=5) { cerr<<"usage: replay_gmp PREFIX SUFFIX Q STEPS\n";return 2; }
    string prefix=argv[1],suffix=argv[2];
    long long q=stoll(argv[3]); int steps=stoi(argv[4]);
    if(prefix.empty()||suffix.empty()||prefix[0]=='0'||suffix[0]=='0'||suffix.back()=='0'||q<0||steps<1) return 2;
    string seed=prefix+string(q,'0')+suffix;
    mpz_class n=from_decimal(seed);
    mpz_class A=from_decimal(prefix)*from_decimal("1"+string(suffix.size(),'0'));
    mpz_class B=from_decimal(suffix);
    long long shift=0,required_q=0,min_gap=1000000000;
    for(int t=0;t<steps;t++) {
        string sa=A.get_str(),sb=B.get_str(),actual=n.get_str();
        long long e=q+shift,gap=e-(long long)sb.size();
        if(gap<0) { cerr<<"OVERLAP step "<<t<<" gap="<<gap<<"\n";return 3; }
        min_gap=min(min_gap,gap);
        required_q=max(required_q,(long long)sb.size()-shift);
        string expected=sa+string(gap,'0')+sb;
        if(actual!=expected) {cerr<<"MISMATCH step "<<t<<"\n";return 4;}
        if(actual==reverse_copy(actual)) {cerr<<"PALINDROME step "<<t<<"\n";return 5;}
        if(t%1000==0||t==steps-1)
            cout<<t<<" "<<sa.size()<<" "<<sb.size()<<" "<<shift<<" "<<gap<<" "
                <<actual.size()<<" "<<sha256(actual)<<"\n";
        // Actual orbit: full integer reverse-and-add; not predicted via packets.
        mpz_class reverse_n=from_decimal(reverse_copy(actual));
        n+=reverse_n;
        // Separately predict the next complete word via the packet recurrence.
        long long d=(long long)sa.size()-(long long)sb.size();
        mpz_class ra=from_decimal(reverse_copy(sa)),rb=from_decimal(reverse_copy(sb));
        if(d>=0) A+=rb*from_decimal("1"+string(d,'0'));
        else {A=A*from_decimal("1"+string(-d,'0'))+rb;shift+=d;}
        B+=ra;
    }
    cout<<"PASS "<<steps<<" steps min_gap="<<min_gap<<" required_q="<<required_q<<"\n";
}
