import cv2
from typing import Generator
from elements.FrameElement import FrameElement
import numpy as np


class VideoR:
    def __init__(self, conf) -> None:
        print(conf)
        self.video_pth = conf  # путь до видео
        self.stream = cv2.VideoCapture(self.video_pth)
        # self.frame = frame

    def reader(self) -> Generator[FrameElement, None, None]:
        while True:
            ret, frame = self.stream.read()
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
            # cv2.imshow('video', frame)
            yield FrameElement(self.video_pth, frame)
    #     # Инициализация
    #     cap = cv2.VideoCapture(self.video_pth)

    #     # print(cap)
    #    # Проверка, успешно ли открыто видео
    #     if not cap.isOpened():
    #         print("Не удалось открыть видео")

    #     while True:
    #         # Захват кадра
    #         ret, frame = cap.read()

    #         # Проверка, успешно ли захвачен кадр
    #         if not ret:
    #             print("Не удалось получить кадр")
    #             break

    #         # ресайз
    #         scale = 0.5
    #         frame = cv2.resize(frame, (-1, -1), fx=scale, fy=scale)
    #         print(ret)

    #         # Отображение кадра
    #         cv2.imshow('video', frame)

    #         # Выход из цикла по нажатию клавиши 'q'
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break

    #     # Освобождение ресурсов
    #     cap.release()
    #     cv2.destroyAllWindows()
    #     yield frame


VideoR('aurora.mp4')
# v.reader(config='aurora.mp4')
