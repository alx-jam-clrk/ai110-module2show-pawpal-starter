from pawpal_system import Owner, Pet, Task

# --- Setup ---
owner = Owner(owner_name="Jordan", owner_id="owner_001", preferences={"morning_priority": True})

mochi = Pet(pet_name="Mochi", owner_name="Jordan", pet_id="pet_001")
bella = Pet(pet_name="Bella", owner_name="Jordan", pet_id="pet_002")

owner.pets.append(mochi)
owner.pets.append(bella)

# --- Tasks ---
morning_walk = Task(
    title="Morning Walk",
    pet_name="Mochi",
    start_time=8,
    duration=30,
    frequency="daily",
    constraints=["morning only"],
)

feeding = Task(
    title="Feeding",
    pet_name="Bella",
    start_time=9,
    duration=15,
    frequency="daily",
)

bath = Task(
    title="Bath",
    pet_name="Mochi",
    start_time=11,
    duration=20,
    frequency="weekly",
    constraints=["before noon"],
)

owner.add_task(morning_walk)
owner.add_task(feeding)
owner.add_task(bath)

# --- Schedule ---
owner.build_schedule()

print("=" * 40)
print("        TODAY'S SCHEDULE")
print("=" * 40)
print(owner.view_schedule())
print()
print("=" * 40)
print("        SCHEDULE EXPLANATION")
print("=" * 40)
print(owner.scheduler.explain_schedule(preferences=owner.preferences))
