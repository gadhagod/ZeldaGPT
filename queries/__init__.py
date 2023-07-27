from os.path import dirname, join
from rockset.model.field_mapping_query import FieldMappingQuery
from rockset.models import QueryRequestSql

def get_sql(file_name: str) -> str:
    return open(
        join(dirname(__file__), file_name)
    ).read()

_ingest_tranformation = get_sql("ingest-transformation.sql")
def ingest_tranformation() -> FieldMappingQuery:
    return FieldMappingQuery(
        sql=_ingest_tranformation
    )

_link_exists = get_sql("link-exists.sql")
def link_exists(link: str) -> QueryRequestSql:
    return QueryRequestSql(
        query=_link_exists,
        parameters=[{
            "name": "link",
            "type": "string",
            "value": str(link)
        }]
    )
    
_complete_ingest = get_sql("complete-ingest.sql")
def complete_ingest(limit: int) -> QueryRequestSql:
    return QueryRequestSql(
        query=_complete_ingest,
        parameters=[{
            "name": "lim",
            "type": "int",
            "value": str(limit)
        }]
    )