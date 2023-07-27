SELECT 
    DISTINCT source 
FROM (
    SELECT 
        source
    FROM
        commons."hyrule-compendium-ai"
    ORDER BY
        _event_time
    DESC
    LIMIT
        1000
) s