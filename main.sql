-- Think of it as naming a step



WITH step1 AS (

    SELECT * FROM fact_bookings



),





step2 AS (

    SELECT booking_id, room_category
    FROM step1
    WHERE booking_status = 'Checked Out'
    
)



SELECT * FROM step2