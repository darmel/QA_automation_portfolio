from dataclasses import dataclass

@dataclass
class Response:
    status_code: int
    text: str
    as_dict: object
    headers: dict
    