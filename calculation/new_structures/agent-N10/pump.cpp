// Exact pairword insertion conjugacy on two independently evolved REAL decimal integers.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
#include "phase.h"
using namespace std;
vector<unsigned char> seed(int k,int core){
    vector<int> lo(B0.begin(),B0.end());
    for(int i=0;i<k;i++)lo.insert(lo.end(),W0.begin(),W0.end());
    if(core==1){lo.push_back(0);lo.push_back(18);}
    else if(core==2){lo.push_back(2);lo.push_back(4);}
    else if(core==3){lo.push_back(9);lo.push_back(6);}
    else if(core!=0){cerr<<"bad core\n";exit(2);}
    vector<unsigned char>d(lo.size()*2);
    for(size_t i=0;i<lo.size();i++){
        d[i]=lo[i]/2;
        d[d.size()-1-i]=lo[i]-lo[i]/2;
    }
    return d;
}
void addrev(vector<unsigned char>&d){
    vector<unsigned char>n(d.size()+1);int c=0;
    for(size_t i=0,j=d.size()-1;i<d.size();i++,j--){
        int a=d[i]+d[j]+c;
        n[i]=a%10;c=a/10;
    }
    if(c)n.back()=c;else n.pop_back();
    d.swap(n);
}
int main(int argc,char**argv){
    const int k=argc>1?atoi(argv[1]):300,
        T=argc>2?atoi(argv[2]):20000,
        core=argc>3?atoi(argv[3]):0;
    if(k<1||T<1||core<0||core>3)return 2;
    auto a=seed(k,core),b=seed(k+1,core);
    uint64_t verified=0;
    for(int t=0;t<=T;t++){
        if(b.size()!=a.size()+40){cerr<<"len at "<<t<<'\n';return 2;}
        const auto& w=PHASE_W[t%8];
        const size_t n=a.size(),m=b.size();
        // Full pairword of b equals that of a after inserting W_t at
        // position 39 and reverse(W_t) immediately before the last 39 sites.
        for(size_t i=0;i<m;i++){
            int exp;
            if(i<39)exp=a[i]+a[n-1-i];
            else if(i<59)exp=w[i-39];
            else if(i<n-19){size_t j=i-20;exp=a[j]+a[n-1-j];}
            else if(i<n+1){exp=w[19-(i-(n-19))];}
            else{size_t j=i-40;exp=a[j]+a[n-1-j];}
            int got=b[i]+b[m-1-i];
            if(got!=exp){
                cerr<<"MISMATCH t="<<t<<" i="<<i<<" got="<<got
                    <<" exp="<<exp<<" size="<<m<<"\n";return 3;
            }
        }
        if(t==0||t==1||t==100||t==1000||t==5000||t==10000||t==15000||t==20000)
            cout<<"conjugacy t="<<t<<" digit_lengths="<<n<<","<<m
                <<" exact_pairs="<<m<<"\n";
        verified+=m;
        if(t<T){addrev(a);addrev(b);}
    }
    cout<<"PASS complete-pairword pump k="<<k<<" k+1="<<k+1
        <<" core="<<core<<" steps="<<T
        <<" compared_coefficients="<<verified<<"\n";
    return 0;
}
