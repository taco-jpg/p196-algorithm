# 逐参数压缩判定的作者原始证据归档

归档者与源码作者：真实子代理 `/root/word_intervals`。

本目录按原始字节保存 `universal-author` 中的全部实质源码、失败与成功日志、清单、校验文件和脚本。原记录未改写，首败、修复和最终成功未合并或互相替换。

- `Agent102RunDecision.lean`：检出准备期间的初始暂存草稿，与首败源码相同，不是最终采用源码。
- `attempt-001`：首次编译失败；否定命题内部的 `rw` 未能匹配。该日志不是成功证明。
- `attempt-002`：使用 `not_congr` 修复后的开发编译成功，规格和计算主体未变。
- `final-001`：唯一一次新的串行 clean `--trust=0` 链成功，六个导出接口全部逐字审计通过。
- 两个顶层 Python 文件：原始开发与最终构建脚本，执行路径按原记录保留。

采用的最终源码是 `final-001/Agent102RunDecision.lean`，SHA256 为 `e8d876593b4eec5248afe1dbc53cc6fc704b1ba106402a31637aca3120ece9f8`。

`ARCHIVE_MANIFEST.json` 列出每个复制文件的原字节数、SHA256、证据分类及排除项。`SHA256SUMS.archive` 可用于检查归档副本。全部既有 manifest 和校验文件也逐字保留。

本目录是作者证据。对母代理 `Agent102AffineAllParameters.lean` 的具名独立源码审查另放在同级 `word-independent-all-parameters` 中，不与本作者身份混同。
