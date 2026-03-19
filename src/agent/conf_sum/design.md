# conf_sum 模块设计（Round 3）

## 1. 目标与范围

### 1.1 当前目标

基于最新一轮需求，`conf_sum` 的目标进一步收缩为：

1. 给定会议名，定位该会议最新一届的 accepted papers 列表页。
2. 从 accepted papers 列表中抽取以下最小字段：
   - `conference`
   - `year`
   - `title`
   - `paper_url`
3. 将结果导出为便于人工查看和后续处理的文件。

当前阶段只追求 ICLR 的最小闭环跑通，后续会议扩展建立在同一套轻量接口上。

### 1.2 非目标

以下内容不再属于当前版本范围：

- 抓取 `abstract`
- 抓取作者名
- 抓取作者机构 / affiliations
- 多源字段级 provenance 追踪
- 借助 OpenAlex / OpenReview 做补充富化
- 为所有会议一次性统一实现复杂抓取逻辑

换句话说，这一轮只做“最新 accepted paper 定位与最小信息抽取”。

## 2. 输出数据定义

### 2.1 核心字段

每条论文记录只保留四个业务字段：

- `conference`: 会议简称，例如 `ICLR`
- `year`: 届次年份，例如 `2025`
- `title`: 论文标题
- `paper_url`: 论文页面链接

### 2.2 辅助字段

为保证抓取过程可追踪、可调试，额外保留少量运行字段：

- `crawl_timestamp`: 抓取时间，ISO 8601 格式
- `status`: 记录状态，建议值为 `ok` / `partial` / `error`
- `notes`: 调试备注，例如“paper_url missing”或“title normalized from anchor text”

### 2.3 导出列建议

导出到 CSV / JSONL / XLSX 时，列顺序固定为：

1. `conference`
2. `year`
3. `title`
4. `paper_url`
5. `crawl_timestamp`
6. `status`
7. `notes`

## 3. 数据来源策略

### 3.1 总体策略

当前版本只需要找到“最新一届 accepted papers 列表”并抽取标题和论文链接，因此采用单阶段抓取：

1. 先确定会议最新年份。
2. 找到该年份 accepted papers 列表页。
3. 从列表页中解析出若干论文项。
4. 对每条论文项输出最小记录。

不再需要第二阶段去详情页补抽象、作者机构等字段。

### 3.2 ICLR 的具体策略

ICLR 当前采用官方 conference / virtual 站点作为主来源：

1. 从 `https://iclr.cc/Conferences/<year>` 或对应导航页确认最新年份。
2. 使用 `https://iclr.cc/virtual/<year>/papers.html` 作为 accepted papers 列表入口。
3. 在列表页中抽取：
   - 标题
   - 论文详情页链接
4. 直接生成输出记录。

如果列表页已经给出足够稳定的标题和链接，则无需再访问详情页。

### 3.3 会议扩展原则

后续扩展其他会议时，优先选择以下来源：

1. 官方 proceedings / accepted papers 页面
2. 官方虚拟会场页面
3. 官方 program 页面

选择标准是：

- 页面结构稳定
- 标题和论文链接可以直接提取
- 年份与 accepted 状态容易识别

不优先引入 OpenAlex、OpenReview、Semantic Scholar 这类聚合源，除非官方页面无法满足最小字段需求。

## 4. 模块划分

当前设计应围绕“最小闭环”进一步收缩，避免过度抽象。

### 4.1 `models.py`

职责：定义最小数据结构。

建议保留：

- `PaperRecord`
- `ConferenceRunResult`

#### `PaperRecord`

建议字段：

- `conference: str`
- `year: int`
- `title: str`
- `paper_url: str`
- `crawl_timestamp: str`
- `status: str`
- `notes: str`

#### `ConferenceRunResult`

建议字段：

- `conference: str`
- `year: int`
- `records: list[PaperRecord]`
- `errors: list[str]`
- `source_summary: dict[str, str | int]`

### 4.2 `config.py`

职责：集中管理可调参数。

建议保留：

- `conference_name`
- `sample_size`
- `crawl_all`
- `request_timeout_sec`
- `user_agent`
- `show_progress`
- `output_dir`
- `latest_year_hint`
- `enable_detail_fetch`，默认关闭，当前可仅为未来预留

当前不需要配置多源富化参数。

### 4.3 `sources/base.py`

职责：封装基础 HTTP 请求能力。

最小能力：

- GET 页面
- 超时控制
- User-Agent 设置
- 返回文本内容
- 对网络错误抛出统一异常或返回统一错误信息

### 4.4 `sources/official_pages.py`

职责：封装官方页面解析逻辑。

当前重点是 ICLR：

- 获取最新年份入口
- 获取 `papers.html`
- 从列表页提取论文项

建议这里直接提供与页面结构贴近的轻量对象，例如：

- `PaperCandidate(title, paper_url, source_url)`

当前不需要 `PaperDetail` 这类面向 abstract / affiliations 的复杂结构。

### 4.5 `resolvers/iclr.py`

职责：实现 ICLR 的最小闭环解析器。

输入：

- 会议配置
- 可选 sample size

输出：

