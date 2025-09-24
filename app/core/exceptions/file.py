from dataclasses import dataclass, field

from core.exceptions import ApplicationException


@dataclass
class FileValidationException(ApplicationException):
    filename: str = field(default=None)
    reason: str = field(default=None)
    status_code: int = field(default=422)

    @property
    def message(self):
        return f"Файл '{self.filename}' не валідний: {self.reason}"

@dataclass
class FileNotFoundException(ApplicationException):
    file_path: str = field(default=None)
    status_code: int = field(default=404)

    @property
    def message(self):
        return f"Фізичний файл не знайдено: {self.file_path}"
