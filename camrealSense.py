import pyrealsense2 as rs
import numpy as np
import cv2


class realSense:
    def __init__(self):
        self.SIZE = (640, 480)
        self.FPS = 30
        # Configure depth and color streams
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, self.SIZE[0], self.SIZE[1], rs.format.bgr8, self.FPS)


    def initCamera(self):
        self.pipeline.start(self.config)

    def stopCamera(self):
        self.pipeline.stop()

    def getFrame(self):

        # Wait for a coherent pair of frames: depth and color
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            return []
        color_image = np.asanyarray(color_frame.get_data())

        return color_image


if __name__ == '__main__':
    rl = realSense()
    rl.initCamera()

    try:
        while True:

            color_image = rl.getFrame()
            # Show images

            if not len(color_image):
                continue
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense',color_image)
            key = cv2.waitKey(1)
            if (key & 0xFF) == ord('q'):
                break

    finally:
        rl.stopCamera()
        print('FINISH')

    cv2.destroyAllWindows()
