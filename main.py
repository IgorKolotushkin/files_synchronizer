import requests

from config import TOKEN, LOCAL_DIR
from disk_utils import YandexDisk

URL = 'https://cloud-api.yandex.net/v1/disk/resources'
AUTH_TOKEN = 'OAuth ' + TOKEN
headers = {'Accept': 'application/json', 'Authorization': AUTH_TOKEN}


def main():
    request_disk = YandexDisk(TOKEN, 'files_synchronizer')
    request_disk.get_info()
    # request_disk.load('files_syn/2.txt')
    request_disk.reload(f'{LOCAL_DIR}2.txt')
    # request_disk.delete('files_syn/2.txt')

#files_synchronizer/new


if __name__ == '__main__':
    main()

