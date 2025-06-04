import cv2
import mss
import numpy as np

ref_point = []
cropping = False

def click_and_crop(event, x, y, flags, param):
    global ref_point, cropping
    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]
        cropping = True
    elif event == cv2.EVENT_LBUTTONUP:
        ref_point.append((x, y))
        cropping = False
        cv2.rectangle(param, ref_point[0], ref_point[1], (0, 255, 0), 2)
        cv2.imshow("Select Region", param)

def main():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        img = np.array(sct.grab(monitor))
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        clone = img.copy()
        cv2.namedWindow("Select Region")
        cv2.setMouseCallback("Select Region", click_and_crop, param=img)

        while True:
            cv2.imshow("Select Region", img)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("r"):
                img = clone.copy()
            elif key == ord("c"):
                break

        if len(ref_point) == 2:
            roi = clone[ref_point[0][1]:ref_point[1][1], ref_point[0][0]:ref_point[1][0]]
            cv2.imshow("Captured Region", roi)
            cv2.imwrite("screenshots/selected_region.png", roi)
            cv2.waitKey(0)

        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
