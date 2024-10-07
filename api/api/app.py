from flask import Flask, jsonify, request

from args import get_args
from files import list_videos
from cache import get_cache_dir

app = Flask(__name__)
args = get_args()
cache_dir = get_cache_dir(args.video_directory)

print(f"Video directory: {args.video_directory}")
print(f"Cache directory: {cache_dir}")

@app.route("/")
def home():
    return jsonify({"message": "UP"})

@app.route("/videos", methods=['GET'])
def get_videos():

    videos = [video.dictify() for video in list_videos(args.video_directory)]
    return jsonify(videos)

if __name__ == '__main__':
    app.run(debug=True)
