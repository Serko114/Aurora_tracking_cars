import os
import json
import time
import logging
from typing import Generator
import cv2

# from elements.FrameElement import FrameElement
# from elements.VideoEndBreakElement import VideoEndBreakElement

logger = logging.getLogger(__name__)


class VideoReader:
    """Модуль для чтения кадров с видеопотока"""

    def __init__(self, config: dict) -> None:
        self.video_pth = config["src"]  # путь до видео
        logger.info(self.video_pth)
        self.stream = cv2.VideoCapture(self.video_pth)  # чтение видео
        logger.info(self.stream)

        # Чтение данных из файла JSON (информация о координатах въезда и выезда дорог)
        # with open(config["roads_info"], "r") as file:
        #     data_json = json.load(file)

        # # Преобразование данных координат дорог в формат int
        # self.roads_info = {
        #     key: [int(value) for value in values] for key, values in data_json.items()
        # }

    def process(self):  # -> Generator[FrameElement, None, None]:
        # номер кадра текущего видео
        frame_number = 0

        while True:
            # Захват кадра
            ret, frame = self.stream.read()
            # if not ret:
            #     logger.warning(
            #         "Can't receive frame (stream end?). Exiting ...")
            #     if not self.break_element_sent:
            #         self.break_element_sent = True
            #         # отправим VideoEndBreakElement чтобы обозначить окончание потока
            #         yield VideoEndBreakElement(self.video_pth, self.last_frame_timestamp)
            #     break

            # Вычисление timestamp в случае если вытягиваем с видоса или камеры (стартуем с 0 сек)
            #    if type(self.video_pth) == int or "://" in self.video_pth:
            #         # с камеры:
            #         if frame_number == 0:
            #             self.first_timestamp = time.time()
            #         timestamp = time.time() - self.first_timestamp
            #     else:
            #         # с видео:
            #         timestamp = self.stream.get(cv2.CAP_PROP_POS_MSEC) / 1000

            #         # делаем костыль, чтобы не было 0-вых тайстампов под конец стрима, баг cv2
            #         timestamp = (
            #             timestamp
            #             if timestamp > self.last_frame_timestamp
            #             else self.last_frame_timestamp + 0.1
            #         )

            #     # Пропустим некоторые кадры если требуется согласно конфигу
            #     if abs(self.last_frame_timestamp - timestamp) < self.skip_secs:
            #         continue

            #     self.last_frame_timestamp = timestamp

            # ресайз
            scale = 0.5
            frame = cv2.resize(frame, (-1, -1), fx=scale, fy=scale)
            # Отображение кадра
            cv2.imshow(self.video_pth, frame)
            # Выход из цикла по нажатию клавиши 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            frame_number += 1

            yield frame
