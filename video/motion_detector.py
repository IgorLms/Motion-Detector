from typing import Union
from cv2 import UMat

import cv2

from services.json_file import get_json
from video.grey_video import GrayVideoCaptureRTSP
from video.video import VideoCaptureRTSP


class SubtractionFrame(GrayVideoCaptureRTSP):
    """Класс для вычитания двух кадров"""

    def _get_frame(self) -> [bool, UMat]:
        """Вычитание двух кадров"""

        # Получение двх кадров
        ret1, frame1 = super()._get_frame()
        ret2, frame2 = super()._get_frame()

        # Создание логической переменной, которая отвечает за корректность двух кадров
        ret = ret1 and ret2

        if ret:
            # Накладывание чёрной маски на кадр видео для исключения детектирования
            frame1 = self.mask_coordinates(frame1, self.mask_json["mask"])
            frame2 = self.mask_coordinates(frame2, self.mask_json["mask"])
            # Нахождение разницы двух кадров
            frame1 = self._subtract(frame1, frame2)
            # Расширение области объекта
            frame1 = self._blur_object(frame1)
            # Закрытие внутренних пикселей
            frame1 = self._morphed(frame=frame1, mode='close', ksize=3)
            # Удаление шума
            frame1 = self._morphed(frame=frame1, mode='open', ksize=3)
            # Выделение кромки объекта белым цветом
            frame1 = self._highlighting_white_object(frame1)
            # Удаление шума
            frame1 = self._morphed(frame=frame1, mode='open', ksize=3)
            # Нарисовать линии
            self.drawing_lines(frame1, self.mask_json["line"])

        return ret, frame1


class VideoBackgroundSubtractorKNN(VideoCaptureRTSP):
    """Алгоритм сегментации фона/переднего плана основанный на K-ближайшей соседней"""

    def __init__(self, path_rtsp: Union[int, str]):
        """Инициализация параметров"""

        # Наследование параметров от базового класса
        super().__init__(path_rtsp)
        # Создание сегментации фона на основе K-ближайшей соседней
        self.__knn = cv2.createBackgroundSubtractorKNN(detectShadows=False)

    def _get_mask_frame(self, mask: cv2.BackgroundSubtractor) -> tuple:
        """Получение сегментации по маске"""

        # Получение кадра из видео
        ret, frame = super()._get_frame()
        # Накладывание чёрной маски на кадр видео для исключения детектирования
        frame = self.mask_coordinates(frame, self.mask_json["mask"])
        # Получение маски для кадра
        frame_mask = mask.apply(frame)
        # Расширение границ
        frame_morphology_close = self._morphed(frame=frame_mask, mode='close', ksize=7)
        # Удаление шума в кадре
        frame_morphology_open = self._morphed(frame=frame_morphology_close, mode='open', ksize=7)
        # Выделение кромки объекта белым цветом
        thresh = self._highlighting_white_object(frame=frame_morphology_open, thresh=180)

        return ret, frame, thresh

    @staticmethod
    def _fill_poly(min_area_contour, max_area_counter, frame):
        """
        Закрашивание маленьких контуров чёрным цветом.
        Создание белого многоугольника по контурам.
        """

        # Создание белого многоугольника по контурам
        for contour in max_area_counter:
            x, y, w, h = cv2.boundingRect(contour)
            frame[y:y + h, x:x + w] = 255

        # Закрашивание маленьких контуров чёрным цветом
        cv2.fillPoly(frame, min_area_contour, (0, 0, 0))
        # Закрашивание многоугольников белым цветом
        cv2.fillPoly(frame, max_area_counter, (255, 255, 255))

    def _mask_frame(self, frame, frame_filter):
        """Заменить белый фон цветным изображением"""

        # Преобразование одноканального изображения в многоканальное путем репликации
        frame_filter_bgr = cv2.cvtColor(frame_filter, cv2.COLOR_GRAY2BGR)
        # Удаление шума в кадре
        frame_morphology_open = self._morphed(frame=frame_filter_bgr, mode='open', ksize=7)
        # Заменить белый фон цветным изображением
        frame_bitwise_and = cv2.bitwise_and(frame, frame_morphology_open)

        return frame_bitwise_and

    def _get_frame(self) -> tuple:
        """Преобразование кадра с использованием KNN и удаление шума в кадре"""

        # Получение сегментации по маске
        ret, frame, frame_filter = self._get_mask_frame(mask=self.__knn)
        # Нахождение контуров
        min_area_contour, max_area_counter = self._find_contours(frame_filter)
        # Закрашивание маленьких контуров чёрным цветом.
        # Создание белого многоугольника по контурам.
        self._fill_poly(min_area_contour, max_area_counter, frame_filter)
        # Заменить белый фон цветным изображением
        frame = self._mask_frame(frame, frame_filter)
        # Нарисовать линии
        self.drawing_lines(frame, self.mask_json["line"])

        return ret, frame
