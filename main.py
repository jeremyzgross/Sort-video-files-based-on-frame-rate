import os
import shutil
import ffmpeg
import tkinter as tk
from tkinter import filedialog
from constants import BASE_PATH

def get_video_frame_rate(video_path):
    probe = ffmpeg.probe(video_path)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    if video_stream is not None:
        frame_rate = eval(video_stream['avg_frame_rate'])
        return frame_rate
    else:
        return None

def create_frame_rate_directories(video_files):
    frame_rates = set()
    for video_file in video_files:
        video_path = os.path.join(BASE_PATH, video_file)
        frame_rate = get_video_frame_rate(video_path)
        if frame_rate is not None:
            frame_rates.add(frame_rate)

    for frame_rate in frame_rates:
        new_directory = os.path.join(BASE_PATH, f"{frame_rate}fps")
        os.makedirs(new_directory, exist_ok=True)

    return frame_rates

def move_files_to_directories(video_files, frame_rates):
    moved_files = []  # List to store the moved file paths
    for video_file in video_files:
        video_path = os.path.join(BASE_PATH, video_file)
        frame_rate = get_video_frame_rate(video_path)
        if frame_rate is not None:
            src = video_path
            dst = os.path.join(BASE_PATH, f"{frame_rate}fps", video_file)
            shutil.move(src, dst)
            moved_files.append((video_file, dst))
        else:
            print(f"Failed to retrieve frame rate for file: {video_file}")

    # Print the moved file paths
    for video_file, destination_path in moved_files:
        print(f"Moved file: {video_file} -> {destination_path}")

def sort_videos():
    video_files = [filename for filename in os.listdir(BASE_PATH) if filename.endswith((".mp4", ".mov", ".mxf"))]
    frame_rates = create_frame_rate_directories(video_files)
    move_files_to_directories(video_files, frame_rates)

def select_base_path():
    root = tk.Tk()
    root.withdraw()
    base_path = filedialog.askdirectory(title="Select Base Path")
    if base_path:
        global BASE_PATH  # Use the global variable
        BASE_PATH = base_path
        sort_videos()
        print("Video files sorted into frame rate directories.")
    else:
        print("No base path selected.")

if __name__ == '__main__':
    select_base_path()
