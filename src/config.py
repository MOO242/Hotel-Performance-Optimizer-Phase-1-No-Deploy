rules = {
    "room_category": {"type": "list", "values": ["RT1", "RT2", "RT3", "RT4", "RT5"]},
    "booking_status": {
        "type": "list",
        "values": ["Checked Out", "Cancelled", "No Show"],
    },
    "booking_platform": {
        "type": "list",
        "values": [
            "direct online",
            "direct offline",
            "makeyourtrip",
            "others",
            "journey",
            "logtrip",
            "tripster",
        ],
    },
    "ratings_given": {"type": "list", "values": [1, 2, 3, 4, 5, 6], "nullable": True},
    "no_guests": {"type": "range", "values": [1, 2, 3, 4, 5, 6]},
}

# Columns that can NEVER be null
critical_columns = [
    "booking_id",
    "property_id",
    "booking_date",
    "check_in_date",
    "checkout_date",
    "no_guests",
    "room_category",
    "booking_platform",
    "booking_status",
    "rooms_sold",
    "room_available",
]

# Columns that CAN be null
nullable_columns = [
    "ratings_given",
    "revenue_generated",
    "revenue_realized",
    "room_rate",
    "nights",
]

# schema for data type
schema_ = {
    "booking_id": "str",
    "property_id": "str",
    "booking_date": "datetime64[ns]",
    "check_in_date": "datetime64[ns]",
    "checkout_date": "datetime64[ns]",
    "no_guests": "int64",
    "room_category": "str",
    "booking_platform": "str",
    "booking_status": "str",
    "ratings_given": "Int64",
    "revenue_generated": "float64",
    "revenue_realized": "float64",
    "room_rate": "float64",
    "nights": "Int64",
    "room_available": "int64",
    "rooms_sold": "int64",
}
