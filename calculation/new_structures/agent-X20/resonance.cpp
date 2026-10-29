#define main X20_unused
#include "two_counter.cpp"
#undef main
int main(){int m=40,n=40;V P=seed(m,n),D=norm(P).first,w=W,v=Q;State first=extract(P,m,n,w,v);for(int t=0;t<=480;t++){
 if(t==8||t==88||t==272||t==480){auto s=extract(P,m,n,w,v);V candidate=seed(m+t/272,n+t/272);long long diff=0;int prefix=0,last=-1;bool sameLen=candidate.size()==P.size();if(sameLen){for(int i=0;i<(int)P.size();i++){if(P[i]!=candidate[i]){diff++;last=i;}else if(prefix==i)prefix++;}}int jdiff=0;for(int i=0;i<(int)s.J.size();i++)jdiff+=(s.J[i]!=first.J[i]);cout<<"t="<<t<<" digits="<<D.size()<<" outer="<<(s.A==first.A)<<" W="<<(s.W==first.W)<<" V="<<(s.Q==first.Q)<<" jdiff="<<jdiff<<" C="<<s.C.size()<<" C0="<<first.C.size()<<" candidate_lenmatch="<<sameLen<<" mismatch="<<diff<<" prefix="<<prefix<<" last="<<last<<"\n";}
 if(t==480)break;V nd=add(D),np=pairs(D);D.swap(nd);P.swap(np);w=bulk(w,t%2==0);v=bulk(v,t%2==0);
}}
