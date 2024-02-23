import pickle
import nltk
nltk.download('punkt') # download the newest punkt tokenizer
nltk.download('stopwords') # download the newest stopwords
nltk.download('wordnet') # download the newest wordnet
import random
import re
import math
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from tqdm import tqdm
from pyvis.network import Network
from nltk.corpus import stopwords
from scrap_issue_content import SingleIssueContent, Comment, load_saved_results

class plots:
    cooccurence_pairs: pd.DataFrame
    unique_words_total_count: pd.DataFrame
    unique_words_pair_count: pd.DataFrame
    showed_pairs: pd.DataFrame
    showed_pairs_dict: dict
    word_pair_original_issues: dict

    def __init__(self, cooccurence_pairs: dict, unique_words_significance: dict, unique_words_pair_count: dict, cooccurence_pairs_origin_issue_index: dict):
        self.cooccurence_pairs = pd.DataFrame.from_dict(cooccurence_pairs, orient='index', columns=['count']).sort_values(by=['count'], ascending=False)
        self.unique_words_total_count = pd.DataFrame.from_dict(unique_words_significance, orient='index', columns=['count']).sort_values(by=['count'], ascending=False)
        self.unique_words_pair_count = pd.DataFrame.from_dict(unique_words_pair_count, orient='index', columns=['count']).sort_values(by=['count'], ascending=False)
        self.cooccurence_pairs_origin_issue_index = cooccurence_pairs_origin_issue_index

    def plot_distribution_of_pairs(self, bins: int = 100):
        self.cooccurence_pairs.plot.hist(bins=bins, logy=True, title="Distribution of Pairs")
        plt.show()

    def plot_distribution_of_words_significance(self, bins: int = 100):
        self.unique_words_total_count.plot.hist(bins=bins, logy=True, title="Distribution of Words Pair Numbers")
        plt.show()

    def plot_distribution_of_words_pair_count(self, bins: int = 100):
        self.unique_words_pair_count.plot.hist(bins=bins, logy=True, title="Distribution of Words Pair Count")
        plt.show()

    # pair_list is a list of frozensets, each frozenset contains two words
    def plot_interactive_cooccurence_network(self, 
                                            dir_path: str, 
                                            number_of_pairs: int = 2000, 
                                            height: str = "1000px", 
                                            width: str = "1900px",
                                            pairs_to_ignore: list = []):
        # Get the first number_of_pairs rows from the DataFrame
        print("\n\n---------------plotting interactive cooccurence network--------------")
        number_of_pairs = min(number_of_pairs, len(self.cooccurence_pairs))
        top_pairs = self.cooccurence_pairs.head(number_of_pairs)
        G = Network(notebook=False, height=height, width=width)

        # set the physics layout of the network
        G.options = {
            'configure': {
                'filter': 'rgb(60, 60, 60)'  # Set background color to a deep gray
            },
            'nodes': {
                'shape': 'dot',
                'scaling': {
                    'min': 10,
                    'max': 30
                },
                'shadow': True  # Set shadow option to True for nodes
            },
            'edges': {
                'smooth': False,  # Set smooth option to False for edges
                'shadow': True  # Set shadow option to True for edges
            },
            # 'physics': {
            #     'enabled': False,  # Disable physics
            #     'forceAtlas2Based': {
            #         'avoidOverlap': 1
            #     },
            # }
            'physics': {
                'stabilization': True,
                'stabilization.iterations': 1000,
                'solver': 'forceAtlas2Based',
                'forceAtlas2Based': {
                    'avoidOverlap': 0.5,
                    'springLength': 100,
                    'springConstant': 0.05
                },
                'minVelocity': 0.75,
            }
        }

        print("\ngenerating html file...")
        showed_pairs = {}
        for index, row in tqdm(top_pairs.iterrows(), total=number_of_pairs):
            pair = index
            count = int(row['count'])  # convert count to native int type
            pair_list = list(pair)

            # if the pair is in the pairs_to_ignore list, skip this pair
            if pair in pairs_to_ignore:
                continue

            # Set node size based on the significance value in unique_words_significance
            node_size1 = int(self.unique_words_total_count.loc[pair_list[0], 'count'])
            node_size2 = int(self.unique_words_total_count.loc[pair_list[1], 'count'])
            G.add_node(pair_list[0], value=node_size1)
            G.add_node(pair_list[1], value=node_size2)
            G.add_edge(pair_list[0], pair_list[1], value=count, title=str(count)) # add title to edge

            # add the pair to showed_pairs
            showed_pairs[pair] = count
        self.showed_pairs = pd.DataFrame.from_dict(showed_pairs, orient='index', columns=['count']).sort_values(by=['count'], ascending=False)  
        self.showed_pairs_dict = showed_pairs 
        # Get the number of nodes and edges
        num_of_nodes = G.num_nodes()
        num_of_edges = G.num_edges()
        print(f"number of nodes: {num_of_nodes} \nnumber of edges: {num_of_edges}")

        # Provide options of physics layout of the network in the interface
        # G.show_buttons(filter_=['physics', "nodes", "edges", "layout", "interaction", "manipulation", "physics"])
        G.save_graph(dir_path + "/cooccurence_network.html")
        print("\n------------------------------finished------------------------------\n")

    def get_word_pair_count_in_showed_network(self, 
                                  number_of_clusters: int = 10, 
                                  height: str = "1000px", 
                                  width: str = "1900px"):
        print("\n\n---------------getting clusters from cooccurence network--------------")
        # Get the first number_of_pairs rows from the DataFrame
        number_of_pairs = min(number_of_clusters, len(self.cooccurence_pairs))
        top_pairs = self.showed_pairs.head(number_of_pairs)

        word_pair_count = {}
        for index, row in tqdm(top_pairs.iterrows(), total=number_of_pairs):
            index_tuple = list(index)
            word_1 = index_tuple[0]
            word_2 = index_tuple[1]
            for word in [word_1, word_2]:
                if word in word_pair_count:
                    word_pair_count[word] += 1
                else:
                    word_pair_count[word] = 1
               
        return word_pair_count
    
    def get_important_showed_pairs(self, number_of_clusters: int = 10):
        important_pairs = {}
        # showed_pairs_dict = self.showed_pairs.to_dict()
        for word in showed_word_pair_count_important.index:
            word_pairs = get_pairs_contain_word(self.showed_pairs_dict, word, sort=True)
            important_pairs[word] = list(word_pairs.items())[:5]
        print("\n\n---------------important surronding pairs around the clusters--------------")
        print("\n\npair, count of total occurrence, count of occured issues")
        for word in important_pairs:
            print(f"\nword: {word}")
            for pair in important_pairs[word]:
                # print the pair and its value
                num_appeared_issues = len(self.cooccurence_pairs_origin_issue_index[frozenset(pair[0])])
                print(pair, num_appeared_issues)
        return important_pairs

