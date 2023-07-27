from queries import complete_ingest
from constants import rockset
from ingest import Scraper

Scraper(
    [res["source"] for res in rockset.Queries.query(sql=complete_ingest(1000)).results ]
)