from config import MAX_HISTORY
from models.request_model import ApiRequest
from models.response_model import ApiResponse
from storage.file_storage import FileStorage


class HistoryManager:
    def __init__(self) -> None:
        self._storage = FileStorage()

    def add(self, request: ApiRequest, response: ApiResponse) -> None:
        history = self._storage.load_history()
        history.insert(0, {
            "request":  request.to_dict(),
            "response": response.to_dict(),
        })
        self._storage.save_history(history[:MAX_HISTORY])

    def get_all(self) -> list:
        return self._storage.load_history()

    def clear(self) -> None:
        self._storage.save_history([])
