WITH source AS (
    SELECT *
    FROM { { source(
            'public',
            'dim_hotels'
        ) } }
)
SELECT *
FROM source