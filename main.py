from pawpal_system import Owner, Pet, Task

# --- Setup ---
owner = Owner(owner_name="Jordan", owner_id="owner_001", preferences={"morning_priority": True})

mochi = Pet(pet_name="Mochi", owner_name="Jordan", pet_id="pet_001")
bella = Pet(pet_name="Bella", owner_name="Jordan", pet_id="pet_002")

owner.pets.append(mochi)
owner.pets.append(bella)

# --- Tasks added OUT OF ORDER intentionally ---
bath = Task(
    title="Bath",
    pet_name="Mochi",
    start_time=11,
    duration=20,
    frequency="weekly",
    constraints=["before noon"],
)

evening_walk = Task(
    title="Evening Walk",
    pet_name="Bella",
    start_time=18,
    duration=30,
    frequency="daily",
)

feeding = Task(
    title="Feeding",
    pet_name="Bella",
    start_time=9,
    duration=15,
    frequency="daily",
)

morning_walk = Task(
    title="Morning Walk",
    pet_name="Mochi",
    start_time=8,
    duration=30,
    frequency="daily",
    constraints=["morning only"],
)

vet_visit = Task(
    title="Vet Visit",
    pet_name="Mochi",
    start_time=14,
    duration=60,
    frequency="monthly",
)

owner.add_task(bath)        # 11am — added first
owner.add_task(evening_walk)  # 6pm
owner.add_task(feeding)     # 9am
owner.add_task(morning_walk)  # 8am — added last
owner.add_task(vet_visit)   # 2pm

# Mark one task complete to test filtering
owner.complete_task(morning_walk)

scheduler = owner.scheduler

# --- Sort by time ---
print("=" * 40)
print("  SORTED BY TIME (earliest first)")
print("=" * 40)
for task in scheduler.sort_by_time():
    status = "done" if task.completed else "pending"
    print(f"  {task.start_time:02d}:00 — {task.title} ({task.pet_name}) [{status}]")

print()

# --- Filter: pending only ---
print("=" * 40)
print("  PENDING TASKS ONLY")
print("=" * 40)
for task in scheduler.filter_tasks(completed=False):
    print(f"  {task.title} ({task.pet_name})")

print()

# --- Filter: completed only ---
print("=" * 40)
print("  COMPLETED TASKS ONLY")
print("=" * 40)
for task in scheduler.filter_tasks(completed=True):
    print(f"  {task.title} ({task.pet_name})")

print()

# --- Filter: by pet name ---
print("=" * 40)
print("  MOCHI'S TASKS ONLY")
print("=" * 40)
for task in scheduler.filter_tasks(pet_name="Mochi"):
    status = "done" if task.completed else "pending"
    print(f"  {task.title} at {task.start_time:02d}:00 [{status}]")

print()

# --- Filter: combined (Bella's pending tasks) ---
print("=" * 40)
print("  BELLA'S PENDING TASKS")
print("=" * 40)
for task in scheduler.filter_tasks(completed=False, pet_name="Bella"):
    print(f"  {task.title} at {task.start_time:02d}:00")
