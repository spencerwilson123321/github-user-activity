import argparse
import requests
import json


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("username")
    args = parser.parse_args()
    base_url = f"https://api.github.com/users/{args.username}/events"
    response = requests.get(base_url)
    response.raise_for_status()
    events = response.json()
    for event in events:
        repository_name = event["repo"]["name"]
        if event["type"] == "CreateEvent":
            thing_created = event["payload"]["ref_type"]
            print(f"Created {thing_created} {'on' if thing_created in ('branch', 'tag') else 'named'} {repository_name}")
        elif event["type"] == "DeleteEvent":
            thing_deleted = event["payload"]["ref_type"]
            print(f"Deleted {thing_deleted} on {repository_name}")
        elif event["type"] == "PushEvent":
            num_commits = event["payload"]["size"]
            plural = 's' if num_commits > 1 else ''
            print(f"Pushed {num_commits} commit{plural} to {repository_name}")


