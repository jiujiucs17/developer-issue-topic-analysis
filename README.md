# Developer Issue Topic Analysis

This project analyzes recurring topics, questions, and technical entities in developer issues, using PyTorch GitHub Issues as a case study. It collects open and closed issues from GitHub, cleans and processes the initial issue descriptions, and identifies prominent topics and relationships through word co-occurrence networks. It also analyzes questions, exception types, and PyTorch module mentions to support further research on developer problems and software architecture.

> This repository is a research prototype. Target repositories, input/output paths, and most parameters are currently configured directly in the scripts and should be reviewed before use. The existing `scrapping` and `scrapper` names are historical misspellings; the standard terms are `scraping` and `scraper`.

## Methodology

The analysis pipeline consists of the following steps:

1. **Collect issue links:** Playwright traverses the open and closed PyTorch issue lists and saves their links and collection logs.
2. **Collect issue content:** Requests and Beautiful Soup extract authors, comment text, and code snippets. The results are stored as text files and pickle checkpoints.
3. **Preprocess the text:** The main analysis uses the initial description of each issue. Text is converted to lowercase, tokenized, lemmatized, and filtered to remove stop words, numbers, punctuation, and GitHub issue-template content. Sections such as `Versions`, `Error logs`, `Code example`, `System info`, and `Environment` are excluded to reduce noise from structured environment information.
4. **Identify topics:** Undirected word pairs are counted within a sliding window whose default maximum token distance is 2. The project calculates word frequencies, pair frequencies, and the source issues for each pair, then creates an interactive co-occurrence network with PyVis. Here, a “topic” is interpreted from frequent words, co-occurrence relationships, central network nodes, and manual inspection of sampled issues. This is not a probabilistic topic model such as LDA.
5. **Perform supplementary analyses:**
   - Extract sentences containing question marks and count question words such as `what`, `why`, and `how`.
   - Count occurrences of Python and PyTorch exception types.
   - Count PyTorch module mentions and sample the associated issues.
   - Experimentally explore PyTorch package structure, import relationships, and call graphs.

## Repository Structure

| File | Purpose |
| --- | --- |
| `scrap_issue_links.py` | Traverses GitHub issue lists and collects links; it can also invoke content collection |
| `scrap_issue_content.py` | Collects comment text and code snippets from individual issues or issue lists |
| `cooccurence_network.py` | Cleans text, calculates word co-occurrences, samples source issues, and generates interactive networks |
| `question_mark_search.py` | Analyzes questions, question words, and their co-occurrence network |
| `look_for_errors.py` | Counts Python and PyTorch exception types |
| `module_name_search.py` | Counts PyTorch module mentions and samples related issues |
| `scrapper.ipynb` | Exploratory notebook for issue collection and co-occurrence analysis |
| `nested_network.py`, `create_torch_nn_network.py` | Experimental package-structure, import-relation, and call-graph code; local paths must be updated before use |
| `scrapper_results/` | Collection checkpoints, statistics, samples, plots, and interactive HTML output |
| `notes.md` | Preliminary findings, manual analysis notes, and research ideas |

## Installation

The project was originally developed with Python 3.9. An isolated virtual environment is recommended:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install playwright beautifulsoup4 requests pandas nltk networkx matplotlib tqdm pyvis
playwright install chromium
```

The module-name and architecture analyses also require:

```bash
python -m pip install torch openpyxl jupyter
```

On its first run, the co-occurrence analysis downloads the NLTK `punkt`, `stopwords`, and `wordnet` datasets.

## Usage

Run all commands from the repository root. The scripts currently do not expose command-line arguments. To change the target repository, collection scope, output paths, or analysis parameters, edit the configuration in each script's `if __name__ == "__main__":` block.

### 1. Prepare the Output Directories

The default scripts expect the relevant directories to exist:

```bash
mkdir -p scrapper_results/{open_issues,closed_issues,test_results}/{issues_contents,log_screenshots}
mkdir -p scrapper_results/{cooccurence_network_results,question_search_results,error_search_results,module_name_search_results}
mkdir -p scrapper_results/cooccurence_network_results/important_pairs
```

### 2. Collect Issues

```bash
python scrap_issue_links.py
```

By default, the entry point collects all open and closed PyTorch issues and then retrieves the content of every issue. A complete run may take a long time and generate many network requests. Test the workflow first by enabling `test_link` in `scrap_issue_links.py` and temporarily disabling the full collection calls. Playwright and Beautiful Soup selectors may need to be updated if GitHub changes its page structure.

The main outputs are:

- `scrapper_results/{open_issues,closed_issues}/links.csv`
- `scrapper_results/{open_issues,closed_issues}/issues_contents.pkl`
- Collection reports, screenshots, and per-issue text files in the corresponding directories

### 3. Generate the Co-occurrence Topic Network

```bash
python cooccurence_network.py
```

The script reads the open and closed issue pickle checkpoints and generates co-occurrence statistics, a report, source-issue indexes, sampled text, and `cooccurence_network.html`. The main parameters can be adjusted near the bottom of the script:

- `maximum_word_distance`: co-occurrence window distance; default: `2`
- `number_of_pairs`: number of frequent word pairs displayed in the network; default: `2000`
- `pairs_to_ignore`: noisy word pairs to exclude from the visualization

Open the following file in a browser to explore the interactive topic network:

```text
scrapper_results/cooccurence_network_results/cooccurence_network.html
```

### 4. Run Supplementary Analyses

After generating `issues_contents.pkl`, run:

```bash
python question_mark_search.py
python look_for_errors.py
python module_name_search.py
```

`module_name_search.py` currently loads an existing `module_names_count.pkl` file by default. To recalculate the statistics for new data, uncomment the call to `count_occurrence_of_module_names(...)` and the corresponding save operation.

## Outputs and Reproducibility

- `.gitignore` excludes CSV, TXT, and pickle files by default. Large raw corpora and intermediate checkpoints are therefore usually not committed to Git. Reproducing the full analysis requires recollecting the issues or obtaining these files from the associated research data archive.
- HTML and PNG results are stored under `scrapper_results/`. The interactive HTML output uses the front-end resources in `lib/`.
- GitHub issues may contain personal or sensitive information. Before sharing datasets or samples, review the GitHub terms, applicable research-ethics requirements, and anonymization procedures.
- Use an appropriate request interval to avoid placing unnecessary load on GitHub.

## Scope and Limitations

- The current case study and some entity-recognition logic are specific to PyTorch. The collection and co-occurrence workflow can be adapted to other GitHub repositories by changing the URLs and cleaning rules.
- The analysis mainly uses the initial issue description and therefore does not fully represent later discussion, resolution processes, or participant interactions.
- Issue templates, environment information, logs, and code snippets can dominate frequent word pairs. Rule-based cleaning and manual sampling reduce this noise but cannot remove it completely.
- The dataset covers the full project lifecycle and is suitable for identifying persistent topics, but the current workflow does not directly model how topics change over time.
