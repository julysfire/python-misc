import os
import urllib.request

#Try to import libraries, if not, install them
try:
    import requests
    import pandas as pd
except ImportError:
    os.system('pip install pandas')
    os.system('pip install requests')
    import requests
    import pandas as pd
x = [[]]

def indeedScraper(searchTerm, searchLocation):
    # Get first
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    r = requests.get("https://indeed.com/q-" + searchTerm + "-l-" + searchLocation + "-jobs.html", headers=headers, proxies=urllib.request.getproxies())
    y = r.text

    #Variables
    jobCounter = 0
    totalCounter = 0
    pageCounter = 0
    looper = True

    # Total Pages
    beginLen = y.find("Page 1 of", 1, len(y))

    if beginLen == -1:
        print("Bad search. Try again.")
        return -1
    else:
        totalPages = y[beginLen + 10:y.find("jobs", beginLen, len(y)) - 1]
        if totalPages.find(",", 1, len(y)):
            pages = totalPages.replace(",", "")
        else:
            pages = totalPages

        pages = int(pages)

    #Cut down on text
    jobMapLoc = y.find("var jobmap = {};")
    y = y[jobMapLoc+18:y.find("</script>", jobMapLoc, len(y))]

    #Start main loop
    print("Total Pages: " + str(pages) + "\n")
    while pageCounter < pages:
        print("Current Page: " + str(pageCounter))
        while looper:

            #They have a nice array for us laid out in their Javascript :)
            if y.find("jobmap["+str(jobCounter)+"]") > -1:
                nextJobLoc = y.find("jobmap["+str(jobCounter+1)+"]")
                if nextJobLoc < 0:
                    nextJobLoc = len(y)

                jobLink = "https://www.indeed.com/viewjob?jk=" + y[y.find("{jk:", 0, nextJobLoc-1)+5:y.find(",efccid:", 0, nextJobLoc-1)-2]
                jobCompany = y[y.find("cmp:", 0, nextJobLoc-1)+5:y.find("cmpesc:", 0, nextJobLoc-1)-2]
                jobTitle = y[y.find("title:", 0, nextJobLoc-1)+7:y.find("locid:", 0, nextJobLoc-1)-2]
                jobTitle = jobTitle.replace("&amp;", '&')
                jobTitle = jobTitle.replace("\\/", "-")
                jobLoc = y[y.find("loc:", 0, nextJobLoc-1)+5:y.find("country:", 0, nextJobLoc-1)-2]

                x.insert(totalCounter, [jobTitle, jobCompany, jobLink, jobLoc])

                #Update text and county
                jobCounter += 1
                totalCounter += 1
                y = y[nextJobLoc:len(y)]
            else:
                looper = False

        # Get next page
        #Variables
        pageCounter = pageCounter + 10
        jobCounter = 0
        looper = True

        #New Text
        r = requests.get("https://www.indeed.com/jobs?q=" + searchTerm + "&l=" + searchLocation + "&start=" + str(pageCounter))
        y = r.text
        jobMapLoc = y.find("var jobmap = {};")
        y = y[jobMapLoc + 18:y.find("</script>", jobMapLoc, len(y))]


if __name__ == "__main__":
    searchtermIn = input("Please enter a term to search for: ")
    locationIn = input("Please enter a location to search for: ")

    #HTML Encoding, common codes
    htmlCodes = ((' ', "%20"), ("'", '%27'), ('"', "%22"), ('>', '%3F;'), ('<', '%3C;'), ('&', '%26;'), ("#", "%23"), ("!", "%21"), (":", "%3A",), (";", "%3B"))

    for codes in htmlCodes:
        searchtermIn = searchtermIn.replace(codes[0], codes[1])
        locationIn = locationIn.replace(codes[0], codes[1])

    #Get data
    if indeedScraper(searchtermIn, locationIn) != -1:
        df = pd.DataFrame(data=x, columns=["Job Title", "Hiring Company", "Job Link", "Job Location"])

        # Pandas
        pd.set_option("display.max_colwidth", -1)
        pd.set_option("display.max_rows", 999)
        print(df.to_string)

        # Export to CSV
        export_csv = df.to_csv(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + '\\IndeedJobs.csv', index=None, header=True)
