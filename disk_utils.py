from abc import ABC, abstractmethod
from requests import Session


class DiskAbstract(ABC):
    def __init__(self, token, folder_path):
        self.token = token
        self.folder_path = folder_path
        self.session = Session()
        self.headers = {'Accept': 'application/json', 'Authorization': 'OAuth ' + self.token}

    @abstractmethod
    def load(self, path):
        pass

    @abstractmethod
    def reload(self, path):
        pass

    @abstractmethod
    def delete(self, filename):
        pass

    @abstractmethod
    def get_info(self):
        pass


class YandexDisk(DiskAbstract):
    URL = 'https://cloud-api.yandex.net/v1/disk/resources/'

    def load(self, path):
        pass

    def reload(self, path):
        pass

    def delete(self, filename):
        pass

    def get_info(self):
        response = self.session.get(self.URL + f'files?path=disk:/files_synchronizer/', headers=self.headers)
        print(response.json())
