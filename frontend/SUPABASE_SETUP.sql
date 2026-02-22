-- Supabase Schema Setup for Ivy Wealth AI Platform
-- Run this SQL in your Supabase Project SQL Editor

-- 1. Create the clients table
CREATE TABLE IF NOT EXISTS clients (
  id BIGSERIAL PRIMARY KEY,
  client_id TEXT UNIQUE NOT NULL DEFAULT 'CLIENT_' || LPAD(CAST(CURRVAL('clients_id_seq') - 1 AS TEXT), 3, '0'),
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  portfolio_value BIGINT NOT NULL,
  risk_tolerance TEXT NOT NULL CHECK (risk_tolerance IN ('Conservative', 'Moderate', 'Aggressive')),
  goal_amount BIGINT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('On Track', 'At Risk', 'Needs Review')),
  last_report TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Enable RLS (Row Level Security)
ALTER TABLE clients ENABLE ROW LEVEL SECURITY;

-- 3. Create policy to allow public read access
CREATE POLICY "Enable read access for all users" ON clients
  FOR SELECT USING (true);

-- 4. Create policy to allow public insert access (for admin purposes)
CREATE POLICY "Enable insert for all users" ON clients
  FOR INSERT WITH CHECK (true);

-- 5. Create policy to allow public update access
CREATE POLICY "Enable update for all users" ON clients
  FOR UPDATE USING (true);

