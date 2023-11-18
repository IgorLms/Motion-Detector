# Детектор движения

## Суть проекта
Создание приложения для просмотра видео, с возможностью применения фильтра для поиска движения.

## Реализованные фильтры

- Обычный просмотр видео ([VideoCaptureRTSP](video/video.py));
- Просмотр чёрно белого видео ([GrayVideoCaptureRTSP](video/grey_video.py));
- Просмотр видео с использованием вычитания двух чёрно белых кадров видео ([SubtractionFrame](video/motion_detector.py));
- Просмотр видео с сегментацией на основе модели Гаусса ([VideoBackgroundSubtractorMOG2](video/video_background_subtractor.py));
- Просмотр видео с сегментацией на основе K-ближайших соседей ([VideoBackgroundSubtractorKNN](video/video_background_subtractor.py));
- Просмотр видео с использованием детектора движения ([MotionDetector](video/motion_detector.py)).

**Пример**

```python
import cv2
from motion_detector import MotionDetector

# Просмотр видео с использованием детектора движения
video = MotionDetector(0)

while True:
    # Просмотр видео
    video.get_show()
    # Остановка видео при нажатии клавиши q 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
```

*Больше примеров в файле [example.py](video/example.py)*
