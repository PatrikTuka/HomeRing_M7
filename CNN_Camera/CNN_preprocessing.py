# 00 - Import Dependencies
import cv2, os
import numpy as np

def CNN_preprocessor(input_frame):
    resized_image = cv2.resize(input_frame, (170, 130))
    blurred_image = cv2.blur(resized_image,(7, 7))
    return blurred_image

def CNN_preprocess_all(base_in, base_out, categories):
    for label in categories:
        folder_path = os.path.join(base_in, label)

        for file in os.listdir(folder_path):
            in_path = os.path.join(base_in, label, file)
            processed_image = CNN_preprocessor(cv2.imread(in_path))

            out_path = os.path.join(base_in, ("prep_" + label), file)
            cv2.imwrite(out_path, processed_image)

            print(f"[IMG]: {out_path}")


if __name__ == "__main__":
    testing = False

    if testing == True:
        un_processed_frame = "/Volumes/T7/M7/tv/tv10-0001.jpg"

        cv2.imshow("original", cv2.imread(un_processed_frame))
        cv2.waitKey(0)

        returned_frame = CNN_preprocessor(cv2.imread(un_processed_frame))
        cv2.imshow("returned", returned_frame)
        cv2.waitKey(0)

    else:
        CNN_preprocess_all("/Volumes/T7/M7/","/Volumes/T7/M7/", ["speaker", "tv", "lamp"])

