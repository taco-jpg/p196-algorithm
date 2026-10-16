# 原依赖精确来源

所有条目都在本次复核中重新计算 Git blob SHA-1 与 SHA256，并逐字确认 module 副本等于 original-bytes。原对象文件采用此前已独立验证的缓存；对象哈希保存在 verification.json。

| 模块 | 原仓库路径 | Git blob | SHA256 |
|---|---|---|---|
| LychrelDigitSums | `proofs/research/continuation/LychrelDigitSums.lean` | `8a865176625283648a8a20dd2411ed77670eb0a2` | `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57` |
| Trace | `proofs/contributions/agent-13/folded-binary-family/Trace.lean` | `eb7b0887e00a39d59c2d0fe09af06775274d62f9` | `0ebded79e1c0ad1dcfe68bb2f9f07745da6d531d1f6647d09ea29489eeefe662` |
| WholeWord | `proofs/contributions/agent-13/folded-binary-family/WholeWord.lean` | `28606c392883370d1e9772db516daa6964ef169d` | `5d647c31cce3d1c15265a4a86a162c5a68baa48afc2e27ef47ac5c2c5271dc62` |
| Safety | `proofs/contributions/agent-13/folded-binary-family/Safety.lean` | `56f3ef696b417117001537210ac4a4352fa51d50` | `7457b8cc978ca974dc61841abe2e46afcca7cdb4d94213c7745babd5ec140430` |
| Indexing | `proofs/contributions/agent-13/folded-binary-family/Indexing.lean` | `9514313487a903c3e0fa776528535a48ffcf497e` | `42e6a23bbc66f0e582366a5eb0da8e5ef39ec0b435836c565fa71a645d87f3e3` |
| FiniteWords | `proofs/contributions/agent-13/folded-product-weights/FiniteWords.lean` | `9e709c2d72efbdde53e3e6e21b9838f0e8358f0f` | `77a560658d9d9b006fd987d9c07cf4fd130dd5fbfc75594a9a7029db3c1c1575` |
| FamilyStates | `proofs/contributions/agent-13/folded-product-weights/FamilyStates.lean` | `7bc577184a7da71f172a71ad7342a7b948944c2f` | `9767c2a60539e0cc5231878f714e28645d909e323ce35e6f7e6db039016160c0` |

固定提交：`12a32789056f5eec8247166564ac2ef745c3c9d6`。

关键语义直接阅读了 FamilyStates、FiniteWords、Indexing、WholeWord、Trace，以及 LychrelDigitSums 的 value、Canonical、nextWidth、Admissible、representation_next 定义或定理。完整字面副本见 original-sources/。
