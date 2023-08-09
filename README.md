# ZeldaGPT
Zelda lookup site, available at [zeldagpt-558d219d8755.herokuapp.com](https://zeldagpt-558d219d8755.herokuapp.com).

ZeldaGPT uses ChatGPT, Rockset, and the Zelda Fandom Wiki to answer questions about the Zelda universe. 

## Setup
First, you must setup your Rockset and OpenAI credentials. 
Access your OpenAI API key from the [OpenAI Platform](https://platform.openai.com/account/api-keys).
Create a Rockset API key from the [Rockset Console](https://console.rockset.com/apikeys).
Get your Rockset API server from the [Rockset API reference](https://rockset.com/docs/rest-api#introduction).

```bash
export ROCKSET_API_KEY="<rockset api key>"
export ROCKSET_API_SERVER="<rockset api server>"
export OPENAI_API_KEY="<openai api key>"
```

Then, install the requirements.

```bash
pip3 install -r requirements.txt
```

## Data ingestion
Before you can run the app, data must be scraped from zelda.fandom.com, split into chunks, embedded, and then saved into your Rockset collection. 
`ingest.py` does all this.
```bash
python3 ingest.py --reset # the 'reset' flag creates a new collection
```

If the program terminates for some reason, you can continue the ingest with `complete_ingest.py`.
```bash
python3 complete_ingest.py
```

## Starting the server
After your embeddings are stored in Rockset, you can run the app.
```python3
python3 main.py 
```

## Deployment
See [Heroku docs](https://devcenter.heroku.com/articles/github-integration#manual-deploys).