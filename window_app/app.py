from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPixmap, QCloseEvent
from PyQt5 import QtGui

import numpy as np
import json
import cv2

from window_app.designer import ApplicationDesign
from video.motion_detector import VideoBackgroundSubtractorKNN
from video.video import VideoCaptureRTSP


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

        # Привязка функций к кнопкам
        self.open_video.clicked.connect(self.__run_open_video)
        self.open_filter_video.clicked.connect(self.__run_open_filter_video)
        self.open_video_full.clicked.connect(self.__full_screen_video)
        self.add_camera.clicked.connect(self._add_camera_json)

    def closeEvent(self, event: QCloseEvent) -> None:
        """Метод закрытия окна"""
        # Остановить просмотр видео
        self.__stop_video()
        # Закрыть приложение
        event.accept()

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

    def __stop_video(self) -> None:
        """Остановить видео просмотр"""

        # Остановить просмотр видео, если он существует
        if self.__thread:
            self.__thread.stop()
        # Удалить последний кадр с виджета image_label
        self.image_label.clear()

    def __start_video(self) -> None:
        """Начать видео просмотр"""

        # Подключение к сигналу просмотра видео
        self.__thread.change_pixmap_signal.connect(self.__update_image)
        # запустить просмотр видео
        self.__thread.start()

    def __run_video(self, class_video):
        """Запуск видео"""

        # Если путь для запуска видео существует
        if self.__path or type(self.__path) == int and self.__path == 0:
            self.__stop_video()
            # Класс для получения видео
            try:
                # То запустить просмотр видео
                self.__thread = class_video
                self.__start_video()
            except Exception as e:
                # вывести ошибку, если при запуске видео возникли ошибки
                self._create_error(str(e))
                self.__stop_video()

    def __run_open_video(self) -> None:
        """Запуск видео основного потока"""

        try:
            if self.__path or type(self.__path) == int and self.__path == 0:
                self.__run_video(VideoCaptureRTSP(self.__path))
            else:
                self._create_error('Укажите камеру')
        except Exception as e:
            # Обработка ошибок при инициализации видеопотока
            self._create_error(str(e))

    def __run_open_filter_video(self) -> None:
        """Запуск видео с фильтром"""

        if self.__path or type(self.__path) == int and self.__path == 0:
            self.__run_video(VideoBackgroundSubtractorKNN(self.__path))
        else:
            self._create_error('Укажите камеру')

    @pyqtSlot(np.ndarray)
    def __update_image(self, frame: QPixmap) -> None:
        """Метод обновления изображения на видео"""

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
