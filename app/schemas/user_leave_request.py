from .leave_request import LeaveRequestRead
from .user import UserRead


class LeaveRequestWithUserRead(LeaveRequestRead):
    user: UserRead


class UserWithLeaveRequestsRead(UserRead):
    leave_requests: list[LeaveRequestRead]