#define main W30_OLD_MAIN
#include "replay.cpp"
#undef main
int main(int argc,char **argv){int T=argc>1?atoi(argv[1]):60000;Word P=make_P(300,4200);for(int t=0;t<T;t++){auto [Q,g]=pair_step(P);std::cout<<g;P.swap(Q);}std::cout<<"\n";return 0;}
