# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smart Scheduling Features

### Sorting

Tasks can be sorted by start time using `Scheduler.sort_by_time()`, which returns all scheduled tasks ordered from earliest to latest regardless of the order they were added.

```python
for task in scheduler.sort_by_time():
    print(task.title, task.start_time)
```

### Filtering

Tasks can be filtered by completion status, pet name, or both using `Scheduler.filter_tasks()`. All parameters are optional and can be combined.

```python
scheduler.filter_tasks(completed=False)           # pending tasks only
scheduler.filter_tasks(pet_name="Mochi")          # one pet's tasks
scheduler.filter_tasks(completed=True, pet_name="Bella")  # combined
```

### Conflict Detection

`Scheduler.verify_schedule()` checks whether any pet has overlapping tasks. Tasks are grouped by pet, sorted by start time, and each consecutive pair is checked for overlap based on start time and duration. `Owner.build_schedule()` calls this automatically and raises a `ValueError` if a conflict is found.

```python
try:
    owner.build_schedule()
except ValueError as e:
    print(f"Warning: {e}")
```

### Recurring Tasks

When a task is marked complete via `Owner.complete_task()`, a fresh copy is automatically added to the scheduler for daily, weekly, and monthly tasks — keeping the schedule populated without manual re-entry.

```python
owner.complete_task(walk)  # walk is done; next occurrence queued automatically
```

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
