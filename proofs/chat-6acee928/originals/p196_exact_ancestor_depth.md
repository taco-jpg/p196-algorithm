# P196 的继续推进：精确反推深度与两类新的无限排除族

本文给出本轮新推得的两个定理，证明不依赖有限枚举。附后的计算只用于独立核验数位方程、结构分类和达到上界的构造。

完整 P196 猜想仍未证明。这里不主张文献首创，也不把所得深度上界推广到本文目标族之外。

## 一、结果及其准确范围

令
\[
T(N)=N+\operatorname{rev}(N),\qquad N_t=T^t(196).
\]
反转忽略前导零。定义两种数位操作：

- \(D(V)\)：每个数位重复两次，例如 \(D(10201)=1100220011\)；
- \(I(V)\)：每两个相邻数位之间插入一个零，例如 \(I(121)=10201\)。

总有
\[
D(V)=11I(V).
\tag{1}
\]
这里的相等是整数相等；乘法没有进位。

为避免“首次到达”和“任意时刻出现”的混淆，定义
\[
H_{11}(P)=\sup\{k\ge0:\ \exists A>0,\ 11\mid A,\ T^k(A)=P\}.
\tag{2}
\]
其中允许起点和中间项为回文。以下上界控制所有出现时刻。

**定理 A：十一对同数字的精确深度。**
设 \(B\) 是十进制数位只含 0、1 的正回文，且恰有 11 个数位 1。对 \(1\le d\le8\)，令
\[
d=2^fu,\quad u\text{ 为奇数},\qquad a=\frac{u+9}{2}.
\]
则
\[
\boxed{H_{11}(D(dB))=f+2+v_2(a).}
\tag{3}
\]
\(v_2(a)\) 是 2 在 \(a\) 中的指数。具体为

| \(d\) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 精确最大步数 | 2 | 3 | 3 | 4 | 2 | 4 | 5 | 5 |

该公式不涉及各零串长度；每个上界对每一个符合条件的 \(B\) 都可以达到。表中没有声称 \(d=9\) 的普适深度上界。

**196 推论 A。**对以上任意 \(B\)，以及全部 \(1\le d\le9\)，
\[
\boxed{N_t\ne D(dB)\quad(t\ge0).}
\tag{4}
\]
因此，十一段 \(dd\) 之间插入任意偶数长度的零串，只要整体对称，就永远不会出现在 196 轨道中。零串允许为空。

**定理 B：混合奇数数位的精确深度。**
设 \(V\) 是正回文，满足：

1. 非零数位属于 \(\{1,3,5,7\}\)；
2. 非零数位个数为奇数 \(h\le21\)；
3. 中央数位为 1 或 5；
4. 数位和 \(w\) 满足 \(w\equiv2h\pmod{11}\)。

则
\[
\boxed{H_{11}(D(V))=2.}
\tag{5}
\]
从而
\[
\boxed{N_t\ne D(V)\quad(t\ge0).}
\tag{6}
\]
该定理允许任意长度、对称配置的零串。它不要求所有非零数位相同。

一个不被模 3 直接排除的特例是：任意 \(a,b,c\ge0\) 时，196 轨道永不出现
\[
77\,0^{2a}77\,0^{2b}77\,0^{2c}55\,
0^{2c}77\,0^{2b}77\,0^{2a}77.
\tag{7}
\]
其对应的 \(V\) 有 \(h=7,w=47\)，且 \(47\equiv14\pmod{11}\)。全部零串为空时，目标为 \(77777755777777\)。

## 二、基本数位方程

对 \(n\) 位正整数 \(N\)，从低位向高位记数位 \(a_i\)，并记
\[
s_i=q(N)_i=a_i+a_{n-1-i}.
\]
可实现的原始对称和字恰好满足：对称、每项在 0 到 18 之间、首项正；奇数长度时中央项必须为偶数。

反转相加的进位和输出为
\[
c_0=0,\qquad c_{i+1}=\left\lfloor\frac{s_i+c_i}{10}\right\rfloor,
\qquad b_i=s_i+c_i-10c_{i+1}.
\tag{8}
\]
若 \(c_n=1\)，添上最高位 \(b_n=1\)，称为增位。否则称不增位。

**引理 1：一步回文判据。**
\[
T(N)\text{ 为回文}
\iff
(\forall i,\ s_i\le9)
\quad\text{或}\quad
(\forall i,\ s_i\in\{0,11\}).
\tag{9}
\]
前一情形不增位且完全无进位；后一情形增位，输出为 \(11U\)，其中 \(U\) 是只含 0、1 的回文。

