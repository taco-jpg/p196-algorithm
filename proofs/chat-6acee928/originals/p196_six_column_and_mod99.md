# P196：78、85 首部排除定理与模 99 轨道不可区分构造

日期：2026-10-14。本报告继续上一轮的四位置进位研究。下面是部分定理与完整可运行证书，**不是完整的 196 猜想证明**。不主张这些结果已经过文献查新、同行评审或形式化证明。

设

\[
T(n)=n+\operatorname{rev}(n),\qquad
H(P)=\max\{k\ge0:\exists A>0,\ T^k(A)=P\}.
\]

所有数均为十进制正整数，反转后舍弃前导零；迭代中途即使出现回文也继续计算。

本轮的正面结论是

\[
\boxed{P\text{ 回文且首两位为 }78\implies H(P)\le40,}
\]
\[
\boxed{P\text{ 回文且首两位为 }85\implies H(P)\le38.}
\]

两条上界都与位数及内部数字无关，不要求起点被 11 整除。它们是有限状态计算证明得到的上界，**尚未证明最优**。

再加本轮另外 25 种三位首部，已排除的三位首部总数由 360 增至 **396**；完整二位首部类别由 14 增至 **16**。另一方面，本轮还构造了无穷多个第 10 步首次成为回文的数，其整个模 99 轨迹与 196 从第 3 步起完全相同。这准确限制了仅靠模 9、11、99 信息的证明方法。

## 1. 数位模型及最后一步的必要条件

将 \(X\) 的数位从低到高写成 \(a_0,\ldots,a_{n-1}\)，定义对称和

\[
q(X)_i=a_i+a_{n-1-i}=s_i.
\]

\(s\) 对称，项属于 \(0,\ldots,18\)，首项正，奇数长度的中央项为偶数。反转相加的进位公式为

\[
c_0=0,\qquad c_{i+1}=\left\lfloor\frac{s_i+c_i}{10}\right\rfloor,
\qquad b_i=s_i+c_i-10c_{i+1}.
\tag{1}
\]

进位只能为 0、1。最高进位为 1 时称增位，记 G；否则称不增位，记 N。把 \(s\) 规范化为输出数字后再取对称和，记此映射为 \(F\)，则

\[
q(T(X))=F(q(X)).
\tag{2}
\]

如果 \(T(X)\) 是回文且不增位，比较对称位置得

\[
c_i-c_{n-1-i}=10(c_{i+1}-c_{n-i}).
\]

两侧必须同为零；从边界向内归纳，所有进位为零。因此 \(q(X)\) 恰为该回文的数位字。

如果回文由增位产生，其首位为 1。更精确地，由首尾输出均为 1 得 \(s_0=11\)，向内比较可得全部 \(s_i\in\{0,11\}\)。写 \(s_i=11e_i\)，输出数位为 \(e_i+e_{i-1}\)，其中 \(e_i\in\{0,1\}\)、边界外为零。因此长度至少 3 的增位回文，前三位只可能为

\[
110,111,121,122.
\tag{3}
\]

本轮所有目标首部均不属于这四类。所以它们的最后一步都是无进位步骤，前驱的 \(q\) 字全部属于 \(0,\ldots,9\)。

## 2. 六位置逆推没有遗漏真实进位

在 N 步中，从外向内读入原始和 \(s\)，保存低端输入进位 \(x\) 和高端输出进位 \(y\)。向内进位为 \(x',y'\)，输出对称和为 \(p\)，条件是

\[
x'=\lfloor(s+x)/10\rfloor,\quad
y=\lfloor(s+y')/10\rfloor,\quad
p=2s+x+y'-10(x'+y).
\tag{4}
\]

