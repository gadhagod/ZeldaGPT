# Zelda GPT
Zelda lookup site, available at [zeldagpt-558d219d8755.herokuapp.com](https://zeldagpt-558d219d8755.herokuapp.com).

## Setup
```bash
export ROCKSET_API_KEY="<rockset api key>"
export ROCKSET_API_SERVER="<rockset api server>"
export OPENAI_API_KEY="<open api key>"
pip3 install -r requirements.txt
```

## Data ingestion
```
python3 ingest.py
```

## Starting the server
```python3
python3 main.py
```

## Deployment
See [Heroku docs](https://devcenter.heroku.com/articles/github-integration#manual-deploys).