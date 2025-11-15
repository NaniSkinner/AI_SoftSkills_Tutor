-- ============================================================================
-- SEED ASSESSMENTS - Sample pre-generated assessments for demo
-- ============================================================================
-- This file contains realistic sample assessments for the 4 seed students
-- across all 17 Executive Function and SEL skills.
-- These assessments are pre-generated to avoid OpenAI API costs on deployment.
-- ============================================================================

-- First, insert sample data entries that these assessments are based on
INSERT INTO data_entries (id, student_id, teacher_id, type, date, content, metadata) VALUES
('S001_20250815_1', 'S001', 'T001', 'Group Discussion Transcript', '2025-08-15', 'Student Eva actively participated in literature circle discussion about The Giver, demonstrating strong communication and social awareness skills.', '{}'),
('S002_20250816_1', 'S002', 'T001', 'Group Discussion Transcript', '2025-08-16', 'Student Lucas led a highly organized discussion with color-coded questions, showing exceptional planning and organization skills.', '{}'),
('S001_20250818_1', 'S001', 'T001', 'Reflection Journal', '2025-08-18', 'Eva reflected on her leadership role in the group project, showing self-awareness about her communication strengths and organization challenges.', '{}'),
('S003_20250916_1', 'S003', 'T002', 'Group Discussion Transcript', '2025-09-16', 'Student Pat participated thoughtfully in discussion, asking clarifying questions and showing cognitive flexibility.', '{}')
ON CONFLICT (id) DO NOTHING;

-- Sample Assessments for S001 (Eva)
-- Eva shows strength in Communication, Social Awareness, and Relationship Skills
-- Still developing in Planning, Organization, and Task Initiation
INSERT INTO assessments (
    data_entry_id, student_id, skill_name, skill_category,
    level, confidence_score, justification, source_quote,
    data_point_count, rubric_version, corrected
) VALUES
-- Executive Function Skills for S001
('S001_20250815_1', 'S001', 'Planning & Prioritization', 'Executive Function', 2, 0.75,
'Eva had a discussion plan but needed a moment to organize when Lucas suggested creating a shared document. She recovered quickly but the execution could be smoother.',
'Um... *pauses, looks at planner* Let me check my notes. *Flips through planner, slightly flustered* I was supposed to organize this better.',
1, 'v1.0', false),

('S001_20250815_1', 'S001', 'Organization', 'Executive Function', 2, 0.72,
'Eva is using her planner, which shows she has organizational tools, but struggled to access the information smoothly when needed during the discussion.',
'Give me a second. *Flips through planner, slightly flustered*',
1, 'v1.0', false),

('S001_20250815_1', 'S001', 'Task Initiation', 'Executive Function', 3, 0.80,
'Eva took the initiative as discussion leader and started the conversation promptly with a clear opening question about the theme.',
'Okay, so I thought we could start with the theme of sameness in the community.',
1, 'v1.0', false),

('S001_20250815_1', 'S001', 'Time Management', 'Executive Function', 2, 0.65,
'Limited evidence, but Eva did need extra time to organize her thoughts mid-discussion, suggesting time management skills are still developing.',
'*pauses, looks at planner* Let me check my notes.',
1, 'v1.0', false),

('S001_20250815_1', 'S001', 'Working Memory', 'Executive Function', 3, 0.78,
'Eva remembered previous discussion points and connected them to new ideas, showing good retention of information.',
'Ms. Rodriguez said yesterday that this book is about utopias and dystopias.',
1, 'v1.0', false),

('S001_20250815_1', 'S001', 'Metacognition', 'Executive Function', 3, 0.82,
'Eva demonstrated awareness of her own learning by reflecting on what she hadn''t considered before when Jordan contributed.',
'That''s a really good observation! I didn''t even think about connecting that to the sameness theme.',
1, 'v1.0', false),

('S001_20250815_1', 'S001', 'Inhibitory Control', 'Executive Function', 3, 0.75,
'Eva maintained focus on the discussion and resisted distractions, keeping the group on task.',
'Let''s keep going. What else?',
1, 'v1.0', false),

