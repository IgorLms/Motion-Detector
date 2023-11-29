from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy, QHBoxLayout, QPushButton, QSpacerItem, QLineEdit, QFrame, QMessageBox
from PyQt5.QtCore import QSize


class ButtonOpenVideo(QPushButton):
    """Класс динамического создания кнопки открытия камеры"""

    def __init__(self, name: str, path: str):
        """Инициализация параметров"""

        # Наследование параметров от класса QPushButton
        super().__init__()
        # RTSP ссылка к камере
        self.path = path
        # Название камеры отобразить в названии кнопки
        self.setText(name)
        # Настройка вертикального и горизонтального отображения кнопки
        policy_open_camera = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        policy_open_camera.setHorizontalStretch(0)
        policy_open_camera.setVerticalStretch(0)
        policy_open_camera.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(policy_open_camera)


class ApplicationDesign(QWidget):
    """Класс для дизайна приложения"""

    def __init__(self):
        """Инициализация параметров"""

        # Наследование параметров от класса QWidget
        super().__init__()

        # Массив экземпляров класса ButtonOpenVideo
        self.list_button = list()

        '''Настройка окна'''
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

        '''Настройка макета'''
        # Создание главного макета
        self.horizontal_layout_main = QHBoxLayout(self)
        # Создание макета для добавления и открытия видео
        self.vertical_layout_open_video = QVBoxLayout()
        # Добавление виджета заголовка "Добавление камеры"
        self.add_camera_title = QLabel(self)
        self.add_camera_title.setText('Добавление камеры')
        font_add_camera_title = QtGui.QFont()
        font_add_camera_title.setBold(True)
        font_add_camera_title.setWeight(75)
        self.add_camera_title.setFont(font_add_camera_title)
        # Добавление виджета заголовка "Название камеры"
        self.name_camera_title = QLabel(self)
        self.name_camera_title.setText('Название камеры')
        # Добавление виджета поля названия камеры
        self.name_camera = QLineEdit(self)
        policy_name_camera = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        policy_name_camera.setHorizontalStretch(0)
        policy_name_camera.setVerticalStretch(0)
        policy_name_camera.setHeightForWidth(self.name_camera.sizePolicy().hasHeightForWidth())
        self.name_camera.setSizePolicy(policy_name_camera)
        # Добавление виджета заголовка "RTSP"
        self.rtsp_title = QLabel(self)
        self.rtsp_title.setText('RTSP')
        # Добавление виджета поля RTSP
        self.rtsp = QLineEdit(self)
        policy_rtsp = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        policy_rtsp.setHorizontalStretch(0)
        policy_rtsp.setVerticalStretch(0)
        policy_rtsp.setHeightForWidth(self.rtsp.sizePolicy().hasHeightForWidth())
        self.rtsp.setSizePolicy(policy_rtsp)
        # Настройка кнопки добавить камеру
        self.add_camera = QPushButton(self)
        self.add_camera.setText('Добавить камеру')
        policy_add_camera = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        policy_add_camera.setHorizontalStretch(0)
        policy_add_camera.setVerticalStretch(0)
        policy_add_camera.setHeightForWidth(self.add_camera.sizePolicy().hasHeightForWidth())
        self.add_camera.setSizePolicy(policy_add_camera)
        # Добавление горизонтальной линии
        self.add_camera_line = QFrame(self)
        font_add_camera_line = QtGui.QFont()
        font_add_camera_line.setBold(False)
        font_add_camera_line.setWeight(50)
        self.add_camera_line.setFont(font_add_camera_line)
        self.add_camera_line.setFrameShape(QFrame.HLine)
        self.add_camera_line.setFrameShadow(QFrame.Sunken)
        # Добавление виджета заголовка "Открытие камеры"
        self.open_camera_title = QLabel(self)
        self.open_camera_title.setText('Открытие камеры')
        font_open_camera_title = QtGui.QFont()
        font_open_camera_title.setBold(True)
        font_open_camera_title.setWeight(75)
        self.open_camera_title.setFont(font_open_camera_title)
        # Добавление прокладки для смещения открытия и добавления видео к верху
        self.vertical_spacer_open_camera = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # Добавление виджетов на макеты
        self.vertical_layout_open_video.addWidget(self.add_camera_title)
        self.vertical_layout_open_video.addWidget(self.name_camera_title)
        self.vertical_layout_open_video.addWidget(self.name_camera)
        self.vertical_layout_open_video.addWidget(self.rtsp_title)
        self.vertical_layout_open_video.addWidget(self.rtsp)
        self.vertical_layout_open_video.addWidget(self.add_camera)
        self.vertical_layout_open_video.addWidget(self.add_camera_line)
        self.vertical_layout_open_video.addWidget(self.open_camera_title)
        self.vertical_layout_open_video.addItem(self.vertical_spacer_open_camera)
        self.__add_button_open_video()
        # Добавление вертикальной линии для разделения области просмотра и добавления
        self.vertical_line_main = QFrame(self)
        self.vertical_line_main.setFrameShape(QFrame.VLine)
        self.vertical_line_main.setFrameShadow(QFrame.Sunken)
        # Создание вертикального макета для просмотра видео и кнопок видео
        self.vertical_layout_watch_video = QVBoxLayout()
        # Настройка виджета для видео
        self.image_label = QLabel(self)
        # Создание макета для кнопок
        self.horizontal_layout_button = QHBoxLayout()
        # Настройка кнопки основной поток
        self.open_video = QPushButton(self)
        self.open_video.setText('Основной поток')
        policy_open_video = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        policy_open_video.setHorizontalStretch(0)
        policy_open_video.setVerticalStretch(0)
        policy_open_video.setHeightForWidth(self.open_video.sizePolicy().hasHeightForWidth())
        self.open_video.setSizePolicy(policy_open_video)
        # Настройка кнопки фильтр
        self.open_filter_video = QPushButton(self)
        self.open_filter_video.setText('Фильтр')
        policy_open_filter_video = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        policy_open_filter_video.setHorizontalStretch(0)
        policy_open_filter_video.setVerticalStretch(0)
        policy_open_filter_video.setHeightForWidth(self.open_filter_video.sizePolicy().hasHeightForWidth())
        self.open_filter_video.setSizePolicy(policy_open_filter_video)
        # Настройка кнопки полноэкранный
        self.open_video_full = QPushButton(self)
        self.open_video_full.setText('Полноэкранный')
        policy_open_video_full = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        policy_open_video_full.setHorizontalStretch(0)
        policy_open_video_full.setVerticalStretch(0)
        policy_open_video_full.setHeightForWidth(self.open_video_full.sizePolicy().hasHeightForWidth())
        self.open_video_full.setSizePolicy(policy_open_video_full)
        # Добавление прокладки для смещения кнопок к левому углу
        horizontal_spacer_button = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Preferred)
        # Добавление виджетов на макеты
        self.vertical_layout_watch_video.addWidget(self.image_label)
        self.horizontal_layout_button.addWidget(self.open_video)
        self.horizontal_layout_button.addWidget(self.open_filter_video)
        self.horizontal_layout_button.addItem(horizontal_spacer_button)
        self.horizontal_layout_button.addWidget(self.open_video_full)
        self.vertical_layout_watch_video.addLayout(self.horizontal_layout_button)
        # Добавление макетов на главный макет
        self.horizontal_layout_main.addLayout(self.vertical_layout_open_video)
        self.horizontal_layout_main.addWidget(self.vertical_line_main)
        self.horizontal_layout_main.addLayout(self.vertical_layout_watch_video)

    def __add_button_open_video(self) -> None:
        """Метод добавления кнопок открытия видео из JSON файла"""

        # Прочитаем JSON файл
        data_json = self._get_json()
        # Перебираем JSON файл
        for name, path in data_json.items():
            self._create_button(name, path)

    def _create_button(self, name: str, path: str) -> None:
        """Метод создания кнопки"""

        # Создаём кнопку на основе класса ButtonOpenVideo
        button = ButtonOpenVideo(name, path)
        # Привязываем кнопку к функции
        button.clicked.connect(lambda ch, path_rtsp=button.path: self._button_open_video(path_rtsp))
        # Добавляем кнопку на макет
        self.vertical_layout_open_video.insertWidget(self.vertical_layout_open_video.count() - 1, button)
        # Добавляем экземпляр кнопки в массив
        self.list_button.append(button)

    def _create_error(self, text: str) -> None:
        """Генерация ошибки"""

        QMessageBox.critical(self, "Ошибка", text, QMessageBox.Ok)
