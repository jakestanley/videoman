import subprocess
import os
import shutil

def get_video_length_in_seconds(video_path):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)

def generate_frame_at(video_path, frames_dir, seconds, index):

    width = 320
    filters = (
        f"scale={width}:-1,"
        f"drawtext=text='{seconds}':"
        "fontcolor=white:fontsize=24:"
        "x=20:y=20:"
        "box=1:boxcolor=black@0.5:boxborderw=10"
    )

    command = [
        "ffmpeg", 
        "-ss", str(seconds),
        "-i", video_path,
        "-vframes", "1",
        "-q:v", "2",
        "-f", "image2",
        "-vf", filters,
        f"image_{str(index).zfill(8)}.jpg"
    ]

    subprocess.run(command, cwd=frames_dir)

def generate_frames(video_path, interval_length, intervals, frames_dir):

    shutil.rmtree(frames_dir, ignore_errors=True)
    os.makedirs(frames_dir, exist_ok=True)
    for i in range(intervals):
        generate_frame_at(video_path, frames_dir, i * interval_length, i)

def generate_gif(frames_dir, gif_output_path):

    command = [
        "ffmpeg",
        "-framerate", "4",
        "-i", "image_%08d.jpg",
        gif_output_path
    ]

    subprocess.run(command, cwd=frames_dir)

def generate_preview(video_path):
    
    interval_length = 180
    video_length_in_seconds = get_video_length_in_seconds(video_path)
    intervals = int(video_length_in_seconds // interval_length)
    frames_dir = os.path.splitext(video_path)[0] + "-frames"
    gif_output_path = os.path.splitext(video_path)[0] + ".gif"
    
    generate_frames(video_path, interval_length, intervals, frames_dir)
    generate_gif(frames_dir, gif_output_path)

if __name__ == '__main__':
    generate_preview('/Users/jake/Downloads/Peter Pan.MOV')
