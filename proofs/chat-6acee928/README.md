# 严格证明 P196 猜想：聊天研究归档

来源：https://chatgpt.com/c/6acee928-7e48-83e8-91db-34a286073ba0

本次归档保留本聊天已取得的全部 10 个附件：9 份完整 Markdown 和 1 份原始 Python。另补录最初两轮未附文件的正文论证，提取 8 段 Python 附录为独立脚本，加上原始脚本共 9 份可运行核验程序。原始文件不作内容改写，所有反例、失败推广、未解决问题和历史结论均随原稿保留。

**完整 196 猜想仍未证明。** 这是研究材料整理；原稿中的书面证明与计算证书保留其原有范围，本次重新运行脚本不等于独立审查全部无限范围证明，也不是 Lean 形式化验证。

## 阅读顺序与覆盖

先读 [聊天正文独有结果](CHAT_ONLY_RESULTS.md)：单步判据、无限归纳反例族、固定模数障碍、五模式不变量和增位回文 110/122 排除。之后按原附件形成顺序阅读：

| 顺序 | 原始文件 | 主题 |
|---|---|---|
| 1 | [p196_odd_gap_certificate.md](originals/p196_odd_gap_certificate.md) | 奇数零间隔首次回文族、有限自动机逆像证书 |
| 2 | [p196_double_image_theorem.md](originals/p196_double_image_theorem.md) | 首位 1 回文的二重像充要条件、进位对称引理、递降反例 |
| 3 | [p196_double_image_verify.py](originals/p196_double_image_verify.py) | 上一份原稿配套的原始验证程序 |
| 4 | [p196_all_palindromes_and_eight_families.md](originals/p196_all_palindromes_and_eight_families.md) | 全部回文两步判据、八个无限排除族、剩余 d=5 分支 |
| 5 | [p196_seven_pairs_obstruction.md](originals/p196_seven_pairs_obstruction.md) | 进位段计数充要条件、七对同数字全时排除、五对分支 |
| 6 | [p196_exact_ancestor_depth.md](originals/p196_exact_ancestor_depth.md) | 十一对数字精确深度、混合奇数数位定理 |
| 7 | [p196_uniform_five_layer_obstruction.md](originals/p196_uniform_five_layer_obstruction.md) | 统一五层前驱障碍、最优六步上界、首次回文两步界 |
| 8 | [p196_thirteen_prefix_theorem.md](originals/p196_thirteen_prefix_theorem.md) | 十三种二位首部的最优统一祖先深度 |
| 9 | [p196_four_column_obstruction.md](originals/p196_four_column_obstruction.md) | 33 首部最优五步界、360 种三位首部证书 |
| 10 | [p196_six_column_and_mod99.md](originals/p196_six_column_and_mod99.md) | 78/85 上界、396 种三位首部、无限模 99 轨道不可区分族 |

## 最新附件的结论

最新收录稿为 `p196_six_column_and_mod99.md`。其中报告：78 首部回文的 H(P)≤40、85 首部 H(P)≤38（不声称最优）；累计 16 类完整二位首部、396 类三位首部被排除。它还构造无限多个第 10 步首次回文、但整个模 99 轨迹与 196 从第 3 步起相同的轨道，说明单靠该模轨迹不能完成证明。完整前提、证明、表格及反例以原稿为准。

## 代码与验证

`code/` 中的 8 个附录提取文件与 Markdown 代码块逐字一致；`p196_double_image_verify.py` 与独立原附件逐字节相同。映射和原稿行号见 [CODE_ORIGINS.json](CODE_ORIGINS.json)。9 个脚本均已在本次归档环境运行，全部退出码为 0；原始 stdout/stderr 和运行耗时见 [verification/results.json](verification/results.json)。这些程序只验证各自声明的范围。

在本目录运行任意一个脚本，例如：

```sh
python3 code/p196_six_column_and_mod99.py
sha256sum -c MANIFEST.sha256
```

## 完整性边界

已从最初“尝试严格数论证明P196猜想”核对正文，并收录截至上述最新附件的可获取研究材料。原聊天当时仍显示 Working；此归档是固定快照，不包含其之后的新结果。正文独有两轮为明确标注的整理稿，不是完整逐字聊天记录。未取得原会话执行环境里的未附加临时脚本、工具调用原始日志、隐藏中间文件或编辑分支；不将它们伪称已完整恢复。后续若取得原聊天工作目录或完整导出，应追加这些材料并更新清单。

本聊天未提供 universal waiting-time theorem 的 Lean 源码，不能把其他聊天或仓库中同名研究移入本聊天的来源链。外部公开论文只保留原稿引用，没有冒充本聊天产物。原仓库已有的其他研究保持独立。

## 文件与来源

[SOURCES.json](SOURCES.json) 记录附件身份、时间与大小；[INVENTORY.json](INVENTORY.json) 及 [MANIFEST.sha256](MANIFEST.sha256) 记录本归档所有内容的大小和 SHA-256；[CONTENTS.md](CONTENTS.md) 列出各原稿的全部章节。
