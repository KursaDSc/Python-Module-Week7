from dataclasses import dataclass

@dataclass
class Event:
    title: str
    start_time: str
    attendee_email: str
    organizer_email: str