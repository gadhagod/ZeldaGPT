from os.path import dirname, join
from rockset.model.field_mapping_query import FieldMappingQuery

ingest_tranformation = FieldMappingQuery(
    sql=open(
        join(dirname(__file__), "ingest-transformation.sql")
    ).read()
)