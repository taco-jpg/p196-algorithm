# AgentN01TwoBand480Uniform
**COMPUTED:** a base-10 two-band reverse-and-add template family has **480 consecutive exact nonpalindromic edges for every integer k>=40**.
Source: coefficient pairword `P_k=(B W^k [9] V^k) [9] reverse(B W^k [9] V^k)`; |B|=39, |W|=20, |V|=48, with source arrays in replay20k.cpp.
Every time state is `A_t W_t^(k-40) J_t V_t^(k-40) C_t` plus reflection and optional centre; |A_t|=199, |J_t|=1217, |C_0|=1344, |C_480|=1464.
An independent C++ 80-state two-ended carry checker tests all 480 edges; each period-20 and period-48 band matrix is idempotent, so r=0,1 checks certify every r=k-40>=0.
Ordinary digit-array arithmetic independently verifies k=40,41,42 at all 481 times; independent GMP replay k=45/480 yields 6,442 digits and FNV64 `43d7778659e5a1ae`.
At t480 the exterior A_t and both bulk rows return, but the junction J_t differs at 391 positions and C grows 120; **no template cycle, no decimal Lychrel proof**.
Reproduce: `g++ -O3 -std=c++17 calculation/new_structures/agent-N01/chain480.cpp -o /tmp/n01chain480 && /tmp/n01chain480`.
GMP control: `/tmp/n01gmp 45 480` after compiling replay_gmp20k.cpp with `-lgmpxx -lgmp`.
Files: calculation/new_structures/agent-N01/chain480.cpp, calculation/new_structures/agent-N01/chain480_expected.json, reports/AgentN01TwoBand480Uniform.md.
