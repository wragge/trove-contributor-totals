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
        for term in zone["facets"]["facet"][0]["term"]:
            facets += get_term(term)
    except (KeyError, TypeError):
        return []
    return facets


def get_contrib_category_totals():
    params = {
        "category": "book,diary,image,research,magazine,music",
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
            # Could use either index or facet -- they seem to produce the same results
            # params["q"] = f'nuc:"{nuc}"'
            params["l-partnerNuc"] = nuc
            response = s.get("https://api.trove.nla.gov.au/v3/result", params=params)
            data = response.json()
            for category in data["category"]:
                totals.append(
                    {
                        "nuc": nuc,
                        "name": contrib["name"],
                        "category_name": category["name"],
                        "category_code": category["code"],
                        "total": category["records"]["total"],
                    }
                )
                facets = get_formats(category)
                for facet in facets:
                    facet.update({"nuc": nuc, "name": contrib["name"], "category_name": category["name"], "category_code": category["code"]})
                    formats.append(facet)
            time.sleep(0.2)
    return totals, formats

def main():
    Path("data").mkdir(exist_ok=True)
    cat_totals, cat_formats = get_contrib_category_totals()
    df_cat_totals = pd.DataFrame(cat_totals)
    df_cat_totals[["nuc", "name", "category_name", "category_code", "total"]].to_csv(Path("data", "trove-contributors-categories.csv"), index=False)
    df_cat_formats = pd.DataFrame(cat_formats)
    df_cat_formats[["nuc", "name", "category_name", "category_code", "format", "total"]].to_csv(Path("data", "trove-contributors-categories-formats.csv"), index=False)

if __name__ == "__main__":
    main()