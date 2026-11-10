# Developer Issue Topic Analysis

本项目以 PyTorch GitHub Issues 为案例，分析开发者在 issue 中反复讨论的主题、问题和技术实体。项目从 GitHub 抓取 open/closed issues，对首条 issue 描述进行清洗和自然语言处理，并通过词共现网络识别高频主题及其关联；此外还统计疑问句、异常类型和 PyTorch 模块名，为后续的软件架构与开发者问题研究提供依据。

> 当前代码是研究型原型：目标仓库、输入输出路径和大部分参数直接写在脚本中，运行前请按研究范围修改配置。仓库名称中的 `scrapping`/`scrapper` 是历史拼写，准确写法应为 `scraping`/`scraper`。

## 分析方法

整体流程如下：

1. **采集 issue 链接**：使用 Playwright 遍历 PyTorch 的 open/closed issue 列表页，保存链接和抓取日志。
2. **采集 issue 内容**：使用 Requests 和 Beautiful Soup 提取作者、评论正文及代码片段，并将结果保存为文本和 pickle 检查点。
3. **文本预处理**：主要分析每个 issue 的首条描述；转为小写，移除停用词、数字、标点和 GitHub issue 模板内容，并进行词形还原。为减少环境信息造成的噪声，还会忽略 `Versions`、`Error logs`、`Code example`、`System info`、`Environment` 等区段。
4. **主题识别**：在默认距离为 2 个 token 的滑动窗口内统计无向词对，计算词频、词对频率及出现该词对的原始 issues，并用 PyVis 生成交互式词共现网络。这里的“topic”是通过高频词、共现关系、网络核心节点及原始 issue 抽样解释得到的，并非 LDA 等概率主题模型。
5. **补充分析**：
   - 提取带问号的句子并统计 `what`、`why`、`how` 等疑问词；
   - 统计 Python/PyTorch 异常类型在 issues 中的出现次数；
   - 统计 PyTorch 模块名的提及次数，并抽样查看相关 issue；
   - 实验性探索 PyTorch 包结构、导入关系和调用图。

## 主要文件

| 文件 | 用途 |
| --- | --- |
| `scrap_issue_links.py` | 遍历 GitHub issue 列表并抓取链接；也可继续调用内容抓取 |
| `scrap_issue_content.py` | 抓取单个或批量 issue 的评论正文与代码片段 |
| `cooccurence_network.py` | 文本清洗、词共现统计、抽样和交互式网络生成 |
| `question_mark_search.py` | 疑问句、疑问词及其共现网络分析 |
| `look_for_errors.py` | Python/PyTorch 异常类型统计 |
| `module_name_search.py` | PyTorch 模块名提及统计和 issue 抽样 |
| `scrapper.ipynb` | 抓取与共现分析的探索性 Notebook |
| `nested_network.py`、`create_torch_nn_network.py` | 包结构、导入关系和调用图的实验性代码，含本地路径，需修改后使用 |
| `scrapper_results/` | 抓取检查点、统计结果、样本、图表和交互式 HTML |
| `notes.md` | 初步结果、人工分析记录和研究思路 |

## 环境安装

该项目最初在 Python 3.9 环境中开发。建议使用独立虚拟环境：

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install playwright beautifulsoup4 requests pandas nltk networkx matplotlib tqdm pyvis
playwright install chromium
```

模块名和架构相关分析还需要：

```bash
python -m pip install torch openpyxl jupyter
```

首次运行共现分析时，脚本会通过 NLTK 下载 `punkt`、`stopwords` 和 `wordnet` 数据。

## 使用方式

所有命令均在项目根目录执行。脚本目前没有命令行参数；更换目标仓库、抓取范围或输出目录时，需要修改各脚本 `if __name__ == "__main__":` 区域中的 URL、路径和参数。

### 1. 准备输出目录

默认脚本要求相关目录已经存在：

```bash
mkdir -p scrapper_results/{open_issues,closed_issues,test_results}/{issues_contents,log_screenshots}
mkdir -p scrapper_results/{cooccurence_network_results,question_search_results,error_search_results,module_name_search_results}
mkdir -p scrapper_results/cooccurence_network_results/important_pairs
```

### 2. 抓取 issues

```bash
python scrap_issue_links.py
```

默认入口会抓取 PyTorch 的全部 open 和 closed issues，然后抓取每个 issue 的内容。完整运行耗时较长，也会产生大量网络请求；建议先在 `scrap_issue_links.py` 中启用 `test_link`，并暂时关闭完整抓取调用。GitHub 页面结构变化时，Playwright/Beautiful Soup 选择器也可能需要更新。

主要输出包括：

- `scrapper_results/{open_issues,closed_issues}/links.csv`
- `scrapper_results/{open_issues,closed_issues}/issues_contents.pkl`
- 对应的抓取报告、截图和逐 issue 文本

### 3. 生成词共现主题网络

```bash
python cooccurence_network.py
```

脚本读取 open/closed issues 的 pickle 检查点，生成共现统计、报告、原始 issue 索引、抽样文本和 `cooccurence_network.html`。核心参数可在脚本底部调整：

- `maximum_word_distance`：共现窗口距离，默认 `2`；
- `number_of_pairs`：网络中展示的高频词对数量，默认 `2000`；
- `pairs_to_ignore`：需要从可视化中排除的噪声词对。

用浏览器打开以下文件即可交互查看主题网络：

```text
scrapper_results/cooccurence_network_results/cooccurence_network.html
```

### 4. 运行补充分析

在已有 `issues_contents.pkl` 的前提下运行：

```bash
python question_mark_search.py
python look_for_errors.py
python module_name_search.py
```

其中 `module_name_search.py` 当前默认加载已经保存的 `module_names_count.pkl`。如果需要对新数据重新统计，请取消脚本中 `count_occurrence_of_module_names(...)` 及其保存代码的注释。

## 输出与复现说明

- `.gitignore` 默认忽略 CSV、TXT 和 pickle 文件，因此大体积原始语料和中间检查点通常不会提交到 Git；复现完整分析需要先重新抓取，或从研究数据存档中取得这些文件。
- HTML 和 PNG 结果保存在 `scrapper_results/` 下，可直接查看；交互式 HTML 依赖仓库中的 `lib/` 前端资源。
- GitHub issue 可能包含个人信息或敏感内容。共享数据集或样本前，请检查 GitHub 条款、研究伦理要求及匿名化方案。
- 请控制请求频率，避免对 GitHub 服务造成不必要的压力。

## 当前范围与局限

- 当前案例和部分实体识别逻辑与 PyTorch 强相关，但抓取与共现分析流程可以通过修改 URL 和规则迁移到其他 GitHub 项目。
- 分析主要使用首条 issue 描述，不能完整反映后续讨论、解决过程或参与者互动。
- issue 模板、环境信息、日志和代码片段可能主导高频词对；当前使用规则清洗和人工抽样解释，但仍可能存在噪声。
- 数据覆盖项目完整生命周期，适合寻找长期稳定主题，但当前流程未直接建模主题随时间的变化。

