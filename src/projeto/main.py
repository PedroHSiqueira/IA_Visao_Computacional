import cv2
import numpy as np

VIDEO = "./src/videos/cars.mp4"

def main():
    cap = cv2.VideoCapture(VIDEO)
    while True:
        check, frame = cap.read()
        if not check:
            break
        frame = cv2.resize(frame, (640, 480))

        cv2.imshow("frame", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
