import torch
import importlib
import sys
import pickle
import re
import inspect
import importlib
import pandas as pd
from cooccurence_network import *

class ModuleNamespace:
    def __init__(self, module_name: str, sub_module_names: []):
        self.module_name = module_name
        self.sub_module_names = sub_module_names

def traversedir(module, pref=''):
    for attr in dir(module):
        if attr[0] == '_':
            continue
        if attr not in sys.modules:
            fullname = f'{pref}.{attr}'
            yield fullname
            try:
                importlib.import_module(fullname)
                for submodule in traversedir(getattr(module, attr), pref=fullname):
                    yield submodule
            except:
                continue

def get_first_comments_and_snippets_as_text(issues_contents: [SingleIssueContent]) -> [str]:
    first_comments = []
    print("getting first comments and snippets as text...")
    for issue_content in tqdm(issues_contents):
        first_comment = issue_content.comments[0]
        # data cleaning
        first_comment_text = first_comment.text_content.lower()
        first_comment_snippets = first_comment.snippets_content.lower()
        first_comments.append(first_comment_text + " " + first_comment_snippets)
    return first_comments

def count_occurrence_of_module_names(module_names: [str], first_comments: [str]) -> dict:
    module_namespaces_statistic = {}
    module_namespaces_occurred_in_comments = {}
    print("counting occurence of module names...")
    for module_name in tqdm(module_names):
        # the first element is the depth of the module, for example, torch.nn.functional is 2
        # the second element is the number of occurence of the module name in the first comments
        module_depth = module_name.count(".")

        module_name_split = module_name.split(".")
        module_short_name = module_name_split[-1]

        # count occurence of module name
        # module name has to occure with a space or a dot and a space after it
        # for example, "torch.nn.functional" will not be counted if it is written as "torch.nn.functional.relu"

        count = 0
        comment_list = []
        for i in range(len(first_comments)):
            first_comment = first_comments[i]
            # if re.search(r'\b' + module_short_name + r'(\. | | \? )', first_comment):
            if re.search(r'\b' + module_name + r'(\. | | \? )', first_comment):
                count += 1
                comment_list.append(i)
            # count += first_comment.count(module_sub_name + " ")
            # count += first_comment.count(module_sub_name + ". ")

        module_info = (module_short_name, module_depth, count)
        module_namespaces_statistic[module_name] = module_info
        module_namespaces_occurred_in_comments[module_name] = comment_list

    return module_namespaces_statistic, module_namespaces_occurred_in_comments

def save_results(results, output_path: str):
    print("saving results...")
    with open(output_path, "wb") as f:
        pickle.dump(results, f)
    print("results saved")
    return

def load_saved_results(pickle_path: str):
    print("loading results...")
    with open(pickle_path, "rb") as f:
        results = pickle.load(f)
    print("results loaded")
    return results

def get_pytorch_package_names() -> [str]:
    list_of_modules = []
    for x in traversedir(torch, pref='torch'):
        try:
            module_or_function = importlib.import_module(x)
            if inspect.ismodule(module_or_function) or inspect.isfunction(module_or_function):
                list_of_modules.append(x)
                print("imported module: ", x)
        except Exception as e:
            # print("\nerror importing module: ", x, "\n        ", e)
            pass

    return list_of_modules

def get_comment_sample_for_module_name(module_name: str, 
                                       module_name_comments: dict, 
                                       first_comments: [str], 
                                       dir_path: str, 
                                       sample_size: int = 100) -> [str]:
    sample_size = min(sample_size, len(module_name_comments[module_name]))

    print(f"getting {sample_size} comments mentioning {module_name}...")

    sample = random.sample(module_name_comments[module_name], sample_size)
    sample_comments = []
    for comment_id in sample:
        sample_comments.append(first_comments[comment_id])
    
    with open(dir_path + f"/comments_sample_mentioning_({module_name}).txt", "w" ,encoding="utf-8") as f:
            i = 0
            for comment in sample_comments:
                f.write(f"----------------------------------------Comment {str(i+1)}----------------------------------------\n" + comment + "\n")
                i += 1
    
    return sample_comments

if __name__ == "__main__":
    output_path = "./scrapper_results"
    list_of_modules = get_pytorch_package_names()

    print("number of modules: ", len(list_of_modules))

    # prepare the issues contents
    pickle_path_open = "./scrapper_results/open_issues/issues_contents.pkl"
    pickle_path_closed = "./scrapper_results/closed_issues/issues_contents.pkl"

    issues_contents_open = load_saved_results(pickle_path_open)
    issues_contents_closed = load_saved_results(pickle_path_closed)

    # get first comments as text
    open_issues_first_comments = get_first_comments_and_snippets_as_text(issues_contents_open)
    closed_issues_first_comments = get_first_comments_and_snippets_as_text(issues_contents_closed)

    first_comments = open_issues_first_comments + closed_issues_first_comments

    # print("number of first comments: ", len(first_comments))

    # # count occurence of module names and save to pickle file
    # module_names_count, module_name_comments = count_occurrence_of_module_names(list_of_modules, first_comments)
    # save_results((module_names_count, module_name_comments), output_path + "/module_name_search_results/module_names_count.pkl")

    # load saved results
    module_names_count, module_name_comments = load_saved_results(output_path + "/module_name_search_results/module_names_count.pkl")

    # sort the results by the number of occurence
    sorted_module_names_count = sorted(module_names_count.items(), key=lambda item: item[1][2], reverse=True)

    # Assuming sorted_module_names_count is a list of tuples, where each tuple is in the form of (module_full_name, (module_short_name, depth, occurrence_count))
    df = pd.DataFrame(sorted_module_names_count, columns=['module_full_name', 'temp'])
    df[['module_short_name', 'depth', 'occurrence_count']] = pd.DataFrame(df.temp.tolist(), index= df.index)
    df = df.drop('temp', axis=1)

    save_results(df, output_path + "/module_name_search_results/module_names_count_df.pkl")
    df = load_saved_results(output_path + "/module_name_search_results/module_names_count_df.pkl")
        
    print(df.head(40))
    num_of_modules_to_include = 25
    # get a histogram of the first 20 modules with highest occurrence
    ax = df[:num_of_modules_to_include].plot(x='module_full_name', y='occurrence_count', kind='bar', figsize=(25, 15))
    plt.xlabel('Module Full Name', fontsize=20)
    plt.subplots_adjust(bottom=0.3)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.legend(fontsize=20) 
    plt.title('Module Name Occurrence Count', fontsize=24)
    plt.savefig(output_path + "/module_name_search_results/module_names_count_df_histogram.png")

    # Adjust the position of the x-axis labels
    ax.set_xticklabels(df['module_full_name'][:num_of_modules_to_include], rotation=30, ha="right")

    # Add numbers to the top of the bars
    for bar in ax.patches:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom', fontsize=20)

    plt.savefig(output_path + "/module_name_search_results/module_names_count_df_histogram.png")

    # get a sample of comments mentioning a module name
    important_modules = ["torch.backends.cuda", 
                         "torch.cuda",
                         "torch.version",
                         "torch.backends.cudnn",
                         "torch.autograd.function"]
    
    for important_module_name in important_modules:
        get_comment_sample_for_module_name(important_module_name, 
                                        module_name_comments, 
                                        first_comments, 
                                        output_path + "/module_name_search_results", 
                                        sample_size=100)

