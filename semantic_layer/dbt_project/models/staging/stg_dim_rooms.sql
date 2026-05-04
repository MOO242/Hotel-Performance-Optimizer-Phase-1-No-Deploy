WITH source AS (
    SELECT
        *
    FROM
        {{ source(
            'public',
            'dim_rooms'
        ) }}
)
SELECT
    *
FROM
    source
