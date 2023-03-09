# Trove contributor totals

[![Frictionless](https://github.com/wragge/trove-contributor-totals/actions/workflows/frictionless.yaml/badge.svg)](https://repository.frictionlessdata.io/report?user=wragge&repo=trove-contributor-totals&flow=frictionless)

This repository contains an automated git scraper that uses the [Trove API](https://troveconsole.herokuapp.com/) to save details of organisations and projects that contribute metadata to Trove. It runs every week and updates the following datasets:

* [trove-contributors.json](data/trove-contributors.json)
* [trove-contributors.csv](data/trove-contributors.csv)
* [trove-contributors-zones.csv](data/trove-contributors-zones.csv)
* [trove-contributors-formats.csv](data/trove-contributors-formats.csv)

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

* `id` – Trove identifier for organisation/project
* `nuc` – NUC (National Union Catalogue) identifier for this organisation/project
* `name` – name of the organisation/project
* `parent` – identifier of parent organisation
* `zone` – name of the Trove zone
* `total` – number of records contributed by this organisation/project

### trove-contributors-formats.csv

This dataset was created by searching for contributor's NUC codes in each Trove zone and requesting the `format` facet. This gives a count of records by contributor, zone, and format. The dataset is saved as a CSV file containing the following columns:

* `id` – Trove identifier for organisation/project
* `nuc` – NUC (National Union Catalogue) identifier for this organisation/project
* `name` – name of the organisation/project
* `parent` – identifier of parent organisation
* `zone` – name of the Trove zone
* `format` – format type (see Trove's [list of formats](https://trove.nla.gov.au/about/create-something/using-api/api-technical-guide#formats))
* `total` – number of records contributed by this organisation/project



---

Created by [Tim Sherratt](https://timsherratt.org), April 2022. If you think this is useful, you can become a [GitHub sponsor](https://github.com/sponsors/wragge).

