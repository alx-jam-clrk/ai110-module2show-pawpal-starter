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
