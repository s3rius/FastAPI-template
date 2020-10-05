from fastapi import HTTPException
from httpx import Response


class ServiceError(HTTPException):
    def __init__(self, action: str, service_response: Response) -> None:
        try:
            error_data = service_response.json()
        except LookupError:
            error_data = service_response.text
        self.detail = (
            f"Can't {action}. Getter respond: {error_data}"
            f" (status code: {service_response.status_code})"
        )
        self.response = service_response
        self.status_code = 400
