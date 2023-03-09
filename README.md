# Trove contributor totals

[![Frictionless](https://github.com/wragge/trove-contributor-totals/actions/workflows/frictionless.yaml/badge.svg)](https://repository.frictionlessdata.io/report?user=wragge&repo=trove-contributor-totals&flow=frictionless)

This repository contains an automated git scraper that uses the [Trove API](https://troveconsole.herokuapp.com/) to save details of organisations and projects that contribute metadata to Trove. It runs every week and updates the following datasets:

* [trove-contributors.csv](data/trove-contributors.csv)

By retrieving all versions of these files from the commit history, you can analyse changes in Trove over time.

## Dataset details

### trove-contributors.csv

The dataset is saved as a CSV file containing the following columns:

* `id` – Trove identifier for organisation/project
* `name` – name of the organisation/project
* `total_items` – number of records contributed by this organisation/project
* `parent` – identifier of parent organisation
* `nuc` – NUC (National Union Catalogue) identifier for this organisation/project

Note that you can use the `nuc` values to search for items in Trove. For example, searching for `nuc:"ANU:IR"` will find [records from the ANU Institutional Repository](https://trove.nla.gov.au/search?keyword=nuc%3A%22ANU%3AIR%22).

---

Created by [Tim Sherratt](https://timsherratt.org), April 2022. If you think this is useful, you can become a [GitHub sponsor](https://github.com/sponsors/wragge).

