import requests
import os

token = os.environ['GH_TOKEN']
owner = os.environ['REPO_OWNER']
repo = os.environ['REPO_NAME']

headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

def get_runs():
    runs = []
    page = 1
    while True:
        url = f'https://api.github.com/repos/{owner}/{repo}/actions/runs?page={page}&per_page=100'
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            print(f"Hata: {r.status_code} — {r.text}")
            break
        data = r.json()
        if not data.get('workflow_runs'):
            break
        runs.extend(data['workflow_runs'])
        page += 1
    return runs

def delete_run(run_id):
    url = f'https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}'
    r = requests.delete(url, headers=headers)
    if r.status_code == 204:
        print(f"✅ Silindi: {run_id}")
    else:
        print(f"❌ Silinemedi: {run_id} — {r.status_code} — {r.text}")

runs = get_runs()
print(f"{len(runs)} adet run bulundu.")
for run in runs:
    delete_run(run['id'])
