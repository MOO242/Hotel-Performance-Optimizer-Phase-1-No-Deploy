WITH source AS (
    SELECT
        *
    FROM
        {{ source(
            'public',
            'fact_aggregated'
        ) }}
)
SELECT
    *
FROM
    source
