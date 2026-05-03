WITH source AS (SELECT * from 

{{source ('public', 'fact_bookings')}}),

renamed AS (

    SELECT 

        booking_id,
        property_id,
        booking_date,
        check_in_date,
        checkout_date,
        no_guests AS number_of_guests,
        room_category AS room_type,
        booking_platform AS booking_channel,
        ratings_given AS guest_rating_score,
        booking_status,
        revenue_generated AS revenue_booked_amount,
        revenue_realized,
        room_rate AS room_rate_amount,
        nights AS number_of_nights

FROM  source 

)

select * from renamed 
