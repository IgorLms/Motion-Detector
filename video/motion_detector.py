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