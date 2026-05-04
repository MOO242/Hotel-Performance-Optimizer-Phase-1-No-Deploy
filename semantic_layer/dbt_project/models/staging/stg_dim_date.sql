WITH source AS (
    SELECT *
    FROM { { source(
            'public',
            'dim_date'
        ) } }
),
deduped AS (
    SELECT DISTINCT DATE,
        "mmm yy",
        "week no",
        day_type
    FROM source
)
SELECT *
FROM deduped