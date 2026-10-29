// X09 genuine decimal reverse-and-add replay, independently written.
// g++ -O3 -std=c++17 orbit.cpp -o orbit && ./orbit 100000 ./scratch
#include <bits/stdc++.h>
using namespace std;
static vector<uint8_t> next_digits(const vector<uint8_t>& a){
    int carry=0;vector<uint8_t> b;b.reserve(a.size()+1);
    for(size_t i=0,n=a.size();i<n;i++){
        int s=a[i]+a[n-1-i]+carry;
        b.push_back(s%10);carry=s/10;
    }
    if(carry)b.push_back(carry);
    return b;
}
static bool is_pal(const vector<uint8_t>& a){
    for(size_t i=0;i<a.size()/2;i++)if(a[i]!=a[a.size()-1-i])return false;
    return true;
}
static void snapshot(const vector<uint8_t>& a,int t,const string& dir){
    ofstream out(dir+"/t"+to_string(t)+".txt");
    if(!out)throw runtime_error("cannot open snapshot");
    out<<"time="<<t<<" digits="<<a.size()<<"\n";
    for(auto i=a.rbegin();i!=a.rend();i++)out<<int(*i);
    out<<"\n";
    const char *code="0123456789ABCDEFGHI";
    for(size_t i=0;i<a.size();i++)out<<code[a[i]+a[a.size()-1-i]];
    out<<"\n";
}
int main(int argc,char**argv){
    if(argc!=3){cerr<<"Usage: orbit STEPS OUTPUT_DIRECTORY\n";return 2;}
    int steps=stoi(argv[1]);string dir=argv[2];
    vector<uint8_t> digits={6,9,1};
    set<int> saved={1000,2000};
    for(int t:{10000,20000,40000,80000,100000})for(int d:{-88,-8,0,8,88})saved.insert(t+d);
    int pals=0;
    for(int t=0;t<=steps;t++){
        if(saved.count(t))snapshot(digits,t,dir);
        pals+=is_pal(digits);
        if(t%10000==0||t==steps)
            cout<<"t="<<t<<" digits="<<digits.size()<<" palindromes="<<pals<<"\n";
        if(t!=steps)digits=next_digits(digits);
    }
    return pals?1:0;
}
