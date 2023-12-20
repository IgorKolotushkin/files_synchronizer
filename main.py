import requests

from config import TOKEN

URL = 'https://cloud-api.yandex.net/v1/disk'
AUTH_TOKEN = 'OAuth ' + TOKEN
headers = {'Accept': 'application/json', 'Authorization': AUTH_TOKEN}


def main():
    response = requests.get(URL, headers=headers, timeout=5)
    print(response.json())


if __name__ == '__main__':
    main()

