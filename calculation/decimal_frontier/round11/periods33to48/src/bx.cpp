// bx: exact exterior (B-cycle) position-automaton engine, NO key truncation.
// For a fixed cyclic overflow word g (length p), decides whether a B-cycle with overflow stream g exists, for ALL B lengths.
//
// Same mathematical automaton as structure/bauto.cpp (read & re-derived, see EXTERIOR.md section 1) but:
//   * state key = (L, H, Y[]) packed into W 64-bit words (W chosen at compile time by -DKW, default 2: p<=32, G*ydig<=64)
//   * exact comparison in an open-addressing table (no hashing-only identification, no 127-bit limit)
//   * backward viability DP for the p-step closure => successor enumeration is output-sensitive
//   * word-list mode, resource caps (states, seconds), depth cap (for funnel statistics), first-accept mode.
//
// usage: bx b -g WORD | -f FILE   [-cap N] [-sec S] [-maxdepth D] [-first] [-w] [-q]
//   status per word:  EXHAUSTED (no cycle), ACCEPT (e streams listed), CAPPED(states|time), DEPTHCAP
// Output lines (one per word):  RES b p G g STATUS states depth secs  [e=... ...]
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <string>
#include <map>
#include <set>
#include <algorithm>
#include <chrono>
#include <unistd.h>
#include <new>
using namespace std;
typedef uint64_t u64; typedef unsigned __int128 u128;
#ifndef KW
#define KW 2
#endif
struct Key { u64 w[KW]; bool operator==(const Key&o) const { for(int i=0;i<KW;i++) if(w[i]!=o.w[i]) return false; return true; } };
static inline u64 mix(u64 x){ x^=x>>33; x*=0xff51afd7ed558ccdULL; x^=x>>33; x*=0xc4ceb9fe1a85ec53ULL; x^=x>>33; return x; }
static inline u64 hashKey(const Key&k){ u64 h=0x9E3779B97F4A7C15ULL; for(int i=0;i<KW;i++){ h=mix(h^k.w[i])+0x632BE59BD9B4E019ULL*(i+1);} return h; }

// ---------------- problem context ----------------
int b, p, G, ydig, NX;           // NX = 2b-1 values of x (0..2b-2)
int gv[64], gi[64], gt[64];      // gv[t] overflow bit, gi[t] index among overflow times, gt[i] = time of i-th overflow
u64 MASKP;
int YPERW, YWORDS;               // Y digits per word
bool MR=false; int YBITS=0;      // MR: Y digits packed in mixed radix b (u64), YBITS bits
Key SENT;
bool SEG=false;
int symM=1, symS=0;   // g has least period symS, symM = p/symS ; quotient by the cyclic time shift of symS steps (default on)
bool USESYM=true; bool COUNTMODE=false;
bool FORCEMR=false;   // segment mode: no cyclic closure x_p = x_0 (feasibility of a finite overflow pattern)

struct St { u64 L, H; unsigned char Y[64]; };

static inline Key packKey(const St&s){
  Key k; for(int i=0;i<KW;i++) k.w[i]=0;
  // word 0 : L (bits 0..p-1), H (bits p..2p-1) if 2p<=64 else spill
  // generic bit-buffer packing
  int pos=0;
  auto put=[&](u64 v,int nb){ // nb<=64
    int wi=pos>>6, off=pos&63;
    k.w[wi]|=v<<off;
    if(off+nb>64) k.w[wi+1]|=v>>(64-off);
    pos+=nb; };
  put(s.L,p); put(s.H,p);
  if(!MR){ for(int i=0;i<G;i++) put((u64)s.Y[i],ydig); }
  else { u64 v=0; for(int i=G-1;i>=0;i--) v=v*(u64)b+s.Y[i]; put(v,YBITS); }
  return k;
}
static inline void unpackKey(const Key&k,St&s){
  int pos=0;
  auto get=[&](int nb)->u64{
    int wi=pos>>6, off=pos&63;
    u64 v=k.w[wi]>>off;
    if(off+nb>64) v|=k.w[wi+1]<<(64-off);
    pos+=nb;
    return nb==64? v : (v&((1ULL<<nb)-1)); };
  s.L=get(p); s.H=get(p);
  if(!MR){ for(int i=0;i<G;i++) s.Y[i]=(unsigned char)get(ydig); }
  else { u64 v=get(YBITS); for(int i=0;i<G;i++){ s.Y[i]=(unsigned char)(v%(u64)b); v/=(u64)b; } }
}

