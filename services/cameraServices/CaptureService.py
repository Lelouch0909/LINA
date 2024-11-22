import os
from pprint import pprint
import threading

import cv2


class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.pause_reading = threading.Event()
        self.resume_reading = threading.Event()
        self.save_dir = os.path.abspath("ressources/videos")

        self._context = "initial"
        self._index = 0

    @property
    def get_context(self):
        return (self._context)

    @property
    def get_index(self):
        return self._index

    def create_dir(self, path):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except OSError as exc:
            print(f"OS error: {exc}")

    def launch_video(self):
        self._index = 0
        if not self.cap.isOpened():
            print("Error opening video stream")
            return
        while True:
            if not self.pause_reading.is_set():
                ret, frame = self.cap.read()
                if ret == False:
                    self.cap.release()
                    break
                # cv2.imshow("frame", frame)

                cv2.imwrite(f"{self.save_path}/{self._index}.png", frame)
                pprint(f"Saved frame {self._index} at {self.save_path}")
                self._index += 1
            else:
                self.resume_reading.wait()

    def pause_video(self):
        self.pause_reading.set()
        self.resume_reading.clear()
        pprint("Pausing video")

    def resume_video(self):
        self.pause_reading.clear()
        self.resume_reading.set()
        pprint("Resuming video")

    def change_context(self, context_room):
        self._context = context_room
        self.save_path = os.path.join(self.save_dir, self._context)
        self.create_dir(self.save_path)

