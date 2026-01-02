-- Create messages table in Supabase
CREATE TABLE IF NOT EXISTS messages (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create an index on created_at for faster queries
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- Drop policy if it exists, then create a new one
-- This allows the script to be run multiple times without errors
DROP POLICY IF EXISTS "Allow all operations for testing" ON messages;

-- Create a policy that allows all operations (adjust based on your security needs)
-- For testing purposes, we'll allow all operations
-- In production, you should restrict this based on your authentication requirements
CREATE POLICY "Allow all operations for testing" ON messages
    FOR ALL
    USING (true)
    WITH CHECK (true);

