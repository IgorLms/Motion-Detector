import cv2
import numpy as np

from video.grey_video import GrayVideoCaptureRTSP


class SubtractionFrame(GrayVideoCaptureRTSP):
    """Класс для вычитания двух кадров"""

    def _get_frame(self) -> cv2.UMat:
        """Вычитание двух кадров"""

        # Получение двх кадров
        frame1 = super()._get_frame()
        frame2 = super()._get_frame()

        # Вычитание двух кадров
        subtract = np.uint8(np.abs(np.int32(frame1) - np.int32(frame2)))

        return subtract


class MotionDetector(GrayVideoCaptureRTSP):
    """Класс детектора движения"""

    def _get_frame(self) -> cv2.UMat:
        """Получить кадр из видео в виде массива"""

        # Получение двх кадров
        frame1 = super()._get_frame()
        frame2 = super()._get_frame()

        # Нахождение разницы двух кадров
        frame = self.__subtract(frame1, frame2)
        # Размытие контуров
        frame = self.__blur_object(frame)
        # Выделение кромки объекта белым цветом
        frame = self.__highlighting_white_object(frame)
        # Расширение области объекта
        frame = self.__extension_object(frame)

        return frame

    @staticmethod
    def __subtract(frame_old: cv2.UMat, frame_new: cv2.UMat) -> cv2.UMat:
        """Нахождение разницы двух кадров"""

        return cv2.absdiff(frame_old, frame_new)

    @staticmethod
    def __blur_object(frame: cv2.UMat) -> cv2.UMat:
        """Размытие контуров объекта"""

        return cv2.GaussianBlur(frame, (5, 5), 0)

    @staticmethod
    def __highlighting_white_object(frame: cv2.UMat) -> cv2.UMat:
        """Выделение кромки объекта белым цветом"""

        _, thresh = cv2.threshold(frame, 20, 255, cv2.THRESH_BINARY)
        return thresh

    @staticmethod
    def __extension_object(frame: cv2.UMat) -> cv2.UMat:
        """Расширение области объекта"""

        return cv2.dilate(frame, None, iterations=2)
