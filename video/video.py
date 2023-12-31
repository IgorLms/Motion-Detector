from typing import Union
from PyQt5.QtCore import QThread, pyqtSignal

import numpy as np
import subprocess
import re
import cv2


class VideoCaptureRTSP(QThread):
    """Просмотр камеры по RTSP потоку"""

    # Сигнал передачи видео
    change_pixmap_signal = pyqtSignal(np.ndarray)
    # Сигнал остановки видео
    signal_stop_video = pyqtSignal()

    def __init__(self, path_rtsp: Union[int, str]):
        """Инициализация параметров"""

        # Наследование параметров от класса QThread
        super().__init__()

        # Флаг для управления потоком видео
        self.__run_flag = False

        # Сохранение пути до камеры
        self.__path_rtsp = path_rtsp
        # Валидация пинга IP адреса
        self.__validate_ping_ip_address()
        # Валидация пути видео
        self.__validate_path_rtsp()
        # Определение устройства воспроизведения видео
        self.__cap = cv2.VideoCapture(path_rtsp)
        # Проверка, что видео открывается
        self.__validate_open_video_source()

    def __del__(self):
        """Завершение работы с классом"""

        try:
            # Прекратить обращение к видео, если оно существовало
            self.__cap.release()
        except AttributeError:
            pass
        finally:
            # Уничтожить все открытые окна
            cv2.destroyAllWindows()

    def run(self):
        """Получение изображения """

        # Если run_flag False, то сделать True
        if not self.__run_flag:
            self.__run_flag = True

        # Запуск цикла получения кадров видео
        while self.__run_flag:
            # Получение кадра видео
            ret, frame = self._get_frame()

            if ret:
                # Отправка сигнала о существовании корректного кадра
                self.change_pixmap_signal.emit(frame)
            else:
                # Если кадр некорректный, то остановить цикл и отправить сигнал об остановке просмотра
                self.stop()
                self.signal_stop_video.emit()

        # Прекратить обращение к видео
        self.__cap.release()

    def stop(self):
        """Метод завершения потока получения изображения"""

        # Изменение переменной для остановки цикла
        self.__run_flag = False
        # Блокировка потока
        self.wait()

    def _get_frame(self) -> [bool, cv2.typing.MatLike]:
        """Получить кадр из видео в виде массива"""

        # Получить кадр из видео в виде логической переменной и массива
        ret, frame = self.__cap.read()

        return ret, frame

    def get_show(self, ret: bool = True, frame: cv2.UMat = None, name: str = 'Video') -> None:
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

    def __validate_path_rtsp(self) -> None:
        """Проверка, что ссылка на видео число 0 или строка"""

        if not isinstance(self.__path_rtsp, (str, int)):
            raise ValueError('Ссылка на камеру должна быть rtsp строкой или числом 0 (веб-камера)!')
        elif isinstance(self.__path_rtsp, int) and self.__path_rtsp != 0:
            raise ValueError('Для доступа к веб-камере передайте число 0!')

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
            ip = re.findall("(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)", self.__path_rtsp)

            # Если найден хоть один ip адрес в RTSP, то пингануть его
            if len(ip) > 0:
                if subprocess.run(f'ping -n 1 -w 1 {ip[0]}', shell=True, stdout=subprocess.DEVNULL).returncode:
                    raise ConnectionError(f'{ip[0]} не доступен.')
