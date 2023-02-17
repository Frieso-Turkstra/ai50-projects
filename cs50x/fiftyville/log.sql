-- Keep a log of any SQL queries you execute as you solve the mystery.

-- 1) The crime scene report seemed a good starting point
SELECT * FROM crime_scene_reports
    WHERE year == 2021
    AND month == 7
    AND day == 28
    AND street == 'Humphrey Street';

-- 2) I decided to look at the interviews of the witnesses mentioned in the crime scene report
SELECT * FROM interviews
    WHERE year == 2021
    AND month == 7
    AND day == 28
    AND transcript LIKE '%bakery%';

-- 3) @Ruth, I extracted all the license plates of the cars that left within 10 minutes of the theft
SELECT license_plate FROM bakery_security_logs
    WHERE year == 2021
    AND month == 7
    AND day == 28
    AND hour == 10
    AND minute BETWEEN 15 AND 25;

-- 4) @Eugene, I extracted the account numbers of people that withdrew money from Legget Street's ATM
SELECT account_number FROM atm_transactions
    WHERE year == 2021
    AND month == 7
    AND day == 28
    AND atm_location == 'Leggett Street'
    AND transaction_type == 'withdraw';

-- 5) @Raymond, I collected all the phone numbers that called that day for less than a minute
SELECT caller FROM phone_calls
    WHERE year == 2021
    AND month == 7
    AND day == 28
    AND duration < 60;

-- 6) @Raymond, I checked the first flight leaving from Fiftyville tomorrow
SELECT destination_airport_id, id FROM flights
    WHERE year == 2021
    AND month == 7
    AND day == 29
    AND origin_airport_id == (SELECT id FROM airports WHERE city == 'Fiftyville')
    ORDER BY hour
    LIMIT 1;

-- 7) Based on (6), the destination airport id is 4 so the city the thief escaped to is New York City
SELECT city FROM airports WHERE id == 4;

-- 8) Based on (6), I took all the passport numbers of the people taking that flight
SELECT passport_number FROM passengers WHERE flight_id == 36;

-- 9) I cross-referenced people based on their phone_number, passport_number and license plate
SELECT id FROM people
    WHERE phone_number IN
        (SELECT caller FROM phone_calls
            WHERE year == 2021
            AND month == 7
            AND day == 28
            AND duration < 60)
    AND passport_number IN
        (SELECT passport_number FROM passengers
            WHERE flight_id == 36)
    AND license_plate IN
        (SELECT license_plate FROM bakery_security_logs
            WHERE year == 2021
            AND month == 7
            AND day == 28
            AND hour == 10
            AND minute BETWEEN 15 AND 25);

-- 10) There are three suspects based on (9) whose id's I checked with the account numbers from (4)
SELECT person_id FROM bank_accounts
    WHERE person_id IN (398010, 560886, 686048)
    AND account_number IN
        (SELECT account_number FROM atm_transactions
            WHERE year == 2021
            AND month == 7
            AND day == 28
            AND atm_location == 'Leggett Street'
            AND transaction_type == 'withdraw');

-- 11) From (10), we learn that Bruce is the thief
SELECT name, phone_number FROM people WHERE id == 686048;

-- 12) The accomplice is the one who is called by Bruce, i.e. Robin
SELECT name FROM people
    WHERE phone_number ==
        (SELECT receiver FROM phone_calls
            WHERE year == 2021
            AND month == 7
            AND day == 28
            AND duration < 60
            AND caller == '(367) 555-5533');
