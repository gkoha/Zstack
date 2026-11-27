# Zstack

面向 Linux 内核、QEMU 和虚拟化开发的 agent 技能集，支持 Claude Code、Codex、
Gemini CLI 和 Antigravity。
工作流程和公共约束参考了 [pstack](https://github.com/cursor/plugins/tree/main/pstack)。

## 目录结构

```
core/skills/          公共部分，每个项目都装
  z-mode/             入口：选 playbook、套用原则、验证
    playbooks/        17 个流程
    principles/       22 条原则
    references/       Claude Code / Codex / Gemini CLI / Antigravity 工具名对照
    worker.md         子 agent 必读规则
  z-task-record/      .mydoc/ 任务记录
  z-log/              append-only TSV 决策日志（含 scripts/log.sh）
  z-architect/ z-blast-radius/ z-interrogate/ z-benchmark/
  z-how/ z-why/ z-teach/ z-recall/ z-tdd/ z-patch/ z-writing/ z-reflect/
  z-correct/ z-sharpen/ z-reframe/ z-in-your-own-words/
  z-swarm/ z-arena/ z-create-verify/ z-no-comments/
packs/qemu/skills/
  qemu-dev/           QEMU 知识：KVM、VFIO、virtio、迁移、构建测试
  qemu-upstream/      上游 QEMU 提交规则（含 AI 内容限制）
packs/linux/skills/
  linux-dev/          内核知识：KVM、VFIO/mdev、iommufd、virtio、调试
  linux-upstream/     上游内核提交规则（DCO、AI 披露）
scripts/check-skills.py
```

`*-dev` 是知识，任何包含该代码的项目都能用。`*-upstream` 是提交流程，只在给上游
写补丁的项目里装。

## 安装

在项目根目录执行。`-a` 选择要装到的 agent：Claude Code 装到 `.claude/skills/`；
Codex、Gemini CLI、Antigravity 共用 `.agents/skills/`（Gemini CLI 和 Antigravity
都会读这个目录）。下面的命令把四个都列出来，只用其中几个就删掉对应的 `-a`。

```bash
# 每个项目都装
npx skills add https://github.com/gkoha/Zstack/tree/main/core --skill '*' -a claude-code -a codex -a gemini-cli -a antigravity

# QEMU 项目
npx skills add https://github.com/gkoha/Zstack/tree/main/packs/qemu --skill '*' -a claude-code -a codex -a gemini-cli -a antigravity

# 内核项目
npx skills add https://github.com/gkoha/Zstack/tree/main/packs/linux --skill '*' -a claude-code -a codex -a gemini-cli -a antigravity

# vGPU 项目：只要知识，不要上游流程
npx skills add https://github.com/gkoha/Zstack/tree/main/packs/qemu  --skill qemu-dev  -a claude-code -a codex -a gemini-cli -a antigravity
npx skills add https://github.com/gkoha/Zstack/tree/main/packs/linux --skill linux-dev -a claude-code -a codex -a gemini-cli -a antigravity
```

更新：`npx skills update`。安装生成的 `skills-lock.json`、`.claude/skills/` 和
`.agents/skills/` 中的 Zstack 技能不应进入上游补丁，可写入 `.git/info/exclude`。

## 使用

- Claude Code：`/z-mode` 后输入任务。
- Codex：`$z-mode` 或 `/skills` 选择。
- Gemini CLI、Antigravity：直接说"用 z-mode 技能做这个任务"。Gemini CLI 会调用
  `activate_skill` 并要求你确认。

显式调用型工作流技能（`z-mode`、`z-interrogate`、`z-reflect`、`z-correct`、
`z-sharpen`、`z-reframe`、`z-teach`、`z-recall`、`z-log`、`z-swarm`、`z-arena`、
`z-create-verify`、`z-in-your-own-words`、`z-no-comments`）只在手动触发时启动
（Claude Code 用 `disable-model-invocation: true`，Codex 用 `agents/openai.yaml`）。
Gemini CLI 和 Antigravity 的文档只定义 `name` 和 `description`，这两个标记在它们
那里不生效：模型有可能自己加载这些技能，Gemini CLI 里唯一的拦截是加载前的确认
提示。其余技能由 agent 按 description 自动选用。

## 优先级

仓库自身规则（`AGENTS.md`、AI 政策、项目内 `.agents/skills/`）> Zstack 项目
pack > Zstack core。只在一个仓库成立的规则放在那个仓库自己的 `.agents/skills/`，
不放进 Zstack。

## 修改技能

1. 改 Zstack 仓库里的文件，不要改已安装的副本。
2. 运行 `python3 scripts/check-skills.py`，检查 frontmatter、重名、脚本权限和跨文件引用。
3. 提交、推送后，在项目里执行 `npx skills update`。

新增项目 pack：建 `packs/<name>/skills/<skill>/SKILL.md`，按上面的命令安装。

## 从 pstack 移植的内容

pstack 采用 MIT 许可，版权声明见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
以下内容按 pstack 的结构移植并适配为 Linux 内核、QEMU 和虚拟化场景，同时保持跨
Claude Code、Codex、Gemini CLI 和 Antigravity 可用（不依赖 Cursor 专属功能）。

| Zstack | 来自 pstack | 改动 |
| --- | --- | --- |
| `z-mode` | `poteto-mode` | 去掉 Cursor 模型路由、Bugbot、PR 流程；保留新鲜子 agent、Lead/Worker 分离与原则触发；加入"仓库规则优先"和不加 `Signed-off-by:`、不发邮件 |
| `z-mode/worker.md` | `poteto-mode/worker.md` | 去掉 PR 格式，改成补丁和宿主机安全约束 |
| `z-mode/references/harness.md` | `docs/harness/claude-code.md` | 改成 Claude Code、Codex、Gemini CLI、Antigravity 四列对照 |
| 22 条原则 | 24 条 `principle-*` | 见下表 |
| playbook：investigation、bug-fix、feature、refactoring、perf-issue、hillclimb、autonomous-run、runtime-forensics、prototype、session-pickup、pause-safely、authoring-a-skill | 同名 playbook | 工具换成 ftrace、perf、gdb、QEMU trace、selftest、qtest；去掉 Cursor `/loop` 与 PR 步骤，保留吞吐检查点、冻结 harness 与退出谓词循环 |
| `artifact-forensics` | `trace-forensics` | 对象换成 oops、vmcore、core dump |
| `series-plan` | `multi-phase-plan` | PR 换成补丁系列 |
| `preparing-a-series` | `opening-a-pr` + `shipping` | 改成邮件列表流程，只生成补丁不发送 |
| `figure-it-out` | `figure-it-out` 技能 | 保留完整 5 阶段闭环、三态判定、门禁防作弊和 `z-log` 联动，纳入 playbook |
| `z-architect`、`z-blast-radius`、`z-interrogate`、`z-benchmark`、`z-how`、`z-why`、`z-tdd`、`z-reflect` | `architect`、`blast-radius`、`interrogate`、`benchmark-checklist`、`how`、`why`、`tdd`、`reflect` | 加入锁、生命周期、uAPI、迁移、VM-exit 等检查项；`z-blast-radius` 保留 5 级确信度阶梯 |
| `z-correct`、`z-sharpen`、`z-reframe`、`z-teach`、`z-recall`、`z-in-your-own-words` | `correct`、`sharpen`、`reframe`、`teach`、`recall`、`in-your-own-words` | 全面改写为内核/QEMU 工具链、`.mydoc/` 与各 harness 的 transcript 路径 |
| `z-log`（含 `scripts/log.sh`） | `show-me-your-work` | 保留 append-only TSV、run 边界 `start` 行、transcript 自审与独立复核，默认落盘到 `.mydoc/<task>/output/decisions.tsv` |
| `z-swarm`、`z-arena` | `swarm`、`arena` | 去掉 Cursor 模型路由与 Cloud Agent 绑定，保留并行切片/竞速 SHA 校验、隐式 Rubric 盲评与基底嫁接 |
| `z-create-verify` | `create-verification-skill` + `maintain-verification-skill` | 合并生成与定期维护两套模式，面向 QEMU VM/QMP、内核 `-kernel`、VFIO/vGPU 与 selftest |
| `z-no-comments` | `no-comments` + `agents/comment-sicko.md` | 改写为内核/QEMU 白名单（放行 SPDX、锁与内存屏障注释、硬件 quirk/spec、kernel-doc），猎杀废话与 workaround 注释并推动重构或静态断言编码 |
| `z-writing` | `unslop` + `technical-writing` | 合并，加入代码注释规则；补充中文 AI 空话禁词 |
| `z-patch` | `opening-a-pr` 的标题和正文规则 | 改成 commit message 和 cover letter；显式套用 `z-writing`，要求纯文本、对齐 `git log` 风格，禁止复述 diff 的 bullet、Markdown、空洞总结句，以及 AI 的 `Co-Authored-By:` 和 `Generated with` 尾巴（上游政策要求披露时除外） |

原则对照：

| Zstack | pstack |
| --- | --- |
| 移植并改写为系统编程示例（20 条） | laziness-protocol、foundational-thinking、redesign-from-first-principles、attack-the-premise、subtract-before-you-add、minimize-reader-load、build-the-lever、model-the-domain、boundary-discipline、type-system-discipline（改为 C/sparse/`BUILD_BUG_ON` 语境）、separate-before-serializing-shared-state、make-operations-idempotent、prove-it-works、fix-root-causes、sequence-verifiable-units、test-behavior-not-implementation、explain-the-number、guard-the-context-window、never-block-on-the-human、encode-lessons-in-structure |
| 改名（1 条） | migrate-callers-then-delete-legacy-apis → `migrate-callers-then-delete`（限定为内部 API） |
| 新增（1 条） | `keep-external-contracts`：uAPI、QAPI、迁移流、machine type |
| 未移植（3 条） | experience-first、exhaust-the-design-space（偏 UI/产品体验）、outcome-oriented-execution（与内核"每个补丁可 bisect"冲突） |

未移植的 pstack 内容：模型路由和 `setup-pstack`、`poteto-help`、`ketchup`/`ketchup-video`、
`bro`、`make-bot-ui`、`automate-me`、`typescript-best-practices`、`statechart` 与形式化验证生成器、
Benny 自动化，以及 babysit、shipping、autopilot、visual-parity、eval、worktree-cleanup
等依赖 Cursor、GitHub PR 或 UI 的 playbook。

## 来自现有项目技能的公共部分

`qemu/.agents/skills/qemu-codebase` 和 `linux/.agents/skills/linux-kernel-development`
重复的规则提到了 core：

- `.mydoc/` 任务记录（`z-task-record`），两边的目录名差异留在各自 pack：
  QEMU 用 `readme.md` + `outputs/`，内核用 `README.md` + `output/`。
- 不清理用户改动、窄测试优先、跑 checkpatch、不发外部通信（`z-mode`、`z-patch`）。

项目相关部分进了 pack：QEMU 的子系统文档索引、构建目录和测试规则进
`qemu-dev`；AI 内容政策进 `qemu-upstream`；内核 commit 和 DCO 规则进
`linux-upstream`。两个仓库里原有的技能文件没有改动。
