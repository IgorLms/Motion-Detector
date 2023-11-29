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
