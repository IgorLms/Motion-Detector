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

    def _add_camera_json(self) -> None:
        """Добавление камеры в JSON файл"""

        # Валидация данных
        if not 1 <= len(self.name_camera.text()) <= 19:
            self._create_error("Длина названия камеры должна быть от 1 до 19 символов")
        elif len(self.rtsp.text()) == 0:
            self._create_error("Укажите RTSP поток камеры")
        else:
            # Прочитаем JSON файл
            data_json = self._get_json()
            if self.name_camera.text() in data_json.keys():
                self._create_error("Название камеры уже существует")
            elif len(data_json) > 10:
                self._create_error("Можно добавить не более 10 камер")
                # Отчистить поле RTSP
                self.rtsp.clear()
            else:
                # Добавление камеры в JSON файл
                self.__update_json(data_json, self.name_camera.text(), self.rtsp.text())
                # Создание новых кнопок
                self._create_button(self.name_camera.text(), self.rtsp.text())
                # Отчистить поле RTSP
                self.rtsp.clear()
            # Отчистить поле названия камеры
            self.name_camera.clear()