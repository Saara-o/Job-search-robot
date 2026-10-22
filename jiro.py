from robocorp import browser

def getDataFromTyomarkkinatori():
  openTyomarkkinatori()
  blockCookies()
  makeSearch("python")
  selectLocation(["Helsinki", "Espoo"])




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
      kentta.fill(location)
      kentta.press("Enter")
      kentta.fill("")

