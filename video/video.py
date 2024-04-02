from typing import Union
from PyQt5.QtCore import QThread, pyqtSignal
from cv2 import UMat

import numpy as np
import subprocess
import re
import cv2

from services.json_file import get_json


class VideoCaptureRTSP(QThread):
    """Просмотр камеры по RTSP потоку"""

    # Сигнал передачи видео
    change_pixmap_signal = pyqtSignal(np.ndarray)
    # Сигнал остановки видео
    signal_stop_video = pyqtSignal()
    # Флаг для управления потоком видео
    status = True

    def __init__(self, path_rtsp: Union[int, str]):
        """Инициализация параметров"""

        # Наследование параметров от класса QThread
        super().__init__()

        # Сохранение пути до камеры
        self.__path_rtsp = path_rtsp

        self.flag_line = ''
        self.coordinates_line = list()

        # Валидация пинга IP адреса
        self.__validate_ping_ip_address()
        # Валидация пути видео
        self.__validate_path_rtsp()
        # Определение устройства воспроизведения видео
        self.__cap = cv2.VideoCapture(path_rtsp, cv2.CAP_DSHOW)
        self.__cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.__cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        # Проверка, что видео открывается
        self.__validate_open_video_source()

    def __del__(self):
        """Завершение работы с классом"""

        try:
            # Прекратить обращение к видео, если оно существовало
            self.cap_release()
        except AttributeError:
            pass
        finally:
            # Уничтожить все открытые окна
            cv2.destroyAllWindows()

    def get_size(self) -> list:
        """Получение размера фрейма"""

        return [self.__cap.get(cv2.CAP_PROP_FRAME_WIDTH), self.__cap.get(cv2.CAP_PROP_FRAME_HEIGHT)]

    def set_status(self, flag: bool):
        """Изменение статуса"""

        self.status = flag

    def cap_release(self):
        """Прекратить обращение к видео"""

        self.set_status(False)
        self.__cap.release()

    def run(self):
        """Получение изображения """

        # Запуск цикла получения кадров видео
        while self.status:
            # Получение кадра видео
            ret, frame = self._get_frame()

            if ret:
                # Отправка сигнала о существовании корректного кадра
                self.change_pixmap_signal.emit(frame)

    @staticmethod
    def mask_coordinates(frame: cv2.typing.MatLike, coordinates: list) -> UMat:
        """Накладывание чёрной маски на кадр видео для исключения детектирования"""

        if coordinates:
            # Создание нулевой матрицы, размером кадра видео
            mask = np.zeros(frame.shape, dtype=np.uint8)
            # Замена значений нулевой матрицы на 255 (из белого цвета в чёрный цвет)
            mask[mask == 0] = 255

            # Создание массива из списка координат
            array_coordinates = np.array(coordinates, dtype=np.int32)

            # Рисование на чёрном изображении белых многоугольников по координатам
            cv2.fillPoly(mask, array_coordinates, (0,) * frame.shape[2])

            # Объединение кадра с видео и маски
            return cv2.bitwise_and(frame, mask)

        return frame

    @staticmethod
    def drawing_lines(frame: cv2.typing.MatLike, coordinates: list) -> None:
        """Рисование линии"""

        array_coordinates = np.array(coordinates, np.int32)
        cv2.polylines(frame, array_coordinates, True, (0, 255, 255), 3)

    def _get_frame(self) -> [bool, cv2.typing.MatLike]:
        """Получить кадр из видео в виде массива"""

        # Получить кадр из видео в виде логической переменной и массива
        ret, frame = self.__cap.read()

        # Прочитать json файл
        mask_json = get_json(path_json='data/mask.json')

        if self.flag_line == "mask":
            self.drawing_lines(frame, mask_json[self.flag_line])
            self.drawing_lines(frame, [self.coordinates_line])

        return ret, frame

    def get_show(self, ret: bool = True, frame: UMat = None, name: str = 'Video') -> None:
        """Вывод кадра с видеопотока"""

        if frame is None:
            ret, frame = self._get_frame()

        # Проверить, что кадр существует
        self.__validate_ret(ret)

        # Установка размера просмотра видео на полный экран
        cv2.namedWindow(name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        # Запустить просмотр видео
        cv2.imshow(name, frame)

    @staticmethod
    def _subtract(frame_old: UMat, frame_new: UMat) -> UMat:
        """Нахождение разницы двух кадров"""

        return np.uint8(np.abs(np.int32(frame_old) - np.int32(frame_new)))

    @staticmethod
    def _blur_object(frame: UMat, ksize: int = 5) -> UMat:
        """Размытие контуров объекта"""

        return cv2.GaussianBlur(frame, (ksize, ksize), 0)

    @staticmethod
    def _highlighting_white_object(frame: UMat, thresh: float = 20) -> UMat:
        """Выделение кромки объекта белым цветом"""

        _, threshold = cv2.threshold(frame, thresh, 255, cv2.THRESH_BINARY)
        return threshold

    @staticmethod
    def _morphed(frame: UMat, mode: str, ksize: int = 5, iterations: int = 1) -> UMat:
        """Морфологические фильтры"""

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))

        if mode == 'open':
            # Удаление шума
            morphed = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
        elif mode == 'close':
            # Закрытие внутренних пикселей
            morphed = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel)
        elif mode == 'erode':
            # Размытие контуров объекта
            morphed = cv2.erode(frame, kernel, iterations)
        elif mode == 'dilate':
            # Расширение контуров объекта
            morphed = cv2.dilate(frame, kernel, iterations)
        else:
            # Отправить обратно кадр
            morphed = frame

        return morphed

    @staticmethod
    def _sharpness(frame):
        """Контурная резкость"""

        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        frame = cv2.filter2D(frame, -1, kernel)

        return frame

    @staticmethod
    def _find_contours(frame: UMat, size: int = 200) -> tuple:
        """Создание кортежа контуров (маленьких и больших)."""

        min_area_contour = []
        max_area_counter = []

        contours, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            if area < size:
                min_area_contour.append(contour)
            else:
                max_area_counter.append(contour)

        return min_area_contour, max_area_counter

    def __validate_path_rtsp(self) -> None:
        """Проверка, что ссылка на видео число 0 или строка"""

        if not isinstance(self.__path_rtsp, (str, int)):
            raise ValueError('Ссылка на камеру должна быть rtsp строкой или числом!')

    def __validate_open_video_source(self) -> None:
        """Проверка, что видео открывается"""

        if not self.__cap.isOpened():
            raise ConnectionError('Видео не открывается!')

    @classmethod
    def __validate_ret(cls, ret: bool) -> None:
        """Проверка логической переменной отвечающей за корректность кадра изображения"""

        if not ret:
            raise ValueError('Ошибка кадра!')

    def __validate_ping_ip_address(self) -> None:
        """Проверка, ip адрес из rtsp ссылки пингуется"""

        if isinstance(self.__path_rtsp, str):
            # Поиск ip в RTSP ссылке
            ip = re.findall(
                r"(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)",
                self.__path_rtsp)

            # Если найден хоть один ip адрес в RTSP, то пингануть его
            if len(ip) > 0:
                if subprocess.run(f'ping -n 1 -w 1 {ip[0]}', shell=True, stdout=subprocess.DEVNULL).returncode:
                    raise ConnectionError(f'{ip[0]} не доступен.')
