from robocorp.tasks import task
from robocorp import browser

from RPA.Email.ImapSmtp import ImapSmtp
from dotenv import load_dotenv 
import os
import json

from jiro import getDataFromTyomarkkinatori
from saara import getDataFromJobly, saveToExcel
from atte import search_duunitori, saveToExcel

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

@task
def atte_test():
    browser.configure(headless=False, slowmo = 500)
    data = search_duunitori()
    saveToExcel(data)


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