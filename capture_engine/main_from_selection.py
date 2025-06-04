import mss
import cv2
import numpy as np
import json
import os

import subprocess

def load_region():
    config_path = "config/region.json"
    if not os.path.exists(config_path):
        print("No region defined. Opening selection tool...")
        subprocess.run(["python", "capture_engine/define_trading_region.py"])
    
    with open(config_path, "r") as f:
        region = json.load(f)
    return region


def main():
    region = load_region()
    print(f"Using region: {region}")

    with mss.mss() as sct:
        while True:
            screenshot = sct.grab(region)
            img = np.array(screenshot)
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            cv2.imshow("Selected Trading Region - Live", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
