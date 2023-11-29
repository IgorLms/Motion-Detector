import cv2

from grey_video import GrayVideoCaptureRTSP
from motion_detector import SubtractionFrame
from video import VideoCaptureRTSP
from video_background_subtractor import VideoBackgroundSubtractorMOG2, VideoBackgroundSubtractorKNN

# Просмотр видео
video = VideoCaptureRTSP(0)

# Просмотр чёрно белого видео
# video = GrayVideoCaptureRTSP(0)

# Просмотр видео с использованием вычитания двух чёрно белых кадров видео
# video = SubtractionFrame(0)

# Просмотр видео с сегментацией на основе модели Гаусса
# video = VideoBackgroundSubtractorMOG2(0)

# Просмотр видео с сегментацией на основе K-ближайших соседей
# video = VideoBackgroundSubtractorKNN(0)

while True:
    video.get_show()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
