from cv2 import UMat

import cv2

from video.video import VideoCaptureRTSP


class GrayVideoCaptureRTSP(VideoCaptureRTSP):
    """Класс для получения чёрно белого изображения"""

    def _get_frame(self) -> [bool, UMat]:
        """Преобразовать кадр в черно-белый цвет"""

        # Получение кадра с видео
        ret, frame = super()._get_frame()

        if ret:
            # Если кадр корректный, то преобразовать его в чёрно-белый цвет
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        return ret, frame
