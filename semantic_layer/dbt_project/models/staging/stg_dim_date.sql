WITH source AS (

    SELECT * FROM {{ source('public', 'dim_date')}}

),

renamed AS (

    SELECT 
            "mmm yy" AS month_year,
            "week no" AS week_number 

    FROM source   
)


SELECT * FROM renamed