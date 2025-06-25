-- Create the table
CREATE TABLE IF NOT EXISTS public.request (
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    caller_id VARCHAR(10) NOT NULL CHECK (caller_id IN ('python', 'go'))
);
