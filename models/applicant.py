from dataclasses import dataclass

@dataclass
class Applicant:
    name: str
    email: str
    application_date: str
    status: str  # e.g., "pending", "accepted", "rejected"