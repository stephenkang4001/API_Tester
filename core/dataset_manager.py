import uuid
from datetime import datetime

from models.request_model import ApiRequest
from storage.file_storage import FileStorage


class DataSetManager:
    def __init__(self) -> None:
        self._storage = FileStorage()

    def get_all(self) -> list:
        return self._storage.load_datasets()

    def add(self, name: str, request: ApiRequest) -> str:
        datasets = self._storage.load_datasets()
        ds_id = str(uuid.uuid4())
        datasets.append({
            "id":         ds_id,
            "name":       name,
            "updated_at": datetime.now().isoformat(),
            "request":    request.to_dict(),
        })
        self._storage.save_datasets(datasets)
        return ds_id

    def update(self, ds_id: str, name: str, request: ApiRequest) -> None:
        datasets = self._storage.load_datasets()
        for ds in datasets:
            if ds["id"] == ds_id:
                ds["name"]       = name
                ds["updated_at"] = datetime.now().isoformat()
                ds["request"]    = request.to_dict()
                break
        self._storage.save_datasets(datasets)

    def delete(self, ds_id: str) -> None:
        datasets = [ds for ds in self._storage.load_datasets() if ds["id"] != ds_id]
        self._storage.save_datasets(datasets)