def calculate_sample_size(population_size, confidence_level, margin_of_error):
    # Z-score for the given confidence level
    if confidence_level == 0.90:
        z = 1.645
    elif confidence_level == 0.95:
        z = 1.96
    elif confidence_level == 0.99:
        z = 2.576
    else:
        raise ValueError("Invalid confidence level. Choose from 0.90, 0.95, or 0.99.")

    # Proportion (assuming maximum variability i.e., p = 0.5)
    p = 0.5

    # Calculate the sample size
    sample_size = (z**2 * p * (1-p)) / (margin_of_error**2)

    # Adjust the sample size for finite population
    sample_size = sample_size / (1 + ((sample_size - 1) / population_size))

    return math.ceil(sample_size)  # Round up to the nearest whole number

def get_first_comments_as_list_of_words(issues_contents: [SingleIssueContent], 
                                        skip_stop_words: bool = True, 
                                        stop_words: set = set(stopwords.words('english')), 
                                        stem: bool = False, 
                                        lemmatize: bool = True,
                                        ignore_list_of_sections: bool = True) -> [[str]]:
    
    list_of_words = []
    lemmatizer = nltk.stem.WordNetLemmatizer()
    stemmer = nltk.stem.PorterStemmer()
    print("\nextracting first comments...")
    for issue_content in tqdm(issues_contents):
        comment = issue_content.comments[0]
        text_comment = comment.text_content.lower()

        # delete the fout sections: "versions", "error logs", "code example", "system info"
        # use regular expression, ignore all texts after the section title, till the end of comment
        if ignore_list_of_sections:
            section_titles = ["versions", 
                            "error logs", 
                            "code example", 
                            "system info", 
                            "system information", 
                            "system info", 
                            "environment"]
            for section_title in section_titles:
                text_comment = re.sub(section_title + ".*", "", text_comment, flags=re.DOTALL)

        # also, delete several format string of issues, but keep the content after them
        format_string = ["🐛 Describe the bug", 
                         "🚀 The feature, motivation and pitch",
                         "📚 The doc issue"]
        for string in format_string:
            text_comment = re.sub(string, "", text_comment)
            
        # # delete urls
        # text_comment = re.sub(r"http\S+", "", text_comment)

        # data pre-processing and cleaning
        tokenized_comment = nltk.word_tokenize(text_comment)

        # remove all the invalid words and put all the words into lower case
        # perform stemming or lemmatization,
        # if both stem and lemmatize are true, perform lemmatization
        for i in reversed(range(len(tokenized_comment))):
            if word_invalid(tokenized_comment[i], skip_stop_words, stop_words):
                tokenized_comment.pop(i)
                continue
            if lemmatize:
                tokenized_comment[i] = lemmatizer.lemmatize(tokenized_comment[i])
                continue
            elif stem:
                tokenized_comment[i] = stemmer.stem(tokenized_comment[i])
                continue
        
        # perform data pre-processing on text, 
        # tokenize the text into words,
        # and put all the words into lower case
        list_of_words.append(tokenized_comment)
    return list_of_words

