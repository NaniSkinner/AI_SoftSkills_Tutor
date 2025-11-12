# Shard 2: Mock Data Generation Engine

**Owner:** Content/Data Engineer
**Estimated Time:** 2 days
**Dependencies:** Shard 1 (Database schema)
**Priority:** P0 (Critical Path)

---

## Objective

Generate 76 realistic data entries (transcripts, reflections, notes) for 4 students over 3 months, incorporating authentic middle school behaviors aligned with the rubric. Use kind, growth-oriented language throughout.

---

## Inputs

1. [Docs/Rubric.md](../Docs/Rubric.md) - Behavioral indicators for all 17 skills
2. [Docs/Curriculum.md](../Docs/Curriculum.md) - Developmental context for middle schoolers
3. [Docs/PRD.md](../Docs/PRD.md) - Section 3: Mock Data Specifications
4. Student archetypes from PRD Section 3.1

---

## Student Growth Arcs

### Eva (S001): The Steady Climber
**Trajectory:**
- **Month 1 (Aug):** Developing in most SEL skills, Emerging in EF (organization, planning)
- **Month 2 (Sep):** Proficient in Communication & Collaboration, Growing in Self-Management
- **Month 3 (Oct):** Proficient in most SEL, Developing→Proficient in EF skills

**Key Behaviors:**
- Consistently shows empathy and active listening
- Gradually improves time management and task initiation
- Uses coping strategies more independently over time

### Lucas (S002): The Executive Function Champion
**Trajectory:**
- **Month 1:** Proficient in SEL (self-aware, manages emotions well), Emerging in Planning/Organization
- **Month 2:** Breakthrough in Organization (discovers planner system)
- **Month 3:** Proficient in Task Initiation, Planning & Prioritization

**Key Behaviors:**
- Emotionally mature from start
- Struggles with materials management initially
- Dramatic improvement after teacher scaffolding in September

### Pat (S003): The Late Bloomer
**Trajectory:**
- **Month 1:** Emerging in Collaboration (reserved), Developing in Communication
- **Month 2:** Stable, slight progress
- **Month 3:** Rapid acceleration - Proficient in Collaboration, Critical Thinking, Social Awareness

**Key Behaviors:**
- Quiet, observant in early discussions
- Needs invitation to share ideas
- Finds voice through project work in October

### Mia (S004): The Well-Rounded Leader
**Trajectory:**
- **Month 1:** Proficient in most skills, already models peer mentoring
- **Month 2:** Achieves Advanced in Communication, Collaboration, Social Awareness
- **Month 3:** Advanced in 5+ skills, natural facilitator

**Key Behaviors:**
- Naturally inclusive, invites quieter peers
- Synthesizes ideas across group discussions
- Demonstrates metacognition in reflections

---

## Data Type Templates

### 1. Group Discussion Transcript

**Template Structure:**
```markdown
# Group Discussion: [Topic]

**Date:** [Date]
**Participants:** [Names with IDs]
**Duration:** [X] minutes
**Context:** [Class/project context]

---

**[Teacher Name]:** "[Setup prompt]"

**[Student 1]:** "[Response showing specific skill level]"

**[Student 2]:** _[action cue]_ "[Response]"

[Continue dialogue showing observable behaviors]

---

**Teacher Observation:** [Optional summary note]
```

**Skills to Target:**
- Collaboration, Communication, Relationship Skills
- Social Awareness (empathy, turn-taking)
- Cognitive Flexibility (adapting ideas)

**Language Guidelines:**
- Use growth-oriented descriptors: "beginning to...", "showing progress in...", "developing ability to..."
- Avoid deficit language: Instead of "fails to listen" → "working on maintaining focus when others speak"
- Show scaffolding: teacher prompts, peer support

### 2. Reflection Journal

**Template Structure:**
```markdown
# Weekly Reflection: [Week of X]

**Student:** [Name]
**Date:** [Date]
**Prompt:** [Teacher prompt]

---

[Student's written reflection showing internal thought process]

**Teacher Comment:** [Optional growth-focused feedback]
```