// ---------------- hash table ----------------
struct Table {
  vector<Key> t; u64 mask=0, n=0;
  void init(u64 cap){ u64 c=1024; while(c<cap) c<<=1; t.assign(c,SENT); mask=c-1; n=0; }
  void grow(){ vector<Key> old; old.swap(t); u64 c=(mask+1)*2; t.assign(c,SENT); mask=c-1; for(auto&k:old) if(!(k==SENT)){ u64 h=hashKey(k)&mask; while(!(t[h]==SENT)) h=(h+1)&mask; t[h]=k; } }
  bool insert(const Key&k){ // returns true if new
    if((n+1)*10>(mask+1)*6) grow();
    u64 h=hashKey(k)&mask;
    while(true){ if(t[h]==SENT){ t[h]=k; n++; return true; } if(t[h]==k) return false; h=(h+1)&mask; }
  }
  size_t bytes() const { return t.size()*sizeof(Key); }
};

// ---------------- transitions ----------------
static u64 vm[66][64];     // vm[t][x] : bitmask of reachable x_p values
static inline int validc(int Ht,int x){ // bitmask of c in {0,1} with floor((x+c)/b)==Ht
  int m=0;
  for(int c=0;c<2;c++) if(((x+c)>=b)==(Ht!=0)) m|=1<<c;
  return m;
}
static int tabValid[2][64];   // [Ht][x]
static int tabBase[2][64];    // [Lt][x] = (x+Lt)%b
static int tabPart[64][2];    // [x][c] = (x+c)%b
static int tabCar[2][64];     // (x+Lt)>=b

struct Succ { u64 L, H; unsigned char Y[64]; };

template<class F> void expand(const St&s,bool first,F emit){
  int Lt[64],Ht[64],Yt[64];
  for(int t=0;t<p;t++){ Lt[t]=(s.L>>t)&1; Ht[t]=(s.H>>t)&1; Yt[t]= gv[t]? s.Y[gi[t]] : 0; }
  for(int x=0;x<NX;x++) vm[p][x]= SEG ? 1ULL : (1ULL<<x);   // SEG: every end value allowed (mask bit 0 = 'accepted')
  for(int t=p-1;t>=0;t--){
    const u64* nxt=vm[t+1]; u64* cur=vm[t];
    int Lc=Lt[t],Hc=Ht[t]; int gg=gv[t]; int Y=Yt[t];
    for(int x=0;x<NX;x++){
      if(first&&x==0){ cur[x]=0; continue; }
      int vc=tabValid[Hc][x]; if(!vc){ cur[x]=0; continue; }
      int base=tabBase[Lc][x]; u64 m=0;
      if(gg){ m|=nxt[base+Y]; /* both valid c lead to the same x'; c only changes H2,Y2 */ }
      else { if(vc&1) m|=nxt[base+tabPart[x][0]]; if(vc&2) m|=nxt[base+tabPart[x][1]]; }
      cur[x]=m;
    }
  }
  int xs[64]; int cs[64];
  for(int x0=(first?1:0);x0<NX;x0++){
    int tgt = SEG ? 0 : x0;
    if(!((vm[0][x0]>>tgt)&1)) continue;
    // iterative DFS
    int t=0; xs[0]=x0; int choice[64]; // choice[t] = next c to try (0,1,2=done)
    // we maintain L2,H2,Y2 incrementally; simplest: recompute at leaf (p<=64) -- cheap relative to hash insert
    choice[0]=0;
    while(t>=0){
      if(t==p){
        // leaf: xs[p]==x0 guaranteed
        Succ sc; sc.L=0; sc.H=0;
        for(int tt=0;tt<p;tt++){ sc.L|=(u64)tabCar[Lt[tt]][xs[tt]]<<tt; sc.H|=(u64)cs[tt]<<tt; }
        for(int i=0;i<G;i++){ int tt=gt[i]; sc.Y[i]=(unsigned char)tabPart[xs[tt]][cs[tt]]; }
        emit(sc,xs,cs);
        t--; continue;
      }
      int vc=tabValid[Ht[t]][xs[t]];
      bool adv=false;
      while(choice[t]<2){
        int c=choice[t]++;
        if(!((vc>>c)&1)) continue;
        int base=tabBase[Lt[t]][xs[t]];
        int nv= gv[t]? base+Yt[t] : base+tabPart[xs[t]][c];
        if(!((vm[t+1][nv]>>tgt)&1)) continue;
        cs[t]=c; xs[t+1]=nv; t++; choice[t]=0; adv=true; break;
      }
      if(!adv){ t--; }
    }
  }
}

