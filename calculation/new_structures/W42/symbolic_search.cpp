#include <algorithm>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>
#include <map>
using namespace std;
using V=vector<int>; using i64=long long;
struct E {
  i64 q=0,k=0,c=0;
  E() {}
  E(i64 Q,i64 K,i64 C):q(Q),k(K),c(C) {}
  i64 val(i64 Q,i64 K) const { return q*Q+k*K+c; }
  bool zero() const { return q==0&&k==0&&c==0; }
};
E operator+(E a,E b){return {a.q+b.q,a.k+b.k,a.c+b.c};}
E operator-(E a,E b){return {a.q-b.q,a.k-b.k,a.c-b.c};}
E operator*(E a,i64 n){return {a.q*n,a.k*n,a.c*n};}
string str(E a){return to_string(a.q)+"q+"+to_string(a.k)+"k+"+to_string(a.c);}
i64 modp(i64 x,i64 m){i64 r=x%m;return r<0?r+m:r;}
i64 floordiv(i64 x,i64 m){i64 r=modp(x,m);return (x-r)/m;}
struct R { V w; E n; E len() const {return n*(i64)w.size();} };
struct Cannot:runtime_error { using runtime_error::runtime_error; };
const E Q={1,0,0}, K={0,1,0};
void nonnegative(E e,i64 qmin,i64 kmin){
  if(e.q<0||e.k<0||e.val(qmin,kmin)<0)
    throw Cannot("count not uniformly >=0: "+str(e));
}
R run(V w,i64 n=1){return {std::move(w),E(0,0,n)};}
vector<R> clean(vector<R> seq){
  vector<R> out;
  for(auto &r:seq){
    if(r.w.empty()||r.n.zero())continue;
    if(!out.empty()&&out.back().w==r.w){
      out.back().n=out.back().n+r.n;
    } else if(!out.empty()&&out.back().n.q==0&&out.back().n.k==0&&r.n.q==0&&r.n.k==0){
      i64 L=(i64)out.back().w.size()*out.back().n.c+(i64)r.w.size()*r.n.c;
      if(L<=8192){
        V w; w.reserve((size_t)L);
        for(i64 i=0;i<out.back().n.c;i++)w.insert(w.end(),out.back().w.begin(),out.back().w.end());
        for(i64 i=0;i<r.n.c;i++)w.insert(w.end(),r.w.begin(),r.w.end());
        out.pop_back(); out.push_back(run(std::move(w)));
      } else out.push_back(r);
    } else out.push_back(r);
  }
  return out;
}
E choose(E a,E b,i64 qmin,i64 kmin){
  E d=a-b;
  if(d.q>=0&&d.k>=0&&d.val(qmin,kmin)>=0)return b;
  if(d.q<=0&&d.k<=0&&d.val(qmin,kmin)<=0)return a;
  throw Cannot("ambiguous symbolic boundary comparison "+str(a)+" vs "+str(b));
}
vector<R> eat(R r,E amt,i64 qmin,i64 kmin){
  i64 m=(i64)r.w.size();
  if(modp(amt.q,m)!=0||modp(amt.k,m)!=0)
    throw Cannot("parameter-dependent cut phase "+str(amt)+" mod "+to_string(m));
  E t={floordiv(amt.q,m),floordiv(amt.k,m),floordiv(amt.c,m)};
  i64 rem=modp(amt.c,m);
  if(rem){
    E n=r.n-t-E(0,0,1); nonnegative(n,qmin,kmin);
    V rot; rot.insert(rot.end(),r.w.begin()+rem,r.w.end());
    rot.insert(rot.end(),r.w.begin(),r.w.begin()+rem);
    V tail(r.w.begin()+rem,r.w.end());
    return clean({R{rot,n},run(std::move(tail))});
  }
  E n=r.n-t; nonnegative(n,qmin,kmin);
  return clean({R{r.w,n}});
}
vector<R> add_runs(R a,R b,E amt,i64 qmin,i64 kmin){
  if(amt.q==0&&amt.k==0){
    V w; w.reserve((size_t)amt.c);
    for(i64 i=0;i<amt.c;i++)w.push_back(a.w[i%a.w.size()]+b.w[i%b.w.size()]);
    return {run(std::move(w))};
  }
  i64 m=std::lcm((i64)a.w.size(),(i64)b.w.size());
  if(modp(amt.q,m)!=0||modp(amt.k,m)!=0)
    throw Cannot("parameter-dependent paired phase "+str(amt)+" mod "+to_string(m));
  V w; w.reserve((size_t)m);
  for(i64 i=0;i<m;i++)w.push_back(a.w[i%a.w.size()]+b.w[i%b.w.size()]);
  E copies={floordiv(amt.q,m),floordiv(amt.k,m),floordiv(amt.c,m)};
  nonnegative(copies,qmin,kmin);
  i64 rem=modp(amt.c,m);
  vector<R> out={R{w,copies}};
  if(rem)out.push_back(run(V(w.begin(),w.begin()+rem)));
  return clean(std::move(out));
}
struct Compare {bool equal=false; E first; int observed=-1,expected=-1;};
vector<R> zip_pair(vector<R> left,vector<R> right,i64 qmin,i64 kmin,
                   bool compare=false,Compare *cmp=nullptr,int limit=25000){
  auto aa=clean(std::move(left)); auto bb=clean(std::move(right));
  vector<R> out; E pos; int iterations=0;
  while(!aa.empty()&&!bb.empty()){
    if(++iterations>limit)throw Cannot("symbolic fragment limit");
    R a=aa[0],b=bb[0];
    E amt=choose(a.len(),b.len(),qmin,kmin);
    if(amt.val(qmin,kmin)<=0)throw Cannot("zero-width interval at bound");
    if(compare){
      i64 period=(amt.q||amt.k)?std::lcm((i64)a.w.size(),(i64)b.w.size()):amt.c;
      i64 cap=min(amt.val(qmin,kmin),period);
      for(i64 h=0;h<cap;h++){
        int x=a.w[h%a.w.size()],y=b.w[h%b.w.size()];
        if(x!=y){
          if(cmp){cmp->equal=false;cmp->first=pos+E(0,0,h);cmp->observed=x;cmp->expected=y;}
          return {};
        }
      }
      if(cap<period&&(amt.q!=0||amt.k!=0))
        throw Cannot("too short for universal period equality");
    } else {
      auto x=add_runs(a,b,amt,qmin,kmin); out.insert(out.end(),x.begin(),x.end());
    }
    pos=pos+amt;
    auto ea=eat(a,amt,qmin,kmin),eb=eat(b,amt,qmin,kmin);
    vector<R> na=ea,nb=eb;
    na.insert(na.end(),aa.begin()+1,aa.end());
    nb.insert(nb.end(),bb.begin()+1,bb.end());
    aa=clean(std::move(na)); bb=clean(std::move(nb));
  }
  if(!aa.empty()||!bb.empty())throw Cannot("symbolic unequal total lengths");
  if(cmp){cmp->equal=true;cmp->first=pos;cmp->observed=cmp->expected=-1;}
  return clean(std::move(out));
}
vector<R> rev_runs(const vector<R>&s){
  vector<R> out;
  for(auto it=s.rbegin();it!=s.rend();++it){
    V w=it->w; reverse(w.begin(),w.end()); out.push_back(R{std::move(w),it->n});
  }
  return out;
}
pair<vector<R>,int> normalized(const vector<R>&s,i64 qmin,i64 kmin){
  int carry=0; vector<R> out;
  for(auto &r:s){
    if(r.n.zero())continue;
    nonnegative(r.n-E(0,0,1),qmin,kmin);
    V d; d.reserve(r.w.size()); int c=carry;
    for(int a:r.w){
      if(a<0||a>18)throw Cannot("invalid coefficient");
      int z=a+c; d.push_back(z%10); c=z/10;
    }
    out.push_back(run(d));
    V stable; stable.reserve(r.w.size()); int cc=c;
    for(int a:r.w){int z=a+cc;stable.push_back(z%10);cc=z/10;}
    if(cc!=c)throw Cannot("block carry transducer not idempotent");
    out.push_back(R{std::move(stable),r.n-E(0,0,1)});
    carry=c;
  }
  if(carry)out.push_back(run(V{carry}));
  return {clean(std::move(out)),carry};
}
pair<vector<R>,int> step(const vector<R>&s,i64 qmin,i64 kmin){
  auto [d,g]=normalized(s,qmin,kmin); auto r=rev_runs(d);
  return {zip_pair(std::move(d),std::move(r),qmin,kmin),g};
}
vector<R> tpl(const V&B,const V&W,const V&J,const V&U,const V&C){
  vector<R> h={run(B),R{W,Q},run(J),R{U,K}};
  vector<R> out=h; out.push_back(run(C));
  auto r=rev_runs(h); out.insert(out.end(),r.begin(),r.end());
  return clean(std::move(out));
}
int alt(const V&v){int x=0;for(size_t i=0;i<v.size();i++)x+=(i%2?-1:1)*v[i];return x;}
V nums(int n,int len){V a(len);for(int i=0;i<len;i++){a[i]=n%19;n/=19;}return a;}
int main(int argc,char**argv){
  int nsel=argc>1?atoi(argv[1]):3;
  int zstart=argc>2?atoi(argv[2]):0;
  int zend=argc>3?atoi(argv[3]):1000000;
  V B={10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
  V W={5,18,4,8,1,15,4,0,5}; V U={10,8,9},C={0,0,0};
  i64 qmin=512,kmin=512; map<int,int> hist;
  int count=0,err=0,clockfail=0; vector<pair<V,E>> survivors;
  int lim=1;for(int i=0;i<nsel;i++)lim*=19;
  for(int z=max(0,zstart);z<min(lim,zend);z++){
    V J=nums(z,nsel); if(alt(J)%11!=0)continue; count++;
    try{
      auto cur=tpl(B,W,J,U,C); bool clk=true;
      for(int t=0;t<120;t++){
        auto [next,g]=step(cur,qmin,kmin);
        if(g!=((t%4)==0))clk=false;
        cur=std::move(next);
      }
      auto exp=tpl(B,W,J,U,C);
      for(auto &r:exp)if(r.n.k)r.n.c+=5;
      Compare cmp; zip_pair(cur,exp,qmin,kmin,true,&cmp);
      if(!cmp.equal){
        int off=cmp.first.c-34; hist[off]++;
        if(cmp.first.q!=9||cmp.first.k!=0)
          throw Cannot("mismatch position not 9q+offset: "+str(cmp.first));
        if(off>=0)survivors.push_back({J,cmp.first});
      } else survivors.push_back({J,cmp.first});
      if(!clk)clockfail++;
    }catch(const exception&e){
      err++; if(err<=3)cerr<<"ERR J="<<nsel<<":"<<z<<" "<<e.what()<<"\n";
    }
  }
  cout<<"len="<<nsel<<" raw="<<zstart<<".."<<min(lim,zend)-1
      <<" mod11_admissible="<<count<<" errors="<<err<<" clockfail="<<clockfail
      <<" survivors_with_no_pre_cut_mismatch="<<survivors.size()<<"\n";
  cout<<"histogram (offset from W9|J cut):\n";
  for(auto [o,c]:hist)cout<<o<<":"<<c<<" ";
  cout<<"\n";
  for(auto &s:survivors){
    cout<<"survivor J=";for(int x:s.first)cout<<x<<",";
    cout<<" mismatch="<<str(s.second)<<"\n";
  }
}
