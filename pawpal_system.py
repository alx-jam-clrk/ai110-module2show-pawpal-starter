from dataclasses import dataclass, field, replace
from typing import List


@dataclass
class Task:
    title: str
    pet_name: str            # string ref to avoid circular dependency with Pet
    start_time: int          # hour of day, e.g. 8 = 8am
    duration: int            # minutes
    frequency: str           # "daily" | "weekly" | "monthly"
                             # daily=7x/wk, weekly=1x/wk, monthly=~1x/4wks
    constraints: List[str] = field(default_factory=list)  # e.g. ["morning only", "before noon"]
    completed: bool = False


@dataclass
class Pet:
    pet_name: str
    owner_name: str
    pet_id: str
    tasks: List[Task] = field(default_factory=list)


class Scheduler:
    def __init__(self, owner_name: str):
        """Initialize the scheduler for a given owner with an empty task list.

        Args:
            owner_name: The name of the owner this scheduler belongs to.
        """
        self.owner_name: str = owner_name
        self.tasks: List[Task] = []

    #FIX???
    @property
    def pet_names(self) -> List[str]:
        """Return a deduplicated list of pet names from all scheduled tasks.

        Returns:
            A list of unique pet name strings derived from self.tasks.
        """
        return list({task.pet_name for task in self.tasks})

    def schedule_task(self, task: Task) -> None:
        """Add a task to the scheduler's task list.

        Args:
            task: The Task object to add to the schedule.
        """
        self.tasks.append(task)

    def schedule_next_occurrence(self, task: Task) -> Task:
        """Create and schedule the next occurrence of a recurring task.

        Args:
            task: A completed Task with a 'daily', 'weekly', or 'monthly' frequency.

        Returns:
            The new Task for the next occurrence, or None if frequency is unrecognized.
        """
        if task.frequency not in ("daily", "weekly", "monthly"):
            return None

        next_task = replace(task, completed=False)
        self.schedule_task(next_task)
        return next_task

    def _group_tasks_by_pet(self) -> dict:
        """Return a dict mapping each pet name to its list of tasks.

        Returns:
            A dict where keys are pet name strings and values are lists of Tasks.
        """
        groups: dict = {}
        for task in self.tasks:
            groups.setdefault(task.pet_name, []).append(task)
        return groups

    def _tasks_overlap(self, first: Task, second: Task) -> bool:
        """Return True if first task's end time runs into second task's start time.

        Args:
            first: The earlier task.
            second: The later task to compare against.

        Returns:
            True if the first task ends after the second task starts, else False.
        """
        first_end = first.start_time + first.duration / 60
        return first_end > second.start_time

    def _pet_has_conflicts(self, tasks: List[Task]) -> bool:
        """Return True if any two adjacent tasks for one pet overlap.

        Args:
            tasks: A list of Tasks belonging to a single pet.

        Returns:
            True if at least one pair of adjacent tasks overlaps, else False.
        """
        sorted_tasks = sorted(tasks, key=lambda t: t.start_time)
        for i in range(len(sorted_tasks) - 1):
            if self._tasks_overlap(sorted_tasks[i], sorted_tasks[i + 1]):
                return True
        return False

    def verify_schedule(self) -> bool:
        """Return True if no pet has overlapping tasks.

        Returns:
            True if the schedule is conflict-free, False if any pet has overlapping tasks.
        """
        for tasks in self._group_tasks_by_pet().values():
            if self._pet_has_conflicts(tasks):
                return False
        return True

    def sort_by_time(self) -> List[Task]:
        """Return tasks sorted by start time.

        Returns:
            A list of Task objects ordered from earliest to latest start_time.
        """
        return sorted(self.tasks, key=lambda t: t.start_time)

    def filter_tasks(self, completed: bool = None, pet_name: str = None) -> List[Task]:
        """Return tasks filtered by completion status and/or pet name.

        Args:
            completed: If provided, only return tasks matching this completion status.
            pet_name: If provided, only return tasks belonging to this pet.

        Returns:
            A list of Task objects matching all provided filters.
        """
        return [
            t for t in self.tasks
            if (completed is None or t.completed == completed)
            and (pet_name is None or t.pet_name == pet_name)
        ]

    def _format_hour(self, hour: int) -> str:
        """Convert a 24-hour integer to a readable 12-hour string.

        Args:
            hour: An integer hour in 24-hour format, e.g. 14.

        Returns:
            A formatted string like '2:00pm' or '8:00am'.
        """
        am_pm = "am" if hour < 12 else "pm"
        display_hour = hour if hour <= 12 else hour - 12
        return f"{display_hour}:00{am_pm}"

    def _frequency_label(self, frequency: str) -> str:
        """Return a human-readable frequency description.

        Args:
            frequency: A frequency string, one of 'daily', 'weekly', or 'monthly'.

        Returns:
            A plain-English description of the frequency, or the original string if unrecognized.
        """
        labels = {
            "daily": "daily (every day)",
            "weekly": "weekly (once a week)",
            "monthly": "monthly (once every ~4 weeks)",
        }
        return labels.get(frequency, frequency)

    def generate_schedule(self) -> str:
        """Return a formatted human-readable summary of the schedule.

        Returns:
            A multi-line string listing all tasks sorted by start time,
            or 'No tasks scheduled.' if the task list is empty.
        """
        if not self.tasks:
            return "No tasks scheduled."

        lines = [f"Daily schedule for {self.owner_name}:\n"]
        for task in self.sort_by_time():
            status = "done" if task.completed else "pending"
            lines.append(
                f"  {self._format_hour(task.start_time)} — {task.title} ({task.pet_name})"
                f" | {task.duration} min | {task.frequency} | {status}"
            )
        return "\n".join(lines)

    def explain_schedule(self, preferences: dict = None) -> str:
        """Return a reasoning summary explaining why each task is scheduled when it is.

        Args:
            preferences: An optional dict of owner preferences to include in the explanation.

        Returns:
            A multi-line string with a numbered explanation for each task,
            or 'No tasks to explain.' if the task list is empty.
        """
        if not self.tasks:
            return "No tasks to explain."

        preferences = preferences or {}
        sorted_tasks = self.sort_by_time()
        lines = [f"Schedule explanation for {self.owner_name}:\n"]

        for i, task in enumerate(sorted_tasks):
            lines.append(f"{i + 1}. {task.title} ({task.pet_name}) at {self._format_hour(task.start_time)}")
            lines.append(f"   - Frequency: {self._frequency_label(task.frequency)}")

            if task.constraints:
                lines.append(f"   - Constraints: {', '.join(task.constraints)}")

            if preferences:
                lines.append(f"   - Owner preferences applied: {', '.join(f'{k}: {v}' for k, v in preferences.items())}")

            if i == 0:
                lines.append(f"   - Order: first task of the day")
            else:
                prev = sorted_tasks[i - 1]
                prev_end = prev.start_time + prev.duration / 60
                prev_end_str = self._format_hour(int(prev_end))
                lines.append(f"   - Order: follows {prev.title} (starts after {prev_end_str} end time)")

            lines.append("")

        return "\n".join(lines)