def word_invalid(word: str, skip_stop_words: bool = True, stop_words: set = set(stopwords.words('english'))):
    # if the word is not a word, skip it
    if re.match("\W+", word): return True
    # if the word is a stop word, skip it
    elif skip_stop_words and (word in stop_words): return True
    # if the word is a pure number, skip it
    elif re.match("^\d+$", word): return True
    # if the word is a number with one decimal point, skip it
    elif re.match("^\d+\.\d+$", word): return True
    # if the word is a number with two decimal points, skip it
    elif re.match("^\d+\.\d+\.\d+$", word): return True
    return False

# for each word, count the sum of the occurence of all the pairs it is in
def get_words_pair_counts(cooccurence_pairs: dict):
    unique_word_total_occurence = {}
    print("\ncalculating pair counts of each word...")
    for pair in tqdm(cooccurence_pairs):
        # if pair == frozenset(['version', 'runtime']):
        #     print(pair_significance, pair, unique_word_significance['version'], unique_word_significance['runtime'])
        
        for word in pair:
            if word in unique_word_total_occurence:
                unique_word_total_occurence[word] += 1
            else:
                unique_word_total_occurence[word] = 1
        
        # if pair == frozenset(['version', 'runtime']):
        #     print(unique_word_significance['version'], unique_word_significance['runtime'])
        #     break
    return unique_word_total_occurence
    
def get_cooccurence_pairs(corpus: [[str]], maximum_word_distance: int = 2):
    cooccurence_pairs = {}
    cooccurence_pairs_origin_issues = {}
    unique_words_total_occurence = {}

    # for each comment, get all the cooccurence pairs
    print("\nextracting cooccurence pairs...")
    for issue_num in tqdm(range(len(corpus))):
        comment = corpus[issue_num]

        # for each word in the comment, get their cooccurence pairs base on the maximum_word_distance
        # stop if the word is too close to the end of the comment
        for i in range(len(comment) - maximum_word_distance):
            # get the first word
            # and perform some filtering (e.g. stop words, non-words)
            first_word = comment[i]

            # check if the word pair is already in the dictionary, 
            # if so, increment the count, 
            # otherwise, add it to the dictionary
            for j in range(maximum_word_distance):

                # get the second word
                # and perform some filtering (e.g. stop words, non-words)
                second_word = comment[i+j+1] 
                # if the two words are the same, skip it
                if first_word == second_word:
                    continue

                words_pair = frozenset([first_word, second_word])
                    
                # add the words pair to the cooccurence_pairs dictionary
                if words_pair in cooccurence_pairs:
                    cooccurence_pairs[words_pair] += 1
                else:
                    cooccurence_pairs[words_pair] = 1
                
                # add the words pair to the cooccurence_pairs_origin_issues dictionary
                if words_pair in cooccurence_pairs_origin_issues:
                    if issue_num not in cooccurence_pairs_origin_issues[words_pair]:
                        cooccurence_pairs_origin_issues[words_pair].append(issue_num)
                else:
                    cooccurence_pairs_origin_issues[words_pair] = [issue_num]

                # add the words to the unique_words dictionary
                # this is used to calculate the total number of words pairs each word has
                for word in [first_word, second_word]:
                    if word in unique_words_total_occurence:
                        unique_words_total_occurence[word] += 1
                    else:
                        unique_words_total_occurence[word] = 1

    return cooccurence_pairs, unique_words_total_occurence, cooccurence_pairs_origin_issues

