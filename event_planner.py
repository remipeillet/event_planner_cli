from datetime import time, datetime
from typing import List


class Event:
    name: str
    start_time: time
    end_time: time

    def __init__(self, name: str, start_time: time, end_time: time):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return f"{self.name}: {self.start_time} - {self.end_time}"

class EventPlanner:
    events: List[Event]

    def __init__(self):
        self.events = []

    def add_event(self, name, start_time, end_time):
        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, "%H:%M").time()
        elif not isinstance(start_time, time):
            raise ValueError(
                "l'heure de début doit être un objet de type datetime.time ou str")
        if isinstance(end_time, str):
            end_time = datetime.strptime(end_time, "%H:%M").time()
        elif not isinstance(start_time, time):
            raise ValueError(
                "l'heure de fin doit être un objet de type datetime.time ou str")
        if start_time > end_time:
            raise ValueError("l'heure de début doit être inférieur à l'heure de fin")
        new_event = Event(name, start_time, end_time)
        conflicts = []
        for event in self.events:
            if event.name == new_event.name:
                raise ValueError("un événement avec ce nom existe déjà")
            if self.check_conflict(event, new_event):
                conflicts.append(event.name)
        if conflicts:
            print(f"conflits avec les événements: {', '.join(conflicts)}")
            force = input("insérer l'événement (o/n)")
            if force == "o":
                self.events.append(new_event)
        else:
            self.events.append(new_event)

    def list_events(self):
        return sorted(self.events, key=lambda event: event.start_time)

    def find_conflicts(self):
        conflicts = []
        for index, event in enumerate(self.list_events()):
            for next_event in self.list_events()[index + 1:]:
                if self.check_conflict(event, next_event):
                    conflicts.append((event, next_event))
                else:
                    break
        return conflicts

    @staticmethod
    def check_conflict(event_1: Event, event_2: Event):
        return (event_1.end_time > event_2.start_time and
                event_1.start_time < event_2.end_time)