-- Database Optimization Script for Job Matching System
-- Run this script after database creation to improve performance

-- Add indexes for frequently queried columns
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_user_type ON users(user_type);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);

CREATE INDEX IF NOT EXISTS idx_job_postings_is_active ON job_postings(is_active);
CREATE INDEX IF NOT EXISTS idx_job_postings_company_id ON job_postings(company_id);
CREATE INDEX IF NOT EXISTS idx_job_postings_created_at ON job_postings(created_at);
CREATE INDEX IF NOT EXISTS idx_job_postings_location ON job_postings(location);

CREATE INDEX IF NOT EXISTS idx_job_applications_job_id ON job_applications(job_id);
CREATE INDEX IF NOT EXISTS idx_job_applications_candidate_id ON job_applications(candidate_id);
CREATE INDEX IF NOT EXISTS idx_job_applications_status ON job_applications(application_status);
CREATE INDEX IF NOT EXISTS idx_job_applications_applied_at ON job_applications(applied_at);

CREATE INDEX IF NOT EXISTS idx_candidate_skills_candidate_id ON candidate_skills(candidate_id);
CREATE INDEX IF NOT EXISTS idx_candidate_skills_skill_id ON candidate_skills(skill_id);

CREATE INDEX IF NOT EXISTS idx_job_required_skills_job_id ON job_required_skills(job_id);
CREATE INDEX IF NOT EXISTS idx_job_required_skills_skill_id ON job_required_skills(skill_id);

CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read);
CREATE INDEX IF NOT EXISTS idx_notifications_created_at ON notifications(created_at);

CREATE INDEX IF NOT EXISTS idx_messages_sender_id ON messages(sender_id);
CREATE INDEX IF NOT EXISTS idx_messages_receiver_id ON messages(receiver_id);
CREATE INDEX IF NOT EXISTS idx_messages_thread_id ON messages(thread_id);

CREATE INDEX IF NOT EXISTS idx_exam_attempts_candidate_id ON exam_attempts(candidate_id);
CREATE INDEX IF NOT EXISTS idx_exam_attempts_exam_id ON exam_attempts(exam_id);
CREATE INDEX IF NOT EXISTS idx_exam_attempts_status ON exam_attempts(status);

-- Composite indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_job_postings_active_created ON job_postings(is_active, created_at);
CREATE INDEX IF NOT EXISTS idx_notifications_user_unread ON notifications(user_id, is_read, created_at);
CREATE INDEX IF NOT EXISTS idx_job_applications_candidate_job ON job_applications(candidate_id, job_id);

-- Add database constraints for data integrity
ALTER TABLE users ADD CONSTRAINT chk_email_format CHECK (email REGEXP '^[^@]+@[^@]+\.[^@]+$');
ALTER TABLE candidate_profiles ADD CONSTRAINT chk_salary_positive CHECK (salary_expectation >= 0);
ALTER TABLE job_postings ADD CONSTRAINT chk_salary_range CHECK (salary_min <= salary_max);
ALTER TABLE job_postings ADD CONSTRAINT chk_experience_positive CHECK (experience_required >= 0);

-- Set proper character sets for text fields
ALTER TABLE job_postings MODIFY description TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE job_postings MODIFY requirements TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE candidate_profiles MODIFY summary TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE companies MODIFY description TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Optimize table storage
OPTIMIZE TABLE users;
OPTIMIZE TABLE job_postings;
OPTIMIZE TABLE job_applications;
OPTIMIZE TABLE candidate_profiles;
OPTIMIZE TABLE companies;
OPTIMIZE TABLE notifications;

-- Update table statistics
ANALYZE TABLE users;
ANALYZE TABLE job_postings;
ANALYZE TABLE job_applications;
ANALYZE TABLE candidate_profiles;
ANALYZE TABLE companies;