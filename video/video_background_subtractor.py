from typing import Union

import cv2

from video.video import VideoCaptureRTSP


class VideoBackgroundSubtractor(VideoCaptureRTSP):
    """Класс для алгоритмов сегментации фона/переднего плана"""

    def __init__(self, path_rtsp: Union[int, str]):
        """Инициализация параметров"""

        # Наследование параметров от базового класса
        super().__init__(path_rtsp)
        # Создание структурирующего элемента
        self.__kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def __noise_removal(self, frame: cv2.UMat) -> cv2.UMat:
        """Удаление шума в кадре"""

        return cv2.morphologyEx(frame, cv2.MORPH_OPEN, self.__kernel)

    def _get_mask_frame(self, mask: cv2.BackgroundSubtractor) -> cv2.UMat:
        """Получение сегментации по маске"""

        # Получение кадра из видео
        frame = super()._get_frame()
        # Получение маски для кадра
        frame_mask = mask.apply(frame)
        # Удаление шума в кадре
        frame_morphology = self.__noise_removal(frame_mask)

        return frame_morphology


class VideoBackgroundSubtractorMOG2(VideoBackgroundSubtractor):
    """Алгоритм сегментации фона/переднего плана основанный на модели Гаусса"""

    def __init__(self, path_rtsp: Union[int, str]):
        """Инициализация параметров"""

        # Наследование параметров от базового класса
        super().__init__(path_rtsp)
        # Создание сегментации фона на основе модели Гаусса
        self.__mog_2 = cv2.createBackgroundSubtractorMOG2(detectShadows=False)

    def _get_frame(self) -> cv2.UMat:
        """Преобразование кадра с использованием MOG2 и удаление шума в кадре"""

        return self._get_mask_frame(mask=self.__mog_2)


class VideoBackgroundSubtractorKNN(VideoBackgroundSubtractor):
    """Алгоритм сегментации фона/переднего плана основанный на K-ближайшей соседней"""

    def __init__(self, path_rtsp: Union[int, str]):
        """Инициализация параметров"""

        # Наследование параметров от базового класса
        super().__init__(path_rtsp)
        # Создание сегментации фона на основе K-ближайшей соседней
        self.__knn = cv2.createBackgroundSubtractorKNN(detectShadows=False)

    def _get_frame(self) -> cv2.UMat:
        """Преобразование кадра с использованием KNN и удаление шума в кадре"""

        return self._get_mask_frame(mask=self.__knn)