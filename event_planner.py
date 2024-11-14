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

    '''
        Method for adding events to the planner
        Params:
            name: <str> name of the event
            start_time: <time> or <str> with '%H:%M' format start time of 
            the event
            end_time: <time> or <str> with '%H:%M' format end time of the event
        Returns:
            None
        Name must be unique.
        Start time must be upper than end time.
        If conflict is detected we ask if we would force insert it or not by 
        enter 'o' in console input
    '''
    def add_event(self, name, start_time, end_time) -> None:
        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, "%H:%M").time()
        elif not isinstance(start_time, time):
            raise ValueError(
                "l'heure de début doit être un objet de type datetime.time ou "
                "str")
        if isinstance(end_time, str):
            end_time = datetime.strptime(end_time, "%H:%M").time()
        elif not isinstance(start_time, time):
            raise ValueError(
                "l'heure de fin doit être un objet de type datetime.time ou "
                "str")
        if start_time > end_time:
            raise ValueError("l'heure de début doit être inférieur à "
                             "l'heure de fin")
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

    """
        List events of planner order by start time
        Params:
            None
        Returns:
            <List[Event]> list of events sorted by start time
    """
    def list_events(self) -> List[Event]:
        return sorted(self.events, key=lambda event: event.start_time)

    """
        Find conflicts in planner
        Params:
            None
        Returns:
            <List[tuple[Event, Event]]> list of conflicts
    """
    def find_conflicts(self) -> List[tuple[Event, Event]]:
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