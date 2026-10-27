// Independent exact exterior B-graph for the one-neutral-band checker, base 10.
// Build: c++ -O3 -std=c++17 b_width_graph.cpp -o b_width_graph
// Run:   ./b_width_graph 5
// Full states: 19^K canonical B words (B empty or B[0]!=0, entries 0..18).
// All trailing-nine trims are tried. No center is assumed or searched.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <queue>
#include <vector>
#include <cstdlib>
using namespace std;
using U = uint32_t;

U pow19(int n) {
    U v=1;
    for(int i=0;i<n;i++) v*=19;
    return v;
}

struct Transition { U dest; int u; int g; };

// Every word is encoded in base 19 with B[0] as the most significant digit.
// The empty word is encoded as 0. Hence length<=K is exactly IDs [0,19^K).
vector<Transition> outgoing(U code, int K) {
    int B[16], n=0;
    U t=code;
    while(t) { B[n++]=t%19; t/=19; }
    reverse(B,B+n);
    int D[16], R[16], rd[17], carry=0;
    for(int j=0;j<n;j++){
        const int a=B[j]+carry;
        D[j]=a%10; carry=a/10;
    }
    const int e=carry;
    carry=1-e;  // Hyp forces the center terminal carry to complement e.
    for(int j=0;j<n;j++){
        const int a=B[n-1-j]+carry;
        R[j]=a%10; carry=a/10;
    }
    const int g=carry;
    const int m=n+g;
    if(g){
        if(n==0) rd[0]=10;
        else rd[0]=D[0]+1;
        for(int j=1;j<n;j++) rd[j]=D[j]+R[n-j];
        if(n>0) rd[n]=9*(1-e)+R[0];
    }else{
        for(int j=0;j<n;j++) rd[j]=D[j]+R[n-1-j];
    }
    int suffix=0;
    for(int j=m-1;j>=0 && rd[j]==9;j--) suffix++;
    vector<Transition> edges;
    for(int u=0;u<=suffix;u++){
        int remain=m-u;
        if(remain>K || (remain && rd[0]==0)) continue;
        U target=0;
        bool valid=true;
        for(int j=0;j<remain;j++){
            if(rd[j]<0 || rd[j]>18) { valid=false; break; }
            target=19*target + rd[j];
        }
        if(valid) edges.push_back({target,u,g});
    }
    return edges;
}

int main(int argc,char**argv){
    const int K=argc>=2?atoi(argv[1]):4;
    if(K<1 || K>7) { cerr<<"Allowed K=1..7\n"; return 2; }
    const U n=pow19(K);
    vector<uint8_t> indeg(n,0);
    uint64_t edgeCount=0, trim[9]={0}, overflows[2]={0};
    for(U i=0;i<n;i++){
        for(auto tr:outgoing(i,K)){
            if(indeg[tr.dest]==255) { cerr<<"ERROR: indegree would overflow uint8_t\n"; return 3; }
            indeg[tr.dest]++;edgeCount++;trim[tr.u]++;overflows[tr.g]++;
        }
    }
    U maxInDegree=0;
    uint64_t zeroDegree=0;
    for(auto d:indeg){ maxInDegree=max(maxInDegree,(U)d); if(d==0) zeroDegree++; }
    // In-degree peeling: a finite digraph has a directed cycle iff any node
    // remains after repeatedly deleting vertices of indegree zero.
    queue<U> ready;
    for(U i=0;i<n;i++) if(indeg[i]==0) ready.push(i);
    uint64_t removed=0;
    while(!ready.empty()){
        const U u=ready.front();ready.pop(); removed++;
        for(auto tr:outgoing(u,K)){
            uint8_t &deg=indeg[tr.dest];
            if(--deg==0)ready.push(tr.dest);
        }
    }
    cout<<"K="<<K<<" states="<<n<<" edges="<<edgeCount
        <<" gamma0="<<overflows[0]<<" gamma1="<<overflows[1]
        <<" trimmed=";
    for(int j=0;j<=K;j++) cout<<(j?",":"")<<j<<":"<<trim[j];
    cout<<" max_indegree="<<maxInDegree<<" indegree_zero="<<zeroDegree<<" peeled="<<removed<<" residual="<<(n-removed)
        <<" cycle="<<(removed<n)<<"\n";
}