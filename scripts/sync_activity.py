import os
import re
import urllib.request
import json

def fetch_merged_prs(author):
    url = f"https://api.github.com/search/issues?q=author:{author}+type:pr+is:merged&sort=updated&order=desc&per_page=5"
    headers = {"User-Agent": "profile-updater"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        return data.get("items", [])
    except Exception as exc:
        print(f"Error fetching PRs: {exc}")
        return []

def main():
    prs = fetch_merged_prs("AmeerAliAnwar")
    if not prs:
        print("No PRs found or network error.")
        return

    lines = []
    for pr in prs:
        repo = pr["repository_url"].split("/repos/")[-1]
        title = pr["title"].replace("—", ":").replace("--", "-")
        lines.append(f"- [{repo}#{pr['number']}]({pr['html_url']}): {title}")

    pr_block = "\n".join(lines)
    
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"(<!-- PR_FEED_START -->)(.*?)(<!-- PR_FEED_END -->)"
    replacement = f"\\1\n{pr_block}\n\\3"
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated_content)

if __name__ == "__main__":
    main()
