REPO = 'facebook/react'

#GitHub read-only access token will expire 15 October 2023
GITHUB_TOKEN = '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'

from requests import get
from time import sleep
import json

endpoint = 'https://api.github.com/repos/' + REPO + '/issues'
#docs at https://docs.github.com/en/rest/issues/issues#list-repository-issues

headers = {'Authorization': 'Bearer ' + GITHUB_TOKEN,
           'Accept': 'application/vnd.github+json',
           'X-GitHub-Api-Version': '2022-11-28'}

if 'issues' not in globals():
  issues = []  # array

def load_issues(page=1):  #load from given page number or from the beginning if not specified

  while True:  #each page has 30 issues by default

    print('*** LOADING PAGE', page)

    response = get(endpoint, headers=headers,
                  params={'page': page, 'state': 'all'})  # ~12,300 open and closed
    if response.status_code in [422, 403]:  # rate limited
      print('!!! WARNING: rate limited (5000 requests per hour?) sleepiing a minute')
      sleep(60)  # back off after hitting rate limits; actually takes much longer
      continue

    gh_issues = response.json()
    if not gh_issues:
      break  # no more pages

    if response.status_code != 200:
      print('!!! BAD RESPONSE STATUS CODE:', response.status_code)
      break

    for ghiss in gh_issues:
      issue = {}
      comments = []

      issue['number'] = int(ghiss['url'].split('/')[-1])
      issue['title'] = ghiss['title']
      issue['state'] = ghiss['state']

      issue['labels'] = [label['name']
                              for label in ghiss['labels']]  # array of strings

      if ghiss['body']:  # occasionally None
        issue['body'] = ghiss['body']

      if int(ghiss['comments']):
        for attempt in range(20):  # try 20 times just in case
          ghcomments = get(ghiss['comments_url'], headers=headers)
          if response.status_code in [422, 403]:  # rate limited
            print('!!! WARNING: rate limited (5000 requests per hour?) sleeping a minute')
            sleep(60)  # back off after hitting rate limits
            continue
          else:
            break
          if attempt == 19:
            raise RuntimeError("Too many retires, timed out")
        for comment in ghcomments.json():
          if isinstance(comment, dict) and 'body' in comment:  # cant remember why but needed
            comments.append(comment['body'])
        issue['comments'] = comments

      issues.append(issue)

    #Go to the next page
    page += 1

#load_issues(page=253) ###got 7569 issues before being rate limited by GitHub

print(len(issues))
print(len(json.dumps(issues, indent=2)))
