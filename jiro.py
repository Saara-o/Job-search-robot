from robocorp import browser
from RPA.Excel.Files import Files

import json

with open("search_criteria.json", "r", encoding="utf-8") as f:
    data = json.load(f)

keywordlist = data["keywords"]
locationslist = data["location"]


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




def openTyomarkkinatori():
  browser.goto("https://tyomarkkinatori.fi/henkiloasiakkaat")

def blockCookies():
  page = browser.page()
  page.wait_for_timeout(500)
  page.locator("#CybotCookiebotDialogBodyButtonDecline").click()

def makeSearch(keyword):
  page = browser.page()
  form = page.locator("form[action='/henkiloasiakkaat/avoimet-tyopaikat']")
  form.locator("#simpleForm-jobSearch").fill(keyword)
  form.locator("button[type='submit']").click()

def selectLocation(locationList):
  page = browser.page()
  kentta = page.get_by_role("combobox", name="Sijainti")

  for location in locationList:
    page.wait_for_timeout(1000)
    kentta.fill(location)
    kentta.press("Enter")
    kentta.fill("")


def collectCardsData():
  page = browser.page()
  cards = page.locator("#tmt-haku-search-results-scroll-anchor > div").all()

  jobs = []
  for card in cards[1:-1]:
    a = card.locator("a[href]").first
    title = a.inner_text()
    texts = card.locator("span").all_inner_texts()

    title = a.inner_text()
    company = texts[0]
    location = texts[1]
    url = a.evaluate("el => el.href")
    jobPortal = "Työmarkkinatori"

    jobs.append([title, company, location, url, jobPortal])
  print(jobs)
  return jobs

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

