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
        response_href = self.session.get(self.URL + f'upload?path={self.folder_path}/2.txt', headers=self.headers)
        href = response_href.json()['href']
        with open(path, 'rb') as file:
            data = file.read()
            response = self.session.put(url=href, data=data, headers=self.headers)
            print(response)

    def reload(self, path):
        self.delete(path)
        self.load(path)

    def delete(self, filename):
        response = self.session.delete(self.URL + f'?path={self.folder_path}/2.txt', headers=self.headers)
        print(response)

    def get_info(self):
        response = self.session.get(self.URL + 'files', headers=self.headers)
        for item in response.json()['items']:
            if self.folder_path in item['path']:
                print(item['name'])
