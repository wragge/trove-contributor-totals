import os
from pathlib import Path
import time

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

def get_children(term):
    facets = []
    for child_term in term["term"]:
        facets += get_term(child_term)
    return facets


def get_term(term):
    facets = []
    facets.append({"format": term["search"], "total": int(term["count"])})
    if "term" in term:
        facets += get_children(term)
    return facets


def get_formats(zone):
    facets = []
    try:
        for term in zone["facets"]["facet"]["term"]:
            facets += get_term(term)
    except (KeyError, TypeError):
        return []
    return facets


def get_contrib_totals():
    params = {
        "zone": "article,book,collection,map,music,people,picture",
        "facet": "format",
        "encoding": "json",
        "n": 0,
        "key": API_KEY,
    }
    contributors = pd.read_csv(Path("data", "trove-contributors.csv")).to_dict("records")
    totals = []
    formats = []
    for contrib in contributors:
        if nuc := contrib["nuc"]:
            params["q"] = f'nuc:"{nuc}"'
            response = s.get("https://api.trove.nla.gov.au/v2/result", params=params)
            data = response.json()
            for zone in data["response"]["zone"]:
                totals.append(
                    {
                        "nuc": nuc,
                        "name": contrib["name"],
                        "zone": zone["name"],
                        "total": zone["records"]["total"],
                    }
                )
                facets = get_formats(zone)
                for facet in facets:
                    facet.update({"nuc": nuc, "name": contrib["name"], "zone": zone["name"]})
                    formats.append(facet)
            time.sleep(0.2)
    return totals, formats

def main():
    Path("data").mkdir(exist_ok=True)
    totals, formats = get_contrib_totals()
    df_totals = pd.DataFrame(totals)
    df_totals[["nuc", "name", "zone", "total"]].to_csv(Path("data", "trove-contributors-zones.csv"), index=False)
    df_formats = pd.DataFrame(formats)
    df_formats[["nuc", "name", "zone", "format", "total"]].to_csv(Path("data", "trove-contributors-formats.csv"), index=False)

if __name__ == "__main__":
    main()