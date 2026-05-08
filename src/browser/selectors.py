"""Centralized selector mapping for IRCTC UI interactions."""

LOGIN_SELECTORS = {
    "username": [
        "input[name='userid']",
        "input[formcontrolname='userid']",
        "input[placeholder*='User']",
    ],
    "password": [
        "input[name='password']",
        "input[formcontrolname='password']",
        "input[type='password']",
    ],
    "captcha_image": [
        "img[alt='captcha']",
        "img.captcha-img",
        "img[src*='captcha']",
    ],
    "captcha_input": [
        "input[name='captcha']",
        "input[formcontrolname='captcha']",
        "input[placeholder*='Captcha']",
    ],
    "submit": [
        "button[type='submit']",
        "button:has-text('SIGNIN')",
        "button:has-text('SIGN IN')",
        "button:has-text('Login')",
    ],
}

SEARCH_SELECTORS = {
    "from_station": [
        "input[name='fromStationCode']",
        "input[placeholder*='From']",
        "input[aria-label*='From']",
    ],
    "to_station": [
        "input[name='toStationCode']",
        "input[placeholder*='To']",
        "input[aria-label*='To']",
    ],
    "travel_date": [
        "input[name='travelDate']",
        "input[placeholder*='Date']",
        "input[aria-label*='Date']",
    ],
    "class_select": [
        "select[name='class']",
        "select[formcontrolname='journeyClass']",
    ],
    "search_button": [
        "button[name='search']",
        "button:has-text('Search')",
        "button:has-text('Find Trains')",
    ],
    "result_rows": [
        "app-train-list .train_avl_enq_box",
        ".train_avl_enq_box",
        "table tbody tr",
    ],
    "train_number": [".train-number", ".trainNo", "[data-train-number]"],
    "train_name": [".train-name", ".trainName", "[data-train-name]"],
    "book_button": [
        "button:has-text('Book Now')",
        "button:has-text('Book')",
        "button:has-text('Continue')",
    ],
}

BOOKING_SELECTORS = {
    "pnr": [
        "text=/PNR\\s*[:\\-]?\\s*\\d{10}/i",
        "[class*='pnr']",
        ".pnr-number",
    ],
    "passenger_name_inputs": [
        "input[name*='passengerName']",
        "input[formcontrolname*='passengerName']",
        "input[placeholder*='Passenger Name']",
    ],
    "passenger_age_inputs": [
        "input[name*='passengerAge']",
        "input[formcontrolname*='passengerAge']",
        "input[placeholder*='Age']",
    ],
    "passenger_gender_selects": [
        "select[name*='passengerGender']",
        "select[formcontrolname*='passengerGender']",
    ],
    "berth_selects": [
        "select[name*='berth']",
        "select[formcontrolname*='berth']",
    ],
    "continue_button": [
        "button:has-text('Continue')",
        "button:has-text('Proceed')",
        "button:has-text('Review Journey Details')",
    ],
    "payment_page_marker": [
        "text=/Payment/i",
        "app-payment-options",
        ".payment-options",
    ],
}
