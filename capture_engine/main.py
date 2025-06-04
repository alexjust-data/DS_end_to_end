import mss
import cv2
import numpy as np
import time

def main():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Change to [2] or specific region for other screens
        print("Starting screen capture. Press Ctrl+C to stop.")

        while True:
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)

            # Convert BGRA to BGR
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            # Show the screen capture in a window
            cv2.imshow("ATAS Screen - Live Capture", frame)

            # Break loop with 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
