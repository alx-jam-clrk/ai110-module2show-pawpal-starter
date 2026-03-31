from dataclasses import dataclass, field
from typing import List


@dataclass
class Pet:
    pet_name: str
    owner_name: str
    pet_id: str


@dataclass
class Task:
    title: str
    pet: Pet
    duration: int           # in minutes
    constraints: List[str] = field(default_factory=list)  # e.g. ["morning only", "before 9am"]


class Scheduler:
    def __init__(self, owner_name: str):
        self.owner_name: str = owner_name
        self.tasks: List[Task] = []

    @property
    def pet_names(self) -> List[str]:
        return list({task.pet.pet_name for task in self.tasks})

    def schedule_task(self, task: Task) -> None:
        pass

    def verify_schedule(self) -> bool:
        pass

    def generate_schedule(self) -> List[Task]:
        pass

    def explain_schedule(self) -> str:
        pass


class Owner:
    def __init__(self, owner_name: str, owner_id: str, preferences: dict = None):
        self.owner_name: str = owner_name
        self.owner_id: str = owner_id
        self.preferences: dict = preferences or {}
        self.pets: List[Pet] = []
        self.tasks: List[Task] = []
        self.scheduler: Scheduler = Scheduler(owner_name=self.owner_name)

    def add_task(self, task: Task) -> None:
        pass

    def build_schedule(self) -> None:
        pass

    def delete_task(self, task: Task) -> None:
        pass

    def edit_preferences(self, preferences: dict) -> None:
        pass

    def view_tasks(self) -> List[Task]:
        pass

    def view_schedule(self) -> List[Task]:
        pass
