# Branch review: evaluation harness and model changes

Reviewed 2026-09-25. Reader: branch maintainer. Action: resolve the findings before using this harness to recommend a skill. Revisit after runner fixes, the first evaluation attempt, or a target model/surface change.

Scope: fujiakito/houserules, branch claude/clever-clarke-dnni5u at 731fc7d. At review time this branch was three commits ahead of and one commit behind main (1e9ee8a). No provider-backed evaluation was run for this review.

## 這個 branch 要達成甚麼

三個 commits 記錄 evaluation harness 的 prior art，加入 [offline runner](../tests/eval/README.md) 與 regression tests，並凍結第一個 [hr-tdd-01 case](../tests/workflows/skill-eval/hr-tdd-01/README.md)。目的是補上 [PORTABILITY.md 的 fallback admission criterion 5](../research/PORTABILITY.md#fallback-admission-criteria)：比較 optional skill 與 baseline 的 outcome、cost 和 failure cases，才決定是否有證據推薦該 skill。

hr-tdd-01 在相同 task 比較四個 arms：沒有 procedure 的 baseline、完整 hr-tdd 的 candidate、長度相近的一般 procedure (control-length)，以及一句 test-first 指令 (one-line)。Rubric 重視失敗原因、public interface 和最小修正。這是 prompt-only case，測量 skill 文字對回答的影響；它不測 native skill discovery、tool-using iteration 或實際 test execution。Case 在 2026-09-15 已凍結，但截至本 review **尚未執行**，因此沒有 hr-tdd 優於其他 arms 的結果。

## Code review findings

### [P1] Resume 可混合不同執行設定

[cmd_run](../tests/eval/runner.py#L364) 讀取既有 attempt.json 後只核對 schema_version 和 input hashes，沒有比對 model、runner、argv、timeout_seconds、budget 或原本的 cell plan。以 mocked provider 重現：先用 model-A 執行 baseline，再用 model-B 和 --resume 執行 candidate，結果標為 completed，但 record 仍標示 model-A。這不能作為相同設定下的 arm comparison。Resume 應拒絕與既有 attempt 固定設定不一致的請求。

### [P1] 部分 arms 也可標為 completed

[cmd_run](../tests/eval/runner.py#L366) 每次依當次 --arm 和 --trials 建立 cells，並用它判定整個 attempt 的 status。重現中只跑 baseline 就得到 completed，儘管 case 另有三個 arms。這不符合 [rubric 的 G1](../tests/workflows/skill-eval/hr-tdd-01/rubric.md#release-gate--maintainer-only-not-for-the-grader)。Attempt 應保存完整 campaign plan，並依它判定 status。

### [P2] Grading 未核對 response hash

[run_cell](../tests/eval/runner.py#L490) 記錄 output_sha256，但 [cmd_grade](../tests/eval/runner.py#L498) 在產生 blind packet 或接收 scores 前沒有重新核對 .out。執行後若 response 被改動，grader 會評分改後內容，而 record 保留原 hash。Grading 應核對每個 output。

### [P2] Codex JSONL 未抽取 agent response

Runner 使用 codex exec --json，但 [parse_payload](../tests/eval/runner.py#L201) 對 JSONL events 只抽取 usage 和 cost，不抽取 agent_message。因此 [cmd_grade](../tests/eval/runner.py#L519) 會把 raw JSONL 寫入 blind packet，而非單純的回答。2026-09-25 在本機 codex-cli 0.155.0-alpha.16.4 的 codex exec --help 確認 --json 輸出 JSONL；這只是在 CLI surface 的觀察，未驗證 Desktop app 或 IDE。應加入 response parsing 與 regression test。

## 驗證與限制

在上述 branch HEAD 的 Windows/Python 環境，python check.py、python install.py --check、runner.py verify --case tests/workflows/skill-eval/hr-tdd-01 及 git diff --check origin/main...HEAD 均通過；runner 的 25 個 regression tests 全部通過。完整 python -m unittest discover -s tests -v 執行 101 tests，結果是 1 failure、5 skipped。Failure 位於此 branch 未修改的 test_follow_up_command_survives_paths_containing_spaces：Windows temp path 的長名稱與 8.3 短名稱不一致；因此不能稱完整 suite 通過。以上 findings 是 runner logic review，沒有執行付費 provider cells。

## 新 models 對 repo 的影響

截至 2026-09-25，[OpenAI Docs](https://developers.openai.com/api/docs/guides/latest-model) 所列 GPT-6 family 是 Astra、Sol、Luna；沒有 GPT-6 Terra，Terra 屬於 GPT-5.6 family。[OpenAI changelog](https://developers.openai.com/api/docs/changelog) 記錄 GPT-6 Sol 和 Luna 於 2026-09-22 發布；[Anthropic docs](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5) 記錄 Claude Opus 5.5 的新行為。這些官方頁面均於 2026-09-25 檢索。

新 model 可能自行產出良好的 regression test，令 hr-tdd 相對 baseline 的增益縮小；也可能仍受益。兩者都是待測假設。每個 evaluation result 應綁定 model、agent surface、CLI version、effort、task、permissions 和 tools。[Anthropic docs](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5) 指出 Opus 5.5 的 default effort 為 medium，與 Opus 5 的 high 不同；不能直接沿用舊 run 的 latency/cost 假設。該文件於 2026-09-25 檢索，描述 API/model 行為，並非本 repo 對 Claude Code CLI 的實測 effort。

Repo 的核心設計仍具體：它區分 documented capability、local runtime evidence 與 comparative outcome，並以 admission criteria 限制推薦。但 optional skills 的效果尚未得到本 branch 的實驗支持。先修正兩項 P1 與 grading 的證據完整性，再分別在目標 model/surface 上記錄 attempts；跨 provider 的 raw scores 不能視為只差 skill 的比較。新 models 是重查 model/surface 假設的觸發點，不會自動推翻 installer、ownership 或 handoff contract。
