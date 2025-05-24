import cv2
import numpy as np

VIDEO = "./src/videos/cars.mp4"

def main():
    cap = cv2.VideoCapture(VIDEO)
    while True:
        _, frame = cap.read()

        cv2.imshow("frame", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