证明不增位部分：输出对称给出
\[
c_i-c_{n-1-i}=10(c_{i+1}-c_{n-i}).
\]
左边绝对值至多 1，右边为 10 的倍数，因此两边均为零。从 \(c_0=c_n=0\) 向内推进，得到所有进位为零。

证明增位部分：首尾输出为 1，故 \(s_0=11\)。向内逐层使用 \(b_i=b_{n-i}\)，可得
\[
s_i=10c_{i+1}+c_{n-i}.
\]
这里两个进位必须相等：若分别为 1、0，则同一原始和 10 在对侧不产生进位，矛盾；若分别为 0、1，则原始和 1 在对侧产生进位，也矛盾。于是 \(s_i=11c_{i+1}\)。反向验证直接代入式 (8) 即可。更详细的归纳是：已知上一层 \(s_{i-1}=11c_i\) 及 \(c_i=c_{n-i+1}\)，输出相等先给出上式，再用两侧进位更新迫使 \(c_{i+1}=c_{n-i}\)。初始层由 \(s_0=11\) 成立。∎

对不增位的映射 \(Y\mapsto X\)，从外向内考察一对数位。令
\[
x=c_i,\quad y=c_{n-i},\quad x'=c_{i+1},\quad y'=c_{n-1-i},
\]
来源当前原始和为 \(s\)，输出对称和为 \(p\)。则
\[
x'=\lfloor(s+x)/10\rfloor,\quad
y=\lfloor(s+y')/10\rfloor,
\quad p=2s+x+y'-10(x'+y).
\tag{10}
\]

**引理 2：不增位的两个奇偶性质。**

(a) 若 \(X=T(Y)\) 不增位，且 \(q(X)\) 的所有项均为偶数，则 \(X\) 为回文。

(b) 若 \(X=T(Y)\) 不增位，\(X\) 位数为偶数，且 \(q(X)\) 不含 9，则 \(q(X)\) 的前一半中，奇数项个数必为偶数。

