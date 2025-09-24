from dataclasses import dataclass, field

from core.exceptions import ApplicationException


@dataclass
class PathException(ApplicationException):
    path: str = field(default=None)
    reason: str = field(default="невідома")
    status_code: int = field(default=422)

    @property
    def message(self):
        return f"Шлях '{self.path}' не валідний. Причина: {self.reason}"
