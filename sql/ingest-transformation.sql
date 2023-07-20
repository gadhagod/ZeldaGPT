SELECT
    *, VECTOR_ENFORCE(embeddings, 1536, 'float') as embeddings
FROM
    _input