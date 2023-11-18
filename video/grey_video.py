import cv2

from video.video import VideoCaptureRTSP


class GrayVideoCaptureRTSP(VideoCaptureRTSP):
    """Класс для получения чёрно белого изображения"""

    def _get_frame(self) -> cv2.UMat:
        """Преобразовать кадр в черно-белый цвет"""

        return cv2.cvtColor(super()._get_frame(), cv2.COLOR_BGR2GRAY)