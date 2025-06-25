
-- Create the table to store request counts
-- and the last requested time for Golang and Python
-- This table will be used to track the number of requests made for each language
CREATE TABLE request_counts (
    id SERIAL PRIMARY KEY,
    golang_requested_counts INT DEFAULT 0,
    python_requested_counts INT DEFAULT 0,
    last_go_requested_time TIMESTAMP,
    last_python_requested_time TIMESTAMP
);

-- Insert initial values into the request_counts table
INSERT INTO request_counts (id, golang_requested_counts, python_requested_counts) VALUES (1, 0, 0)