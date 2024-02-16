import cv2

from grey_video import GrayVideoCaptureRTSP
from motion_detector import SubtractionFrame, VideoBackgroundSubtractorKNN
from video import VideoCaptureRTSP

# Просмотр видео
video = VideoCaptureRTSP(0)

# Просмотр чёрно белого видео
# video = GrayVideoCaptureRTSP(0)

# Просмотр видео с использованием вычитания двух чёрно белых кадров видео
# video = SubtractionFrame(0)

# Просмотр видео с использованием детекции движения KNN
# video = VideoBackgroundSubtractorKNN(0)

while True:
    video.get_show()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
