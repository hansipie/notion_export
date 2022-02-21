import math
import os
import shutil
import tempfile
import time
import zipfile
import requests
import json
import yaml

def EnqueueTask(id, token):
    url = "https://www.notion.so/api/v3/enqueueTask"
    payload = json.dumps({
        "task": {
            "eventName": "exportBlock",
            "request": {
            "block": {
                "id": id
            },
            "recursive": False,
            "exportOptions": {
                "exportType": "markdown",
                "timeZone": "Europe/Paris",
                "locale": "en"
            }
            }
        }
    })
    headers = {
    'Cookie': 'token_v2=' +  token,
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    resp = response.json()
    return(resp["taskId"])

def GetTasks(taskid, token):
    url = "https://www.notion.so/api/v3/getTasks"
    payload = json.dumps({
    "taskIds": [
        taskid
    ]
    })
    headers = {
    'Cookie': 'token_v2=' + token,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    
    return(response.json())

def DownloadArchive(url, dest):
    print("Download url: " + url)
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    destfile = os.path.join(dest,"archive.zip")
    with open(destfile, "wb") as f:
        f.write(response.content)
    return(destfile)

with open("my_variables.yml", 'r') as stream:
    try:
        my_variables_map = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print("[Error]: while reading yml file", exc)

taskid=EnqueueTask(my_variables_map["DATABASE_ID"], my_variables_map["MY_NOTION_INTERNAL_TOKEN"])

mytime = str(math.floor(time.time()))
destpath = os.path.join("files", mytime)
temppath = tempfile.mkdtemp()
loop = 1
while (loop == 1):
    resp = GetTasks(taskid, my_variables_map["MY_NOTION_INTERNAL_TOKEN"])
    for v in resp["results"]:
        print("state: " + v["state"])
        if (v["state"] == "success"):
            if (v["status"]["type"] == "complete"):
                print("status: " + v["status"]["type"])
                archive = DownloadArchive(v["status"]["exportURL"], temppath)
                with zipfile.ZipFile(archive, 'r') as zip_ref:
                    zip_ref.extractall(destpath)
                loop = 0
                break
        print("retry")

shutil.rmtree(temppath)
print("Done")

