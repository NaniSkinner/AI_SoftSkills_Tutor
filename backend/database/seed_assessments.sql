-- ============================================================================
-- SEED ASSESSMENTS - Sample pre-generated assessments for demo
-- ============================================================================
-- This file contains 4 sample assessments per student (16 total)
-- These assessments are pre-generated to avoid OpenAI API costs on deployment.
-- ============================================================================

-- First, insert sample data entries that these assessments are based on
INSERT INTO data_entries (id, student_id, teacher_id, type, date, content, metadata) VALUES
('S001_20250815_1', 'S001', 'T001', 'Group Discussion Transcript', '2025-08-15', 'Student Eva actively participated in literature circle discussion about The Giver, demonstrating strong communication and social awareness skills.', '{}'),
('S002_20250816_1', 'S002', 'T001', 'Group Discussion Transcript', '2025-08-16', 'Student Lucas led a highly organized discussion with color-coded questions, showing exceptional planning and organization skills.', '{}'),
('S003_20250916_1', 'S003', 'T002', 'Group Discussion Transcript', '2025-09-16', 'Student Pat participated thoughtfully in discussion, asking clarifying questions and showing cognitive flexibility.', '{}'),
('S004_20250918_1', 'S004', 'T002', 'Reflection Journal', '2025-09-18', 'Student Mia reflected on a group project, showing strong self-awareness and collaborative spirit.', '{}')
ON CONFLICT (id) DO NOTHING;

-- ============================================================================
-- Sample Assessments - 4 per student showing diverse skill levels
-- ============================================================================

INSERT INTO assessments (
    data_entry_id, student_id, skill_name, skill_category,
    level, confidence_score, justification, source_quote,
    data_point_count, rubric_version, corrected
) VALUES

-- S001 (Eva) - 4 assessments showing her strengths and growth areas
('S001_20250815_1', 'S001', 'Communication', 'Social-Emotional', 'Advanced', 0.90,
'Eva articulates ideas clearly, builds on others'' contributions, and uses persuasive language. She makes thoughtful connections between text and theme.',
'Yeah, and I think it shows that even in a super controlled community, people still have emotions and curiosity.',
1, 'v1.0', false),

('S001_20250815_1', 'S001', 'Social Awareness', 'Social-Emotional', 'Advanced', 0.88,
'Eva actively noticed Jordan''s hesitation and made deliberate effort to include them, showing strong awareness of social dynamics.',
'Jordan, did you notice anything in the chapter that stood out to you? *Makes eye contact and leans forward slightly*',
1, 'v1.0', false),

('S001_20250815_1', 'S001', 'Organization', 'Executive Function', 'Developing', 0.72,
'Eva is using her planner, which shows she has organizational tools, but struggled to access the information smoothly when needed during the discussion.',
'Give me a second. *Flips through planner, slightly flustered*',
1, 'v1.0', false),

('S001_20250815_1', 'S001', 'Cognitive Flexibility', 'Executive Function', 'Proficient', 0.85,
'Eva easily adapted when Jordan brought up an unexpected connection, building on it rather than dismissing it.',
'Good thinking! That''s, like, the deeper question. It''s not just WHAT they control, but WHY.',
1, 'v1.0', false),

-- S002 (Lucas) - 4 assessments showing exceptional organization but developing social skills
('S002_20250816_1', 'S002', 'Organization', 'Executive Function', 'Advanced', 0.95,
'Lucas demonstrated exceptional organization with color-coded questions, tabbed book pages, and systematic materials management.',
'I color-coded them. Blue is for community rules, green is for emotion and choice, and yellow is for character development.',
1, 'v1.0', false),

('S002_20250816_1', 'S002', 'Planning & Prioritization', 'Executive Function', 'Advanced', 0.92,
'Lucas prepared a comprehensive, time-managed discussion plan with categorized questions, demonstrating advanced planning skills.',
'I made a list of discussion questions last night. I organized them by theme. We have 25 minutes, so that''s about two minutes per question if we''re efficient.',
1, 'v1.0', false),

('S002_20250816_1', 'S002', 'Social Awareness', 'Social-Emotional', 'Developing', 0.68,
'Lucas didn''t immediately pick up on social cues when Amir seemed overwhelmed by the number of questions.',
'This is a lot. Do we have to answer all of them? [Amir''s concern not initially addressed by Lucas]',
1, 'v1.0', false),

('S002_20250816_1', 'S002', 'Cognitive Flexibility', 'Executive Function', 'Developing', 0.70,
'Lucas struggled when the discussion deviated from his prepared questions, showing difficulty with spontaneity.',
'That wasn''t one of my prepared questions, but... *hesitates* ...okay, that is important.',
1, 'v1.0', false),

-- S003 (Pat) - 4 assessments showing thoughtful participation
('S003_20250916_1', 'S003', 'Communication', 'Social-Emotional', 'Proficient', 0.78,
'Pat communicated ideas clearly and asked thoughtful clarifying questions during the discussion.',
'Can we talk about why the community made these rules in the first place?',
1, 'v1.0', false),

('S003_20250916_1', 'S003', 'Cognitive Flexibility', 'Executive Function', 'Advanced', 0.86,
'Pat demonstrated strong ability to consider multiple perspectives and adapt thinking based on new information.',
'Maybe it''s both controlling and protective at the same time?',
1, 'v1.0', false),

('S003_20250916_1', 'S003', 'Self-Management', 'Social-Emotional', 'Proficient', 0.75,
'Pat maintained composure and focus throughout the discussion, managing emotions effectively.',
'*Takes a deep breath* Let me think about that for a moment.',
1, 'v1.0', false),

('S003_20250916_1', 'S003', 'Collaboration', 'Social-Emotional', 'Advanced', 0.82,
'Pat worked well with group members, building on ideas and encouraging participation from others.',
'That''s a really interesting point. What does everyone else think?',
1, 'v1.0', false),

-- S004 (Mia) - 4 assessments showing self-awareness and collaboration
('S004_20250918_1', 'S004', 'Self-Awareness', 'Social-Emotional', 'Advanced', 0.89,
'Mia demonstrated strong understanding of her own strengths and areas for growth in her reflection.',
'I realized I''m really good at encouraging others, but I need to work on speaking up more with my own ideas.',
1, 'v1.0', false),

('S004_20250918_1', 'S004', 'Collaboration', 'Social-Emotional', 'Advanced', 0.87,
'Mia showed excellent collaborative skills, actively supporting team members and contributing to group success.',
'I made sure everyone had a chance to share their ideas before we made the final decision.',
1, 'v1.0', false),

('S004_20250918_1', 'S004', 'Growth Mindset', 'Social-Emotional', 'Advanced', 0.85,
'Mia views challenges as opportunities to learn and is open to feedback and improvement.',
'I didn''t understand the concept at first, but I asked for help and practiced until I got it.',
1, 'v1.0', false),

('S004_20250918_1', 'S004', 'Task Initiation', 'Executive Function', 'Developing', 0.67,
'Mia sometimes needs prompting to begin tasks, showing task initiation is still developing.',
'I wasn''t sure where to start, so I waited until the teacher gave us more instructions.',
1, 'v1.0', false);
