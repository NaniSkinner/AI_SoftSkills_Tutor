-- ============================================================================
-- SEED ASSESSMENTS - Longitudinal Progress Data (6 Months)
-- ============================================================================
-- This file contains 16 assessments showing student progress over 6 months
-- 4 students × 4 time periods × 1 core skill = 16 total assessments
--
-- Timeline: Sept 2024 → Nov 2024 → Jan 2025 → Feb 2025
--
-- Each student has ONE focus skill tracked across all 4 time periods,
-- demonstrating realistic learning curves with plateaus and breakthroughs.
-- ============================================================================

-- Data Entries: 16 total (4 per student across 6 months)
INSERT INTO data_entries (id, student_id, teacher_id, type, date, content, metadata) VALUES
-- S001 (Eva) - Focus: Organization skill development
('S001_20240915_1', 'S001', 'T001', 'Teacher Observation', '2024-09-15', 'Eva participated in group discussion about The Giver. She had good ideas but struggled to organize her notes and needed time to find information in her planner when called upon.', '{}'),
('S001_20241115_2', 'S001', 'T001', 'Teacher Observation', '2024-11-15', 'Eva led a book club discussion. Still working on organization - her materials were spread out and she had to pause to locate her discussion questions, but showing gradual improvement.', '{}'),
('S001_20250115_3', 'S001', 'T001', 'Group Discussion Transcript', '2025-01-15', 'Eva facilitated project planning meeting with color-coded agenda and organized materials. Breakthrough moment - she quickly accessed all needed information without hesitation!', '{}'),
('S001_20250215_4', 'S001', 'T001', 'Project Presentation', '2025-02-15', 'Eva presented final project with exceptional organization - all materials tabbed, timeline clearly displayed, and smooth transitions between topics. Maintains new organizational habits consistently.', '{}'),

-- S002 (Lucas) - Focus: Social Awareness skill development
('S002_20240916_1', 'S002', 'T001', 'Teacher Observation', '2024-09-16', 'Lucas led discussion with impressive preparation but missed social cues when teammates seemed overwhelmed by his detailed agenda. Needs development in reading group dynamics.', '{}'),
('S002_20241116_2', 'S002', 'T001', 'Peer Feedback', '2024-11-16', 'Lucas organized group project. Peers noted he is starting to check in more with team members, though still sometimes pushes his plans without reading the room. Showing awareness is developing.', '{}'),
('S002_20250116_3', 'S002', 'T001', 'Group Discussion Transcript', '2025-01-16', 'Lucas facilitated brainstorming session and successfully picked up on Jordan''s hesitation, pausing to invite their input. Clear progress in noticing and responding to social cues!', '{}'),
('S002_20250216_4', 'S002', 'T001', 'Collaboration Activity', '2025-02-16', 'Lucas demonstrated consistent social awareness - regularly checked team members'' understanding, adjusted pace based on group energy, and created inclusive environment throughout project.', '{}'),

-- S003 (Pat) - Focus: Communication skill development
('S003_20240917_1', 'S003', 'T002', 'Group Discussion Transcript', '2024-09-17', 'Pat asked thoughtful clarifying questions during literature circle. Communication is clear and ideas are well-expressed, though sometimes hesitant to elaborate on initial thoughts.', '{}'),
('S003_20241117_2', 'S003', 'T002', 'Teacher Observation', '2024-11-17', 'Pat presented book review with good structure. Communication skills are solid - spoke clearly with supporting evidence. Building confidence in expressing complex ideas to larger audience.', '{}'),
('S003_20250117_3', 'S003', 'T002', 'Reflection Journal', '2025-01-17', 'Pat led class debate on environmental policy. Excellent communication - articulated nuanced position, responded to counterarguments effectively, and helped others understand complex issues.', '{}'),
('S003_20250217_4', 'S003', 'T002', 'Project Presentation', '2025-02-17', 'Pat delivered persuasive presentation to panel of teachers. Exceptional communication skills - clear thesis, compelling evidence, engaging delivery, and sophisticated response to questions.', '{}'),

