import hydra
# from nodes.VideoReader import VideoReader
from video import VideoR


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(config) -> None:
    # print(config.video_reader.src)
    VideoR(config.video_reader.src)
    # print()
    # for frame_element in video_reader.process():
    #     cv2.imshow(frame_element)
    # video_reader.process


if __name__ == "__main__":
    main()
