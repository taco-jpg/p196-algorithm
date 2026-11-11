// dawg.cpp: minimal acyclic DFA size (per level) of each layer of a dumped level file, bottom-to-top and top-to-bottom cell order.
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <algorithm>
#include <map>
#include <numeric>
#include <vector>
using namespace std;
typedef uint8_t u8; typedef uint32_t u32; typedef uint64_t u64;
int T,K;
struct Layer{int t,j,par,n; vector<u8> c;};
// compute number of minimal DFA nodes at each depth for words list sorted lex order (words as bytes of length K)
static vector<u64> dawg(const vector<u8>& cells, int n, int K, bool rev, vector<u64>* outdeg=nullptr){
  vector<u8> a(cells);
  if(rev){ for(int i=0;i<n;i++){ reverse(a.begin()+i*K, a.begin()+(i+1)*K);} 
    vector<u32> idx(n); iota(idx.begin(), idx.end(),0);
    sort(idx.begin(), idx.end(), [&](u32 x,u32 y){return memcmp(&a[x*(size_t)K],&a[y*(size_t)K],K)<0;});
    vector<u8> b(a.size()); for(int i=0;i<n;i++) memcpy(&b[i*(size_t)K],&a[idx[i]*(size_t)K],K); a.swap(b);
  }
  // node at depth d: ids; process levels from deepest
  vector<u64> counts(K+1,0);
  // for each word position i, for each depth d: class id of subtree rooted at prefix of length d of word i (only for first occurrences)
  // bottom-up: level K: single leaf id 0
  vector<u32> cls(n,0); counts[K]=n?1:0;
  // prefix starts: at depth d, group consecutive words with same prefix of length d
  for(int d=K-1;d>=0;d--){
    // groups of words sharing prefix length d: children at depth d+1 grouped by letter
    map<vector<u32>,u32> mp; // use hashing via vector key
    vector<u32> ncls; // class per group
    vector<u32> groupStart;
    int i=0;
    vector<u32> ncl(n,0);
    while(i<n){
      int j=i;
      while(j<n && memcmp(&a[i*(size_t)K],&a[j*(size_t)K],d)==0) j++;
      // children
      vector<u32> key; 
      int p=i;
      while(p<j){ int q=p; while(q<j && a[q*(size_t)K+d]==a[p*(size_t)K+d]) q++; key.push_back(a[p*(size_t)K+d]); key.push_back(cls[p]); p=q; }
      auto it=mp.find(key); u32 id;
      if(it==mp.end()){ id=mp.size(); mp[key]=id; } else id=it->second;
      for(int k=i;k<j;k++) ncl[k]=id;
      i=j;
    }
    counts[d]=mp.size();
    if(outdeg && d<(int)outdeg->size()){ }
    cls.swap(ncl);
  }
  return counts;
}
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"rb"); int hdr[2]; fread(hdr,sizeof(int),2,f); T=hdr[0];K=hdr[1];
  vector<Layer> L(T);
  for(int l=0;l<T;l++){ int rec[4]; fread(rec,sizeof(int),4,f); L[l].t=rec[0];L[l].j=rec[1];L[l].par=rec[2];L[l].n=rec[3]; L[l].c.resize((size_t)L[l].n*K); fread(L[l].c.data(),1,L[l].c.size(),f);}    
  fclose(f);
  int step = argc>2? atoi(argv[2]): 16;
  u64 tot[2]={0,0}; vector<u64> sum0(K+1,0), sum1(K+1,0); u64 ntot=0;
  for(int l=0;l<T;l++){
    ntot+=L[l].n;
    auto c0=dawg(L[l].c,L[l].n,K,false); auto c1=dawg(L[l].c,L[l].n,K,true);
    for(int d=0;d<=K;d++){ tot[0]+=c0[d]; tot[1]+=c1[d]; sum0[d]+=c0[d]; sum1[d]+=c1[d]; }
    if(l%step==0){
      printf("layer %d (t=%d j=%d par=%d) n=%d\n bottom-to-top:",l,L[l].t,L[l].j,L[l].par,L[l].n);
      for(int d=0;d<=K;d++) printf(" %llu",(unsigned long long)c0[d]);
      printf("\n top-to-bottom:"); for(int d=0;d<=K;d++) printf(" %llu",(unsigned long long)c1[d]); printf("\n");
    }
  }
  printf("TOTAL states %llu, DAWG nodes bottom-up order %llu, top-down order %llu\n",(unsigned long long)ntot,(unsigned long long)tot[0],(unsigned long long)tot[1]);
  printf("per-depth sum bottom-to-top:"); for(int d=0;d<=K;d++) printf(" %llu",(unsigned long long)sum0[d]); printf("\n");
  printf("per-depth sum top-to-bottom:"); for(int d=0;d<=K;d++) printf(" %llu",(unsigned long long)sum1[d]); printf("\n");
}
