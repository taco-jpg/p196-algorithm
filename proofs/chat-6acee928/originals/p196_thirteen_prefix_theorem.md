# P196 的继续推进：十三类回文首部的精确反推深度

本轮得到一个与数位长度无关的结论：只指定回文的前两位，就能对十三种首部给出统一、可达到的前驱深度上界。中间数位可以任意变化，不限制非零数位数量，不要求数位成对重复，也不要求来源是 11 的倍数。

这些结论排除了 196 轨道中的十三类无限回文集合，但没有证明完整的 P196 猜想。本文不作文献首创判断。无限范围的结论由下文逐列进位证明；附录程序用于独立核验。

## 1. 定理

定义
\[
T(N)=N+\operatorname{rev}(N),\qquad
H(P)=\max\{k\ge0:\exists A\in\mathbb Z_{>0},\ T^k(A)=P\}.
\]
反转忽略前导零。由于 \(T(N)>N\)，对固定的 \(P\)，上述最大值总是有限的。

**定理。**若 \(P\) 是十进制回文，其前两位为下表中的首部，则有对应的上界。每一个上界都可以达到，而且可以在最后一步才首次出现回文。

| 回文前两位 | 对这一类所有回文成立的上界 |
|---|---:|
| 10 | \(H(P)\le1\) |
| 20、32 | \(H(P)\le2\) |
| 40、41、60、64、76 | \(H(P)\le3\) |
| 80、81、82、83 | \(H(P)\le4\) |
| 65 | \(H(P)\le6\) |

这里的上界允许中间出现其他回文。特别地，任何以 65 开头的回文都不属于 \(T^7(\mathbb Z_{>0})\)。

**196 推论。**令 \(N_t=T^t(196)\)。对任意 \(t\ge0\)，\(N_t\) 都不可能是具有上述十三种首部之一的回文。

## 2. 数位对称和与进位

对 \(n\) 位正整数 \(X\)，从低位开始记数位为 \(a_i\)，定义
\[
q(X)_i=a_i+a_{n-1-i}=s_i.
\]
则 \(s\) 是对称字，\(0\le s_i\le18\)，\(s_0>0\)，且奇数长度的中央项为偶数。

计算 \(T(X)\) 时，
\[
c_0=0,\qquad
c_{i+1}=\left\lfloor\frac{s_i+c_i}{10}\right\rfloor,
\qquad b_i=s_i+c_i-10c_{i+1}.
\tag{1}
\]
若 \(c_n=1\)，添上最高位 \(b_n=1\)，称这一步增位；否则称不增位。把 \(s\) 依式 (1) 规范化，再取输出的对称数位和，记为 \(F(s)\)。因此
\[
q(T(X))=F(q(X)).
\tag{2}
\]

下文的三元组均表示从外向内的三个对称数位和；它们不是三位十进制整数。例如 \((1,11,2)\) 中的 11 是两个相对数位之和。

## 3. 下降的首两位，强迫最后两步都不增位

**引理 1。**设回文 \(P\) 的前两位为 \(a,b\)，且 \(b<a\)。任何两步路径
\[
X\longrightarrow M\longrightarrow P
\]
的两步均不增位；最后一步完全没有进位。因此 \(q(M)\) 恰好是 \(P\) 的数位字。

**证明。**先看最后一步。

若最后一步增位，回文首尾都是 1，来源最外对称和必为 11。此时输出次高位为 \(1+c_{n-1}\)，至少为 1，不可能小于最高位。这与 \(b<a\) 矛盾。

所以最后一步不增位。此时 \(c_0=c_n=0\)。比较输出的相对数位，回文性给出
\[
c_i-c_{n-1-i}=10(c_{i+1}-c_{n-i}).
\]
左侧绝对值不超过 1，右侧是 10 的倍数，所以两边均为零。从边界向内递推，得到所有进位为零。于是 \(q(M)\) 就是 \(P\) 的数位字，各项都不超过 9。

