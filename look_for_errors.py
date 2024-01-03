from cooccurence_network import *
import builtins
import torch
from tqdm import tqdm



if __name__ == '__main__':
    # load the data
    pickle_path_open = "./scrapper_results/open_issues/issues_contents.pkl"
    pickle_path_closed = "./scrapper_results/closed_issues/issues_contents.pkl"
    output_path = "./scrapper_results/error_search_results"

    issues_contents_open = load_saved_results(pickle_path_open)
    issues_contents_closed = load_saved_results(pickle_path_closed)
    issue_contents = issues_contents_open + issues_contents_closed

    # Get a list of all built-in exceptions
    list_of_errors = [item for item in dir(builtins) if item.endswith("Error") or item.endswith("Exception")]

    # Get a list of all exceptions in torch
    list_of_errors  += [item for item in dir(torch) if item.endswith("Error") or item.endswith("Exception")]

    # look for errors in issues
    print("looking for errors in issues...")
    error_appearence_count = {} # count how many issues an error appears in
    for error in tqdm(list_of_errors):
        error_appearence_count[error] = 0
        for issue in issue_contents:
            issue_first_comment = issue.comments[0]
            issue_content = issue_first_comment.text_content + issue_first_comment.snippets_content
            issue_content = issue_content.lower()
            if error.lower() in issue_content:
                error_appearence_count[error] += 1

    # sort the errors by their appearence count
    sorted_errors = sorted(error_appearence_count.items(), key=lambda x: x[1], reverse=True)
    print(sorted_errors)

    # generate a histogram for the sorted errors
    sorted_errors_names = [item[0] for item in sorted_errors]
    sorted_errors_count = [item[1] for item in sorted_errors]
    plt.bar(sorted_errors_names, sorted_errors_count)
    plt.xticks(rotation=90)
    plt.savefig(output_path+"/errors_histogram.png")