('S001_20250815_1', 'S001', 'Cognitive Flexibility', 'Executive Function', 3, 0.85,
'Eva easily adapted when Jordan brought up an unexpected connection, building on it rather than dismissing it.',
'Good thinking! That''s, like, the deeper question. It''s not just WHAT they control, but WHY.',
1, 'v1.0', false),

-- SEL Skills for S001
('S001_20250815_1', 'S001', 'Communication', 'Social-Emotional', 4, 0.90,
'Eva articulates ideas clearly, builds on others'' contributions, and uses persuasive language. She makes thoughtful connections between text and theme.',
'Yeah, and I think it shows that even in a super controlled community, people still have emotions and curiosity. *Builds on Lucas''s point*',
1, 'v1.0', false),

('S001_20250815_1', 'S001', 'Social Awareness', 'Social-Emotional', 4, 0.88,
'Eva actively noticed Jordan''s hesitation and made deliberate effort to include them, showing strong awareness of social dynamics.',
'Jordan, did you notice anything in the chapter that stood out to you? *Makes eye contact and leans forward slightly*',
1, 'v1.0', false),

('S001_20250815_1', 'S001', 'Relationship Skills', 'Social-Emotional', 4, 0.87,
'Eva created an inclusive, collaborative environment by validating contributions and using supportive language.',
'That''s a really good observation! I didn''t even think about connecting that to the sameness theme. *Validates Jordan''s contribution*',
1, 'v1.0', false),

('S001_20250815_1', 'S001', 'Self-Awareness', 'Social-Emotional', 3, 0.76,
'Eva recognized her preparation could have been better when she needed time to check her planner.',
'I was supposed to organize this better. Give me a second.',
1, 'v1.0', false),

('S001_20250815_1', 'S001', 'Self-Management', 'Social-Emotional', 3, 0.80,
'Eva recovered well from a moment of being flustered, maintaining composure and continuing to lead effectively.',
'*Finds the page* Okay, so far we have: names are secret until the ceremony...',
1, 'v1.0', false),

('S001_20250815_1', 'S001', 'Decision Making', 'Social-Emotional', 3, 0.77,
'Eva made the decision to proceed with Lucas''s shared document idea after brief consideration.',
'Lucas, yeah, go ahead and start the doc. Can you share it with all of us?',
1, 'v1.0', false),

('S001_20250815_1', 'S001', 'Growth Mindset', 'Social-Emotional', 3, 0.81,
'Eva expressed interest in learning Lucas''s organizational system, showing openness to improvement.',
'That''s really smart. I should do that.',
1, 'v1.0', false),

('S001_20250815_1', 'S001', 'Stress Management', 'Social-Emotional', 3, 0.74,
'Eva handled the unexpected suggestion calmly despite being slightly flustered initially.',
'Um... *pauses, looks at planner* Give me a second.',
1, 'v1.0', false),

('S001_20250815_1', 'S001', 'Collaboration', 'Social-Emotional', 4, 0.89,
'Eva facilitated group collaboration effectively, ensuring all voices were heard and ideas were built upon.',
'Jordan, did you notice anything? Amir, what do you think?',
1, 'v1.0', false),

-- Sample Assessments for S002 (Lucas)
-- Lucas excels in Organization, Planning, and Executive Function skills
-- Still developing in Social Awareness, Cognitive Flexibility, and Relationship Skills
('S002_20250816_1', 'S002', 'Planning & Prioritization', 'Executive Function', 4, 0.92,
'Lucas prepared a comprehensive, time-managed discussion plan with categorized questions, demonstrating advanced planning skills.',
'I made a list of discussion questions last night. I organized them by theme. We have 25 minutes, so that''s about two minutes per question if we''re efficient.',
1, 'v1.0', false),

('S002_20250816_1', 'S002', 'Organization', 'Executive Function', 5, 0.95,
'Lucas demonstrated exceptional organization with color-coded questions, tabbed book pages, and systematic materials management.',
'I color-coded them. Blue is for community rules, green is for emotion and choice, and yellow is for character development.',
1, 'v1.0', false),

('S002_20250816_1', 'S002', 'Task Initiation', 'Executive Function', 4, 0.90,
'Lucas prepared thoroughly in advance without prompting, showing strong task initiation.',
'I made a list of discussion questions last night.',
1, 'v1.0', false),