-- 6. Insert 50 sample clients
INSERT INTO clients (name, email, portfolio_value, risk_tolerance, goal_amount, status, last_report) VALUES
('John Smith', 'john.smith@email.com', 450000, 'Conservative', 750000, 'On Track', '2024-12-15'),
('Sarah Johnson', 'sarah.j@email.com', 850000, 'Moderate', 1200000, 'On Track', '2024-12-14'),
('Michael Brown', 'mbrown@email.com', 320000, 'Aggressive', 950000, 'At Risk', '2024-12-10'),
('Emma Davis', 'emma.davis@email.com', 620000, 'Conservative', 1000000, 'Needs Review', '2024-12-12'),
('David Garcia', 'd.garcia@email.com', 780000, 'Moderate', 1500000, 'On Track', '2024-12-15'),
('Lisa Martinez', 'lisa.m@email.com', 540000, 'Conservative', 850000, 'On Track', '2024-12-13'),
('James Wilson', 'james.w@email.com', 920000, 'Aggressive', 1800000, 'On Track', '2024-12-15'),
('Anna Anderson', 'anna.a@email.com', 380000, 'Moderate', 700000, 'Needs Review', '2024-12-11'),
('Robert Taylor', 'robert.t@email.com', 650000, 'Conservative', 1100000, 'At Risk', '2024-12-09'),
('Maria Thomas', 'maria.thomas@email.com', 510000, 'Moderate', 900000, 'On Track', '2024-12-14'),
('Christopher Moore', 'chris.moore@email.com', 1100000, 'Aggressive', 2000000, 'On Track', '2024-12-15'),
('Patricia Jackson', 'patricia.j@email.com', 420000, 'Conservative', 800000, 'On Track', '2024-12-15'),
('Daniel White', 'daniel.white@email.com', 680000, 'Moderate', 1300000, 'Needs Review', '2024-12-10'),
('Jennifer Harris', 'jennifer.h@email.com', 560000, 'Conservative', 950000, 'On Track', '2024-12-12'),
('Matthew Martin', 'matthew.m@email.com', 940000, 'Aggressive', 1900000, 'At Risk', '2024-12-08'),
('Linda Lee', 'linda.lee@email.com', 480000, 'Moderate', 850000, 'On Track', '2024-12-15'),
('Joseph Clark', 'joseph.c@email.com', 740000, 'Moderate', 1400000, 'On Track', '2024-12-14'),
('Barbara Rodriguez', 'barbara.r@email.com', 360000, 'Conservative', 700000, 'Needs Review', '2024-12-09'),
('Thomas Lewis', 'thomas.l@email.com', 820000, 'Aggressive', 1700000, 'On Track', '2024-12-15'),
('Susan Walker', 'susan.w@email.com', 520000, 'Conservative', 900000, 'On Track', '2024-12-13'),
('Charles Hall', 'charles.hall@email.com', 670000, 'Moderate', 1250000, 'At Risk', '2024-12-07'),
('Dorothy Allen', 'dorothy.a@email.com', 430000, 'Conservative', 800000, 'On Track', '2024-12-15'),
('Mark Young', 'mark.young@email.com', 890000, 'Aggressive', 1750000, 'On Track', '2024-12-15'),
('Ashley King', 'ashley.k@email.com', 510000, 'Moderate', 950000, 'Needs Review', '2024-12-11'),
('Anthony Wright', 'anthony.w@email.com', 620000, 'Conservative', 1050000, 'On Track', '2024-12-14'),
('Kimberly Gonzalez', 'kimberly.g@email.com', 950000, 'Aggressive', 1950000, 'On Track', '2024-12-15'),
('Donald Nelson', 'donald.n@email.com', 380000, 'Conservative', 750000, 'At Risk', '2024-12-06'),
('Donna Carter', 'donna.c@email.com', 730000, 'Moderate', 1350000, 'On Track', '2024-12-15'),
('Steven Mitchell', 'steven.m@email.com', 590000, 'Conservative', 1000000, 'On Track', '2024-12-13'),
('Carol Perez', 'carol.p@email.com', 860000, 'Aggressive', 1700000, 'Needs Review', '2024-12-12'),
('Paul Roberts', 'paul.r@email.com', 470000, 'Moderate', 850000, 'On Track', '2024-12-15'),
('Janet Phillips', 'janet.ph@email.com', 640000, 'Conservative', 1100000, 'On Track', '2024-12-14'),
('Andrew Campbell', 'andrew.c@email.com', 920000, 'Aggressive', 1850000, 'At Risk', '2024-12-05'),
('Maria Edwards', 'maria.e@email.com', 520000, 'Moderate', 900000, 'On Track', '2024-12-15'),
('Kenneth Collins', 'kenneth.c@email.com', 680000, 'Conservative', 1200000, 'On Track', '2024-12-13'),
('Kathleen Stewart', 'kathleen.s@email.com', 800000, 'Aggressive', 1600000, 'On Track', '2024-12-15'),
('Dennis Sanchez', 'dennis.s@email.com', 410000, 'Conservative', 800000, 'Needs Review', '2024-12-10'),
('Christine Morris', 'christine.m@email.com', 590000, 'Moderate', 1050000, 'On Track', '2024-12-14'),
('Jerry Rogers', 'jerry.r@email.com', 1050000, 'Aggressive', 2050000, 'On Track', '2024-12-15'),
('Cynthia Morgan', 'cynthia.m@email.com', 480000, 'Conservative', 900000, 'At Risk', '2024-12-04'),
('Lawrence Peterson', 'lawrence.p@email.com', 710000, 'Moderate', 1300000, 'On Track', '2024-12-15'),
('Kathleen Gardner', 'kathleen.g@email.com', 560000, 'Conservative', 1000000, 'On Track', '2024-12-13'),
('Ryan Payne', 'ryan.p@email.com', 870000, 'Aggressive', 1750000, 'Needs Review', '2024-12-11'),
('Shirley Dallas', 'shirley.d@email.com', 530000, 'Moderate', 900000, 'On Track', '2024-12-15'),
('Jacob Garland', 'jacob.g@email.com', 690000, 'Conservative', 1150000, 'On Track', '2024-12-14'),
('Angela Herrera', 'angela.h@email.com', 820000, 'Aggressive', 1650000, 'At Risk', '2024-12-03'),
('Jose Fields', 'jose.f@email.com', 450000, 'Moderate', 850000, 'On Track', '2024-12-15'),
('Helen Warner', 'helen.w@email.com', 620000, 'Conservative', 1050000, 'On Track', '2024-12-13');

-- 7. Create an index for faster queries
CREATE INDEX idx_clients_status ON clients(status);
CREATE INDEX idx_clients_risk_tolerance ON clients(risk_tolerance);

-- 8. Verify data was inserted
SELECT COUNT(*) as total_clients, 
       COUNT(CASE WHEN status = 'On Track' THEN 1 END) as on_track,
       COUNT(CASE WHEN status = 'At Risk' THEN 1 END) as at_risk,
       COUNT(CASE WHEN status = 'Needs Review' THEN 1 END) as needs_review
FROM clients;
