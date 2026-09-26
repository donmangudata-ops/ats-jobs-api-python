# ATS Jobs API for Python and MCP: Greenhouse, Lever and Ashby jobs API

Get every open job at the companies you list, from Greenhouse, Lever, Ashby, Workday and 18 more job boards, in one JSON format, from Python, curl or an AI agent.

The jobs come from [ATS Jobs API](https://apify.com/conserving_celerytop/live-career-page-jobs-api), a hosted Actor on Apify. This repo holds a Python quick start, a curl example and MCP setup for 5 AI clients. There is no scraper code here. The example code is MIT licensed.

## What it returns

Send job board links, company websites or names, up to 500 per run. You get one row per open job:

```json
{
  "rowType": "job",
  "companySlug": "stripe",
  "title": "Senior Data Engineer",
  "department": "Engineering",
  "location": "Dublin, Ireland",
  "countryCode": "IE",
  "workplaceType": "hybrid",
  "seniority": "senior",
  "salaryMin": null,
  "postedAt": "2026-09-21T09:12:00.000Z",
  "url": "https://..."
}
```

- The same fields on all 22 boards, including `title`, `department`, `location`, `countryCode`, `remote`, `workplaceType`, `seniority`, `jobFunction`, `salaryMin`, `salaryMax`, `salaryCurrency`, `postedAt`, `url` and `applyUrl`.
- `jobKey` stays the same across runs, so you can join runs on it.
- A company with no job to return gets one status row, such as `no_matching_jobs`, `no_open_jobs` or `not_found`.
- Filters: title words, location, remote only, seniority, job function, posted since, published salary.
- `"outputMode": "companies"` gives one hiring summary row per company instead.
- `"onlyNewJobs": true` returns only new and closed jobs since your last check.

Boards: Greenhouse, Lever, Ashby, Workday, Eightfold, Workable, Personio, Teamtailor, Recruitee, JOIN, Homerun, Gem, JazzHR, Paylocity, Freshteam, PageUp, Polymer, HireHive, HiringThing, Trakstar Hire, ClearCompany and GoHire.

## Python quick start

You need an Apify account and its API token (Apify Console > **Settings** > **API & Integrations**).

```bash
pip install "apify-client>=3.2,<4"
export APIFY_TOKEN=<YOUR_APIFY_TOKEN>
```

```python
import os
from decimal import Decimal
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
companies = ["https://boards.greenhouse.io/stripe", "https://jobs.lever.co/palantir", "https://jobs.ashbyhq.com/openai"]
run = client.actor("conserving_celerytop/live-career-page-jobs-api").call(
    run_input={"companies": companies, "titleIncludes": ["engineer"]}, max_total_charge_usd=Decimal("0.10"))
for row in client.dataset(run.default_dataset_id).iterate_items():
    if row["rowType"] == "job":
        print(row["companySlug"], "|", row["title"], "|", row["location"], "|", row["url"])
```

`max_total_charge_usd` caps what the run can cost. The full script is [examples/quickstart.py](examples/quickstart.py): it takes companies as arguments and saves the jobs to `jobs.csv`.

```bash
pip install -r examples/requirements.txt
python examples/quickstart.py stripe linear.app https://jobs.ashbyhq.com/openai
```

## curl

This request starts a run, waits up to 300 seconds and returns the rows.

```bash
curl -X POST "https://api.apify.com/v2/acts/conserving_celerytop~live-career-page-jobs-api/run-sync-get-dataset-items?maxTotalChargeUsd=0.10" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"companies": ["https://boards.greenhouse.io/stripe", "https://jobs.lever.co/palantir"], "postedSince": "7 days"}'
```

Add `&format=csv` to the URL for CSV.

## Use it as an MCP tool in Claude, Cursor, VS Code or ChatGPT

Apify hosts the MCP server. This URL adds only this Actor as a tool:

```
https://mcp.apify.com/?tools=fetch-actor-details,conserving_celerytop/live-career-page-jobs-api
```

On first use, the client opens a browser window to sign in to Apify (OAuth). Runs are charged to your Apify account at the prices below.

**Claude Code**

```bash
claude mcp add --transport http ats-jobs-api "https://mcp.apify.com/?tools=fetch-actor-details,conserving_celerytop/live-career-page-jobs-api"
```

Then run `/mcp` in Claude Code and sign in.

**Claude (desktop app and claude.ai)**

**Settings** > **Connectors** > **Add custom connector**. Name: `ATS Jobs API`. URL: the URL above.

**Cursor** (`.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "ats-jobs-api": {
      "url": "https://mcp.apify.com/?tools=fetch-actor-details,conserving_celerytop/live-career-page-jobs-api"
    }
  }
}
```

**VS Code** (`.vscode/mcp.json`)

```json
{
  "servers": {
    "ats-jobs-api": {
      "type": "http",
      "url": "https://mcp.apify.com/?tools=fetch-actor-details,conserving_celerytop/live-career-page-jobs-api"
    }
  }
}
```

**ChatGPT** (Developer mode on)

**Settings** > **Apps & Connectors** > **Create**. MCP Server URL: the URL above. Authentication: OAuth.

To use a token instead of OAuth, send the header `Authorization: Bearer <YOUR_APIFY_TOKEN>`. Then ask, for example: "List the open data engineering jobs at Stripe, Linear and Ramp posted in the last 14 days."

## Pricing

$0.01 per company, including up to 1,000 of its open jobs, so 100 companies cost $1.00 (less on paid Apify plans: $0.0095 on Starter, $0.009 on Scale, $0.008 on Business). Each further 1,000 jobs of the same company costs $0.01. A later check with `onlyNewJobs` costs $0.002 per 1,000 open jobs on the board. Descriptions on Workday, Eightfold and 8 other boards cost $0.01 per 200 jobs, and are free on the rest. Invalid, unsupported and duplicate entries are free, and Apify platform usage is included. These are the prices in September 2026; the [Store page](https://apify.com/conserving_celerytop/live-career-page-jobs-api) has the current ones.

## Related

- [Tech Jobs Search](https://apify.com/conserving_celerytop/tech-jobs-search): search the open jobs of 574 tech, AI and remote-first companies by keyword, $1 per 1,000 matching jobs.
- [Live Jobs HTTP API](https://apify.com/conserving_celerytop/live-jobs-http-api): the same data in one GET or POST request.

Questions and board requests: the **Issues** tab of the [Actor's page](https://apify.com/conserving_celerytop/live-career-page-jobs-api).

## Not affiliated

This repo and the Actor are not affiliated with or endorsed by Greenhouse, Lever, Ashby, Workday, Eightfold or any other job board. Their names are trademarks of their owners. The Actor reads only job postings that companies publish on public job boards, with no login.

## License

MIT. See [LICENSE](LICENSE). Made by Don Mangu.
