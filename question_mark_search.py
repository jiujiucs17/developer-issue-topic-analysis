from scrap_issue_content import *
from cooccurence_network import *
from tqdm import tqdm
import matplotlib.pyplot as plt
import nltk
import re
import pickle

def get_first_comments_as_text(issues_contents: [SingleIssueContent]) -> [str]:
    first_comments = []
    print("getting first comments as text...")
    for issue_content in tqdm(issues_contents):
        first_comment = issue_content.comments[0]
        first_comment_text = first_comment.text_content.lower()
        first_comments.append(first_comment_text)
    return first_comments

def find_all_questions(comments_text: [str]) -> [str]: 
    questions = []
    print("finding all questions...")
    for text in tqdm(comments_text):
        question = re.findall(r"\s*([^\.]*\?)", text)
        if len(question) > 0:
            questions += question
    return questions

def save_results_for_questions(results: [str], output_dir_path: str):
    print("saving results...")
    with open(output_dir_path + "/questions.pkl", "wb") as f:
        pickle.dump(results, f)
    print("results saved")
    return

def load_results_for_questions(dir_path: str) -> [str]:
    print("loading results...")
    with open(dir_path + "/questions.pkl", "rb") as f:
        results = pickle.load(f)
    print("results loaded")
    return results

# change it to search question marks from questions
def count_question_words(comments_text: [str], 
                         plot_path_dir: str,
                         question_words: [str] = ["what", "who", "when", "why", "where", "how"]) -> dict:
    question_words_count = {}
    for word in question_words:
        question_words_count[word] = 0

    print("counting question words...")
    for text in tqdm(comments_text):
        for word in question_words:
            matches = re.findall(r'\b' + word + r'\b', text, re.IGNORECASE)
            question_words_count[word] += len(matches)

    if plot_path_dir != "":
        sorted_keys, sorted_values = zip(*sorted(question_words_count.items(), key=lambda item: item[1], reverse=True))
        bars = plt.bar(sorted_keys, sorted_values)
        plt.xlabel('Question Words')
        plt.ylabel('Count')
        plt.title('Histogram of Question Words')
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')
        plt.savefig(plot_path_dir + "/question_words_histogram.png")
        # plt.show()
    
    return question_words_count

def sample_questions(questions: [str], 
                     question_word: str = "", 
                     output_dir_path: str = "",
                     sample_size: int = 100) -> [str]:
    if question_word == "":
        sample_size = min(sample_size, len(questions))
        random_sample = random.sample(questions, sample_size)    
        with open(output_dir_path + f"/questions_sample_{sample_size}.txt", "w") as f:
            for question in random_sample:
                f.write("\n --------- " + question + "\n")
    else:
        questions_with_word = []
        for question in questions:
            matches = re.findall(r'\b' + question_word + r'\b', question, re.IGNORECASE)
            if len(matches) > 0:
                questions_with_word.append(question)

        sample_size = min(sample_size, len(questions_with_word))
        random_sample = random.sample(questions_with_word, sample_size)    
        with open(output_dir_path + f"/questions_sample_{question_word}_{sample_size}.txt", "w") as f:
            for question in random_sample:
                f.write("\n --------- " + question + "\n")

def word_invalid_for_questions(word: str, skip_stop_words: bool = True, stop_words: set = set(stopwords.words('english'))):
    question_words = ["what", "who", "when", "why", "where", "how"]
    # Remove question words from stop words
    stop_words = stop_words.difference(question_words)

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

if __name__ == "__main__":
    sample_question_number = 100
    question_words = ["what", "who", "when", "why", "where", "how"]
    output_path = "./scrapper_results/question_search_results"

    # prepare the issues contents
    pickle_path_open = "./scrapper_results/open_issues/issues_contents.pkl"
    pickle_path_closed = "./scrapper_results/closed_issues/issues_contents.pkl"

    issues_contents_open = load_saved_results(pickle_path_open)
    issues_contents_closed = load_saved_results(pickle_path_closed)

    # get first comments as text
    open_issues_first_comments = get_first_comments_as_text(issues_contents_open)
    closed_issues_first_comments = get_first_comments_as_text(issues_contents_closed)

    # find all questions
    open_issues_questions = find_all_questions(open_issues_first_comments)
    closed_issues_questions = find_all_questions(closed_issues_first_comments)
    issues_questions = open_issues_questions + closed_issues_questions

    print(f"number of questions in open issues: {len(open_issues_questions)}")
    print(f"number of questions in closed issues: {len(closed_issues_questions)}")
    print(f"number of questions in total: {len(issues_questions)}")

    # save results for question search
    save_results_for_questions(issues_questions, output_path)

    issues_questions = load_results_for_questions(output_path)

    # save a random sample of questions to a txt file
    sample_questions(issues_questions, output_dir_path=output_path, sample_size=sample_question_number)
    for word in question_words:
        print(f"sample questions with word '{word}'")
        sample_questions(issues_questions, question_word=word, output_dir_path=output_path, sample_size=sample_question_number)

    # count question words
    question_words_stats = count_question_words(open_issues_questions + closed_issues_questions,
                                                output_path,
                                                question_words=question_words)
    
    # get co-occurence network of questions
    tokenized_questions = []
    lemmatizer = nltk.stem.WordNetLemmatizer()
    for question in issues_questions:
        tokenized_question = nltk.word_tokenize(question.lower())
        for i in reversed(range(len(tokenized_question))):
            if word_invalid_for_questions(tokenized_question[i]):
                tokenized_question.pop(i)
                continue
            tokenized_question[i] = lemmatizer.lemmatize(tokenized_question[i])
        tokenized_questions.append(tokenized_question)

    cooccurence_pairs, unique_words_total_occurence, cooccurence_pairs_origin_question = get_cooccurence_pairs(tokenized_questions)
    unique_words_pair_count = get_words_pair_counts(cooccurence_pairs)
    plot_questions_storage = plots(cooccurence_pairs, unique_words_total_occurence, unique_words_pair_count)
    plot_questions_storage.plot_interactive_cooccurence_network(dir_path=output_path,
                                                                number_of_pairs=900, 
                                                                height="1250px", 
                                                                width="2500px")