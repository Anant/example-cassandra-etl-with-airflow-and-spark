CREATE TABLE test.previous_employees_by_job_title (
    job_title text,
    employee_id uuid,
    employee_name text,
    first_day timestamp,
    last_day timestamp,
    PRIMARY KEY (job_title, employee_id)
) WITH CLUSTERING ORDER BY (employee_id ASC);

CREATE TABLE test.days_worked_by_previous_employees_by_job_title (
    job_title text,
    employee_id uuid,
    employee_name text,
    days_worked int,
    PRIMARY KEY (job_title, employee_id)
) WITH CLUSTERING ORDER BY (employee_id ASC);