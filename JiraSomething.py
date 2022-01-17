import json
import pandas  # pip install pandas
import requests

# Username: ReportUser
# Password: Welcome#1#Htrk
def get_issue_data(issue_key, auth: tuple = ("ReportUser", "Welcome#1#Htrk")):
    # get the issue from the API and store it's fields as a python dictionary
    url = f"http://atlprd:8080/jira/rest/api/latest/issue/{issue_key}"
    request = requests.get(url=url, auth=auth)
    issue_fields = json.loads(request.text)['fields']
    print(json.dumps(issue_fields, indent=2))
    # get the desired field values
    results = dict()
    results['Summary'] = f"\n{issue_key} : {issue_fields['summary']}\n\n"
    results['Priority'] = issue_fields['priority'].get("name")
    #if isinstance(issue_fields['fixVersions'], list):
    #    results['Fix Version'] = issue_fields['fixVersions'][0].get("name")
    #else:
    #    results['Fix Version'] = issue_fields['fixVersions'].get("name")
    results['Link'] = f"\nhttp://atlprd:8080/jira/browse/{issue_key}\n\n"
    results['Description'] = issue_fields['description']
    results['Comments'] = "\n".join(
        [f"{comment['created']} - {comment['body']}\n" for comment in issue_fields['comment']['comments']]
    )
    return results

# get the requested fields/values and store them in a dictionary
jira_issue_number = input("Enter the jira issue number: ")  # TODO: change to desired jira ticket
my_values = get_issue_data(jira_issue_number)
# for key, value in my_values.items():
#     print(f"{key}: {value}")
# write to an excel spreadsheet
df = pandas.DataFrame([list(my_values.keys()), list(my_values.values())])
df.to_excel("output.xlsx", sheet_name=jira_issue_number)
# write it to a csv file (the "separator" in this case is "<|%|>")
with open("my_flat_file.txt", "w") as ff:
    headers = "<|%|>".join(list(my_values.keys()))
    values = "<|%|>".join(list(my_values.values()))
    ff.write(f"{headers}\n")
    ff.write(f"{values}\n")