-- S004 (Mia) - Focus: Task Initiation skill development
('S004_20240918_1', 'S004', 'T002', 'Teacher Observation', '2024-09-18', 'Mia participated in group activity but needed multiple prompts to begin her portion of the task. Waited for explicit instructions before starting each step. Task initiation needs development.', '{}'),
('S004_20241118_2', 'S004', 'T002', 'Reflection Journal', '2024-11-18', 'Mia reflected on group project. She acknowledged needing reminders to start tasks but showed awareness of the issue. Still requires some prompting but attempting to self-start occasionally.', '{}'),
('S004_20250118_3', 'S004', 'T002', 'Teacher Observation', '2025-01-18', 'Mia began independent research project with minimal prompting. Asked clarifying questions then dove in. Notable improvement - she is starting to take initiative more consistently!', '{}'),
('S004_20250218_4', 'S004', 'T002', 'Project Presentation', '2025-02-18', 'Mia independently initiated all project phases, created her own timeline, and began tasks without waiting for reminders. Task initiation has become a strength rather than area of concern.', '{}')

ON CONFLICT (id) DO NOTHING;

-- ============================================================================
-- Assessments: 16 total (4 per student, 1 per time period)
-- Each student has ONE skill tracked over time showing progression
-- ============================================================================

INSERT INTO assessments (
    data_entry_id, student_id, skill_name, skill_category,
    level, confidence_score, justification, source_quote,
    data_point_count, rubric_version, corrected
) VALUES

-- ============================================================================
-- S001 (Eva) - Organization: Developing → Developing → Proficient → Advanced
-- Story: Struggles with organizing materials, has breakthrough in January,
-- maintains new organizational habits through February
-- ============================================================================

('S001_20240915_1', 'S001', 'Organization', 'Executive Function', 'Developing', 0.72,
'Eva has organizational tools (planner) but struggles to use them efficiently. She needed time to locate information when called upon during discussion, indicating developing organization skills.',
'She had good ideas but struggled to organize her notes and needed time to find information in her planner.',
1, 'v1.0', false),

('S001_20241115_2', 'S001', 'Organization', 'Executive Function', 'Developing', 0.76,
'Eva continues to work on organization. Materials were spread out and she had to pause to locate discussion questions. Shows gradual improvement with slight increase in efficiency.',
'Her materials were spread out and she had to pause to locate her discussion questions, but showing gradual improvement.',
2, 'v1.0', false),

('S001_20250115_3', 'S001', 'Organization', 'Executive Function', 'Proficient', 0.84,
'Breakthrough! Eva demonstrated proficient organization with color-coded agenda and organized materials. She quickly accessed all needed information without hesitation - major progress.',
'She facilitated meeting with color-coded agenda and organized materials. She quickly accessed all needed information without hesitation!',
3, 'v1.0', false),

('S001_20250215_4', 'S001', 'Organization', 'Executive Function', 'Advanced', 0.91,
'Eva now consistently demonstrates advanced organization. All materials tabbed, timeline clearly displayed, smooth transitions. She has internalized organizational systems and maintains them independently.',
'Presented with exceptional organization - all materials tabbed, timeline clearly displayed, and smooth transitions. Maintains new habits consistently.',
4, 'v1.0', false),

-- ============================================================================
-- S002 (Lucas) - Social Awareness: Developing → Developing → Proficient → Proficient
-- Story: Struggles with reading social cues, shows gradual improvement,
-- reaches proficiency in January and maintains it
-- ============================================================================

('S002_20240916_1', 'S002', 'Social Awareness', 'Social-Emotional', 'Developing', 0.68,
'Lucas missed social cues when teammates seemed overwhelmed by his detailed agenda. He needs development in reading group dynamics and responding to others'' emotional states.',
'Lucas missed social cues when teammates seemed overwhelmed by his detailed agenda. Needs development in reading group dynamics.',
1, 'v1.0', false),

('S002_20241116_2', 'S002', 'Social Awareness', 'Social-Emotional', 'Developing', 0.73,
'Peers noted Lucas is starting to check in more with team members, though still sometimes pushes his plans without reading the room. Shows social awareness is developing with slight progress.',
'He is starting to check in more with team members, though still sometimes pushes his plans without reading the room.',
2, 'v1.0', false),

