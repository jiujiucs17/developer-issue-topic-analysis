from bs4 import BeautifulSoup
import re
import requests
import time
import random
import datetime
import pickle
import pandas as pd

class Comment:
    author_name: str
    text_content: str # contain all the text messages sent by the comment author
    snippets_content: str # contain all the code sent by the comment author

    def __init__(self, author_name: str, text_content: str = None, snippets_content: str = None):
        self.author_name = author_name
        self.text_content = text_content
        self.snippets_content = snippets_content

class SingleIssueContent:
    url: str
    comments: [Comment]
    main_author_name: str
    scrap_time: str
    def __init__(self, url: str, comments: [Comment], main_author_name: str = None) -> None:
        self.url = url
        self.comments = comments
        self.scrap_time = str(datetime.datetime.now())
        if main_author_name is None:
            # if main author name is not provided, function will use the first comment's author name as the main author name of this issue
            self.main_author_name = comments[0].author_name
        else:
            self.main_author_name = main_author_name
    
    def generate_file_output(self, path_to_file: str):
        output_all_comments = f"url: {self.url}\n"
        output_all_comments += f"time of scrapping: {self.scrap_time}\n"
        output_all_comments += f"main author of this issue: {self.main_author_name}"
        for comment in self.comments:
            output_this_comment = "\n--------------------------- comment start ---------------------------\n\n"
            output_this_comment += f"** author:\n{comment.author_name}\n\n"
            output_this_comment += f"** text:\n{comment.text_content}\n\n"
            output_this_comment += f"** snippets:\n{comment.snippets_content}\n\n"
            output_this_comment += "\n--------------------------- comment end ---------------------------\n\n"
            output_all_comments += output_this_comment

        with open(path_to_file, "w", encoding="utf-8") as f:
            f.write(output_all_comments)

        return

def scrap_single_issue(issue_url: str) -> SingleIssueContent:

    try:
        page = requests.get(issue_url)
        # raise Exception("Fake Time Out") # for testing the exception handlers
    except:
        print(f"error requesting {issue_url}")
        raise

    soup = BeautifulSoup(page.content, "html.parser")

    all_comments_elements = soup.find_all("td", class_= "d-block comment-body markdown-body js-comment-body")
    all_authors_elements = soup.find_all("a", class_ = "author Link--primary text-bold css-overflow-wrap-anywhere")

    all_comments = []
    for comment_number in range(len(all_comments_elements)):
        comment_element = all_comments_elements[comment_number] # the html element of this comment

        # get the author
        author = all_authors_elements[comment_number].get_text()

        # get the text and gather the snippet 
        # delete the snippet from the text
        # also will delete the template format of github: "🐛 Describe the bug"
        comment_snippet_elements = comment_element.find_all("pre", class_ = "notranslate")
        comment_text = comment_element.get_text()

            # here, gether snippet and remove them from the plain text
        snippets = ""
        for element in comment_snippet_elements:
            snippet = element.get_text()
            snippets += snippet + "\n\n\n"
            if comment_text.find(snippet) > -1:
                comment_text = comment_text.replace(snippet, "")

        this_comment = Comment(author_name=author,
                               text_content=comment_text,
                               snippets_content=snippets)
        
        all_comments.append(this_comment)

    issue_content = SingleIssueContent(url= issue_url, comments=all_comments)
    return issue_content

