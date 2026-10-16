# 归档排除说明

仅排除下列可由保留源码和命令重新生成的 Lean 编译产物；未排除任何 `.lean`、日志、manifest、校验文件或复现脚本。空构建目录不作为文件证据复制。

| 原相对路径 | 字节数 | 原 SHA256 |
| --- | ---: | --- |
| `attempt-002-build/Agent102RunDecision.olean` | 81000 | `63048e9dc0b445e733f6d4621b8b2a5efdb84f7847e3c9a07f0f057583650e60` |
| `final-001-empty-build/Agent102RunDecision.olean` | 81000 | `d3f2b88377f3e155d5a410549a5d01e829181e0e2c16a242ee364d836f8c745d` |
| `final-001-empty-build/Agent102RunDefs.olean` | 306968 | `061783d0c7aed3758b7f19f8e5ccfc0893fdf6e87c7eea4b72d9765ec1d5101e` |
| `final-001-empty-build/Agent102RunWord.olean` | 352688 | `57059f7b3538f21c53f2a121a643f1bf96b76a137384fe745b89066df1f85100` |
| `final-001-empty-build/LiteralAudit.olean` | 17256 | `874145bf0a7303817452aa24c07bcb033679017f6dbf83d7f576a4f8ed907523` |

开发阶段在本目录外复用的依赖 `.olean` 亦未额外复制；对应源码副本、原产物路径和 SHA 已完整保留在两个 attempt 的 manifest 中。

上述排除不改变任何失败/成功分类，也不把编译产物当成证明源码。
