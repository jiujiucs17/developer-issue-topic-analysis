from playwright.sync_api import Playwright, sync_playwright, TimeoutError as PlaywrightTimeoutError
import time
import random
import datetime
import scrap_issue_content
import pandas as pd


def get_list_of_issue_links(playwright: Playwright, 
                            start_page_url: str, 
                            result_direcotry: str, 
                            maximum_wait_time: int = 10,
                            headless: bool = False) -> ([str], [int], int, int):
    # ---------------------
    root_url = "https://github.com"

    # ---------------------
    # set up the playwright browser
    browser = playwright.chromium.launch(headless=headless)
    context = browser.new_context()
    page = context.new_page()

    # ---------------------
    # open the webpage using the provided url
    page.goto(start_page_url)
    page.wait_for_url(start_page_url) # make sure the page is fully loaded

    num_of_page = 0
    button_next_page = page.get_by_role("link", name="Next", exact=True)
    page.screenshot(path=f"{result_direcotry}/log_screenshots/{str(num_of_page+1)}.png", full_page=True)
    big_list_of_links = []
    list_of_num_of_links_each_page = []
    sum_num_of_links = 0

    once_more = True
    while once_more:
        # ---------------------
        # make sure the while loop run one more time at the last page
        try:
            if (button_next_page.get_attribute('class', timeout=6000) == "next_page"):
                once_more = True
        except PlaywrightTimeoutError:
            print("have reached the last page")
            once_more = False

        # ---------------------
        # extract elements containing the links to issues on the page
        # can be improved using id identifier and genex
        link_wrappers = page.locator('xpath=//*[contains(@id, "issue_") and contains(@id, "_link")]').all()

        # ---------------------
        # extract links from the elements and save them into a list
        # update variables for one page, these vairiables only change at the beginning of and within this for loop
        num_of_links=0
        list_of_links = []
        for wrapper in link_wrappers:
            link = wrapper.get_attribute('href')
            # print(num_of_links, ": ", link, "\n")
            list_of_links.append(link)
            num_of_links += 1
        
        # ---------------------
        # update the variables for all pages
        sum_num_of_links += num_of_links
        list_of_num_of_links_each_page.append(num_of_links)
        big_list_of_links.extend(list_of_links)

        # ---------------------
        # if this already the last page, then don't try to go to the next page 
        # (to avoid playwight waiting for timeout due to not able to find the button)
        if once_more == False: break 
        # if this is not the last page, 
        # wait random seconds (between 0-5), then
        # go to next page
        rand_wait_time = max(random.randint(-maximum_wait_time, maximum_wait_time), 0)
        print(f"waiting {rand_wait_time} seconds for page No.{num_of_page+1}")
        time.sleep(rand_wait_time)
        try: 
            button_next_page.click()
            page.wait_for_url(root_url + button_next_page.get_attribute('href')) # make sure the page is fully loaded
            page.wait_for_selector('#repo-content-pjax-container > div > div.paginate-container.d-none.d-sm-flex.flex-sm-justify-center > div > a.next_page')
            button_next_page = page.get_by_role("link", name="Next", exact=True)
            num_of_page += 1
            page.screenshot(path=f"{result_direcotry}/log_screenshots/{str(num_of_page+1)}.png", full_page=True)
        except:
            print(f"saving error screenshot, {num_of_page}")
            page.screenshot(path=f"{result_direcotry}/error_screenshot.png", full_page=True)
            break

    # ---------------------
    # clear the browser
    context.close()
    browser.close()

    # ---------------------
    return (big_list_of_links, list_of_num_of_links_each_page, sum_num_of_links, num_of_page+1)

def scrap_link(start_page_url: str, 
               result_directory: str, 
               playwright: Playwright, 
               maximum_wait_time: int = 5, 
               headless: bool = True):
    start_time = time.time()
    list_of_links, list_of_num_of_links_each_page, sum_num_of_links, num_of_page = get_list_of_issue_links(playwright, 
                                                                                                           start_page_url, 
                                                                                                           result_directory, 
                                                                                                           maximum_wait_time, 
                                                                                                           headless)
    end_time = time.time()
    elapsed_time = end_time - start_time

    report_string = ""
    report_string += f"\n\n\n------------------ Report ------------------\n\ndate of scrapping: {datetime.datetime.now()}\n\n"
    report_string += f"length of list_of_links: {len(list_of_links)}\n\n"
    report_string += f"length of list_of_num_of_links_each_page: {len(list_of_num_of_links_each_page)}\n\n"
    report_string += f"sum_num_of_links: {sum_num_of_links}\n\nscrapped pages: {num_of_page}\n\n"
    report_string += "time spent: " + time.strftime("%M Minutes, %S Seconds", time.gmtime(elapsed_time)) + "\n\n"
    report_string += f"--------------------------------------------\n\n"
    print(report_string)

    # write results to external files
    write_data = pd.DataFrame(columns=['links'], data=list_of_links)
    write_data.to_csv(result_directory + '/links.csv')
    with open(result_directory + '/link_scrapping_report.txt', "w") as f:
        f.write(report_string)

def scrap_issue_links():
    with sync_playwright() as playwright:
        results_directory_open = './scrapper_results/open_issues'
        link_open = "https://github.com/pytorch/pytorch/issues?q=is%3Aopen+is%3Aissue" # link to open issues

        results_directory_closed = './scrapper_results/closed_issues'
        link_closed = "https://github.com/pytorch/pytorch/issues?q=is%3Aissue+is%3Aclosed" # link to closed issues

        test_link = "https://github.com/pytorch/pytorch/issues?page=495&q=is%3Aissue+is%3Aopen"
        test_directory = "./scrapper_results/test_results"

        # scrap_link(test_link, test_directory, playwright, 0, False)

        scrap_link(link_open, results_directory_open, playwright, 2)
        scrap_link(link_closed, results_directory_closed, playwright, 2)
    return 

if __name__ == "__main__":
    scrap_issue_links()

    open_issues_links = "./scrapper_results/open_issues/links.csv"
    closed_issues_links = "./scrapper_results/closed_issues/links.csv"
    test_issues_links = "./scrapper_results/test_results/links.csv"

    print("scrapping open issues")
    open_issues_contents = scrap_issue_content.scrap_issues_content(open_issues_links, result_directory="./scrapper_results/open_issues", maximum_wait_time=0)

    print("scrapping closed issues")
    closed_issues_contents = scrap_issue_content.scrap_issues_content(closed_issues_links, result_directory="./scrapper_results/closed_issues", maximum_wait_time=0)
    

