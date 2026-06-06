import requests

USERNAME = "sameer1012"

URL = "https://leetcode.com/graphql"


def get_recent_submissions():

    query = """
    query getRecentSubmissions($username: String!) {
      recentAcSubmissionList(username: $username) {
        title
        titleSlug
        timestamp
      }
    }
    """

    response = requests.post(
        URL,
        json={
            "query": query,
            "variables": {
                "username": USERNAME
            }
        }
    )

    data = response.json()

    return data["data"]["recentAcSubmissionList"]