**Skills to Target:**
- Self-Awareness, Self-Management
- Metacognition
- Responsible Decision-Making

### 3. Peer Tutoring Transcript

**Skills:** Social Awareness, Communication, Self-Management (patience)

### 4. Project Presentation Transcript

**Skills:** Communication, Critical Thinking, Creativity

### 5. Peer Feedback Form

**Format:** JSON
```json
{
  "from_student": "S001",
  "to_student": "S002",
  "date": "2025-09-05",
  "project": "Climate Change Solutions",
  "strengths": "Lucas had really creative ideas about food waste...",
  "growth_areas": "Maybe could listen more when others are talking...",
  "rating": {
    "collaboration": 4,
    "communication": 3
  }
}
```

### 6. Teacher Observation Note

**Format:** Markdown
**Skills:** All skills - holistic classroom observation

### 7. Parent Note

**Format:** Markdown (email-style)
**Skills:** Self-Management, Task Initiation, Organization (home context)

---

## Implementation Script

**File:** `scripts/generate_mock_data.py`

Key functions needed:
1. `generate_group_discussion(student, archetype, month, participants)` - Create realistic dialogue
2. `generate_reflection(student, archetype, month, prompt)` - Student voice reflection
3. `select_behavioral_markers(skill, level, archetype)` - Pick rubric-aligned behaviors
4. `ensure_growth_trajectory(student, month)` - Verify progression makes sense
5. `apply_kind_language_filter(text)` - Replace any deficit language

**Output:**
- `mock_data/config.json` - Master manifest
- Individual files in subdirectories (transcripts/, reflections/, etc.)

---

## Example: Eva Month 1 Group Discussion

**File:** `mock_data/transcripts/S001_group_disc_2025-08-15.md`

```markdown
# Group Discussion: Climate Change Solutions

**Date:** August 15, 2025
**Participants:** Eva (S001), Lucas (S002), Jordan (S003)
**Duration:** 45 minutes
**Context:** Science class collaborative project

---

**Ms. Rodriguez:** "Alright team, today you're going to discuss potential solutions to climate change. Remember to listen to each other and build on ideas. Eva, would you like to start us off?"

**Eva:** "Sure! Um, I was thinking we could focus on renewable energy? Like, solar panels and wind turbines."

**Lucas:** _interrupts_ "That's boring! Everyone talks about that. We should do something about stopping people from wasting food."

**Eva:** _pauses, then responds calmly_ "I hear you, Lucas. Food waste is definitely important. Maybe we could look at both? They're kind of connected—like, food production uses a lot of energy."

[SKILL MARKER: Social Awareness - Proficient level. Eva recognizes Lucas's frustration and validates his idea while maintaining her own perspective]

**Lucas:** "Oh... I didn't think about that. Yeah, okay."

**Jordan:** _quietly_ "I also read that transportation is a big problem..."

**Eva:** "Great point, Jordan! Can you tell us more about what you found?"

[SKILL MARKER: Relationship Skills - Proficient level. Eva actively invites quieter peer to participate]

**Jordan:** _sits up a bit_ "Well, um, like cars and planes produce a lot of carbon. Maybe we could talk about electric vehicles?"

**Eva:** "Yes! So we could do three solutions: renewable energy, food waste, and transportation. That covers a lot. Lucas, which one do you want to research?"

**Lucas:** "I'll do food waste. That's the one I care about most."

**Eva:** "Perfect. Jordan, transportation? And I'll take renewable energy. Should we meet again on Friday to share what we found?"

**Ms. Rodriguez:** _observing from nearby_ "Eva, I like how you're helping the group organize. Make sure everyone agrees on the Friday timeline."

**Eva:** "Oh, right! Jordan, Lucas, does Friday work for you both?"

[SKILL MARKER: Planning & Prioritization - Developing level. Eva creates a plan with teacher prompting]

**Jordan & Lucas:** _nod in agreement_

**Eva:** _pulls out planner_ "Okay, I'm writing it down: Friday, share research. We should each find at least three sources."

[SKILL MARKER: Organization - Developing level. Eva uses a planner with visible effort]

---

**Teacher Observation Note:**
Eva demonstrated strong collaboration and communication skills today. She naturally included Jordan and managed Lucas's initial interruption with maturity. She's beginning to take more initiative in planning group work, though she still benefits from reminders to check in with teammates. Her use of a planner is becoming more consistent - great progress from last month!
```