再反设 \(X\to M\) 增位。令 \(X\) 有 \(n\) 位，使用式 (1) 的记号。由于 \(q(M)_0=a\le9\)，
\[
s_0=a+9,\qquad c_1=c_n=1.
\]
次外对称和为
\[
q(M)_1=b_1+a-1+c_{n-1}.
\]
若它小于 \(a\)，唯一可能是
\[
b=a-1,\quad b_1=0,\quad c_{n-1}=0.
\]
由 \(c_1=1\)、\(b_1=0\) 得 \(s_1=9,c_2=1\)。来源的对称性及 \(c_{n-1}=0\) 又给出 \(c_{n-2}=0\)。此时输出相应的高端数位为 9。由于 \(q(M)_2\le9\)，对应低端数位只能为零，于是
\[
s_2=9,\quad c_3=1,\quad c_{n-3}=0.
\]
同一推导不断重复：低端进位始终为 1，高端相对进位始终为 0。继续向内必使同一个进位同时等于 0 和 1，矛盾。

更形式化地，若已有 \(s_j=9,c_{j+1}=1,c_{n-j}=0\)，高端列方程先强迫 \(c_{n-j-1}=0\)；该输出高端数位为 9，条件 \(q(M)_{j+1}\le9\) 再强迫 \(s_{j+1}=9,c_{j+2}=1\)。这一归纳最终与 \(c_1=1\) 矛盾。\(n=2\) 时初始条件 \(c_{n-1}=0\) 已直接与 \(c_1=1\) 矛盾。

因此前一步也不增位。∎

十三种首部全部满足 \(b<a\)，所以此引理同时适用于它们。

## 4. 不增位的精确反推公式

在一层外侧数位对上，记
\[
x=c_i,\quad y=c_{n-i},\quad
x'=c_{i+1},\quad y'=c_{n-1-i}.
\]
若来源对称和为 \(s\)，输出对称和为 \(p\)，则
\[
x'=\left\lfloor\frac{s+x}{10}\right\rfloor,
\quad y=\left\lfloor\frac{s+y'}{10}\right\rfloor,
\quad p=2s+x+y'-10(x'+y).
\tag{3}
\]
不增位的外边界为 \((x,y)=(0,0)\)。

