SELECT 
    DISTINCT source 
FROM (
    SELECT 
        source
    FROM
        zeldagpt
    ORDER BY
        _event_time
    DESC
    LIMIT
        :lim
) s