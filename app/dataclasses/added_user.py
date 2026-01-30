from dataclasses import dataclass

from requests import Response

from ..models.user import UserCreate, User


@dataclass
class AddedUserData:
    raw_response: Response
    new_user: User
    user_data: UserCreate