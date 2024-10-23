{{ config(
    materialized='table'
) }}

WITH trainer_data AS (
    SELECT
        worker_id,
        location,
        role,
        joined_date,
        trained,
        sessions_conducted,
        supervisor_name,
        phone_number,
        email,
        department
    FROM
        {{ ref('trainer_details') }}
)

SELECT
    worker_id,
    location,
    role,
    joined_date,
    trained,
    sessions_conducted,
    supervisor_name,
    phone_number,
    email,
    department
FROM
    trainer_data
