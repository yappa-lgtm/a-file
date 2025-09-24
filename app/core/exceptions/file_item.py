from dataclasses import dataclass, field

from pydantic import UUID4

from core.exceptions import ApplicationException

@dataclass
class FileItemNotFoundException(ApplicationException):
    file_id: UUID4 = field(default=None)
    status_code: int = field(default=404)

    @property
    def message(self):
        return f"Файл з ID {self.file_id} не знайдено"