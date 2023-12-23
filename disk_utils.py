import logging
from abc import ABC, abstractmethod
from requests import Session, Response

from config import LOG_PATH

logger: logging.Logger = logging.getLogger(__name__)
logging.basicConfig(
        filename=f'{LOG_PATH}logs.log',
        level=logging.INFO,
        format="%(name)s %(asctime)s %(levelname)s %(message)s",
    )


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
    """
    Класс с методами для работы с YandexDisk
    """
    URL = 'https://cloud-api.yandex.net/v1/disk/resources/'

    def __init__(self, token, folder_path) -> None:
        """
        :param token: токен
        :param folder_path: папка на YandexDisk
        """
        super().__init__(token, folder_path)
        self.headers = {
            'Accept': 'application/json',
            'Authorization': 'OAuth ' + self.token
        }

    def load(self, path: str) -> None:
        """
        Метод по загрузке файлов на Яндекс Диск используя Yandex Disk API
        :param path: путь к файлу на Яндекс Диск
        :return: None
        """
        response_href: Response = self.session.get(
            self.URL + f'upload?path={self.folder_path}/{path.split("/")[-1]}',
            headers=self.headers,
        )
        if response_href.status_code != 200:
            logger.error(response_href.json()['message'])
        try:
            href: str = response_href.json()['href']
            with open(path, 'rb') as file:
                data: bytes = file.read()
                self.session.put(
                    url=href,
                    data=data,
                    headers=self.headers,
                )
        except KeyError:
            pass

    def reload(self, path: str) -> None:
        """
        Метод для перезаписи файла на Яндекс Диск
        :param path: путь к файлу на Яндекс Диск
        :return: None
        """
        self.delete(path.split("/")[-1])
        self.load(path)

    def delete(self, filename: str) -> None:
        """
        Метод для удаления файла с Яндекс Диск
        :param filename: имя удаляемого файла
        :return: None
        """
        response: Response = self.session.delete(
            self.URL + f'?path={self.folder_path}/{filename}',
            headers=self.headers,
        )
        if response.status_code != 204:
            logger.error(response.json()['message'])

    def get_info(self) -> list:
        """
        Метод для получения списка файлов на Яндекс Диск
        :return: список файлов
        """
        files_ydisk: list = []
        response: Response = self.session.get(self.URL, headers=self.headers)
        if response.status_code != 200:
            logger.error(response.json()['message'])

        for item in response.json()['items']:
            if self.folder_path in item['path']:
                files_ydisk.append(item['name'])

        return files_ydisk
