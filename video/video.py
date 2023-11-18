from typing import Union

import cv2


class VideoCaptureRTSP:
    """Просмотр камеры по RTSP потоку"""

    def __init__(self, path_rtsp: Union[int, str]):
        """Инициализация параметров"""

        # Сохранение пути до камеры
        self.__path_rtsp = path_rtsp
        # Валидация пути видео
        self.__validate_path_rtsp()
        # Определение устройства воспроизведения видео
        self.__cap = cv2.VideoCapture(path_rtsp)

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

    def _get_frame(self) -> cv2.typing.MatLike:
        """Получить кадр из видео в виде массива"""

        # Проверка, что видео открывается
        self.__validate_open_video_source()
        # Получить кадр из видео в виде логической переменной и массива
        ret, frame = self.__cap.read()
        # Проверить, что кадр существует
        self.__validate_ret(ret)

        return frame

    def get_show(self, frame: cv2.UMat = None, name: str = 'Video') -> None:
        """Вывод кадра с видеопотока"""

        if frame is None:
            frame = self._get_frame()

        cv2.namedWindow(name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

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