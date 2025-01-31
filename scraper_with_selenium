import os
import time
import random

#Check for required packages, if not, install them
try:
    from selenium.webdriver import Firefox
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.common.by import By
    import pandas as pd
except ImportError:
    print("Missing packages, installing them.")
    os.system('pip install selenium')
    os.system('pip install pandas')
    from selenium.webdriver import Firefox
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.common.by import By
    import pandas as pd

#Get the headlines from the pages
def scrape_page(page_num, html):
    dfToAppend = [[]]
    x = 0
    while x > -1:
        x = html.find('vue-archives-item--headline')
        if x > -1:
            html = html[x+38:]
            page_url = html[:html.find('>')-1]
            html = html[html.find('>')+1:]
            title = html[0:html.find('<')]
            dfToAppend.append([page_num, title, ('https://a_site.com' + page_url)])
    dfToAppend.pop(0)
    dfToAppend.pop(len(dfToAppend)-1)
    return dfToAppend


if __name__ == "__main__":
    # Check that firefox (geckodriver.exe) is available
    if "geckodriver.exe" in os.listdir(os.getcwd()):
        print("Good to go, proceeding.")
    else:
        print("Missing Firefox driver, get geckodriver.exe")
        exit()

    pagesToLoop = int(input("Enter the number of pages you would like to scrape: "))

    #Setup Pandas DF
    df = pd.DataFrame(columns=["PageNum", "Article Title", "Article URL"])

    #Set up the Firefox driver
    opts = Options()
    opts.headless = True
    browser = Firefox(options=opts)

    #Open the URL for the first time
    url = 'https://a_site.com/archives'

    browser.get(url)
    print("Opened URL.")
    pageNum = 1

    while pageNum <= pagesToLoop:
        # Make sure the page loads
        randNum = random.randint(2, 3)
        time.sleep(randNum)

        print("Getting headlines for page: " + str(pageNum))
        appendDf = scrape_page(pageNum, browser.page_source)
        df2 = pd.DataFrame(data=appendDf, columns=["PageNum", "Article Title", "Article URL"])
        df = pd.concat([df, df2], ignore_index=True)

        pageNum += 1

        if pageNum <= pagesToLoop:
            #Check for correct button
            next_page = browser.find_elements(By.CLASS_NAME, 'page-button-clickable')
            for i in next_page:
                if int(i.accessible_name) == pageNum:
                    i.click()
                    break

            #Make sure the page loads
            randNum = random.randint(2, 3)
            time.sleep(randNum)

    export_csv = df.to_csv("a_site_scrape.csv", index=None, header=True)
    browser.close()