---

## Deliverables

### Required Files (76 total data entries)

**Per Student (19 entries × 4 students):**
- 3 group discussion transcripts
- 3 peer tutoring transcripts
- 3 project presentations
- 3 reflection journals
- 2 peer feedback forms
- 3 teacher observation notes
- 2 parent notes

### Master Configuration

**File:** `mock_data/config.json`

```json
{
  "project": {
    "name": "Flourish Skills Tracker MVP",
    "version": "1.0",
    "rubric_version": "1.0",
    "data_period": {
      "start": "2025-08-01",
      "end": "2025-10-31"
    }
  },
  "students": [
    {
      "id": "S001",
      "name": "Eva",
      "grade": 7,
      "teacher_id": "T001",
      "archetype": "steady_climber"
    }
    // ... S002, S003, S004
  ],
  "teachers": [
    {
      "id": "T001",
      "name": "Ms. Rodriguez",
      "email": "rodriguez@flourishschools.edu"
    },
    {
      "id": "T002",
      "name": "Mr. Thompson",
      "email": "thompson@flourishschools.edu"
    }
  ],
  "data_entries": [
    {
      "id": "DE001",
      "student_id": "S001",
      "teacher_id": "T001",
      "type": "group_discussion_transcript",
      "date": "2025-08-15",
      "file_path": "transcripts/S001_group_disc_2025-08-15.md",
      "metadata": {
        "duration_mins": 45,
        "participants": ["S001", "S002", "S003"],
        "topic": "Climate change solutions debate",
        "context": "Science class collaborative project"
      },
      "expected_skills": [
        {"skill": "Collaboration", "expected_level": "Proficient"},
        {"skill": "Social Awareness", "expected_level": "Proficient"},
        {"skill": "Planning & Prioritization", "expected_level": "Developing"}
      ]
    }
    // ... 75 more entries
  ]
}
```

**Note:** `expected_skills` field is for validation testing (Shard 8) - not used in production inference.

---

## Acceptance Criteria

- [ ] 76 data entries created (19 per student)
- [ ] All files use kind, growth-oriented language
- [ ] Each student shows clear progression over 3 months
- [ ] Behavioral markers align with rubric descriptors
- [ ] All 17 skills represented across the dataset
- [ ] config.json validates as proper JSON
- [ ] File naming convention followed: `{STUDENT_ID}_{TYPE}_{DATE}.md`
- [ ] Metadata includes context, participants, duration where applicable
- [ ] At least 3 entries per data type per student
- [ ] Authentic middle school voice (not overly formal)

---

## Testing

```bash
# Validate config.json structure
python scripts/validate_mock_data.py

# Count files
find mock_data -name "*.md" -o -name "*.json" | wc -l
# Expected: 77 (76 data files + 1 config.json)

# Check growth trajectories
python scripts/analyze_student_arcs.py
# Should show progression for each student across months
```

---

## Dependencies for Next Shards

- **Shard 3** (AI Inference): Needs at least 10 sample data entries to test prompt engineering
- **Shard 7** (Data Ingestion): Needs complete dataset + config.json

**Completion Checklist:**
- [ ] All transcripts written
- [ ] Reflections authentic to middle school voice
- [ ] Peer feedback constructive and realistic
- [ ] Teacher notes professional and growth-focused
- [ ] Parent notes show home context behaviors
- [ ] Config.json complete and valid
- [ ] Quality review: kind language verified
- [ ] Rubric alignment checked

**Sign-off:** _____________________
**Date:** _____________________
