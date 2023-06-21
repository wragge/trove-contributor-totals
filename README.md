# Trove contributor totals

[![Frictionless](https://github.com/wragge/trove-contributor-totals/actions/workflows/frictionless.yaml/badge.svg)](https://repository.frictionlessdata.io/report?user=wragge&repo=trove-contributor-totals&flow=frictionless)

This repository contains an automated git scraper that uses the [Trove API](https://troveconsole.herokuapp.com/) to save details of organisations and projects that contribute metadata to Trove. It runs every week and updates the following datasets:

* [trove-contributors.json](data/trove-contributors.json)
* [trove-contributors.csv](data/trove-contributors.csv)
* [trove-contributors-zones.csv](data/trove-contributors-zones.csv)
* [trove-contributors-formats.csv](data/trove-contributors-formats.csv)
* [trove-contributors-categories.csv](data/trove-contributors-categories.csv) (API v3)
* [trove-contributors-categories-formats.csv](data/trove-contributors-categories-formats.csv) (API v3)

Note that the Trove API v3 organises resources by `category` rather than `zone`. The categories match those used in the web interface, but don't map directly to the old zones. I'm currently harvesting contributor data from both zones and categories and will continue to do so until the API v2 is decommissioned.

By retrieving all versions of these files from the commit history, you can analyse changes in Trove over time.

## Dataset details

### trove-contributors.json

This is the response from the Trove API's `contributor` endpoint saved as a JSON file without any additional processing. The JSON includes nested records which can make it tricky to use.

### trove-contributors.csv

This is a 'flattened' version of the nested contributors data. The dataset is saved as a CSV file containing the following columns:

* `id` – Trove identifier for organisation/project
* `nuc` – NUC (National Union Catalogue) identifier for this organisation/project
* `name` – name of the organisation/project
* `parent` – identifier of parent organisation
* `total` – number of records contributed by this organisation/project

Note that you can use the `nuc` values to search for items in Trove. For example, searching for `nuc:"ANU:IR"` will find [records from the ANU Institutional Repository](https://trove.nla.gov.au/search?keyword=nuc%3A%22ANU%3AIR%22).

### trove-contributors-zones.csv

This dataset was created by searching for contributor's NUC codes in each Trove zone. This gives a count of records by contributor and zone. The dataset is saved as a CSV file containing the following columns:

* `nuc` – NUC (National Union Catalogue) identifier for this organisation/project
* `name` – name of the organisation/project
* `zone` – name of the Trove zone
* `total` – number of records contributed by this organisation/project

### trove-contributors-formats.csv

This dataset was created by searching for contributor's NUC codes in each Trove zone and requesting the `format` facet. This gives a count of records by contributor, zone, and format. The dataset is saved as a CSV file containing the following columns:

* `nuc` – NUC (National Union Catalogue) identifier for this organisation/project
* `name` – name of the organisation/project
* `zone` – name of the Trove zone
* `format` – format type (see Trove's [list of formats](https://trove.nla.gov.au/about/create-something/using-api/api-technical-guide#formats))
* `total` – number of records contributed by this organisation/project

### trove-contributors-categories.csv

This dataset was created by applying the `l-partnerNuc` facet for each contributor to each Trove category. This gives a count of records by contributor and category. The dataset is saved as a CSV file containing the following columns:

* `nuc` – NUC (National Union Catalogue) identifier for this organisation/project
* `name` – name of the organisation/project
* `category_name` – full name of the Trove category
* `category_code` – Trove category slug
* `total` – number of records contributed by this organisation/project

### trove-contributors-categories-formats.csv

This dataset was created by applying the `l-partnerNuc` facet for each contributor to each Trove category and requesting the `format` facet. This gives a count of records by contributor, category, and format. The dataset is saved as a CSV file containing the following columns:

* `nuc` – NUC (National Union Catalogue) identifier for this organisation/project
* `name` – name of the organisation/project
* `category_name` – full name of the Trove category
* `category_code` – Trove category slug
* `format` – format type (see Trove's [list of formats](https://trove.nla.gov.au/about/create-something/using-api/api-technical-guide#formats))
* `total` – number of records contributed by this organisation/project

---

Created by [Tim Sherratt](https://timsherratt.org). If you think this is useful, you can become a [GitHub sponsor](https://github.com/sponsors/wragge).

