import threading
import time

from flask import Flask, jsonify, request

from api.args import get_args
from api.files import list_videos
from api.cache import get_cache_dir
import signal
import sys

app = Flask(__name__)
args = get_args()
cache_dir = get_cache_dir(args.video_directory)

print(f"Video directory: {args.video_directory}")
print(f"Cache directory: {cache_dir}")

stop_event = threading.Event()

def scan_videos():
    while not stop_event.is_set():
        print("Scanning for new videos...")
        time.sleep(5)

    print("Cleaning up video scan...")

def start_video_scan_thread():
    thread = threading.Thread(target=scan_videos)
    # this allows the thread to complete before shutdown
    thread.daemon = False
    thread.start()
    return thread

def stop_video_scan_thread(signal, frame):
    print("Stopping video scan...")
    stop_event.set()
    # wait for thread to finish
    scan_thread.join()
    print("Video scan stopped.")
    sys.exit(0)

signal.signal(signal.SIGINT, stop_video_scan_thread)
signal.signal(signal.SIGTERM, stop_video_scan_thread)

@app.route("/")
def home():
    return jsonify({"message": "UP"})

@app.route("/videos", methods=['GET'])
def get_videos():

    videos = [video.dictify() for video in list_videos()]
    return jsonify(videos)

if __name__ == '__main__':
    scan_thread = start_video_scan_thread()
    app.run(debug=False)
