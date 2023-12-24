import logging
import time
from os import listdir, path

from requests.exceptions import ConnectionError

from config import TOKEN, LOCAL_DIR, YANDEX_DIR, TIME_WATCH, LOG_PATH
from disk_utils import YandexDisk

logger: logging.Logger = logging.getLogger(__name__)


def get_local_files(local_dir: str) -> dict:
    """
    Функция получения названия и времени изменения файлов в локальном хранилище
    :param local_dir: локальная папка для синхронизации
    :return: словарь с названиями файлов и времени их изменения
    """
    file_storage: dict = {}
    try:
        for file_name in listdir(local_dir):
            if file_name not in file_storage.keys():
                file_storage[file_name] = path.getmtime(local_dir + file_name)

        return file_storage
    except FileNotFoundError:
        print(f"Папки {local_dir} не существует")
        return {}


def upload_files(local_dir: str, files: set, ydisk: YandexDisk) -> None:
    """
    :param local_dir: локальная папка
    :param files: файлы для загрузки на Yandex Disk
    :param ydisk: экземпляр класса для работы с Яндекс Диском
    :return: None
    """
    for file in files:
        try:
            ydisk.load(f'{local_dir}{file}')
            logger.info(f"Файл {file} успешно записан")
        except ConnectionError:
            logger.error(f"Файл {file} не записан. Ошибка соединения")


def update_files(file_storage: dict, updated_storage: dict, ydisk: YandexDisk) -> None:
    """
    Функция для обновления файлов на Yandex Disk
    :param file_storage: словарь файлов в локальном хранилище
    :param updated_storage: обновленный словарь файлов в локальном хранилище
    :param ydisk: экземпляр класса для работы с Яндекс Диском
    :return: None
    """
    for file in file_storage:
        if file_storage[file] < updated_storage[file]:
            try:
                ydisk.reload(f'{LOCAL_DIR}{file}')
                logger.info(f'Файл {file} успешно перезаписан')
            except ConnectionError:
                logger.error(f"Файл {file} не перезаписан. Ошибка соединения")


def add_new_files(local_dir: str, file_storage: dict, new_files: set, ydisk: YandexDisk) -> dict:
    """
    Функция для добавления новых файлов на Yandex Disk
    :param local_dir: локальная папка для синхронизации файлов
    :param file_storage: словарь файлов в локальном хранилище
    :param new_files: файлы для добавления Yandex Disk
    :param ydisk: экземпляр класса для работы с Яндекс Диском
    :return: обновленный словарь с файлами локальной папки
    """
    for file in new_files:
        file_storage[file] = path.getmtime(local_dir + file)
        try:
            ydisk.load(f'{local_dir}{file}')
            logger.info(f"Файл {file} успешно записан")
        except ConnectionError:
            logger.error(f"Файл {file} не записан. Ошибка соединения")

    return file_storage


def delete_files(files_for_delete: set, file_storage: dict, ydisk: YandexDisk) -> dict:
    """
    Функция для удаления файлов с Yandex Disk
    :param files_for_delete: файлы для удаления
    :param file_storage: словарь файлов в локальном хранилище
    :param ydisk: экземпляр класса для работы с Яндекс Диском
    :return: обновленный словарь с файлами локальной папки
    """
    for file in files_for_delete:
        ydisk.delete(file)
        logger.info(f'Файл {file} удален')
        file_storage.pop(file)

    return file_storage


def main() -> None:
    logger.info(f"Программа синхронизации файлов начинает работу с директорией {LOCAL_DIR}")
    ydisk: YandexDisk = YandexDisk(TOKEN, YANDEX_DIR)
    file_storage: dict[str, float] = get_local_files(LOCAL_DIR)
    upload_files(LOCAL_DIR, set(file_storage), ydisk)

    while True:
        updated_storage: dict[str, float] = get_local_files(LOCAL_DIR)
        if len(updated_storage) > len(file_storage):
            new_files: set[str] = updated_storage.keys() - file_storage.keys()
            file_storage: dict[str, float] = add_new_files(LOCAL_DIR, file_storage, new_files, ydisk)
        elif len(updated_storage) < len(file_storage):
            files_for_delete: set[str] = file_storage.keys() - updated_storage.keys()
            file_storage: dict[str, float] = delete_files(files_for_delete, file_storage, ydisk)
        else:
            update_files(file_storage, updated_storage, ydisk)
            file_storage: dict[str, float] = updated_storage

        time.sleep(float(TIME_WATCH))


if __name__ == '__main__':
    logging.basicConfig(
        filename=f'{LOG_PATH}',
        level=logging.INFO,
        format="%(name)s %(asctime)s %(levelname)s %(message)s",
    )
    main()

