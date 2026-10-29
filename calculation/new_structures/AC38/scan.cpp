// AC38: exact endpoint-only phase-5 J6 census, no strict W9 pruning.
// g++ -O3 -std=c++17 -Wall -Wextra scan.cpp -o /tmp/ac38scan
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <vector>
using namespace std;
using V=vector<int>;
struct Phase{V B,W;};
Phase read_p5(const string& file){
    ifstream f(file);if(!f)throw runtime_error("missing lattice file");
    string line;vector<V> rows;
    while(getline(f,line)){
        if(line.empty())continue;
        istringstream ss(line);V row;int v;
        while(ss>>v)row.push_back(v);
        rows.push_back(row);
    }
    if(rows.size()!=38||rows[0]!=V({12,34,9,10}))
        throw runtime_error("unexpected p12/m9 format");
    return {rows.at(31),rows.at(7)};
}
V make_word(const Phase& ph,const V& J,const V& U,const V& C,int q,int k){
    V h=ph.B;
    for(int i=0;i<q;i++)h.insert(h.end(),ph.W.begin(),ph.W.end());
    h.insert(h.end(),J.begin(),J.end());
    for(int i=0;i<k;i++)h.insert(h.end(),U.begin(),U.end());
    V p=h;p.insert(p.end(),C.begin(),C.end());
    p.insert(p.end(),h.rbegin(),h.rend());return p;
}
int step(V& p){
    V d;d.reserve(p.size()+1);int carry=0;
    for(int x:p){int v=x+carry;d.push_back(v%10);carry=v/10;}
    if(carry)d.push_back(carry);
    int n=d.size();p.resize(n);
    for(int i=0;i<n;i++)p[i]=d[i]+d[n-i-1];
    return carry;
}
int first_mismatch(const V&a,const V&b){
    for(int i=0;i<(int)min(a.size(),b.size());i++)
        if(a[i]!=b[i])return i;
    return a.size()==b.size()?-1:(int)min(a.size(),b.size());
}
int main(int argc,char**argv){
    if(argc<2){cerr<<"scan root_file [J0] [suffix-pair-count]\n";return 2;}
    auto ph=read_p5(argv[1]);
    int j0=argc>=3?stoi(argv[2]):0,limit=argc>=4?stoi(argv[3]):361;
    if(j0<0||j0>18||limit<1||limit>361)return 2;
    long long tested=0,returned=0,band_match=0,growth_fail=0,clock_fail=0;
    map<int,long long> hist;
    for(int a=0;a<=18;a+=2){
        array<int,3> b={9,a,18-a};
        for(int rot=0;rot<3;rot++){
            V U={b[rot],b[(rot+1)%3],b[(rot+2)%3]};
            for(int ci=0;ci<2;ci++){
                V C=ci==0?V({4,4}):V({4,14,4});
                for(int code=0;code<limit;code++){
                    V J={j0,code/19,code%19,0,0,0};
                    V p=make_word(ph,J,U,C,14,100);
                    V target=make_word(ph,J,U,C,14,105);
                    int bits=0;string clock;
                    for(int t=0;t<120;t++){
                        int g=step(p);bits+=g;clock+=g?'1':'0';
                    }
                    if(bits!=30||p.size()!=target.size())growth_fail++;
                    string want;for(int t=0;t<120;t++)want+=(t%4==3?'1':'0');
                    if(clock!=want)clock_fail++;
                    int bad=first_mismatch(p,target);
                    if(bad<0)returned++;
                    if(equal(target.begin(),target.begin()+34+9*14,p.begin()))
                        band_match++;
                    hist[bad]++;tested++;
                }
            }
        }
    }
    cout<<"phase=5 Jlen=6 J0="<<j0<<" suffix_code=0.."<<limit-1
        <<" U=30 C=2,3 tested="<<tested<<" returns="<<returned
        <<" B+W_matches="<<band_match<<" growth_fail="<<growth_fail
        <<" clock_fail="<<clock_fail<<"\nfirst_mismatch:";
    for(auto [idx,n]:hist)cout<<" "<<idx<<":"<<n;
    cout<<"\n";
    return growth_fail||clock_fail?1:0;
}
