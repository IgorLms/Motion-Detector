from PyQt5.QtCore import pyqtSlot, Qt, QThread, QSize
from PyQt5.QtGui import QPixmap, QCloseEvent, QKeyEvent, QIcon
from PyQt5 import QtGui

import numpy as np
import cv2
from PyQt5.QtWidgets import QMainWindow, QLabel, QMenuBar, QMenu, QAction, QSizePolicy

from services.json_file import get_json, set_json
from window_app.designer import ApplicationDesign
from video.motion_detector import VideoBackgroundSubtractorKNN
from video.video import VideoCaptureRTSP


class App(ApplicationDesign):
    """Класс создания приложения"""

    def __init__(self):
        """Инициализация параметров"""

        # Наследование параметров от класса ApplicationDesign
        super().__init__()

        # Инициализация пути RTSP, по умолчанию 0
        self.__path = 0

        # Инициализация класса для получения видео
        self.__thread = QThread(self)
        self.video = VideoCaptureRTSP(self.__path)
        self.filter_video = VideoBackgroundSubtractorKNN(self.__path)

        # Привязка функций к кнопкам
        # self.open_video.clicked.connect(self.__run_open_video)
        # self.open_filter_video.clicked.connect(self.__run_open_filter_video)
        # self.open_video_full.clicked.connect(self.__full_screen_video)
        # self.add_camera.clicked.connect(self._add_camera_json)

        # Словарь ключ: нажатая кнопка, значение: ключ в json файле
        self.key = {
            Qt.Key_F5: "mask",
            Qt.Key_F6: "line"
        }

    def closeEvent(self, event: QCloseEvent) -> None:
        """Метод закрытия окна"""
        # Остановить просмотр видео
        self.__stop_video()
        # Закрыть приложение
        event.accept()

    def _add_camera_json(self) -> None:
        """Добавление камеры в JSON файл"""

        # Валидация данных
        if not 1 <= len(self.name_camera.text()) <= 19:
            self._create_error("Длина названия камеры должна быть от 1 до 19 символов")
        elif len(self.rtsp.text()) == 0:
            self._create_error("Укажите RTSP поток камеры")
        else:
            # Прочитаем JSON файл
            data_json = get_json('data/data.json')
            if self.name_camera.text() in data_json.keys():
                self._create_error("Название камеры уже существует")
            elif len(data_json) > 10:
                self._create_error("Можно добавить не более 10 камер")
                # Отчистить поле RTSP
                self.rtsp.clear()
            else:
                # Добавление камеры в JSON файл
                set_json(data_json, self.name_camera.text(), self.rtsp.text(), 'data/data.json')
                # Создание новых кнопок
                self._create_button(self.name_camera.text(), self.rtsp.text())
                # Отчистить поле RTSP
                self.rtsp.clear()
            # Отчистить поле названия камеры
            self.name_camera.clear()

    def __stop_video(self) -> None:
        """Остановить видео просмотр"""

        # Остановить просмотр видео, если он существует
        if self.__thread.isRunning():
            self.__thread.set_status(False)

    def __start_video(self) -> None:
        """Начать видео просмотр"""

        # Указать положительный флаг для запуска видео
        self.__thread.set_status(True)
        # Подключение к сигналу просмотра видео
        self.__thread.change_pixmap_signal.connect(self.__update_image)
        # запустить просмотр видео
        self.__thread.start()

    def __run_video(self, class_video):
        """Запуск видео"""

        # Остановить видео просмотр
        self.__stop_video()
        # Изменить класс для просмотра видео
        self.__thread = class_video
        # Начать видео просмотр
        self.__start_video()

    def __run_open_video(self) -> None:
        """Запуск видео основного потока"""

        self.__run_video(self.video)

    def __run_open_filter_video(self) -> None:
        """Запуск видео с фильтром"""

        self.__run_video(self.filter_video)

    @pyqtSlot(np.ndarray)
    def __update_image(self, frame: QPixmap) -> None:
        """Метод обновления изображения на видео"""

        # Передать координаты нажатия мыши в класс VideoCaptureRTSP
        self.video.coordinates_line = self.image_label.coordinates
        # По сигналу остановить просмотр видео
        self.__thread.signal_stop_video.connect(self.__stop_video)
        # Преобразование изображения из OpenCV в QPixmap
        frame = self.__convert_cv_qt(frame)
        # Поместить изображение в виджет
        self.image_label.setPixmap(frame)

    def __convert_cv_qt(self, frame: cv2.typing.MatLike) -> QPixmap:
        """Преобразование изображения из OpenCV в QPixmap"""

        # Преобразование изображения в RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Получение размеров изображения
        h, w, ch = frame.shape
        # Конвертирование в QPixmap
        convert_to_qt_format = QtGui.QImage(frame.data, w, h, ch * w, QtGui.QImage.Format_RGB888)
        # Копия изображения масштабируемая под виджет
        frame_to_widget = convert_to_qt_format.scaled(self.image_label.size(), Qt.IgnoreAspectRatio)
        return QPixmap.fromImage(frame_to_widget)

    def _button_open_video(self, path: str) -> None:
        """Открыть видео по кнопке"""

        # Меняем RTSP путь до видео
        try:
            # Проверка, что путь к камере это число
            self.__path = int(path)
        except ValueError:
            # Иначе сохранить, как строка
            self.__path = path

        # Запускаем видео
        self.__run_open_video()

    def __full_screen_video(self) -> None:
        """Видео на полный экран"""

        if self.isFullScreen():
            # Видео вернуть в прежнее состояние
            self.showNormal()
            # Показать макет для добавления и открытия видео
            self.add_camera_title.show()
            self.name_camera_title.show()
            self.name_camera.show()
            self.rtsp_title.show()
            self.rtsp.show()
            self.add_camera.show()
            self.add_camera_line.show()
            self.open_camera_title.show()
            for button in self.list_button:
                button.show()
            self.vertical_line_main.show()
        else:
            # Видео на полный экран
            self.showFullScreen()
            # Скрыть макет для добавления и открытия видео
            self.add_camera_title.hide()
            self.name_camera_title.hide()
            self.name_camera.hide()
            self.rtsp_title.hide()
            self.rtsp.hide()
            self.add_camera.hide()
            self.add_camera_line.hide()
            self.open_camera_title.hide()
            for button in self.list_button:
                button.hide()
            self.vertical_line_main.hide()

    @staticmethod
    def update_array(array: list) -> list:
        """Редактирование массива для уравнения его размерности"""

        # Узнать максимальную длину массива с координатами
        max_len = max(len(coordinate) for coordinate in array)
        # Редактирование массива для уравнения его размерности
        for coordinate in array:
            while len(coordinate) < max_len:
                coordinate.append(coordinate[-1])

        return array

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        По нажатию клавиши F5, F6 активировать функцию получения координат с лейбла.
        По нажатию клавиши F4 деактивировать функцию получения координат с лейбла и записать их json файл.
        """

        if event.key() in [Qt.Key_F5, Qt.Key_F6]:
            # Изменить флаг размера лейбла
            self.image_label.size_label = self.get_size()
            # Изменить флаг размера кадра
            self.image_label.size_frame = self.video.get_size()
            # Изменить флаг для прослушивания клика мыши по лейблу
            self.image_label.flag = self.key[event.key()]
            # Изменить флаг для рисования линии
            self.video.flag_line = self.key[event.key()]
        elif event.key() == Qt.Key_F4:
            if self.image_label.coordinates:
                # Прочитать json файл с координатами
                mask_json = get_json('data/mask.json')
                # Добавить в список старых координат новые координаты
                if self.video.flag_line == 'line':
                    mask_json[self.video.flag_line].extend(self.image_label.coordinates)
                elif self.video.flag_line == 'mask':
                    mask_json[self.video.flag_line].append(self.image_label.coordinates)
                # Редактирование массива для уравнения его размерности
                self.update_array(mask_json[self.video.flag_line])
                # Записать координаты маскирования детектирования в json файл
                # Обновить атрибут mask_json данных в классе VideoCaptureRTSP
                self.video.mask_json = self.filter_video.mask_json = set_json(
                    mask_json,
                    self.video.flag_line,
                    mask_json[self.video.flag_line],
                    'data/mask.json'
                )
            # Изменить флаг для прослушивания клика мыши по лейблу
            self.image_label.flag = ''
            # Изменить флаг для рисования линии
            self.video.flag_line = ''
            # Обнулить список координат для нажатия мышки
            self.image_label.coordinates = list()
            self.image_label.coordinates_line = list()