static inline bool accepting(const St&s){
  if((s.L^s.H)!=MASKP) return false;
  for(int i=0;i<G;i++){ int l=(s.L>>gt[i])&1; if(s.Y[i]!=(unsigned)((b-1)*l)) return false; }
  return true;
}

// ---------------- driver ----------------
struct Opts { int layered=0; u64 lcap=20000000ULL; int mdd=0; bool verbose=false; u64 cap=40000000ULL; double sec=1e18; int maxdepth=1<<30; bool first=false; bool wit=false; bool quiet=false; };
double now(){ return chrono::duration<double>(chrono::steady_clock::now().time_since_epoch()).count(); }

bool setupWord(const string&gs){
  p=gs.size(); if(p>=60) return false;
  G=0; for(int t=0;t<p;t++){ gv[t]=gs[t]=='1'; if(gv[t]){ gi[t]=G; gt[G]=t; G++; } else gi[t]=-1; }
  MASKP=(p==64)?~0ULL:((1ULL<<p)-1);
  symM=1; symS=p; if(USESYM){ for(int sp=1;sp<p;sp++){ if(p%sp) continue; bool ok=true; for(int t=0;t<p;t++) if(gv[t]!=gv[(t+sp)%p]){ok=false;break;} if(ok){ symS=sp; symM=p/sp; break; } } }
  ydig=1; while((1<<ydig)<=b) ydig++;
  NX=2*b-1; if(NX>63) return false;
  MR=false; YBITS=ydig*G;
  if(FORCEMR || 2*p+ydig*G>64*KW-1){ // try mixed radix
    double lg=0; for(int i=0;i<G;i++) lg+=__builtin_log2((double)b); int nb=(int)lg+1; if(nb>63||2*p+nb>64*KW-1) return false; MR=true; YBITS=nb; // b^G < 2^nb
    unsigned __int128 pw=1; for(int i=0;i<G;i++) pw*=b; if(pw>((unsigned __int128)1<<nb)) return false; }
  for(int h=0;h<2;h++) for(int x=0;x<NX;x++){ tabValid[h][x]=validc(h,x); tabBase[h][x]=(x+h)%b; tabCar[h][x]=((x+h)>=b); }
  for(int x=0;x<NX;x++) for(int c=0;c<2;c++) tabPart[x][c]=(x+c)%b;
  // note: x+c for c=1 can be 2b-1 -> %b fine
  return true;
}


static inline u64 rotbits(u64 v,int r){ // v'[t] = v[(t+r)%p]
  if(r==0) return v;
  return ((v>>r)|(v<<(p-r)))&MASKP; }
static inline void canonSt(St&s){
  if(symM==1) return;
  Key best=packKey(s); St bs=s;
  int gper=G/symM;
  for(int j=1;j<symM;j++){
    St t; t.L=rotbits(s.L,j*symS); t.H=rotbits(s.H,j*symS);
    for(int i=0;i<G;i++) t.Y[i]=s.Y[(i+j*gper)%G];
    Key k=packKey(t);
    bool less=false; for(int w=KW-1;w>=0;w--){ if(k.w[w]!=best.w[w]){ less=k.w[w]<best.w[w]; break; } }
    if(less){ best=k; bs=t; }
  }
  s=bs;
}


