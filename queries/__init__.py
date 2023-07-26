from os.path import dirname, join
from rockset.model.field_mapping_query import FieldMappingQuery
from rockset.models import QueryRequestSql

def get_sql(file_name: str) -> str:
    return open(
        join(dirname(__file__), file_name)
    ).read()

_ingest_tranformation = get_sql("ingest-tranformation.sql")
def ingest_tranformation() -> FieldMappingQuery:
    return FieldMappingQuery(
        sql=_ingest_tranformation
    )

_link_exists = get_sql("link-exists.sql")
def link_exists(link: str) -> QueryRequestSql:
    return QueryRequestSql(
        query=_link_exists,
        params={
            "name": "link",
            "type": "string",
            "value": str(link)
        }
    )