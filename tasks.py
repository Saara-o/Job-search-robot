from robocorp.tasks import task
from robocorp import browser

from jiro import getDataFromTyomarkkinatori

"""@task
def job_search_robot():
    with open("config.json", encoding="utf-8") as f:
        config = json.load(f)
    print("Config loaded:", config)"""

@task
def jiro_test():
  slowmo=3000
  getDataFromTyomarkkinatori()