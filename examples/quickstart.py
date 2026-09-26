"""Open jobs at the companies you name, saved to jobs.csv.

Uses ATS Jobs API, a hosted Actor on Apify that reads Greenhouse, Lever,
Ashby, Workday and 18 more job boards.

Install: pip install -r requirements.txt
Run:     APIFY_TOKEN=<YOUR_APIFY_TOKEN> python quickstart.py [company ...]

A company can be a job board link, a website or a name, such as
https://boards.greenhouse.io/stripe, linear.app or palantir.
Your token is in Apify Console > Settings > API & Integrations.
Price per company, up to 1,000 of its open jobs included: $0.01 until
October 10, 2026, $0.045 from October 11, 2026, $0.12 planned from November 15, 2026.
MAX_CHARGE_USD caps what this one run can cost.
"""

import csv
import os
import sys
from decimal import Decimal

from apify_client import ApifyClient

ACTOR_ID = "conserving_celerytop/live-career-page-jobs-api"
MAX_CHARGE_USD = Decimal("0.50")
DEFAULT_COMPANIES = [
    "https://boards.greenhouse.io/stripe",
    "https://jobs.lever.co/palantir",
    "https://jobs.ashbyhq.com/openai",
]
COLUMNS = [
    "companySlug", "title", "department", "location", "countryCode", "workplaceType",
    "seniority", "jobFunction", "salaryMin", "salaryMax", "salaryCurrency", "salaryPeriod",
    "postedAt", "url",
]


def main() -> None:
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set APIFY_TOKEN first, for example: APIFY_TOKEN=<YOUR_APIFY_TOKEN> python quickstart.py")

    run_input = {
        "companies": sys.argv[1:] or DEFAULT_COMPANIES,  # up to 500 per run
        "postedSince": "30 days",
    }

    client = ApifyClient(token)
    # Starts a run and waits until it finishes.
    run = client.actor(ACTOR_ID).call(run_input=run_input, max_total_charge_usd=MAX_CHARGE_USD)
    if run is None or run.status != "SUCCEEDED":
        sys.exit(f"The run did not succeed: {run.status if run else 'no run'}")

    saved = 0
    with open("jobs.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for row in client.dataset(run.default_dataset_id).iterate_items():
            if row.get("rowType") == "job":
                writer.writerow(row)
                saved += 1
            elif row.get("rowType") == "status":
                # A company with no job rows gets one status row, such as no_matching_jobs.
                print(f"{row.get('company')}: {row.get('companyStatus')}")

    print(f"Saved {saved} jobs to jobs.csv")


if __name__ == "__main__":
    main()
