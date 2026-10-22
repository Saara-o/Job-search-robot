ort json
from robocorp.tasks import task
from robocorp import browser

@task
def job_search_robot():
    with open("config.json", encoding="utf-8") as f:
        config = json.load(f)
    print("Config loaded:", config)