def cooccurence_network(issue_contents: [SingleIssueContent], maximum_word_distance: int = 2, skip_stop_words: bool = True, stem: bool = False, lemmatize: bool = True):
    output_string = ""
    output_string += f"\n\n------------------------getting cooccurence pairs-------------------------\n" 
    print(f"\n\n------------------------getting cooccurence pairs-------------------------\n")    
    first_comments = get_first_comments_as_list_of_words(issue_contents, skip_stop_words=skip_stop_words, stem=stem, lemmatize=lemmatize)
    cooccurence_pairs, unique_words_total_occurence, cooccurence_pairs_origin_issue_index = get_cooccurence_pairs(first_comments, maximum_word_distance=maximum_word_distance)
    unique_words_pair_count = get_words_pair_counts(cooccurence_pairs)

    max_cooccurence_pair = max(cooccurence_pairs, key=cooccurence_pairs.get)
    output_string += f"\nthe most occured word pair is: \n{max_cooccurence_pair},"
    output_string += f" occured {cooccurence_pairs[max_cooccurence_pair]} times\n"
    
    max_unique_word = max(unique_words_total_occurence, key=unique_words_total_occurence.get)
    output_string += f"\nthe word has the most total occurence is: {max_unique_word},"
    output_string += f" occured {unique_words_total_occurence[max_unique_word]} times"
    output_string += f" in {unique_words_pair_count[max_unique_word]} pairs"
    
    max_unique_word_significance = max(unique_words_pair_count, key=unique_words_pair_count.get)
    output_string += f"\nthe word occured in the most pairs is: {max_unique_word_significance},"
    output_string += f" occured {unique_words_total_occurence[max_unique_word_significance]} times"
    output_string += f" in {unique_words_pair_count[max_unique_word_significance]} pairs\n"
    
    avg_pair_count = sum(cooccurence_pairs.values()) / len(cooccurence_pairs)
    avg_word_pair_count = sum(unique_words_pair_count.values()) / len(unique_words_pair_count)
    avg_word_significance = sum(unique_words_total_occurence.values()) / len(unique_words_total_occurence)
    output_string += f"the average number of pairs each word has is: {round(avg_word_pair_count, 3)}\n"
    output_string += f"the average number of occurence each word has is: {round(avg_word_significance, 3)}\n"
    output_string += f"the average number of occurence each pair has is: {round(avg_pair_count, 3)}\n"
    
    output_string += "\n\n----------------------------finished---------------------------------\n"
    print("\n\n----------------------------finished---------------------------------\n")
    print(output_string)
        
    return cooccurence_pairs, unique_words_total_occurence, unique_words_pair_count, output_string, cooccurence_pairs_origin_issue_index

def save_variables_to_checkpoint(dir_path: str, cooccurence_pairs: dict, unique_words_total_occurence: dict, unique_words_pair_count: dict, pairs_origin_issue_index: dict = None):
    print(f"\nsaving variables to {dir_path}...")
    with open(dir_path+"/co_occurence_pairs.pkl", "wb") as f:
        pickle.dump(cooccurence_pairs, f, protocol=-1)

    with open(dir_path+"/unique_words_total_occurence.pkl", "wb") as f:
        pickle.dump(unique_words_total_occurence, f, protocol=-1)

    with open(dir_path+"/unique_words_pair_count.pkl", "wb") as f:
        pickle.dump(unique_words_pair_count, f, protocol=-1)

    with open(dir_path+"/cooccurence_pairs_origin_issue_index.pkl", "wb") as f:
        pickle.dump(pairs_origin_issue_index, f, protocol=-1)

    print(f"saved")

