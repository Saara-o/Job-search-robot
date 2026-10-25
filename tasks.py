from robocorp.tasks import task
from robocorp import browser
from RPA.Excel.Files import Files


from RPA.Email.ImapSmtp import ImapSmtp
import os
import json

try:
    from dotenv import load_dotenv
except importError:
    def load_dotenv(*args, **kwargs):
        return False

from jiro import getDataFromTyomarkkinatori
from saara import getDataFromJobly
from atte import load_criteria, search_duunitori

OUTPUT_FILE = "output/Jobs.xlsx"
COLUMNS = ["Title", "Company", "Location", "URL", "Job Portal"]

def rows_to_dicts(data_set):
    """Jiro and Saara return lists ->> dicts"""
    jobs = []
    for search in data_set:
        for row in search:
            jobs.attend(dict(zip(COLUMNS, row)))
        return jobs

def remove_duplicates(jobs):
    """Remove duplicates by URL, and by title + company + location."""
    seen_urls = set()
    seen_keys = set()
    unique = []
    for job in jobs:
        url = (job.get("URL") or "").split("?")[0].strip().lower()
        key = tuple((job.get(c) or "").strip().lower() for c in ("Title", "Company", "Location"))
        if (url and url in seen_urls) or key in seen_keys:
            continue
        seen_urls.add(url)
        seen_keys.add(key)
        unique.append(job)
    return unique

def write_excel(jobs, path=OUTPUT_FILE):
    """Write all unique jobs to one Excel file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    rows = [{c: job.get(c, "") for c in COLUMNS} for job in jobs]
    excel = Files()
    excel.create_workbook(path, sheet_name="Jobs")
    excel.append_rows_to_worksheet(rows, header=True)
    excel.save_workbook()
    excel.close_workbook()
 
 
def send_excel_by_email(recipient, summary, path=OUTPUT_FILE):
    """Send the Excel file and the run summary to the user."""
    mail = ImapSmtp(smtp_server="smtp.gmail.com", smtp_port=587)
    mail.authorize_smtp(
        account=os.environ["EMAIL_ACCOUNT"],
        password=os.environ["EMAIL_PASSWORD"],
    )
    mail.send_message(
        sender=os.environ["EMAIL_ACCOUNT"],
        recipients=recipient,
        subject="Job listings",
        body=f"Hi,\n\nThe job listings file is attached.\n\n{summary}",
        attachments=path,
    )

@task
def job_search_robot():
    load_dotenv()
    criteria = load_criteria()

    browser.configure(headless=False, slowmo = 500)

    all_jobs = []
    sites_ok = 0
    failed_sites = []

    sites = [
        ("Työmarkkinatori", lambda: rows_to_dicts(getDataFromTyomarkkinatori())),
        ("Jobly", lambda: rows_to_dicts(getDataFromJobly())),
        ("Duunitori", lambda: search_duunitori(criteria)),
    ]
    
    """One portal failing does not stop the others"""
    for name, run in sites:
        try:
            jobs = run()
            all_jobs.extend(jobs)
            sites_ok += 1
            print(f"{name}: {len(jobs)} listings collected")
        except Exception as error:
            failed_sites.append(name)
            print(f"ERROR: {name} failed: {error}")


    unique_jobs = remove_duplicates(all_jobs)
    print(f"Total {len(all_jobs)} listings, {len(unique_jobs)} unique")

    if not unique_jobs:
        print("HELP NEEDED: no listings found from any site.")
        return

    write_excel(unique_jobs)


"""@task
def job_search_robot():
    with open("config.json", encoding="utf-8") as f:
        config = json.load(f)
    print("Config loaded:", config)"""

"""@task
def jiro_test():
  slowmo=3000
  getDataFromTyomarkkinatori()

  load_dotenv()
  recipient = getEmailRecipient()
  send_excel_by_email(recipient)"""

"""@task
def saara_test():
    browser.configure(headless=False, slowmo = 500)
    data = getDataFromJobly()
    saveToExcel(data)
"""

"""@task
def atte_test():
    browser.configure(headless=False, slowmo = 500)
    criteria = load_criteria()
    data = search_duunitori(criteria)
    write_excel(data)
"""

####################################################################
"""
def getEmailRecipient():
    with open("search_criteria.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        return data["email_recipient"]

def send_excel_by_email(recipient, filename="./output/Jobs.xlsx"):
    mail = ImapSmtp(smtp_server="smtp.gmail.com", smtp_port=587)
    mail.authorize_smtp(
        account=os.environ["EMAIL_ACCOUNT"],
        password=os.environ["EMAIL_PASSWORD"],
    )
    mail.send_message(
        sender=os.environ["EMAIL_ACCOUNT"],
        recipients=recipient,
        subject="Työpaikat",
        body="Hei,\n\nliitteenä uusimmat työpaikat.",
        attachments=filename,
    )
"""