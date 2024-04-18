# 00 - Importing Dependencies
import os, cv2

def extract_every_n_frame(current_file_name, video_path, output_dir, n):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Capture the video from the file
    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    saved_frame_count = 0

    while True:
        # Read a frame
        read_successful, frame = cap.read()

        # Break the loop if there are no more frames
        if not read_successful:
            break

        if frame_count % n == 0:
            #output_dir = /Volumes/T7/M7_data/split_raw_tv/tv1-frame1
            frame_path = os.path.join(output_dir, f"{current_file_name}_frame{saved_frame_count}.jpg")
            cv2.imwrite(frame_path, frame)
            saved_frame_count += 1
            print(f"Saved: {frame_path}")

        frame_count += 1

    # Release the video capture object
    cap.release()
    print("Done processing video.")

if __name__ == "__main__":

    base_dir = "/Volumes/T7/M7_data"
    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)
        for file in os.listdir(folder_path):
            video_path = os.path.join(base_dir,folder, file)
            output_dir = os.path.join(base_dir, "split_" + folder)
            extract_every_n_frame(file.replace('.mov', ''), video_path, output_dir, 25)