def load_variables_from_checkpoint(dir_path: str):
    print(f"\nloading variables from {dir_path}...")
    with open(dir_path+"/co_occurence_pairs.pkl", "rb") as f:
        cooccurence_pairs = pickle.load(f)

    with open(dir_path+"/unique_words_total_occurence.pkl", "rb") as f:
        unique_words_total_occurence = pickle.load(f)

    with open(dir_path+"/unique_words_pair_count.pkl", "rb") as f:
        unique_words_pair_count = pickle.load(f)

    with open(dir_path+"/cooccurence_pairs_origin_issue_index.pkl", "rb") as f:
        cooccurence_pairs_origin_issue_index = pickle.load(f)

    print(f"loaded")
    return cooccurence_pairs, unique_words_total_occurence, unique_words_pair_count, cooccurence_pairs_origin_issue_index

def save_report_to_file(dir_path: str, report_str: str):
    print("\nsaving report to file...")
    with open(dir_path+"/cooccurence_network_report.txt", "w") as f:
        f.write(report_str)
    print("saved")

def get_cooccurence_pairs_origin_issues(cooccurence_pairs_origin_issue_index: dict, issues_contents: [SingleIssueContent]):
    cooccurence_pairs_origin_issues_issue_contents = {}
    
    print("\ngetting origin issues of each pair...")
    for pair in tqdm(cooccurence_pairs_origin_issue_index):
        issue_nums = cooccurence_pairs_origin_issue_index[pair]
        issue_url_contents = [(issues_contents[i].url, issues_contents[i].comments[0].text_content) for i in issue_nums]
        cooccurence_pairs_origin_issues_issue_contents[pair] = issue_url_contents
    return cooccurence_pairs_origin_issues_issue_contents

def get_comment_sample_for_pair(pair_list: list, 
                                cooccurence_pairs_origin_issues_issue_contents: dict, 
                                sample_size: int = None, 
                                dir_path: str = None, 
                                log: bool = True,
                                confidence_level: float = None,
                                margin_of_error: float = None):
    
    if sample_size is None and (confidence_level is None or margin_of_error is None):
        raise Exception("sample_size or confidence_level and margin_of_error must be provided")

    if log:
        print(f"\ngetting sample of comments for pair ({pair_list[0]}, {pair_list[1]})...")
    if len(pair_list) != 2:
        raise Exception("pair must be a list of two words")
    pair_set = frozenset(pair_list)
    comments_url_content = cooccurence_pairs_origin_issues_issue_contents[pair_set]
    if sample_size is None:
        sample_size = calculate_sample_size(len(comments_url_content), confidence_level, margin_of_error)
    sample_size = min(sample_size, len(comments_url_content))
    sample = random.sample(comments_url_content, sample_size)
    if dir_path:
        with open(dir_path + f"/sample_of_({pair_list[0]},{pair_list[1]})_size_{sample_size}_popu_{len(comments_url_content)}.txt", "w" ,encoding="utf-8") as f:
            i = 0
            for comment in sample:
               f.write(f"----------------------------------------Comment {str(i+1)}----------------------------------------\nurl: " + comment[0] + "\n" + comment[1] + "\n")
               i += 1
    if log:
        print("finished")
    return sample

def get_pairs_contain_word(cooccurence_pairs: dict, word: str, sort: bool = True):
    word_pairs = {}
    for pair in cooccurence_pairs:
        if word in pair:
            # make sure the word is the first element in the pair tuple as the key
            key = tuple(pair)
            if key[0] != word:
                key = (key[1], key[0])
            word_pairs[key] = cooccurence_pairs[pair]
            # print("word: ", word, "key: ", key, "\n cooccurence_pairs[pair]: ", cooccurence_pairs[pair], "\n")    
    if sort:
        word_pairs = dict(sorted(word_pairs.items(), key=lambda item: item[1], reverse=True))
    return word_pairs

