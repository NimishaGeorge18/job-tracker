from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict
 
@dataclass
class JobApplication:
    id: int
    company: str
    role: str
    location: str
    status: str  # Applied / Interview / Rejected / Offer
    applied_date: str  # YYYY-MM-DD
    notes: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict) -> "JobApplication":
        return JobApplication(**data)

    @staticmethod
    def today() -> str:
        return datetime.now().strftime("%Y-%m-%d")