# wiki-data-generator

Generates page data for a game wiki, backed by scraped data and manual additions.

## Requirements

- Python 3.11 or newer
- Access to the site being queried

## Installation

Install the project with its development dependency group. This uses pip's
dependency-group support, so use a recent version of pip:

```text
python -m pip install --upgrade pip
python -m pip install --group dev -e .
```

Using a virtual environment is optional and can be useful for isolating this
project's dependencies:

```text
python -m venv .venv
```

Activate `.venv` using the command appropriate for your shell before running
the installation command above if you choose to use one.

## Configuration

Set `FETCHER_BASE_URL` to the base URL of the site. The fetcher builds these
page URLs from it:

```text
<base-url>/Item.asp?id=<id>
<base-url>/Monster.asp?id=<id>
```

Configuration can be supplied through environment variables or a `.env` file
in the project directory:

```dotenv
FETCHER_BASE_URL=https://wiki.example.com
FETCHER_USER_AGENT_SUFFIX=(my wiki data project)
FETCHER_CACHE_DB=./fetcher_cache.sqlite
```

`FETCHER_BASE_URL` is required. The user-agent suffix defaults to
`(personal wiki-data project)`, and the cache defaults to
`./fetcher_cache.sqlite`.

## Usage

Run the CLI as a Python module file, specifying the entity type and numeric ID:

```text
python cli.py item 123
python cli.py monster 456
```

The command logs whether the requested page exists. A missing page exits with
status code `1`; a successful lookup exits with status code `0`.

## Fetching behavior

- Successful pages (`200`) return their HTML.
- Missing pages (`302`, which redirects to search) are reported as invalid.
- Unexpected HTTP status codes raise `RuntimeError`.
- Responses are cached in a SQLite database, so cached requests do not wait for
	the network rate limit.
- Uncached requests wait a random 2 to 4 seconds between requests and retry
	transient failures such as `429` and `5xx` responses.

## Testing

With the development dependency group installed, run:

```text
python -m pytest
```

The tests mock HTTP responses and timing, so they do not require access to the
live site.
