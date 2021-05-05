def indeedScraper(searchTerm, searchLocation):
    #Get first
    r = requests.get("https://indeed.com/q-" + searchTerm + "-l-" + searchLocation + "-jobs.html")
    jobCounter = 0

    y = r.text

    #Total Pages
    beginLen = y.find("Page 1 of", 1, len(y))

    if beginLen == -1:
        totalPages = -1
    else:
        totalPages = y[beginLen + 10:y.find("jobs", beginLen, len(y)) - 1]

    #Bad HTML pull, no data found
    if totalPages == -1:
        print("Bad search. Try again.")
        return
    else:
        if totalPages.find(",", 1, len(y)):
            pages = totalPages.replace(",", "")
        pages = int(pages)

    pageCounter = 0
    looper = True

    while pageCounter < pages:
        while looper:
            # Look for title and company in HTML to ensure there is a posting listed
            titlePos = y.find('<div class="title', 1, len(y))
            companyPos = y.find('<span class="company', titlePos, len(y))

            # Found that there is a job title and company in the remaining HTML text
            if titlePos > -1 and companyPos > -1:
                jobTitle = y[y.find("title=", titlePos + 20, len(y)) + 7:y.find("class=", titlePos + 20, len(y)) - 2]
                jobTitle = jobTitle.replace("&amp;", "&")
                if y.find("href=", companyPos, companyPos + 250) > -1:
                    jobCompany = y[y.find("href=", companyPos, len(y)) + 11:y.find("onmousedown", companyPos,len(y)) - 18]
                else:
                    jobCompany = y[y.find(">", companyPos, len(y)) + 3:y.find("<", companyPos + 2, len(y))]

                jobLink = "https://www.indeed.com/" + y[y.find("href=", titlePos, len(y)) + 7:y.find("onmousedown", titlePos, len(y)) - 18]

                # Insert into array
                if jobTitle.find(",", 1, len(jobTitle)):
                    jobTitle = jobTitle.replace(",", ":")
                if jobCompany.find(",", 1, len(jobCompany)):
                    jobCompany = jobCompany.replace(",", ":")

                x.insert(jobCounter, [jobTitle, jobCompany, jobLink, (jobTitle + jobCompany)])

                jobCounter = jobCounter + 1
                y = y[companyPos:len(y)]
            else:
                looper = False

        #Get next page
        pageCounter = pageCounter + 10
        r = requests.get("https://www.indeed.com/jobs?q=" + searchTerm + "&l=" + searchLocation + "&start=" + str(pageCounter))
        y = r.text
        looper = True
        
        
#TODO Add the rest, will do so soon
