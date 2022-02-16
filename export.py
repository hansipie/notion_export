import requests
import yaml

class MyExport:

    def __init__(self):
        """
        Gets required variable data from config yaml file.
        """
        with open("my_variable.yml", 'r') as stream:
            try:
                self.my_variables_map = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print("[Error]: while reading yml file", exc)
            self.my_variables_map["NOTION_ENTRIES"] = {}
            self.getTaskId()

    def getTaskId(self):
        url = "https://www.notion.so/api/v3/enqueueTask"
        headers = {
            'Cookie': 'token2=' + self.my_variables_map["MY_NOTION_INTERNAL_TOKEN" + '; ']
        }
        body = {}
        response = requests.post(url, headers=headers, json=body)
        self.my_variables_map["TASK_ID"] = response.json()["taskId"]                



if __name__ == "__main__":
    MyExport().UpdateIndefinitely()
