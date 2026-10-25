import json
from urllib.parse import urlencode

from robocorp import browser
from RPA.Excel.Files import Files

SITE = "Duunitori"
SEARCH_URL = "https://duunitori.fi/tyopaikat"
PAGES_PER_SEARCH = 2  # Duunitori shows 20 jobs per page


def load_criteria(file_name="search_criteria.json"):
    """Read the search settings from the JSON file."""
    with open(file_name, encoding="utf-8") as file:
        return json.load(file)


def search_duunitori(criteria):
    """Search every keyword and return found jobs as list."""
    found_jobs = []
    seen_links = set()  # skip the same job if it is found again

    for keyword in criteria["keywords"]:
        for page_number in range(1, PAGES_PER_SEARCH + 1):
            go_to_results(keyword, criteria, page_number)
            reject_extra_cookies()

            for job in read_job_cards():
                if job["URL"] not in seen_links:
                    seen_links.add(job["URL"])
                    found_jobs.append(job)

            if not next_page_exists(page_number):
                break

    print(f"{SITE}: {len(found_jobs)} different jobs found")
    return found_jobs


def go_to_results(keyword, criteria, page_number):
    """Open the result page, all locations are searched, separated with ';'."""
    settings = {
        "haku": keyword,
        "alue": ";".join(criteria["location"]).lower(),
    }
    if criteria.get("job_type") == "full-time":
        settings["filter_work_type"] = "full_time"
    if page_number > 1:
        settings["sivu"] = page_number

    browser.goto(SEARCH_URL + "?" + urlencode(settings, safe=";"))


def reject_extra_cookies():
    """Keep only the necessary cookies. Banner is shown only on the first visit."""
    page = browser.page()
    manage_link = page.get_by_text("Hallitse evästeitä")
    if manage_link.is_visible():
        manage_link.click()
        page.get_by_role("button", name="Tallenna evästevalinnat").click()


def read_job_cards():
    """Read title, company, location and link from every job card on the page."""
    page = browser.page()
    jobs = []

    for link in page.locator("a.job-box__hover.gtm-search-result").all():
        card = link.locator("..")  # The card around the link
        place = card.locator(".job-box__job-location").inner_text()

        jobs.append({
            "Title": link.text_content().strip(),
            "Company": link.get_attribute("data-company"),
            "Location": place.replace("–", "").strip(),
            "URL": "https://duunitori.fi" + link.get_attribute("href"),
            "Job portal": SITE,
        })

    return jobs


def next_page_exists(page_number):
    """True if the page has link to the next result page."""
    next_link = browser.page().locator(f"a.pagination__pagenum[href*='sivu={page_number + 1}']")
    return next_link.count() > 0


def saveToExcel(dataSet, path="./output/Duunitori.xlsx"):
    rows = [job for search in dataSet for job in search]

    excel = Files()
    excel.create_workbook(path)
    excel.append_rows_to_worksheet(
        [["Title", "Company", "Location", "URL", "Job portal"]] + rows
    )

    excel.save_workbook()
    excel.close_workbook()