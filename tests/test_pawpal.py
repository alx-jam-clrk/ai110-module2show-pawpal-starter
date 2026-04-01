import pytest
from pawpal_system import Owner, Pet, Task


# --- Shared fixtures ---

@pytest.fixture
def owner():
    o = Owner(owner_name="Jordan", owner_id="owner_001")
    o.pets.append(Pet(pet_name="Mochi", owner_name="Jordan", pet_id="pet_001"))
    return o

@pytest.fixture
def task():
    return Task(title="Morning Walk", pet_name="Mochi", start_time=8, duration=30, frequency="daily")


# --- complete_task() tests ---

def test_task_starts_incomplete(task):
    """A newly created task should have completed=False by default."""
    assert task.completed is False

def test_complete_task_changes_status(owner, task):
    """complete_task() should set task.completed to True."""
    owner.add_task(task)
    owner.complete_task(task)
    assert task.completed is True

def test_complete_task_does_not_affect_other_tasks(owner):
    """Completing one task should not change the status of other tasks."""
    task1 = Task(title="Morning Walk", pet_name="Mochi", start_time=8, duration=30, frequency="daily")
    task2 = Task(title="Feeding", pet_name="Mochi", start_time=10, duration=15, frequency="daily")
    owner.add_task(task1)
    owner.add_task(task2)
    owner.complete_task(task1)
    assert task2.completed is False


# --- add_task() pet task count tests ---

def test_add_task_increases_pet_task_count(owner, task):
    """Adding a task should increase the matching pet's task count by 1."""
    mochi = owner.pets[0]
    before = len(mochi.tasks)
    owner.add_task(task)
    assert len(mochi.tasks) == before + 1

def test_add_multiple_tasks_increases_count_correctly(owner):
    """Adding three tasks to the same pet should result in exactly 3 tasks."""
    tasks = [
        Task(title="Walk",    pet_name="Mochi", start_time=8,  duration=30, frequency="daily"),
        Task(title="Feeding", pet_name="Mochi", start_time=10, duration=15, frequency="daily"),
        Task(title="Bath",    pet_name="Mochi", start_time=14, duration=20, frequency="weekly"),
    ]
    for t in tasks:
        owner.add_task(t)
    assert len(owner.pets[0].tasks) == 3

def test_add_task_only_affects_matching_pet(owner):
    """A task added for one pet should not appear in another pet's task list."""
    owner.pets.append(Pet(pet_name="Bella", owner_name="Jordan", pet_id="pet_002"))
    task = Task(title="Walk", pet_name="Mochi", start_time=8, duration=30, frequency="daily")
    owner.add_task(task)
    bella = next(p for p in owner.pets if p.pet_name == "Bella")
    assert len(bella.tasks) == 0

def test_add_task_unknown_pet_raises_error(owner):
    """Adding a task for a pet that doesn't exist should raise a ValueError."""
    task = Task(title="Walk", pet_name="Unknown", start_time=8, duration=30, frequency="daily")
    with pytest.raises(ValueError):
        owner.add_task(task)


# --- sort_by_time() tests ---

def test_sort_by_time_returns_chronological_order(owner):
    """sort_by_time() should return tasks ordered from earliest to latest start_time."""
    tasks = [
        Task(title="Bath",    pet_name="Mochi", start_time=14, duration=20, frequency="weekly"),
        Task(title="Feeding", pet_name="Mochi", start_time=10, duration=15, frequency="daily"),
        Task(title="Walk",    pet_name="Mochi", start_time=8,  duration=30, frequency="daily"),
    ]
    for t in tasks:
        owner.add_task(t)
    sorted_tasks = owner.scheduler.sort_by_time()
    start_times = [t.start_time for t in sorted_tasks]
    assert start_times == sorted(start_times)

def test_sort_by_time_single_task(owner, task):
    """sort_by_time() with one task should return a list containing just that task."""
    owner.add_task(task)
    assert owner.scheduler.sort_by_time() == [task]

def test_sort_by_time_empty_scheduler():
    """sort_by_time() on an empty scheduler should return an empty list."""
    from pawpal_system import Scheduler
    s = Scheduler(owner_name="Jordan")
    assert s.sort_by_time() == []


# --- Recurrence Logic tests ---

def test_complete_daily_task_adds_new_task(owner, task):
    """Completing a daily task should add one new pending task to the scheduler."""
    owner.add_task(task)
    count_before = len(owner.scheduler.tasks)
    owner.complete_task(task)
    assert len(owner.scheduler.tasks) == count_before + 1

def test_next_occurrence_is_pending(owner, task):
    """The task added after completing a daily task should have completed=False."""
    owner.add_task(task)
    owner.complete_task(task)
    new_task = owner.scheduler.tasks[-1]
    assert new_task.completed is False

def test_next_occurrence_preserves_title_and_time(owner, task):
    """The next occurrence should have the same title and start_time as the original."""
    owner.add_task(task)
    owner.complete_task(task)
    new_task = owner.scheduler.tasks[-1]
    assert new_task.title == task.title
    assert new_task.start_time == task.start_time


# --- Conflict Detection tests ---

def test_verify_schedule_detects_overlap(owner):
    """verify_schedule() should return False when two tasks for the same pet overlap."""
    # Walk starts at 8 and lasts 60 min (ends at 9); Feeding starts at 8 — clear overlap
    task1 = Task(title="Walk",    pet_name="Mochi", start_time=8, duration=60, frequency="daily")
    task2 = Task(title="Feeding", pet_name="Mochi", start_time=8, duration=15, frequency="daily")
    owner.add_task(task1)
    owner.add_task(task2)
    assert owner.scheduler.verify_schedule() is False

def test_verify_schedule_no_overlap(owner):
    """verify_schedule() should return True when tasks for the same pet do not overlap."""
    # Walk ends at 8:30 (8 + 30 min); Feeding starts at 10 — no overlap
    task1 = Task(title="Walk",    pet_name="Mochi", start_time=8,  duration=30, frequency="daily")
    task2 = Task(title="Feeding", pet_name="Mochi", start_time=10, duration=15, frequency="daily")
    owner.add_task(task1)
    owner.add_task(task2)
    assert owner.scheduler.verify_schedule() is True

def test_verify_schedule_different_pets_same_time(owner):
    """Tasks at the same time for different pets should not count as a conflict."""
    owner.pets.append(Pet(pet_name="Bella", owner_name="Jordan", pet_id="pet_002"))
    task1 = Task(title="Walk", pet_name="Mochi", start_time=8, duration=60, frequency="daily")
    task2 = Task(title="Walk", pet_name="Bella", start_time=8, duration=60, frequency="daily")
    owner.add_task(task1)
    owner.add_task(task2)
    assert owner.scheduler.verify_schedule() is True
