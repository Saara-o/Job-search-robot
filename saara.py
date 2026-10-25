from robocorp import browser
from RPA.Excel.Files import Files
from urllib.parse import quote_plus
import json

with open("search_criteria.json", "r", encoding ="utf-8") as f:
    data = json.load(f)

keywordlist = data["keywords"]
locationslist = data["location"]

def getDataFromJobly():
    dataSet = []
    for keyword in keywordlist:
        for location in locationslist:
            openJobly(keyword, location)
            blockCookies()
            dataSet.append(collectData())
    return dataSet

"""Navigate to the given URL, URL changes according to given keywords and location """
def openJobly(keyword, location):
    url = (
        "https://www.jobly.fi/tyopaikat"
        f"?search={quote_plus(keyword)}"
        f"&job_geo_location={quote_plus(location + ', Suomi')}"
    )

    page = browser.page()
    page.goto(url, wait_until="domcontentloaded", timeout = 15000)

"""Clicks on cookie banner only necessary cookies"""
def blockCookies():
    page = browser.page()

    page.wait_for_timeout(1000)
    for frame in page.frames:
        btn = frame.locator("button[title= 'Vain välttämättömät']")
        if btn.count() > 0:
            btn.first.click()
            return
    print("Cookie banner not found.")

"""Collects searched job listings: job title, company, location, link to the job listing, and site where the listing is from"""
def collectData():
    page = browser.page()
    cards = page.locator("article.node-job").all()

    jobs = []
    for card in cards:
        a = card.locator("h2.node__title a").first
        title = a.inner_text().strip()
        url = a.evaluate("el => el.href")
        jobPortal = "Jobly"
        company = card.locator(".recruiter-company-profile-job-organization").first.inner_text().strip()
        location = card.locator(".location span").first.inner_text().strip()
        jobs.append([title, company, location, url, jobPortal])

    print(jobs)
    return jobs

"""Save the data into excel file"""
def saveToExcel(dataSet, path="./output/Jobly.xlsx"):
    rows = [job for search in dataSet for job in search]

    excel = Files()
    excel.create_workbook(path)
    excel.append_rows_to_worksheet(
        [["Title", "Company", "Location", "URL", "Job portal"]] + rows
    )

    excel.save_workbook()
    excel.close_workbook()