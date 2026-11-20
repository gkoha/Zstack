# Zstack

面向 Linux 内核、QEMU 和虚拟化开发的 agent 技能集，支持 Claude Code 和 Codex。
工作流程和公共约束参考了 [pstack](https://github.com/cursor/plugins/tree/main/pstack)。

## 目录结构

```
core/skills/          公共部分，每个项目都装
  z-mode/             入口：选 playbook、套用原则、验证
    playbooks/        15 个流程
    principles/       19 条原则
    references/       Claude Code / Codex 工具名对照
    worker.md         子 agent 必读规则
  z-task-record/      .mydoc/ 任务记录
  z-architect/ z-blast-radius/ z-interrogate/ z-benchmark/
  z-how/ z-why/ z-tdd/ z-patch/ z-writing/ z-reflect/
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

在项目根目录执行。`-a` 同时装到 Claude Code（`.claude/skills/`）和 Codex
（`.agents/skills/`）。

```bash
# 每个项目都装
npx skills add https://github.com/gkoha/Zstack/tree/main/core --skill '*' -a claude-code -a codex

# QEMU 项目
npx skills add https://github.com/gkoha/Zstack/tree/main/packs/qemu --skill '*' -a claude-code -a codex

# 内核项目
npx skills add https://github.com/gkoha/Zstack/tree/main/packs/linux --skill '*' -a claude-code -a codex

# vGPU 项目：只要知识，不要上游流程
npx skills add https://github.com/gkoha/Zstack/tree/main/packs/qemu  --skill qemu-dev  -a claude-code -a codex
npx skills add https://github.com/gkoha/Zstack/tree/main/packs/linux --skill linux-dev -a claude-code -a codex
```

更新：`npx skills update`。安装生成的 `skills-lock.json`、`.claude/skills/` 和
`.agents/skills/` 中的 Zstack 技能不应进入上游补丁，可写入 `.git/info/exclude`。

## 使用

- Claude Code：`/z-mode` 后输入任务。
- Codex：`$z-mode` 或 `/skills` 选择。

`z-mode`、`z-interrogate`、`z-reflect` 只在显式调用时启动（Claude Code 用
`disable-model-invocation: true`，Codex 用 `agents/openai.yaml`）。其余技能由
agent 按 description 自动选用。

## 优先级

仓库自身规则（`AGENTS.md`、AI 政策、项目内 `.agents/skills/`）> Zstack 项目
pack > Zstack core。只在一个仓库成立的规则放在那个仓库自己的 `.agents/skills/`，
不放进 Zstack。

## 修改技能

1. 改 Zstack 仓库里的文件，不要改已安装的副本。
2. 运行 `python3 scripts/check-skills.py`，检查 frontmatter、重名和跨文件引用。
3. 提交、推送后，在项目里执行 `npx skills update`。

新增项目 pack：建 `packs/<name>/skills/<skill>/SKILL.md`，按上面的命令安装。

## 从 pstack 移植的内容

pstack 采用 MIT 许可，版权声明见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
以下内容按 pstack 的结构重写，并改成内核和 QEMU 的场景。

| Zstack | 来自 pstack | 改动 |
| --- | --- | --- |
| `z-mode` | `poteto-mode` | 去掉 Cursor 模型路由、Bugbot、PR 流程；加入"仓库规则优先"和不加 `Signed-off-by:`、不发邮件 |
| `z-mode/worker.md` | `poteto-mode/worker.md` | 去掉 PR 格式，改成补丁和宿主机安全约束 |
| `z-mode/references/harness.md` | `docs/harness/claude-code.md` | 改成 Claude Code 和 Codex 两列对照 |
| 19 条原则 | 24 条 `principle-*` | 见下表 |
| playbook：investigation、bug-fix、feature、refactoring、perf-issue、runtime-forensics、prototype、session-pickup、pause-safely、authoring-a-skill | 同名 playbook | 工具换成 ftrace、perf、gdb、QEMU trace、selftest、qtest |
| `artifact-forensics` | `trace-forensics` | 对象换成 oops、vmcore、core dump |
| `series-plan` | `multi-phase-plan` | PR 换成补丁系列 |
| `preparing-a-series` | `opening-a-pr` + `shipping` | 改成邮件列表流程，只生成补丁不发送 |
| `figure-it-out` | `figure-it-out` 技能 | 精简为 playbook |
| `z-architect`、`z-blast-radius`、`z-interrogate`、`z-benchmark`、`z-how`、`z-why`、`z-tdd`、`z-reflect` | `architect`、`blast-radius`、`interrogate`、`benchmark-checklist`、`how`、`why`、`tdd`、`reflect` | 加入锁、生命周期、uAPI、迁移、VM-exit 等检查项 |
| `z-writing` | `unslop` + `technical-writing` | 合并，加入代码注释规则 |
| `z-patch` | `opening-a-pr` 的标题和正文规则 | 改成 commit message 和 cover letter |

原则对照：

| Zstack | pstack |
| --- | --- |
| 照搬并改写示例（17 条） | laziness-protocol、foundational-thinking、redesign-from-first-principles、attack-the-premise、subtract-before-you-add、minimize-reader-load、build-the-lever、model-the-domain、boundary-discipline、prove-it-works、fix-root-causes、sequence-verifiable-units、test-behavior-not-implementation、explain-the-number、guard-the-context-window、never-block-on-the-human、encode-lessons-in-structure |
| 改名（1 条） | migrate-callers-then-delete-legacy-apis → `migrate-callers-then-delete`（限定为内部 API） |
| 新增（1 条） | `keep-external-contracts`：uAPI、QAPI、迁移流、machine type |
| 未移植（6 条） | experience-first、exhaust-the-design-space（偏 UI 产品）、type-system-discipline（偏 TypeScript）、outcome-oriented-execution（与内核"每个补丁可 bisect"冲突）、separate-before-serializing-shared-state（并行 worker 场景，并入 foundational-thinking 的并发检查）、make-operations-idempotent（偏分布式任务重试） |

未移植的 pstack 内容：模型路由和 `setup-pstack`、`arena`、`swarm`、
`ketchup`、`bro`、`recall`、`teach`、`statechart`、形式化验证生成器、
`no-comments`、`automate-me`、`correct`、`sharpen`、Benny 自动化，以及
babysit、shipping、hillclimb、autopilot、visual-parity、eval、worktree-cleanup
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
