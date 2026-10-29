// Independent GMP integer vs grade-school decimal vector replay. No rotation code.
#include <gmpxx.h>
#include <bits/stdc++.h>
using namespace std;
static vector<unsigned char> parse(string s) {
    vector<unsigned char>d;
    for(int i=(int)s.size()-1;i>=0;--i) {
        if(s[i]<'0'||s[i]>'9')throw runtime_error("invalid seed");
        d.push_back(s[i]-'0');
    }
    return d;
}
static string decimal(const vector<unsigned char>&d) {
    string s;for(int i=(int)d.size()-1;i>=0;--i)s.push_back(char('0'+d[i]));
    return s;
}
static vector<unsigned char> school(const vector<unsigned char>&d) {
    int c=0;vector<unsigned char>out;out.reserve(d.size()+1);
    for(size_t i=0;i<d.size();++i) {
        int v=d[i]+d[d.size()-1-i]+c;
        out.push_back(v%10);c=v/10;
    }
    if(c)out.push_back(c);
    while(out.size()>1&&out.back()==0)out.pop_back();
    return out;
}
static bool pal(const vector<unsigned char>&d) {
    for(size_t i=0;i<d.size()/2;++i)
        if(d[i]!=d[d.size()-1-i])return false;
    return true;
}
int main(int argc,char**argv) {
    if(argc!=3){cerr<<"usage: replay SEED_FILE STEPS\n";return 2;}
    ifstream f(argv[1]);string seed;getline(f,seed);
    int steps=stoi(argv[2]);
    vector<unsigned char>d=parse(seed);
    mpz_class n(seed,10);
    int firstpal=-1,mismatches=0;
    uint64_t h=1469598103934665603ull;
    for(int t=0;t<=steps;++t) {
        string x=n.get_str();
        if(x!=decimal(d)){cerr<<"integer/schoolbook mismatch at "<<t<<"\n";return 3;}
        if(pal(d)&&firstpal<0)firstpal=t;
        for(auto v:d){h^=v;h*=1099511628211ull;}
        if(t==steps)break;
        string r=x;reverse(r.begin(),r.end());
        n+=mpz_class(r,10);d=school(d);
    }
    cout<<"steps="<<steps<<" first_pal="<<firstpal
        <<" final_digits="<<d.size()<<" hash="<<h
        <<" independent_mismatches="<<mismatches<<"\n";
    return firstpal>=0?4:0;
}
