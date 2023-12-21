import requests

from config import TOKEN
from disk_utils import YandexDisk

URL = 'https://cloud-api.yandex.net/v1/disk/resources'
AUTH_TOKEN = 'OAuth ' + TOKEN
headers = {'Accept': 'application/json', 'Authorization': AUTH_TOKEN}


def main():
    request_disk = YandexDisk(TOKEN, 'files_synchronizer')
    request_disk.get_info()
    # response = requests.get(URL, headers=headers, timeout=5)
    # print(response.json())
    # with open('1.txt', 'rb') as file:
    #     data = file.read()
    #     response = requests.put(url="https://uploader2v.disk.yandex.net:443/upload-target/20231220T144438.775.utd.6my8aq1pshwpu7ogrn8i6ico8-k2v.29806689", data=data)
    #     print(response)
#files_synchronizer/new


if __name__ == '__main__':
    main()

