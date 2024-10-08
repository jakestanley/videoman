import os

from flask import Flask, jsonify, request

from api.args import get_args
from api.cache import get_cache_dir
from api.files import get_videos as fget_videos



args = get_args()
# TODO make sure we don't share redis files, consider using a subdirectory in the cache for those
app = Flask(__name__, static_folder=get_cache_dir(args.video_directory), static_url_path="/assets")

@app.route("/")
def home():
    return jsonify({"message": "UP"})

@app.route("/videos", methods=['GET'])
def get_videos():

    videos = fget_videos()
    # TODO serve static content
    # videos = [video.dictify() for video in list_videos()]
    # return jsonify(videos)
    return jsonify(videos)

def start():
    app.run(debug=False)

if __name__ == '__main__':
    start()
