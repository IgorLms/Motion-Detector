import json

from window_app.designer import ApplicationDesign


class App(ApplicationDesign):
    """Класс создания приложения"""

    def __init__(self):
        """Инициализация параметров"""

        # Наследование параметров от класса ApplicationDesign
        super().__init__()

        # Инициализация пути RTSP, по умолчанию False
        self.__path = False

        # Инициализация класса для получения видео, по умолчанию False
        self.__thread = False

    @staticmethod
    def _get_json() -> json:
        """Чтение JSON файла"""

        return json.load(open('data/data.json'))

    @staticmethod
    def __update_json(data_json, name: str, path: str) -> None:
        """Запись в JSON файл"""

        data_json.update({name: path, })
        json.dump(data_json, open('data/data.json', 'w'), sort_keys=True, indent=2, ensure_ascii=False)
