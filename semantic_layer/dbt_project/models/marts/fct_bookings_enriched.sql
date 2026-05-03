WITH bookings AS (
    SELECT * FROM {{ ref('stg_fact_bookings') }}
),

hotels AS (
    SELECT * FROM {{ref('stg_dim_hotels')}}
),

rooms AS (
    SELECT * FROM {{ref('stg_dim_rooms')}}
),

dates  AS (
    SELECT * FROM {{ref('stg_dim_date')}}
),


joined  AS (

    SELECT 
    b.booking_id,
    b.property_id,
    b.check_in_date,
    b.checkout_date,
    b.number_of_guests,
    b.booking_channel,
    b.guest_rating_score,
    b.booking_status,
    b.revenue_booked_amount,
    b.revenue_realized,
    b.room_rate_amount,
    b.number_of_nights,
    b.room_type,
    b.booking_date,
    h.property_name,
    h.category,
    h.city,
    r.room_class, 
    d.day_type,
    MIN(b.room_rate_amount) OVER (PARTITION BY b.room_type) AS hurdle_rate,

    -- Season
CASE
    WHEN EXTRACT(MONTH FROM b.check_in_date) IN (5,6,7)   THEN 'High Season'
    WHEN EXTRACT(MONTH FROM b.check_in_date) IN (12,1,2)  THEN 'Peak Season'
    ELSE 'Low Season'

END AS season

FROM bookings b


    LEFT JOIN hotels h ON b.property_id::bigint = h.property_id
    LEFT JOIN rooms r ON b.room_type = r.room_id 
    LEFT JOIN dates d ON b.check_in_date::date = d.date::date
    

)

SELECT * FROM joined