def generate_report_and_checkpoint(issues_contents, 
                                   failed_urls, 
                                   elapsed_time, 
                                   result_directory, 
                                   num_of_finished_issues: str = "all"):
    report_string = ""
    report_string += f"\n\n\n------------------ Report ------------------\n\n"
    report_string += f"date of scrapping: {datetime.datetime.now()}\n\n"
    report_string += f"number of scrapped issues: {len(issues_contents)}\n\n"
    report_string += f"number of failed issues: {len(failed_urls)}\n\n"
    report_string += f"time spent: {time.strftime(f'%H Hours %M Minutes, %S Seconds', time.gmtime(elapsed_time))}\n\n"

    if len(failed_urls) > 0:
        report_string += "list of failed urls: \n"
        for url in failed_urls:
            report_string += f"-------{url[0]}: {url[1]}\n"
        print("\n\n")

    report_string += f"--------------------------------------------\n\n"
    print(report_string)

    with open(result_directory + "/issues_contents.pkl", "wb") as f:
        pickle.dump(issues_contents, f, protocol=-1)

    with open(result_directory + '/content_scrapping_report.txt', "w") as f:
        f.write(report_string)

def scrap_issues_content(csv_path: str, 
                         root_url: str = "https://github.com", 
                         result_directory: str = "./scrapper_results/test_results",
                         maximum_wait_time: int = 0) -> [SingleIssueContent]:
    issues_urls = pd.read_csv(csv_path, index_col=0)
    issues_contents = []
    failed_urls = [] # list of tuples, (failed_link: str, its_exception: Exception)
    start_time = time.time()

    for row_num in range(issues_urls.shape[0]):
        rand_wait_time = max(random.randint(-maximum_wait_time, maximum_wait_time), 0)
        if rand_wait_time != 0:
            print(f"waiting {rand_wait_time} seconds before proceeding")
        time.sleep(rand_wait_time)
        print(f"scrapping issue {row_num + 1}")

        issue_url = root_url + issues_urls.iloc[row_num, 0]

        try:
            single_issue_content = scrap_single_issue(issue_url)
        except Exception as e:
            failed_urls.append((issue_url, e))
            print(f"issues {row_num+1} had Exception: {e}")
        else:
            issues_contents.append(single_issue_content)
            single_issue_content.generate_file_output(result_directory+f"/issues_contents/issue_{row_num + 1}.txt")
            print("succeed")

        # update report and checkpoint after every 500 issues
        if (row_num + 1) % 500 == 0:
            print(row_num)
            end_time = time.time()
            elapsed_time = end_time - start_time
            generate_report_and_checkpoint(issues_contents=issues_contents,
                                   failed_urls=failed_urls,
                                   elapsed_time=elapsed_time,
                                   result_directory=result_directory,
                                   num_of_finished_issues=str(row_num+1))

    end_time = time.time()
    elapsed_time = end_time - start_time
    generate_report_and_checkpoint(issues_contents=issues_contents,
                                   failed_urls=failed_urls,
                                   elapsed_time=elapsed_time,
                                   result_directory=result_directory,)

    return issues_contents

def load_saved_results(path: str) -> [SingleIssueContent]:
    with open(path, "rb") as f:
        issues_contents = pickle.load(f)
        return issues_contents

if __name__ == "__main__":
    open_issues_links = "./scrapper_results/open_issues/links.csv"
    closed_issues_links = "./scrapper_results/closed_issues/links.csv"
    test_issues_links = "./scrapper_results/test_results/links.csv"

    # # test all functions
    # test_issues_contents = scrap_issues_content(test_issues_links, result_directory="./scrapper_results/test_results")
    # issues_contents = load_saved_results("./scrapper_results/test_results/issues_contents.pkl")
    # if len(issues_contents) > 0: 
    #     issues_contents[0].generate_file_output("./scrapper_results/test_results/test_file_recovery.txt")

    # test scrap_single_issue()
    # test_issue = scrap_single_issue("https://github.com/pytorch/pytorch/issues/113208")
    # test_issue.generate_file_output("./scrapper_results/test_results/issues_contents/issue_1.txt")

    print("scrapping open issues")
    issues_contents_open = scrap_issues_content(open_issues_links, result_directory="./scrapper_results/open_issues", maximum_wait_time=0)

    print("scrapping closed issues")
    issues_contents_closed = scrap_issues_content(closed_issues_links, result_directory="./scrapper_results/closed_issues", maximum_wait_time=0)






