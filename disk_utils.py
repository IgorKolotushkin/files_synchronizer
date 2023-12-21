from abc import ABC, abstractmethod
from requests import Session


class DiskAbstract(ABC):
    def __init__(self, token, folder_path):
        self.token = token
        self.folder_path = folder_path
        self.session = Session()

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

    def __init__(self, token, folder_path):
        super().__init__(token, folder_path)
        self.headers = {
            'Accept': 'application/json',
            'Authorization': 'OAuth ' + self.token
        }

    def load(self, path: str):
        print(path.split("/")[-1])
        response_href = self.session.get(
            self.URL + f'upload?path={self.folder_path}/{path.split("/")[-1]}',
            headers=self.headers,
        )
        href = response_href.json()['href']
        with open(path, 'rb') as file:
            data: bytes = file.read()
            response = self.session.put(
                url=href,
                data=data,
                headers=self.headers,
            )
            print(response)

    def reload(self, path: str) -> None:
        self.delete(path.split("/")[-1])
        self.load(path)

    def delete(self, filename: str):
        response = self.session.delete(
            self.URL + f'?path={self.folder_path}/{filename}',
            headers=self.headers,
        )
        print(response)

    def get_info(self):
        files_ydisk = []
        response = self.session.get(self.URL + 'files', headers=self.headers)
        for item in response.json()['items']:
            if self.folder_path in item['path']:
                files_ydisk.append(item['name'])

        return files_ydisk
