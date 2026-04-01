# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
  
  The **three core actions** that a user must have
    - set tasks/constraints
    - build schedule
    - add/edit basic info & preferences

- What classes did you include, and what responsibilities did you assign to each?

  I included the Owner, Pet, Task, and Scheduler classes. The Owner Class is the "master" class with the ability to use the Scheduler, manage Task, and own the Pet. The Scheduler schedules Task, and Task is assigned to Pet.


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
  
  One of the major changes I made during implementation were the Scheduler attributes. Before, I passed pet_names, owner_name, and tasks are passed and stored as independent attributes. Now, owner_name is the only attribute being passed and stored, where tasks is initialized as an empty list, and pet_names is a computed property derived from tasks.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

  My scheduler prioritizes time and preferences

- How did you decide which constraints mattered most?

  Time and preferences in my opinion are more important than priority because a task can be somewhat implicitly prioritized based on the time in which it was scheduled. Time and preferences are explicit constraints that must be addressed to for the task to be done successfully

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

  One tradeoff my schedular makes is by using the dataclass decorators built-in replace function in schedule_next_occurence(). Although its way easier to read, you lose the meaning of what the line is doing (overwriting a Task instance with a new Task)

- Why is that tradeoff reasonable for this scenario?

  This tradeoff makes sense because the code is already a little cluttered already, so the cleaner the code is, the better

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

  I used Claude Code ot help me do all of the above (design, brainstorm, debug, and refactor!)

- What kinds of prompts or questions were most helpful?

  The most helpful prompt I used was when I asked it to ask me clarifying questions until we both understood the what must be implemented

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

  When I was creating my core implementation for my methods, I was given a HUGE for-loop to verify the schedule has no conflicts, but it was so unreadable that I asked it to refactor into smaller helper functions.

- How did you evaluate or verify what the AI suggested?

  First I asked myself does it makes sense? Then I ask, more importantly, can I understand it from a glance?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?

 3/5 stars

- What edge cases would you test next if you had more time?

I would try to fix the recurring task / pet.tasks sync bug, since they both have their own independent tasks lists

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
