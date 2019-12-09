from tkinter import *
from tkinter import messagebox

import requests
import time
import pandas as pd
import os

#TODO: Loading bar would be nice...

#Setup root tkinter
root = Tk()
root.title("Job Scraper")

#vars
indSelect, glasSelect, linkSelect = BooleanVar(), BooleanVar(), BooleanVar()
saveLocation, searchTerm, searchLocation = StringVar(), StringVar(), StringVar()
x = [[]]

#Scraper functions
# noinspection PyPep8Naming
def indeedScraper():
    #Get first
    r = requests.get("https://indeed.com/q-" + searchTerm.get() + "-l-" + searchLocation.get() + "-jobs.html")
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
        messagebox.showinfo("Bad search: Indeed", "No results were found for the search term/search location on Indeed.")
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
                if (jobTitle.find(",", 1, len(jobTitle))):
                    jobTitle = jobTitle.replace(",", ":")
                if (jobCompany.find(",", 1, len(jobCompany))):
                    jobCompany = jobCompany.replace(",", ":")

                x.insert(jobCounter, [jobTitle, jobCompany, jobLink, (jobTitle + jobCompany)])

                jobCounter = jobCounter + 1
                y = y[companyPos:len(y)]
            else:
                looper = False

        #Get next page
        pageCounter = pageCounter + 10
        r = requests.get("https://www.indeed.com/jobs?q=" + searchTerm.get() + "&l=" + searchLocation.get() + "&start=" + str(pageCounter))
        y = r.text
        looper = True

#TODO: Contiue further reserach, use of location ID blocks getting location properly, search term works
def glassdoorScraper():
    print("Currently not working")

#TODO: Continue further research, results obfuscated AF like jfc is this even possible
def linkedScraper():
    #Get first
    r = requests.get("https://www.linkedin.com/jobs/search/?keywords=" + searchTerm.get() + "&" + searchLocation.get())
    jobCounter = 0
    y = r.text

    #beginLen = y.find('<div class="t-12 t-black--light t-normal">',1,len(y))

    #if beginLen == -1:
    #    print("Bad search. Try again.")
    #    messagebox.showinfo("Bad search: Indeed", "No results were found for the search term/search location on Indeed.")
    #    return
    #else:
    #    totalResults = y[beginLen:y.find("</div>",beginLen,len(y))-1]


#Button function
def getChecked():
    if saveLocation.get() == "":
        messagebox.showinfo("No Save Location","No save location was enter for saving the CSV file.")
    elif searchTerm.get() == "":
        messagebox.showinfo("No Search Term","Please enter a term to search.  This is general a title or keyword.")
    elif searchLocation.get() == "":
        messagebox.showinfo("No Save Location","Please enter a location to search.")
    else:
        #Clean spaces
        if searchLocation.get().find(" ",1,len(searchLocation.get())):
            searchLocation.set(searchLocation.get().replace(" ","%20"))
        if searchTerm.get().find(" ", 1, len(searchTerm.get())):
            searchTerm.set(searchTerm.get().replace(" ", "%20"))
        #Add \ if needed
        if saveLocation.get()[len(saveLocation.get())-1] != "\\":
            saveLocation.set(saveLocation.get() + "\\")
            if os.path.isdir(saveLocation.get()) == False:
                print("Path entered does not exist.")
                exit()

        if indSelect.get():
            indeedScraper()
        if glasSelect.get():
            glassdoorScraper()
        if linkSelect.get():
            linkedScraper()

        #Pandas dataframe
        df = pd.DataFrame(x)
        df.columns = ["Title","Company","Link","DupeDrop"]

        #Get those dupes out of there
        df = df.drop_duplicates(subset="Link",keep="first",inplace=False)
        df = df.drop_duplicates(subset="DupeDrop",keep="first",inplace=False)
        df = df.drop(["DupeDrop"],axis=1)

        #Export to CSV
        export_csv = df.to_csv(saveLocation.get()+"JobScrape.csv",index=None,header=True)
        messagebox.showinfo("CSV Saved", "CSV file saved at " + saveLocation.get() +"!")


#Layout
Label(root, text="Which Job Sits To Scrape", font=("Calibri", 10)).grid(row=0, sticky=N)
Checkbutton(root, text="Indeed", variable=indSelect).grid(row=1, sticky=N)
Checkbutton(root, text="Glassdoor", variable=glasSelect, state=DISABLED).grid(row=2, sticky=N)
Checkbutton(root, text="LinkedIn", variable=linkSelect, state=DISABLED).grid(row=3, sticky=N)

Label(root, text="").grid(row=4, sticky=W)
Label(root, text="Location to save CSV file (example: C:\\users\\BobbyP\\Desktop\\)").grid(row=5, sticky=W, padx=75)
saveLocation.set(os.path.dirname(os.path.abspath(__file__)))    #Default value
Entry(root, width=50, textvariable=saveLocation).grid(row=6, sticky=W, padx=75)

Label(root, text="").grid(row=7, sticky=W)
Label(root, text="Search Term: ").grid(row=8, sticky=W, padx=75)
Entry(root, width=20, textvariable=searchTerm).grid(row=8)
Label(root, text="Search Location: ").grid(row=9, sticky=W, padx=75)
Entry(root, width=20, textvariable=searchLocation).grid(row=9)

Label(root, text="").grid(row=10, sticky=W)
Button(root, text="Scrape", command=getChecked, height=3, width=15).grid(row=11, sticky=W)
Button(root, text="Quit", command=root.quit, height=3, width=15).grid(row=11, sticky=E)

#Alawys Last
root.mainloop()