- `ConferenceRunResult`

主要流程：

1. 确认 ICLR 最新年份
2. 构造 proceedings / papers 页面 URL
3. 解析列表页中的论文候选项
4. 规范化标题与链接
5. 生成 `PaperRecord`
6. 返回结果与错误信息

### 4.6 `normalize.py`

职责：只保留当前版本需要的轻量清洗逻辑。

建议保留：

- `normalize_whitespace`
- `normalize_title`
- `normalize_url`（如有需要）

建议移除或停用：

- abstract 相关处理
- affiliations 相关处理
- OpenAlex best match 逻辑

### 4.7 `sample.py`

职责：对抓取结果做稳定采样。

因为 accepted papers 数量可能很多，原型阶段仍然建议保留：

- `stable_head_sample(records, sample_size)`

便于快速验证，不必每次抓取全量记录。

### 4.8 `export.py`

职责：导出结果。

保留三个导出接口即可：

- `export_csv`
- `export_jsonl`
- `export_xlsx`

导出内容只面向 Round 3 的最小字段和辅助字段。

### 4.9 `pipeline.py`

职责：串联完整流程，供脚本或后续 agent 调用。

最小入口建议：

- `run_iclr_latest_sample(...)`
- `main()`

流程：

1. 读取配置
2. 调用 `IclrResolver`
3. 显示抓取进度条
4. 可选采样或全量导出
5. 导出文件
6. 输出运行日志

## 5. 处理流程

整体流程如下：

1. 用户指定会议，例如 `ICLR`
2. `pipeline` 加载默认配置
3. `resolver` 找到最新年份
4. `official_pages` 解析 accepted papers 列表
5. `normalize` 清洗标题和链接
6. `resolver` 显示当前处理进度
7. `sample` 截取样本或保留全量（可选）
8. `export` 写出 CSV / JSONL / XLSX

可以概括为：

“会议 -> 最新年份 -> accepted list -> 标题与链接 -> 导出”

## 6. 错误处理与状态设计

虽然当前需求已很简单，但仍需要基本错误处理，避免静默失败。

### 6.1 记录级状态

- `ok`: 标题和论文链接都成功获取
- `partial`: 标题存在，但 `paper_url` 缺失或可疑
- `error`: 该记录解析失败，不建议进入最终导出；若保留则需在 `notes` 中写明原因

### 6.2 运行级错误

`ConferenceRunResult.errors` 建议记录：

- 列表页访问失败
- 最新年份识别失败
- 页面结构变化导致选择器失效
- 导出失败

### 6.3 设计原则

- 单条记录失败不应导致全量流程中断
- 但当 proceedings 页面完全无法解析时，应显式失败并输出错误
- `notes` 应尽量简短、可读、可用于定位页面结构变化
- 长时间抓取时应提供可见的进度条反馈

## 7. 为什么要简化代码

Round 3 的需求已经明确收缩到“会议名、年份、标题、论文 url”。因此设计上应避免继续保留为 abstract / affiliations 设计的大量结构，否则会带来以下问题：

1. 代码路径比需求更复杂，增加维护成本
2. 源站不稳定时，额外抓取只会提高失败率
3. 输出字段过多，不利于快速验证结果是否正确
4. 后续扩展会议时，最难的部分通常是“accepted list 定位”，不是 abstract / affiliation 富化

所以当前最合理的策略是：

- 保留会议解析框架
- 删除或边缘化富化逻辑
- 把实现重心放在“稳定找到 accepted papers 列表并抽取标题与链接”

## 8. 当前推荐落地方案

针对当前仓库，推荐的最小实现组织如下：

- `config.py`: 配置
- `models.py`: 最小记录结构
- `normalize.py`: 标题 / 链接清洗
- `sample.py`: 稳定采样
- `export.py`: 导出
- `pipeline.py`: 入口流程
- `sources/base.py`: HTTP 基础层
- `sources/official_pages.py`: 官方页面抓取
- `resolvers/iclr.py`: ICLR 解析器

如果需要继续简化，下一步甚至可以把：

- `latest.py` 的复杂逻辑合并回 resolver
- `openalex.py` 从主流程中移除
- 详情页解析逻辑降为可选能力

## 9. 验收标准

Round 3 的验收标准应聚焦在最小闭环，而不是字段丰富度：

1. 输入 `ICLR`，能够定位到最新一届年份
2. 能够找到 accepted papers 列表页
3. 能稳定抽取若干条论文记录
4. 每条记录至少包含：
   - `conference`
   - `year`
   - `title`
   - `paper_url`
5. 能导出为 CSV / JSONL / XLSX
6. 当页面结构变化或网络失败时，能输出可读错误信息

## 10. 后续扩展方式

未来如果需求重新扩大，可以按需逐步恢复复杂度，而不是提前保留整套重设计：

1. 先扩展更多会议的 accepted-list resolver
2. 再增加详情页抓取能力
3. 最后才考虑 abstract / authors / affiliations 等富化字段

也就是说，扩展顺序应为：

“多会议 accepted-list 能力” -> “详情页能力” -> “富化字段能力”

这与当前 Round 3 的最小目标是一致的。