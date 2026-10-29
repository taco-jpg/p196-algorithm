#define main n01_reference_main_not_called
#include "replay20k.cpp"
#undef main
int main(){
 const int k=500,steps=20000;
 vector<Digit> h=B;
 for(int i=0;i<k;i++)h.insert(h.end(),W.begin(),W.end());
 h.push_back(9);
 for(int i=0;i<k;i++)h.insert(h.end(),V.begin(),V.end());
 vector<Digit>P=h;P.push_back(9);P.insert(P.end(),h.rbegin(),h.rend());
 auto D=normalize_coeff(P).first;auto w=W,v=V;
 int samples[]={0,128,480,1000,2000,5000,10000,15000,20000};int si=0;
 cout<<"time,W_long_start,W_long_end,W_long_length,W_mismatches,V_long_start,V_long_end,V_long_length,V_mismatches\n";
 for(int t=0;t<=steps;t++){
   if(t==samples[si]){
     auto run=[&](int start,int end,const vector<Digit>&word){
       int count=0,bs=start,be=start,beg=start;bool active=false;
       int mismatches=0;
       for(int j=start;j<end;j++){
         bool ok=P[j]==word[(j-start)%word.size()];
         if(!ok){mismatches++;active=false;}
         if(ok&&!active){active=true;beg=j;}
         if(ok&&j+1-beg>count){count=j+1-beg;bs=beg;be=j+1;}
       }
       return vector<int>{bs,be,count,mismatches};
     };
     auto a=run(39,39+20*k,w),b=run(39+20*k+1,39+20*k+1+48*k,v);
     cout<<t;for(int q:a)cout<<","<<q;for(int q:b)cout<<","<<q;cout<<"\n";
     if(++si==9)break;
   }
   if(t==steps)break;
   auto nextP=pair_word(D);D=ordinary_add_reverse(D);P=move(nextP);
   int g=t%2==0;w=bulk(w,g);v=bulk(v,g);
 }
}