('S002_20250816_1', 'S002', 'Time Management', 'Executive Function', 4, 0.88,
'Lucas calculated time allocation for the discussion, showing awareness of time constraints.',
'We have 25 minutes, so that''s about two minutes per question if we''re efficient.',
1, 'v1.0', false),

('S002_20250816_1', 'S002', 'Working Memory', 'Executive Function', 4, 0.87,
'Lucas recalled exact page numbers and quotes, demonstrating excellent information retention.',
'The text supports that on page 47 where it says— *flips to exact page*—"the community is carefully designed to eliminate pain."',
1, 'v1.0', false),

('S002_20250816_1', 'S002', 'Metacognition', 'Executive Function', 3, 0.76,
'Lucas showed some awareness of his learning preferences but limited reflection on effectiveness.',
'I just... I like having a plan. It helps me focus.',
1, 'v1.0', false),

('S002_20250816_1', 'S002', 'Inhibitory Control', 'Executive Function', 4, 0.89,
'Lucas stayed focused on the discussion goals despite social pressures and distractions.',
'We should probably start with the blue ones since Chapter 4 introduces more rules.',
1, 'v1.0', false),

('S002_20250816_1', 'S002', 'Cognitive Flexibility', 'Executive Function', 2, 0.70,
'Lucas struggled when the discussion deviated from his prepared questions, showing difficulty with spontaneity.',
'That wasn''t one of my prepared questions, but... *hesitates* ...okay, that is important.',
1, 'v1.0', false),

('S002_20250816_1', 'S002', 'Communication', 'Social-Emotional', 3, 0.74,
'Lucas communicated clearly and precisely but lacked warmth and spontaneity in his delivery.',
'That''s question B3. Good choice. It connects to the theme we discussed yesterday.',
1, 'v1.0', false),

('S002_20250816_1', 'S002', 'Social Awareness', 'Social-Emotional', 2, 0.68,
'Lucas didn''t immediately pick up on social cues when Amir seemed overwhelmed by the number of questions.',
'This is a lot. Do we have to answer all of them? [Amir''s concern not initially addressed by Lucas]',
1, 'v1.0', false),

('S002_20250816_1', 'S002', 'Relationship Skills', 'Social-Emotional', 2, 0.71,
'Lucas offered to help Eva but interactions felt somewhat transactional rather than warm.',
'I could show you my system if you want. I use different colored tabs for different themes.',
1, 'v1.0', false),

('S002_20250816_1', 'S002', 'Self-Awareness', 'Social-Emotional', 3, 0.79,
'Lucas demonstrated awareness of his need for structure and planning.',
'I just... I like having a plan. It helps me focus.',
1, 'v1.0', false),

('S002_20250816_1', 'S002', 'Self-Management', 'Social-Emotional', 3, 0.77,
'Lucas managed discomfort when the discussion changed direction, adapting after brief hesitation.',
'*Nods stiffly* Okay. Um... Jordan, which question do you think is most interesting?',
1, 'v1.0', false),

('S002_20250816_1', 'S002', 'Decision Making', 'Social-Emotional', 3, 0.75,
'Lucas made decisions about discussion flow but initially resisted deviating from his plan.',
'But then we might not cover everything important. [Eventually adapted after teacher guidance]',
1, 'v1.0', false),

('S002_20250816_1', 'S002', 'Growth Mindset', 'Social-Emotional', 3, 0.78,
'Lucas showed willingness to adapt his approach when guided by the teacher.',
'*Nods stiffly* Okay.',
1, 'v1.0', false),

('S002_20250816_1', 'S002', 'Stress Management', 'Social-Emotional', 3, 0.76,
'Lucas appeared uncomfortable when things didn''t go as planned but maintained composure.',
'*Looks down, slightly uncomfortable* I just... I like having a plan.',
1, 'v1.0', false),

('S002_20250816_1', 'S002', 'Collaboration', 'Social-Emotional', 3, 0.73,
'Lucas shared prepared materials and worked with the group but preferred structured collaboration.',
'Okay, I made a list of discussion questions. Everyone gets a copy.',
1, 'v1.0', false);

-- Note: For a full demo, you would add similar assessments for S003 (Pat) and S004 (Mia)
-- This provides ~34 sample assessments across 2 students for demonstration purposes