// ---- experiment: size of the reduced ordered MDD (levels = time t, symbol = (L_t,H_t,Y_t)) of a set of states ----
#include <unordered_map>
static size_t mddNodes(const vector<Key>&fr, size_t&edges){
  // symbols per level: L,H bits (+Y digit if overflow)
  int nsym=0; (void)nsym;
  vector<vector<unsigned>> seq(fr.size(), vector<unsigned>(p));
  for(size_t i=0;i<fr.size();i++){ St s; unpackKey(fr[i],s); for(int t=0;t<p;t++){ unsigned sy=((s.L>>t)&1)|(((s.H>>t)&1)<<1); if(gv[t]) sy|=(unsigned)s.Y[gi[t]]<<2; seq[i][t]=sy; } }
  vector<unsigned> idx(fr.size()); for(size_t i=0;i<idx.size();i++) idx[i]=i;
  sort(idx.begin(),idx.end(),[&](unsigned a,unsigned b2){ return seq[a]<seq[b2]; });
  // build bottom-up by recursion over sorted ranges
  struct H3{ size_t operator()(const vector<unsigned>&v) const { size_t h=1469598103934665603ULL; for(unsigned x:v){ h^=x+0x9e3779b97f4a7c15ULL+(h<<6)+(h>>2);} return h; } };
  vector<unordered_map<vector<unsigned>,unsigned,H3>> uniq(p+1);
  size_t nodes=0; edges=0;
  // recursive lambda
  struct Rec { const vector<vector<unsigned>>&seq; const vector<unsigned>&idx; vector<unordered_map<vector<unsigned>,unsigned,H3>>&uniq; int p; size_t&nodes; size_t&edges;
    unsigned go(size_t lo,size_t hi,int level){
      if(level==p) return 0;
      vector<unsigned> key; // (sym, child)*
      size_t i=lo;
      while(i<hi){ size_t j=i; unsigned sy=seq[idx[i]][level]; while(j<hi && seq[idx[j]][level]==sy) j++;
        unsigned ch=go(i,j,level+1); key.push_back(sy); key.push_back(ch); i=j; }
      auto it=uniq[level].find(key); if(it!=uniq[level].end()) return it->second;
      unsigned id=uniq[level].size()+1; uniq[level][key]=id; nodes++; edges+=key.size()/2; return id; }
  } R{seq,idx,uniq,p,nodes,edges};
  R.go(0,idx.size(),0);
  return nodes;
}

struct Result { string status; u64 states=0; int depth=0; double secs=0; vector<pair<u64,int>> acc; size_t bytes=0; };