从 \((x,y)=(0,0)\) 开始，枚举所有 \(s\in\{0,\ldots,18\}\) 与 \(y'\in\{0,1\}\)，首项要求 \(s>0\)。

在 G 步中，目标首对称和 \(p_0\le9\) 对应来源首项 \(s_0=p_0+9\)；若 \(p_0=10\)，则 \(s_0=9\)；若 \(p_0>10\)，此分支不可能。初态为

\[
x=\lfloor s_0/10\rfloor,\qquad y=1.
\]

设已知前一个来源项 \(v\)，下一目标项为 \(p_i\)。枚举 \(y'\in\{0,1\}\) 满足

\[
\lfloor(v+y')/10\rfloor=y,
\]

然后要求

\[
d=p_i-v-y'+10y\in\{0,\ldots,9\},\qquad
s_i=d+10x'-x\in\{0,\ldots,18\},
\tag{5}
\]

其中 \(x'\in\{0,1\}\)。更新状态为 \((x',y')\)。最后还检查最后一个已知高端列存在合法输入进位。

程序使用这两组公式读取六个位置。它允许未知内部自由延伸，因而可能保留不能在中央闭合的假路径，但每个真实步骤必在其枚举之内。**排除一个上近似集合中的全部路径，足以排除真实路径。**

还使用一个已证明的边界引理：如果回文 \(P\) 的前两位为 \(a,b\)，且 \(b<a\)，那么在任何两步链 \(X\to M\to P\) 中，\(X\to M\) 也不增位。

简证：假设前一步增位，输出首对称和为 \(a\le9\)，来源首项为 \(a+9\)。第二项至少为 \(a-1\)，下降只能取 \(b=a-1\)。此时来源第二项被迫为 9，两侧相应进位分别为 1 和 0。此后对称和至少为 9；最后一步无进位又要求它至多为 9，因此必须恰为 9，这个进位差持续向内传播，最终同一中央进位被要求既为 0 又为 1，矛盾。短长度直接使用对称性检查；两位来源增至三位时输出对称和为 \((j,2j,j)\)，不可能下降。

所以对 85 类及其他下降首部，第一次逆推只用 N；之后每次均保留 N、G 两种模式。

## 3. 78 与 85 的有限证书如何结束

对 \(ab=78\) 或 \(85\)，令

\[
R_0^{ab}=\{(a,b,d_2,d_3,d_4,d_5):0\le d_i\le9\}.
\]

令 \(R_{r+1}\) 是 \(R_r\) 所有允许逆像首部的并集，85 类第一步限定 N。逐列计算得到：

| 位置 | 78 类 | 85 类 |
|---|---:|---:|
| 初始集合 | 10000 | 10000 |
| 第一次逆推 | 66383 | 6231 |
| 第二次逆推 | 36630 | 3919 |
| 进入相同集合的深度 | 25 | 23 |
| 此相同集合的大小 | 344 | 344 |
| 倒数第二个非空集合大小 | 41 | 41 |
| 最后非空集合的深度 | 39 | 37 |
| 最后非空集合大小 | 35 | 35 |
| 空集的深度 | 40 | 38 |

这里不仅是基数相同，程序还检查

\[
R_{25}^{78}=R_{23}^{85}.
\]

最后的 35 个六元组投影到前三项，恰好只剩

\[
(1,8,3),\qquad(1,9,6).
\tag{6}
\]

这两个短首部本身都不可能有前驱。证明很短：不增位输出的首对称和至少为 2，所以首项为 1 必须来自增位，来源首项为 10。若输出第二项为 \(b\ge2\)，设进入来源最高列的进位为 \(y\)：

- \(y=0\) 时，来源第二项为 \(b-1\)，输出第三项至少为 \(b-1\)；
- \(y=1\) 时，来源第二项为 \(b+8\)，输出第三项至少为 \(b-2\)。

故统一有第三项至少 \(b-2\)。\((1,8,3)\) 需要 \(3\ge6\)，\((1,9,6)\) 需要 \(6\ge7\)，均矛盾。一位或两位来源可直接检查，也不能产生式 (6) 中的首部。

于是 \(R_{40}^{78}=\varnothing\)、\(R_{38}^{85}=\varnothing\)。例如一条 41 步链到达 78 类回文时，删去最后的无进位步骤，就会给出 40 条真实的 \(F\) 逆像边，与前者为空冲突。因此 \(H(P)\le40\)；85 类同理得到 \(H(P)\le38\)。

这一步是明确的有限状态计算证明，不是“试算了许多数没有找到反例”。完整每层基数与生成规则在源码中。

### 短位数边界

六位置论证要求所有参与的来源至少六位。如果一条 \(B+1\) 步反例链中有某项少于六位，由于 \(T(n)>n\)，它的初始数必小于 \(10^5\)。因此穷尽全部 \(1\le A<100000\) 的相应 \(B+1\) 步即可补齐全部短边界。验证程序执行了这个完整检查，没有例外。

程序还对全部长度 6、7、8 的 194940 个可行原始和字，检查实际步骤是否被六位置逆像包含。这个交叉核验检查实现；无限长度结论依靠式 (4)、(5) 的推导与空集证书。

两类至少都能在第 6 步首次命中：

\[
1009100\to1028101\to2046302\to4082704
\to8155508\to16211026\to78222287,
\]

\[
1023944\to5517145\to10934300\to11278201
\to21565412\to43021924\to85933958.
\]

这只是上界不平凡的例子，不证明 40 或 38 最优。

## 4. 396 类首部及对 196 的结论

除完整的 78、85 两类外，本轮还用同一规则证明下表 25 个三位首部的上界。

| 首三位 | 已证明上界 |
|---|---:|
| 119 | 8 |
| 213 | 23 |
| 216 | 10 |
| 217 | 28 |
| 218 | 36 |
| 257 | 16 |
| 276 | 31 |
| 277 | 31 |
| 278 | 31 |
| 348 | 16 |
| 377 | 8 |
| 384 | 7 |
| 385 | 8 |
| 426 | 24 |
| 429 | 22 |
| 474 | 7 |
| 674 | 5 |
| 737 | 12 |
| 755 | 12 |
| 777 | 27 |
| 778 | 25 |
| 905 | 11 |
| 906 | 11 |
| 923 | 7 |
| 935 | 10 |

上一轮的 360 类中，78 已包含三个三位首部，85 已包含六个。因此本轮两条完整二位首部定理新增加 \((10-3)+(10-6)=11\) 个三位首部，再加表中 25 个，得到

\[
360+11+25=396.
\]

此计数是与 [上一轮完整证明](sandbox:/workspace/scratch/9660d01d1835/p196_four_column_obstruction.md) 的并集；它不表示完整猜想的完成百分比。

完整二位首部类别为

\[
10,20,32,33,40,41,60,64,65,76,\mathbf{78},80,81,82,83,\mathbf{85}.
\]

全部已列类别的统一上界不超过 40。直接整数计算确认 \(N_0=196\) 至 \(N_{40}\) 均不是回文，其中

\[
N_{40}=13305261530450734933.
\]

如果 \(t>40\) 时到达其中某个回文 \(P\)，则原轨道给出 \(H(P)\ge t>40\)，与上界冲突。因此 396 类全部被永久排除。

## 5. 一个不能忽略的十步实例

令

\[
A=1031001007250916996999909039935.
\]

其首次回文恰在第 10 步，且

\[
T^{10}(A)=55\underbrace{00\cdots0}_{30\text{ 个零}}55.
\tag{7}
\]

完整轨道如下，每一行均可用一次整数相加复核。

| 步数 | 数值 |
|---|---|
| 0 | 1031001007250916996999909039935 |
| 1 | 6430310107247913187526910041236 |
| 2 | 12751710303505726384953920171582 |
| 3 | 41268813239454089135484221887303 |
| 4 | 71647625487907287180977453773517 |
| 5 | 143185360965815465451955906448134 |
| 6 | 575029970524970029970524970029475 |
| 7 | 1149950049950049950049950049950050 |
| 8 | 1650549450549450549450549450549461 |
| 9 | 3300000000000000000000000000000022 |
| 10 | 5500000000000000000000000000000055 |

另外，\(11\mid A\)，\(A\equiv44\pmod{99}\)。所以“被 11 整除的起点，遇到 \(55\,0^k\,55\) 应当很快”不能作为未经证明的补充条件；至少任何小于 10 的统一首次命中上界已经被这个实例否定。

## 6. 无穷多个轨道与 196 具有完全相同的模 99 记录

**区块复制引理。** 假设 \(A_t=T^t(A)\)，\(0\le t\le k\) 的位数都不超过 \(L\)，定义

\[
S_{r,L}=\sum_{j=0}^{r-1}10^{jL},\qquad B=A S_{r,L}.
\]

则

\[
T^t(B)=A_tS_{r,L}\quad(0\le t\le k),
\tag{8}
\]

并且这期间 \(T^t(B)\) 为回文，当且仅当 \(A_t\) 为回文。

证明：各区块不重叠，按整个数字反转，区块位置次序颠倒，每个区块内部也反转。所有区块内容相同，所以

\[
\operatorname{rev}(A_tS_{r,L})
=\operatorname{rev}(A_t)S_{r,L}.
\]

即使 \(A_t\) 末尾有零，这个数值恒等式仍成立。相加后归纳得到式 (8)；再约去正数 \(S_{r,L}\)，得到回文性的等价。

将第 5 节的十步实例代入，最大位数为 34。故对每个整数 \(L\ge34\)，令

\[
\boxed{B_L=A\sum_{j=0}^{6}10^{jL}.}
\tag{9}
\]

每个 \(B_L\) 都恰在第 10 步首次成为回文。不同 \(L\) 给出不同数，所以这是一个无穷族。复制后的目标仍以 55 开头，但含多个区块，不声称它仍只有中间一段零。

下面证明它们的**整个模 99 轨迹**与 196 的轨道尾部相同。

对任意 \(11\mid n\)，有

\[
11\mid T(n),\qquad T(n)\equiv2n\pmod{99}.
\tag{10}
\]

确实，若 \(n\) 有 \(m\) 位，由 \(10^2\equiv1\pmod{99}\) 得

\[
\operatorname{rev}(n)\equiv10^{m-1}n\pmod{99}.
\]

奇数位时得到 \(T(n)\equiv2n\)；偶数位时得到 \(T(n)\equiv11n\equiv2n\)，最后一个等价使用 \(99\mid9n\)。被 11 整除的性质也随之保持。

又因为 \(S_{7,L}\equiv7\pmod9\)、\(A/11\equiv4\pmod9\)，

\[
B_L\equiv11\cdot4\cdot7\equiv11\pmod{99}.
\]

而 \(N_3=T^3(196)=7436\equiv11\pmod{99}\)，且被 11 整除。故式 (10) 给出

\[
\boxed{T^t(B_L)\equiv T^{t+3}(196)\pmod{99}\quad\text{对所有 }t\ge0.}
\tag{11}
\]

注意式 (11) 对全部未来时刻成立，不仅是前十步；虽然区块复制恒等式这里只保证到第十步，但以后模 99 的递推仍由式 (10) 保证。

所以，仅观察模 99 的整个未来轨迹，无法将 196 的这一轨道尾部与这些十步就出现回文的轨道区分开。模 9、模 11 的记录也同样无法区分。

这个结论只针对上述同余信息。它没有否定加入长度、具体数位结构、其他模数或更强联合约束的证明方法，也没有说明 196 会出现回文。

## 7. 证明状态与验证程序

正面推进是两个新的完整首部排除定理及 25 个额外三位首部。方法上的推进是明确说明模 99 的整条记录仍不足以作出所需区分。完整 196 猜想的缺口没有消失：其余目标没有全部排除，也没有建立将 196 永久限制在已排除类别中的不变量。

候选上界曾用另一个 C++ 六位置全图实现产生，图有 44569782 个顶点、66854673 条边；其中 39584650 个顶点获得有限秩。该实现的四位置版本与上一轮 Python 的全部 360 个上界逐项相同。下附 Python 程序无需建立这个大图，直接重建本轮 27 个目标证书，核对短位数边界及两个构造。两种实现已得到一致结论。

将下列代码保存为 `six_column_certificate.py`，用 Python 3 运行，仅依赖标准库。完整检查已经运行通过。代码中的有限数字检查与逐列覆盖检查不能脱离上面的数学论证单独当成无限长度证明。

```python
"""Six-position carry certificates and the block-replication lemma.

This is not a proof of the full 196 conjecture. The accompanying report
proves why these finite prefix certificates apply to unbounded lengths.
"""
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import product


def T(n):
    return n + int(str(n)[::-1])


def pal(n):
    a = str(n)
    return a == a[::-1]


def normalize(s):
    digits, carry = [], 0
    for u in s:
        carry, d = divmod(u + carry, 10)
        digits.append(d)
    if carry:
        digits.append(carry)
    return tuple(digits)


def forward(s):
    d = normalize(s)
    return tuple(a + b for a, b in zip(d, d[::-1]))


@lru_cache(200000)
def inv_nongrowth(p):
    states = {((), 0, 0)}
    for i, v in enumerate(p):
        nxt = set()
        for word, x, y in states:
            for s in range(1 if i == 0 else 0, 19):
                xx = (s + x) // 10
                for yy in (0, 1):
                    if ((s + yy) // 10 == y
                            and 2*s + x + yy - 10*(xx + y) == v):
                        nxt.add((word + (s,), xx, yy))
        states = nxt
    return frozenset(word for word, _, _ in states)


@lru_cache(200000)
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
                digit = v - word[-1] - yy + 10*y
                if not 0 <= digit <= 9:
                    continue
                for xx in (0, 1):
                    s = digit + 10*xx - x
                    if 0 <= s <= 18:
                        nxt.add((word + (s,), xx, yy))
        states = nxt
    return frozenset(word for word, _, y in states
                     if any((word[-1] + z) // 10 == y for z in (0, 1)))


@lru_cache(200000)
def inv_prefix(p):
    return inv_nongrowth(p) | inv_growth(p)


CASES = {'78': 40, '85': 38, '119': 8, '213': 23, '216': 10,
         '217': 28, '218': 36, '257': 16, '276': 31, '277': 31,
         '278': 31, '348': 16, '377': 8, '384': 7, '385': 8,
         '426': 24, '429': 22, '474': 7, '674': 5, '737': 12,
         '755': 12, '777': 27, '778': 25, '905': 11, '906': 11,
         '923': 7, '935': 10}

EXPECTED_78 = [10000, 66383, 36630, 19665, 11773, 6557, 3796, 6251,
               8403, 4979, 4730, 1761, 4425, 2531, 7923, 4595, 2244,
               1304, 964, 350, 515, 650, 424, 342, 141, 344, 305, 918,
               778, 455, 342, 257, 116, 197, 267, 215, 118, 44, 41, 35, 0]
EXPECTED_85 = [10000, 6231, 3919, 2594, 3354, 5634, 7851, 4704, 4601,
               1879, 3869, 2386, 6921, 4129, 2045, 1160, 755, 297, 472,
               599, 416, 318, 133, 344, 305, 918, 778, 455, 342, 257,
               116, 197, 267, 215, 118, 44, 41, 35, 0]


def certificates():
    records, shared = {}, {}
    for prefix, bound in CASES.items():
        inv_prefix.cache_clear()
        inv_nongrowth.cache_clear()
        inv_growth.cache_clear()
        pre = tuple(map(int, prefix))
        layer = {pre + p for p in product(range(10), repeat=6-len(pre))}
        counts = [len(layer)]
        for depth in range(1, bound+1):
            inverse = (inv_nongrowth if depth == 1 and pre[1] < pre[0]
                       else inv_prefix)
            layer = {s for p in layer for s in inverse(p)}
            counts.append(len(layer))
            if prefix in ('78', '85') and depth == bound-15:
                shared[prefix] = layer.copy()
            if prefix in ('78', '85') and depth == bound-1:
                assert len(layer) == 35
                assert {p[:3] for p in layer} == {(1, 8, 3), (1, 9, 6)}
            if not layer:
                break
        assert len(counts) == bound+1 and not layer, (prefix, counts)
        if prefix == '78':
            assert counts == EXPECTED_78
        if prefix == '85':
            assert counts == EXPECTED_85
        records[prefix] = counts
    assert shared['78'] == shared['85'] and len(shared['78']) == 344
    assert not inv_prefix((1, 8, 3))
    assert not inv_prefix((1, 9, 6))
    return records


def raw_words(n):
    half = n // 2
    for first in range(1, 19):
        for tail in product(range(19), repeat=half-1):
            left = (first,) + tail
            if n % 2:
                for center in range(0, 19, 2):
                    yield left + (center,) + left[::-1]
            else:
                yield left + left[::-1]


def carry_coverage():
    count = 0
    for n in range(6, 9):
        for s in raw_words(n):
            d, p = normalize(s), forward(s)
            inverse = inv_growth if len(d) > n else inv_nongrowth
            assert s[:6] in inverse(p[:6]), (s, p)
            count += 1
    assert count == 194940
    return count


def short_boundary():
    at_step = defaultdict(list)
    for prefix, bound in CASES.items():
        at_step[bound+1].append(prefix)
    for root in range(1, 100000):
        n = root
        for k in range(1, 42):
            n = T(n)
            ds = str(n)
            if ds == ds[::-1]:
                assert all(not ds.startswith(p) for p in at_step[k]), (root, k, n)


def constructive_checks():
    examples = {'78': 1009100, '85': 1023944}
    for prefix, root in examples.items():
        path = [root]
        for _ in range(6):
            path.append(T(path[-1]))
        assert not any(map(pal, path[:-1])) and pal(path[-1])
        assert str(path[-1]).startswith(prefix)
    A = 1031001007250916996999909039935
    path = [A]
    for _ in range(10):
        path.append(T(path[-1]))
    assert path[-1] == int('55' + '0'*30 + '55')
    assert not any(map(pal, path[:-1])) and pal(path[-1])
    assert max(map(lambda n: len(str(n)), path)) == 34
    assert A % 99 == 44 and A % 11 == 0
    for L in (34, 35, 40):
        S = sum(10**(j*L) for j in range(7))
        b = A*S
        assert b % 99 == 7436 % 99 == 11
        for k, a in enumerate(path):
            assert b == a*S
            assert pal(b) == (k == 10)
            assert b % 99 == 11*pow(2, k, 99) % 99
            b = T(b)
    return path


def verify():
    records = certificates()
    print('27 finite inverse certificates passed.', flush=True)
    coverage = carry_coverage()
    print('Six-position carry coverage:', coverage, flush=True)
    short_boundary()
    print('All 99999 short roots passed through step 41.', flush=True)
    path = constructive_checks()
    orbit = [196]
    for _ in range(40):
        orbit.append(T(orbit[-1]))
    assert not any(map(pal, orbit))
    return {'counts': records, 'first_hit_10_path': path,
            'N40': orbit[-1], 'coverage': coverage}


if __name__ == '__main__':
    result = verify()
    print(result)
    print('This verifies partial results, not the full 196 conjecture.')


```
