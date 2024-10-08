import subprocess
import os
import shutil
import platform

def get_video_length_in_seconds(video_path):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)

def generate_frame_at(video_path, frames_dir, seconds, index):

    width = 320
    # height = -1
    height = 240
    drawtext=f"drawtext=text='{index}':"
    if platform.system().lower() == 'windows':
        drawtext=f"drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='{index}':"
    filters = (
        f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad=320:240:(ow-iw)/2:(oh-ih)/2,"
        f"{drawtext}"
        "fontcolor=white:fontsize=24:"
        "x=20:y=20:"
        "box=1:boxcolor=black@0.5:boxborderw=10"
    )

    # TODO: debug mode that disables quiet?
    command = [
        "ffmpeg", "-y", "-loglevel", "quiet",
        "-ss", str(seconds),
        "-i", video_path,
        "-vframes", "1",
        "-q:v", "2",
        "-f", "image2",
        "-vf", filters,
        "-pix_fmt", "yuvj444p",
        f"image_{str(index).zfill(8)}.jpg"
    ]

    subprocess.run(command, cwd=frames_dir)

def generate_frames(video_path, interval_length, intervals, frames_dir):

    shutil.rmtree(frames_dir, ignore_errors=True)
    os.makedirs(frames_dir, exist_ok=True)
    for i in range(intervals):
        generate_frame_at(video_path, frames_dir, (i-1) * interval_length, i)

def generate_gif(frames_dir, gif_output_path):

    command = [
        "ffmpeg", "-y", "-loglevel", "quiet",
        "-framerate", "4",
        "-i", "image_%08d.jpg",
        "-pix_fmt", "rgb8",
        gif_output_path
    ]

    subprocess.run(command, cwd=frames_dir)
    shutil.rmtree(frames_dir, ignore_errors=True)

def generate_preview(video_path, gif_output_path=None):

    interval_length = 30
    video_length_in_seconds = get_video_length_in_seconds(video_path)
    intervals = int(video_length_in_seconds // interval_length) + 1
    frames_dir = os.path.splitext(video_path)[0] + "-frames"
    if gif_output_path is None:
        gif_output_path = os.path.splitext(video_path)[0] + ".gif"
    
    generate_frames(video_path, interval_length, intervals, frames_dir)
    generate_gif(frames_dir, gif_output_path)

if __name__ == '__main__':
    generate_preview('/Users/jake/Downloads/Peter Pan.MOV')
