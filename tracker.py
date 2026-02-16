import json
from pathlib import Path
from typing import List, Optional

from models import JobApplication
from utils import VALID_STATUSES


class JobTracker:
    def __init__(self, data_path: str = "data/applications.json"):
        self.data_file = Path(data_path)
        self.applications: List[JobApplication] = []
        self._load()

    def _load(self) -> None:
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.data_file.exists():
            self.data_file.write_text("[]", encoding="utf-8")

        raw = json.loads(self.data_file.read_text(encoding="utf-8"))
        self.applications = [JobApplication.from_dict(x) for x in raw]

    def _save(self) -> None:
        data = [a.to_dict() for a in self.applications]
        self.data_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def _next_id(self) -> int:
        if not self.applications:
            return 1
        return max(a.id for a in self.applications) + 1

    def add(self, company: str, role: str, location: str, status: str, notes: str = "") -> JobApplication:
        if status not in VALID_STATUSES:
            raise ValueError("Invalid status")

        app = JobApplication(
            id=self._next_id(),
            company=company,
            role=role,
            location=location,
            status=status,
            applied_date=JobApplication.today(),
            notes=notes
        )
        self.applications.append(app)
        self._save()
        return app

    def list_all(self) -> List[JobApplication]:
        return sorted(self.applications, key=lambda a: a.id)

    def find_by_id(self, app_id: int) -> Optional[JobApplication]:
        for a in self.applications:
            if a.id == app_id:
                return a
        return None

    def update_status(self, app_id: int, new_status: str) -> bool:
        app = self.find_by_id(app_id)
        if not app:
            return False
        if new_status not in VALID_STATUSES:
            raise ValueError("Invalid status")

        app.status = new_status
        self._save()
        return True

    def delete(self, app_id: int) -> bool:
        app = self.find_by_id(app_id)
        if not app:
            return False
        self.applications.remove(app)
        self._save()
        return True

    def filter_by_status(self, status: str) -> List[JobApplication]:
        if status not in VALID_STATUSES:
            raise ValueError("Invalid status")
        return [a for a in self.applications if a.status == status]

    def stats(self) -> dict:
        total = len(self.applications)
        by_status = {s: 0 for s in VALID_STATUSES}
        for a in self.applications:
            if a.status in by_status:
                by_status[a.status] += 1
        interviews = by_status.get("Interview", 0)
        interview_rate = (interviews / total * 100) if total else 0.0
        return {
            "total": total,
            "by_status": by_status,
            "interview_rate_percent": round(interview_rate, 2),
        }
    
    def search_company(self, keyword: str):
        k = keyword.lower().strip()
        return [a for a in self.applications if k in a.company.lower()]

