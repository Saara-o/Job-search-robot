from robocorp import browser
from RPA.Excel.Files import Files

import json

# Get json data(keywords, locations)
with open("search_criteria.json", "r", encoding="utf-8") as f:
    data = json.load(f)

keywordlist = data["keywords"]
locationslist = data["location"]

######################################
# Exportable function to tasks.py
def getDataFromTyomarkkinatori():
  openTyomarkkinatori()
  blockCookies()
  dataSet = []
  for keyword in keywordlist:
    makeSearch(keyword)
    selectLocation(locationslist)
    dataSet.append(collectCardsData())
    openTyomarkkinatori()
    
  upendCardsDataToExcel(dataSet)
#######################################


# Open Työmarkkinatori's homepage
def openTyomarkkinatori():
  browser.goto("https://tyomarkkinatori.fi/henkiloasiakkaat")

# Declie the cookies pop up
def blockCookies():
  page = browser.page()
  page.wait_for_timeout(500)
  page.locator("#CybotCookiebotDialogBodyButtonDecline").click()

# Fill search bar with given keyword and submit(search)
def makeSearch(keyword):
  page = browser.page()
  form = page.locator("form[action='/henkiloasiakkaat/avoimet-tyopaikat']")
  form.locator("#simpleForm-jobSearch").fill(keyword)
  form.locator("button[type='submit']").click()

# Add given location criteria
def selectLocation(locationList):
  page = browser.page()
  kentta = page.get_by_role("combobox", name="Sijainti")

  for location in locationList:
    page.wait_for_timeout(1000)
    kentta.fill(location)
    kentta.press("Enter")
    kentta.fill("")

# Collect job posts from the site
def collectCardsData():
  page = browser.page()
  cards = page.locator("#tmt-haku-search-results-scroll-anchor > div").all()

  jobs = []
  # Cycle trough all job posts (cards)
  for card in cards[1:-1]: # skip first and last row (they are't job posts)
    # Collect job post's info
    a = card.locator("a[href]").first
    texts = card.locator("span").all_inner_texts()

    title = a.inner_text()
    company = texts[0]
    location = texts[1]
    url = a.evaluate("el => el.href")
    jobPortal = "Työmarkkinatori"

    # Append job post info to "jobs" list as a list
    jobs.append([title, company, location, url, jobPortal])
  print(jobs)
  return jobs

# Create excel file and fill it with job posts information
def upendCardsDataToExcel(dataSet):
  excel = Files()
  excel.create_workbook("./output/Jobs.xlsx")

  for oneKeyword in dataSet:
    for workPlace in oneKeyword:
      emptyRow = excel.find_empty_row()
      column = 1
      for value in workPlace:
        excel.set_worksheet_value(emptyRow, column, value)
        column += 1

  excel.save_workbook()
  excel.close_workbook()

