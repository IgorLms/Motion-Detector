import cv2
import numpy as np

from grey_video import GrayVideoCaptureRTSP


class SubtractionFrame(GrayVideoCaptureRTSP):
    """Класс для вычитания двух кадров"""

    def _get_frame(self) -> [bool, cv2.UMat]:
        """Вычитание двух кадров"""

        # Получение двх кадров
        ret1, frame1 = super()._get_frame()
        ret2, frame2 = super()._get_frame()

        # Создание логической переменной, которая отвечает за корректность двух кадров
        ret = ret1 and ret2

        if ret:
            # Размытие контуров
            frame1 = self.__blur_object(frame1)
            frame2 = self.__blur_object(frame2)
            # Нахождение разницы двух кадров
            frame1 = self.__subtract(frame1, frame2)
            # Расширение области объекта
            frame1 = self.__extension_object(frame1)
            # Выделение кромки объекта белым цветом
            frame1 = self.__highlighting_white_object(frame1)

        return ret, frame1

    @staticmethod
    def __subtract(frame_old: cv2.UMat, frame_new: cv2.UMat) -> cv2.UMat:
        """Нахождение разницы двух кадров"""

        return np.uint8(np.abs(np.int32(frame_old) - np.int32(frame_new)))

    @staticmethod
    def __blur_object(frame: cv2.UMat) -> cv2.UMat:
        """Размытие контуров объекта"""

        return cv2.GaussianBlur(frame, (3, 3), 0)

    @staticmethod
    def __highlighting_white_object(frame: cv2.UMat) -> cv2.UMat:
        """Выделение кромки объекта белым цветом"""

        _, thresh = cv2.threshold(frame, 20, 255, cv2.THRESH_BINARY)
        return thresh

    @staticmethod
    def __extension_object(frame: cv2.UMat) -> cv2.UMat:
        """Расширение области объекта"""

        return cv2.dilate(frame, None, iterations=2)