if __name__ == "__main__":
    number_of_pairs = 2000
    # prepare the issues contents
    pickle_path_open = "./scrapper_results/open_issues/issues_contents.pkl"
    pickle_path_closed = "./scrapper_results/closed_issues/issues_contents.pkl"
    output_path = "./scrapper_results/cooccurence_network_results"

    # set up pairs to ignore in the cooccurence network
    pairs_to_ignore = [frozenset(("", ""))]

    issues_contents_open = load_saved_results(pickle_path_open)
    issues_contents_closed = load_saved_results(pickle_path_closed)

    issue_contents = issues_contents_open + issues_contents_closed

    # udpate the cooccurence network
    coocurence_pairs, unique_words_total_occurence, unique_words_pair_count, report_str, cooccurence_pairs_origin_issue_index = cooccurence_network(issue_contents, maximum_word_distance=2, stem=False, lemmatize=True)

    # save the variables related to the network to checkpoints
    save_variables_to_checkpoint(output_path,  
                                 cooccurence_pairs=coocurence_pairs, 
                                 unique_words_total_occurence=unique_words_total_occurence, 
                                 unique_words_pair_count=unique_words_pair_count,
                                 pairs_origin_issue_index=cooccurence_pairs_origin_issue_index)
    save_report_to_file(output_path, report_str)

    # load the variables from checkpoint
    cooccurence_pairs, unique_words_total_occurence, unique_words_pair_count, cooccurence_pairs_origin_issue_index = load_variables_from_checkpoint(output_path)

    # get the origin issues of each pair
    cooccurence_pairs_origin_issues_issue_contents = get_cooccurence_pairs_origin_issues(cooccurence_pairs_origin_issue_index, issue_contents)

    # generate interactive cooccurence network
    plots_storage = plots(cooccurence_pairs, unique_words_total_occurence, unique_words_pair_count, cooccurence_pairs_origin_issue_index)
    plots_storage.plot_interactive_cooccurence_network(dir_path=output_path, 
                                                       number_of_pairs=number_of_pairs, 
                                                       height="1250px", 
                                                       width="2500px",
                                                       pairs_to_ignore=pairs_to_ignore)

    # get the word pair count in the showed network
    showed_word_pair_count = plots_storage.get_word_pair_count_in_showed_network(number_of_clusters=number_of_pairs)
    showed_word_pair_count = pd.DataFrame.from_dict(showed_word_pair_count, 
                                                    orient='index', 
                                                    columns=['count']).sort_values(by=['count'], 
                                                    ascending=False)
    # plot the distribution of the first 100 word pair count in the showed network and save it to file
    showed_word_pair_count.plot(kind='line', logy=True, title="Distribution of Words Pair Count in Showed Network")
    # Define a custom formatter function
    def format_y(value, _):
        return f'{value:.0f}'

    # Apply the custom formatter to the y-axis
    plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(format_y))
    # save the plot to file
    plt.savefig(output_path + "/distribution_of_words_pair_count_in_showed_network.png")

    # select the first 1.5% of the word pair count in the showed network
    showed_word_pair_count_important = showed_word_pair_count.head(math.ceil(showed_word_pair_count.shape[0] * 0.015))
    print("\n\n---------------important cluster cores in the network--------------")
    print(showed_word_pair_count_important)

    # get first 5 pairs and their values for each words in the showed_word_pair_count_important
    # put the value as the third element of the tuple
    important_pairs = plots_storage.get_important_showed_pairs(number_of_clusters=10)

    # print(important_pairs)

    # get the sample origin issues of each pair in important_pairs
    # remember to delete all existing files in the output_path/important_pairs folder before running this
    print("\n\noutput sample origin issues of each pair in txt files...")
    samples_of_issues_contain_pairs = {}
    for word in important_pairs:
        samples_of_issues_contain_pairs[word] = []
        for pair in important_pairs[word]:
            sample = get_comment_sample_for_pair(list(pair[0]), 
                                                 cooccurence_pairs_origin_issues_issue_contents, 
                                                 dir_path=output_path + "/important_pairs",
                                                 log = False,
                                                 confidence_level=0.9,
                                                 margin_of_error=0.1)
            samples_of_issues_contain_pairs[word].append(sample)
    print("done")

    # print(cooccurence_pairs_origin_issue_index[frozenset(("error", "reference"))])

    # print the average occurrrence of each pair in the network
    print("\n\n---------------average/median occurrrence of each pair in the network--------------")
    print(sum(coocurence_pairs.values()) / len(coocurence_pairs))
    print(pd.DataFrame.from_dict(coocurence_pairs, orient='index', columns=['count']).sort_values(by=['count'], ascending=False).median())
    # print the average occurrence of pairs contain "error" in the network
    print("\n\n---------------average occurrence of pairs contain \"error\" in the network--------------")
    print(sum(get_pairs_contain_word(coocurence_pairs, "error").values()) / len(get_pairs_contain_word(coocurence_pairs, "error")))