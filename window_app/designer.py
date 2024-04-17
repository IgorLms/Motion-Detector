from typing import Optional
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import (QWidget,
                             QLabel,
                             QSizePolicy,
                             QMessageBox,
                             QMainWindow,
                             QMenu,
                             QAction)
from PyQt5.QtCore import QSize, Qt

from services.json_file import get_json


class Label(QLabel):
    """Класс лейбла для отображения видео"""

    def __init__(self, parent: Optional[QWidget]) -> None:
        """Инициализация параметров"""

        # Наследование параметров от класса QLabel
        super().__init__()
        # Инициализация родителя QWidget
        self.parent = parent
        # Массив с координатами
        self.coordinates = list()
        # Массив с координатами линии
        self.coordinates_line = list()
        # Флаг для работы с функцией mousePressEvent
        self.flag = ''
        # Размер кадра
        self.size_frame = []
        # Размер лейбла
        self.size_label = []

    @staticmethod
    def coordinate_correction(coordinate: int, size: int) -> int:
        """
        Коррекция координат точки.
        coordinate координаты нажатой мыши
        size размер кадра
        """

        if 0 <= coordinate <= 10:
            return 0
        elif size - 10 <= coordinate <= size:
            return size
        else:
            return coordinate

    def __get_coordinate_correction(self, event: Optional[QMouseEvent]) -> list[int]:
        """Формирование массива координат нажатой клавиши мыши"""

        # Коэффициенты отношения размера кадра и лейбла
        kx = self.size_frame[0] / self.size_label[0]
        ky = self.size_frame[1] / self.size_label[1]
        coordinates = [
            self.coordinate_correction(int(event.x() * kx), int(self.size_frame[0])),
            self.coordinate_correction(int(event.y() * ky), int(self.size_frame[1]))
        ]

        return coordinates

    def mousePressEvent(self, event: Optional[QMouseEvent]) -> None:
        """Получение координат мыши на лейбле"""

        if self.size_label and self.size_frame:
            if self.flag == "mask":
                # Добавить в список откорректированные координаты мышки
                self.coordinates.append(self.__get_coordinate_correction(event))
            elif self.flag == "line":
                # Добавить в список откорректированные координаты мышки
                self.coordinates_line.append(self.__get_coordinate_correction(event))
                if len(self.coordinates_line) == 2:
                    # Если две точки уже существуют в массиве, то добавить их в общие координаты
                    self.coordinates.append(self.coordinates_line)
                    self.coordinates_line = list()


