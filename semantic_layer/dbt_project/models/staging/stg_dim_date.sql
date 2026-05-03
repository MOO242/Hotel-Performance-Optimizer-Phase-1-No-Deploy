WITH source AS (
    SELECT * FROM {{ source('public', 'dim_date') }}
),

deduped AS (
    SELECT DISTINCT
        date,
        "mmm yy",
        "week no",
        day_type
    FROM source
)

SELECT * FROM deduped