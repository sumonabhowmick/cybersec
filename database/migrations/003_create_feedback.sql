ALTER TABLE analyst_feedback ADD COLUMN IF NOT EXISTS reviewed BOOLEAN NOT NULL DEFAULT FALSE;
CREATE INDEX IF NOT EXISTS idx_feedback_reviewed ON analyst_feedback(reviewed, created_at);