证明：式 (10) 中，\(x'\ne y\) 只可能发生在 \(s=9,p=9\)。因此当 \(p\ne9\) 时，
\[
x'=y,\qquad x'\mathbin{\oplus}y'
=x\mathbin{\oplus}y\mathbin{\oplus}(p\bmod2).
\tag{11}
\]
其中 \(\oplus\) 表示异或。

若所有 \(p\) 为偶数，从外边界 \((x,y)=(0,0)\) 出发，式 (10)、(11) 迫使下一状态仍为 \((0,0)\)，并有 \(s=p/2\)。奇数长度时中央列也无进位。因此所有进位为零，输出回文，得到 (a)。

偶数长度时，从外侧的状态 \((0,0)\) 走到中央，两个进位最终是同一个中央进位，异或仍为零。累加式 (11)，得到 (b)。∎

**引理 3：增位输出的首两层限制。**
若 \(X=T(Y)\) 增位，且 \(q(X)_0=j\le9\)，则
\[
q(X)_1\ge j-1.
\tag{12}
\]
这里假定相应数位存在。因为最高位是 1，来源最外原始和必为 \(j+9\)，输出次高位为 \(j-1+c_{n-1}\)，已经至少为 \(j-1\)。∎

## 三、孤立数位的精确反推深度

**引理 4：孤立高对称和不能由增位产生。**
设 \(X\) 至少有 5 位，\(q(X)\) 的所有奇数位置为零，而每个偶数位置属于
\[
\{0,10,11,\ldots,18\}.
\]
则 \(X\) 不能是一次增位的反转相加输出。

证明：增位输出的首尾和至多为 10，因此只需考虑
\[
q(X)_0=10,\quad q(X)_1=q(X)_3=0,
\quad q(X)_2\notin\{1,2\}.
\]
设增位来源有 \(n\) 位，原始和为 \(s_i\)。由首尾和 10 得
\[
s_0=9,\quad c_1=0,\quad c_n=1.
\]
由 \(q(X)_1=0\)，次高位与次低位都为零，于是
\[
c_{n-1}=1,\qquad s_1=10,\qquad c_2=1.
\]
令 \(z=c_{n-2}\)。由 \(q(X)_3=0\)，特别有 \(b_{n-3}=0\)，故
\[
s_2+c_{n-3}=10z.
\]
因此 \((z,s_2)\) 只能为 \((0,0),(1,9),(1,10)\)。另一方面
\[
b_{n-2}=z,\qquad b_2=(s_2+1)\bmod10,
\]
所以
\[
q(X)_2=b_2+b_{n-2}\in\{1,2\},
\]
矛盾。中央数位重合时上述等式仍然成立，故五位情形也包括在内。∎

**引理 5：插零回文的精确深度。**
设 \(B\) 为至少有三个 1、且 1 的个数为奇数的二进制数位回文。令 \(U=I(B)\)。对任意 \(1\le d\le9\)，
\[
\max\{k:\exists A>0,\ T^k(A)=dU\}=v_2(d).
\tag{13}
\]
此处来源 \(A\) 不必是 11 的倍数。

证明：\(dU\) 为奇数长度回文，首两位为 \(d0\)，中央数位为 \(d\)。它不能是增位回文输出：增位输出首位必须为 1；首位为 1 的增位回文又具有形式 \(11W\)，其中 \(W\) 是二进制数位回文，因而第二位至少为 1，不能为零。

若 \(d\) 为奇数，不增位回文的中央数位必须是偶数，与中央数位 \(d\) 矛盾。所以深度为零。

若 \(d\) 为偶数，当然 \(T((d/2)U)=dU\)。若存在两步以上的来源，写最后两步为
\[
Y\longrightarrow X\longrightarrow dU.
\]
最后一步不增位且无进位，故 \(q(X)\) 就是 \(dU\) 的数位字。其最外两项是 \((d,0)\)，由式 (12)，\(Y\to X\) 不可能增位。又 \(q(X)\) 全为偶数，引理 2(a) 强制
\[
X=(d/2)U.
\]
因此每增加一层前驱，就必须再把 \(d\) 除以 2，直到奇数为止；逐次加倍也构造了达到该深度的路径。∎

**推论 5.1。**对上述 \(U\) 及 \(c\in\{10,12,14,16,18\}\)，在所有满足 \(q(X)=c\,\operatorname{digits}(U)\) 的 \(X\) 中，其可能拥有的最大前驱深度恰为
\[
v_2(c/2).
\tag{14}
\]
证明：引理 4 排除增位前驱；引理 2(a) 说明，一旦有前驱，\(X\) 必为回文 \((c/2)U\)。再用引理 5。这个回文本身也实现上界；当上界为零时，所有符合条件的 \(X\) 都无前驱。∎

## 四、把进位结构压缩为一个整数

本节只需要一个必要条件，而不依赖之前更完整的充要条件定理。

**引理 6：增位、无进位两步的进位对称性。**
若 \(X\to M\) 增位，\(M\to P\) 无进位，则第一步满足
\[
c_{i+1}=c_{n-i},\qquad u_i=s_i-9c_{i+1},
\tag{15}
\]
其中 \(u_i\) 组成一个合法回文 \(U\)，并且 \(P=11U\)。

证明：第二步无进位意味着 \(b_i+b_{n-i}\le9\)。从外侧得到 \(s_0\ge10\)，所以 \(c_1=c_n=1\)。令
\[
\delta_i=c_{i+1}-c_{n-i}.
\]
首尾缺陷均为零。

若第一个非零缺陷为 \(-1\)，两侧对同一原始和的进位判定迫使
\(s_i=9,c_i=0,c_{n-i-1}=1\)。于是 \(b_i=9\)。上一缺陷为零又给出
\(b_{n-i}=s_{i-1}+1\ge1\)，与第二步无进位矛盾。

若存在正缺陷，则同理有
\(s_i=9,c_i=1,c_{n-i-1}=0\)，从而 \(b_{n-i-1}=9\)。第二步无进位强制 \(b_{i+1}=0\)，继而
\(s_{i+1}=9,c_{i+2}=1\)，所以 \(\delta_{i+1}=1\)。正缺陷会一直传播到已知为零的末端，仍矛盾。因此全部缺陷为零。

令 \(e_i=c_{i+1}\)。则 \(e\) 对称，首尾为 1，且 \(u=s-9e\) 是合法回文数位字。直接计算（边界外的 \(u\) 记为零）得到
\[
b_i+b_{n-i}=u_i+u_{i-1}.
\]
故 \(P=11U\)。∎

设现在 \(P=D(V)\)，\(V\) 有 \(h\) 个非零数位、数位和为 \(w\)。由式 (1) 与唯一除法，引理 6 中的 \(U\) 必为 \(I(V)\)。其非零位置都是偶数位置。

每一个进位 1 段的起点都必须满足 \(u_i>0\)：启动进位时 \(e_{i-1}=0,e_i=1\)，式 (8) 要求 \(u_i\ge1\)。由对称性，每个 1 段的终点也在非零位置。因此每段的两个端点均为偶数位置，每段对交错和贡献恰为 1。

若共有 \(k\) 段，则
\[
1\le k\le h,\qquad
\sum_i(-1)^ie_i=k,
\qquad
\sum_i(-1)^iu_i=w.
\tag{16}
\]
来源 \(X\) 有奇数位数。中央原始和为偶数，故中央进位的奇偶性与 \(U\) 的中央数位一致。本文两个定理中的 \(V\) 均为奇数长度，此时 \(U=I(V)\) 的中央数位就是 \(V\) 的中央数位。特别地，当中央数位为奇数时，\(k\) 为奇数；中央数位为偶数时，\(k\) 为偶数。

如果 \(11\mid X\)，则
\[
0\equiv2X\equiv\sum_i(-1)^is_i
=w+9k\equiv w-2k\pmod{11}.
\tag{17}
\]

**关键后果。**若上述限制唯一允许 \(k=h\)，则所有进位段都必须是单点，且恰在 \(U\) 的非零位置上。于是
\[
\boxed{s_i=u_i+9\,\mathbf 1_{u_i>0}.}
\tag{18}
\]
原因是每段至少占用一个非零位置；\(h\) 个位置容纳 \(h\) 段时，每段只能占一个位置，其起止点必重合。

## 五、定理 A 的完整证明

设 \(B\) 恰有 11 个 1，\(U=I(B)\)，\(P_d=D(dB)\)。考察任意从 11 的倍数出发、在第 \(t\ge2\) 步到达 \(P_d\) 的路径。11 的整除性在反转相加中保持，所以倒数第二步的来源仍为 11 的倍数。

最后一步不能增位：若 \(d>1\)，首位不是 1；若 \(d=1\)，引理 1 强制上一步原始和为 \(11\operatorname{digits}(U)\)，但其中央项为 11，不可实现。

因此最后一步无进位。设最后两步为 \(X\to M\to P_d\)。

若 \(d\) 为奇数且 \(d\le7\)，\(X\to M\) 不能不增位：\(q(M)\) 是 \(P_d\) 的数位字，不含 9，其前半部恰有 11 个奇数项，违反引理 2(b)。所以只能是“增位、无进位”。式 (17) 给出
\[
11d-2k\equiv0\pmod{11},\quad 1\le k\le11,\quad k\text{ 为奇数},
\]
唯一解为 \(k=11\)。由式 (18)，
\[
q(X)=(d+9)\operatorname{digits}(U).
\]
用推论 5.1，\(X\) 的前驱深度至多 \(v_2((d+9)/2)\)，所以
\[
t\le2+v_2((d+9)/2).
\tag{19}
\]

若 \(d\) 为偶数，进位段数 \(k\) 必为偶数，且 \(k\le10\)，式 (17) 没有解。因此 \(X\to M\) 不增位。\(q(M)\) 全为偶数，引理 2(a) 迫使
\[
M=P_{d/2}.
\tag{20}
\]
故每剥去 \(d\) 的一个因子 2，上界恰增加一步。这证明式 (3) 的上界。

下面构造达到上界的起点。写 \(d=2^fu\)、\(a=(u+9)/2=2^er\)，其中 \(r\) 为奇数。取
\[
A=rU.
\]
\(U\) 的所有非零数位在偶数位置，且恰有 11 个，所以 \(U\equiv11\equiv0\pmod{11}\)，进而 \(11\mid A\)。

经过 \(e\) 次无进位加倍得到 \(aU\)。再经过两步，
\[
aU\longrightarrow(u+9)U\longrightarrow11uU=D(uB).
\tag{21}
\]
第一步输出在每个非零锚点产生数位对 \(1,(u-1)\)；与反转相加后，每一对成为 \(u,u\)。最后再加倍 \(f\) 次，得到 \(D(dB)\)。总步数为 \(e+2+f\)，恰等于上界。∎

例如取 \(B=11111111111\)，\(d=7\) 时达到五步上界的路径是
\[
\begin{aligned}
101010101010101010101
&\to202020202020202020202\\
&\to404040404040404040404\\
&\to808080808080808080808\\
&\to1616161616161616161616\\
&\to7777777777777777777777.
\end{aligned}
\]
这里起点已经是回文，符合式 (2) 允许所有中间情况的定义。

证明 196 推论：\(N_3=7436\) 是 11 的倍数，故定理 A 强制任何 \(d\le8\) 的目标若在 196 轨道出现，只能在 \(t\le3+5=8\) 时出现。但这些目标至少有 22 位，而
\[
(N_0,\ldots,N_8)=
(196,887,1675,7436,13783,52514,94039,187088,1067869).
\]
无一符合。对于 \(d=9\)，目标被 3 整除，而
\(N_t\equiv2^t196\not\equiv0\pmod3\)，同样不可能。∎

## 六、定理 B 的完整证明

设 \(V\) 满足定理 B，\(P=D(V)\)。由于 \(h\) 为奇数，\(V\) 为奇数长度，中央非零。

最后一步不能增位：增位回文必须形如 \(11W\)，\(W\) 为二进制数位回文。而这里唯一的商为 \(I(V)\)。若 \(V\) 含 3、5、7，则商不是二进制数位字；若全部非零数位都是 1，则商的中央项为 1，使来源中央原始和为 11，仍不合法。

若最后两步都不增位，倒数第一项的对称和就是 \(P\) 的数位字；它不含 9，前半部有奇数个奇数项 \(h\)，违反引理 2(b)。所以对于任何 \(t\ge2\) 的来源，最后两步只能为“增位、无进位”。

在 11 的倍数轨道中，式 (17) 给出
\[
k\equiv h\pmod{11},\qquad k\equiv h\pmod2,
\qquad 1\le k\le h\le21.
\]
也即 \(k\equiv h\pmod{22}\)，因此唯一可能是 \(k=h\)。由式 (18)，倒数第二项 \(X\) 的原始对称和满足：

- 奇数位置全为零；
- 非零项属于 \(\{10,12,14,16\}\)；
- 中央项为 10 或 14。

引理 4 排除 \(X\) 是增位输出的可能。若 \(X\) 是不增位输出，引理 2(a) 强制 \(X\) 为回文，且其数位是上述对称和的一半；中央数位因此为 5 或 7。引理 1 又要求不增位回文的中央数位为偶数，矛盾。

所以 \(X\) 没有任何前驱，所有 11 的倍数来源至多只能在两步内到达 \(P\)。

上界也可以达到：令 \(W\) 由 \(V\) 的数位逐个替换得到
\[
0\mapsto0,\quad1\mapsto5,\quad3\mapsto6,
\quad5\mapsto7,\quad7\mapsto8,
\]
并取 \(A=I(W)\)。则
\[
A\equiv\frac{w+9h}{2}\equiv0\pmod{11}.
\]
第一步在每个非零位置产生数位对 \(1,(v_j-1)\)；第二步与反转相加后，这些数位对成为 \((v_j,v_j)\)，且没有进位。因此 \(T^2(A)=D(V)\)，从而 \(H_{11}(P)=2\)。∎

对于 196，若在 \(t\ge3\) 时出现这种目标，式 (5) 强制 \(t\le5\)。另一方面，\(h=1,3\) 都不满足定理的数位和条件：\(h=1\) 时中央数位 1、5 均不等于 2 模 11；\(h=3\) 时数位和为 \(2a+c\)，其中 \(a\in\{1,3,5,7\}\)、\(c\in\{1,5\}\)，其值中没有 6 模 11 的数。因此实际 \(h\ge5\)，目标至少有十位，而 \(N_0,\ldots,N_5\) 均少于十位。得到式 (6)。∎

忽略零串长度，只统计非零数位构成的回文骨架，定理 B 的条件给出下表。每个骨架均允许任意对称零串；其中部分目标也可直接由模 3 排除，表中没有把它们扣除。

| 非零数位个数 \(h\) | 5 | 7 | 9 | 11 | 13 | 15 | 17 | 19 | 21 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 骨架数 | 7 | 1 | 71 | 167 | 579 | 4054 | 7800 | 58857 | 172801 |

## 七、验证记录及尚未解决的问题

附录程序本轮执行通过：

- 穷尽 76 种合法的局部不增位进位转移；
- 检查 75,447 个长度不超过 7 的可实现原始对称和字，核对直接加法与前驱算法，并核对全偶对称和引理；
- 精确反推 351 个插零回文，核对式 (13)，同时核对五种孤立高对称和值的深度；
- 对 256 个十一对同数字目标，核对全部最后两步分支及达到上界的构造；
- 对 492 个混合数字目标，核对全部最后两步分支及第三步障碍；
- 核对上表骨架数，以及 196 的前九项。

这些检查不代替无界参数的证明；无界零串由前述逐列论证处理。

本轮也尝试继续反推此前剩余的五对 7 分支，其关键原始对称和在五个锚点为 16，其余为 9。精确前驱自动机在资源上限处停止，尚未得到空语言；不能据此声称已排除。此前的 \(55\,0^{2r}\,55\) 分支也仍未排除。

更一般的回文目标还不满足本文的数位限制。因此，本文证明的是两类新的无限排除族与精确深度公式，没有完成“196 永远不产生任何回文”的全称命题。

## 附录：自包含核验程序

保存下列代码为 Python 文件后运行。仅使用标准库；不调用网络、不读取既有证明文件。

```python
from itertools import product
from collections import Counter
from functools import lru_cache

def T(n): return n+int(str(n)[::-1])
def D(v): return int(''.join(x*2 for x in str(v)))
def I(v): return int('0'.join(str(v)))
def ds(n): return tuple(map(int,str(n)[::-1]))
def q(n):
 a=ds(n);return tuple(x+y for x,y in zip(a,a[::-1]))
def normalize(s):
 a=[];carry=0
 for x in s:
  carry,x=divmod(x+carry,10);a.append(x)
 if carry:a.append(carry)
 return tuple(a)
def F(s):
 a=normalize(s);return tuple(x+y for x,y in zip(a,a[::-1]))
def feasible(s):
 return bool(s) and s[0]>0 and s==s[::-1] and all(0<=x<=18 for x in s) and (len(s)%2==0 or s[len(s)//2]%2==0)
def representative(s):
 a=[0]*len(s)
 for i in range(len(s)//2):
  a[-1-i]=max(1 if i==0 else 0,s[i]-9);a[i]=s[i]-a[-1-i]
 if len(s)%2:a[len(s)//2]=s[len(s)//2]//2
 return sum(d*10**i for i,d in enumerate(a))

@lru_cache(maxsize=10000)
def inverse(qt):
 # Exact inverse of F on feasible symmetric digit-sum words.
 L=len(qt);ans=set()
 for grow in (0,1):
  n=L-grow
  if n<1:continue
  half=(n+1)//2
  if not grow:
   states=[((),0,0)]
   for p in qt[:half]:
    nxt=[]
    for word,x,y in states:
     for u in range(1 if not word else 0,19):
      xx=(u+x)//10
      for yy in (0,1):
       if (u+yy)//10==y and 2*u+x+yy-10*(xx+y)==p:
        nxt.append((word+(u,),xx,yy))
    states=nxt
   words=[word for word,_,_ in states]
  else:
   if qt[0]>10:continue
   u=qt[0]+9 if qt[0]<=9 else 9
   states=[((u,),u//10,1)]
   for p in qt[1:half]:
    nxt=[]
    for word,x,y in states:
     for yy in (0,1):
      if (word[-1]+yy)//10!=y:continue
      b=p-word[-1]-yy+10*y
      if 0<=b<=9:
       for xx in (0,1):
        u=b+10*xx-x
        if 0<=u<=18:nxt.append((word+(u,),xx,yy))
    states=nxt
   words=[word for word,_,_ in states]
  for word in words:
   s=word+word[:n//2][::-1]
   if feasible(s) and F(s)==qt:ans.add(s)
 return tuple(sorted(ans))

def v2(n):
 k=0
 while n%2==0:k+=1;n//=2
 return k

def with_gaps(values,gaps):
 # Palindromic nonzero skeleton and its symmetric zero gaps.
 a=len(gaps);allgaps=tuple(gaps)+tuple(gaps)[::-1]
 assert len(values)==2*a+1
 return int(''.join(str(x)+('0'*allgaps[i] if i<len(allgaps) else '') for i,x in enumerate(values)))

def test_local():
 count=0
 for s,x,y,xx,yy in product(range(19),range(2),range(2),range(2),range(2)):
  if (s+x)//10!=xx or (s+yy)//10!=y:continue
  p=2*s+x+yy-10*(xx+y)
  if p!=9:
   assert xx==y
   assert (xx^yy)==(x^y^(p%2))
  count+=1
 total=0
 for n in range(1,8):
  if n==1:words=[(c,) for c in range(2,19,2)]
  else:
   words=[]
   for first in range(1,19):
    for mid in product(range(19),repeat=n//2-1):
     left=(first,)+mid
     if n%2:
      words.extend(left+(c,)+left[::-1] for c in range(0,19,2))
     else:words.append(left+left[::-1])
  for s in words:
   a=normalize(s);p=F(s)
   if len(a)==n and all(x%2==0 for x in p):assert a==a[::-1]
   # The inverse algorithm must recover every actual source.
   assert s in inverse(p)
   total+=1
 print('local carry transitions:',count,'actual raw words:',total,flush=True)

def test_sparse_height():
 count=0
 for h in (3,5,7):
  for gaps in product(range(3),repeat=(h-1)//2):
   B=with_gaps((1,)*h,gaps);U=I(B)
   for d in range(1,10):
    p=ds(d*U)
    states={p} if feasible(p) else set();height=0
    while states:
     height+=1
     states={s for z in states for s in inverse(z)}
     assert height<=4
    assert height==v2(d),(B,d,height)
    count+=1
   for c in (10,12,14,16,18):
    raw=tuple(c*x for x in ds(U));states={raw};height=-1
    while states:
     height+=1;states={s for z in states for s in inverse(z)}
     assert height<=4
    assert height==v2(c//2),(B,c,height)
 print('sparse palindrome height cases:',count,flush=True)

def test_eleven():
 cases=0
 for gaps in product(range(2),repeat=5):
  B=with_gaps((1,)*11,gaps);U=I(B)
  for d in range(1,9):
   p=D(d*B);raw=ds(p);parents=inverse(raw)
   nn={s for s in parents if len(s)==len(raw)}
   gn={s for s in parents if len(s)==len(raw)-1 and representative(s)%11==0}
   assert nn==({tuple(x//2 for x in raw)} if d%2==0 else set()),(d,B,'NN')
   expected=tuple((d+9)*x for x in ds(U))
   assert gn==({expected} if d%2 else set()),(d,B,'GN')
   f=v2(d);u=d//2**f;a=(u+9)//2;e=v2(a);root=(a//2**e)*U
   assert root%11==0
   n=root
   for _ in range(f+e+2):n=T(n)
   assert n==p,(d,B,'sharpness')
   cases+=1
 print('eleven-one skeletons, exact last-two-step branches and sharp constructions:',cases,flush=True)

def test_mixed():
 cases=0
 for h in (5,7,9,11):
  a=(h-1)//2
  for left in product((1,3,5,7),repeat=a):
   for center in (1,5):
    values=left+(center,)+left[::-1]
    if (sum(values)-2*h)%11:continue
    for gaps in ((0,)*a,tuple((i+sum(left))%3 for i in range(a))):
     v=with_gaps(values,gaps);raw=ds(D(v));parents=inverse(raw)
     assert not any(len(s)==len(raw) for s in parents),(v,'NN')
     gn={s for s in parents if len(s)==len(raw)-1 and representative(s)%11==0}
     expected=tuple(x+9 if x else 0 for x in ds(I(v)))
     assert gn=={expected},(v,'GN')
     assert not inverse(expected),(v,'extra ancestor')
     cases+=1
 print('mixed-digit targets, all two-step branches and third-step obstruction:',cases,flush=True)

def count_skeletons():
 counts=[]
 for h in range(1,22,2):
  c=Counter({0:1})
  for _ in range((h-1)//2):
   nxt=Counter()
   for r,n in c.items():
    for d in (1,3,5,7):nxt[(r+d)%11]+=n
   c=nxt
  count=sum(n for r,n in c.items() for center in (1,5) if (2*r+center-2*h)%11==0)
  counts.append((h,count))
 assert counts==[(1,0),(3,0),(5,7),(7,1),(9,71),(11,167),(13,579),(15,4054),(17,7800),(19,58857),(21,172801)]
 print('mixed-digit skeleton counts:',counts,flush=True)

if __name__=='__main__':
 test_local();test_sparse_height();test_eleven();test_mixed();count_skeletons()
 n=196;early=[]
 for _ in range(9):early.append(n);n=T(n)
 assert early==[196,887,1675,7436,13783,52514,94039,187088,1067869]
 print('196 initial segment:',early,flush=True)
```
