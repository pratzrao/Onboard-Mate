with source_data as (
    select 
        worker_id,
        location,
        role,
        joined_date,
        sessions_conducted,
        supervisor_name,
        phone_number,
        email,
        department
    from 
        {{ source('hackathon_pratiksha', 'trainer_details') }}
)

select 
    worker_id,
    location,
    role,
    joined_date,
    sessions_conducted,
    supervisor_name,
    phone_number,
    email,
    department
from 
    source_data