('S002_20250116_3', 'S002', 'Social Awareness', 'Social-Emotional', 'Proficient', 0.82,
'Clear progress! Lucas successfully picked up on Jordan''s hesitation and paused to invite their input. Demonstrates proficient social awareness - noticing and responding to social cues appropriately.',
'Lucas picked up on Jordan''s hesitation, pausing to invite their input. Clear progress in noticing and responding to social cues!',
3, 'v1.0', false),

('S002_20250216_4', 'S002', 'Social Awareness', 'Social-Emotional', 'Proficient', 0.86,
'Lucas maintains proficient social awareness - regularly checks team understanding, adjusts pace based on group energy, and creates inclusive environment. Consistently demonstrates these skills.',
'Regularly checked team members'' understanding, adjusted pace based on group energy, and created inclusive environment throughout project.',
4, 'v1.0', false),

-- ============================================================================
-- S003 (Pat) - Communication: Proficient → Proficient → Advanced → Advanced
-- Story: Already communicates well, builds confidence and sophistication,
-- reaches advanced level and maintains it
-- ============================================================================

('S003_20240917_1', 'S003', 'Communication', 'Social-Emotional', 'Proficient', 0.78,
'Pat communicates clearly with thoughtful questions during discussion. Ideas are well-expressed, though sometimes hesitant to elaborate. Shows proficient communication skills.',
'Pat asked thoughtful clarifying questions. Communication is clear and ideas are well-expressed, though sometimes hesitant to elaborate.',
1, 'v1.0', false),

('S003_20241117_2', 'S003', 'Communication', 'Social-Emotional', 'Proficient', 0.82,
'Pat presented book review with good structure and clear speaking. Communication skills are solid with supporting evidence. Building confidence in expressing complex ideas to larger audience.',
'Presented with good structure. Spoke clearly with supporting evidence. Building confidence in expressing complex ideas.',
2, 'v1.0', false),

('S003_20250117_3', 'S003', 'Communication', 'Social-Emotional', 'Advanced', 0.87,
'Pat demonstrates advanced communication - articulated nuanced position in debate, responded to counterarguments effectively, and helped others understand complex issues. Significant growth in sophistication.',
'Articulated nuanced position, responded to counterarguments effectively, and helped others understand complex issues.',
3, 'v1.0', false),

('S003_20250217_4', 'S003', 'Communication', 'Social-Emotional', 'Advanced', 0.90,
'Exceptional communication skills maintained - clear thesis, compelling evidence, engaging delivery to panel, and sophisticated responses to questions. Consistently demonstrates advanced mastery.',
'Clear thesis, compelling evidence, engaging delivery, and sophisticated response to questions.',
4, 'v1.0', false),

-- ============================================================================
-- S004 (Mia) - Task Initiation: Developing → Developing → Proficient → Proficient
-- Story: Needs prompts to start tasks, shows awareness and attempts,
-- achieves independence in January and maintains it
-- ============================================================================

('S004_20240918_1', 'S004', 'Task Initiation', 'Executive Function', 'Developing', 0.67,
'Mia needed multiple prompts to begin tasks. She waited for explicit instructions before starting each step. Task initiation skills are developing and need continued support.',
'Needed multiple prompts to begin her portion of the task. Waited for explicit instructions before starting each step.',
1, 'v1.0', false),

('S004_20241118_2', 'S004', 'Task Initiation', 'Executive Function', 'Developing', 0.71,
'Mia shows awareness of needing reminders to start tasks and is attempting to self-start occasionally. Still requires some prompting but making gradual progress in task initiation.',
'Acknowledged needing reminders but showed awareness of the issue. Still requires some prompting but attempting to self-start occasionally.',
2, 'v1.0', false),

('S004_20250118_3', 'S004', 'Task Initiation', 'Executive Function', 'Proficient', 0.79,
'Notable improvement! Mia began independent research with minimal prompting - asked clarifying questions then dove in. She is starting to take initiative more consistently, reaching proficiency.',
'Began independent research project with minimal prompting. Asked clarifying questions then dove in. Taking initiative more consistently!',
3, 'v1.0', false),

('S004_20250218_4', 'S004', 'Task Initiation', 'Executive Function', 'Proficient', 0.84,
'Mia independently initiated all project phases, created her own timeline, and began tasks without reminders. Task initiation has become a strength - maintains proficient self-direction.',
'Independently initiated all project phases, created her own timeline, and began tasks without waiting for reminders.',
4, 'v1.0', false);
