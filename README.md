# Fetch Papers

A command-line tool to fetch research papers from PubMed.

## Features
- Search PubMed using a custom query.
- Save results to a CSV file.

## Installation
Use Poetry to install dependencies:
```bash
pip install poetry
poetry install    #NOTE : pyproject.toml should be in same directory where you will be running this command"
poetry run python fetch_papers.py "Diabetes treatment" --file results.csv
