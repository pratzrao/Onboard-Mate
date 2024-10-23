{{ config(
    materialized='table',
    schema='public',
    alias='t2'
) }}

WITH donor_data AS (
    SELECT
        donor_id,
        first_name,
        last_name,
        age,
        email,
        country,
        postal_code,
        donation_amount,
        donation_date,
        donation_purpose
    FROM
        {{ ref('donor_details') }}
)

SELECT
    donor_id,
    first_name,
    last_name,
    age,
    email,
    country,
    postal_code,
    donation_amount,
    donation_date,
    donation_purpose
FROM
    donor_data
