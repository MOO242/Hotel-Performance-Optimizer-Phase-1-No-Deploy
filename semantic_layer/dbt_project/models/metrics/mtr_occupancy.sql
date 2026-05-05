
WITH aggregated AS(
    select *
    from {{ ref('stg_fact_aggregated_bookings')}}
),

booking_agg AS (
    SELECT
        check_in_date::date,
        property_id::bigint,
        room_type,
        SUM(revenue_realized) AS total_revenue
    FROM {{ ref('stg_fact_bookings') }}
    WHERE booking_status = 'Checked Out'
    GROUP BY check_in_date::date, property_id::bigint, room_type
),


calculation AS (

SELECT

f.check_in_date,
f.rooms_sold,
f.rooms_available,
f.room_category,
f.property_id,
b.total_revenue,
f.rooms_available - f.rooms_sold,
b.total_revenue / f.rooms_sold AS adr,
f.rooms_sold / f.rooms_available * 100 AS occupancy_rate,
b.total_revenue / f.rooms_available AS revpar



FROM aggregated f
LEFT JOIN booking_agg b 
    on f.property_id = b.property_id
    AND f.check_in_date ::date = b.check_in_date
    AND f.room_category = b.room_type
WHERE room_category IS NOT NULL 

)

SELECT * FROM calculation
