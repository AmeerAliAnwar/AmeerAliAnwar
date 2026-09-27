import urllib.request
import json
import os

def fetch_data():
    headers = {"User-Agent": "Mozilla/5.0"}
    
    # 1. User info
    req_user = urllib.request.Request("https://api.github.com/users/AmeerAliAnwar", headers=headers)
    user_info = {}
    try:
        with urllib.request.urlopen(req_user) as resp:
            user_info = json.loads(resp.read().decode())
    except Exception as e:
        print("User fetch error:", e)
        
    # 2. Repos
    req_repos = urllib.request.Request("https://api.github.com/users/AmeerAliAnwar/repos?per_page=100&sort=updated", headers=headers)
    repos = []
    try:
        with urllib.request.urlopen(req_repos) as resp:
            repos = json.loads(resp.read().decode())
    except Exception as e:
        print("Repos fetch error:", e)

    # 3. Merged PRs
    req_prs = urllib.request.Request("https://api.github.com/search/issues?q=author:AmeerAliAnwar+type:pr+is:merged&sort=updated&order=desc", headers=headers)
    prs = []
    try:
        with urllib.request.urlopen(req_prs) as resp:
            prs_data = json.loads(resp.read().decode())
            prs = prs_data.get("items", [])
    except Exception as e:
        print("PRs fetch error:", e)

    print(f"User: {user_info.get('login')} (Public repos: {user_info.get('public_repos')}, Followers: {user_info.get('followers')})")
    print("\nPublic Repositories:")
    for r in repos:
        desc = r.get("description") or "No description"
        print(f"- {r.get('name')}: {desc} | Lang: {r.get('language')} | Stars: {r.get('stargazers_count')} | Forks: {r.get('forks_count')}")

    print(f"\nMerged PRs ({len(prs)} total):")
    for p in prs[:10]:
        repo = p.get("repository_url", "").split("/repos/")[-1]
        print(f"- {repo}#{p.get('number')}: {p.get('title')}")

if __name__ == "__main__":
    fetch_data()
