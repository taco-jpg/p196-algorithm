// Agent N02: exact 20,000-step GMP & independent decimal schoolbook proof-of-run
// for a transient reflecting centre suffix; extends glider_replay.cpp.
#define main n02_plain_replay_main
#include "glider_replay.cpp"
#undef main
static const int centre_suffix[]={8,13,14,8,9,17,16,8,5,7,1,8,4,14,12,10,1,9,0,4,18,1,17,9,10,14,3,10,4,14,1,0,5,5,4,1,7,9,17,11,5,4,7,6,10,8,4};
int main(int argc,char**argv){
    int q=224,steps=20140;
    if(argc>1)q=stoi(argv[1]);
    if(argc>2)steps=stoi(argv[2]);
    if(q<1||q>10000||steps<1)return 2;
    vector<int> half;for(int j=0;j<39;j++)half.push_back(path[j][0]);
    for(int k=0;k<q;k++)for(int j=0;j<20;j++)half.push_back(cyc[j][0]);
    for(int x:centre_suffix)half.push_back(x);
    vector<Digit> d(2*half.size());
    for(size_t j=0;j<half.size();++j){int lo=min(half[j],9);d[j]=Digit(lo);d[d.size()-1-j]=Digit(half[j]-lo);}
    mpz_class n(to_str(d),10);
    uint64_t checksum=1469598103934665603ULL;
    int first_bad=-1,last_front=-1;
    for(int t=0;t<steps;t++){
        string ns=n.get_str(10);
        if(ns!=to_str(d))throw runtime_error("GMP <> digit value mismatch");
        if(equal(d.begin(),d.end(),d.rbegin()))throw runtime_error("PALINDROME t="+to_string(t));
        int front=int((d.size()+1)/2),ph=t%8;
        for(int j=0;j<(int)((d.size()+1)/2);j++){
            int pair=int(d[j])+int(d[d.size()-1-j]);
            int expected=j<39?path[j][ph]:cyc[(j-39)%20][ph];
            if(pair!=expected){front=j;break;}
        }
        if(front<39){first_bad=t;cout<<"REFLECT_PREFIX_BREAK step="<<t<<" index="<<front<<"\n";break;}
        last_front=front;
        checksum ^= (uint64_t(front)<<16)^uint64_t(ph)^uint64_t(d.size());
        checksum *= 1099511628211ULL;
        auto next=ordinary_step(d);
        mpz_class nnext=n+reverse_gmp(n);
        if(nnext.get_str(10)!=to_str(next))throw runtime_error("GMP <> schoolbook successor mismatch");
        if(int(next.size())-int(d.size())!=int(t%2==0))throw runtime_error("unexpected overflow");
        d=move(next);n=move(nnext);
        if((t+1)%5000==0)cout<<"REFLECT_CHECKPOINT step="<<t+1<<" digits="<<d.size()<<" front="<<front<<" checksum="<<checksum<<"\n"<<flush;
    }
    cout<<"REFLECT_GMP_AND_SCHOOLBOOK_PASS q="<<q<<" checked_steps="<<steps<<" first_bad="<<first_bad
        <<" initial_digits="<<2*half.size()<<" final_digits="<<d.size()<<" last_front="<<last_front<<" checksum="<<checksum<<"\n";
}
