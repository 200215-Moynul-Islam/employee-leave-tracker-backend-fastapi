from app.models import LeaveRequest
from app.repositories.base_repository import EntityBaseRepository


class LeaveRequestRepository(EntityBaseRepository[LeaveRequest]):
    def __init__(self, db):
        super().__init__(db, LeaveRequest)