class ApplicationDesign(QMainWindow):
    """Класс для дизайна приложения"""

    def __init__(self) -> None:
        """Инициализация"""

        super().__init__()

        # Заголовок окна
        self.setWindowTitle("Видеонаблюдение")
        # Установка размера окна при открытии
        self.resize(960, 540)
        # Настройка вертикального и горизонтального отображения окна
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        # Установка минимального размера окна
        self.setMinimumSize(QSize(640, 480))
        # Создание главного макета для просмотра видео
        self.image_label = Label(self)
        self.image_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.image_label)
        # Создание меню
        self._create_menu()

    def _create_menu(self) -> None:
        """
        Создание меню
        """

        # Словарь для названий элементов меню
        self.name_element = {
            "add": "Добавить",
            "delete": "Удалить",
            "save": "Сохранить",
            "camera": "Камера",
            "mask": "Маска",
            "grid": "Сетка",
            "name": "Название",
            "edit": "Редактирование",
            "watch": "Просмотр",
            "main_thread": "Основной поток",
            "filter_1": "Фильтр 1",
            "filter_2": "Фильтр 2",
            "full_screen": "Полноэкранный",
        }

        # Инициализация меню
        self.menu = self.menuBar()
        # Инициализация списка меню
        self._create_actions_edit()
        # Инициализация меню из раздела редактирования
        self._create_menu_edit()
        # Инициализация меню из раздела просмотр
        self._create_menu_watch()

    def _create_menu_edit(self) -> None:
        """
        Создание меню редактирование
        """

        # Добавление меню редактирование
        edit_menu = QMenu(self.name_element.get("edit"), self)
        self.menu.addMenu(edit_menu)
        # Добавление раздела камера
        camera_edit_menu = edit_menu.addMenu(self.name_element.get("camera"))
        camera_edit_menu.addAction(self.camera_add_action)
        camera_delete_menu = camera_edit_menu.addMenu(self.name_element.get("delete"))
        camera_delete_menu.addAction(*self.list_camera["delete"].keys())
        # Добавление раздела маска
        mask_edit_menu = edit_menu.addMenu(self.name_element.get("mask"))
        mask_edit_menu.addAction(self.mask_add_action)
        mask_edit_menu.addAction(self.mask_delete_action)
        mask_edit_menu.addAction(self.mask_save_action)
        # Добавление раздела сетка
        grid_edit_menu = edit_menu.addMenu(self.name_element.get("grid"))
        grid_edit_menu.addAction(self.grid_add_action)
        grid_edit_menu.addAction(self.grid_delete_action)
        grid_edit_menu.addAction(self.grid_save_action)
        # Добавление раздела название
        name_edit_menu = edit_menu.addMenu(self.name_element.get("name"))
        name_edit_menu.addAction(self.name_add_action)
        name_edit_menu.addAction(self.name_delete_action)
        name_edit_menu.addAction(self.name_save_action)

    def _create_menu_watch(self) -> None:
        """
        Создание меню просмотра
        """

        # Добавление меню просмотр
        watch_menu = QMenu(self.name_element.get("watch"), self)
        self.menu.addMenu(watch_menu)
        # Добавление раздела основного потока
        main_thread_menu = watch_menu.addMenu(self.name_element.get("main_thread"))
        main_thread_menu.addAction(*self.list_camera["main_thread"].keys())
        # Добавление раздела фильтр 1
        filter_1_menu = watch_menu.addMenu(self.name_element.get("filter_1"))
        filter_1_menu.addAction(*self.list_camera["filter_1"].keys())
        # Добавление раздела фильтр 2
        filter_2_menu = watch_menu.addMenu(self.name_element.get("filter_2"))
        filter_2_menu.addAction(*self.list_camera["filter_2"].keys())
        # Добавление раздела полноэкранного просмотра
        self.action_full_screen = watch_menu.addAction(self.name_element.get("full_screen"))
        self.action_full_screen.setShortcut("F11")

    def _create_actions_edit(self) -> None:
        """
        Инициализация списка меню
        """
        # Инициализация списка камер
        data_json = get_json('data/data.json')
        self.list_name = [
            "main_thread",
            "filter_1",
            "filter_2",
            "delete",
        ]
        self.list_camera = {
            name_actions: {QAction(name): path for name, path in data_json.items()} for name_actions in self.list_name
        }
        # Список добавить камеры
        self.camera_add_action = QAction(self.name_element.get("add"), self)
        # Список добавить, удалить, сохранить маску
        self.mask_add_action = QAction(self.name_element.get("add"), self)
        self.mask_delete_action = QAction(self.name_element.get("delete"), self)
        self.mask_save_action = QAction(self.name_element.get("save"), self)
        # Список добавить, удалить, сохранить сетку
        self.grid_add_action = QAction(self.name_element.get("add"), self)
        self.grid_delete_action = QAction(self.name_element.get("delete"), self)
        self.grid_save_action = QAction(self.name_element.get("save"), self)
        # Список добавить, удалить, сохранить название
        self.name_add_action = QAction(self.name_element.get("add"), self)
        self.name_delete_action = QAction(self.name_element.get("delete"), self)
        self.name_save_action = QAction(self.name_element.get("save"), self)

    def _create_error(self, text: str) -> None:
        """Генерация ошибки"""

        QMessageBox.critical(self, "Ошибка", text, QMessageBox.Ok)

    def get_size(self) -> list:
        """Отправка размеров лейбла"""

        return [self.image_label.size().width(), self.image_label.size().height()]
