
WITH aggregated AS(
    select *
    from {{ ref('stg_fact_aggregated_bookings')}}
),

booking_agg AS (
    SELECT
        check_in_date::date,
        property_id::bigint,
        booking_channel,
        room_type,
        SUM(revenue_realized) AS total_revenue
    FROM {{ ref('stg_fact_bookings') }}
    WHERE booking_status = 'Checked Out'
    GROUP BY check_in_date::date, property_id::bigint, room_type,booking_channel
),

hotels_city AS (

    SELECT 
    property_id::bigint,
    city,
    category
    FROM {{ ref('stg_dim_hotels') }}
),


rooms_class AS (

    SELECT 
    room_id,
    room_class ::bigint
    FROM {{ ref('stg_dim_rooms') }}
),



calculation AS (

SELECT

f.check_in_date,
f.rooms_sold,
f.rooms_available,
f.room_category,
f.property_id,
b.total_revenue,
b.booking_channel,
h.city,
h.category,


CASE 
    WHEN f.rooms_sold > 0 THEN b.total_revenue / f.rooms_sold 
            ELSE 0 
    END AS adr

FROM aggregated f
LEFT JOIN booking_agg b 
    on f.property_id = b.property_id
    AND f.check_in_date ::date = b.check_in_date
    AND f.room_category = b.room_type
LEFT JOIN hotels_city h    
    on  f.property_id = h.property_id
LEFT JOIN rooms_class r
    on f.room_category = r.room_id

WHERE room_category IS NOT NULL 

)

SELECT * FROM calculation