Result runWord(const string&gs,const Opts&o, vector<vector<int>>*witCols=nullptr, u64 witE=~0ULL){
  Result R; double t0=now();
  Table tab; tab.init(4096);
  St s0; s0.L=0; s0.H=0; for(int t=0;t<p;t++) if(gv[t]) s0.H|=1ULL<<t; for(int i=0;i<G;i++) s0.Y[i]=1;
  Key k0=packKey(s0); tab.insert(k0);
  vector<Key> fr(1,k0), nf; int depth=0; bool capped=false; string capwhy;
  set<u64> accSeen;
  // witness bookkeeping: parent pointers via map from key to (parent key, xs)
  struct Par { Key par; vector<unsigned char> xs; };
  vector<pair<Key,Par>> parlist; // appended in discovery order, looked up via small table when needed
  Table* ptab=nullptr; vector<Par> pvals;
  if(o.wit){ ptab=new Table(); ptab->init(4096); }
  auto findParIdx=[&](const Key&k)->long{ // linear probe in ptab for index mapping: use separate map
    return -1; };
  (void)findParIdx; (void)parlist;
  map<vector<u64>,Par> pmap; // simple (witness mode only; small instances)
  if(o.wit) pmap[vector<u64>(k0.w,k0.w+KW)]=Par{k0,{}};
  while(!fr.empty()){
    if(depth>=o.maxdepth){ R.status="DEPTHCAP"; break; }
    nf.clear();
    for(size_t fi=0;fi<fr.size();fi++){
      St s; unpackKey(fr[fi],s);
      if(accepting(s) && !accSeen.count(s.L)){ accSeen.insert(s.L); R.acc.push_back({s.L,depth});
        if(o.wit){ if(witCols){ // reconstruct columns
            vector<vector<int>> cols; Key cur=fr[fi];
            while(true){ auto it=pmap.find(vector<u64>(cur.w,cur.w+KW)); if(it==pmap.end()||it->second.xs.empty()) break; vector<int> col(it->second.xs.begin(),it->second.xs.end()); cols.push_back(col); cur=it->second.par; }
            reverse(cols.begin(),cols.end()); *witCols=cols; } }
        if(o.first){ R.status="ACCEPT"; goto done; } }
      expand(s,depth==0,[&](Succ&sc,int*xs,int*cs){
        St s2; s2.L=sc.L; s2.H=sc.H; for(int i=0;i<G;i++) s2.Y[i]=sc.Y[i];
        canonSt(s2);
        Key k=packKey(s2);
        if(tab.insert(k)){ nf.push_back(k); if(o.wit){ Par pr; pr.par=fr[fi]; pr.xs.assign(xs,xs+p); pmap[vector<u64>(k.w,k.w+KW)]=pr; } }
      });
      if((fi&1023)==0){ if(tab.n>o.cap){ capped=true; capwhy="states"; break; } if(now()-t0>o.sec){ capped=true; capwhy="time"; break; } }
    }
    if(capped) break;
    fr.swap(nf); depth++;
    if(o.mdd>0 && depth%o.mdd==0){ size_t ed; size_t nn=mddNodes(fr,ed); fprintf(stderr,"  MDD depth %d: %zu states in frontier -> %zu nodes %zu edges\n",depth,fr.size(),nn,ed);
      { set<pair<u64,u64>> lh; set<vector<unsigned char>> ys; set<u64> ls,hs; for(auto&k:fr){ St s; unpackKey(k,s); lh.insert({s.L,s.H}); ls.insert(s.L); hs.insert(s.H); ys.insert(vector<unsigned char>(s.Y,s.Y+G)); } fprintf(stderr,"     distinct (L,H) %zu, distinct L %zu, distinct H %zu, distinct Y %zu\n",lh.size(),ls.size(),hs.size(),ys.size()); } }
    if(o.mdd>0 && depth%o.mdd==0 && tab.n<=3000000ULL){ vector<Key> all; all.reserve(tab.n); for(auto&k:tab.t) if(!(k==SENT)) all.push_back(k); size_t ed; size_t nn=mddNodes(all,ed); fprintf(stderr,"  MDDV depth %d: visited %zu states -> %zu nodes %zu edges\n",depth,all.size(),nn,ed); }
    if(o.verbose) fprintf(stderr,"  depth %d frontier %zu states %llu t=%.1f\n",depth,fr.size(),(unsigned long long)tab.n,now()-t0);
    if(tab.n>o.cap){ capped=true; capwhy="states"; break; }
    if(now()-t0>o.sec){ capped=true; capwhy="time"; break; }
  }
  if(o.wit && !fr.empty() && witCols && R.acc.empty()){ Key cur=fr[fr.size()/2]; vector<vector<int>> cols; while(true){ auto it=pmap.find(vector<u64>(cur.w,cur.w+KW)); if(it==pmap.end()||it->second.xs.empty()) break; cols.push_back(vector<int>(it->second.xs.begin(),it->second.xs.end())); cur=it->second.par; } reverse(cols.begin(),cols.end()); *witCols=cols; }
  if(R.status.empty()){
    if(capped) R.status="CAPPED_"+capwhy;
    else R.status= R.acc.empty()? "EXHAUSTED":"ACCEPT";
  }
  done:
  R.states=tab.n; R.depth=depth; R.secs=now()-t0; R.bytes=tab.bytes();
  if(ptab) delete ptab;
  return R;
}

