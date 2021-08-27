from typing import Any, Dict

class UserStatus:

    def __init__(self, data: Dict[str, str]) -> None:
        self.text: str = data.get("text")
        self.presence: str = data.get("presence")

class UserAvatar:

    def __init__(self, data: Dict[str, Any]) -> None:
        self.id: str = data.get("id")
        self.tag: str = data.get("tag")
        self.filename: str = data.get("filename")
        self.metadata: Dict[str, Any] = data.get("metadata")


class User:

    __slots__ = ("data", "id", "username", "is_online", "is_bot", "badges")

    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data
        self.id: str = data.get("_id")
        self.username = data.get("username")
        self.is_online: bool = data.get("online")
        self.is_bot: bool = True if data.get("bot") else False
        self.badges: int = data.get("badges")

    def __eq__(self, o: object) -> bool:
        return isinstance(o, User) and o.id == self.id

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    @property
    def avatar(self) -> UserAvatar:
        return UserAvatar(self.data.get("avatar"))

    @property
    def avatar_url(self) -> str:
        avatar = self.data.get("avatar")
        return f"https://autumn.revolt.chat/avatars/{avatar['_id']}/{avatar['filename']}"

    @property
    def status(self) -> UserStatus:
        return UserStatus(self.data.get("status"))