当 \(p\ne9\) 时，
\[
x'=y,\qquad y'=x\mathbin{\oplus}(p\bmod2),
\qquad s=10y+\frac{p-x-y'}2.
\tag{4}
\]
因为如果 \(x'\ne y\)，相同的来源列和在两端产生不同的出进位，只可能发生于 \(s=9\)，代入式 (3) 必得 \(p=9\)。式 (4) 随即由式 (3) 得到。仍须保留 \(0\le s\le18\) 及外层 \(s>0\) 的条件。

对于例外 \(p=9\)，全部合法选择如下，表项为 \((s,x',y')\)：

| 当前 \((x,y)\) | 全部选择 |
|---|---|
| \((0,0)\) | \((4,0,1)\) |
| \((0,1)\) | \((9,0,1),(14,1,1)\) |
| \((1,0)\) | \((4,0,0),(9,1,0)\) |
| \((1,1)\) | \((14,1,0)\) |

这张小表是不能省略的：在部分行中，第三个对称和可以额外取到 9。

## 5. 增位的外侧限制

不增位输出的最外对称和至少为 2。

若增位输出的最外对称和为 \(j\le9\)，则来源最外和为 \(j+9\)，输出的第二项 \(p\) 满足
\[
j-1\le p\le j+9.
\tag{5}
\]
若第三项记为 \(z\)，还满足
\[
\begin{cases}
z\ge9,&p=j-1,\\
z\ge\max(0,p-j-1),&p\ge j.
\end{cases}
\tag{6}
\]
推导：次高输出数位为 \(j-1+y\)，其中 \(y\in\{0,1\}\)。第二来源和为 \(s_1\)，则第二低输出数位为 \((s_1+1)\bmod10\)。当 \(p=j-1\) 时，这两项强迫 \(y=0,s_1=9\)，下一高端输出数位为 9，得到第一行。其余情形分别取 \(y=0,1\)，下一高端输出数位至少为 \(p-j\) 或 \(p-j-1\)，得到第二行。

本文反复使用的“不可能有前驱”的前缀为
\[
\begin{aligned}
&(1,b,z),&&b>10;\\
&(1,0,z),&&z<9;\\
&(1,10,z),&&z<8.
\end{aligned}
\tag{7}
\]
不增位因首项为 1 而不可能；增位分别违反式 (5) 或式 (6)。

另外，\((3,2,z)\) 若由增位产生，必须 \(z\ge9\)。\((3,0,z)\)、\((2,0,z)\)、\((4,0,z)\)、\((4,1,z)\) 则直接违反式 (5)。

## 6. 十二种首部的手算反推表

假设 \(T^k(A)=P\)，\(k\ge2\)，并令 \(M\) 为 \(P\) 的前一项。定义
\[
Q_0=q(M),\qquad F(Q_{r+1})=Q_r
\]
表示继续向前反推的对称和字。

若 \(P\) 首部为 \(ab\)，则 \(Q_0\) 的前三项为 \((a,b,c)\)，其中 \(0\le c\le9\)。引理 1 使第一层反推只能不增位。之后必须检查两种增位模式。

以下记 \((a,b;S)\) 为第三项在集合 \(S\) 中的全部三元组，\([u,v]\) 表示整数区间。应用式 (3)—(7)，得到下表。各格是实际前驱前缀的超集，因此可以忽略尚未使用的中央对称性；这不会误删任何实际路径。

| 首部 | \(Q_1\) 的必要前缀 | \(Q_2\) 的必要前缀 | \(Q_3\) 的必要前缀 | 首次空层 |
|---|---|---|---|---:|
| 10 | 空 | — | — | 1 |
| 20 | \((1,0;[0,4])\) | 空 | — | 2 |
| 32 | \((1,11;\{0,1,2,3,4,9\})\) | 空 | — | 2 |
| 40 | \((2,0;[0,4])\) | \((1,0;[0,2])\) | 空 | 3 |
| 41 | \((2,0;[9,14])\) | \((1,0;[4,7])\) | 空 | 3 |
| 60 | \((3,0;[0,4])\) | \((1,10;\{0,1\})\) | 空 | 3 |
| 64 | \((3,2;[0,4])\) | \((1,11;\{0,1\})\) | 空 | 3 |
| 76 | \((3,13;\{0,1,2,3,4,9\})\) | \((1,16;\{9,10,11,14\})\) | 空 | 3 |
| 80 | \((4,0;[0,4])\) | \((2,0;[0,2])\) | \((1,0;\{0,1\})\) | 4 |
| 81 | \((4,0;[9,14])\) | \((2,0;[4,7])\) | \((1,0;\{2,3\})\) | 4 |
| 82 | \((4,1;[0,4])\) | \((2,0;[10,12])\) | \((1,0;\{5,6\})\) | 4 |
| 83 | \((4,1;[9,14])\) | \((2,0;\{9,14,15,16,17\})\) | \((1,0;\{4,7,8\})\) | 4 |

这里每一条未终止的反推均被强制为不增位：除了第 5 节已经列出的前缀，\((3,13,z)\) 违反 \(p\le j+9=12\)；\((3,2,z)\) 在本表的第三项不超过 4，违反增位所需的 \(z\ge9\)。终止格使用式 (7)。

例如首部 83：第一次不增位反推给出
\[
(8,3,c)\rightsquigarrow(4,1;[9,14]).
\]
随后不增位反推为
\[
(2,0;\{9,14,15,16,17\})
\rightsquigarrow(1,0;\{4,7,8\}),
\]
最后一个集合因第三项全部小于 9 而没有前驱。表中的额外数值 9 来自第 4 节的例外进位表。

若第 \(h\) 层为空，则必须 \(k-1<h\)，即 \(k\le h\)。这证明十二种首部的所列上界。

## 7. 首部 65：六层障碍的完整证明

仍从 \(Q_0=(6,5,c,\ldots)\)、\(0\le c\le9\) 开始。第一步只能不增位。式 (3)、(4) 给出
\[
Q_1\text{ 的前缀属于 }(3,2;[9,14]).
\tag{8}
\]

此处必须保留两类前驱。

若 \(Q_1\) 来自不增位，其前驱前缀属于
\[
(1,11;\{4,5,6,9\}).
\]
这些字再没有前驱，因而这一分支很快终止。

若 \(Q_1\) 来自增位，前两项 \((3,2)\) 强制来源前两项为 \((12,9)\)。若 \(Q_1\) 第三项为 \(v\)，则下一高端输出数位为 9，下一低端输出数位为 \(v-9\)。令该列低端出进位为 \(x'\)，来源第三项为
\[
s_2=v-10+10x'.
\]
高端出进位为零要求 \(s_2\le9\)。因此 \(v=9\) 时只能 \(s_2=9\)，而 \(10\le v\le14\) 时只能 \(s_2=v-10\)。于是这个增位分支给出
\[
(12,9;\{0,1,2,3,4,9\}).
\]

完整的反推表是

| 层数 | 全部必要前缀 |
|---:|---|
| 0 | \((6,5;[0,9])\) |
| 1 | \((3,2;[9,14])\) |
| 2 | \((1,11;\{4,5,6,9\})\ \cup\ (12,9;\{0,1,2,3,4,9\})\) |
| 3 | \((6,4;\{9,10,11,12,14\})\) |
| 4 | \((3,2;\{4,5,6,7\})\) |
| 5 | \((1,11;\{1,2,3\})\) |
| 6 | 空 |

第二层中首项为 12 的分支不能有增位前驱，因为任何增位输出的最外对称和至多为 10。第三层的 \((6,4)\) 违反增位下界 \(4\ge6-1\)，所以只能不增位。第四层虽然仍以 \((3,2)\) 开头，但第三项至多为 7，违反增位所需的第三项至少为 9，因此也只能不增位。第五层首部 \((1,11)\) 由式 (7) 没有任何前驱。

故 \(Q_6\) 不可能存在，得到
\[
\boxed{P\text{ 回文且以 65 开头}\ \Longrightarrow\ H(P)\le6.}
\tag{9}
\]

**短位数边界。**十三种首部都不是两个相同数字，所以相应回文至少有三位，前三项总存在。十二种首部的表中，所有实际可继续的步骤均不增位，不会丢失第三项。65 表中唯一可继续的增位反推发生在 \((3,2;[9,14])\) 处；若目标只有三位，对称性会要求第三项等于第一项 3，与该集合矛盾。因此该增位分支出现时来源至少有三位。所有表均覆盖短位数情形，不需要假定目标很长。∎

## 8. 每个上界都可以在首次回文时达到

下表列出起点与首次回文。每一行按 \(T\) 迭代，首次回文恰在指定步数出现。

| 首部 | 起点 | 首次回文步数 | 首次回文 |
|---|---:|---:|---:|
| 10 | 100 | 1 | 101 |
| 20 | 1005000 | 2 | 2010102 |
| 32 | 12090 | 2 | 32223 |
| 40 | 1008000 | 3 | 4034304 |
| 41 | 1008400 | 3 | 4194914 |
| 60 | 1103090 | 3 | 6034306 |
| 64 | 1203090 | 3 | 6434346 |
| 65 | 1203290 | 6 | 65477456 |
| 76 | 17590 | 3 | 76667 |
| 80 | 1009000 | 4 | 8074708 |
| 81 | 1009200 | 4 | 8136318 |
| 82 | 1006500 | 4 | 8250528 |
| 83 | 1009400 | 4 | 8394938 |

65 的例子完整写为
\[
\begin{aligned}
1203290&\longrightarrow2126311\\
&\longrightarrow3262523\\
&\longrightarrow6515146\\
&\longrightarrow12930302\\
&\longrightarrow33234223\\
&\longrightarrow65477456.
\end{aligned}
\]
前六个数都不是回文，最后一个是回文。此外 \(1203290=11\cdot109390\)，所以即使要求起点是 11 的倍数，65 族的六步上界仍不能缩短。

上界加上这些构造，给出了每个首部类别的精确最大前驱深度；不是仅仅找到了一个可能偏松的常数。

## 9. 196 的推论与尚未解决的部分

若上述任何目标 \(P\) 在 \(N_t=T^t(196)\) 中出现，主定理强制 \(t\le6\)。但
\[
N_0,\ldots,N_6
=196,887,1675,7436,13783,52514,94039
\]
均不是回文。因此十三类回文在 196 的轨道中全部被排除，且是对所有时刻的排除。

这次的推广不限制中间数位的排列，也不限制非零数位数量。它和此前依赖成对数位、进位段计数的排除族属于不同的覆盖方式。

仍缺少把所有可能的首次回文纳入已排除集合的全局论证。特别是，这次的首部集合不含 55 或 77，因此此前的 \(55\,0^{2r}\,55\) 与五对 7 的剩余分支没有被本定理解决。十三种首部的精确深度上界不能解释为所有回文的统一等待上界，也不能解释为完整 P196 证明只剩有限个具体数字。

## 10. 核验记录

附录程序使用 Python 标准库，完成了以下核验：

- 从整数列运算直接构造 75,420 个长度为 3 至 7 的可实现原始对称和字，检查前缀反推规则覆盖真实前驱。其中 39,804 个为增位情形，8,910 个符合“增位后无进位”，并核对其回文首部不能下降。
- 独立核对两位来源增至三位的边界公式。
- 复现十三张有限前缀表，确认指定层为空。
- 对所有小于一百万的正整数按 \(T(N)>N\) 作精确动态规划，核对其中符合十三类首部的 286 个回文的实际最大前驱深度。
- 逐步验证十三条锐性路径、65 例子的 11 整除性，以及 196 的前七项。

65 的有限前缀集合大小依次为
\[
10,6,10,5,4,3,0.
\]
这里处理的是全部允许前缀的集合。无限长度的覆盖性来自进位方程和第 7 节的边界论证，不来自整数扫描的长度上限。

## 附录：自包含核验代码

将下面代码保存为 Python 文件运行。它不读取其他证明文档，也不访问网络。

```python
"""Independent finite checks for the thirteen palindromic prefix theorem.

The unbounded-length proof is the carry argument and finite prefix tables in
the accompanying report. The integer scan here is a cross-check, not a
substitute for that proof. Python standard library only.
"""
from collections import defaultdict
from functools import lru_cache
from itertools import product

BOUNDS = {(1, 0): 1, (2, 0): 2, (3, 2): 2, (4, 0): 3,
          (4, 1): 3, (6, 0): 3, (6, 4): 3, (6, 5): 6,
          (7, 6): 3, (8, 0): 4, (8, 1): 4, (8, 2): 4, (8, 3): 4}
SHARP_ROOTS = {(1, 0): 100, (2, 0): 1005000, (3, 2): 12090,
               (4, 0): 1008000, (4, 1): 1008400, (6, 0): 1103090,
               (6, 4): 1203090, (6, 5): 1203290, (7, 6): 17590,
               (8, 0): 1009000, (8, 1): 1009200, (8, 2): 1006500,
               (8, 3): 1009400}


def T(n):
    return n + int(str(n)[::-1])


def pal(n):
    a = str(n)
    return a == a[::-1]


def normalize(s):
    out, carry = [], 0
    for u in s:
        carry, d = divmod(u + carry, 10)
        out.append(d)
    if carry:
        out.append(carry)
    return tuple(out)


def forward(s):
    d = normalize(s)
    return tuple(a + b for a, b in zip(d, d[::-1]))


@lru_cache(None)
def inv_nongrowth(p):
    # Read the known outer columns from the two ends. Leave the interior free.
    states = {((), 0, 0)}
    for i, v in enumerate(p):
        nxt = set()
        for word, x, y in states:
            for s in range(1 if i == 0 else 0, 19):
                xx = (s + x) // 10
                for yy in (0, 1):
                    if ((s + yy) // 10 == y
                            and 2 * s + x + yy - 10 * (xx + y) == v):
                        nxt.add((word + (s,), xx, yy))
        states = nxt
    return frozenset(word for word, _, _ in states)


@lru_cache(None)
def inv_growth(p):
    if p[0] > 10:
        return frozenset()
    first = p[0] + 9 if p[0] <= 9 else 9
    states = {((first,), first // 10, 1)}
    for v in p[1:]:
        nxt = set()
        for word, x, y in states:
            for yy in (0, 1):
                if (word[-1] + yy) // 10 != y:
                    continue
                digit = v - word[-1] - yy + 10 * y
                if not 0 <= digit <= 9:
                    continue
                for xx in (0, 1):
                    s = digit + 10 * xx - x
                    if 0 <= s <= 18:
                        nxt.add((word + (s,), xx, yy))
        states = nxt
    # There must be a legal carry entering the last known high column.
    return frozenset(word for word, x, y in states
                     if any((word[-1] + z) // 10 == y for z in (0, 1)))


@lru_cache(None)
def inv_prefix(p):
    return inv_nongrowth(p) | inv_growth(p)


def raw_words(n):
    half = n // 2
    for first in range(1, 19):
        for tail in product(range(19), repeat=half - 1):
            left = (first,) + tail
            if n % 2:
                for center in range(0, 19, 2):
                    yield left + (center,) + left[::-1]
            else:
                yield left + left[::-1]


def coverage_check():
    count = growth_count = gn_count = 0
    for n in range(3, 8):
        for s in raw_words(n):
            d = normalize(s)
            p = forward(s)
            grow = len(d) > n
            inverse = inv_growth if grow else inv_nongrowth
            assert s[:3] in inverse(p[:3]), (s, p)
            if grow:
                growth_count += 1
                # A growth step followed by a carry-free step cannot make
                # a palindrome with a descending first digit pair.
                if max(p) <= 9:
                    assert p[1] >= p[0], (s, p)
                    gn_count += 1
            count += 1
    # A two-digit source growing to three digits has a special short boundary.
    for s in range(10, 19):
        assert forward((s, s)) == (s - 9, 2 * (s - 9), s - 9)
    return count, growth_count, gn_count


def prefix_certificates():
    all_layers = {}
    for ab, bound in BOUNDS.items():
        layer = {(ab[0], ab[1], c) for c in range(10)}
        layers = [layer]
        for depth in range(1, bound + 1):
            inverse = inv_nongrowth if depth == 1 else inv_prefix
            layer = {s for p in layer for s in inverse(p)}
            layers.append(layer)
        assert not layers[-1], (ab, layers[-1])
        assert all(layers[:-1])
        all_layers[ab] = layers
    return all_layers


def actual_integer_check(limit=1_000_000):
    # Exact heights for all targets below limit: T(n)>n, so ascending dynamic
    # programming has already seen every predecessor when it processes n.
    heights = bytearray(limit)
    checked = 0
    for n in range(1, limit):
        value = T(n)
        if value < limit:
            heights[value] = max(heights[value], heights[n] + 1)
        ds = str(n)
        if len(ds) >= 3 and ds == ds[::-1]:
            ab = (int(ds[0]), int(ds[1]))
            if ab in BOUNDS:
                assert heights[n] <= BOUNDS[ab], (n, heights[n])
                checked += 1
    return checked


def sharpness_check():
    result = {}
    for ab, root in SHARP_ROOTS.items():
        path = [root]
        for _ in range(BOUNDS[ab]):
            path.append(T(path[-1]))
        assert not any(map(pal, path[:-1]))
        assert pal(path[-1])
        assert str(path[-1]).startswith(''.join(map(str, ab)))
        result[ab] = path
    assert SHARP_ROOTS[(6, 5)] % 11 == 0
    orbit = [196]
    for _ in range(max(BOUNDS.values())):
        orbit.append(T(orbit[-1]))
    assert orbit == [196, 887, 1675, 7436, 13783, 52514, 94039]
    assert not any(map(pal, orbit))
    return result


if __name__ == '__main__':
    layers = prefix_certificates()
    print('Exact finite prefix certificates:')
    for ab, chain in layers.items():
        print(''.join(map(str, ab)), [len(s) for s in chain])
    print('Direct carry-coverage checks:', coverage_check())
    print('Palindrome targets checked below one million:', actual_integer_check())
    print('Sharp first-hit paths:')
    for ab, path in sharpness_check().items():
        print(''.join(map(str, ab)), path)
    print('All checks passed. This does not prove the full 196 conjecture.')
```