// Layered mode (no global de-duplication): R_d = set of cut states reachable after EXACTLY d positions, kept for the current layer only.
//   * memory = O(max layer), runs to any depth D; accepted states are detected at every layer (an ACCEPT is a genuine B-cycle of width d);
//   * R_d = empty  => EXHAUSTED (exact);  reaching depth D with a non-empty layer proves only "no cycle of width < D" (status LAYERED).
Result runLayered(const string&gs,const Opts&o){
  (void)gs; Result R; double t0=now();
  St s0; s0.L=0; s0.H=0; for(int t=0;t<p;t++) if(gv[t]) s0.H|=1ULL<<t; for(int i=0;i<G;i++) s0.Y[i]=1;
  Key k0=packKey(s0);
  vector<Key> fr(1,k0), nf; int depth=0; u64 total=1, maxlayer=1; set<u64> accSeen; bool capped=false;
  Table tab;
  while(!fr.empty() && depth<o.layered){
    u64 want=4096; while(want*6 < (u64)fr.size()*10*2) want<<=1;    // about 2x the previous layer to start with (table grows if needed)
    tab.init(want); nf.clear();
    for(size_t fi=0;fi<fr.size();fi++){
      St s; unpackKey(fr[fi],s);
      if(accepting(s) && !accSeen.count(s.L)){ accSeen.insert(s.L); R.acc.push_back({s.L,depth}); }
      expand(s,depth==0,[&](Succ&sc,int*xs,int*cs){ (void)xs; (void)cs;
        St s2; s2.L=sc.L; s2.H=sc.H; for(int i=0;i<G;i++) s2.Y[i]=sc.Y[i];
        canonSt(s2); Key k=packKey(s2); if(tab.insert(k)) nf.push_back(k); });
      if((fi&1023)==0){ if(nf.size()>o.lcap){ capped=true; break; } if(now()-t0>o.sec){ capped=true; break; } }
    }
    if(capped) break;
    fr.swap(nf); depth++; total+=fr.size(); if(fr.size()>maxlayer) maxlayer=fr.size();
    if(o.verbose && depth%10==0) fprintf(stderr,"  layer %d size %zu total %llu t=%.1f\n",depth,fr.size(),(unsigned long long)total,now()-t0);
  }
  if(fr.empty() && !capped) R.status= R.acc.empty()? "EXHAUSTED":"ACCEPT";
  else if(capped) R.status= R.acc.empty()? "CAPPED_layer":"ACCEPT_FOUND";
  else R.status= R.acc.empty()? "LAYERED":"ACCEPT_FOUND";
  R.states=maxlayer; R.depth=depth; R.secs=now()-t0; R.bytes=tab.bytes();
  return R;
}

string eString(u64 e){ string s; for(int t=0;t<p;t++) s+=char('0'+((e>>t)&1)); return s; }

// Path counting (small instances): number of distinct position-choice histories (x_0[k], c_t for k=0..d-1) ending in an accepting cut state at exactly depth d,
// per accepted stream e.  Layered, no symmetry quotient should be used (-nosym) so that every history is one B (up to nothing).  Counts saturate at 2^63.
#include <unordered_map>
struct KeyHash { size_t operator()(const Key&k) const { return (size_t)hashKey(k); } };
int runCount(const string&gs,const Opts&o){
  (void)gs; double t0=now();
  St s0; s0.L=0; s0.H=0; for(int t=0;t<p;t++) if(gv[t]) s0.H|=1ULL<<t; for(int i=0;i<G;i++) s0.Y[i]=1;
  unordered_map<Key,u64,KeyHash> cur, nxt; cur[packKey(s0)]=1; int depth=0;
  map<pair<u64,int>,u64> accCnt;       // (e,depth) -> number of histories
  while(!cur.empty() && depth<o.layered){
    nxt.clear();
    for(auto&kv:cur){
      St s; unpackKey(kv.first,s);
      if(accepting(s)) accCnt[{s.L,depth}]+=kv.second;
      expand(s,depth==0,[&](Succ&sc,int*xs,int*cs){ (void)xs; (void)cs;
        St s2; s2.L=sc.L; s2.H=sc.H; for(int i=0;i<G;i++) s2.Y[i]=sc.Y[i];
        canonSt(s2); Key k=packKey(s2); u64&c=nxt[k]; c+=kv.second; });
    }
    cur.swap(nxt); depth++;
    if(now()-t0>o.sec){ printf("COUNT p=%d g=%s TIMEOUT depth=%d\n",p,gs.c_str(),depth); break; }
  }
  printf("COUNT p=%d g=%s depth_reached=%d layer_empty=%d\n",p,gs.c_str(),depth,(int)cur.empty());
  for(auto&kv:accCnt) printf("  ACCEPTPATHS e=%s depth=%d histories=%llu\n",eString(kv.first.first).c_str(),kv.first.second,(unsigned long long)kv.second);
  return 0;
}

