import os
import json
from pathlib import Path

import pandas as pd  # makes manipulating the data easier
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from dotenv import load_dotenv

load_dotenv()

# Create a session that will automatically retry on server errors
s = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
s.mount("http://", HTTPAdapter(max_retries=retries))
s.mount("https://", HTTPAdapter(max_retries=retries))

API_KEY = os.getenv("TROVE_API_KEY")

def get_contrib_details(record, parent=None):
    records = []
    details = {
        "id": record["id"],
        "name": record["name"],
        "total": int(record["totalholdings"]),
        "parent": None,
    }
    if "nuc" in record:
        details["nuc"] = record["nuc"][0]
    else:
        details["nuc"] = None
    if parent:
        if not record["name"].startswith(parent["name"]):
            details["name"] = f"{parent['name']} {record['name']}"
        details["parent"] = parent["id"]
    records = [details]
    if "children" in record:
        record["name"] = details["name"]
        records += get_children(record)
    return records


def get_children(parent):
    children = []
    for child in parent["children"]["contributor"]:
        children += get_contrib_details(child, parent)
    return children


def get_contributors():
    contributors = []
    params = {"encoding": "json", "reclevel": "full", "key": API_KEY}
    response = s.get(
        "https://api.trove.nla.gov.au/v2/contributor", params=params
    )
    data = response.json()
    Path("data", "trove-contributors.json").write_text(json.dumps(data))
    for contrib in data["response"]["contributor"]:
        contributors += get_contrib_details(contrib)
    return contributors


def main():
    Path("data").mkdir(exist_ok=True)
    contributors = get_contributors()
    df = pd.DataFrame(contributors)
    print(df.shape)
    df[["id", "nuc", "name", "parent", "total"]].to_csv(Path("data", "trove-contributors.csv"), index=False)

if __name__ == "__main__":
    main()