class Owner:
    def __init__(self, owner_name: str, owner_id: str, preferences: dict = None):
        """Initialize an Owner with an empty pet roster and a linked Scheduler.

        Args:
            owner_name: The owner's display name.
            owner_id: A unique identifier for the owner.
            preferences: An optional dict of scheduling preferences.
        """
        self.owner_name: str = owner_name
        self.owner_id: str = owner_id
        self.preferences: dict = preferences or {}
        self.pets: List[Pet] = []
        self.scheduler: Scheduler = Scheduler(owner_name=self.owner_name)

    def add_task(self, task: Task) -> None:
        """Add a task to the matching pet's task list and register it with the scheduler.

        Args:
            task: The Task object to add. Its pet_name must match an existing pet.

        Raises:
            ValueError: If no pet with the given pet_name exists on this owner.
        """
        for pet in self.pets:
            if pet.pet_name == task.pet_name:
                pet.tasks.append(task)
                self.scheduler.schedule_task(task)
                return
        raise ValueError(f"No pet named '{task.pet_name}' found.")

    def delete_task(self, task: Task) -> None:
        """Remove a task from the matching pet's task list and the scheduler.

        Args:
            task: The Task object to remove.

        Raises:
            ValueError: If the task is not found on any pet.
        """
        for pet in self.pets:
            if pet.pet_name == task.pet_name and task in pet.tasks:
                pet.tasks.remove(task)
                self.scheduler.tasks.remove(task)
                return
        raise ValueError(f"Task '{task.title}' not found.")

    def complete_task(self, task: Task) -> None:
        """Mark a task as completed and schedule its next occurrence if recurring.

        Args:
            task: The Task object to mark as done.
        """
        task.completed = True
        if task.frequency in ("daily", "weekly", "monthly"):
            self.scheduler.schedule_next_occurrence(task)

    def edit_preferences(self, preferences: dict) -> None:
        """Merge new key-value pairs into the owner's existing preferences.

        Args:
            preferences: A dict of preference updates to apply.
        """
        self.preferences.update(preferences)

    def view_tasks(self) -> List[Task]:
        """Return a flat list of all tasks across all pets.

        Returns:
            A list of Task objects collected from every pet's task list.
        """
        return [task for pet in self.pets for task in pet.tasks]

    def build_schedule(self) -> None:
        """Sync all pet tasks into the scheduler and verify for conflicts.

        Raises:
            ValueError: If any pet has overlapping tasks after syncing.
        """
        self.scheduler.tasks = self.view_tasks()
        if not self.scheduler.verify_schedule():
            raise ValueError("Schedule has time conflicts. Please adjust task times.")

    def view_schedule(self) -> str:
        """Return the formatted schedule string from the scheduler.

        Returns:
            A multi-line string summary of today's schedule.
        """
        return self.scheduler.generate_schedule()