int main(int argc,char**argv){
  if(argc<3){ fprintf(stderr,"usage: bx b (-g WORD | -f FILE) [-cap N] [-sec S] [-maxdepth D] [-first] [-w] [-q]\n"); return 2; }
  b=atoi(argv[1]); Opts o; string gword, gfile;
  for(int i=2;i<argc;i++){ string a=argv[i];
    if(a=="-g") gword=argv[++i]; else if(a=="-f") gfile=argv[++i]; else if(a=="-cap") o.cap=strtoull(argv[++i],0,10);
    else if(a=="-sec") o.sec=atof(argv[++i]); else if(a=="-maxdepth") o.maxdepth=atoi(argv[++i]); else if(a=="-first") o.first=true;
    else if(a=="-v") o.verbose=true; else if(a=="-nosym") USESYM=false; else if(a=="-forcemr") FORCEMR=true; else if(a=="-mdd") o.mdd=atoi(argv[++i]); else if(a=="-seg") SEG=true; else if(a=="-layered") o.layered=atoi(argv[++i]); else if(a=="-count") { o.layered=atoi(argv[++i]); COUNTMODE=true; } else if(a=="-lcap") o.lcap=strtoull(argv[++i],0,10); else if(a=="-w") o.wit=true; else if(a=="-q") o.quiet=true; }
  for(int i=0;i<KW;i++) SENT.w[i]=~0ULL;
  vector<string> words;
  if(!gword.empty()) words.push_back(gword);
  if(!gfile.empty()){ FILE*f=fopen(gfile.c_str(),"r"); if(!f){ perror("open"); return 2; } char buf[256]; while(fgets(buf,sizeof buf,f)){ string s(buf); while(!s.empty()&&(s.back()=='\n'||s.back()=='\r'||s.back()==' ')) s.pop_back(); if(!s.empty()) words.push_back(s); } fclose(f); }
  for(auto&gs:words){
    if(!setupWord(gs)){ printf("RES b=%d p=%d G=? g=%s UNSUPPORTED(KW=%d)\n",b,(int)gs.size(),gs.c_str(),KW); fflush(stdout); continue; }
    if(COUNTMODE){ runCount(gs,o); continue; }
    vector<vector<int>> cols;
    Result R;
    try { R= o.layered? runLayered(gs,o) : runWord(gs,o,o.wit?&cols:nullptr); } catch(std::bad_alloc&) { R.status="CAPPED_mem"; R.states=0; R.depth=0; }
    printf("RES b=%d p=%d G=%d g=%s %s states=%llu depth=%d secs=%.2f tabMB=%.0f wdone=%d m=%d",b,p,G,gs.c_str(),R.status.c_str(),(unsigned long long)R.states,R.depth,R.secs,R.bytes/1048576.0,(R.status=="EXHAUSTED")?-1:R.depth-1,symM);
    for(auto&a:R.acc) printf(" e=%s@%d",eString(a.first).c_str(),a.second);
    printf("\n");
    if(o.wit && !cols.empty()){
      printf("WIT g=%s B_t=",gs.c_str());
      for(int t=0;t<p;t++){ printf("["); vector<int> r; for(auto&c:cols) r.push_back(c[t]); while(!r.empty()&&r.back()==b-1) r.pop_back(); for(size_t i=0;i<r.size();i++) printf("%d%s",r[i],i+1<r.size()?",":""); printf("]"); }
      printf("\n");
    }
    fflush(stdout);
  }
  return 0;
}
